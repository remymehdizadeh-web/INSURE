#!/usr/bin/env python3
"""Builds the static preview into ../out. Run: python3 src/build.py"""
import json, os, re, shutil, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out")
LP = "/workspace/leadgen/overnight/deliverables/landing-pages"
SITE = "https://www.simpleinsure.co"
PHONE = "(516) 226-7969"; TEL = "tel:+15162267969"
HOURS = ""  # hours TBD; do not show until Remy confirms

SCHEMA = {
 "@context": "https://schema.org", "@type": "InsuranceAgency", "@id": SITE + "/#organization",
 "name": "SimpleINSURE Brokerage LLC", "alternateName": "SimpleINSURE", "url": SITE,
 "logo": SITE + "/simpleinsure-wordmark.png", "image": SITE + "/img/og-image-v2.png",
 "telephone": "+1-516-226-7969", "email": "info@simpleinsure.co",
 "address": {"@type": "PostalAddress", "streetAddress": "900 Stewart Ave Ste 210", "addressLocality": "Garden City", "addressRegion": "NY", "postalCode": "11530", "addressCountry": "US"},
 "areaServed": {"@type": "State", "name": "New York", "sameAs": "https://en.wikipedia.org/wiki/New_York_(state)"},
 "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "license", "name": "New York insurance broker license BR-1984615", "recognizedBy": {"@type": "GovernmentOrganization", "name": "New York State Department of Financial Services"}},
 "sameAs": ["https://www.manta.com/c/m1h3szd", "https://nextdoor.com/page/simpleinsure-garden-city-ny/"],
 "knowsAbout": ["Habitational insurance","Restaurant insurance","Liquor liability","Contractors general liability","Workers compensation","NY disability and paid family leave","Commercial property","Excess and surplus lines","Homeowners insurance"]}

def head(title, desc, path, extra=""):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{SITE}{path}">
<link rel="icon" href="/img/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon.ico" sizes="any"><link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}{path}"><meta property="og:image" content="{SITE}/img/og-image-v2.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="/fonts/franklin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/newsreader.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/site.css">
<script type="application/ld+json">{json.dumps(SCHEMA)}</script>{extra}
</head><body>"""

PREVIEW_BAR = '<div class="pv">Preview build for review only. Not live. Forms open an email draft; chat does not send anything.</div>'

def header(cta="/quote"):
    return f"""<a class="skip" href="#main">Skip to content</a>{PREVIEW_BAR}
<div class="top"><div class="wrap"><span><b>NY DFS licensed broker</b> · License BR-1984615</span><span class="r">Serving all of New York State, by phone, email and video · <a href="{TEL}">{PHONE}</a></span></div></div>
<header class="site"><div class="wrap"><a class="logo" href="/" aria-label="SimpleINSURE home"><img src="/img/simpleinsure-wordmark-560.png" alt="SimpleINSURE" width="140" height="30"></a>
<nav class="main" aria-label="Main"><a href="/new-york-building-insurance">Buildings</a><a href="/new-york-restaurant-insurance">Restaurants</a><a href="/new-york-contractor-insurance">Contractors</a><a href="/policy-review">Policy review</a><a href="/partners">Partners</a><a href="/about">About</a></nav>
<div class="hright"><a class="cc" href="/client-center">Client Center</a><a class="btn s sm hphone" href="{TEL}" aria-label="Call {PHONE}">Call</a><a class="btn p sm" href="{cta}">Get a quote</a></div></div></header>
<main id="main">"""

def footer():
    return f"""</main><footer class="site"><div class="wrap"><div class="g"><div><img src="/img/simpleinsure-wordmark-white-560.png" alt="SimpleINSURE" width="122" height="26" loading="lazy"><p style="margin-top:16px">Independent commercial and personal insurance for New York. Remote service, no walk-ins.</p></div>
