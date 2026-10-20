# -*- coding: utf-8 -*-
"""HTML for the SimpleINSURE static site. Root-absolute URLs are rewritten at build time."""
import html as html_lib
import json
import os
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHONE = "(516) 226-7969"
TEL = "tel:+15162267969"
EMAIL = "info@simpleinsure.co"
MAIL = "mailto:info@simpleinsure.co"
ADDR = "900 Stewart Ave Ste 210, Garden City, NY 11530"
SITE = "https://www.simpleinsure.co"
ARROW = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

CRED = json.load(open(os.path.join(ROOT, "src", "photo_credits.json"), encoding="utf-8"))
for _c in CRED.values():
    _c["artist"] = _c["artist"].replace("firstdorsal.eu", "").strip()
    if "unsplash.com" not in _c.get("page", "") and "commons.wikimedia.org" not in _c.get("page", ""):
        _title = _c["title"].replace(" ", "_")
        _c["page"] = "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(_title, safe="()'-._~")

DIMS = {
    "hero": (1600, 1067),
    "estate": (1600, 1067),
    "hospitality": (1600, 1067),
    "construction": (1600, 1067),
    "professional": (1600, 1067),
    "personal": (1600, 1067),
    "facade": (1600, 1404),
    "counter": (1600, 2400),
}


def h(value):
    return html_lib.escape(str(value), quote=True)


# Same file family at every width. The query busts a cached estate-800 that was a different photograph.
PHOTO_V = "6"


def photo_src(key, width, ext="webp"):
    return f"/photos/{key}-{width}.{ext}?v={PHOTO_V}"


def pic(key, eager=False, sizes="(max-width: 860px) 100vw, 46vw", alt=None):
    c = CRED[key]
    w, height = DIMS[key]
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    alt_text = c["alt"] if alt is None else alt
    srcset = ", ".join(f"{photo_src(key, width)} {width}w" for width in (800, 1200, 1600))
    avif = ", ".join(f"{photo_src(key, width, 'avif')} {width}w" for width in (800, 1200, 1600))
    return (
        f'<picture><source type="image/avif" srcset="{avif}" sizes="{sizes}">'
        f'<img src="{photo_src(key, 800)}" srcset="{srcset}" sizes="{sizes}" '
        f'alt="{h(alt_text)}" width="{w}" height="{height}" {load}></picture>'
    )


def cred(key):
    c = CRED[key]
    # One inline span so spaces survive if a parent is a flex container.
    return (
        '<span class="cap">Photograph by '
        f'<a href="{h(c["page"])}" rel="noopener">{h(c["artist"])}</a>, '
        f'<a href="{h(c["license_url"])}" rel="noopener">{h(c["license"])}</a></span>'
    )


def figure_block(key, sizes, eager=False, cls="photo-block"):
    return f'<figure class="{cls}"><div class="shot">{pic(key, eager=eager, sizes=sizes)}</div></figure>'


def photo_attrs(key):
    c = CRED[key]
    srcset = f"/photos/{key}-800.webp 800w, /photos/{key}-1200.webp 1200w, /photos/{key}-1600.webp 1600w"
    return (
        f'data-src="/photos/{key}-1200.webp" data-srcset="{srcset}" data-alt="{h(c["alt"])}" '
        f'data-artist="{h(c["artist"])}" data-page="{h(c["page"])}" data-license="{h(c["license"])}" '
        f'data-license-url="{h(c["license_url"])}"'
    )


def schema(path):
    data = {
        "@context": "https://schema.org",
        "@type": "InsuranceAgency",
        "name": "SimpleINSURE Brokerage LLC",
        "alternateName": "SimpleINSURE",
        "url": SITE + "/",
        "logo": SITE + "/img/simpleinsure-wordmark.png",
        "image": SITE + "/img/og.png",
        "telephone": "+1-516-226-7969",
        "email": EMAIL,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "900 Stewart Ave, Ste 210",
            "addressLocality": "Garden City",
            "addressRegion": "NY",
            "postalCode": "11530",
            "addressCountry": "US",
        },
        "areaServed": [
            {"@type": "AdministrativeArea", "name": "Nassau County"},
            {"@type": "AdministrativeArea", "name": "Suffolk County"},
            {"@type": "City", "name": "New York City"},
            {"@type": "State", "name": "New York"},
        ],
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "09:00",
            "closes": "17:00",
        },
    }
    if path == "/legal/":
        data["hasCredential"] = {
            "@type": "EducationalOccupationalCredential",
            "credentialCategory": "license",
            "name": "New York insurance broker license BR-1984615",
            "recognizedBy": {"@type": "GovernmentOrganization", "name": "New York State Department of Financial Services"},
        }
    return json.dumps(data, ensure_ascii=True)


COVER = [
    ("/coverage/#real-estate", "Real estate", "Buildings and landlords", "estate"),
    ("/coverage/#hospitality", "Hospitality", "Restaurants and bars", "hospitality"),
    ("/coverage/#construction", "Contractors", "Trades and job sites", "construction"),
    ("/coverage/#professional", "Offices", "Professional firms", "professional"),
    ("/coverage/#personal", "Personal", "Household, home, and auto", "personal"),
]
INDUSTRY_NAV = [
    ("/restaurant-insurance/", "Restaurant insurance"),
    ("/contractor-insurance/", "Contractor insurance"),
    ("/building-owner-insurance/", "Building insurance"),
]
FIRM = [
    ("/about/", "The firm", "The practice"),
    ("/client-center/", "Client service", "What to expect"),
    ("/switching/", "Switching brokers", "The order of work"),
    ("/partners/", "Partners", "Attorneys, managers, CPAs"),
    ("/resources/", "Resources", "Glossary and guides"),
]


def nav_links(items, current):
    out = []
    for href, title, sub, *_rest in items:
        cur = ' aria-current="page"' if current == href else ""
        out.append(f'<a href="{href}"{cur}><b>{h(title)}</b><small>{h(sub)}</small></a>')
    return "".join(out)


def sheet_links(current):
    parts = ['<a href="/coverage/">Coverage</a>', '<div class="sheet-subs">']
    for href, title, _sub, *_r in COVER:
        parts.append(f'<a class="sub" href="{href}">{h(title)}</a>')
    parts.append("</div>")
    for href, label in INDUSTRY_NAV:
        parts.append(f'<a class="sub" href="{href}">{h(label)}</a>')
    for href, label in (
        ("/client-center/", "Client Center"),
        ("/about/", "Firm"),
        ("/contact/", "Contact"),
    ):
        cur = ' aria-current="page"' if current == href else ""
        parts.append(f'<a href="{href}"{cur}>{label}</a>')
    return "".join(parts)


def header(current):
    def top(href, label):
        cur = ' aria-current="page"' if current == href else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="bar">
    <a class="logo" href="/" aria-label="SimpleINSURE home"><img src="/simpleinsure-wordmark.png" alt="SimpleINSURE" width="1684" height="360"></a>
    <nav class="nav-desk" aria-label="Primary">
      {top("/coverage/", "Coverage")}
      {top("/client-center/", "Client Center")}
      {top("/about/", "Firm")}
      {top("/contact/", "Contact")}
    </nav>
    <div class="nav-actions">
      <a class="phone-full" href="{TEL}">{PHONE}</a>
      <a class="btn btn-sm" href="/policy-review/">Request a review</a>
      <button class="nav-btn" type="button" aria-expanded="false" aria-controls="sheet"><span class="nav-ic" aria-hidden="true"></span><span class="sr">Menu</span></button>
    </div>
  </div>
</header>
<div class="sheet" id="sheet" hidden>
  <nav aria-label="Mobile">{sheet_links(current)}</nav>
  <div class="sheet-cta"><a class="btn" href="/policy-review/">Request a review</a><a href="{TEL}">{PHONE}</a><a href="{MAIL}">{EMAIL}</a></div>
</div>'''


def footer():
    cov = "".join(f'<li><a href="{href}">{h(title)}</a></li>' for href, title, _s, *_r in COVER)
    cov += "".join(f'<li><a href="{href}">{h(title)}</a></li>' for href, title in INDUSTRY_NAV)
    return f'''<footer class="site-footer">
  <div class="wrap foot-grid">
    <div>
      <a class="logo" href="/" aria-label="SimpleINSURE home"><img src="/simpleinsure-wordmark.png" alt="SimpleINSURE" width="1684" height="360"></a>
      <p class="addr">Commercial and personal insurance.</p>
      <p class="addr">{ADDR}</p>
    </div>
    <div><h2>Coverage</h2><ul>{cov}</ul></div>
    <div><h2>Advisory</h2><ul>
      <li><a href="/policy-review/">Policy review</a></li>
      <li><a href="/client-center/">Client Center</a></li>
      <li><a href="/contact/">Contact</a></li>
    </ul></div>
    <div><h2>Firm</h2><ul>
      <li><a href="/about/">The firm</a></li>
    </ul></div>
    <div><h2>Office</h2><ul>
      <li><a href="{TEL}">{PHONE}</a></li>
      <li><a href="{MAIL}">{EMAIL}</a></li>
    </ul></div>
  </div>
  <div class="wrap legal-line">
    <span>© 2026 SimpleINSURE Brokerage LLC, licensed New York property and casualty insurance broker, NY DFS License No. BR-1984615. Coverage descriptions are general summaries. The issued policy governs. <a href="/legal/">Licenses and disclosures</a>.</span>
  </div>
  <div class="m-foot m-only">
    <div class="wrap">
      <a class="logo" href="/" aria-label="SimpleINSURE home"><img src="/simpleinsure-wordmark.png" alt="SimpleINSURE" width="1684" height="360"></a>
      <div class="m-foot-cols">
        <div><h2>Coverage</h2><ul>{cov}</ul></div>
        <div><h2>Advisory</h2><ul>
          <li><a href="/policy-review/">Policy review</a></li>
          <li><a href="/client-center/">Client Center</a></li>
          <li><a href="/contact/">Contact</a></li>
        </ul></div>
        <div><h2>Firm</h2><ul>
          <li><a href="/about/">The firm</a></li>
        </ul></div>
        <div><h2>Office</h2><ul>
          <li><a href="{TEL}">{PHONE}</a></li>
          <li><a href="{MAIL}">{EMAIL}</a></li>
          <li>{ADDR}</li>
        </ul></div>
      </div>
      <p class="m-legal">© 2026 SimpleINSURE Brokerage LLC, licensed New York property and casualty insurance broker, NY DFS License No. BR-1984615. Coverage descriptions are general summaries. The issued policy governs. <a href="/legal/">Licenses and disclosures</a>.</p>
    </div>
  </div>
</footer>'''


def document(title, desc, path, main, current=None, canonical=None, extra="", show_footer=True):
    cur = path if current is None else current
    canon = SITE + (path if canonical is None else canonical)
    if path == "/":
        canon = SITE + "/"
    cinematic = path in ("/", "/style-preview/")
    preload = '<link rel="preload" href="/fonts/newsreader.woff2" as="font" type="font/woff2" crossorigin>'
    if cinematic:
        preload += f'''
<link rel="preload" as="image" href="{photo_src("hero", 800)}" imagesrcset="{photo_src("hero", 800)} 800w, {photo_src("hero", 1200)} 1200w, {photo_src("hero", 1600)} 1600w" imagesizes="100vw" fetchpriority="high">'''
    if path == "/coverage/":
        preload += f'''
<link rel="preload" as="image" href="{photo_src("estate", 800)}" imagesrcset="{photo_src("estate", 800)} 800w, {photo_src("estate", 1200)} 1200w, {photo_src("estate", 1600)} 1600w" imagesizes="100vw" fetchpriority="high">'''
    body = "page-home" if cinematic else "page-inner"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#061018" media="(max-width: 1023px)">
<title>{h(title)}</title>
<meta name="description" content="{h(desc)}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{h(canon)}">
<link rel="icon" href="/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="{h(title)}">
<meta property="og:description" content="{h(desc)}">
<meta property="og:url" content="{h(canon)}">
<meta property="og:image" content="{SITE}/img/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{h(title)}">
<meta name="twitter:description" content="{h(desc)}">
<meta name="twitter:image" content="{SITE}/img/og.png">
<link rel="preload" href="/fonts/franklin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/site.css?v=26">
<style>
.m-only{{display:none}}
@media (max-width:980px){{
  .site-header{{position:fixed !important;top:calc(12px + env(safe-area-inset-top)) !important;left:0 !important;right:0 !important;padding-top:0 !important;z-index:80 !important;transform:translate3d(0,var(--header-shift,0px),0)}}
  .site-header:before{{content:"";position:absolute;left:0;right:0;bottom:100%;height:calc(12px + env(safe-area-inset-top));background:transparent;pointer-events:none}}
  html.veil .site-header:before{{background:#fff;height:calc(12px + env(safe-area-inset-top));top:auto;bottom:100%}}
  .h-pin{{height:auto !important}}
  .h-sticky{{position:static !important;height:auto !important;display:block !important;overflow:visible !important}}
  .h-intro{{width:auto !important;display:block !important;padding:48px 20px 16px !important;box-sizing:border-box !important}}
  .h-track{{display:block !important;transform:none !important;height:auto !important;width:auto !important}}
  .slide{{position:relative !important;display:block !important;width:100% !important;height:72vh !important;min-height:420px !important;overflow:hidden !important;color:#fff !important;flex:none !important}}
  .slide img{{position:absolute !important;inset:0 !important;width:100% !important;height:100% !important;max-width:none !important;object-fit:cover !important}}
  .slide-shade{{position:absolute !important;inset:0 !important}}
  .slide-copy{{position:absolute !important;left:20px !important;right:20px !important;bottom:22px !important;z-index:2 !important;color:#fff !important}}
  .slide-copy strong,.slide-copy small{{display:block !important;color:#fff !important}}
  .slide-copy small{{margin-top:8px !important}}
}}
</style>
<link rel="stylesheet" href="/mobile.css?v=10">
<script>document.documentElement.classList.toggle("scrolled",(window.scrollY||0)>8);if(matchMedia("(max-width:980px)").matches)document.documentElement.classList.add("is-mobile");if(!matchMedia("(prefers-reduced-motion: reduce)").matches)document.documentElement.classList.add("motion")</script>
{preload}
<script type="application/ld+json">{schema(path)}</script>
{extra}
</head>
<body class="{body}">
{header(cur)}
<main id="main">{main}</main>
{footer() if show_footer else ""}
<script src="/site.js?v=14" defer></script>
<script>
addEventListener("load",function(){{
  var s=document.createElement("script");
  s.async=true;
  s.src="https://www.googletagmanager.com/gtag/js?id=G-ZQH2G4PPLQ";
  document.head.appendChild(s);
  window.dataLayer=window.dataLayer||[];
  function gtag(){{dataLayer.push(arguments);}}
  gtag("js",new Date());
  gtag("config","G-ZQH2G4PPLQ");
}});
</script>
</body>
</html>'''


