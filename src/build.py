#!/usr/bin/env python3
"""Build the static site into out/. Relative URLs work at / and under /INSURE/."""
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, SRC)

from render import REDIRECTS, SITE, pages  # noqa: E402


def split_root_url(url):
    path, query, fragment = url, "", ""
    if "#" in path:
        path, fragment = path.split("#", 1)
        fragment = "#" + fragment
    if "?" in path:
        path, query = path.split("?", 1)
        query = "?" + query
    return path, query, fragment


def to_relative(url, depth):
    if not url.startswith("/") or url.startswith("//"):
        return url
    path, query, fragment = split_root_url(url)
    if path == "/":
        rel = "./" if depth == 0 else "../" * depth
    else:
        rel = ("../" * depth) + path.lstrip("/")
    return rel + query + fragment


def rewrite_srcset(value, depth):
    parts = []
    for item in value.split(","):
        item = item.strip()
        if not item:
            continue
        bits = item.split()
        if bits and bits[0].startswith("/") and not bits[0].startswith("//"):
            bits[0] = to_relative(bits[0], depth)
        parts.append(" ".join(bits))
    return ", ".join(parts)


def relativize_urls(text, depth):
    def repl_attr(m):
        attr, quote, url = m.group(1), m.group(2), m.group(3)
        if url.startswith("/") and not url.startswith("//"):
            url = to_relative(url, depth)
        return f"{attr}={quote}{url}{quote}"

    text = re.sub(
        r'\b(href|src|action|poster|data-src|data-href)=(["\'])([^"\']*)\2',
        repl_attr,
        text,
    )

    def repl_srcset(m):
        attr, quote, val = m.group(1), m.group(2), m.group(3)
        return f"{attr}={quote}{rewrite_srcset(val, depth)}{quote}"

    text = re.sub(r'\b(srcset|imagesrcset|data-srcset)=(["\'])([^"\']*)\2', repl_srcset, text)

    def repl_url(m):
        quote, inner = m.group(1), m.group(2).strip()
        if inner.startswith("/") and not inner.startswith("//"):
            inner = to_relative(inner, depth)
        return f"url({quote}{inner}{quote})"

    text = re.sub(r'url\(\s*(["\']?)([^"\')]+)\1\s*\)', repl_url, text)
    return text


def assert_portable(out_dir):
    bad = []
    for dirpath, _, files in os.walk(out_dir):
        for name in files:
            if not name.endswith((".html", ".css", ".js")):
                continue
            fp = os.path.join(dirpath, name)
            rel = os.path.relpath(fp, out_dir)
            text = open(fp, encoding="utf-8").read()
            if "\u2014" in text or "\u2013" in text:
                bad.append(rel + ": em dash or en dash")
            if name.endswith(".html") and 'name="robots" content="noindex, nofollow"' not in text:
                bad.append(rel + ": missing noindex")
            for i, line in enumerate(text.splitlines(), 1):
                if re.search(r'''(?:href|src|srcset|imagesrcset|action|poster|data-src|data-srcset)\s*=\s*["']/''', line):
                    bad.append(f"{rel}:{i}: root-absolute attribute")
                if re.search(r'''url\(\s*["']?/''', line):
                    bad.append(f"{rel}:{i}: root-absolute url()")
                if 'href="#"' in line or "href='#'" in line:
                    bad.append(f"{rel}:{i}: empty hash link")
    home = open(os.path.join(out_dir, "index.html"), encoding="utf-8").read()
    if "BR-1984615" not in home:
        bad.append("index.html: footer license number missing")
    legal = open(os.path.join(out_dir, "legal", "index.html"), encoding="utf-8").read()
    if "BR-1984615" not in legal:
        bad.append("legal/index.html: missing license number")
    if bad:
        raise SystemExit("portable URL check failed:\n" + "\n".join(bad[:60]))


