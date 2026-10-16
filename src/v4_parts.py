# v4 overrides, exec'd after v3_parts.py
def v4fix(s):
    return s
_head_v3 = head
def head(title, desc, path, extra=""):
    h = _head_v3(title, desc, path, extra)
    h = h.replace('<link rel="stylesheet" href="/v3m.css">', '<link rel="stylesheet" href="/v3m.css"><link rel="stylesheet" href="/v4.css">')
    if path == "":
        h = h.replace('imagesizes="(max-width:620px) 100vw, 50vw"', 'imagesizes="100vw"')
    return h

ARROW = '<span class="arr" aria-hidden="true">→</span>'
QTYPES = [("building","Building or real estate"),("restaurant","Restaurant or bar"),("contractor","Contractor"),("business","Small business"),("personal","Home and auto")]
def qstart(cls=""):
    chips = "".join(f'<a class="chip" href="/quote?type={k}">{t}{ARROW}</a>' for k,t in QTYPES)
    return f'<div class="qs {cls}"><p class="qs-h">What do you need to insure?</p><div class="chips">{chips}</div><p class="qs-f">Free, no obligation. Or call <a href="{TEL}">{PHONE}</a>.</p></div>'

def home():
    cards = [("building","/new-york-building-insurance","Real estate","Buildings","Apartment, mixed-use and commercial property."),
             ("restaurant","/new-york-restaurant-insurance","Hospitality","Restaurants","Property, liquor liability, comp and more."),
             ("contractor","/new-york-contractor-insurance","Construction","Contractors","Coverage that meets NYC and GC contracts."),
             ("business","/quote?type=business","Small business","Small business","Offices, retail and service firms.")]
    alts = {"building":"Brownstones on Park Place, Brooklyn","restaurant":"Counter service at a Manhattan diner","contractor":"Crew installing a sidewalk shed in Manhattan","business":"An independent bookstore in Brooklyn"}
    ind = "".join(f'<a class="lc" href="{u}"><div class="im">{pic(k,alts[k],sizes="(max-width:767px) 82vw, 25vw")}</div><div class="b"><span class="k">{kk}</span><h3>{t}</h3><p>{p}</p><span class="lnk">Explore{ARROW}</span></div></a>' for k,u,kk,t,p in cards)
    ind += f'<a class="lc lc-t" href="/quote?type=personal"><div class="b"><span class="k">Personal lines</span><h3>Home, auto and umbrella</h3><p>For owners and their families.</p><span class="lnk">Get a quote{ARROW}</span></div></a>'
    return head("New York Commercial Insurance Broker | SimpleINSURE","Licensed New York insurance broker for buildings, restaurants, contractors, small businesses and personal lines. Garden City, NY. Free quotes.","") + header() + f"""
<section class="h4" aria-label="Introduction">
<div class="h4-bg">{pic("hero","Lower Manhattan skyline from the Hudson River",px="0.06",eager=True,sizes="100vw")}</div>
<div class="wrap h4-in">
<div class="h4-copy"><p class="eyb">Licensed New York insurance broker</p>
<h1 class="h1m"><span class="ln"><span>Insurance for</span></span> <span class="ln"><span>the businesses</span></span> <span class="ln"><span>that build <em>New York.</em></span></span></h1>
<p class="h4-sub">One licensed broker for buildings, restaurants, contractors and small business.</p>
<ul class="h4-trust"><li>NY DFS License BR-1984615</li><li>Garden City, NY</li></ul></div>
{qstart("h4-qs")}
</div><p class="h4-cr">{credit("hero")}</p></section>

<section class="proof4" aria-label="Credentials"><div class="wrap p4">
<div><b>Licensed by NY DFS</b><span>License BR-1984615 · <a href="https://myportal.dfs.ny.gov/nylinxext/elsearch.alice" rel="noopener">Verify</a></span></div>
<div><b>Garden City office</b><span>900 Stewart Ave, Ste 210</span></div>
<div><b>Admitted and specialty markets</b><span>We shop your account</span></div>
<div><b>One broker</b><span>Quote, certificates, claims</span></div></div></section>

<section class="cs4" id="case-study" aria-labelledby="cs-h"><div class="wrap cs-in">
<div class="cs-l"><p class="eyb">Case study · Manhattan restaurant</p>
<h2 id="cs-h">Left a national broker. <em>Better coverage, far less premium.</em></h2>
<ul class="cs-list"><li><b>Same</b> liability limits</li><li><b>Umbrella</b> raised from $1M to $5M</li><li><b>Employment practices</b> added, previously excluded</li></ul>
<a class="btn w" href="/quote">Get your policy reviewed{ARROW}</a></div>
<div class="cs-r" aria-label="Annual premium went from $71,196 to $21,309">
<div class="cs-row"><span class="cs-k">Before</span><span class="cs-n strike" data-money="71196">$71,196</span><span class="cs-u">a year</span></div>
<div class="cs-bar"><i style="--w:100%"></i></div>
<div class="cs-row"><span class="cs-k">After</span><span class="cs-n" data-money="21309">$21,309</span><span class="cs-u">a year</span></div>
<div class="cs-bar"><i class="after" style="--w:30%"></i></div>
<p class="cs-save">Nearly <b>$50,000</b> saved a year, about 70%.</p>
<p class="cs-fine">Annual premium of the prior program versus the new program as proposed, before broker service fees. Client not named for privacy. Every account is different and results depend on underwriting.</p></div>
</div></section>

<section class="ln4" aria-labelledby="ln-h"><div class="wrap"><div class="sec-h"><p class="eyb dk">Who we insure</p><h2 id="ln-h">Five lines. <em>One broker.</em></h2></div>
<div class="rail">{ind}</div></div></section>

<section class="how4" aria-labelledby="how-h"><div class="wrap"><div class="sec-h"><p class="eyb dk">How it works</p><h2 id="how-h">Three steps.</h2></div>
<ol class="steps4"><li><span>01</span><h3>Tell us the account</h3><p>Two questions, or send your current policy.</p></li><li><span>02</span><h3>We go to market</h3><p>Admitted and specialty carriers.</p></li><li><span>03</span><h3>You choose</h3><p>Price, limits and gaps, side by side.</p></li></ol></div></section>

<section class="band4" aria-labelledby="band-h"><div class="band-bg" data-px="0.1" style="background-image:url(/photos/state-1600.webp)" role="img" aria-label="Lower Manhattan skyline"></div>
<div class="wrap band-in"><h2 id="band-h">Paying too much? <em>Find out free.</em></h2><p>Send your declarations page. A licensed broker reviews it.</p>
<div class="band-cta"><a class="btn w" href="/quote">Start a quote{ARROW}</a><a class="btn o" href="{TEL}">Call {PHONE}</a></div><p class="band-cr">{credit("state")}</p></div></section>
""" + footer()