def cinematic_sections(eager=False):
    blurbs = {
        "estate": "Apartment and commercial buildings.",
        "hospitality": "Restaurants, bars, and cafes.",
        "construction": "Trades and contractors.",
        "professional": "Offices, shops, and firms.",
        "personal": "Home, auto, and umbrella.",
    }
    slides = []
    for i, (href, title, _sub, key) in enumerate(COVER, 1):
        slides.append(
            f'<div class="slide rise-photo{" slide-hospitality" if key == "hospitality" else ""}">'
            f'{pic(key, eager=eager, sizes="(max-width: 980px) 100vw, 22vw")}'
            f'<span class="slide-shade" aria-hidden="true"></span>'
            f'<a class="slide-hit" href="{href}"><span class="sr">{h(title)}</span></a>'
            f'<span class="slide-copy" data-rise><em>{i:02d}</em><strong>{h(title)}</strong> <small>{h(blurbs[key])}</small></span>'
            f'</div>'
        )
    return f'''
<section class="hero" aria-label="Introduction">
  <div class="hero-media">
    <div class="ken">{pic("hero", eager=True, sizes="100vw")}</div>
    <div class="hero-shade" aria-hidden="true"></div>
  </div>
  <div class="hero-copy wrap">
    <h1 class="rise"><span class="line"><span>Insurance,</span></span><span class="line"><span>made simple.</span></span></h1>
    <h2 class="place-line">Commercial and personal insurance. Garden City, Long Island, and New York City.</h2>
    <p class="lede">Send us your policy. We'll walk you through it in plain English.</p>
    <div class="cta-row">
      <a class="btn btn-light magnet" href="/policy-review/">Request a review {ARROW}</a>
    </div>
  </div>
  <a class="scroll-cue" href="#practices"><span class="sr">Practices</span><i aria-hidden="true"></i></a>
</section>
<section class="h-pin" id="practices" aria-labelledby="practices-h">
  <div class="h-sticky">
    <div class="h-intro">
      <div class="h-copy">
        <h2 class="rise" id="practices-h"><span class="line"><span>Five</span></span><span class="line"><span>practices.</span></span></h2>
      </div>
    </div>
    <div class="h-track">{''.join(slides)}</div>
  </div>
</section>
'''


def mobile_home():
    tiles = []
    for i, (href, title, _sub, key) in enumerate(COVER):
        wide = " m-tile-wide" if i == len(COVER) - 1 else ""
        tiles.append(
            f'<a class="m-tile{wide}" href="{href}">'
            f'{pic(key, sizes="(max-width: 768px) 46vw, 240px")}'
            f"<span>{h(title)}</span></a>"
        )
    practices = []
    for i, (href, title, _sub, _key) in enumerate(COVER, 1):
        practices.append(
            f'<li><a href="{href}"><span>{i:02d}</span><strong>{h(title)}</strong></a></li>'
        )
    steps = [
        ("We read it", "Your policy, forms, and endorsements."),
        ("We tell you", "If it's right, we say so."),
        ("We shop it", "Only when there's a reason to."),
        ("We switch it", "Dates lined up."),
    ]
    step_html = "".join(
        f'<li><div><span>{i:02d}</span><div><strong>{h(title)}</strong><em>{h(text)}</em></div></div></li>'
        for i, (title, text) in enumerate(steps, 1)
    )
    faqs = [
        ("Read the policy before a broker of record letter", "We read what you have before anyone is asked to sign a broker of record letter."),
        ("Say so when it should stay", "If the current program is already right, we say so."),
        ("Do not cut coverage to win on price", "A lower premium is not a reason to thin the program. Limits, valuation, and exclusions have to match the account."),
        ("Stay after it is bound", "The same broker stays with certificates, renewals, and a claim."),
    ]
    faq_html = "".join(f"<details><summary>{h(q)}</summary><p>{h(a)}</p></details>" for q, a in faqs)
    practices_block = f'''
<div class="m-home m-only">
<section class="m-block">
  <div class="wrap">
    <h2>Five<span class="b">practices.</span></h2>
    <div class="m-tiles">{''.join(tiles)}</div>
  </div>
</section>
</div>
'''
    steps_block = f'''
<div class="m-home m-only">
<section class="m-block" style="padding-top:8px">
  <div class="wrap">
    <h2>How it<span class="b">works.</span></h2>
    <ol class="m-num m-num-notes">{step_html}</ol>
  </div>
</section>
</div>
'''
    return practices_block, steps_block


def client_result():
    return f'''<section class="client-result client-result-grays" id="grays" aria-labelledby="grays-h">
  <figure class="result-photo rise-photo only-1024">{pic("counter", sizes="(min-width: 1024px) 58vw, 100vw", alt="Gray's Papaya storefront at 72nd Street and Broadway")}<figcaption class="result-rep">Gray's Papaya, 72nd and Broadway. Photo: Kidfly182 / <a href="https://commons.wikimedia.org/wiki/File:Upper_West_Side_August_2022_073.jpg">Wikimedia Commons</a>, <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>, cropped.</figcaption></figure>
  <div class="wrap">
    <p class="result-label" data-rise>Client result</p>
    <p class="result-name" data-rise>Gray's Papaya</p>
    <h2 id="grays-h" data-rise><span class="desk-break">More coverage for</span> a New York original.</h2>
    <p class="result-line" data-rise><span>Same liability limits.</span> <span>A higher umbrella limit.</span> <span>Employment practices coverage added.</span></p>
    <p class="result-body" data-rise>Gray's Papaya has served hot dogs at 72nd and Broadway for years. We reviewed the full insurance program, took it to market, and put a broader program in place.</p>
    <p class="result-foot" data-rise>Every account is different. Terms depend on underwriting.</p>
  </div>
</section>'''


def home():
    m_top, m_steps = mobile_home()
    return document(
        "Commercial Insurance Broker in Garden City | SimpleINSURE",
        "Commercial and personal insurance broker in Garden City, for Long Island, Nassau, and New York City.",
        "/",
        cinematic_sections() + m_top + client_result() + m_steps + f'''
<section class="section work" id="work" aria-labelledby="work-h">
  <div class="wrap work-grid">
    <div class="work-intro">
      <h2 class="rise" id="work-h" data-rise><span class="line"><span>How it</span></span><span class="line"><span>works.</span></span></h2>
      <p data-rise>We read your policy before you sign anything.</p>
    </div>
    <ol class="work-steps">
      <li data-rise><div><h3>We read it</h3><p>Your policy, forms, and endorsements.</p></div></li>
      <li data-rise><div><h3>We tell you</h3><p>If it's right, we say so.</p></div></li>
      <li data-rise><div><h3>We shop it</h3><p>Only when there's a reason to.</p></div></li>
      <li data-rise><div><h3>We switch it</h3><p>Dates lined up.</p></div></li>
    </ol>
  </div>
</section>
<section class="close" aria-labelledby="close-h">
  <div class="hero-media">
    <div class="ken">{pic("personal", sizes="100vw")}</div>
    <div class="hero-shade" aria-hidden="true"></div>
  </div>
  <div class="wrap close-inner">
    <h2 class="rise" id="close-h" data-rise><span class="line"><span>Bring the policy</span></span><span class="line"><span><em>you have.</em></span></span></h2>
    <p data-rise>We'll walk you through it, even if the answer is to keep it.</p>
    <div class="cta-row">
      <a class="btn btn-light magnet" href="/policy-review/">Request a review {ARROW}</a>
      <a class="btn btn-line magnet" href="{TEL}">{PHONE}</a>
    </div>
  </div>
</section>
''',
    )


def style_preview():
    return document(
        "Style preview | SimpleINSURE",
        "A preview of the SimpleINSURE home: the opening photograph, the practices, and a case study.",
        "/style-preview/",
        cinematic_sections(eager=True) + '''
<section class="method" id="method" aria-labelledby="method-h">
  <div class="wrap method-grid">
    <div class="method-lead">
      <h2 class="rise" id="method-h"><span class="line"><span>Read it first.</span></span></h2>
      <p class="lede">We read what you have before anyone is asked to sign a broker of record letter.</p>
    </div>
    <div class="method-steps">
      <p><b>Read.</b> Declarations, forms, and the endorsements behind them.</p>
      <p><b>Say so.</b> If the current program is already right, we say so.</p>
      <p><b>Market.</b> Only when there is a reason to move the account.</p>
      <p><b>Hand over.</b> Dates, certificates, and the renewal calendar.</p>
    </div>
  </div>
</section>
''',
        current="/style-preview/",
        show_footer=False,
    )


LINES = [
    ("real-estate", "A building or a real estate schedule"),
    ("hospitality", "A restaurant, bar, or cafe"),
    ("construction", "A contracting or trade business"),
    ("professional", "An office, retail, or professional firm"),
    ("personal", "Home, auto, or an umbrella"),
    ("unsure", "I am not sure yet"),
]


def field(fid, label, kind="text", options=None, required=False, show=None, full=False, need=None, attrs="", hint=""):
    show_attr = f' data-for="{show}"' if show else ""
    cls = "field full" if full or kind == "textarea" else "field"
    req = " required" if required else ""
    need_attr = f' data-need="{need}"' if need else ""
    if kind == "textarea":
        control = f'<textarea id="{fid}" name="{fid}"{req}{need_attr}></textarea>'
    elif kind == "select":
        opts = '<option value="">Select</option>' + "".join(f"<option>{h(o)}</option>" for o in options or [])
        control = f'<select id="{fid}" name="{fid}"{req}{need_attr}>{opts}</select>'
    else:
        control = f'<input id="{fid}" name="{fid}" type="{kind}"{req}{need_attr} {attrs}>'
    note = f'<p class="quiet">{h(hint)}</p>' if hint else ""
    return f'<div class="{cls}"{show_attr}><label for="{fid}">{h(label)}</label>{control}{note}</div>'


def line_choices(prefix=""):
    bits = []
    for val, label in LINES:
        fid = prefix + "line-" + val
        bits.append(
            f'<label class="choice" for="{fid}"><input id="{fid}" type="radio" name="line" value="{val}" required>'
            f"<span>{h(label)}</span></label>"
        )
    return "".join(bits)


def coverage_groups():
    groups = {
        "real-estate": ["Building property", "Loss of rents", "General liability", "Umbrella", "Workers compensation", "Ordinance or law", "Equipment breakdown"],
        "hospitality": ["Property and equipment", "Business income", "General liability", "Liquor liability", "Workers compensation", "Umbrella", "Employment practices", "Spoilage or equipment breakdown"],
        "construction": ["General liability", "Workers compensation", "Commercial auto", "Umbrella", "Inland marine", "Additional insured wording", "Waiver of subrogation"],
        "professional": ["Package or business owners policy", "Professional liability", "Cyber liability", "Workers compensation", "Hired and non-owned auto", "Umbrella"],
        "personal": ["Homeowners or renters", "Auto", "Personal umbrella", "Valuable articles", "Rental dwelling"],
        "unsure": ["Help me decide"],
    }
    blocks = []
    for key, items in groups.items():
        chips = []
        for i, label in enumerate(items):
            fid = f"cov-{key}-{i}"
            chips.append(f'<label for="{fid}"><input id="{fid}" name="{fid}" type="checkbox" checked> {h(label)}</label>')
        blocks.append(f'<div class="field full" data-for="{key}"><div class="chips">{"".join(chips)}</div></div>')
    return "".join(blocks)


def contact_fields(prefix):
    return (
        field(prefix + "name", "Full name", required=True, full=True, attrs='autocomplete="name"')
        + field(prefix + "biz", "Business or named insured", attrs='autocomplete="organization"')
        + field(prefix + "email", "Email", kind="email", need="email", attrs='autocomplete="email"')
        + field(prefix + "phone", "Phone", kind="tel", need="phone", attrs='autocomplete="tel"')
        + field(prefix + "reach", "Best way to reply", kind="select", options=["Phone", "Email", "Either"])
        + field(prefix + "notes", "Anything we should know", kind="textarea", full=True)
    )


def done_block():
    return f'''<div class="done" hidden>
      <h2>Your note is ready to send.</h2>
      <p class="lede">An email draft to <a href="{MAIL}">{EMAIL}</a> should be open. If not, use the button below. Email is not encrypted, so leave out Social Security, driver's license, birth date, and bank or card numbers, including in attachments, or call {PHONE}.</p>
      <div class="summary"></div>
      <div class="done-actions">
        <a class="btn" data-mailto href="{MAIL}">Open the email draft <span class="arr" aria-hidden="true">→</span></a>
        <button type="button" class="btn-ghost" data-copy>Copy the summary</button>
        <a class="btn-ghost" href="{TEL}">Call {PHONE}</a>
      </div>
    </div>'''


def wizard(subject, final, steps):
    return f'''<form class="wizard" method="post" data-subject="{h(subject)}" data-final="{h(final)}" novalidate>
      <p class="progress"><span data-steplabel>Start</span><span data-stepcount></span></p>
      <div class="meter" aria-hidden="true"><i></i></div>
      {steps}
      <p class="form-error" role="alert" hidden></p>
      <div class="wizard-nav"><button type="button" class="btn-ghost" data-back hidden>Back</button><button type="submit" class="btn" data-next>Continue</button></div>
      {done_block()}
    </form>'''


def aside():
    return f'''<aside class="aside">
      <div class="panel"><h2>What happens next</h2>
        <p>A broker reads what you sent and replies by phone or email.</p>
        <div class="row"><span>Call</span><a href="{TEL}">{PHONE}</a></div>
        <div class="row"><span>Email</span><a href="{MAIL}">{EMAIL}</a></div>
      </div>
    </aside>'''


def page_head(kicker, title, lede="", cls="", lede_cls="", place=""):
    lead_cls = "lede" + (f" {lede_cls}" if lede_cls else "")
    place_html = f'<h2 class="place-line">{h(place)}</h2>' if place else ""
    lead = f'<p class="{lead_cls}">{h(lede)}</p>' if lede else ""
    eye = f'<p class="kicker m-only">{h(kicker)}</p>' if kicker else ""
    extra = f" {cls}" if cls else ""
    return f'<header class="page-head{extra}"><div class="wrap">{eye}<h1 class="rise"><span class="line"><span>{h(title)}</span></span></h1>{place_html}{lead}</div></header>'


