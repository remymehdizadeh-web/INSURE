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
    if "unsplash.com" not in _c.get("page", ""):
        _title = _c["title"].replace(" ", "_")
        _c["page"] = "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(_title, safe="()'-._~")

DIMS = {
    "hero": (1600, 1067),
    "estate": (1600, 1067),
    "hospitality": (1600, 1067),
    "construction": (1600, 1067),
    "professional": (1600, 1067),
    "personal": (1600, 1067),
}


def h(value):
    return html_lib.escape(str(value), quote=True)


# Same file family at every width. The query busts a cached estate-800 that was a different photograph.
PHOTO_V = "4"


def photo_src(key, width):
    return f"/photos/{key}-{width}.webp?v={PHOTO_V}"


def pic(key, eager=False, sizes="(max-width: 860px) 100vw, 46vw"):
    c = CRED[key]
    w, height = DIMS[key]
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    return (
        f'<img src="{photo_src(key, 800)}" '
        f'srcset="{photo_src(key, 800)} 800w, {photo_src(key, 1200)} 1200w, {photo_src(key, 1600)} 1600w" '
        f'sizes="{sizes}" alt="{h(c["alt"])}" width="{w}" height="{height}" {load}>'
    )


def cred(key):
    c = CRED[key]
    # One inline span so spaces survive if a parent is a flex container.
    return (
        '<span class="cap">Photograph by '
        f'<a href="{h(c["page"])}" rel="noopener">{h(c["artist"])}</a>, '
        f'<a href="{h(c["license_url"])}" rel="noopener">{h(c["license"])}</a></span>'
    )


