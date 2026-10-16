# v2 overrides, exec'd by build.py before main()
CRED = json.load(open(os.path.join(ROOT, "src/photo_credits.json")))
def credit(k):
    c = CRED[k]; return f'Photo: {html.escape(c["artist"])}, {c["license"]}'
def pic(k, alt, cls="", px=None, eager=False, sizes="(max-width:620px) 100vw, 50vw"):
    a = f' data-px="{px}"' if px else ""
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return f'<img src="/photos/{k}-800.webp" srcset="/photos/{k}-800.webp 800w, /photos/{k}-1200.webp 1200w, /photos/{k}-1600.webp 1600w" sizes="{sizes}" alt="{alt}" width="800" height="530" {load} class="{cls}"{a}>'

_head_v1 = head
def head(title, desc, path, extra=""):
    extra += '<link rel="stylesheet" href="/v2.css"><script src="/motion.js" defer></script>'
    if path == "": extra += '<link rel="preload" as="image" href="/photos/hero-800.webp" imagesrcset="/photos/hero-800.webp 800w, /photos/hero-1200.webp 1200w, /photos/hero-1600.webp 1600w" imagesizes="(max-width:620px) 100vw, 50vw" fetchpriority="high">'
    return _head_v1(title, desc, path, extra)

NAV = [("/new-york-building-insurance","Buildings"),("/new-york-restaurant-insurance","Restaurants"),("/new-york-contractor-insurance","Contractors"),("/policy-review","Policy review"),("/partners","Partners"),("/about","About")]
def header(cta="/quote"):
    links = "".join(f'<a href="{u}">{t}</a>' for u,t in NAV)
    return f"""<a class="skip" href="#main">Skip to content</a>{PREVIEW_BAR}
<div class="top"><div class="wrap"><span><b>NY DFS licensed broker</b> · License BR-1984615</span><span class="r">Serving all of New York State, by phone, email and video · <a href="{TEL}">{PHONE}</a></span></div></div>
<header class="site"><div class="wrap"><a class="logo" href="/" aria-label="SimpleINSURE home"><img src="/img/simpleinsure-wordmark-560.png" alt="SimpleINSURE" width="140" height="30"></a>
<nav class="main" aria-label="Main">{links}</nav>
<div class="hright"><a class="cc" href="/client-center">Client Center</a><a class="btn s sm hphone" href="{TEL}" aria-label="Call {PHONE}">Call</a><a class="btn p sm" href="{cta}">Get a quote</a><button class="menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="sheet"><span></span></button></div></div></header>
<div class="sheet" id="sheet">{links}<a href="/quote">Get a quote</a><a href="/client-center">Client Center</a><p class="sm"><a href="{TEL}" style="display:inline;font:inherit;border:0;padding:0">{PHONE}</a></p></div>
<main id="main">"""

_footer_v1 = footer
def footer():
    return _footer_v1().replace('<a href="/legal">Legal and privacy</a>', '<a href="/legal">Legal and privacy</a> · <a href="/photo-credits">Photo credits</a>').replace('<i aria-hidden="true">✦</i>', '<i aria-hidden="true"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2"><path d="M4 5h16v11H9l-5 4z"/></svg></i>')

SEAL = """<svg class="seal" viewBox="0 0 120 120" role="img" aria-label="Licensed New York insurance broker, License BR-1984615"><defs><path id="c" d="M60,60 m-46,0 a46,46 0 1,1 92,0 a46,46 0 1,1 -92,0"/></defs>
<circle cx="60" cy="60" r="58" fill="none" stroke="#7CB8F2" stroke-width="1.2"/><circle cx="60" cy="60" r="33" fill="none" stroke="#7CB8F2" stroke-width="1"/>
<g class="ring"><text font-family="Libre Franklin,Arial" font-size="9.2" font-weight="600" letter-spacing="2.1" fill="#dbe7f5"><textPath href="#c">LICENSED BROKER · NEW YORK STATE · BR-1984615 ·</textPath></text></g>
<text x="60" y="57" text-anchor="middle" font-family="Newsreader,Georgia" font-size="15" fill="#fff">NY</text><text x="60" y="72" text-anchor="middle" font-family="Libre Franklin,Arial" font-size="7.5" font-weight="700" letter-spacing="1.5" fill="#7CB8F2">LICENSED</text></svg>"""

def creds():
    return f"""<div class="creds"><div class="wrap">{SEAL}
<div class="it"><b>Licensed by NY DFS</b>Insurance broker License BR-1984615. <a href="https://myportal.dfs.ny.gov/nylinxext/elsearch.alice" rel="noopener" style="color:#7CB8F2">Verify</a></div>
<div class="it"><b>Admitted and specialty markets</b>Standard carriers plus excess and surplus lines through wholesale partners</div>
<div class="it"><b>Statewide</b>Every New York county, by phone, email and video</div>
<div class="it"><b>One broker, quote to claim</b>The same licensed contact for certificates, changes and renewals</div></div></div>"""