def continue_to(links):
    cards = "".join(
        f'<a href="{href}"><b>{h(title)}</b><em>{h(text)}</em></a>'
        for href, _n, title, text in links
    )
    return f'<nav class="next" aria-label="Continue"><div class="wrap">{cards}</div></nav>'


INDUSTRIES = [
    {
        "slug": "real-estate",
        "key": "estate",
        "nav": "Real estate",
        "title": "Real Estate and Building Insurance | SimpleINSURE",
        "desc": "Insurance for apartment, mixed-use, and commercial buildings. Property, liability, umbrella, and the wording lenders ask for.",
        "h1": "Insurance for the building, the schedule, and the lender.",
        "lede": "Apartment, mixed-use, and commercial buildings. One or a whole portfolio.",
        "essay": [
            "A building account is decided by the loan, the tenants, and the condition of the property. We start with the address or the schedule, the construction, the occupancy, and the insurance section of the financing. Lender wording is part of the work, not a footnote after a number comes back.",
            "Property, loss of rents, liability, and umbrella are the core. Older buildings often need ordinance or law coverage. Elevators and boilers raise equipment breakdown. If anyone is employed, including a superintendent, workers compensation belongs in the same conversation. We place coverage where we are licensed to do so, and we say so before a broker of record letter is prepared.",
        ],
        "coverages": [
            ("Building property", "Replacement cost on the structure, with a clear coinsurance and valuation conversation."),
            ("Loss of rents", "Income that stops when a covered loss takes the building out of service."),
            ("General liability", "Premises and operations, including the additional insureds a lender or a tenant requires."),
            ("Umbrella", "Limits above the primary policies when the loan or the exposure calls for them."),
            ("Workers compensation", "For employees and supers. If there is no payroll, we still ask before we assume that."),
            ("Ordinance or law", "The cost of rebuilding to current code after a covered loss, on older property."),
        ],
        "checklist": [
            ("Building at replacement cost", "A limit based on rebuild cost, not on what the property last traded for."),
            ("Loss of rents or business income", "Months of rent, and the indemnity period that matches a real rebuild."),
            ("Ordinance or law", "Coverage for code upgrades, demolition, and the undamaged portion when the form requires it."),
            ("General liability", "Limits and additional insured status that match the loan or the leases."),
            ("Umbrella or excess", "A layer above liability when the lender or the exposure asks for it."),
            ("Mortgagee and loss payee", "The lender named the way the loan documents require."),
            ("Workers compensation", "If anyone is employed at the property, including a superintendent."),
            ("Equipment breakdown", "Boilers, elevators, and electrical equipment the property form may limit."),
        ],
        "asks": [
            "What does the loan's insurance section actually require?",
            "How many locations, and are they one schedule or separate policies?",
            "What is the construction, the year, and the occupancy mix?",
            "Is there payroll on the property?",
        ],
        "faqs": [
            ("Can you work from a lender's requirements?", "Yes. Send the insurance section. We match additional insured, mortgagee, property, and umbrella wording to that page before we call it done."),
            ("Do you place a single building and a schedule?", "Both. Tell us how the properties are owned. The named insured should follow the ownership, not a habit from the last policy."),
            ("What if the current policy is already fine?", "Then we say so. A review that recommends no change is a successful review."),
        ],
    },
    {
        "slug": "hospitality",
        "key": "hospitality",
        "nav": "Hospitality",
        "title": "Restaurant and Bar Insurance | SimpleINSURE",
        "desc": "Insurance for restaurants, bars, and cafes: property, liability, liquor, workers compensation, and the lease.",
        "h1": "A restaurant policy that can survive the lease and a Saturday night.",
        "lede": "Restaurants, bars, and cafes, including liquor liability.",
        "essay": [
            "Hospitality insurance fails in the details: a liquor exclusion, an assault sublimit, a landlord who is not actually an additional insured, or business income that runs out before the kitchen reopens. We read the lease insurance section and the current forms together.",
            "The program usually includes property on improvements and equipment, business income, general liability, and liquor liability when alcohol is served or sold. Where a state requires workers compensation, disability benefits, or paid family leave, those lines sit beside the package. New York is one of the states that requires disability benefits and Paid Family Leave for most employers. Delivery, outdoor seating, and off-site catering change the exposure, so we ask.",
        ],
        "coverages": [
            ("Property", "Improvements, equipment, and stock, including how a tenant policy treats the building."),
            ("Business income", "Payroll, rent, and profit for the time a covered shutdown actually lasts."),
            ("General liability", "Premises, products, and the additional insured wording in the lease."),
            ("Liquor liability", "For service or sale of alcohol. The dram shop exposure is not a general liability footnote."),
            ("Workers compensation", "Required for employees in every state that mandates it."),
            ("Assault or battery sublimit", "Often capped far below the liability limit. The number has to be read."),
        ],
        "checklist": [
            ("Tenant improvements and equipment", "The lease says who insures the buildout. The policy should agree."),
            ("Business income", "An indemnity period long enough for a real reopening, not a default of 30 days."),
            ("General liability and the landlord", "Additional insured status by endorsement, not by a certificate alone."),
            ("Liquor liability", "If alcohol is served or sold, or if the license is pending."),
            ("Assault or battery limit", "Find the sublimit. Do not assume it matches the general liability occurrence limit."),
            ("Workers compensation", "For W-2 staff. Ask separately about leased or contracted labor."),
            ("Statutory disability and paid family leave", "Where the state requires them. We confirm which state once we know where people work."),
            ("Umbrella", "Often required by the lease once alcohol or a high liability limit is in play."),
            ("Spoilage and equipment breakdown", "Refrigeration and cooking equipment fail in ways a basic property form may not cover."),
            ("Hired and non-owned auto", "If anyone delivers in a car the business does not own."),
        ],
        "asks": [
            "What does the lease require, and who is the additional insured?",
            "Is alcohol served, and on what license?",
            "How many employees, and in which state do they work?",
            "Is there delivery, catering, or entertainment?",
        ],
        "faqs": [
            ("Do I need liquor liability?", "If you serve or sell alcohol, yes in any program we would call complete. Many landlords require it, and a general liability form often excludes liquor."),
            ("What should I send from the lease?", "The insurance section, and any rider that names limits, additional insureds, or a waiver of subrogation."),
            ("We are not open yet. Can you still place it?", "Yes. Tell us the opening date, the buildout, and whether a landlord or an investor needs evidence of insurance before you open."),
        ],
    },
    {
        "slug": "construction",
        "key": "construction",
        "nav": "Contractors",
        "title": "Contractor and Trade Insurance | SimpleINSURE",
        "desc": "Contractor insurance written to the contract: general liability, workers compensation, auto, umbrella, and certificates.",
        "h1": "Coverage written to the contract, not to a guess.",
        "lede": "Liability, workers comp, and auto for the trades.",
        "essay": [
            "A contractor's insurance is a contract document. The exhibit names the limits, who must be an additional insured, whether the coverage is primary and noncontributory, and whether subrogation is waived. We read that page before we go to market.",
            "The usual structure is general liability, workers compensation, commercial auto, and umbrella. Tools and equipment in transit are an inland marine question. Design or construction management can require professional liability. Certificates are part of the service. We place coverage where we are licensed, and we will tell you if a project sits outside that.",
        ],
        "coverages": [
            ("General liability", "Ongoing and completed operations, with limits taken from the exhibit rather than a default."),
            ("Additional insured", "Upstream parties, on the edition of the form the contract requires."),
            ("Workers compensation", "Class codes and payroll that match the work, including where the work is done."),
            ("Commercial auto", "Vehicles the business owns, and hired or non-owned exposure when it does not."),
            ("Umbrella", "When the contract asks for limits above the primary policies."),
            ("Inland marine", "Tools, equipment, and installation floaters the auto and property forms do not cover."),
        ],
        "checklist": [
            ("General liability limits", "Per occurrence, aggregate, and products or completed operations, as the contract states them."),
            ("Additional insured, ongoing and completed", "Both, if the exhibit asks for both. Many forms cover only one."),
            ("Primary and noncontributory", "An endorsement, not a sentence on the certificate."),
            ("Waiver of subrogation", "On liability and, when asked, on workers compensation."),
            ("Per project aggregate", "If the upstream party requires the aggregate not to be shared across jobs."),
            ("Workers compensation", "Payroll, class codes, and states."),
            ("Commercial auto", "Owned vehicles, plus hired and non-owned if people drive to jobs."),
            ("Umbrella", "Follow-form questions matter as much as the limit."),
            ("Inland marine", "Tools and equipment that move."),
        ],
        "asks": [
            "May we see the insurance exhibit?",
            "What is the trade, and where is the work performed?",
            "What is the payroll, and do you use subcontractors?",
            "How many certificates do you need in a typical month?",
        ],
        "faqs": [
            ("Can you match a contract's insurance requirements?", "That is the job. Send the exhibit. If a carrier will not give a requested form, we tell you before you sign anything."),
            ("What if I use subcontractors?", "Tell us. It changes the liability structure, the certificates you will be asked to collect, and sometimes the price."),
            ("Do certificates wait until renewal?", "No. Certificate requests are part of servicing the account."),
        ],
    },
    {
        "slug": "professional",
        "key": "professional",
        "nav": "Offices",
        "title": "Professional, Office, and Retail Insurance | SimpleINSURE",
        "desc": "Insurance for offices, retailers, and firms that give advice: package policies, professional liability, cyber, and umbrella.",
        "h1": "For firms whose work is a lease, advice, or client data.",
        "lede": "Offices, shops, and professional firms.",
        "essay": [
            "A small office is not a small risk by default. The lease can require limits and additional insured status. The work can require professional liability. The systems can require a cyber conversation. We separate those instead of folding them into a single cheerful package.",
            "We place business owners or package policies where a location needs property and general liability, workers compensation where there are employees, hired and non-owned auto when people drive their own cars for work, and umbrella when a contract or a balance sheet asks for it. If the current program is already fitted to the work, we will say that.",
        ],
        "coverages": [
            ("Package policy", "Property, business income, and general liability for a location you own or lease."),
            ("Professional liability", "For advice a client relies on. A general liability form usually excludes it."),
            ("Cyber liability", "For client data, payments, and the systems the firm actually uses."),
            ("Workers compensation", "When there are employees, in the states where they work."),
            ("Hired and non-owned auto", "When staff use personal cars for the business."),
            ("Umbrella", "Above the underlying policies when contracts push the limits up."),
        ],
        "checklist": [
            ("General liability", "Premises and operations, plus the landlord if the lease requires it."),
            ("Tenant improvements and equipment", "If you rent, confirm who insures the buildout."),
            ("Business income", "If a shutdown stops revenue, not only if equipment is damaged."),
            ("Professional liability", "If clients rely on your advice, design, or management."),
            ("Cyber liability", "If you hold client, payment, or employee data."),
            ("Workers compensation", "If you have employees."),
            ("Hired and non-owned auto", "Errands and client visits in cars the firm does not own."),
            ("Employment practices", "If you have staff and want hiring and employment disputes addressed."),
            ("Umbrella", "When a client contract or a lease sets a limit above the package."),
        ],
        "asks": [
            "What does the business actually do for its clients?",
            "Is there a lease, and what does it require?",
            "Do you give advice, hold client data, or both?",
            "How many employees, and do they drive for work?",
        ],
        "faqs": [
            ("Is a business owners policy enough?", "Sometimes, for a simple location with no advice and no serious data. It is not a substitute for professional liability or cyber coverage."),
            ("We work from home. Is there anything to place?", "Often yes: professional liability, cyber, workers compensation if you employ anyone, and a personal home policy that has not quietly excluded business activity."),
            ("Can personal insurance sit with the business?", "Yes. Many owners want the house, the cars, and an umbrella quoted in the same review. Start with the coverage guide or the quote form."),
        ],
    },
    {
        "slug": "personal",
        "key": "personal",
        "nav": "Personal",
        "title": "Home, Auto, and Umbrella Insurance | SimpleINSURE",
        "desc": "Homeowners, auto, and personal umbrella for owners and families, including rental property held in a personal name.",
        "h1": "Home, auto, and umbrella, in the same conversation as the business.",
        "lede": "Home, auto, and umbrella for owners and their families.",
        "essay": [
            "The personal account is where a serious liability loss can land after the business policies respond, or instead of them. We would rather see the house, the cars, and the umbrella next to the commercial program than discover the gap after a loss.",
            "We place homeowners or renters, auto, and personal umbrella. If a rental property is held in a personal name, it needs its own discussion, because a homeowners form does not cover it. Valuables above a standard sublimit can be scheduled. We place these where we are licensed to do so.",
        ],
        "coverages": [
            ("Homeowners or renters", "The residence, contents, liability, and the use of the home for any business."),
            ("Auto", "The cars and the people who actually drive them."),
            ("Personal umbrella", "Limits above home and auto, coordinated with the underlying policies."),
            ("Valuable articles", "Jewelry, art, and collections a standard policy caps."),
            ("Rental dwelling", "Investment property in a personal name, which a homeowners policy does not cover."),
        ],
        "checklist": [
            ("Dwelling limit", "Rebuild cost, not the market price and not the mortgage balance."),
            ("Liability on the home", "The underlying limit an umbrella will require."),
            ("Other structures and home business", "A studio, a rental suite, or regular client meetings can fall outside the form."),
            ("Auto liability limits", "High enough to meet the umbrella's underlying requirement."),
            ("Drivers", "Everyone in the household who drives, listed on purpose."),
            ("Personal umbrella", "Especially if you also have a business, a rental, or a youthful driver."),
            ("Scheduled valuables", "Items a standard sublimit would not fully pay."),
            ("Rental or secondary home", "A separate policy if it is not your primary residence."),
        ],
        "asks": [
            "Is this a primary home, a rental, or both?",
            "How many cars, and who drives them?",
            "Is there already a personal umbrella?",
            "Should this be reviewed beside a commercial account?",
        ],
        "faqs": [
            ("Will you look at home and auto with the business?", "Yes. Say so on the quote form or in the coverage guide. One broker can hold both."),
            ("Does my homeowners policy cover a rental apartment I own?", "Not as a residence you rent to others. That is a different policy. Tell us about it."),
            ("What limit should an umbrella start at?", "There is no universal number. It depends on the underlying policies, the assets, and the other liability you already buy. We will show the options rather than invent a rule."),
        ],
    },
]