<div><b>Industries</b><ul><li><a href="/new-york-building-insurance">Buildings and landlords</a></li><li><a href="/new-york-restaurant-insurance">Restaurants and bars</a></li><li><a href="/new-york-contractor-insurance">Contractors</a></li><li><a href="/quote?type=business">Small business</a></li></ul></div>
<div><b>Company</b><ul><li><a href="/about">About</a></li><li><a href="/partners">Partners</a></li><li><a href="/quote">Get a quote</a></li><li><a href="/legal#how-we-are-paid">How we are paid</a></li></ul></div>
<div><b>Contact</b><ul><li><a href="{TEL}">{PHONE}</a></li><li><a href="mailto:info@simpleinsure.co">info@simpleinsure.co</a></li><li>Mailing address (remote service, no walk-ins): 900 Stewart Ave, Ste 210, Garden City, NY 11530</li></ul></div></div>
<div class="legal">© 2026 SimpleINSURE Brokerage LLC · New York DFS licensed insurance broker, License BR-1984615 · Coverage descriptions are general summaries. Coverage is subject to underwriting and the terms of the issued policy. · <a href="/legal#how-we-are-paid">How we are paid</a> · <a href="/legal">Legal and privacy</a></div></div></footer>
<div class="mbar"><a class="btn call" href="{TEL}">Call {PHONE}</a><a class="btn q" href="/quote">Get a quote</a></div>
<button class="chatbtn" type="button" aria-controls="chat" aria-expanded="false" id="chatbtn"><i aria-hidden="true">✦</i>Questions? Chat with us</button>
<div class="chatpanel" id="chat" role="dialog" aria-label="Quote assistant (placeholder)"><div class="h"><span>SimpleINSURE quote assistant</span><button type="button" id="chatx" aria-label="Close">×</button></div>
<div class="bd"><div class="ph-note" style="margin-bottom:10px">Placeholder. The chatbot is not connected yet.</div><div class="bubble">Hi, I am an automated assistant. I can collect a few details and have a licensed broker follow up. I cannot quote prices, bind coverage or give coverage advice.</div><div class="bubble">What do you need to insure?</div>
<div class="opts"><a href="/quote?type=building">A building</a><a href="/quote?type=restaurant">A restaurant or bar</a><a href="/quote?type=contractor">A contracting business</a><a href="/quote?type=business">Another small business</a><a href="{TEL}">Talk to a broker: {PHONE}</a></div></div></div>
<script>(function(){{var b=document.getElementById('chatbtn'),p=document.getElementById('chat');function t(){{var o=p.classList.toggle('open');b.setAttribute('aria-expanded',o)}}b.onclick=t;document.getElementById('chatx').onclick=t}})();</script>
</body></html>"""

TILES = [("building","▤","Apartment or mixed-use building"),("restaurant","◔","Restaurant, bar or cafe"),("contractor","⚒","Contractor or trade"),("business","▣","Other small business"),("personal","⌂","Home, auto or umbrella"),("unsure","?","Not sure yet")]

def home():
    tiles = "".join(f'<a class="tile" href="/quote?type={k}"><i aria-hidden="true">{ic}</i>{t}</a>' for k,ic,t in TILES)
    return head("New York Commercial Insurance Broker | SimpleINSURE","Independent NY licensed broker for apartment buildings, restaurants, contractors and small businesses. We shop admitted and specialty carriers. Free quotes.","") + header() + f"""
