# Technical SEO audit

## Scope and collection

Start from the URL set in sitemaps, navigation and relevant first-party exports. Keep the requested URL, final URL, capture time, host and method. Sample by template and commercial relevance; report the actual denominators. Reuse evidence where possible. For online work use the target owner's constraints and pause on refusal or rate limiting.

Use the provided local parser with a UTF-8 JSON file. Minimal input:

```json
{"schema_version":1,"pages":[{"url":"https://example.test/","http":{"status":200,"final_url":"https://example.test/","headers":{"content-type":"text/html"}},"html":"<title>Catalog</title><h1>Catalog</h1>"}]}
```

The optional `rendered_html` holds a post-render DOM snapshot. `http`, `html` and `rendered_html` are independent observations. An absent view is null. An empty list in an observed view means the corresponding item was absent from that capture. Labels and entity values in titles and structured data still require human verification. JSON-LD parsing checks syntax and reports the top-level JSON value type, such as object or array. It does not extract the Schema.org @type.

## Cross-checks

- Compare status and redirect destination with sitemaps, navigation and expected page function. Record timing and client context before assuming a difference persists.
- Check robots.txt rules by intended crawler, X-Robots-Tag, meta directives, declared canonicals and signals from internal links. Preserve their sources. A declared canonical alone is weak evidence of the selected canonical.
- If Search Console or verified exports are available, record property scope, filter, date, and selected examples. Match URL-level examples to the site's inventory, using the aggregate counts only for their own universe.
- Compare request responses with authorized CDN and origin aggregates or verified crawler observations when access differs. Correlate windows, paths and statuses. Keep origin and edge responses distinct.
- Compare source and rendered titles, H1, directives and JSON-LD. Validate structured data against primary eligibility guidance. Check labels and text against the purpose of the page.
- When testing UX, follow keyboard or pointer through the important action and record viewport, focus, accessible name and feedback. Report performance lab results separately from field data.

Sources: [Google Search Essentials](https://developers.google.com/search/docs/essentials), [indexing report](https://support.google.com/webmasters/answer/7440203), [HTTP response behavior](https://developers.google.com/search/docs/crawling-indexing/http-network-errors), [Web Vitals](https://web.dev/articles/vitals), [W3C accessibility checks](https://www.w3.org/WAI/test-evaluate/easy-checks/).

## Crawler identity and scope

A custom User-Agent only identifies what the client declared. Use the provider's URL inspection tool or verified crawler records to determine what a search service received. One HTTP response, even from an official live test, measures the sampled time and URL. A noindex directive is evidence about the tested search surface under its rules. Treat assertions about other engines, visibility in answers, and lost traffic as separate claims that require evidence.