def checklist_block(ind):
    items = []
    for i, (title, why) in enumerate(ind["checklist"]):
        fid = f'{ind["slug"]}-{i}'
        items.append(
            f'<li><label for="{fid}"><input id="{fid}" type="checkbox" value="{h(title)}">'
            f"<span><b>{h(title)}</b><span>{h(why)}</span></span></label></li>"
        )
    return f'''<div data-checks="{ind["slug"]}" data-label="{h(ind["nav"])}" data-subject="Checklist: {h(ind["nav"])}">
      <ul class="check">{"".join(items)}</ul>
      <div class="cta-row">
        <button type="button" class="btn" data-email-gaps>Email the gaps <span class="arr" aria-hidden="true">→</span></button>
        <a class="btn-ghost" href="/quote/?type={ind["slug"]}">Start a quote</a>
      </div>
      <p class="quiet">Checked items stay in this browser. Nothing is sent until you choose Email the gaps.</p>
    </div>'''


def industry(ind, path=None, canonical=None):
    path = path or f'/coverage/{ind["slug"]}/'
    cov = "".join(f"<div><b>{h(a)}</b><span>{h(b)}</span></div>" for a, b in ind["coverages"])
    asks = "".join(f"<li>{h(q)}</li>" for q in ind["asks"])
    faqs = "".join(f"<details><summary>{h(q)}</summary><p>{h(a)}</p></details>" for q, a in ind["faqs"])
    essay = "".join(f"<p>{h(p)}</p>" for p in ind["essay"])
    faq_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in ind["faqs"]
        ],
    }, ensure_ascii=True)
    main = f'''
<header class="photo-hero">
  <div class="hero-media">
    <div class="ken">{pic(ind["key"], eager=True, sizes="100vw")}</div>
    <div class="hero-shade" aria-hidden="true"></div>
  </div>
  <div class="wrap">
    <p class="kicker m-only">{h(ind["nav"])}</p>
    <h1 class="rise"><span class="line"><span>{h(ind["h1"])}</span></span></h1>
    <p class="lede">{h(ind["lede"])}</p>
    <div class="cta-row"><a class="btn btn-light magnet" href="/quote/?type={ind["slug"]}">Start with this account {ARROW}</a><a class="m-phone m-only" href="{TEL}">{PHONE}</a></div>
  </div>
</header>
<section class="section" style="padding-top:64px"><div class="wrap split">
  <div class="prose"><h2>How we look at it</h2>{essay}</div>
  <div class="ask"><h2>What we ask first</h2><ul>{asks}</ul></div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
  <div class="intro"><p class="kicker">Coverage</p><h2>What a careful program usually includes.</h2></div>
  <div class="defs">{cov}</div>
</div></section>
<section class="section" style="padding-top:0" id="checklist"><div class="wrap">
  <div class="intro"><p class="kicker">Checklist</p><h2>Mark what you already have.</h2>
  <p class="lede">Leave the gaps clear. Then email them, or start a quote with this practice selected.</p></div>
  {checklist_block(ind)}
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
  <div class="intro"><p class="kicker">Questions</p><h2>Asked early.</h2></div>
  <div class="faq">{faqs}</div>
</div></section>
''' + continue_to([
        ("/policy-review/", "01", "Policy review", "Send the policy you have. A second reading is the point."),
        ("/needs/", "02", "Coverage guide", "A short set of questions and a memo for this kind of account."),
        ("/switching/", "03", "Switching brokers", "The order of work, including the broker of record letter."),
    ])
    return document(ind["title"], ind["desc"], path, main, current=f'/coverage/{ind["slug"]}/', canonical=canonical, extra=f'<script type="application/ld+json">{faq_ld}</script>')


def coverage_index():
    rows = []
    for i, (href, title, sub, key) in enumerate(COVER, 1):
        on = "is-on" if i == 1 else ""
        rows.append(
            f'<a class="{on}" href="{href}" {photo_attrs(key)}>'
            f"<span><strong>{h(title)}</strong><em>{h(sub)}</em></span><span class=\"go\" aria-hidden=\"true\">→</span></a>"
        )
    main = page_head(
        "Coverage",
        "Commercial and personal, handled as one account.",
        "Choose a practice for the coverage we place, the questions we ask, and a checklist you can mark.",
    ) + f'''
<section class="section" style="padding-top:12px"><div class="wrap">
  <div class="index-list">{"".join(rows)}</div>
</div></section>
''' + continue_to([
        ("/needs/", "01", "Coverage guide", "Not sure which practice fits? Answer a few questions."),
        ("/checklists/", "02", "All checklists", "Every practice, in one place."),
        ("/quote/", "03", "Request a review", "Tell us the account. A broker follows up."),
    ])
    return document(
        "Coverage | SimpleINSURE",
        "Commercial and personal insurance practices: real estate, hospitality, contractors, offices, and household.",
        "/coverage/",
        main,
    )


def quote_page():
    steps = f'''
<div data-step="1" data-label="Account" data-error="Choose what you want us to look at.">
  <h2 style="font-size:32px;margin-bottom:8px">What should we look at?</h2>
  <div style="margin-top:16px">{line_choices()}</div>
</div>
<div data-step="2" data-label="Details" hidden>
  <h2 style="font-size:32px;margin-bottom:14px">About the account</h2>
  <div class="fields">
    {field("city", "City or ZIP", attrs='autocomplete="postal-code"')}
    {field("timing", "Timing", kind="select", options=["Renewal coming up", "New purchase or opening", "Mid-term", "Not sure"])}
    {field("insured", "Currently insured?", kind="select", options=["Yes", "No", "Not sure"])}
    {field("re-desc", "Property or portfolio", kind="textarea", show="real-estate", full=True)}
    {field("re-loc", "Number of locations", show="real-estate")}
    {field("re-units", "Residential units", show="real-estate")}
    {field("re-com", "Commercial units", show="real-estate")}
    {field("ho-concept", "Concept", show="hospitality")}
    {field("ho-sales", "Estimated annual sales", kind="select", show="hospitality", options=["Under $500,000", "$500,000 to $1 million", "$1 million to $3 million", "Over $3 million", "Not open yet"])}
    {field("ho-seats", "Seats", show="hospitality")}
    {field("ho-emp", "Employees", show="hospitality")}
    {field("ho-alc", "Alcohol", kind="select", show="hospitality", options=["Full liquor", "Beer and wine", "No alcohol", "License pending"])}
    {field("ho-own", "Premises", kind="select", show="hospitality", options=["Lease", "Own the building", "Not open yet"])}
    {field("co-trade", "Trade", show="construction")}
    {field("co-where", "Where the work is performed", show="construction")}
    {field("co-pay", "Annual payroll", kind="select", show="construction", options=["Under $100,000", "$100,000 to $500,000", "$500,000 to $1 million", "Over $1 million"])}
    {field("co-subs", "Subcontractors?", kind="select", show="construction", options=["Yes", "No"])}
    {field("co-limit", "Contract limit, if you know it", show="construction", full=True)}
    {field("pr-does", "What the business does", kind="textarea", show="professional", full=True)}
    {field("pr-rev", "Annual revenue", kind="select", show="professional", options=["Under $250,000", "$250,000 to $1 million", "$1 million to $5 million", "Over $5 million"])}
    {field("pr-emp", "Employees", show="professional")}
    {field("pr-place", "Location", kind="select", show="professional", options=["Rent", "Own", "Home based"])}
    {field("pe-what", "What to cover", kind="select", show="personal", options=["Home", "Auto", "Home and auto", "Umbrella", "Rental property"])}
    {field("pe-zip", "Property ZIP", show="personal")}
    {field("un-about", "Describe what you want insured", kind="textarea", show="unsure", full=True)}
  </div>
</div>
<div data-step="3" data-label="Coverage" hidden>
  <h2 style="font-size:32px;margin-bottom:8px">What should the review include?</h2>
  <p class="quiet">These are preselected for the account type. Change anything.</p>
  <div style="margin-top:16px">{coverage_groups()}</div>
</div>
<div data-step="4" data-label="Contact" data-error="Add your name, and an email or a phone number." hidden>
  <h2 style="font-size:32px;margin-bottom:14px">Where should we reply?</h2>
  <div class="fields">{contact_fields("q")}</div>
  <p class="quiet">By sending this you agree that a broker may contact you about the request. There is no obligation.</p>
</div>'''
    main = page_head(
        "Coverage review",
        "Tell us the account. We will take it from there.",
        "A short form, then an email to the brokerage. A broker replies by phone or email. Call if it is urgent.",
    ) + f'''<section class="section" style="padding-top:28px"><div class="wrap layout">{wizard("Coverage review", "Email this request", steps)}{aside()}</div>
    <p class="quiet" style="margin-top:16px">Prefer to talk first? Call <a href="{TEL}">{PHONE}</a>.</p></section>'''
    return document(
        "Request a Coverage Review | SimpleINSURE",
        "Start a commercial or personal insurance review. The form opens an email to SimpleINSURE. Nothing is stored on the website.",
        "/quote/",
        main,
    )


def policy_page():
    concerns = [
        "The price",
        "The limits",
        "An exclusion or a sublimit",
        "A certificate or a contract",
        "A renewal that is coming up",
        "A claim",
        "I am not sure",
    ]
    chips = []
    for i, label in enumerate(concerns):
        fid = f"concern-{i}"
        chips.append(f'<label for="{fid}"><input id="{fid}" name="{fid}" type="checkbox"> {h(label)}</label>')
    steps = f'''
<div data-step="1" data-label="Account" data-error="Choose what the policy covers.">
  <h2 style="font-size:32px;margin-bottom:8px">What does the current policy cover?</h2>
  <div style="margin-top:16px">{line_choices()}</div>
</div>
<div data-step="2" data-label="The policy" hidden>
  <h2 style="font-size:32px;margin-bottom:8px">What do you want a second opinion on?</h2>
  <p class="quiet">Select any that apply. Add numbers if you have them. Estimates are fine.</p>
  <div class="chips" style="margin:16px 0">{"".join(chips)}</div>
  <div class="fields">
    {field("prem", "Current annual premium, if you know it")}
    {field("carrier", "Current carrier, if you want to say")}
    {field("renew", "Renewal or expiration date", kind="date")}
    {field("worry", "What concerns you", kind="textarea", full=True)}
  </div>
</div>
<div data-step="3" data-label="Contact" data-error="Add your name, and an email or a phone number." hidden>
  <h2 style="font-size:32px;margin-bottom:14px">Where should we reply?</h2>
  <div class="fields">{contact_fields("p")}</div>
</div>'''
    main = page_head(
        "Policy review",
        "A second reading of the policy you already have.",
        "Send what you know. Attach the declarations page to the email draft. If the program is already right, we will say so.",
    ) + f'''<section class="section" style="padding-top:28px"><div class="wrap layout">{wizard("Policy review", "Email this review", steps)}{aside()}</div></section>'''
    return document(
        "Policy Review | SimpleINSURE",
        "Request a second opinion on a current commercial or personal policy. The form opens an email. Nothing is stored on the website.",
        "/policy-review/",
        main,
    )


NEEDS = {
    "lines": [
        {"id": "real-estate", "label": "Property I own or manage", "hint": "Apartments, mixed-use, or commercial buildings", "result": "For property you own or manage"},
        {"id": "hospitality", "label": "A restaurant, bar, or cafe", "hint": "Dining, alcohol, and a lease", "result": "For a restaurant, bar, or cafe"},
        {"id": "construction", "label": "A contracting business", "hint": "Trades, general contracting, and job contracts", "result": "For a contracting business"},
        {"id": "professional", "label": "An office, retailer, or professional firm", "hint": "Advice, a location, or both", "result": "For an office, retailer, or professional firm"},
        {"id": "personal", "label": "Home, auto, or an umbrella", "hint": "Personal insurance, with or without a business", "result": "For home, auto, and personal umbrella"},
    ],
    "questions": [
        {"id": "employees", "label": "Are there employees, including a superintendent or part-time staff?", "lines": ["real-estate", "hospitality", "construction", "professional"]},
        {"id": "alcohol", "label": "Does the business serve or sell alcohol?", "lines": ["hospitality"]},
        {"id": "vehicles", "label": "Are cars or trucks used for the work, including personal cars on deliveries or job sites?", "lines": ["hospitality", "construction", "professional", "real-estate"]},
        {"id": "own-building", "label": "Does the business own the building it occupies?", "lines": ["hospitality", "professional"]},
        {"id": "lease", "label": "Does a lease or a lender set the insurance requirements?", "lines": ["real-estate", "hospitality", "professional"]},
        {"id": "contracts", "label": "Do contracts require you to name someone else on the policy?", "lines": ["construction", "professional", "real-estate"]},
        {"id": "advice", "label": "Does the firm give advice, design, or management that a client relies on?", "lines": ["professional", "construction"]},
        {"id": "data", "label": "Does the firm hold client, payment, or employee data on a system?", "lines": ["professional", "hospitality"]},
        {"id": "personal-too", "label": "Should home, auto, or a personal umbrella be reviewed as well?", "lines": ["real-estate", "hospitality", "construction", "professional"]},
        {"id": "rental", "label": "Do you own a rental property in a personal name?", "lines": ["personal"]},
        {"id": "valuables", "label": "Do you have jewelry, art, or collections a standard policy would cap?", "lines": ["personal"]},
    ],
    "items": [
        {"lines": ["real-estate"], "when": "always", "title": "Building property", "why": "Insure the structure for rebuild cost, and match mortgagee wording to the loan."},
        {"lines": ["real-estate"], "when": "always", "title": "Loss of rents", "why": "A covered shutdown stops income. The indemnity period should match a real repair."},
        {"lines": ["real-estate"], "when": "always", "title": "General liability", "why": "Premises liability, with additional insureds the lender or the leases require."},
        {"lines": ["real-estate"], "when": "always", "title": "Umbrella", "why": "A layer above the primary policies when the loan or the exposure calls for it."},
        {"lines": ["real-estate", "hospitality", "construction", "professional"], "when": "employees", "title": "Workers compensation", "why": "If anyone is employed, this is a statutory placement in the states that require it."},
        {"lines": ["hospitality", "construction", "professional", "real-estate"], "when": "employees", "title": "Statutory disability, where required", "why": "Some states, including New York, require disability benefits and Paid Family Leave beside workers compensation. We confirm the state before we place it."},
        {"lines": ["real-estate"], "when": "lease", "title": "Lender or lease wording", "why": "Additional insured, mortgagee, and cancellation notice should be taken from the document, not from memory."},
        {"lines": ["hospitality"], "when": "always", "title": "Property and business income", "why": "Improvements, equipment, stock, and the income lost while the doors are closed."},
        {"lines": ["hospitality"], "when": "always", "title": "General liability", "why": "Premises and products, plus the landlord if the lease requires additional insured status."},
        {"lines": ["hospitality"], "when": "alcohol", "title": "Liquor liability", "why": "A general liability form often excludes alcohol. If you serve or sell it, liquor liability is its own line."},
        {"lines": ["hospitality"], "when": "always", "title": "Assault or battery sublimit", "why": "Read the sublimit. It is often far below the main liability limit."},
        {"lines": ["hospitality"], "when": "always", "title": "Umbrella", "why": "Leases often require it once alcohol or a higher liability limit is in the picture."},
        {"lines": ["hospitality", "professional"], "when": "own-building", "title": "Building coverage for an owner-occupant", "why": "If you own the building, the property policy has to cover the structure, not only tenant improvements."},
        {"lines": ["construction"], "when": "always", "title": "General liability written to the contract", "why": "Limits, additional insureds, and completed operations should follow the insurance exhibit."},
        {"lines": ["construction"], "when": "contracts", "title": "Primary, noncontributory, and waiver", "why": "These are endorsements. A sentence on a certificate does not create them."},
        {"lines": ["construction"], "when": "always", "title": "Umbrella", "why": "Upstream contracts often ask for limits above the primary policies."},
        {"lines": ["construction", "hospitality", "professional", "real-estate"], "when": "vehicles", "title": "Auto, hired, or non-owned", "why": "Owned trucks are commercial auto. Personal cars used for work are a hired and non-owned question."},
        {"lines": ["construction"], "when": "always", "title": "Inland marine", "why": "Tools and equipment that move are rarely covered well by a liability or auto policy alone."},
        {"lines": ["professional"], "when": "always", "title": "Package or business owners policy", "why": "Property and general liability for a location, sized to the lease."},
        {"lines": ["professional", "construction"], "when": "advice", "title": "Professional liability", "why": "Advice, design, or management that a client relies on is usually excluded from general liability."},
        {"lines": ["professional", "hospitality"], "when": "data", "title": "Cyber liability", "why": "Client, payment, or employee data is a separate form from a package policy."},
        {"lines": ["professional", "hospitality", "real-estate", "construction"], "when": "personal-too", "title": "Home, auto, and personal umbrella", "why": "The personal account is where a liability loss can land after, or instead of, the business policies."},
        {"lines": ["personal"], "when": "always", "title": "Homeowners or renters", "why": "Dwelling, contents, and personal liability, with any business use of the home disclosed."},
        {"lines": ["personal"], "when": "always", "title": "Auto", "why": "The cars and the drivers, with liability limits that can support an umbrella."},
        {"lines": ["personal"], "when": "always", "title": "Personal umbrella", "why": "A layer above home and auto. The underlying limits have to qualify."},
        {"lines": ["personal"], "when": "rental", "title": "Rental dwelling", "why": "A property you rent to others is not covered by a homeowners policy on your residence."},
        {"lines": ["personal"], "when": "valuables", "title": "Scheduled valuables", "why": "Jewelry, art, and collections often sit above a standard sublimit."},
    ],
    "disclaimer": "This is a general list, not a quote and not advice on your contracts. Placement follows the licenses we hold. A broker should read the policies and the agreements before anything is bound.",
}