def _page_band(h2, sub, cta="/quote", cta_t="Start a quote"):
    return f"""<section class="band4" aria-label="Call to action"><div class="band-bg" data-px="0.1" style="background-image:url(/photos/state-1600.webp)" role="img" aria-label="Lower Manhattan skyline"></div>
<div class="wrap band-in"><h2>{h2}</h2><p>{sub}</p>
<div class="band-cta"><a class="btn w" href="{cta}">{cta_t}{ARROW}</a><a class="btn o" href="{TEL}">Call {PHONE}</a></div>
<p class="band-cr">{credit("state")}</p></div></section>"""

def about():
    return head("About SimpleINSURE | Licensed New York Insurance Broker","Independent New York DFS licensed broker, License BR-1984615. Buildings, restaurants, contractors, small business and personal lines. Garden City, NY.","/about") + header() + f"""
<section class="ph4"><div class="wrap"><p class="eyb dk">About</p>
<h1 class="h1m"><span class="ln"><span>A New York broker</span></span> <span class="ln"><span>who reads the policy</span></span> <span class="ln"><span><em>before quoting it.</em></span></span></h1>
<p class="ph4-sub">Licensed by NY DFS, BR-1984615. Based in Garden City. Serving clients across New York remotely.</p></div></section>
<section class="proof4" aria-label="Credentials"><div class="wrap p4">
<div><b>NY DFS License BR-1984615</b><span><a href="https://myportal.dfs.ny.gov/nylinxext/elsearch.alice" rel="noopener">Verify</a></span></div>
<div><b>Garden City office</b><span>900 Stewart Ave, Ste 210</span></div>
<div><b>Independent broker</b><span>We work for you, not one carrier</span></div>
<div><b>Remote across NY</b><span>Phone, email and video</span></div></div></section>
<section class="pg4"><div class="wrap cols2">
<div class="prose4"><h2>Who we are</h2>
<p>SimpleINSURE Brokerage LLC places commercial insurance for buildings, restaurants, contractors and small businesses, plus home, auto and umbrella for the people who own them.</p>
<p>We take each account to admitted and specialty markets. When the standard market says no, we go to surplus lines through wholesale partners.</p>
<h2>How we work</h2>
<ol class="steps4 tight"><li><span>01</span><h3>Start with what you have</h3><p>Send the policy you already carry.</p></li>
<li><span>02</span><h3>We tell you the truth</h3><p>If it is already right, we say so.</p></li>
<li><span>03</span><h3>We stay on the account</h3><p>Certificates, changes and renewals.</p></li></ol></div>
<div class="card founder"><div class="ph stub"><span>Photo of Remy, to be supplied</span></div>
<h2>Remy Mehdizadeh</h2><p class="role">Founder [title and personal license to confirm]</p>
<p>Started SimpleINSURE in 2026 so New York owners get one licensed broker from quote to claim.</p>
<div class="ctas"><a class="btn p sm" href="{TEL}">Call {PHONE}</a><a class="btn s sm" href="mailto:info@simpleinsure.co">Email us</a></div></div>
</div></section>
""" + _page_band("Ready to talk?", "A licensed broker will follow up.") + footer()