<div class="hero"><div class="arc" aria-hidden="true"></div><div class="wrap grid">
<div><div class="label">Independent commercial insurance broker · New York</div>
<h1 style="margin-top:14px">Commercial insurance for New York <em>buildings, restaurants</em> and <em>contractors.</em></h1>
<p class="lead">We shop admitted and specialty carriers for your account, from a single rental building to a portfolio, a new restaurant to a growing contractor. Home and auto too.</p>
<div class="ctas"><a class="btn p" href="/quote">Start a quote <span class="arr">→</span></a><a class="btn s" href="{TEL}">Call {PHONE}</a></div>
<ul class="ticks"><li>NY DFS licensed, BR-1984615</li><li>Admitted and specialty markets</li><li>One broker from quote to claim</li><li>Statewide, fully remote</li></ul></div>
<div class="card qc"><h2>What do you need to insure?</h2><p class="s">Two minutes to start. A licensed broker follows up.</p><div class="tiles">{tiles}</div>
<p class="fine">No obligation. We never sell your information. Already insured? <a href="/policy-review">Upload your declarations page for a free policy review.</a></p></div>
</div></div>
<section><div class="wrap"><div class="sh"><div><div class="label">Who we insure</div><h2 style="margin-top:10px">Built around three kinds of New York accounts.</h2></div><p>Each has its own quote path, coverage checklist and FAQ, so you answer the questions that matter for your business.</p></div>
<div class="ind">
<a class="card" href="/new-york-building-insurance"><div class="ph"><span>Real estate</span></div><div class="b"><h3>Buildings and landlords</h3><p>Apartment, mixed-use and commercial buildings, single properties or schedules. Property, liability, umbrella.</p><span class="lnk">Building insurance →</span></div></a>
<a class="card" href="/new-york-restaurant-insurance"><div class="ph"><span>Hospitality</span></div><div class="b"><h3>Restaurants and bars</h3><p>Opening soon or renewing. Property, liability, liquor liability, workers comp, DBL and PFL.</p><span class="lnk">Restaurant insurance →</span></div></a>
<a class="card" href="/new-york-contractor-insurance"><div class="ph"><span>Construction</span></div><div class="b"><h3>Contractors and trades</h3><p>General liability that meets NYC and GC contract requirements, comp, auto and certificates.</p><span class="lnk">Contractor insurance →</span></div></a>
<a class="card" href="/quote?type=business"><div class="ph"><span>Small business</span></div><div class="b"><h3>Offices, retail and services</h3><p>BOPs, professional and cyber liability, commercial auto and NY statutory coverage.</p><span class="lnk">Start a small business quote →</span></div></a>
</div></div></section>
<section class="paper"><div class="wrap"><div class="sh"><div><div class="label">How it works</div><h2 style="margin-top:10px">One licensed broker, <em>start to finish.</em></h2></div></div>
<div class="steps"><div class="card step"><div class="num">01</div><h3 style="margin-top:12px">Tell us about the account</h3><p>Answer a short form, start a chat, or send the declarations page you already have.</p></div>
<div class="card step"><div class="num">02</div><h3 style="margin-top:12px">We take it to market</h3><p>We approach the carriers that write your type of risk, including specialty markets through our wholesale partners.</p></div>
<div class="card step"><div class="num">03</div><h3 style="margin-top:12px">Compare options with a broker</h3><p>We walk through price, limits and exclusions side by side. You decide.</p></div></div></div></section>
<section class="navyband"><div class="wrap cols"><div><div class="label">Serving all of New York</div><h2 style="margin-top:10px">From the five boroughs to Buffalo.</h2><p style="margin-top:16px;font-size:17px">We work remotely by phone, email and video, so where your property or business sits in New York does not limit who can help you.</p></div>
<div class="regions"><div class="reg"><b>New York City</b><span>All five boroughs</span></div><div class="reg"><b>Long Island</b><span>Nassau and Suffolk</span></div><div class="reg"><b>Westchester</b><span>and Rockland</span></div><div class="reg"><b>Hudson Valley</b><span>Orange to Dutchess</span></div><div class="reg"><b>Capital Region</b><span>Albany, Schenectady, Troy</span></div><div class="reg"><b>Central and Western NY</b><span>Syracuse, Rochester, Buffalo</span></div></div></div></section>
<section><div class="wrap"><div class="sh"><div><div class="label">Why owners work with us</div><h2 style="margin-top:10px">Checked, not just quoted.</h2></div></div>
<div class="trust"><div class="card"><span class="badge">Licensed</span><h3>NY DFS license BR-1984615</h3><p>SimpleINSURE Brokerage LLC is a licensed New York insurance broker. <a href="https://myportal.dfs.ny.gov/nylinxext/elsearch.alice" rel="noopener">Verify us on the DFS website.</a></p></div>
<div class="card"><span class="badge">Markets</span><h3>Admitted and specialty carriers</h3><p>Standard carriers plus excess and surplus lines markets accessed through wholesale partners.</p></div>
<div class="card"><span class="badge">Free review</span><h3>Send the policy you have</h3><p>A broker reads it and tells you what is missing, doubled up or overpriced. If it is right, we say so.</p></div>
<div class="card"><span class="badge">Paid how</span><h3>Plain about compensation</h3><p>We are usually paid a commission by the insurer. <a href="/legal#how-we-are-paid">How we are paid.</a></p></div></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="card partner"><div><div class="label">For real estate attorneys, property managers and accountants</div><h2 style="margin-top:8px;font-size:30px">Refer a client. We keep you in the loop.</h2></div><a class="btn p" href="/partners">Become a referral partner →</a></div></div></section>
""" + footer()

def about():
    return head("About SimpleINSURE | Licensed New York Insurance Broker","SimpleINSURE Brokerage LLC is an independent insurance broker licensed by New York DFS, License BR-1984615, serving buildings, restaurants and contractors statewide.","/about") + header() + f"""
