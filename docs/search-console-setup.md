# Search Console and Bing Webmaster Tools

These steps are for the live site, https://www.simpleinsure.co. The GitHub Pages preview stays noindex, so verify the domain property on the live domain, not on the preview.

You need access to the GoDaddy account that holds the DNS for simpleinsure.co, and a Google account that should own Search Console.

## Google Search Console, domain property

1. Open https://search.google.com/search-console and sign in with the Google account that should own the property.
2. Click Add property.
3. Choose Domain, not URL prefix. Enter `simpleinsure.co` with no https and no www.
4. Search Console shows a TXT record. Copy the value. It looks like `google-site-verification=` followed by a long token.
5. In GoDaddy, open the domain simpleinsure.co, then DNS.
6. Add a record:
   - Type: TXT
   - Name: `@` (the root). Leave it blank if GoDaddy uses a blank host field for the root.
   - Value: the full token from Search Console, including `google-site-verification=`.
   - TTL: 1 hour, or the default.
7. Save. Do not delete the existing TXT records. The root already has an MS record for Microsoft 365 and an SPF record. Add this as another TXT record.
8. Wait for DNS to update. A few minutes is common. It can take longer.
9. Back in Search Console, click Verify.
10. If it fails, check that the TXT name is the root and that the value has no extra quotes or spaces, then try again.

A domain property covers both www.simpleinsure.co and the bare domain, and both http and https.

## Submit the sitemap in Search Console

1. Open the simpleinsure.co property.
2. In the left menu, open Sitemaps.
3. Enter `sitemap.xml` and submit.
4. The live file is https://www.simpleinsure.co/sitemap.xml. It lists the public pages, including the restaurant, contractor, and building owner pages.
5. After it succeeds, use URL inspection for the home page and the three industry pages, and request indexing for each.

## Bing Webmaster Tools, import from Search Console

1. Open https://www.bing.com/webmasters and sign in with a Microsoft account.
2. Choose Import from Google Search Console.
3. Sign in with the same Google account that owns the Search Console property and allow the connection.
4. Select the simpleinsure.co domain property and import it.
5. Bing pulls the verified site across. Open Sitemaps and confirm `https://www.simpleinsure.co/sitemap.xml` is listed. Submit it if the import did not.
6. Use URL submission for the home page and the three industry pages if you want Bing to fetch them sooner.

## What this does not change

Search Console verification does not require a meta tag on the site when you use the DNS TXT method. No page copy changes for this setup.