def needs_page():
    main = page_head(
        "Coverage guide",
        "What does this business need?",
        "Answer a few yes or no questions. You get a coverage memo you can email, plus a path into a quote. It is a guide, not a binder.",
    ) + f'''
<section class="section" style="padding-top:12px"><div class="wrap" style="max-width:800px">
  <script type="application/json" id="needs-data">{json.dumps(NEEDS, ensure_ascii=True)}</script>
  <div id="needs-app" aria-live="polite"></div>
  <a id="needs-quote" class="sr" href="/quote/">Start a quote with these answers</a>
  <noscript>
    <p class="note">The interactive guide needs JavaScript. You can still use the <a href="/checklists/">checklists</a>, email <a href="{MAIL}">{EMAIL}</a>, or call <a href="{TEL}">{PHONE}</a>.</p>
  </noscript>
  <p class="quiet">Prefer to skip the questions? <a href="/quote/">Start a coverage review</a> or call <a href="{TEL}">{PHONE}</a>.</p>
</div></section>'''
    return document(
        "What Does My Business Need? | SimpleINSURE",
        "An interactive coverage guide for property, hospitality, construction, professional firms, and personal insurance.",
        "/needs/",
        main,
    )


def checklists_page():
    buttons = []
    panels = []
    for ind in INDUSTRIES:
        buttons.append(f'<button type="button" role="tab" data-tab="{ind["slug"]}">{h(ind["nav"])}</button>')
        panels.append(f'<div class="tab-panel" id="panel-{ind["slug"]}">{checklist_block(ind)}</div>')
    main = page_head(
        "Checklists",
        "Mark the coverage you already have.",
        "One list for each practice. Check what is in the current program. Email the gaps, or open the full practice page.",
    ) + f'''
<section class="section" style="padding-top:12px"><div class="wrap">
  <div class="tabs" data-tabs>
    <div class="tab-bar" role="tablist">{"".join(buttons)}</div>
    {"".join(panels)}
  </div>
</div></section>'''
    return document(
        "Coverage Checklists | SimpleINSURE",
        "Coverage checklists for real estate, hospitality, construction, professional firms, and personal insurance.",
        "/checklists/",
        main,
    )


def switching_page():
    steps = [
        ("A conversation, not a commitment", "You tell us what the account is and what is not working. Price, a contract, a nonrenewal, a claim, or a broker you rarely hear from. No one is appointed yet."),
        ("We read the current program", "Send the declarations page and, if you have them, the forms list and the endorsements. The declarations page is the cover. The forms decide the coverage."),
        ("An opinion before a market", "We tell you what is solid, what is thin, and whether moving is worth it. If the program should stay where it is, that is the recommendation."),
        ("A market, only if there is a reason", "We approach carriers that write this kind of risk, including specialty markets when the standard market is a poor fit. The account goes to market with a purpose."),
        ("You choose, with the current program still in view", "Options sit beside what you have: price, limits, exclusions, and the wording a lender or a contract requires. You can keep the policy you have."),
        ("The broker of record letter, if you appoint us on an existing policy", "A broker of record letter is a short written appointment. It tells the insurance company that you want SimpleINSURE to service a policy that is already in force. It names you, the policy, and the broker, and you sign it. It does not, by itself, cancel coverage, change limits, or erase a claim. The carrier decides whether to honor it. Some accept a change during the term. Some will not act until renewal. We tell you which case applies before you sign. If the right path is a replacement policy instead of an appointment, we coordinate the effective date so one program ends as the next begins."),
        ("The handover", "Certificates, mortgagee and landlord notices, open claims, and the renewal date move onto our calendar. You should not have to introduce yourself twice."),
    ]
    items = "".join(
        f'<li data-reveal><span class="dot" aria-hidden="true"></span><h3>{h(title)}</h3><p>{h(text)}</p></li>'
        for title, text in steps
    )
    main = page_head(
        "Switching brokers",
        "How a change of broker actually works.",
        "The order we follow, and what a broker of record letter does and does not do.",
    ) + f'''
<section class="section" style="padding-top:20px"><div class="wrap prose narrow">
  <p>People stay with a broker out of inertia, then discover the policy was never read against the lease or the contract. Changing brokers does not require a gap in coverage, and it does not require you to insult the last one. It requires an order.</p>
  <p>We place coverage where we are licensed to do so. If an account sits outside that, we say so before anyone signs an appointment.</p>
</div>
<div class="wrap" style="margin-top:36px"><ol class="time" data-time>{items}</ol></div>
</section>
''' + continue_to([
        ("/policy-review/", "01", "Start with the policy", "A review is the first step. The letter comes later, if at all."),
        ("/resources/#broker-of-record", "02", "Read the letter", "A plain explanation of the appointment."),
        ("/client-center/", "03", "After the move", "Certificates, changes, renewals, and claims."),
    ])
    return document(
        "How Switching Brokers Works | SimpleINSURE",
        "The order of work when you change insurance brokers, including what a broker of record letter does and does not do.",
        "/switching/",
        main,
    )


GLOSSARY = [
    ("Additional insured", "A person or company added to a liability policy, usually by endorsement, for claims arising out of the named insured's work or premises. A certificate that says they are additional insureds does not create that status if the endorsement is missing."),
    ("Admitted carrier", "An insurer licensed to write a line of insurance in a given state. Admitted status is not the same thing as a financial strength rating."),
    ("Broker of record", "The broker the insured has appointed to service a policy with the insurer. The appointment is usually made by a signed broker of record letter. It does not, by itself, rewrite the coverage."),
    ("Business income", "Coverage for income lost, and sometimes continuing expenses, after a covered property loss shuts the operation. The indemnity period and the coinsurance percentage decide whether it is useful."),
    ("Business owners policy", "A package that combines property and liability for many smaller firms. It is a starting structure, not a substitute for professional liability, cyber, liquor, or an umbrella."),
    ("Certificate of insurance", "A snapshot that says a policy exists. It does not change the policy. Additional insured status, waivers, and primary wording live in endorsements."),
    ("Coinsurance", "A property penalty if the limit you buy is below a stated percentage of the value at the time of loss. A building insured for the loan balance can fail this test even when the premium was paid."),
    ("Declarations page", "The cover of the policy: named insured, dates, limits, deductibles, locations, and a list of forms. It is not the whole contract. The forms and endorsements control."),
    ("Deductible", "The amount the insured retains on a covered loss before the policy pays. It is not the same thing as a self-insured retention, which is more common on some liability and umbrella forms."),
    ("Employment practices liability", "Coverage for claims by employees alleging wrongful employment acts, such as discrimination, harassment, or wrongful termination. A general liability policy usually excludes these claims."),
    ("Endorsement", "A form that changes the policy. Additional insureds, waivers, and exclusions that surprise people at a claim are almost always endorsements, not the declarations page."),
    ("Excess liability", "A policy that sits above a scheduled underlying limit and usually follows that underlying form. An umbrella can be broader or narrower. The follow-form wording is the thing to read."),
    ("Exclusion", "Language that takes something out of coverage. Hospitality forms often exclude liquor or cap assault. Contractor forms often exclude professional services. The exclusion, not the brochure, controls."),
    ("General liability", "Coverage for bodily injury, property damage, and certain personal or advertising injury arising from premises and operations. It is not property insurance, not workers compensation, and not professional liability."),
    ("Inland marine", "Coverage for property that moves, or that sits off your premises: tools, equipment, and goods in transit or installation. It fills a hole auto and location property policies leave open."),
    ("Liquor liability", "Coverage for injury alleged to arise from selling, serving, or furnishing alcohol. In many states a dram shop statute creates the exposure. General liability often excludes it."),
    ("Loss payee", "A party, often a lender or a lessor, entitled to be paid for a covered property loss. It is a property concept. It is not the same as an additional insured on a liability policy."),
    ("Loss run", "A carrier's history of claims on a policy. Underwriters ask for it. So should you, before you assume a renewal price is a surprise."),
    ("Named insured", "The person or entity the policy is issued to. Ownership should match the named insured. A policy in the wrong name is a common and expensive mistake."),
    ("Ordinance or law", "Property coverage for the extra cost of rebuilding to current building codes after a covered loss, including demolition and, on some forms, the undamaged portion. It matters on older buildings."),
    ("Primary and noncontributory", "Wording, by endorsement, that your policy responds first and does not seek contribution from the other party's insurance. Contracts ask for it. A certificate line does not create it."),
    ("Replacement cost", "Payment based on the cost to replace with new materials of like kind and quality, without deduction for depreciation. Actual cash value subtracts depreciation. The form says which one you bought."),
    ("Subrogation", "The insurer's right, after paying a loss, to recover from a third party that caused it. A waiver of subrogation gives up that right against a party named in the endorsement, often a landlord or an upstream contractor."),
    ("Umbrella", "Liability limits above underlying policies, and sometimes coverage broader than those policies. Personal and commercial umbrellas are different contracts. The underlying limits have to qualify."),
    ("Waiver of subrogation", "An endorsement in which the insurer waives recovery against a specified party. Leases and construction contracts routinely require it on liability and sometimes on workers compensation."),
    ("Workers compensation", "Statutory coverage for employee injury. It is required for most employers in the states that mandate it. It does not cover the owner's personal health insurance, and it is not general liability."),
]


ESSAYS = [
    ("broker-of-record", "The broker of record letter", [
        "A broker of record letter is a signed note from you to the insurance company. It says that SimpleINSURE, or whichever broker you name, is the broker you want servicing a policy that already exists. The letter identifies you, the policy number, and the new broker.",
        "It does not cancel the policy. It does not change your limits, your deductibles, or your exclusions. It does not settle a claim. The insurer decides whether to accept the appointment. Some carriers honor a change in the middle of the term. Others will not move until the renewal. Commission usually follows the appointment once it is accepted, which is why the prior broker notices.",
        "The letter comes after that reading. We tell you whether a move is useful, and whether the carrier is likely to accept an appointment now or only at renewal. If a replacement policy is the cleaner path, we set the effective dates so coverage continues from one program to the next.",
        "You can ask us for the letter before you sign it. You should. If a broker will not explain the appointment in plain language, that is information about the broker.",
    ]),
    ("declarations", "How to read a declarations page", [
        "The declarations page is the cover sheet. It names the insured, the policy number, the period, the premium, the limits, the deductibles, the locations, and a schedule of form numbers. People treat it as the policy. It is the index.",
        "Start with the named insured. If the building is owned by an LLC and the policy names a person, or the reverse, stop and fix that before you debate the price. Then read the locations. A schedule that dropped an address is a common renewal error.",
        "Limits deserve a second look against the contract or the loan, not against last year's premium. A general liability limit and an assault sublimit can both appear on the page. The smaller number is the one that will matter in that kind of claim. Property limits should be compared with rebuild cost, not with the mortgage.",
        "Then turn to the form list. Each number is a document. Exclusions, additional insured grants, and coinsurance terms live there. If your file has the declarations page and not the forms, ask for the forms. A review without them is a review of the cover.",
    ]),
    ("additional-insured", "Additional insured, loss payee, and waiver of subrogation", [
        "These three phrases share leases and construction contracts, and they are not interchangeable.",
        "An additional insured is a liability status. A landlord, a lender, or an upstream contractor is added, by endorsement, for certain claims arising out of your work or your premises. The edition of the form matters. Some cover ongoing operations only. Some include completed operations. A certificate that lists the party does not create the status.",
        "A loss payee is a property status. If the building burns, that party is paid for its interest. Lenders and equipment lessors ask for this. Naming a bank as an additional insured on liability, and forgetting it as a mortgagee on property, is a frequent closing problem.",
        "A waiver of subrogation is a promise, by endorsement, that the insurer will not pursue a specified party after paying a covered loss. Contracts ask for it so your insurer does not sue the landlord or the general contractor later. It has to be on the policy the contract names. It is not created by a handshake or by a line typed onto a certificate.",
    ]),
    ("renewal", "What a renewal should look like", [
        "A renewal is not a invoice with a new date. Ninety days before expiration is not too early to have the file open. The work is to reread the account against anything that changed: payroll, sales, locations, contracts, drivers, and losses.",
        "Ask for loss runs. Compare the form list to last year. Carriers revise exclusions quietly. A hospitality renewal can add or tighten an assault limitation. A property renewal can change valuation or the ordinance or law grant. If nobody put the two form lists next to each other, nobody reviewed the renewal.",
        "The premium is the last comparison, not the first. A lower price with a lower limit, a higher deductible, or a missing endorsement is not a saving.",
        "If your broker sends the bill and not the comparison, you are allowed to ask for the comparison. You are also allowed to ask someone else to read it.",
    ]),
]