<div class="pagehead"><div class="wrap"><div class="label">About SimpleINSURE</div><h1>A New York broker that reads the policy <em>before quoting it.</em></h1></div></div>
<section style="padding-top:20px"><div class="wrap cols" style="align-items:start"><div class="prose">
<p>SimpleINSURE Brokerage LLC is an independent insurance broker licensed by the New York Department of Financial Services (License BR-1984615). We place commercial insurance for apartment and mixed-use buildings, restaurants and bars, contractors and small businesses, plus home, auto and umbrella for the people who own them.</p>
<p>Because we are a broker, we work for you, not for one insurance company. We take each account to the carriers that write that kind of risk, and to specialty and surplus lines markets through wholesale partners when the standard market says no.</p>
<p>We are a remote firm. Clients across New York State reach us by phone, email and video. There is no storefront, so please call before sending anything to our mailing address.</p>
<h2>How we work</h2><p>We start with what you already have. We tell you when a policy is already right. We come back before renewal with the account already reviewed.</p>
<h2>Verify us</h2><p>Look up License BR-1984615 on the <a href="https://myportal.dfs.ny.gov/nylinxext/elsearch.alice" rel="noopener">New York DFS licensee search</a>. Read <a href="/legal#how-we-are-paid">how we are paid</a>.</p></div>
<div class="card" style="padding:28px"><div class="ph" style="height:220px;border-radius:10px"><span>Photo of Remy, to be supplied</span></div>
<h3 style="margin-top:18px;font-family:var(--serif);font-size:26px;font-weight:500">Remy Mehdizadeh</h3><p style="color:var(--slate);margin:4px 0 14px">Founder [title and personal license to confirm]</p>
<p style="color:var(--slate);font-size:15px">Remy started SimpleINSURE in 2026 to give New York property owners, restaurants and contractors one licensed broker who reads the whole policy and stays on the account from quote to claim.</p>
<div class="ctas" style="margin-top:16px"><a class="btn p sm" href="{TEL}">Call {PHONE}</a><a class="btn s sm" href="mailto:info@simpleinsure.co">Email us</a></div></div></div></section>
""" + footer()

def partners():
    return head("Referral Partners | Real Estate Attorneys, Property Managers, CPAs | SimpleINSURE","Real estate attorneys, property managers and accountants: introduce New York clients to a licensed broker who keeps you informed. No referral fees to unlicensed persons.","/partners") + header() + f"""
<div class="pagehead"><div class="wrap"><div class="label">Referral partners</div><h1>For the professionals New York owners <em>already trust.</em></h1>
<p class="lead">Real estate attorneys, property managers and accountants: when a client needs insurance for a closing, a new building, a lease or a new business, send them to a licensed broker who will keep you informed.</p></div></div>
<section style="padding-top:20px"><div class="wrap"><div class="g3">
<div class="card"><span class="badge">Attorneys</span><h3>Real estate attorneys</h3><p>Closing on a building or a mixed-use property? We arrange binders and evidence of insurance for the lender, and we read the loan insurance requirements before quoting.</p></div>
<div class="card"><span class="badge">Managers</span><h3>Property managers</h3><p>One contact for the buildings you manage: renewals tracked, certificates for vendors and tenants, and help when a carrier non-renews.</p></div>
<div class="card"><span class="badge">CPAs</span><h3>Accountants</h3><p>Clients starting a business or hiring their first employees need workers comp, NY disability and Paid Family Leave. We set it up and keep the audit paperwork clean.</p></div></div>
<div class="cols" style="margin-top:56px;align-items:start"><div><div class="label">How it works</div><h2 style="margin-top:10px">Three steps for you. <em>None for your client to chase.</em></h2>
<ol class="prose" style="padding-left:20px"><li>Send an introduction by email or the form on this page.</li><li>We contact your client within one business day and copy you if they agree.</li><li>We tell you when the client is placed. We never share your client's details with anyone else.</li></ol>
<div class="note" style="margin-top:22px"><b>Our referral policy.</b> SimpleINSURE does not pay referral fees, commissions or any other compensation to unlicensed persons, and we do not share commissions with anyone who is not licensed (NY Insurance Law § 2116). What we offer partners is a responsive broker, referrals back where they fit, and updates on your clients with their permission.</div></div>
<form class="card" style="padding:28px" onsubmit="event.preventDefault();this.querySelector('.ok').hidden=false"><h3 style="font-family:var(--serif);font-size:26px;font-weight:500">Become a referral partner</h3>
<div class="ph-note" style="margin-top:12px">Placeholder form. It is not connected and sends nothing.</div>
<div class="g2"><div class="field"><label for="pn">Name</label><input id="pn" autocomplete="name"></div><div class="field"><label for="pf">Firm</label><input id="pf" autocomplete="organization"></div>
<div class="field"><label for="pr">Role</label><select id="pr"><option>Real estate attorney</option><option>Property manager</option><option>Accountant or CPA</option><option>Other</option></select></div><div class="field"><label for="pe">Email</label><input id="pe" type="email" autocomplete="email"></div>
<div class="field"><label for="pp">Phone</label><input id="pp" type="tel" autocomplete="tel"></div><div class="field"><label for="pc">Client to introduce now?</label><select id="pc"><option>No, not yet</option><option>Yes</option></select></div></div>
<button class="btn p" style="width:100%;margin-top:20px" type="submit">Become a referral partner</button><p class="ok fine" hidden>Preview only: nothing was sent.</p></form></div></div></section>
""" + footer()

def legal():
    return head("Legal, Privacy and How We Are Paid | SimpleINSURE","Licensing, compensation disclosure and privacy for SimpleINSURE Brokerage LLC, a New York DFS licensed insurance broker, License BR-1984615.","/legal") + header() + f"""