def partners():
    cards = [("Attorneys","Real estate attorneys","Binders and evidence of insurance for closings. We read the loan requirements first."),
             ("Managers","Property managers","One contact for renewals, vendor certificates and non-renewals."),
             ("CPAs","Accountants","Workers comp, NY disability and Paid Family Leave when clients hire.")]
    grid = "".join(f'<div class="pcard"><span class="k">{k}</span><h2 style="font-family:var(--serif);font-weight:500;font-size:26px;margin:10px 0 8px">{t}</h2><p>{p}</p></div>' for k,t,p in cards)
    return head("Referral Partners | SimpleINSURE","Real estate attorneys, property managers and accountants: introduce New York clients to a licensed broker. No fees to unlicensed persons.","/partners") + header() + f"""
<section class="ph4"><div class="wrap"><p class="eyb dk">Referral partners</p>
<h1 class="h1m"><span class="ln"><span>Partners that</span></span> <span class="ln"><span>owners already <em>trust.</em></span></span></h1>
<p class="ph4-sub">Attorneys, property managers and accountants. Introduce a client. We keep you informed.</p></div></section>
<section class="pg4"><div class="wrap"><div class="pgrid">{grid}</div>
<div class="cols2" style="margin-top:64px;align-items:start">
<div><p class="eyb dk">How it works</p><h2>Three steps for you.</h2>
<ol class="steps4 tight"><li><span>01</span><h3>Introduce</h3><p>Email us or use the form.</p></li>
<li><span>02</span><h3>We contact them</h3><p>Promptly, and we copy you if they agree.</p></li>
<li><span>03</span><h3>We update you</h3><p>When the client is placed.</p></li></ol>
<div class="note4"><b>Referral policy.</b> We do not pay fees or share commissions with unlicensed persons (NY Ins. Law § 2116). Partners get a responsive broker, referrals back where they fit, and updates with the client's permission.</div></div>
<form class="card qs" style="box-shadow:none;border:1px solid var(--rule)" onsubmit="return partnerMail(event)">
<p class="qs-h">Become a partner</p>
<div class="ph-note">Opens an email to info@simpleinsure.co. Nothing is saved on this site.</div>
<div class="g2"><div class="field"><label for="pn">Name</label><input id="pn" autocomplete="name"></div>
<div class="field"><label for="pf">Firm</label><input id="pf" autocomplete="organization"></div>
<div class="field"><label for="pr">Role</label><select id="pr"><option>Real estate attorney</option><option>Property manager</option><option>Accountant or CPA</option><option>Other</option></select></div>
<div class="field"><label for="pe">Email</label><input id="pe" type="email" autocomplete="email"></div>
<div class="field"><label for="pp">Phone</label><input id="pp" type="tel" autocomplete="tel"></div>
<div class="field"><label for="pc">Client now?</label><select id="pc"><option>No, not yet</option><option>Yes</option></select></div></div>
<button class="btn p" style="width:100%;margin-top:18px" type="submit">Email us</button>
<p class="ok fine" hidden>If your email app did not open, <a class="mailfall" href="mailto:info@simpleinsure.co">email info@simpleinsure.co</a> or call <a href="{TEL}">{PHONE}</a>.</p></form>
<script>
function partnerMail(e){{
  e.preventDefault();
  var f=e.target, lines=[];
  f.querySelectorAll("input,select,textarea").forEach(function(el){{
    var lab=f.querySelector('label[for="'+el.id+'"]');
    if(lab&&String(el.value||"").trim()) lines.push(lab.textContent.trim()+": "+String(el.value).trim());
  }});
  var href="mailto:info@simpleinsure.co?subject="+encodeURIComponent("Referral partner introduction")+"&body="+encodeURIComponent(lines.join("\\n"));
  var ok=f.querySelector(".ok"); if(ok) ok.hidden=false;
  var a=f.querySelector(".mailfall"); if(a) a.href=href;
  window.location.href=href;
  return false;
}}
</script>
</div></div></section>
""" + footer()