def home():
    tiles = "".join(f'<a class="tile" href="/quote?type={k}"><i aria-hidden="true">{ic}</i>{t}</a>' for k,ic,t in TILES)
    cards = [("building","/new-york-building-insurance","Real estate","Buildings and landlords","Apartment, mixed-use and commercial buildings, single properties or schedules.","Brownstones on Park Place, Brooklyn"),
             ("restaurant","/new-york-restaurant-insurance","Hospitality","Restaurants and bars","Opening soon or renewing. Property, liability, liquor liability, comp, DBL and PFL.","Counter service at a Manhattan diner"),
             ("contractor","/new-york-contractor-insurance","Construction","Contractors and trades","General liability that meets NYC and GC contract requirements, comp, auto and certificates.","Crew installing a sidewalk shed on West 47th Street"),
             ("business","/quote?type=business","Small business","Offices, retail and services","BOPs, professional and cyber liability, commercial auto and NY statutory coverage.","An independent bookstore storefront in Brooklyn")]
    ind = "".join(f'<a class="icard" href="{u}"><div class="im">{pic(k,alt,sizes="(max-width:620px) 80vw, 25vw")}</div><div class="b"><span class="k">{kk}</span><h3>{t}</h3><p>{p}</p><span class="lnk">Learn more <span class="arr">→</span></span></div></a>' for k,u,kk,t,p,alt in cards)
    return head("New York Commercial Insurance Broker | SimpleINSURE","Independent NY licensed broker for apartment buildings, restaurants, contractors and small businesses. We shop admitted and specialty carriers. Free quotes.","") + header() + f"""
<div class="hero2"><div class="wrap grid">
<div style="align-self:center"><div class="label rule">Independent commercial insurance broker · New York</div>
<h1>Commercial insurance for New York <em>buildings, restaurants</em> and <em>contractors.</em></h1>
<p class="lead">We shop admitted and specialty carriers for your account, from a single rental building to a portfolio, a new restaurant to a growing contractor. Home and auto too.</p>
<div class="ctas"><a class="btn p" href="/quote">Start a quote <span class="arr">→</span></a><a class="btn s" href="{TEL}">Call {PHONE}</a></div></div>
<figure class="hero-media"><div class="ph2">{pic("hero","Lower Manhattan skyline from the Hudson River waterfront",px="0.08",eager=True)}<figcaption>{credit("hero")}</figcaption></div>
<div class="card qc" data-rv="scale"><h2 style="font-size:25px">What do you need to insure?</h2><p class="s">Two minutes to start. A licensed broker follows up.</p><div class="tiles">{tiles}</div>
<p class="fine">No obligation. We never sell your information. Already insured? <a href="/policy-review">Free policy review.</a></p></div></figure>
</div></div>
{creds()}
<section style="padding-bottom:40px"><div class="wrap"><div class="stats">
<div class="stat"><span class="n" data-count="62">62</span><p>New York counties we serve, from the five boroughs to the Canadian border</p></div>
<div class="stat"><span class="n" data-count="6">6</span><p>Regions covered remotely: NYC, Long Island, Westchester, Hudson Valley, Capital Region, Central and Western NY</p></div>
<div class="stat"><span class="n" data-count="3">3</span><p>Industry specialties: buildings, restaurants and contractors</p></div>
<div class="stat"><span class="n t">Licensed</span><p>New York DFS insurance broker, License BR-1984615</p></div></div></div></section>
<section style="padding-top:40px"><div class="wrap"><div class="sh"><div><div class="label rule">Who we insure</div><h2 style="margin-top:12px;font-size:44px">Built around the accounts <em>New York runs on.</em></h2></div><p>Each has its own quote path, coverage checklist and FAQ, so you answer the questions that matter for your business.</p></div>
<p class="swipe-hint">Swipe to see all four →</p><div class="ind2">{ind}</div></div></section>
<section class="paper"><div class="wrap"><div class="sh"><div><div class="label rule">How it works</div><h2 style="margin-top:12px;font-size:44px">One licensed broker, <em>start to finish.</em></h2></div></div>
<div class="steps2"><div class="st"><div class="dot">1</div><h3>Tell us about the account</h3><p>Answer a short form, start a chat, or send the declarations page you already have.</p></div>
<div class="st"><div class="dot">2</div><h3>We take it to market</h3><p>We approach the carriers that write your type of risk, including specialty markets through our wholesale partners.</p></div>
<div class="st"><div class="dot">3</div><h3>Compare options with a broker</h3><p>We walk through price, limits and exclusions side by side. You decide.</p></div></div></div></section>
<section class="state2"><div class="bg" data-px="0.12" style="background-image:url(/photos/state-1600.webp)" role="img" aria-label="Lower Manhattan skyline"></div><div class="wrap cols"><div><div class="label rule">Serving all of New York</div><h2 style="margin-top:12px">From the five boroughs to Buffalo.</h2><p style="margin-top:16px;font-size:17px">We work remotely by phone, email and video, so where your property or business sits in New York does not limit who can help you.</p><p style="font-size:11px;opacity:.7">{credit("state")}</p></div>
<div class="regions"><div class="reg"><b>New York City</b><span>All five boroughs</span></div><div class="reg"><b>Long Island</b><span>Nassau and Suffolk</span></div><div class="reg"><b>Westchester</b><span>and Rockland</span></div><div class="reg"><b>Hudson Valley</b><span>Orange to Dutchess</span></div><div class="reg"><b>Capital Region</b><span>Albany, Schenectady, Troy</span></div><div class="reg"><b>Central and Western NY</b><span>Syracuse, Rochester, Buffalo</span></div></div></div></section>
<section><div class="wrap"><div class="sh"><div><div class="label rule">Why owners work with us</div><h2 style="margin-top:12px;font-size:44px">Checked, not just quoted.</h2></div></div>
<div class="trust"><div class="card"><span class="badge">Licensed</span><h3>NY DFS license BR-1984615</h3><p>SimpleINSURE Brokerage LLC is a licensed New York insurance broker. <a href="https://myportal.dfs.ny.gov/nylinxext/elsearch.alice" rel="noopener">Verify us on the DFS website.</a></p></div>
<div class="card"><span class="badge">Markets</span><h3>Admitted and specialty carriers</h3><p>Standard carriers plus excess and surplus lines markets accessed through wholesale partners.</p></div>
<div class="card"><span class="badge">Free review</span><h3>Send the policy you have</h3><p>A broker reads it and tells you what is missing, doubled up or overpriced. If it is right, we say so.</p></div>
<div class="card"><span class="badge">Paid how</span><h3>Plain about compensation</h3><p>We are usually paid a commission by the insurer. <a href="/legal#how-we-are-paid">How we are paid.</a></p></div></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="card partner"><div><div class="label">For real estate attorneys, property managers and accountants</div><h2 style="margin-top:8px;font-size:30px">Refer a client. We keep you in the loop.</h2></div><a class="btn p" href="/partners">Become a referral partner <span class="arr">→</span></a></div></div></section>
""" + footer()