<div class="pagehead"><div class="wrap"><div class="label">Legal</div><h1>Licensing, compensation and privacy.</h1></div></div>
<section style="padding-top:10px"><div class="wrap prose">
<h2 id="licensing">Licensing</h2><p>SimpleINSURE Brokerage LLC is a licensed property and casualty insurance broker, New York DFS License BR-1984615. <a href="https://myportal.dfs.ny.gov/nylinxext/elsearch.alice" rel="noopener">Verify on the DFS licensee search.</a></p>
<h2 id="how-we-are-paid">How we are paid</h2><div class="ph-note" style="margin-bottom:14px">Draft for counsel review against 11 NYCRR 30 (Regulation 194) before publishing.</div>
<p>SimpleINSURE Brokerage LLC is usually paid a commission by the insurance company that issues your policy, calculated as a percentage of the premium. In some cases we may also receive other compensation from insurers, such as contingent or bonus payments based on the overall business we place with them. You may ask us for information about the compensation we expect to receive from your policy, and about alternative quotes we presented, and we will provide it.</p>
<h2>Coverage descriptions</h2><p>Coverage descriptions on this site are general summaries for information only. They do not amend, extend or alter any policy and are not an offer or a binder of insurance. Coverage is subject to underwriting and carrier approval, and the terms of the issued policy govern.</p>
<h2>Privacy</h2><p>The live site's existing privacy notice (form data, 23 NYCRR 500 and the client portal) carries over unchanged. It is not reproduced in this preview.</p></div></section>
""" + footer()

def quote():
    q = r"""