def legal():
    return head("Legal, Privacy and How We Are Paid | SimpleINSURE","Licensing, compensation disclosure and privacy for SimpleINSURE Brokerage LLC, NY DFS License BR-1984615.","/legal") + header() + f"""
<section class="ph4"><div class="wrap"><p class="eyb dk">Legal</p>
<h1>Licensing, compensation and privacy.</h1></div></section>
<section class="pg4"><div class="wrap prose4 narrow">
<h2 id="licensing">Licensing</h2>
<p>SimpleINSURE Brokerage LLC is a licensed property and casualty insurance broker, New York DFS License BR-1984615. <a href="https://myportal.dfs.ny.gov/nylinxext/elsearch.alice" rel="noopener">Verify on the DFS licensee search.</a></p>
<h2 id="how-we-are-paid">How we are paid</h2>
<div class="ph-note">Draft for counsel review against 11 NYCRR 30 (Regulation 194) before publishing.</div>
<p>We are usually paid a commission by the insurer that issues your policy, as a percentage of premium. We may also receive other compensation from insurers, such as contingent payments based on overall business placed. Ask us about the compensation we expect on your policy and about alternative quotes we presented. We will provide it.</p>
<h2>Coverage descriptions</h2>
<p>Descriptions on this site are general summaries only. They are not an offer or a binder. Coverage is subject to underwriting and the issued policy.</p>
<h2>Privacy</h2>
<p>The live site's privacy notice (form data, 23 NYCRR 500 and the client portal) carries over unchanged. It is not reproduced in this preview.</p>
</div></section>
""" + footer()

