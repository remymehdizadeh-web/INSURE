# v3 overrides, exec'd after v2_parts.py
V3_FIX = [
 ("usually within 48 hours", "as quickly as the carriers respond"),
 ("quotes in about 48 hours", "quotes from a licensed broker"),
 (", often the same day", " promptly"),
 ("Certificates turned around fast, often the same day.", "Certificates handled promptly."),
 ("We contact your client within one business day", "We contact your client promptly"),
 ("Two minutes to start.", "A short form to start."),
 ("Every New York county, by phone, email and video", "Anywhere in New York, by phone, email and video"),
 ("\u2014", ", "),
]
def v3fix(s):
    for a, b in V3_FIX: s = s.replace(a, b)
    return s

_head_v2 = head
def head(title, desc, path, extra=""):
    return _head_v2(title, desc, path, extra).replace('<script src="/motion.js" defer></script>', '<script src="/motion.js" defer></script><link rel="stylesheet" href="/v3.css"><link rel="stylesheet" href="/v3m.css"><script src="/v3.js" defer></script>', 1)

_header_v2 = header
def header(cta="/quote"):
    return '<div class="prog-bar" aria-hidden="true"></div>' + _header_v2(cta)

LINES = ["Real estate and buildings", "Restaurants and bars", "Contractors and trades", "Small business", "Home, auto and umbrella"]
def marquee():
    items = "".join(f'<span>{t}</span><i aria-hidden="true"></i>' for t in LINES)
    return f'<div class="mq"><p class="sr-only" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Lines of business: {", ".join(LINES)}</p><div class="mq-t" aria-hidden="true">{items}{items}</div></div>'

STATS_V3 = f"""<div class="stats v3s">
<div class="stat"><span class="n" data-count="5">5</span><p>Lines of business: real estate and buildings, restaurants, contractors, small business and personal lines</p></div>
<div class="stat"><span class="n t lic" data-lic="BR-1984615">BR-1984615</span><p>Our New York DFS insurance broker license number. <a href="https://myportal.dfs.ny.gov/nylinxext/elsearch.alice" rel="noopener">Verify it</a></p></div>
<div class="stat"><span class="n t">Garden City</span><p>Based at 900 Stewart Ave, Ste 210, Garden City, NY, serving clients across New York remotely</p></div>
<div class="stat"><span class="n t">Licensed</span><p>One licensed broker from quote to claim: certificates, changes and renewals</p></div></div>"""

_home_v2 = home
def home():
    s = _home_v2()
    s = re.sub(r'<div class="stats">.*?</div></div></div></section>', STATS_V3 + '</div></section>', s, count=1, flags=re.S)
    assert 'data-count="62"' not in s
    # split h1 into masked lines for the hero reveal (transform only, text stays opaque)
    s = s.replace('<h1>Commercial insurance for New York <em>buildings, restaurants</em> and <em>contractors.</em></h1>',
      '<h1 class="h1m"><span class="ln"><span>Commercial</span></span> <span class="ln"><span>insurance for</span></span> <span class="ln"><span>New York <em>buildings,</em></span></span> <span class="ln"><span><em>restaurants</em> and</span></span> <span class="ln"><span><em>contractors.</em></span></span></h1>')
    s = s.replace('{creds_marker}', '')
    s = s.replace('<div class="creds">', marquee() + '<div class="creds">', 1)
    return s

for _n in ("quote","about","partners","legal","photo_credits","industry","home"):
    _f = globals()[_n]
    def _w(*a, _f=_f): return v3fix(_f(*a))
    globals()[_n] = _w