def photo_credits():
    rows = "".join(f'<tr><td>{k}</td><td><a href="{c["page"]}" rel="noopener">{html.escape(c["title"])}</a></td><td>{html.escape(c["artist"])}</td><td><a href="{c["license_url"]}" rel="noopener">{c["license"]}</a></td></tr>' for k,c in CRED.items())
    return head("Photo credits | SimpleINSURE","Sources and licenses for photographs used on simpleinsure.co.","/photo-credits") + header() + f"""
<div class="pagehead"><div class="wrap"><div class="label rule">Photo credits</div><h1>Photography sources and licenses.</h1></div></div>
<section style="padding-top:10px"><div class="wrap"><table class="credits" style="border-collapse:collapse;width:100%"><tr><th>Use</th><th>Original file (Wikimedia Commons)</th><th>Author</th><th>License</th></tr>{rows}</table>
<p class="fine">Images were resized and recompressed for the web. No other changes. CC BY-SA images remain under their original license.</p></div></section>""" + footer()

_industry_v1 = industry
BAND = {"new-york-building-insurance":("building","Brownstones on Park Place, Brooklyn"),"new-york-restaurant-insurance":("restaurant","Counter service at a Manhattan diner"),"new-york-contractor-insurance":("contractor","Crew installing a sidewalk shed on West 47th Street")}
def industry(slug):
    h = _industry_v1(slug); k, alt = BAND[slug]
    band = f'<figure class="pband">{pic(k,alt,px="0.1",sizes="100vw")}<figcaption>{credit(k)}</figcaption></figure>'
    return h.replace("</section>", "</section>" + band, 1)

_partners_v1 = partners
def partners():
    return _partners_v1().replace('<section style="padding-top:20px">', f'<figure class="pband" style="height:300px">{pic("building","Row houses on Park Place, Brooklyn",px="0.1",sizes="100vw")}<figcaption>{credit("building")}</figcaption></figure><section>', 1)
