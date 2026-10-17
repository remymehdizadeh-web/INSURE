# simpleinsure.co

Static marketing site for SimpleINSURE. `python3 src/build.py` writes `out/` from `public/` and `src/`. `out/` is generated and is not committed.

Internal links, CSS, scripts, images, and fonts are relative, so the same build works at a domain root and under the GitHub Pages path `/INSURE/`. Every page sends `noindex, nofollow`. `robots.txt` disallows all crawlers.

## Run

```
python3 src/build.py
python3 -m http.server 4176 -d out --bind 127.0.0.1
```

To check the Pages subpath, serve a parent directory that contains `out/` as `INSURE/`.

## Publish

Push to `main`. `.github/workflows/pages.yml` builds the site and deploys `out/` with GitHub Pages.

Preview: https://remymehdizadeh-web.github.io/INSURE/

## Forms

Quote, policy review, partner, and certificate forms do not post to an API. They open a `mailto:info@simpleinsure.co` draft that includes the answers, then show the summary on the page with the same draft link and a `tel:` link to (516) 226-7969. Nothing is stored on the site.

## Pages

Home, coverage practices, checklists, coverage guide, policy review, quote, switching brokers, resources and glossary, client service, about, partners, licenses, and photo credits. Older industry URLs still resolve.