def resources_page():
    essays = []
    for eid, title, paras in ESSAYS:
        body = "".join(f"<p>{h(p)}</p>" for p in paras)
        essays.append(f'<article id="{eid}"><h2>{h(title)}</h2>{body}</article>')
    jumps = "".join(f'<a href="#{eid}">{h(title)}</a>' for eid, title, _p in ESSAYS)
    jumps += '<a href="#glossary">Glossary</a>'
    terms = "".join(
        f'<article class="term" data-term><h3>{h(term)}</h3><p>{h(defn)}</p></article>'
        for term, defn in GLOSSARY
    )
    main = page_head(
        "Resources",
        "A short shelf for people who would rather read the form.",
        "Guides and a glossary. Nothing here is a binder, a legal opinion, or a substitute for the policy.",
    ) + f'''
<section class="section" style="padding-top:12px"><div class="wrap prose narrow">
  <nav class="jump" aria-label="On this page">{jumps}</nav>
  {"".join(essays)}
  <h2 id="glossary">Glossary</h2>
  <div class="gloss-tools">
    <label class="sr" for="gloss-q">Search the glossary</label>
    <input id="gloss-q" type="search" placeholder="Search terms" autocomplete="off">
    <p id="gloss-count" aria-live="polite"></p>
  </div>
  <div id="gloss">{terms}</div>
</div></section>'''
    return document(
        "Resources and Glossary | SimpleINSURE",
        "Plain-language guides to broker of record letters, declarations pages, additional insureds, renewals, and an insurance glossary.",
        "/resources/",
        main,
    )


def client_page():
    cert = wizard(
        "Certificate request",
        "Email this certificate request",
        f'''<div data-step="1" data-label="Certificate" data-error="Add the named insured, the holder, your name, and an email or phone number.">
          <h2 style="font-size:32px;margin-bottom:14px">Request a certificate</h2>
          <div class="fields">
            {field("ni", "Named insured", required=True, full=True)}
            {field("holder", "Certificate holder", required=True)}
            {field("haddr", "Holder address", full=True)}
            {field("job", "Project, lease, or reason", kind="textarea", full=True)}
            {field("ai", "Additional insured needed?", kind="select", options=["Yes", "No", "Not sure"])}
            {field("needby", "Needed by", kind="date")}
            {field("cname", "Your name", required=True, attrs='autocomplete="name"')}
            {field("cemail", "Email", kind="email", need="email", attrs='autocomplete="email"')}
            {field("cphone", "Phone", kind="tel", need="phone", attrs='autocomplete="tel"')}
          </div>
          <p class="quiet">We issue a certificate when the policy allows it. If the holder wants wording the policy does not grant, we will tell you instead of typing it onto the form.</p>
        </div>''',
    )
    main = page_head(
        "Client service",
        "What you should be able to expect from a broker.",
        "One place for certificates, changes, renewals, and the first hour after a loss.",
    ) + f'''
<section class="section" style="padding-top:20px"><div class="wrap split">
  <div>
    <ol class="standard-list">
      <li><span>01</span><p>You have one broker for the account. You are not reintroduced at every renewal.</p></li>
      <li><span>02</span><p>Certificates go out when the policy supports them. If it does not, we say what is missing.</p></li>
      <li><span>03</span><p>Changes in payroll, vehicles, locations, or ownership are endorsed, not remembered.</p></li>
      <li><span>04</span><p>Renewal work starts before the expiration date, with a comparison, not only a bill.</p></li>
      <li><span>05</span><p>If a loss happens, you call us. We help you notify the carrier and we follow the claim through to the carrier's decision.</p></li>
      <li><span>06</span><p>If your current program is already right, we will tell you to keep it.</p></li>
    </ol>
  </div>
  <div class="panel">
    <h2>Reach us</h2>
    <div class="row"><span>Call</span><a href="{TEL}">{PHONE}</a></div>
    <div class="row"><span>Email</span><a href="{MAIL}">{EMAIL}</a></div>
    <p class="quiet">Most of the work is by phone, email, and video.</p>
  </div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap prose narrow">
  <h2>If a loss happens</h2>
  <p>Call {PHONE}. Note the date, the place, and who was involved. Photograph what you safely can. Describe what happened, not who was at fault. Your policy requires you to report the loss and cooperate with the insurer, and we will help with that. Send the suit papers the day you receive them. Late notice is an avoidable way to damage a claim.</p>
  <p>We report the claim and stay with it. Coverage is the carrier's decision under the policy, and that is the decision we bring back to you.</p>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap layout">{cert}{aside()}</div></section>
'''
    return document(
        "Client Service | SimpleINSURE",
        "Certificates, changes, renewals, and what to do when a loss happens.",
        "/client-center/",
        main,
    )


def about_page():
    main = page_head(
        "The firm",
        "An independent brokerage.",
        "We work for you, not for any one insurance company.",
    ) + f'''
<section class="section" style="padding-top:12px"><div class="wrap split">
  <div class="prose">
    <h2>An independent practice</h2>
    <p>SimpleINSURE Brokerage LLC places commercial and personal insurance for the client, not for a single carrier. We work with a range of insurance companies, including specialty markets for risks the standard market will not write.</p>
    <p>Remy Mehdizadeh founded the firm so an owner could have one broker who reads the policy and remains after it is bound. That standard is on the <a href="/client-center/">client service</a> page: one broker for the account, a policy read against the lease or the contract, and a direct answer when the program already in force should stay.</p>
    <h2>Where we are licensed</h2>
    <p>Each placement follows the license that covers it. The license on record is on the <a href="/legal/">licenses page</a>.</p>
    <h2>How we are paid</h2>
    <p>Usually by commission from the insurer. The plain version is on the licenses page, including how to ask about compensation on your own policy.</p>
    <p><a href="{TEL}">{PHONE}</a> · <a href="{MAIL}">{EMAIL}</a></p>
  </div>
  {figure_block("hero", "(max-width: 980px) 100vw, 40vw")}
</div></section>
''' + continue_to([
        ("/policy-review/", "01", "Policy review", "Bring the policy you have."),
        ("/partners/", "02", "For advisors", "Attorneys, managers, and accountants."),
        ("/legal/", "03", "Licenses", "The New York license and how we are paid."),
    ])
    return document(
        "About SimpleINSURE",
        "SimpleINSURE places commercial and personal insurance and stays with the account after it is bound.",
        "/about/",
        main,
    )


def partners_page():
    form = wizard(
        "Referral partner",
        "Email this introduction",
        f'''<div data-step="1" data-label="Introduction" data-error="Add your name, and an email or a phone number.">
          <h2 style="font-size:32px;margin-bottom:14px">Introduce yourself</h2>
          <div class="fields">
            {field("pn", "Name", required=True, attrs='autocomplete="name"')}
            {field("pf", "Firm", attrs='autocomplete="organization"')}
            {field("pr", "Role", kind="select", options=["Real estate attorney", "Property manager", "Accountant or CPA", "Other"])}
            {field("pe", "Email", kind="email", need="email", attrs='autocomplete="email"')}
            {field("pp", "Phone", kind="tel", need="phone", attrs='autocomplete="tel"')}
            {field("pc", "A client to introduce now?", kind="select", options=["Not yet", "Yes"])}
            {field("pnotes", "Notes", kind="textarea", full=True)}
          </div>
        </div>''',
    )
    main = page_head(
        "Partners",
        "For the advisors an owner already trusts.",
        "Real estate attorneys, property managers, and accountants. Introduce a client. We keep you informed.",
    ) + f'''
<section class="section" style="padding-top:12px"><div class="wrap">
  <div class="defs">
    <div><b>Real estate attorneys</b><span>Binders and evidence of insurance for closings. We read the loan requirements first.</span></div>
    <div><b>Property managers</b><span>One contact for the buildings you manage: renewals, vendor certificates, and a nonrenewal.</span></div>
    <div><b>Accountants</b><span>When a client hires, or buys a building, the insurance should be ready before the deadline is.</span></div>
    <div><b>What you can expect</b><span>A prompt call to your client, a copy to you if they agree, and a note when the account is placed. Their information is not shared beyond that.</span></div>
  </div>
  <div class="note"><b>Referral policy.</b> Compensation for a referral follows the license. New York Insurance Law § 2116 limits referral fees and commission sharing to licensed persons. Partners get a responsive broker and, where it fits, a referral back.</div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap layout">{form}{aside()}</div></section>
'''
    return document(
        "Referral Partners | SimpleINSURE",
        "A referral path for real estate attorneys, property managers, and accountants. No fees to unlicensed persons.",
        "/partners/",
        main,
    )


def legal_page():
    main = page_head("Licenses and disclosures", "The license, the compensation, and the privacy note.") + f'''
<section class="section" style="padding-top:12px"><div class="wrap prose narrow">
  <h2 id="licensing">Licensing</h2>
  <p>SimpleINSURE Brokerage LLC is a New York licensed property and casualty insurance broker, NY DFS License No. BR-1984615. Its licensed individual broker is Remy Mehdizadeh, NY DFS License No. 1982767. You can confirm both records on the <a href="https://myportal.dfs.ny.gov/nylinxext/elsearch.alice" rel="noopener">New York DFS licensee search</a>.</p>
  <p>{ADDR}. Phone <a href="{TEL}">{PHONE}</a>. Email <a href="{MAIL}">{EMAIL}</a>.</p>
  <p>We place insurance where we are licensed to do so. This page states the New York license. It does not claim licenses in other states. If an account requires a license we do not yet hold, we will say so before an appointment or a placement.</p>
  <h2 id="how-we-are-paid">Producer compensation disclosure</h2>
  <p>SimpleINSURE Brokerage LLC is an insurance producer licensed by the State of New York. When you work with us, we act as your insurance broker: we represent you in finding coverage and presenting options from insurers, and we do not act for any single insurer.</p>
  <p>We are usually paid a commission by the insurance company that issues your policy, generally a percentage of the premium. We may also receive other compensation from insurers or from third parties, such as wholesale brokers or managing general agents, including contingent or bonus payments.</p>
  <p>The compensation we receive may vary depending on a number of factors, including the insurance contract and the insurance company you select, the volume of business we place with an insurer, and the profitability of that business.</p>
  <p>You may request information about the compensation we expect to receive from your purchase, and about compensation we would have received on any alternative quotes we presented to you. Ask us before or after you buy, and we will provide it.</p>
  <p>This notice is also provided at or before the time you apply for coverage. It is a general description and not a quote for your account.</p>
  <h2 id="not-a-binder">Not an offer or a binder</h2>
  <p>Descriptions on this website are general. They do not amend a policy and they are not an offer to insure. Coverage is subject to underwriting and to the forms that are issued. The policy governs.</p>
  <h2 id="privacy">Privacy</h2>
  <h3>Forms and email</h3>
  <p>Forms on this site do not submit to a server we control. They open an email draft in your own mail program, addressed to {EMAIL}. Nothing you type into a form is stored on this website. Ordinary email is not encrypted. Do not send Social Security numbers, driver's license numbers, dates of birth, bank account or payment card numbers, or medical information by email, and do not attach a document that shows them. If a declarations page or application shows that kind of information, black it out or call {PHONE} and we will arrange another way to send it.</p>
  <h3>Analytics</h3>
  <p>This site uses Google Analytics, a service of Google LLC, to count visits and see which pages are used. Google Analytics sets cookies in your browser and receives information such as pages viewed, approximate location, device and browser type. We use this only in aggregate to improve the site. We do not sell personal information. You can block or delete cookies in your browser settings, or install the Google Analytics opt-out browser add-on at tools.google.com/dlpage/gaoptout.</p>
  <h3>How we use what you send</h3>
  <p>If you email or call, we use what you send to respond, to obtain quotes and coverage, and to service your account. To do that we share it with insurance companies, wholesale brokers and others involved in placing or servicing your insurance, and otherwise only as permitted or required by law.</p>
  <h3>Privacy notice for personal insurance customers</h3>
  <p>We collect nonpublic personal information about you from your applications and other forms; your transactions with us and with insurance companies; and, with your authorization where required, consumer reporting agencies and motor vehicle records. We do not disclose nonpublic personal information about our customers or former customers to anyone except as permitted by law, for example to insurance companies and others as needed to place, service or process your insurance, to comply with law, or with your consent. We do not share it with nonaffiliated third parties for their own marketing. We restrict access to nonpublic personal information to those who need it to provide services to you, and we maintain physical, electronic and procedural safeguards that comply with applicable New York requirements to protect it. A copy of this notice is provided when you obtain personal insurance through us, and annually as required.</p>
</div></section>'''
    return document(
        "Licenses and Disclosures | NY DFS BR-1984615 | SimpleINSURE",
        "NY DFS License No. BR-1984615. SimpleINSURE Brokerage LLC is a commercial and personal broker in Garden City.",
        "/legal/",
        main,
    )