INDUSTRY = {
 "new-york-building-insurance": dict(
  title="New York Building and Landlord Insurance | SimpleINSURE",
  desc="Apartment, mixed-use and commercial building insurance in New York. Licensed broker, BR-1984615. Free quotes.",
  eyb="Real estate", h1a="Building insurance", h1b="for New York owners.",
  sub="Apartment, mixed-use and commercial property. Single buildings or schedules.",
  photo="building", photo_alt="Brownstones on Park Place, Brooklyn",
  type="building", cta="Get a building quote",
  cov=[("Property","Building and improvements"),("General liability","Premises and operations"),("Umbrella","Higher limits for lenders"),("Workers comp","For staff and supers")],
  faqs=[("What does a lender usually require?","General liability with the lender as additional insured, property coverage matching the loan, and often an umbrella. Send the requirements. We match them."),
        ("Do you handle multi-building schedules?","Yes. Single properties and schedules across New York."),
        ("Can you issue certificates quickly?","Yes. Certificates for lenders, vendors and tenants are part of how we service accounts.")]),
 "new-york-restaurant-insurance": dict(
  title="New York Restaurant and Bar Insurance | SimpleINSURE",
  desc="Restaurant and bar insurance in New York: property, liability, liquor, workers comp. Licensed broker, BR-1984615.",
  eyb="Hospitality", h1a="Restaurant insurance", h1b="done properly.",
  sub="Property, liability, liquor liability, workers comp, DBL and PFL.",
  photo="restaurant", photo_alt="Counter service at a Manhattan diner",
  type="restaurant", cta="Get a restaurant quote",
  cov=[("Business owners policy","Property and liability packaged"),("Liquor liability","Dram Shop Act exposure"),("Workers comp","Required for NY employers"),("NY DBL and PFL","Disability and Paid Family Leave")],
  faqs=[("Do I need liquor liability in New York?","Most landlords require it, and the Dram Shop Act can make you liable for harm caused by a guest you served."),
        ("What does my lease usually require?","General liability with the landlord as additional insured, property on your improvements, and often an umbrella. Send the insurance section."),
        ("Is workers comp required for a small restaurant?","Yes. New York requires workers compensation and disability and Paid Family Leave for nearly every employer.")]),
 "new-york-contractor-insurance": dict(
  title="New York Contractor Insurance | SimpleINSURE",
  desc="Contractor and trade insurance in New York: GL that meets NYC and GC contracts, comp, auto, certificates. Licensed broker.",
  eyb="Construction", h1a="Contractor insurance", h1b="that meets the job.",
  sub="General liability for NYC and GC contracts, workers comp, auto and certificates.",
  photo="contractor", photo_alt="Crew installing a sidewalk shed in Manhattan",
  type="contractor", cta="Get a contractor quote",
  cov=[("General liability","Contract and NYC requirements"),("Workers comp","Payroll and class codes"),("Commercial auto","Vehicles and tools in transit"),("Umbrella","Higher limits when the GC asks")],
  faqs=[("Can you meet NYC contract insurance requirements?","We place GL and certificates to match the schedule in your contract. Send the insurance section."),
        ("Do you handle certificates for GCs?","Yes. Certificate and waiver requests are part of the service."),
        ("What if I use subcontractors?","Tell us. It changes how the policy is structured.")]),
}

def industry(slug):
    d = INDUSTRY[slug]
    cov = "".join(f'<div><b>{a}</b><span>{b}</span></div>' for a,b in d["cov"])
    faq = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in d["faqs"])
    faq_ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in d["faqs"]]})
    extra = f'<script type="application/ld+json">{faq_ld}</script>'
    return head(d["title"], d["desc"], "/"+slug, extra) + header(f"/quote?type={d['type']}") + f"""
<section class="ih4"><div class="ih4-bg">{pic(d["photo"], d["photo_alt"], px="0.06", eager=True, sizes="100vw")}</div>
<div class="wrap ih4-in"><div><p class="eyb">{d["eyb"]}</p>
<h1 class="h1m"><span class="ln"><span>{d["h1a"]}</span></span> <span class="ln"><span><em>{d["h1b"]}</em></span></span></h1>
<p class="h4-sub">{d["sub"]}</p>
<ul class="h4-trust"><li>NY DFS License BR-1984615</li><li>Garden City, NY</li></ul>
<div class="ctas ih-ctas"><a class="btn w" href="/quote?type={d['type']}">{d["cta"]}{ARROW}</a></div></div></div>
<p class="h4-cr">{credit(d["photo"])}</p></section>
<section class="pg4"><div class="wrap"><div class="sec-h"><p class="eyb dk">Coverage</p><h2>What we place.</h2></div>
<div class="cov4">{cov}</div></div></section>
<section class="how4"><div class="wrap"><div class="sec-h"><p class="eyb dk">How it works</p><h2>Three steps.</h2></div>
<ol class="steps4"><li><span>01</span><h3>Tell us the account</h3><p>A short form, or send the policy you have.</p></li>
<li><span>02</span><h3>We go to market</h3><p>Admitted and specialty carriers.</p></li>
<li><span>03</span><h3>You choose</h3><p>Price, limits and gaps, side by side.</p></li></ol></div></section>
<section class="pg4"><div class="wrap"><div class="sec-h"><p class="eyb dk">Questions</p><h2>Asked first.</h2></div>
<div class="faq4">{faq}</div></div></section>
""" + _page_band("Ready for options?", "A licensed broker follows up.", f"/quote?type={d['type']}", d["cta"]) + footer()