def resolve_link(html_path, url):
    path = url.split("#", 1)[0].split("?", 1)[0]
    if not path:
        return html_path
    base = os.path.dirname(html_path)
    return os.path.normpath(os.path.join(base, path))


def assert_links(out_dir):
    html_files = []
    for dirpath, _, files in os.walk(out_dir):
        for name in files:
            if name.endswith(".html"):
                html_files.append(os.path.join(dirpath, name))
    missing = []
    attr_re = re.compile(r'''(?:href|src|data-src)=["']([^"']+)["']''')
    set_re = re.compile(r'''(?:srcset|data-srcset)=["']([^"']+)["']''')
    for fp in html_files:
        text = open(fp, encoding="utf-8").read()
        rel = os.path.relpath(fp, out_dir)
        urls = attr_re.findall(text)
        for raw in set_re.findall(text):
            for part in raw.split(","):
                bit = part.strip().split()
                if bit:
                    urls.append(bit[0])
        for url in urls:
            url = url.strip()
            if not url or url.startswith(("mailto:", "tel:", "http://", "https://", "data:")):
                continue
            resolved = resolve_link(fp, url)
            if os.path.isdir(resolved):
                resolved = os.path.join(resolved, "index.html")
            if not os.path.isfile(resolved):
                missing.append(f"{rel} -> {url}")
    if missing:
        raise SystemExit("broken links:\n" + "\n".join(missing[:80]))


REMOVED = (
    "coverage/real-estate/",
    "coverage/hospitality/",
    "coverage/construction/",
    "coverage/professional/",
    "coverage/personal/",
    "checklists/",
    "needs/",
    "quote/",
    "resources/",
    "partners/",
    "switching/",
    "photo-credits/",
    "style-preview/",
    "new-york-building-insurance",
    "new-york-contractor-insurance",
    "new-york-restaurant-insurance",
)


def assert_retired(out_dir):
    """Old URLs may exist only as redirect documents. No other page may link to them."""
    href_re = re.compile(r'''(?:href|src|action)=["']([^"']+)["']''')
    bad = []
    for dirpath, _, files in os.walk(out_dir):
        for name in files:
            if not name.endswith(".html"):
                continue
            fp = os.path.join(dirpath, name)
            rel = os.path.relpath(fp, out_dir).replace("\\", "/")
            text = open(fp, encoding="utf-8").read()
            if 'http-equiv="refresh"' in text:
                continue
            for url in href_re.findall(text):
                path = url.split("#", 1)[0].split("?", 1)[0]
                if any(piece in path for piece in REMOVED):
                    bad.append(f"{rel} -> {url}")
    if bad:
        raise SystemExit("links to removed pages:\n" + "\n".join(bad[:40]))


def write_sitemap(built):
    locs = []
    for rel in built:
        if rel in REDIRECTS or rel == "404.html" or not rel.endswith("index.html"):
            continue
        if rel == "index.html":
            locs.append(SITE + "/")
        else:
            locs.append(SITE + "/" + rel[: -len("index.html")])
    body = "\n".join(f"  <url><loc>{loc}</loc></url>" for loc in locs)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + body
        + "\n</urlset>\n"
    )
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(xml)


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(ROOT, "public"), OUT)
    for dirpath, _, files in os.walk(OUT):
        for name in files:
            if not name.endswith(".css"):
                continue
            fp = os.path.join(dirpath, name)
            depth = os.path.relpath(fp, OUT).count(os.sep)
            text = open(fp, encoding="utf-8").read()
            new = relativize_urls(text, depth)
            if new != text:
                open(fp, "w", encoding="utf-8").write(new)
    built = pages()
    for rel, doc in built.items():
        fp = os.path.join(OUT, rel)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, "w", encoding="utf-8").write(relativize_urls(doc, rel.count("/")))
    open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8").write("User-agent: *\nDisallow: /\n")
    write_sitemap(built)
    assert_portable(OUT)
    assert_links(OUT)
    assert_retired(OUT)
    print("built", len(built), "pages")


if __name__ == "__main__":
    main()