def arcs():
    rings = [
        (280, 90, 0.16, "#5BA4E5"),
        (280, 2.4, 0.8, "#C5E6FA"),
        (430, 70, 0.13, "#3D86C4"),
        (430, 2, 0.7, "#9ED4F8"),
        (590, 110, 0.14, "#7EBFEE"),
        (590, 2.6, 0.85, "#E7F6FF"),
        (770, 64, 0.11, "#5BA4E5"),
        (770, 1.8, 0.6, "#8ECAF5"),
        (980, 86, 0.12, "#2F6FB0"),
        (980, 2.2, 0.75, "#B9DFF8"),
        (1200, 48, 0.1, "#5BA4E5"),
    ]
    circles = "".join(
        f'<circle cx="120" cy="430" r="{r}" style="fill:none;stroke:{c};stroke-width:{sw};opacity:{op}"/>'
        for r, sw, op, c in rings
    )
    return (
        '<div class="arcs" aria-hidden="true"><div class="arc-glow"></div>'
        '<svg viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice">'
        f'<g class="arc-drift"><g class="arc-spin">{circles}</g></g></svg></div>'
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
            "streetAddress": "900 Stewart Ave Ste 210",
            "addressLocality": "Garden City",
            "addressRegion": "NY",
            "postalCode": "11530",
            "addressCountry": "US",
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
    parts = ['<a href="/coverage/">Coverage</a>']
    for href, title, _sub, *_r in COVER:
        parts.append(f'<a class="sub" href="{href}">{h(title)}</a>')
    for href, label in (
        ("/policy-review/", "Policy review"),
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
      {top("/policy-review/", "Policy review")}
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
      <li><a href="{TEL}">{PHONE}</a></li>
      <li><a href="{MAIL}">{EMAIL}</a></li>
    </ul></div>
  </div>
  <div class="wrap legal-line">
    <span>© 2026 SimpleINSURE Brokerage LLC. Coverage descriptions are general summaries. The issued policy governs.</span>
    <a href="/legal/">Licenses and disclosures</a>
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
          <li><a href="{TEL}">{PHONE}</a></li>
          <li><a href="{MAIL}">{EMAIL}</a></li>
        </ul></div>
        <div><h2>Office</h2><ul>
          <li><a href="{TEL}">{PHONE}</a></li>
          <li><a href="{MAIL}">{EMAIL}</a></li>
          <li>{ADDR}</li>
        </ul></div>
      </div>
      <p class="m-legal">© 2026 SimpleINSURE Brokerage LLC. Coverage descriptions are general summaries. The issued policy governs.</p>
      <p class="m-legal"><a href="/legal/">Licenses and disclosures</a></p>
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
<link rel="preload" as="image" href="{photo_src("hero", 1600)}" imagesrcset="{photo_src("hero", 800)} 800w, {photo_src("hero", 1200)} 1200w, {photo_src("hero", 1600)} 1600w" imagesizes="100vw" fetchpriority="high">'''
    body = "page-home" if cinematic else "page-inner"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
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
<link rel="preload" href="/fonts/franklin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/site.css?v=6">
<style>
.m-only{{display:none}}
@media (max-width:980px){{
  .site-header{{position:fixed !important;top:max(12px,env(safe-area-inset-top)) !important;left:0 !important;right:0 !important;padding-top:0 !important;z-index:80 !important;transform:translate3d(0,var(--header-shift,0px),0)}}
  .site-header:before{{content:"";position:absolute;left:0;right:0;bottom:100%;height:max(12px,env(safe-area-inset-top));background:#071018;pointer-events:none}}
  html.veil .site-header:before{{background:#fff;height:max(12px,env(safe-area-inset-top));top:auto;bottom:100%}}
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
<link rel="stylesheet" href="/mobile.css?v=4">
<script>document.documentElement.classList.toggle("scrolled",(window.scrollY||0)>8);if(matchMedia("(max-width:980px)").matches)document.documentElement.classList.add("is-mobile");if(!matchMedia("(prefers-reduced-motion: reduce)").matches)document.documentElement.classList.add("motion")</script>
{preload}
<script type="application/ld+json">{schema(path)}</script>
{extra}
</head>
<body class="{body}">
{header(cur)}
<main id="main">{main}</main>
{footer() if show_footer else ""}
<script src="/vendor/gsap.min.js" defer></script>
<script src="/vendor/ScrollTrigger.min.js" defer></script>
<script src="/vendor/lenis.min.js" defer></script>
<script src="/site.js?v=4" defer></script>
</body>
</html>'''


def cinematic_sections(eager=False):
    blurbs = {
        "estate": "Buildings, schedules, lenders.",
        "hospitality": "Restaurants, bars, the lease.",
        "construction": "Trades, contracts, certificates.",
        "professional": "Offices and professional firms.",
        "personal": "Home, auto, and the household.",
    }
    slides = []
    for href, title, _sub, key in COVER:
        slides.append(
            f'<div class="slide{" slide-hospitality" if key == "hospitality" else ""}">'
            f'{pic(key, eager=eager, sizes="(max-width: 980px) 100vw, 62vw")}'
            f'<span class="slide-shade" aria-hidden="true"></span>'
            f'<a class="slide-hit" href="{href}"><span class="sr">{h(title)}</span></a>'
            f'<span class="slide-copy"><strong>{h(title)}</strong> <small>{h(blurbs[key])}</small></span>'
            f'</div>'
        )
    return f'''
<section class="hero" aria-label="Introduction">
  <div class="hero-media">
    <div class="ken">{pic("hero", eager=True, sizes="100vw")}</div>
    <div class="hero-shade" aria-hidden="true"></div>
  </div>
  <div class="hero-copy wrap">
    <h1 class="rise"><span class="line"><span>The standard</span></span><span class="line"><span>a broker should</span></span><span class="line"><span><em>already meet.</em></span></span></h1>
    <p class="lede">Send the policy you have. We read it before we talk about replacing it.</p>
    <div class="cta-row">
      <a class="btn btn-light magnet" href="/policy-review/">Request a review {ARROW}</a>
      <a class="m-phone m-only" href="{TEL}">{PHONE}</a>
      <a class="text-link on-dark" href="/policy-review/#read">Review a current policy</a>
    </div>
  </div>
  <a class="scroll-cue" href="#practices"><span class="sr">Practices</span><i aria-hidden="true"></i></a>
</section>
<section class="h-pin" id="practices" aria-labelledby="practices-h">
  <div class="h-sticky">
    <div class="h-intro">
      <div class="h-copy">
        <h2 class="rise" id="practices-h"><span class="line"><span>Five</span></span><span class="line"><span>practices.</span></span></h2>
        <p>Buildings, hospitality, contracting, offices, and the household.</p>
      </div>
    </div>
    <div class="h-track">{''.join(slides)}</div>
  </div>
</section>
<section class="case" id="case-study" aria-labelledby="case-h">
  <figure class="case-bleed">
    {pic("hospitality", eager=eager, sizes="(max-width: 980px) 100vw, 58vw")}
  </figure>
  <div class="case-copy">
    <h2 class="rise" id="case-h"><span class="line"><span>Same limits.</span></span><span class="line"><span><em>A wider umbrella.</em></span></span></h2>
    <p class="story">A Manhattan restaurant. Liability limits stayed. The umbrella rose from $1 million to $5 million, and employment practices liability was added. The prior program had excluded it.</p>
    <div class="money" aria-label="Annual premium went from 71196 dollars to 21309 dollars">
      <div class="money-row before"><span class="lab">Before</span><span class="fig" data-count="71196">$71,196</span></div>
      <div class="money-row"><span class="lab">After</span><span class="fig" data-count="21309">$21,309</span></div>
      <p class="delta">$49,887 less a year.</p>
      <p class="fine">The figures are the annual premium of the prior program and the new program as proposed, before any broker service fee. The difference is $49,887. The client and the prior broker are not named. Every account is different, and the result depends on underwriting.</p>
    </div>
    <div class="cta-row"><a class="btn btn-light magnet" href="/policy-review/">Send a policy for review {ARROW}</a></div>
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
        ("Read", "Declarations, forms, and the endorsements behind them."),
        ("Say so", "If the current program is already right, we say so."),
        ("Market", "Only when there is a reason to move the account."),
        ("Hand over", "Dates, certificates, and the renewal calendar."),
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
    return f'''
<div class="m-home m-only">
<section class="m-block">
  <div class="wrap">
    <p class="m-eye"><i aria-hidden="true"></i>Practices</p>
    <h2>Five<span class="b">practices.</span></h2>
    <p class="m-lead">Buildings, hospitality, contracting, offices, and the household.</p>
    <div class="m-tiles">{''.join(tiles)}</div>
  </div>
</section>
<section class="m-block" style="padding-top:8px">
  <div class="wrap">
    <p class="m-eye"><i aria-hidden="true"></i>Coverage</p>
    <h2>Commercial and<span class="b">personal.</span></h2>
    <div class="m-tabs" data-tabs>
      <div class="m-tabbar" role="tablist" aria-label="Coverage lists">
        <button type="button" role="tab" data-tab="practices">Practices</button>
        <button type="button" role="tab" data-tab="steps">The work</button>
      </div>
      <div class="tab-panel is-on" id="panel-practices" role="tabpanel"><ol class="m-num">{''.join(practices)}</ol></div>
      <div class="tab-panel" id="panel-steps" role="tabpanel"><ol class="m-num m-num-notes">{step_html}</ol><p class="m-more"><a href="/policy-review/#handover">How the handover works {ARROW}</a></p></div>
    </div>
  </div>
</section>
<section class="m-block alt">
  <div class="wrap">
    <p class="m-eye"><i aria-hidden="true"></i>A placed account</p>
    <h2>Same limits.<span class="b">A wider umbrella.</span></h2>
    <p class="m-lead">A Manhattan restaurant. Liability limits stayed. The umbrella rose from $1 million to $5 million, and employment practices liability was added. The prior program had excluded it.</p>
    <div class="m-fig"><div><span>Before</span><b>$71,196</b></div><i style="--w:100%"></i></div>
    <div class="m-fig"><div><span>After</span><b>$21,309</b></div><i style="--w:30%"></i></div>
    <div class="m-card">
      <p class="m-eye"><i aria-hidden="true"></i>The difference</p>
      <h3>$49,887</h3>
      <p>less a year.</p>
      <p class="fine">The figures are the annual premium of the prior program and the new program as proposed, before any broker service fee. The difference is $49,887. The client and the prior broker are not named. Every account is different, and the result depends on underwriting.</p>
    </div>
  </div>
</section>
<section class="m-block">
  <div class="wrap">
    <p class="m-eye"><i aria-hidden="true"></i>The standard</p>
    <h2>What we will<span class="b">not do.</span></h2>
    <div class="faq">{faq_html}</div>
  </div>
</section>
</div>
'''


def home():
    return document(
        "Commercial and Personal Insurance | SimpleINSURE",
        "SimpleINSURE places commercial and personal insurance. Send the policy you have. We read it, approach A-rated markets when there is a reason, and stay after it is bound.",
        "/",
        cinematic_sections() + mobile_home() + f'''
<section class="section work" id="work" aria-labelledby="work-h">
  <div class="wrap work-grid">
    <div class="work-intro">
      <h2 class="rise" id="work-h"><span class="line"><span>Switching is</span></span><span class="line"><span>a sequence.</span></span></h2>
      <p>We read what you have before anyone is asked to sign a broker of record letter. If it should stay, that is the answer.</p>
      <a class="text-link" href="/policy-review/#handover">How the handover works {ARROW}</a>
    </div>
    <ol class="work-steps">
      <li><div><h3>Read</h3><p>Declarations, forms, and the endorsements behind them.</p></div></li>
      <li><div><h3>Say so</h3><p>If the current program is already right, we say so.</p></div></li>
      <li><div><h3>Market</h3><p>Only when there is a reason to move the account.</p></div></li>
      <li><div><h3>Hand over</h3><p>Dates, certificates, and the renewal calendar.</p></div></li>
    </ol>
  </div>
</section>
<section class="close" aria-labelledby="close-h">
  <div class="hero-media">
    <div class="ken">{pic("personal", sizes="100vw")}</div>
    <div class="hero-shade" aria-hidden="true"></div>
  </div>
  <div class="wrap close-inner">
    <h2 class="rise" id="close-h"><span class="line"><span>Bring the policy</span></span><span class="line"><span><em>you have.</em></span></span></h2>
    <p>We will tell you what it does, including when the right answer is to keep it.</p>
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


def field(fid, label, kind="text", options=None, required=False, show=None, full=False, need=None, attrs=""):
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
    return f'<div class="{cls}"{show_attr}><label for="{fid}">{h(label)}</label>{control}</div>'


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
      <p class="lede">An email draft to <a href="{MAIL}">{EMAIL}</a> should be open. If it is not, open it below. Nothing on this form is stored on the website. If you have a declarations page or a contract, attach it to that email.</p>
      <div class="summary"></div>
      <div class="done-actions">
        <a class="btn" data-mailto href="{MAIL}">Open the email draft <span class="arr" aria-hidden="true">→</span></a>
        <button type="button" class="btn-ghost" data-copy>Copy the summary</button>
        <a class="btn-ghost" href="{TEL}">Call {PHONE}</a>
      </div>
    </div>'''


def wizard(subject, final, steps):
    return f'''<form class="wizard" data-subject="{h(subject)}" data-final="{h(final)}" novalidate>
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
      <div class="panel"><h2>Nothing is stored here</h2>
        <p>The form opens an email in your own mail program. This website does not keep the answers.</p></div>
    </aside>'''


def page_head(kicker, title, lede=""):
    lead = f'<p class="lede">{h(lede)}</p>' if lede else ""
    eye = f'<p class="kicker m-only">{h(kicker)}</p>' if kicker else ""
    return f'<header class="page-head"><div class="wrap">{eye}<h1 class="rise"><span class="line"><span>{h(title)}</span></span></h1>{lead}</div></header>'


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
        "lede": "Apartment, mixed-use, and commercial property. One building or a schedule. The loan wording is part of the placement.",
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
        "lede": "Property, liability, liquor, and the statutory lines a staff requires. The lease usually sets the floor.",
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
        "lede": "General liability, compensation, auto, and the certificate wording upstream parties actually ask for.",
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
        "lede": "Offices, retail, and professional practices. The package is only the start if you give advice or hold data.",
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
        "lede": "Personal insurance for people who also own a company, a building, or a rental.",
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
  <p class="quiet">Choose one. You can add detail on the next step.</p>
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
        ("A market, only if there is a reason", "We approach carriers that write this kind of risk, including specialty markets when the standard market is a poor fit. Access to A-rated carriers is the point of that work. The account goes to market with a purpose."),
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
    ("Admitted carrier", "An insurer licensed to write a line of insurance in a given state. Admitted status is not the same thing as a financial strength rating. A placement can also use surplus lines when the admitted market is not a fit."),
    ("A-rated", "A shorthand for a strong financial strength rating from a rating service such as A.M. Best, often A- or better. It describes the carrier's financial size and strength. It is not a promise that a particular policy is the right one."),
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
    ("Surplus lines", "Insurance placed with a carrier that is not admitted in the state, through a licensed surplus lines process, when the admitted market will not write the risk. It is a legitimate market, not a workaround to hide."),
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
        "The premium is the last comparison, not the first. A lower price with a lower limit, a higher deductible, or a missing endorsement is not a saving. The Manhattan restaurant we describe on the home page kept its liability limits, raised the umbrella, and added employment practices. The premium fell because the program was rewritten, not because coverage was stripped.",
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
  <p>Call {PHONE}. Note the date, the place, and who was involved. Photograph what you safely can. Do not guess at fault in a written statement to anyone but your broker and, through us, the carrier. Send the suit papers the day you receive them. Late notice is an avoidable way to damage a claim.</p>
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
        "We place coverage for the client and stay with the account.",
    ) + f'''
<section class="section" style="padding-top:12px"><div class="wrap split">
  <div class="prose">
    <h2>An independent practice</h2>
    <p>SimpleINSURE Brokerage LLC places commercial and personal insurance for the client, not for a single carrier. Admitted markets, specialty markets, and surplus lines are all in reach, with access to A-rated carriers when the risk calls for them.</p>
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
  <p>SimpleINSURE Brokerage LLC is a licensed property and casualty insurance broker. New York DFS license number BR-1984615. You can confirm that record on the <a href="https://myportal.dfs.ny.gov/nylinxext/elsearch.alice" rel="noopener">New York DFS licensee search</a>.</p>
  <p>{ADDR}. Phone <a href="{TEL}">{PHONE}</a>. Email <a href="{MAIL}">{EMAIL}</a>.</p>
  <p>We place insurance where we are licensed to do so. This page states the New York license. It does not claim licenses in other states. If an account requires a license we do not yet hold, we will say so before an appointment or a placement.</p>
  <h2 id="how-we-are-paid">How we are paid</h2>
  <p>We are usually paid a commission by the insurer that issues the policy, as a percentage of premium. We may also receive other compensation from insurers, such as contingent payments based on the overall business placed with them. You may ask what compensation we expect on your policy, and about alternative quotes we presented. We will tell you.</p>
  <p>This description is our disclosure of compensation. It is not a quote for your account.</p>
  <h2 id="not-a-binder">Not an offer or a binder</h2>
  <p>Descriptions on this website are general. They do not amend a policy and they are not an offer to insure. Coverage is subject to underwriting and to the forms that are issued. The policy governs.</p>
  <h2 id="privacy">Privacy</h2>
  <p>Forms on this site do not submit to a server we control. They open an email draft in your own mail program, addressed to {EMAIL}. We do not sell personal information. We do not set advertising cookies on this site. If you email or call, we use what you send to respond and to work on the account.</p>
  <p>Do not include medical details, Social Security numbers, or full payment card numbers in a web email. A declarations page is enough to start a review.</p>
</div></section>'''
    return document(
        "Licenses and Disclosures | SimpleINSURE",
        "New York DFS license BR-1984615, compensation disclosure, and privacy notice for SimpleINSURE Brokerage LLC.",
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
  <p>Photographs are used under the Unsplash License. Credit is optional. It is listed here and is not shown on the other pages.</p>
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
  <p class="quiet">The button opens an email draft to {EMAIL}. This page does not store what you type.</p>
  <div class="fields" style="margin-top:16px">{contact_fields("c")}</div>
  <p class="quiet">By sending this you agree that a broker may contact you about the note. There is no obligation.</p>
</div>'''
    main = page_head(
        "Contact",
        "Call, or send a note.",
        "A broker replies by phone or email. If it is urgent, call. The form opens a draft in your own mail program.",
    ) + f'''<section class="section" style="padding-top:28px"><div class="wrap layout">{wizard("Contact", "Email this note", steps)}{aside()}</div></section>'''
    return document(
        "Contact | SimpleINSURE",
        "Call SimpleINSURE or send a note. The form opens an email to the brokerage. Nothing is stored on the website.",
        "/contact/",
        main,
    )


def not_found():
    main = page_head(
        "Missing page",
        "That page is not on this site.",
        "The address may be old. The pages below are current.",
    ) + '''<section class="section" style="padding-top:0"><div class="wrap ress">
      <a href="/"><h3>Home</h3><p>The firm, the case study, and the practices.</p></a>
      <a href="/policy-review/"><h3>Policy review</h3><p>A second reading of a current policy.</p></a>
      <a href="/contact/"><h3>Contact</h3><p>Call, or send a note.</p></a>
    </div></section>'''
    return document("Page not found | SimpleINSURE", "That page is not on the SimpleINSURE site.", "/404.html", main)


def coverage_page():
    tiles = []
    jumps = []
    bands = []
    for i, ind in enumerate(INDUSTRIES):
        slug = ind["slug"]
        name = ind["nav"]
        href = f"/coverage/#{slug}"
        wide = " m-tile-wide" if i == len(INDUSTRIES) - 1 else ""
        tiles.append(
            f'<a class="m-tile{wide}" href="#{slug}">'
            f'{pic(ind["key"], sizes="(max-width: 768px) 46vw, 240px")}'
            f"<span>{h(name)}</span></a>"
        )
        jumps.append(f'<a href="#{slug}">{h(name)}</a>')
        lines = "".join(
            f"<li><b>{h(a)}</b><span>{h(b)}</span></li>" for a, b in ind["coverages"][:4]
        )
        ask_items = "".join(f"<li>{h(a)}</li>" for a in ind["asks"][:3])
        flip = " flip" if i % 2 else ""
        bands.append(f'''
<section class="section practice" id="{slug}">
  <div class="wrap band{flip}">
    <figure class="shot">{pic(ind["key"], sizes="(max-width: 768px) 100vw, 42vw")}</figure>
    <div>
      <h2 class="rise"><span class="line"><span>{h(name)}</span></span></h2>
      <p class="lede">{h(ind["lede"])}</p>
      <ul class="lines">{lines}</ul>
      <ul class="asks">{ask_items}</ul>
      <a class="more" href="/policy-review/">Review this account {ARROW}</a>
    </div>
  </div>
</section>''')
    main = page_head(
        "Coverage",
        "Five practices. One account.",
        "Real estate, hospitality, contractors, offices, and the household. The same broker reads the policy, the lease, and the contract.",
    ) + f'''
<section class="section" style="padding-top:28px"><div class="wrap">
  <nav class="cov-jump desk-only" aria-label="Practices">{"".join(jumps)}</nav>
  <div class="m-tiles m-only">{"".join(tiles)}</div>
</div></section>
{"".join(bands)}'''
    return document(
        "Coverage | SimpleINSURE",
        "Commercial and personal insurance for real estate, hospitality, contractors, offices, and the household.",
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
  <div style="margin-top:16px">{line_choices()}</div>
</div>
<div data-step="2" data-label="The policy" hidden>
  <h2 style="font-size:32px;margin-bottom:8px">What do you want a second opinion on?</h2>
  <p class="quiet">Select any that apply. Estimates are fine.</p>
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
  <p class="quiet">Choose one. You can add detail on the next step.</p>
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
    main = page_head(
        "Policy review",
        "Send the policy you have.",
        "We read it before anyone is asked to sign a broker of record letter. If it should stay, that is the answer.",
    ) + f'''
<section class="section" id="read" style="padding-top:36px"><div class="wrap">
  <div class="path-tabs" data-tabs>
    <div class="path-bar" role="tablist" aria-label="How to start">
      <button type="button" role="tab" data-tab="read">Read a current policy</button>
      <button type="button" role="tab" data-tab="account">Start from the account</button>
    </div>
    <div class="tab-panel is-on" id="panel-read" role="tabpanel"><div class="layout">{wizard("Policy review", "Email this review", read_steps)}{aside()}</div></div>
    <div class="tab-panel" id="panel-account" role="tabpanel">{wizard("Coverage review", "Email this request", account_steps)}</div>
  </div>
  <div class="prose handover" id="handover">
    <h2>How a handover works</h2>
    <p>We read the declarations, the forms, and the endorsements before a broker of record letter is prepared. The letter tells the insurer who should service a policy that is already in force. It does not, by itself, cancel coverage, change limits, or erase a claim. Some carriers accept it during the term. Some wait until renewal. We tell you which one applies before you sign.</p>
    <p>If the right path is a replacement policy, we line up the dates so one program ends as the next begins.</p>
  </div>
</div></section>'''
    return document(
        "Policy Review | SimpleINSURE",
        "Send a current policy for a second reading, or start a review from the account. The form opens an email. Nothing is stored on the website.",
        "/policy-review/",
        main,
    )


def _svc(title, blurb, subject, button, inner, extra=""):
    return f'''<details class="cc-item">
  <summary><b>{h(title)}</b><em>{h(blurb)}</em></summary>
  <div class="cc-body">{extra}{wizard(subject, button, inner)}</div>
</details>'''


def _who(prefix):
    return (
        field(prefix + "who", "Your name", required=True, full=True, attrs='autocomplete="name"')
        + field(prefix + "em", "Email", kind="email", need="email", attrs='autocomplete="email"')
        + field(prefix + "ph", "Phone", kind="tel", need="phone", attrs='autocomplete="tel"')
    )


def client_center():
    cert = _svc(
        "Request a certificate",
        "Holder, wording, and the date you need it.",
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
          <p class="quiet">A certificate is issued when the policy allows it. If the holder wants wording the policy does not grant, we say so.</p>
        </div>''',
    )
    cards = _svc(
        "Request ID cards",
        "Auto ID cards for the vehicles on the policy.",
        "ID card request",
        "Email this ID card request",
        f'''<div data-step="1" data-label="ID cards" data-error="Add your name, and an email or a phone number.">
          <div class="fields">
            {field("ni", "Named insured", required=True, full=True)}
            {field("veh", "Vehicles or drivers", kind="textarea", full=True)}
            {field("send", "Where should we send them?", kind="select", options=["Email", "Text", "Either"])}
            {_who("i")}
          </div>
        </div>''',
    )
    change = _svc(
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
        "Report a claim",
        "Date, place, and what happened. Call first if it is urgent.",
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
          <p class="quiet">Attach photos to the email draft. Do not guess at fault in a written statement to anyone but your broker and, through us, the carrier.</p>
        </div>''',
        extra=f'<p class="callout">If this is happening now, call <a href="{TEL}">{PHONE}</a> right away. Then send the note below.</p>',
    )
    bill = _svc(
        "Billing question",
        "Payments go to the carrier. We can send the pay link.",
        "Billing question",
        "Email this billing question",
        f'''<div data-step="1" data-label="Billing" data-error="Add your name, and an email or a phone number.">
          <div class="fields">
            {field("bpol", "Policy or account")}
            {field("bask", "What do you need?", kind="textarea", full=True, required=True)}
            {_who("b")}
          </div>
        </div>''',
        extra="<p class=\"cc-note\">Premium payments are made to the insurance carrier, not to SimpleINSURE. When you ask, we send the carrier's pay link.</p>",
    )
    renew = _svc(
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
    main = page_head(
        "Client Center",
        "For the account already in force.",
        "Certificates, ID cards, changes, a claim, a bill, or a renewal. Each one opens an email to the brokerage. Nothing is stored on this site.",
    ) + f'''
<section class="section" style="padding-top:20px"><div class="wrap">
  <div class="cc-list">{cert}{cards}{change}{claim}{bill}{renew}</div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
  <h2>What to expect</h2>
  <ul class="expect">
    <li>One broker stays with the account, including at renewal.</li>
    <li>Certificates go out when the policy supports them. If it does not, we say what is missing.</li>
    <li>A change in vehicles, locations, payroll, or ownership is endorsed, not remembered.</li>
    <li>If the program already in force is right, we say so.</li>
  </ul>
</div></section>'''
    return document(
        "Client Center | SimpleINSURE",
        "Request a certificate, ID cards, a policy change, or help with a claim, a bill, or a renewal. The forms open an email to SimpleINSURE.",
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
        "We place coverage for the client and stay with the account.",
    ) + f'''
<section class="section" style="padding-top:12px"><div class="wrap split">
  <div class="prose">
    <h2>An independent practice</h2>
    <p>SimpleINSURE Brokerage LLC places commercial and personal insurance for the client, not for a single carrier. Admitted markets, specialty markets, and surplus lines are all in reach, with access to A-rated carriers when the risk calls for them.</p>
    <p>Remy Mehdizadeh founded the firm so an owner could have one broker who reads the policy and remains after it is bound. The license on record is on the <a href="/legal/">licenses page</a>. We are usually paid a commission by the insurer. You can ask what we expect on your own policy.</p>
    <p><a href="{TEL}">{PHONE}</a> · <a href="{MAIL}">{EMAIL}</a></p>
  </div>
  {figure_block("hero", "(max-width: 980px) 100vw, 40vw")}
</div></section>
<section class="section" id="partners" style="padding-top:0"><div class="wrap prose narrow">
  <h2>For advisors</h2>
  <p>Real estate attorneys, property managers, and accountants already sit next to the closing, the lease, and the books. Introduce a client and we call them, copy you if they agree, and tell you when the account is placed. Their information is not shared beyond that.</p>
  <p>Compensation for a referral follows the license. New York Insurance Law section 2116 limits referral fees and commission sharing to licensed persons. What an advisor gets from us is a responsive broker.</p>
  <p><a href="/contact/">Introduce a client</a></p>
</div></section>
<section class="section" id="glossary" style="padding-top:0"><div class="wrap">
  <h2>A short glossary</h2>
  <p class="lede">Eight terms that show up in leases, loans, and certificates.</p>
  <div class="gloss-mini">{gloss}</div>
</div></section>'''
    return document(
        "About SimpleINSURE",
        "SimpleINSURE places commercial and personal insurance and stays with the account after it is bound.",
        "/about/",
        main,
    )


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
    canon = SITE + (path if path != "/" else "/") + frag
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Continue | SimpleINSURE</title>
<meta name="description" content="This page has moved.">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{h(canon)}">
<meta http-equiv="refresh" content="0; url={h(rel)}">
</head>
<body>
<p><a href="{h(rel)}">Continue</a></p>
</body>
</html>'''


REDIRECTS = {
    "coverage/real-estate/index.html": "/coverage/#real-estate",
    "coverage/hospitality/index.html": "/coverage/#hospitality",
    "coverage/construction/index.html": "/coverage/#construction",
    "coverage/professional/index.html": "/coverage/#professional",
    "coverage/personal/index.html": "/coverage/#personal",
    "checklists/index.html": "/coverage/",
    "needs/index.html": "/coverage/",
    "quote/index.html": "/policy-review/",
    "resources/index.html": "/about/#glossary",
    "partners/index.html": "/about/#partners",
    "switching/index.html": "/policy-review/#handover",
    "photo-credits/index.html": "/",
    "style-preview/index.html": "/",
    "new-york-building-insurance/index.html": "/coverage/#real-estate",
    "new-york-contractor-insurance/index.html": "/coverage/#construction",
    "new-york-restaurant-insurance/index.html": "/coverage/#hospitality",
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
    for key, target in REDIRECTS.items():
        out[key] = redirect_page(key, target)
    return out