<div class="pagehead" style="padding-bottom:10px"><div class="wrap"><div class="label" id="qlabel">Get a quote</div><h1 id="qh" style="font-size:42px">What do you need to insure?</h1></div></div>
<section style="padding-top:10px"><div class="wrap" style="display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:32px" id="qgrid">
<div><div class="ph-note">Placeholder quote form for review. It is not connected and sends nothing. On the real site it will save to the existing /api/policy-review/partial route.</div>
<ol class="prog" id="prog" aria-label="Progress"><li>1 · Business type</li><li>2 · About the account</li><li>3 · Coverage</li><li>4 · Contact</li></ol>
<form class="card" id="qf" style="padding:30px" novalidate>
<fieldset data-step="1" style="border:0;padding:0;margin:0"><legend class="flabel">Choose one</legend><div class="tiles" id="types"></div></fieldset>
<fieldset data-step="2" hidden style="border:0;padding:0;margin:0"><div id="details"></div>
<div class="field" style="margin-top:18px"><label for="up">Current policy (optional)</label><input id="up" type="file" accept=".pdf,.jpg,.jpeg,.png,.heic" style="padding-top:10px"></div></fieldset>
<fieldset data-step="3" hidden style="border:0;padding:0;margin:0"><legend class="flabel">Pre-checked for your business type. Change anything.</legend><div class="chips" id="cov"></div>
<div class="g2"><div class="field"><label for="when">Needed by</label><input id="when" type="date"></div><div class="field"><label for="stat">Situation</label><select id="stat"><option>Renewing a current policy</option><option>New business or new purchase</option><option>Shopping mid-term</option></select></div></div></fieldset>
<fieldset data-step="4" hidden style="border:0;padding:0;margin:0"><div class="g2">
<div class="field"><label for="cn">Full name</label><input id="cn" autocomplete="name"></div><div class="field"><label for="cb">Business name</label><input id="cb" autocomplete="organization"></div>
<div class="field"><label for="ce">Email</label><input id="ce" type="email" autocomplete="email"></div><div class="field"><label for="cp">Phone</label><input id="cp" type="tel" autocomplete="tel"></div>
<div class="field"><label for="cz">ZIP code</label><input id="cz" inputmode="numeric" autocomplete="postal-code"></div><div class="field"><label for="ct">Best time to call</label><select id="ct"><option>Morning</option><option>Afternoon</option><option>Any time</option></select></div></div>
<p class="fine">By continuing you agree that a licensed broker may contact you about this request. No obligation. We never sell your information. <a href="/legal#how-we-are-paid">How we are paid.</a></p></fieldset>
<div id="done" hidden><h2 style="font-size:30px">Thanks. This is where the confirmation will show.</h2><p class="lead" style="font-size:17px">Preview only: nothing was sent. On the live site: "A licensed broker will review this and contact you within [confirm] business days. If it is urgent, call (516) 226-7969."</p></div>
<div id="nav" style="display:flex;justify-content:space-between;align-items:center;margin-top:26px;border-top:1px solid #e3e9f1;padding-top:20px"><button type="button" class="btn s sm" id="back">← Back</button><button type="button" class="btn p" id="next">Continue →</button></div>
</form><p class="fine" style="margin-top:14px">Prefer to talk it through? Answer the same questions in chat, or call <a href="tel:+15162267969">(516) 226-7969</a>.</p></div>
<aside><div class="card" style="padding:24px;margin-bottom:16px"><h2 style="font-size:20px">What happens next</h2><ol style="padding-left:18px;color:var(--slate);font-size:14.5px"><li>A licensed broker reviews your details and calls if anything is unclear.</li><li>We take the account to the carriers that write this kind of business, including specialty markets through our wholesale partners.</li><li>You get options side by side, with the differences explained.</li></ol></div>
<div class="card" style="padding:24px;background:var(--navy);color:#fff;border-color:var(--navy)"><div class="label" style="color:var(--sky)">Licensed in New York</div><p style="margin:8px 0 0;font-size:14.5px;color:#d3dfec">SimpleINSURE Brokerage LLC, NY DFS License BR-1984615. No obligation. We never sell your information.</p></div></aside>
</div></section>
<style>.prog{display:flex;gap:10px;list-style:none;padding:0;margin:20px 0}.prog li{flex:1;border-top:4px solid #d6e3f1;padding-top:8px;font-size:12.5px;color:var(--slate);font-weight:500}.prog li.done{border-color:var(--blue)}.prog li.cur{border-color:var(--navy);color:var(--navy);font-weight:600}@media(max-width:980px){#qgrid{grid-template-columns:1fr!important}}@media(max-width:620px){.prog li{font-size:0}.prog li.cur{font-size:12.5px}#qh{font-size:32px!important}}</style>
<script>
(function(){
var T=TYPES;
var D={
building:{h:"Tell us about the building.",f:[["Property address","t"],["Residential units","n"],["Commercial units","n"],["Stories","n"],["Year built","n"],["Construction",["Frame","Joisted masonry","Non-combustible","Fire resistive","Not sure"]],["Current renewal date","d"]],c:["Property","General liability","Umbrella","Workers comp"]},
restaurant:{h:"Tell us about the restaurant.",f:[["Opening or renewal date","d"],["Estimated annual sales",["Under $500K","$500K to $1M","$1M to $3M","Over $3M","Not open yet"]],["Seats","n"],["Employees, full and part time","n"],["Serves alcohol?",["Yes, full liquor","Beer and wine only","No alcohol","License pending with the SLA"]],["Anything else",["None","Live music or DJ","Delivery drivers","Outdoor seating","Catering off site","We own the building"]]],c:["Property and equipment","General liability","Liquor liability","Workers comp","NY disability and PFL","Umbrella"]},
contractor:{h:"Tell us about the business.",f:[["Trade","t"],["Work in NYC (five boroughs)?",["Yes","No","Some"]],["Annual payroll",["Under $100K","$100K to $500K","$500K to $1M","Over $1M"]],["Use subcontractors?",["Yes","No"]],["GC or contract insurance requirements","t"],["Certificates needed per month","n"]],c:["General liability","Workers comp","NY disability and PFL","Commercial auto","Umbrella","Inland marine and tools"]},
business:{h:"Tell us about the business.",f:[["What does the business do?","t"],["Annual revenue",["Under $250K","$250K to $1M","$1M to $5M","Over $5M"]],["Employees","n"],["Own or rent your space?",["Rent","Own","Home based"]]],c:["Business owners policy","Professional liability","Cyber liability","Workers comp","NY disability and PFL","Commercial auto"]},
personal:{h:"Tell us what you want to cover.",f:[["What to cover",["Home","Auto","Home and auto","Umbrella","Rental property"]],["Property ZIP","t"],["Current renewal date","d"]],c:["Homeowners","Auto","Personal umbrella","Valuables"]},
unsure:{h:"Tell us a little about it.",f:[["Describe what you want to insure","x"]],c:["Not sure, help me decide"]}};
var step=1,type=new URLSearchParams(location.search).get('type');if(!D[type])type=null;
var tw=document.getElementById('types');T.forEach(function(t){var b=document.createElement('button');b.type='button';b.className='tile';b.innerHTML='<i aria-hidden="true">'+t[1]+'</i>'+t[2];b.onclick=function(){type=t[0];go(2)};b.dataset.k=t[0];tw.appendChild(b)});
function fld(f,i){var id='d'+i,l='<div class="field"><label for="'+id+'">'+f[0]+'</label>';if(Array.isArray(f[1]))return l+'<select id="'+id+'"><option value="">Select</option>'+f[1].map(function(o){return'<option>'+o+'</option>'}).join('')+'</select></div>';if(f[1]=='x')return l+'<textarea id="'+id+'"></textarea></div>';return l+'<input id="'+id+'" type="'+({n:'number',d:'date'}[f[1]]||'text')+'"></div>'}
function build(){var d=D[type];document.getElementById('details').innerHTML='<div class="g2">'+d.f.map(fld).join('')+'</div>';document.getElementById('cov').innerHTML=d.c.concat(["Something else"]).map(function(c,i){return'<label class="chip"><input type="checkbox"'+(i<d.c.length?' checked':'')+'><span>'+c+'</span></label>'}).join('');var t=T.filter(function(x){return x[0]==type})[0];document.getElementById('qlabel').textContent='Get a quote · '+t[2]}
var H={1:"What do you need to insure?",3:"What coverage do you need?",4:"Where should we send your options?"};
function go(s){if(s>1&&!type)return;step=s;if(s==2)build();document.querySelectorAll('[data-step]').forEach(function(f){f.hidden=f.dataset.step!=s});document.getElementById('qh').textContent=s==2?D[type].h:H[s];
document.querySelectorAll('#prog li').forEach(function(li,i){li.className=i+1<s?'done':(i+1==s?'cur':'')});document.getElementById('back').style.visibility=s>1?'visible':'hidden';document.getElementById('next').style.display=s==1?'none':'';document.getElementById('next').textContent=s==4?'Send my request (preview)':'Continue →';
document.querySelectorAll('.tile').forEach(function(b){b.classList.toggle('on',b.dataset.k==type)})}
document.getElementById('next').onclick=function(){if(step<4)go(step+1);else{document.querySelectorAll('[data-step]').forEach(function(f){f.hidden=true});document.getElementById('nav').hidden=true;document.getElementById('done').hidden=false;document.getElementById('qh').textContent='Request received (preview)'}};
document.getElementById('back').onclick=function(){go(step-1)};
go(type?2:1);
})();
</script>"""
    q = q.replace("TYPES", json.dumps([[k,i,t] for k,i,t in TILES]))
    return head("Get a Commercial Insurance Quote in New York | SimpleINSURE","Start a New York insurance quote for a building, restaurant, contracting business or small business. A licensed broker shops admitted and specialty carriers for you.","/quote") + header() + q + footer()

def industry(slug):
    src = open(os.path.join(LP, slug + ".html")).read()
    hd, body = src.split("<body>", 1)
    # keep page-specific meta, FAQ schema and content; swap in shared chrome
    title = re.search(r"<title>(.*?)</title>", hd).group(1)
    desc = re.search(r'name="description" content="(.*?)"', hd).group(1)
    desc = desc.replace(" Licensed NY broker trusted by NYC institutions.", " Licensed NY broker.")
    faq = "".join(m for m in re.findall(r'<script type="application/ld\+json">.*?</script>', hd) if "FAQPage" in m)
    extra = '<link rel="stylesheet" href="/lp.css">' + faq
    main = body.split("</header>", 1)[1].split('<footer class="site">', 1)[0]
    # remove the "Also from" block's .html links -> clean routes
    main = re.sub(r'href="(new-york-[a-z-]+)\.html"', r'href="/\1"', main)
    main = main.replace('href="https://simpleinsure.co"', 'href="/"')
    main = main.replace("assets/", "/img/")
    main = main.replace("Mon to Fri, 9 AM to 6 PM", "")
    main = re.sub(r"Mon to Fri,? 9 AM to [56] PM( ET)?", "", main)
    main = main.replace(" Trusted by NYC institutions.", "")
    main = main.replace('<form method="post" action=""', '<div class="ph-note" style="margin-bottom:10px">This preview cannot save the form. Email info@simpleinsure.co or call (516) 226-7969.</div><form onsubmit="event.preventDefault();location.href=\'mailto:info@simpleinsure.co?subject=\'+encodeURIComponent(\'Insurance inquiry\')" method="post" action=""')
    main = main.replace("Our office is in Garden City and our", "We are based in Garden City and our")
    return head(title, desc, "/" + slug, extra) + header("/quote?type=" + {"new-york-building-insurance":"building","new-york-restaurant-insurance":"restaurant","new-york-contractor-insurance":"contractor"}[slug]) + '<div class="lp">' + main + "</div>" + footer()

def lp_css():
    path = os.path.join(LP, "assets/site.css")
    # v4 industry pages do not use the old landing-page stylesheet. The
    # source tree is not in this repo, so skip it instead of failing the build.
    if not os.path.exists(path):
        return ""
    css = re.sub(r"/\*.*?\*/", "", open(path).read(), flags=re.S)
    # scope landing-page CSS under .lp so it does not fight the shared header/footer
    out = []
    for rule in re.findall(r'([^{}]+)\{([^{}]*)\}', re.sub(r'@media[^{]+\{((?:[^{}]*\{[^{}]*\})*)\s*\}', '', css)):
        sel, decl = rule
        sel = sel.strip()
        if sel.startswith(":root"): out.append(f".lp{{{decl}}}"); continue
        if any(s in sel for s in ("header.site","footer.site",".topbar",".mbar","body","html","*")) : continue
        out.append(",".join(".lp " + s.strip() for s in sel.split(",")) + "{" + decl + "}")
    for m in re.finditer(r'(@media[^{]+)\{((?:[^{}]*\{[^{}]*\})*)\s*\}', css):
        inner = []
        for sel, decl in re.findall(r'([^{}]+)\{([^{}]*)\}', m.group(2)):
            sel = sel.strip()
            if any(s in sel for s in ("header.site","footer.site",".topbar",".mbar","body","html")): continue
            inner.append(",".join(".lp " + s.strip() for s in sel.split(",")) + "{" + decl + "}")
        out.append(m.group(1) + "{" + "".join(inner) + "}")
    return "\n".join(out)

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
    """Turn a root-absolute path into a relative URL.

    Relative links work both at a domain root (a future simpleinsure.co)
    and under a project subpath such as GitHub Pages /INSURE/.
    """
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
    text = re.sub(r'\b(href|src|action|poster)=(["\'])([^"\']*)\2', repl_attr, text)

    def repl_srcset(m):
        attr, quote, val = m.group(1), m.group(2), m.group(3)
        return f"{attr}={quote}{rewrite_srcset(val, depth)}{quote}"
    text = re.sub(r'\b(srcset|imagesrcset)=(["\'])([^"\']*)\2', repl_srcset, text)

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
            if name.endswith(".html") and 'name="robots" content="noindex, nofollow"' not in text:
                bad.append(rel + ": missing noindex")
            for i, line in enumerate(text.splitlines(), 1):
                if re.search(r'''(?:href|src|srcset|imagesrcset|action|poster)\s*=\s*["']/''', line):
                    bad.append(f"{rel}:{i}: root-absolute attribute")
                if re.search(r'''url\(\s*["']?/''', line):
                    bad.append(f"{rel}:{i}: root-absolute url()")
    if bad:
        raise SystemExit("portable URL check failed:\n" + "\n".join(bad[:40]))

exec(open(os.path.join(ROOT, "src/v2_parts.py")).read())
exec(open(os.path.join(ROOT, "src/v3_parts.py")).read())
exec(open(os.path.join(ROOT, "src/v4_parts.py")).read())

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    shutil.copytree(os.path.join(ROOT, "public"), OUT)
    css = lp_css()
    if css:
        open(os.path.join(OUT, "lp.css"), "w").write(css)
    for dirpath, _, files in os.walk(OUT):
        for name in files:
            if not name.endswith(".css"):
                continue
            fp = os.path.join(dirpath, name)
            depth = os.path.relpath(fp, OUT).count(os.sep)
            text = open(fp, encoding="utf-8").read()
            new = relativize_urls(text, depth)
            if new != text:
                open(fp, "w").write(new)
    pages = {"index.html": home(), "quote/index.html": quote(), "about/index.html": about(), "partners/index.html": partners(), "legal/index.html": legal(), "photo-credits/index.html": photo_credits()}
    for s in ("new-york-building-insurance","new-york-restaurant-insurance","new-york-contractor-insurance"):
        pages[s + "/index.html"] = industry(s)
    for p, html_doc in pages.items():
        fp = os.path.join(OUT, p); os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, "w").write(relativize_urls(html_doc, p.count("/")))
    open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nDisallow: /\n")
    assert_portable(OUT)
    print("built", len(pages), "pages")
main()