def credits_page():
    rows = []
    for key, c in CRED.items():
        rows.append(
            f"<tr><td>{h(key)}</td><td><a href=\"{h(c['page'])}\" rel=\"noopener\">{h(c['title'])}</a></td>"
            f"<td>{h(c['artist'])}</td><td><a href=\"{h(c['license_url'])}\" rel=\"noopener\">{h(c['license'])}</a></td></tr>"
        )
    main = page_head("Photo credits", "Every photograph on this site, with the author and the license.") + f'''
<section class="section" style="padding-top:12px"><div class="wrap prose">
  <p>Photographs are used under the Unsplash License or the Pexels License. Credit is optional. It is listed here and is not shown on the other pages.</p>
  <table class="credits" style="width:100%;border-collapse:collapse;margin-top:18px">
    <thead><tr><th style="text-align:left;padding:8px;border-bottom:1px solid var(--line)">Used as</th><th style="text-align:left;padding:8px;border-bottom:1px solid var(--line)">File</th><th style="text-align:left;padding:8px;border-bottom:1px solid var(--line)">Author</th><th style="text-align:left;padding:8px;border-bottom:1px solid var(--line)">License</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</div></section>'''
    # table cells need a bit of padding via a style already inline
    main = main.replace("<td>", '<td style="padding:8px;border-bottom:1px solid var(--line);vertical-align:top">')
    return document(
        "Photo Credits | SimpleINSURE",
        "Photograph credits and licenses for the SimpleINSURE website.",
        "/photo-credits/",
        main,
    )


def contact_page():
    steps = f'''
<div data-step="1" data-label="Message" data-error="Add your name, and an email or a phone number.">
  <h2 style="font-size:32px;margin-bottom:14px">Send a note</h2>
  <p class="quiet">Nothing on this form is stored on the website.</p>
  <div class="fields" style="margin-top:16px">{contact_fields("c")}</div>
  <p class="quiet">By sending this you agree that a broker may contact you about the note. There is no obligation.</p>
</div>'''
    short = f'''
<div data-step="1" data-label="Message" data-error="Add your name, and an email or a phone number.">
  <h2 class="desk-h">Send a note</h2>
  <p class="quiet">Nothing on this form is stored on the website.</p>
  <div class="fields">
    {field("sname", "Full name", required=True, full=True, attrs='autocomplete="name"')}
    {field("semail", "Email", kind="email", need="email", attrs='autocomplete="email"')}
    {field("sphone", "Phone", kind="tel", need="phone", attrs='autocomplete="tel"')}
    {field("snotes", "Anything we should know", kind="textarea", full=True)}
  </div>
  <p class="quiet">By sending this you agree that a broker may contact you about the note. There is no obligation.</p>
</div>'''
    main = page_head(
        "Contact",
        "Call, or send a note.",
        "A broker replies by phone or email. If it's urgent, call.",
        cls="contact-head",
        lede_cls="hide-1024",
        place="Garden City, Long Island, and New York City.",
    ) + f'''
<section class="contact-desk only-1024" aria-label="Office">
  <div class="contact-split">
    <div class="contact-form" data-rise>{wizard("Contact", "Email this note", short)}</div>
    <figure class="contact-visual rise-photo">
      {pic("facade", eager=True, sizes="(min-width: 1024px) 58vw, 100vw")}
      <figcaption>
        <a class="reach-call" href="{TEL}">{PHONE}</a>
        <a class="reach-mail" href="{MAIL}">{EMAIL}</a>
        <p class="reach-addr">{ADDR}</p>
      </figcaption>
    </figure>
  </div>
</section>
<section class="section hide-1024" style="padding-top:28px"><div class="wrap layout">{wizard("Contact", "Email this note", steps)}{aside()}</div></section>'''
    return document(
        "Contact Our Garden City Office | SimpleINSURE",
        "Call (516) 226-7969 or write SimpleINSURE Brokerage, 900 Stewart Ave Ste 210, Garden City, NY 11530.",
        "/contact/",
        main,
    )


def not_found():
    main = page_head(
        "Missing page",
        "That page is not on this site.",
        "The address may be old. The pages below are current.",
    ) + '''<section class="section" style="padding-top:0"><div class="wrap ress">
      <a href="/"><h3>Home</h3><p>The firm and the practices.</p></a>
      <a href="/policy-review/"><h3>Policy review</h3><p>A second reading of a current policy.</p></a>
      <a href="/contact/"><h3>Contact</h3><p>Call, or send a note.</p></a>
    </div></section>'''
    return document(
        "Page Not Found | SimpleINSURE",
        "That address is not a page on this site. Start from the home page or call the Garden City office.",
        "/404.html",
        main,
    )


def coverage_page():
    page_for = {
        "real-estate": ("/building-owner-insurance/", "Building insurance"),
        "hospitality": ("/restaurant-insurance/", "Restaurant insurance"),
        "construction": ("/contractor-insurance/", "Contractor insurance"),
    }
    bands = []
    for ind in INDUSTRIES:
        slug = ind["slug"]
        name = ind["nav"]
        lines = "".join(
            f"<li><b>{h(a)}</b></li>" for a, b in ind["coverages"][:4]
        )
        first = ind["key"] == "estate"
        photo_cls = "stage-photo is-estate" if first else "stage-photo rise-photo"
        more = f'<a class="more" href="/policy-review/">Request a review {ARROW}</a>'
        if slug in page_for:
            href, label = page_for[slug]
            more += f'<a class="more" href="{href}">{h(label)} {ARROW}</a>'
        bands.append(f'''
<section class="stage" id="{slug}">
  <figure class="{photo_cls}">{pic(ind["key"], eager=first, sizes="100vw")}</figure>
  <div class="stage-copy" data-rise>
    <h2 class="rise"><span class="line"><span>{h(name)}</span></span></h2>
    <p class="lede">{h(ind["lede"])}</p>
    <ul class="stage-lines">{lines}</ul>
    {more}
  </div>
</section>''')
    main = '''<header class="page-head cover-head"><div class="wrap"><p class="kicker m-only">Coverage</p><h1 class="rise"><span class="line"><span>Five practices.<br class="only-1024"> One account.</span></span></h1><h2 class="place-line">Commercial and personal insurance for Nassau, Long Island, and New York City.</h2><p class="lede">One broker for the business and the household.</p></div></header>''' + "".join(bands)
    return document(
        "Insurance Coverage in New York City and Long Island | SimpleINSURE",
        "Commercial and personal coverage for real estate, restaurants, contractors, and offices, from a Garden City broker.",
        "/coverage/",
        main,
    )


def policy_hub():
    concerns = [
        "The price",
        "The limits",
        "An exclusion or a sublimit",
        "A certificate or a contract",
        "A renewal that is coming up",
        "A claim",
        "I am not sure",
    ]
    chips = []
    for i, label in enumerate(concerns):
        fid = f"concern-{i}"
        chips.append(f'<label for="{fid}"><input id="{fid}" name="{fid}" type="checkbox"> {h(label)}</label>')
    read_steps = f'''
<div data-step="1" data-label="Account" data-error="Choose what the policy covers.">
  <h2 style="font-size:32px;margin-bottom:8px">What does the current policy cover?</h2>
  <p class="quiet">Nothing on this form is stored on the website.</p>
  <div style="margin-top:16px">{line_choices()}</div>
</div>
<div data-step="2" data-label="The policy" hidden>
  <h2 style="font-size:32px;margin-bottom:8px">What should we check?</h2>
  <p class="quiet">Pick any. Estimates are fine.</p>
  <div class="chips" style="margin:16px 0">{"".join(chips)}</div>
  <div class="fields">
    {field("prem", "Current annual premium, if you know it")}
    {field("carrier", "Current carrier, if you want to say")}
    {field("renew", "Renewal or expiration date", kind="date")}
    {field("worry", "What concerns you", kind="textarea", full=True)}
  </div>
</div>
<div data-step="3" data-label="Contact" data-error="Add your name, and an email or a phone number." hidden>
  <h2 style="font-size:32px;margin-bottom:14px">Where should we reply?</h2>
  <div class="fields">{contact_fields("p")}</div>
</div>'''
    account_steps = f'''
<div data-step="1" data-label="Account" data-error="Choose what you want us to look at.">
  <h2 style="font-size:32px;margin-bottom:8px">What should we look at?</h2>
  <p class="quiet">Nothing on this form is stored on the website.</p>
  <div style="margin-top:16px">{line_choices("q")}</div>
</div>
<div data-step="2" data-label="Details" hidden>
  <h2 style="font-size:32px;margin-bottom:14px">About the account</h2>
  <div class="fields">
    {field("city", "City or ZIP", attrs='autocomplete="postal-code"')}
    {field("timing", "Timing", kind="select", options=["Renewal coming up", "New purchase or opening", "Mid-term", "Not sure"])}
    {field("insured", "Currently insured?", kind="select", options=["Yes", "No", "Not sure"])}
    {field("re-desc", "Property or portfolio", kind="textarea", show="real-estate", full=True)}
    {field("ho-concept", "Concept", show="hospitality")}
    {field("co-trade", "Trade", show="construction")}
    {field("pr-does", "What the business does", kind="textarea", show="professional", full=True)}
    {field("pe-what", "What to cover", kind="select", show="personal", options=["Home", "Auto", "Home and auto", "Umbrella", "Rental property"])}
    {field("un-about", "Describe what you want insured", kind="textarea", show="unsure", full=True)}
  </div>
</div>
<div data-step="3" data-label="Contact" data-error="Add your name, and an email or a phone number." hidden>
  <h2 style="font-size:32px;margin-bottom:14px">Where should we reply?</h2>
  <div class="fields">{contact_fields("q")}</div>
  <p class="quiet">By sending this you agree that a broker may contact you about the request. There is no obligation.</p>
</div>'''
    desk_steps = f'''
<div data-step="1" data-label="Account" data-error="Choose what the policy covers.">
  <p class="quiet">Nothing on this form is stored on the website.</p>
  <div class="fields">
    {field("dcover", "What does the current policy cover?", kind="select", required=True, full=True, options=[label for _val, label in LINES])}
    {field("dcarrier", "Current carrier, if you want to say")}
    {field("drenew", "Renewal or expiration date", kind="date")}
    {field("ddeliver", "The policy", kind="select", required=True, full=True, options=["I'll attach it to the email", "Email it to us"])}
  </div>
</div>
<div data-step="2" data-label="Contact" data-error="Add your name, and an email or a phone number." hidden>
  <h2 class="desk-h">Where should we reply?</h2>
  <div class="fields">
    {field("dname", "Full name", required=True, full=True, attrs='autocomplete="name"')}
    {field("demail", "Email", kind="email", need="email", attrs='autocomplete="email"')}
    {field("dphone", "Phone", kind="tel", need="phone", attrs='autocomplete="tel"')}
  </div>
</div>'''
    main = page_head(
        "Policy review",
        "Send the policy you have.",
        "Commercial and personal accounts. We read it first. If it's right, we say so.",
        cls="policy-head",
        lede_cls="hide-1024",
        place="A Garden City broker, for commercial and personal insurance.",
    ) + f'''
<section class="section desk-sheet only-1024"><div class="wrap">
  {wizard("Policy review", "Email this review", desk_steps)}
  <p class="quiet desk-bor">A broker of record letter changes who services your policy, if the insurer accepts it.</p>
</div></section>
<section class="section hide-1024" id="read" style="padding-top:36px"><div class="wrap">
  <div class="path-tabs" data-tabs>
    <div class="path-bar" role="tablist" aria-label="How to start">
      <button type="button" role="tab" data-tab="read">Read a current policy</button>
      <button type="button" role="tab" data-tab="account">Start from the account</button>
    </div>
    <div class="tab-panel is-on" id="panel-read" role="tabpanel"><div class="layout">{wizard("Policy review", "Email this review", read_steps)}{aside()}</div></div>
    <div class="tab-panel" id="panel-account" role="tabpanel">{wizard("Coverage review", "Email this request", account_steps)}</div>
  </div>
  <div class="prose handover" id="handover">
    <h2>How switching works</h2>
    <p>A broker of record letter changes who services your policy, if the insurer accepts it.</p>
  </div>
</div></section>'''
    return document(
        "Policy Review for Commercial and Personal Insurance | SimpleINSURE",
        "Send a current policy. A Garden City broker reads the commercial or personal forms. Nothing is stored on the website.",
        "/policy-review/",
        main,
    )


def _svc(num, title, blurb, subject, button, inner, extra="", claim=False):
    cls = "cc-item cc-claim" if claim else "cc-item"
    hot = f'<a class="cc-hot" href="{TEL}">Call {PHONE}</a>' if claim else ""
    return f'''<details class="{cls}" data-rise>
  <summary>
    <span class="cc-n">{num}</span>
    <span class="cc-main"><b>{h(title)}</b><em>{h(blurb)}</em></span>
    {hot}
    <span class="cc-go" aria-hidden="true">{ARROW}</span>
  </summary>
  <div class="cc-body"><div class="cc-inner">{extra}{wizard(subject, button, inner)}
    <p class="quiet cc-store">Nothing on this form is stored on the website.</p>
  </div></div>
</details>'''


def _who(prefix):
    return (
        field(prefix + "who", "Your name", required=True, full=True, attrs='autocomplete="name"')
        + field(prefix + "em", "Email", kind="email", need="email", attrs='autocomplete="email"')
        + field(prefix + "ph", "Phone", kind="tel", need="phone", attrs='autocomplete="tel"')
    )