_quote_v3 = quote
def quote():
    s = v4fix(_quote_v3())
    s = s.replace("Two minutes to start. ", "")
    s = s.replace('<div class="ph-note">Placeholder quote form for review. It is not connected and sends nothing. On the real site it will save to the existing /api/policy-review/partial route.</div>',
                  '<div class="ph-note">Preview form. Opens an email to info@simpleinsure.co. Nothing is saved on this site.</div>')
    s = s.replace(
        '<div id="done" hidden><h2 style="font-size:30px">Thanks. This is where the confirmation will show.</h2><p class="lead" style="font-size:17px">Preview only: nothing was sent. On the live site: "A licensed broker will review this and contact you within [confirm] business days. If it is urgent, call (516) 226-7969."</p></div>',
        '<div id="done" hidden><h2 style="font-size:30px">Thanks. This is where the confirmation will show.</h2><p class="lead" style="font-size:17px">This preview cannot store the form. Your email app should open a draft to <a id="mailfall" href="mailto:info@simpleinsure.co">info@simpleinsure.co</a>. Send that email, or call <a href="tel:+15162267969">(516) 226-7969</a>. A policy file is not attached; add it to the email or mention it when you call.</p></div>')
    s = s.replace(
        "document.getElementById('next').onclick=function(){if(step<4)go(step+1);else{document.querySelectorAll('[data-step]').forEach(function(f){f.hidden=true});document.getElementById('nav').hidden=true;document.getElementById('done').hidden=false;document.getElementById('qh').textContent='Request received (preview)'}};",
        "document.getElementById('next').onclick=function(){if(step<4){go(step+1);return}var lines=[];document.querySelectorAll('#qf input,#qf select,#qf textarea').forEach(function(el){if(!el.id||el.type==='checkbox'||el.type==='file')return;var lab=document.querySelector('label[for=\"'+el.id+'\"]');if(lab&&String(el.value||'').trim())lines.push(lab.textContent.trim()+': '+String(el.value).trim())});var cov=[];document.querySelectorAll('#cov input:checked+span').forEach(function(n){cov.push(n.textContent.trim())});if(cov.length)lines.push('Coverage: '+cov.join(', '));var kind=(document.getElementById('qlabel').textContent||'Quote').replace(/^Get a quote\\s*·\\s*/,'');lines.unshift('Type: '+kind);var up=document.getElementById('up');if(up&&up.files&&up.files[0])lines.push('Policy file (not attached): '+up.files[0].name);var href='mailto:info@simpleinsure.co?subject='+encodeURIComponent('Quote request: '+kind)+'&body='+encodeURIComponent(lines.join('\\n'));var fall=document.getElementById('mailfall');if(fall)fall.href=href;document.querySelectorAll('[data-step]').forEach(function(f){f.hidden=true});document.getElementById('nav').hidden=true;document.getElementById('done').hidden=false;document.getElementById('qh').textContent='Request received (preview)';window.location.href=href};")
    s = s.replace("Send my request (preview)", "Email my request")
    s = s.replace('A licensed broker reviews your details and calls if anything is unclear.</li><li>We take the account to the carriers that write this kind of business, including specialty markets through our wholesale partners.</li><li>You get options side by side, with the differences explained.',
                  'A licensed broker reviews your details.</li><li>We take the account to market.</li><li>You get options side by side.')
    s = s.replace('Prefer to talk it through? Answer the same questions in chat, or call', 'Prefer to talk? Call')
    return s

_photo_credits = photo_credits
def photo_credits():
    return v4fix(_photo_credits())

# keep home as already defined above; re-bind wrappers that still need v4fix
_home_keep = home
def home():
    return v4fix(_home_keep())
