# simpleinsure.co preview

Static marketing site. `python3 src/build.py` writes `out/` from `public/` and `src/`. `out/` is generated and is not committed. Internal links, CSS, scripts, images and fonts are relative, so the same build works at a domain root and under the GitHub Pages project path `/INSURE/`.

## Run
    python3 src/build.py
    python3 -m http.server 4176 -d out --bind 127.0.0.1
    # http://127.0.0.1:4176/

To check the Pages subpath, serve a parent directory that contains `out/` as `INSURE/`.

## Publish
Push to `main`. `.github/workflows/pages.yml` builds the site and deploys `out/` with GitHub Pages (`configure-pages` with `enablement: true`, `upload-pages-artifact`, `deploy-pages`).

Preview URL: https://remymehdizadeh-web.github.io/INSURE/

Pages is not on for this repo until the first successful deploy. `enablement: true` cannot turn it on with the default `GITHUB_TOKEN` (that needs `administration:write`). If the deploy fails with "Get Pages site failed", set Settings → Pages → Source to GitHub Actions once.

The quote form does not post to an API. It opens a `mailto:info@simpleinsure.co` draft and shows (516) 226-7969. The partner form does the same. `noindex, nofollow` stays on every page.

## History
Built Thu Oct 15, 2026 from Remy's v3 feedback (too many words; duplicate Call/Quote bars) plus competitor research. v1 to v3 generator layers are still in `src/`.

## Research
`findings.md` and screenshots in `../website_preview_v4_research/` (HUB, Marsh, Gallagher, Lockton, WTW, Brown & Brown, Alliant, Travelers, Chubb, Embroker, Next, Coverwallet at 1440 and 390). Structure only. No assets or text reused.

## What changed from v3
- Home rewritten for conversion: short serif headline, one-line subhead, quote-start chips above the fold on desktop and mobile.
- ONE sticky Call / Get a quote bar on mobile only. Header Call and band Call hidden on mobile so nothing duplicates. Sticky bar hidden on desktop.
- Featured anonymized case study: Manhattan restaurant. Prior program $71,196/yr to $21,309/yr (nearly $50,000, about 70%). Same liability limits. Umbrella $1M to $5M. Employment practices added. Source: Remy's emails. Client and prior broker never named.
- Ruthless copy cuts. Five line cards (photo rails). Three short steps. Closing band.
- Real facts only: NY DFS BR-1984615, Garden City 900 Stewart Ave Ste 210, (516) 226-7969. No invented stats, testimonials or carrier logos.
- Motion: line-rise headline, hero ken burns, case-study money count and bar fill, scroll reveals. Reduced motion respected. Photo credits and noindex kept.

## Lighthouse (13.5.0)
- Home mobile: Performance 93, Accessibility 100, Best Practices 100, SEO 69 (noindex). FCP ~1.8s, LCP ~3.2s, CLS 0.001.
- Home desktop: Performance 99, Accessibility 100.
- Quote mobile: Performance 99, Accessibility 100.
Reports in `lighthouse/`.

## Deliverables
- Screenshots: `screenshots/home-{desktop,mobile}-first-screen.png`, full pages for every route, section shots, `compare-v3-v4-*.png`.
- Demo: `video/simpleinsure_v4.mp4` (~20s, under 60s).
- Local server PID may vary; restart with the Run commands above.

## Inner pages polish (same day)
About, partners, legal, quote and all three industry pages rebuilt to the home standard: short copy, photo heroes on industry pages, one sticky bar on mobile, hours removed site-wide until Remy confirms. Lighthouse mobile (all pages): Performance 93–99, Accessibility 100, SEO 69 (noindex).

## Remaining (needs Remy)
1. Client consent to name the restaurant or use a written testimonial.
2. Carrier / wholesaler relationships Remy is willing to name.
3. Commissioned photography (replace Commons credits).
4. Google / Nextdoor review count once reviews exist.
5. First merge to `main` so GitHub Pages can publish the preview. A custom domain at the root can reuse this build because URLs are relative.
6. Confirm hours (GBP says 9 to 6; site says 9 to 5).