def client_center():
    cert = _svc(
        "01",
        "Request a certificate",
        "Who it's for and when you need it.",
        "Certificate request",
        "Email this certificate request",
        f'''<div data-step="1" data-label="Certificate" data-error="Add your name, and an email or a phone number.">
          <div class="fields">
            {field("holder", "Certificate holder", required=True, full=True)}
            {field("haddr", "Holder address", full=True)}
            {field("ai", "Additional insured needed?", kind="select", options=["Yes", "No", "Not sure"])}
            {field("job", "Project, lease, or reason", kind="textarea", full=True)}
            {field("needby", "Needed by", kind="date")}
            {_who("c")}
          </div>
          <p class="quiet">We issue a certificate when the policy allows it. If it doesn't, we tell you.</p>
        </div>''',
    )
    cards = _svc(
        "02",
        "Request ID cards",
        "Auto ID cards for your vehicles.",
        "ID card request",
        "Email this ID card request",
        f'''<div data-step="1" data-label="ID cards" data-error="Add your name, and an email or a phone number.">
          <div class="fields">
            {field("ni", "Named insured", required=True, full=True)}
            {field("veh", "Vehicles or drivers", kind="textarea", full=True, hint="Vehicle year, make and model, or the last 4 of the VIN. Do not enter driver's license numbers.")}
            {field("send", "Where should we send them?", kind="select", options=["Email", "Text", "Either"])}
            {_who("i")}
          </div>
        </div>''',
    )
    change = _svc(
        "03",
        "Policy change",
        "A vehicle, a driver, a location, or payroll.",
        "Policy change",
        "Email this change",
        f'''<div data-step="1" data-label="Change" data-error="Add your name, and an email or a phone number.">
          <div class="fields">
            {field("kind", "What changed?", kind="select", required=True, options=["Add a vehicle", "Remove a vehicle", "Add a driver", "Remove a driver", "Add a location", "Remove a location", "Payroll or revenue change", "Other"])}
            {field("detail", "Tell us the change", kind="textarea", full=True, required=True)}
            {field("when", "Effective date, if you know it", kind="date")}
            {_who("g")}
          </div>
        </div>''',
    )
    claim = _svc(
        "04",
        "Report a claim",
        "Date, place, and what happened. If anyone is hurt or in danger, call 911 first. Call us if it is urgent.",
        "Claim report",
        "Email this claim note",
        f'''<div data-step="1" data-label="Claim" data-error="Add your name, and an email or a phone number.">
          <div class="fields">
            {field("cdate", "Date of loss", kind="date", required=True)}
            {field("cloc", "Location", required=True, full=True)}
            {field("what", "What happened", kind="textarea", full=True, required=True)}
            {field("inj", "Injuries?", kind="select", options=["Yes", "No", "Not sure"])}
            {field("rep", "Police or report number")}
            {field("photos", "Photos", kind="select", options=["I can attach photos to the email", "I do not have photos"])}
            {_who("k")}
          </div>
          <p class="quiet">Attach photos to the email draft. Describe what happened, not who was at fault. Your policy requires you to report the loss and cooperate with the insurer, and we will help with that.</p>
        </div>''',
        extra=f'<p class="callout">If anyone is hurt or in danger, call 911 first. If this is happening now, call <a href="{TEL}">{PHONE}</a> right away, or your insurer\'s claim line on your policy or ID card. Then send the note below.</p>',
        claim=True,
    )
    bill = _svc(
        "05",
        "Billing question",
        "Most premiums are paid to the insurance company. We can send the pay link.",
        "Billing question",
        "Email this billing question",
        f'''<div data-step="1" data-label="Billing" data-error="Add your name, and an email or a phone number.">
          <div class="fields">
            {field("bpol", "Policy or account")}
            {field("bask", "What do you need?", kind="textarea", full=True, required=True)}
            {_who("b")}
          </div>
        </div>''',
        extra="<p class=\"cc-note\">Most premiums are paid to the insurance company, and we can send the pay link. If we bill you, the invoice comes from SimpleINSURE Brokerage LLC and says where to pay.</p>",
    )
    renew = _svc(
        "06",
        "Renewal or cancellation",
        "A date coming up, or a policy you may end.",
        "Renewal or cancellation",
        "Email this question",
        f'''<div data-step="1" data-label="Renewal" data-error="Add your name, and an email or a phone number.">
          <div class="fields">
            {field("rpol", "Policy or account", full=True)}
            {field("rdate", "Renewal or cancellation date", kind="date")}
            {field("rwhy", "What do you need?", kind="select", options=["Renewal question", "Cancel a policy", "Something else"])}
            {field("rnote", "Notes", kind="textarea", full=True)}
            {_who("r")}
          </div>
        </div>''',
    )
    main = f'''<header class="photo-hero cc-hero">
  <div class="hero-media"><div class="ken">{pic("hero", eager=True, sizes="100vw")}</div><div class="hero-shade" aria-hidden="true"></div></div>
  <div class="wrap">
    <h1 class="rise"><span class="line"><span>Already a client?</span></span></h1>
    <h2 class="place-line">Client service from the Garden City office.</h2>
    <p class="lede">Certificates, ID cards, changes, claims, bills, and renewals.</p>
  </div>
</header>
<section class="cc-portal">
  <div id="portal" class="cc-login"><div class="wrap">
    <div class="ez-card"><iframe title="Customer Service Portal Login" src="https://customerservice.agentinsure.com/EzlynxCustomerService/simpleinsure/Account/LogIn" class="ez-frame block h-[672px] w-full border-0 sm:h-[622px]"><a href="https://customerservice.agentinsure.com/EzlynxCustomerService/simpleinsure/Account/LogIn" target="_blank" rel="noopener">Your browser cannot show the portal here. Open the EZLynx client portal, a third-party service, in a new tab.</a></iframe></div>
    <p class="cc-disclose"><a href="https://customerservice.agentinsure.com/EzlynxCustomerService/simpleinsure/Account/LogIn" target="_blank" rel="noopener">Client login (EZLynx)</a>. Opens a portal run by EZLynx, a third-party service with its own terms and privacy policy.</p>
  </div></div>
  <div class="wrap">  <div class="cc-layout">
  <div class="cc-list">{cert}{cards}{change}{claim}{bill}{renew}</div>
  </div></div>
</section>'''
    return document(
        "Client Center | Garden City Insurance Broker | SimpleINSURE",
        "Certificates, ID cards, changes, and claims for clients of SimpleINSURE Brokerage in Garden City.",
        "/client-center/",
        main,
    )


def about_hub():
    terms = [
        ("Additional insured", "A party added to a liability policy by endorsement. A certificate that names them does not create that status if the endorsement is missing."),
        ("Broker of record", "The broker appointed to service a policy. The appointment is a signed letter. It does not, by itself, rewrite the coverage."),
        ("Certificate of insurance", "A snapshot that a policy exists. It does not change the policy."),
        ("Declarations page", "The cover: named insured, dates, limits, deductibles, locations, and the form list. The forms control."),
        ("Endorsement", "A form that changes the policy. The surprises at claim time usually live here."),
        ("Loss payee", "A party paid for a covered property loss. It is not the same as an additional insured."),
        ("Umbrella", "Liability limits above the underlying policies. The underlying limits have to qualify."),
        ("Waiver of subrogation", "An endorsement in which the insurer gives up recovery against a named party."),
    ]
    gloss = "".join(f"<article><h3>{h(t)}</h3><p>{h(d)}</p></article>" for t, d in terms)
    main = page_head(
        "The firm",
        "An independent brokerage.",
        "We work for you, not for any one insurance company.",
        cls="firm-head",
        place="Garden City, Long Island, and New York City.",
    ) + f'''
<section class="section firm-desk only-1024">
  <div class="wrap firm-split">
    <div class="firm-panel" data-rise><p class="firm-panel-eye">The firm</p><p class="firm-panel-place">Garden City, New York</p></div>
    <div class="firm-copy" data-rise>
      <p class="firm-role">Principal</p>
      <h2>Remy Mehdizadeh</h2>
      <p>Remy Mehdizadeh, a licensed New York property and casualty broker, founded the firm so owners have one broker who reads the policy and stays after it's bound.</p>
      <p class="firm-office">{ADDR}</p>
      <p class="firm-reach"><a href="{TEL}">{PHONE}</a> · <a href="{MAIL}">{EMAIL}</a></p>
    </div>
  </div>
  <div class="wrap">
    <p class="firm-note">© 2026 SimpleINSURE Brokerage LLC, licensed New York property and casualty insurance broker, NY DFS License No. BR-1984615. Coverage descriptions are general summaries. The issued policy governs. New York Insurance Law section 2116 limits referral fees and commission sharing to licensed persons.</p>
  </div>
</section>
<section class="section hide-1024" style="padding-top:12px"><div class="wrap split">
  <div class="prose">
    <h2>An independent practice</h2>
    <p>SimpleINSURE Brokerage LLC works with a range of insurance companies, including specialty markets.</p>
    <p>Remy Mehdizadeh, a licensed New York property and casualty broker, founded the firm so owners have one broker who reads the policy and stays after it's bound. Both licenses are on the <a href="/legal/">licenses page</a>. We're usually paid a commission by the insurer, and you can ask what we expect on your policy.</p>
    <p><a href="{TEL}">{PHONE}</a> · <a href="{MAIL}">{EMAIL}</a></p>
  </div>
  {figure_block("hero", "(max-width: 980px) 100vw, 40vw")}
</div></section>
<section class="section hide-1024" id="partners" style="padding-top:0"><div class="wrap prose narrow">
  <h2>For advisors</h2>
  <p>Attorneys, property managers, and accountants: introduce a client and we'll call them. With their OK, we keep you posted.</p>
  <p>New York Insurance Law section 2116 limits referral fees and commission sharing to licensed persons.</p>
  <p><a href="/contact/">Introduce a client</a></p>
</div></section>'''
    return document(
        "About Our Garden City Insurance Brokerage | SimpleINSURE",
        "An independent commercial and personal insurance broker in Garden City, for Long Island and New York City.",
        "/about/",
        main,
    )


SERVICES = [
    {
        "path": "/restaurant-insurance/",
        "key": "hospitality",
        "kicker": "Restaurants",
        "title": "Restaurant Insurance in NYC and Long Island | SimpleINSURE",
        "desc": "Restaurant and hospitality insurance for New York City and Long Island, from a Garden City broker.",
        "h1": "Restaurant insurance.",
        "place": "New York City and Long Island.",
        "overlay_h": "What we place",
        "overlay_p": "Property, liability, and liquor liability when alcohol is served. Workers compensation where the law requires it.",
        "help_h": "How we help",
        "help_p": "We read the lease and the policy you already have, then tell you what is in place.",
        "next_h": "The next step",
        "next_p": "Send the policy. A broker in Garden City walks you through it.",
    },
    {
        "path": "/contractor-insurance/",
        "key": "construction",
        "kicker": "Contractors",
        "title": "Contractor Insurance in New York | SimpleINSURE",
        "desc": "Contractor insurance for trades in New York City and on Long Island. We read the contract first.",
        "h1": "Contractor insurance.",
        "place": "New York City and Long Island.",
        "overlay_h": "What we place",
        "overlay_p": "Liability, workers compensation, and auto, lined up with the contract.",
        "help_h": "How we help",
        "help_p": "We start with the insurance exhibit and say what the current policy can support.",
        "next_h": "The next step",
        "next_p": "Send the contract or the policy you have.",
    },
    {
        "path": "/building-owner-insurance/",
        "key": "estate",
        "kicker": "Real estate",
        "title": "Building Owner Insurance in Garden City and NYC | SimpleINSURE",
        "desc": "Insurance for building owners and real estate in Garden City, Nassau, Long Island, and New York City.",
        "h1": "Building owner insurance.",
        "place": "Real estate in New York.",
        "overlay_h": "What we place",
        "overlay_p": "Property, liability, and umbrella for a building or a schedule of buildings.",
        "help_h": "How we help",
        "help_p": "We start with the address, the loan wording, and the policy you have.",
        "next_h": "The next step",
        "next_p": "Send the policy, or the insurance section of the loan.",
    },
]


def service_page(spec):
    main = f'''<header class="photo-hero service-hero">
  <div class="hero-media"><div class="ken">{pic(spec["key"], eager=True, sizes="100vw")}</div><div class="hero-shade" aria-hidden="true"></div></div>
  <div class="wrap">
    <p class="kicker m-only">{h(spec["kicker"])}</p>
    <h1 class="rise"><span class="line"><span>{h(spec["h1"])}</span></span></h1>
    <h2 class="place-line">{h(spec["place"])}</h2>
  </div>
</header>
<section class="service-rest"><div class="wrap">
  <h2>{h(spec["overlay_h"])}</h2>
  <p>{h(spec["overlay_p"])}</p>
  <h2>{h(spec["help_h"])}</h2>
  <p>{h(spec["help_p"])}</p>
  <h2>{h(spec["next_h"])}</h2>
  <p>{h(spec["next_p"])}</p>
  <a class="btn" href="/policy-review/">Request a review {ARROW}</a>
</div></section>'''
    return document(spec["title"], spec["desc"], spec["path"], main, current="/coverage/")


def redirect_page(from_key, target):
    frag = ""
    path = target
    if "#" in target:
        path, frag = target.split("#", 1)
        frag = "#" + frag
    if path != "/" and not path.endswith("/"):
        path += "/"
    depth = from_key.count("/")
    if path == "/":
        rel = "../" * depth or "./"
    else:
        rel = ("../" * depth) + path.lstrip("/")
    rel += frag
    canon = SITE + (path if path != "/" else "/")
    label = from_key[: -len("/index.html")].replace("/", " ")
    title = f"Moved: {label} | SimpleINSURE"
    desc = f"The {label} page now lives at {path}."
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{h(title)}</title>
<meta name="description" content="{h(desc)}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{h(canon)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{h(title)}">
<meta property="og:description" content="{h(desc)}">
<meta property="og:url" content="{h(canon)}">
<meta property="og:image" content="{SITE}/img/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{h(title)}">
<meta name="twitter:description" content="{h(desc)}">
<meta name="twitter:image" content="{SITE}/img/og.png">
<meta http-equiv="refresh" content="0; url={h(rel)}">
</head>
<body>
<h1>This page has moved.</h1>
<p><a href="{h(rel)}">Continue</a></p>
</body>
</html>'''


REDIRECTS = {
    "coverage/real-estate/index.html": "/building-owner-insurance/",
    "coverage/hospitality/index.html": "/restaurant-insurance/",
    "coverage/construction/index.html": "/contractor-insurance/",
    "coverage/professional/index.html": "/coverage/",
    "coverage/personal/index.html": "/coverage/",
    "coverage/auto/index.html": "/coverage/",
    "coverage/home/index.html": "/coverage/",
    "coverage/umbrella/index.html": "/coverage/",
    "coverage/business/index.html": "/coverage/",
    "coverage/excess-and-surplus-lines/index.html": "/coverage/",
    "coverage/general-liability/index.html": "/coverage/",
    "coverage/workers-compensation/index.html": "/coverage/",
    "checklists/index.html": "/coverage/",
    "needs/index.html": "/coverage/",
    "quote/index.html": "/policy-review/",
    "resources/index.html": "/about/",
    "partners/index.html": "/about/",
    "switching/index.html": "/policy-review/",
    "articles/index.html": "/about/",
    "photo-credits/index.html": "/",
    "style-preview/index.html": "/",
    "new-york-building-insurance/index.html": "/building-owner-insurance/",
    "new-york-contractor-insurance/index.html": "/contractor-insurance/",
    "new-york-restaurant-insurance/index.html": "/restaurant-insurance/",
}


def pages():
    out = {
        "index.html": home(),
        "coverage/index.html": coverage_page(),
        "policy-review/index.html": policy_hub(),
        "client-center/index.html": client_center(),
        "about/index.html": about_hub(),
        "contact/index.html": contact_page(),
        "legal/index.html": legal_page(),
        "404.html": not_found(),
    }
    for spec in SERVICES:
        out[spec["path"].strip("/") + "/index.html"] = service_page(spec)
    for key, target in REDIRECTS.items():
        out[key] = redirect_page(key, target)
    return out
