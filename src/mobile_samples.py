# -*- coding: utf-8 -*-
"""Standalone mobile home previews. Not linked from the live site."""
from render import ADDR, COVER, EMAIL, MAIL, PHONE, TEL, h, pic

FONT = '''
@font-face{font-family:Franklin;src:url("/fonts/franklin.woff2") format("woff2");font-weight:100 900;font-style:normal;font-display:swap}
@font-face{font-family:Newsreader;src:url("/fonts/newsreader.woff2") format("woff2");font-weight:500;font-style:normal;font-display:swap}
@font-face{font-family:Newsreader;src:url("/fonts/newsreader-italic.woff2") format("woff2");font-weight:500;font-style:italic;font-display:swap}
'''

CHEV = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>'

CASE = (
    "A Manhattan restaurant. Liability limits stayed. The umbrella rose from "
    "$1 million to $5 million, and employment practices liability was added."
)
FINE = (
    "The figures are the annual premium of the prior program and the new program "
    "as proposed, before any broker service fee. The difference is $49,887. "
    "The client and the prior broker are not named."
)


def shell(title, body_class, css, main, extra=""):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{h(title)}</title>
<meta name="robots" content="noindex, nofollow">
<style>
{FONT}
{css}
</style>
</head>
<body class="{body_class}">
<header class="top">
  <a class="logo" href="/" aria-label="SimpleINSURE home"><img src="/simpleinsure-wordmark.png" alt="SimpleINSURE" width="1684" height="360"></a>
  <button class="menu" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
</header>
<nav id="nav" hidden>
  <a href="/coverage/">Coverage</a>
  <a href="/policy-review/">Policy review</a>
  <a href="/about/">The firm</a>
  <a href="/contact/">Contact</a>
  <a href="{TEL}">{PHONE}</a>
</nav>
<main>{main}</main>
{extra}
<script>
(function(){{
  var b=document.querySelector(".menu"), n=document.getElementById("nav");
  if(!b||!n) return;
  b.addEventListener("click", function(){{
    var open=n.hasAttribute("hidden");
    if(open) n.removeAttribute("hidden"); else n.setAttribute("hidden","");
    b.setAttribute("aria-expanded", open?"true":"false");
  }});
}})();
</script>
</body>
</html>'''


def sample_a():
    rows = []
    blurbs = {
        "estate": "Buildings, schedules, lenders.",
        "hospitality": "Restaurants, bars, the lease.",
        "construction": "Trades, contracts, certificates.",
        "professional": "Offices and professional firms.",
        "personal": "Home, auto, and the household.",
    }
    for href, title, _sub, key in COVER:
        rows.append(
            f'<li><a href="{href}"><span><b>{h(title)}</b><small>{h(blurbs[key])}</small></span>{CHEV}</a></li>'
        )
    main = f'''
<div class="pad intro a1">
  <p class="eyebrow">Commercial and personal insurance</p>
  <h1>Start with the policy you have.</h1>
  <p class="lede">We read it before we talk about replacing it. If it should stay, that is the answer.</p>
  {pic("hero", eager=True, sizes="360px").replace("<img ", '<img class="shot" ', 1)}
</div>
<ul class="list a2">{''.join(rows)}</ul>
<section class="pad case a3" aria-label="Case study">
  <h2>Same limits. A wider umbrella.</h2>
  <p>{CASE}</p>
  <div class="nums">
    <div><span>Before</span><b>$71,196</b></div>
    <div><span>After</span><b>$21,309</b></div>
    <div><span>Less a year</span><b>$49,887</b></div>
  </div>
  <p class="fine">{FINE}</p>
</section>'''
    extra = f'''<div class="dock">
  <a class="call" href="{TEL}">Call</a>
  <a class="go" href="/quote/">Request a review</a>
</div>'''
    css = '''
:root{color-scheme:light}
*{box-sizing:border-box}
html,body{margin:0;background:#fff;color:#1B365D}
body{font-family:Franklin,Arial,sans-serif;font-weight:450;font-size:17px;line-height:1.45;padding-bottom:92px}
img{max-width:100%;display:block}
a{color:inherit}
button{font:inherit;color:inherit;background:none;border:0;padding:0}
.top{position:sticky;top:0;z-index:5;display:flex;align-items:center;justify-content:space-between;height:56px;padding:0 20px;background:#fff;border-bottom:1px solid #E4DDD2}
.logo{display:flex;align-items:center}
.logo img{height:22px;width:auto;max-width:none}
.menu{min-width:44px;min-height:44px;font-size:16px;font-weight:560}
#nav{display:flex;flex-direction:column;padding:8px 20px 16px;border-bottom:1px solid #E4DDD2;background:#fff}
#nav[hidden]{display:none}
#nav a{padding:14px 0;border-top:1px solid #E4DDD2;text-decoration:none;font-size:18px}
.pad{padding-left:22px;padding-right:22px}
.intro{padding-top:28px}
.eyebrow{margin:0 0 10px;font-size:15px;color:#3E4854}
h1{font-family:Newsreader,Georgia,serif;font-weight:500;font-size:40px;line-height:1.05;letter-spacing:-.02em;margin:0 0 12px}
.lede{margin:0 0 18px;color:#3E4854;font-size:18px;max-width:22em}
.shot{width:100%;height:140px;object-fit:cover;object-position:center 42%;border-radius:18px}
.list{list-style:none;margin:26px 0 0;padding:0 22px}
.list a{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:72px;padding:14px 0;border-top:1px solid #E4DDD2;text-decoration:none}
.list li:last-child a{border-bottom:1px solid #E4DDD2}
.list b{display:block;font-family:Newsreader,Georgia,serif;font-weight:500;font-size:24px;line-height:1.1}
.list small{display:block;margin-top:4px;color:#3E4854;font-size:15px;font-weight:450}
.list svg{flex:none;color:#1B365D}
.case{padding-top:28px;padding-bottom:8px}
.case h2{font-family:Newsreader,Georgia,serif;font-weight:500;font-size:32px;line-height:1.08;letter-spacing:-.02em;margin:0 0 10px}
.case p{margin:0;color:#3E4854;font-size:16px}
.nums{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:18px}
.nums span{display:block;color:#3E4854;font-size:13px}
.nums b{display:block;margin-top:4px;font-family:Newsreader,Georgia,serif;font-weight:500;font-size:22px;letter-spacing:-.03em;color:#1B365D}
.fine{margin-top:14px;font-size:13px;line-height:1.45;color:#3E4854}
.dock{position:fixed;left:0;right:0;bottom:0;z-index:6;display:grid;grid-template-columns:.8fr 1.4fr;gap:10px;padding:12px 20px calc(12px + env(safe-area-inset-bottom));background:#fff;border-top:1px solid #E4DDD2}
.dock a{display:flex;align-items:center;justify-content:center;min-height:48px;border-radius:999px;text-decoration:none;font-size:15px;font-weight:600}
.dock .call{color:#1B365D;border:1.5px solid #1B365D;background:#fff}
.dock .go{color:#fff;background:#1F6FC4}
@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.a1{animation:rise .5s ease both}
.a2{animation:rise .5s ease .08s both}
.a3{animation:rise .5s ease .14s both}
@media (prefers-reduced-motion:reduce){.a1,.a2,.a3{animation:none}}
'''
    return shell("Clean white preview | SimpleINSURE", "sample-a", css, main, extra)


def sample_b():
    blurbs = {
        "estate": "Buildings, schedules, lenders.",
        "hospitality": "Restaurants, bars, the lease.",
        "construction": "Trades, contracts, certificates.",
        "professional": "Offices and professional firms.",
        "personal": "Home, auto, and the household.",
    }
    rows = []
    for href, title, _sub, key in COVER:
        rows.append(
            f'<a class="row" href="{href}"><strong>{h(title)}</strong><span>{h(blurbs[key])}</span></a>'
        )
    main = f'''
<div class="pad intro a1">
  <p class="eyebrow">Commercial and personal insurance</p>
  <h1>Read it before you replace it.</h1>
  <p class="lede">Send the policy you have. If it is already right, we say so.</p>
</div>
<nav class="practices a2" aria-label="Practices">{''.join(rows)}</nav>
<section class="pad stat a3" aria-label="Case study">
  <p class="k">One account</p>
  <p class="big">$21,309</p>
  <p class="was">Before $71,196. $49,887 less a year.</p>
  <p class="story">{CASE}</p>
  <p class="fine">{FINE}</p>
</section>'''
    extra = f'''<div class="dock">
  <a class="go" href="/quote/">Request a review</a>
  <a class="call" href="{TEL}">Call {PHONE}</a>
</div>'''
    css = '''
:root{color-scheme:dark}
*{box-sizing:border-box}
html,body{margin:0;background:#071422;color:#F4F7FB}
body{font-family:Franklin,Arial,sans-serif;font-weight:450;font-size:17px;line-height:1.45;padding-bottom:118px}
img{max-width:100%;display:block}
a{color:inherit}
button{font:inherit;color:inherit;background:none;border:0;padding:0}
.top{position:sticky;top:0;z-index:5;display:flex;align-items:center;justify-content:space-between;height:56px;padding:0 20px;background:#071422;border-bottom:1px solid rgba(255,255,255,.14)}
.logo{display:flex;align-items:center}
.logo img{height:22px;width:auto;max-width:none;filter:brightness(0) invert(1)}
.menu{min-width:44px;min-height:44px;font-size:16px;font-weight:560;color:#fff}
#nav{display:flex;flex-direction:column;padding:8px 20px 16px;background:#071422;border-bottom:1px solid rgba(255,255,255,.14)}
#nav[hidden]{display:none}
#nav a{padding:14px 0;border-top:1px solid rgba(255,255,255,.14);text-decoration:none;font-size:18px;color:#fff}
.pad{padding-left:24px;padding-right:24px}
.intro{padding-top:28px}
.eyebrow{margin:0 0 14px;font-size:16px;color:#D5E0EA}
h1{font-family:Newsreader,Georgia,serif;font-weight:500;font-size:52px;line-height:.96;letter-spacing:-.03em;margin:0 0 16px;color:#fff}
.lede{margin:0;color:#D5E0EA;font-size:18px;max-width:16em}
.practices{display:flex;flex-direction:column;margin-top:28px;padding:0 24px}
.row{display:block;padding:12px 0;border-top:1px solid rgba(255,255,255,.16);text-decoration:none}
.row:last-child{border-bottom:1px solid rgba(255,255,255,.16)}
.row strong{display:block;font-family:Newsreader,Georgia,serif;font-weight:500;font-size:28px;line-height:1.05;color:#fff}
.row span{display:block;margin-top:4px;color:#D5E0EA;font-size:15px}
.stat{padding-top:36px}
.k{margin:0 0 8px;color:#D5E0EA;font-size:15px}
.big{margin:0;font-family:Newsreader,Georgia,serif;font-weight:500;font-size:64px;line-height:.9;letter-spacing:-.04em;color:#fff}
.was{margin:12px 0 0;font-size:18px;color:#F4F7FB}
.story{margin:14px 0 0;color:#D5E0EA;font-size:16px}
.fine{margin:12px 0 0;font-size:13px;line-height:1.45;color:#D5E0EA}
.dock{position:fixed;left:0;right:0;bottom:0;z-index:6;display:flex;flex-direction:column;gap:8px;padding:12px 20px calc(12px + env(safe-area-inset-bottom));background:#071422;border-top:1px solid rgba(255,255,255,.14)}
.dock .go{display:flex;align-items:center;justify-content:center;min-height:52px;border-radius:999px;background:#fff;color:#071422;text-decoration:none;font-size:16px;font-weight:650}
.dock .call{display:block;text-align:center;color:#F4F7FB;text-decoration:none;font-size:15px;padding:4px 0 2px}
@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.a1{animation:rise .5s ease both}
.a2{animation:rise .5s ease .08s both}
.a3{animation:rise .5s ease .14s both}
@media (prefers-reduced-motion:reduce){.a1,.a2,.a3{animation:none}}
'''
    return shell("Dark minimal preview | SimpleINSURE", "sample-b", css, main, extra)


def sample_c():
    cov = "".join(
        f'<a href="{href}">{h(title)}</a>' for href, title, _sub, _key in COVER
    )
    main = f'''
<section class="card hero a1">
  <p class="eyebrow">Commercial and personal insurance</p>
  <h1>A quieter way to review coverage.</h1>
  <p class="lede">Send the policy you have. We read it, then tell you what should change.</p>
  <a class="go" href="/quote/">Request a review</a>
  <a class="call" href="{TEL}">Call {PHONE}</a>
</section>
<section class="card a2" aria-labelledby="how">
  <h2 id="how">How it works</h2>
  <div class="step"><b>Read</b><span>Declarations, forms, and the endorsements behind them.</span></div>
  <div class="step"><b>Say so</b><span>If the current program is already right, we say so.</span></div>
  <div class="step"><b>Hand over</b><span>Dates, certificates, and the renewal calendar, when a move is warranted.</span></div>
</section>
<section class="card a3" aria-label="Case study">
  <h2>One restaurant account</h2>
  <p>{CASE}</p>
  <dl>
    <div><dt>Before</dt><dd>$71,196</dd></div>
    <div><dt>After</dt><dd>$21,309</dd></div>
    <div><dt>Less a year</dt><dd>$49,887</dd></div>
  </dl>
  <p class="fine">{FINE}</p>
</section>
<div class="folds a4">
  <details>
    <summary>Coverage</summary>
    <div class="fold">{cov}</div>
  </details>
  <details>
    <summary>The firm</summary>
    <div class="fold">
      <a href="/about/">The firm</a>
      <a href="/policy-review/">Policy review</a>
      <a href="/switching/">Switching brokers</a>
      <a href="/contact/">Contact</a>
    </div>
  </details>
  <details>
    <summary>Contact</summary>
    <div class="fold">
      <a href="{TEL}">{PHONE}</a>
      <a href="{MAIL}">{EMAIL}</a>
      <p>{ADDR}</p>
    </div>
  </details>
</div>'''
    css = '''
:root{color-scheme:light}
*{box-sizing:border-box}
html,body{margin:0;background:#EFE8DF;color:#1B365D}
body{font-family:Franklin,Arial,sans-serif;font-weight:450;font-size:17px;line-height:1.5}
img{max-width:100%;display:block}
button,summary{font:inherit;color:inherit}
.top{position:sticky;top:0;z-index:5;display:flex;align-items:center;justify-content:space-between;height:56px;padding:0 20px;background:#EFE8DF}
.logo{display:flex;align-items:center}
.logo img{height:22px;width:auto;max-width:none}
.menu{min-width:44px;min-height:44px;background:none;border:0;font-size:16px;font-weight:560}
#nav{display:flex;flex-direction:column;margin:0 20px 8px;padding:6px 18px;background:#fff;border-radius:16px}
#nav[hidden]{display:none}
#nav a{padding:12px 0;border-top:1px solid #E6DFD4;text-decoration:none;color:#1B365D;font-size:17px}
#nav a:first-child{border-top:0}
main{padding:8px 20px 28px}
.card{background:#fff;border-radius:22px;padding:22px 20px;margin:0 0 14px}
.eyebrow{margin:0 0 8px;font-size:15px;color:#3E4854}
h1{font-family:Newsreader,Georgia,serif;font-weight:500;font-size:36px;line-height:1.08;letter-spacing:-.02em;margin:0 0 10px}
h2{font-family:Newsreader,Georgia,serif;font-weight:500;font-size:28px;line-height:1.1;letter-spacing:-.02em;margin:0 0 6px}
.lede{margin:0 0 18px;color:#3E4854;font-size:17px}
.go{display:flex;align-items:center;justify-content:center;min-height:48px;border-radius:14px;background:#1B365D;color:#fff;text-decoration:none;font-weight:600;font-size:16px}
.call{display:block;margin-top:12px;text-align:center;color:#1B365D;font-weight:600;text-decoration:none}
.step{padding:14px 0;border-top:1px solid #E6DFD4}
.a3{margin-top:64px}
.step:first-of-type{margin-top:8px}
.step b{display:block;font-family:Newsreader,Georgia,serif;font-weight:500;font-size:22px}
.step span{display:block;margin-top:4px;color:#3E4854;font-size:16px}
.card p{margin:8px 0 0;color:#3E4854;font-size:16px}
dl{margin:16px 0 0;display:grid;gap:10px}
dl div{display:flex;justify-content:space-between;align-items:baseline;gap:12px;padding-top:10px;border-top:1px solid #E6DFD4}
dt{color:#3E4854;font-size:15px}
dd{margin:0;font-family:Newsreader,Georgia,serif;font-weight:500;font-size:26px;letter-spacing:-.03em;color:#1B365D}
.fine{margin-top:12px;font-size:13px;line-height:1.45;color:#3E4854}
.folds details{background:#fff;border-radius:18px;margin:0 0 10px;padding:0 18px}
.folds summary{display:flex;align-items:center;justify-content:space-between;min-height:56px;font-size:18px;font-weight:600;cursor:pointer;list-style:none}
.folds summary::-webkit-details-marker{display:none}
.folds summary:after{content:"+";font-weight:500;font-size:22px;color:#1B365D}
.folds details[open] summary:after{content:"\\2013"}
.fold{padding:0 0 14px}
.fold a,.fold p{display:block;padding:8px 0;color:#3E4854;text-decoration:none;font-size:16px;font-weight:450}
@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.a1{animation:rise .5s ease both}
.a2{animation:rise .5s ease .08s both}
.a3{animation:rise .5s ease .14s both}
.a4{animation:rise .5s ease .2s both}
@media (prefers-reduced-motion:reduce){.a1,.a2,.a3,.a4{animation:none}}
'''
    # The accordion uses a minus sign, not an en dash. The escape above is a unicode escape in CSS
    # written as a real hyphen via the string below if the escape is wrong. Keep a hyphen.
    css = css.replace('.folds details[open] summary:after{content:"\\2013"}', '.folds details[open] summary:after{content:"-"}')
    return shell("Soft app preview | SimpleINSURE", "sample-c", css, main)


def samples():
    return {
        "mobile-samples/a/index.html": sample_a(),
        "mobile-samples/b/index.html": sample_b(),
        "mobile-samples/c/index.html": sample_c(),
    }
