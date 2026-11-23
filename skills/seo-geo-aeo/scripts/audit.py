"""Inspect captured SEO signals without making network requests."""

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
from urllib.parse import urljoin, urlsplit


def reject_constant(value):
    raise ValueError(f"{value} is not valid JSON")


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def parse_json(text):
    return json.loads(
        text,
        parse_constant=reject_constant,
        object_pairs_hook=unique_keys,
    )


def require_http_url(value, field):
    if not isinstance(value, str) or any(char.isspace() for char in value):
        raise ValueError(f"{field} must be an absolute HTTP(S) URL")
    try:
        url = urlsplit(value)
        if url.scheme in ("http", "https") and url.hostname and url.username is None:
            _ = url.port
            return value
    except ValueError:
        pass
    raise ValueError(f"{field} must be an absolute HTTP(S) URL without credentials")


def resolve_href(base, href):
    if href is None:
        return None
    try:
        return urljoin(base, href)
    except ValueError:
        return None


def relations(attributes):
    return (attributes.get("rel") or "").lower().split()


class PageHTML(HTMLParser):
    """Collect explicit HTML signals using the standard library parser."""

    def __init__(self):
        super().__init__()
        self.base_href = None
        self.titles = []
        self.h1 = []
        self.canonical = []
        self.meta_robots = []
        self.json_ld = []
        self.links = []
        self._text = {}
        self._json_ld_text = None
        self._inert_depth = 0

    def handle_starttag(self, tag, attributes):
        if tag == "template":
            self._inert_depth += 1
        if self._inert_depth:
            return

        attrs = {}
        for key, value in attributes:
            attrs.setdefault(key, value if value is not None else "")

        if tag in ("title", "h1"):
            self.finish_text(tag)
            self._text[tag] = []
        elif tag == "base" and self.base_href is None:
            self.base_href = attrs.get("href")
        elif tag == "link" and "canonical" in relations(attrs):
            self.canonical.append(attrs.get("href"))
        elif tag == "meta":
            name = attrs.get("name", "").strip().lower()
            if name == "robots" or name.split("-", 1)[0].endswith("bot") or name == "slurp":
                self.meta_robots.append({"name": name, "content": attrs.get("content")})
        elif tag in ("a", "area") and "href" in attrs:
            self.links.append({"href": attrs["href"], "rel": relations(attrs)})
        elif tag == "script":
            script_type = attrs.get("type", "").partition(";")[0].strip().lower()
            if script_type == "application/ld+json":
                self._json_ld_text = []

    def handle_endtag(self, tag):
        if self._inert_depth:
            if tag == "template":
                self._inert_depth -= 1
            return
        self.finish_text(tag)
        if tag == "script":
            self.finish_json_ld()

    def handle_data(self, data):
        if self._inert_depth:
            return
        if self._json_ld_text is not None:
            self._json_ld_text.append(data)
        elif not self.cdata_elem:
            for segments in self._text.values():
                segments.append(data)

    def finish_text(self, tag):
        segments = self._text.pop(tag, None)
        if segments is not None:
            items = self.titles if tag == "title" else self.h1
            items.append(" ".join("".join(segments).split()))

    def finish_json_ld(self):
        if self._json_ld_text is None:
            return
        try:
            value = parse_json("".join(self._json_ld_text))
            json_type = {
                dict: "object",
                list: "array",
                str: "string",
                int: "number",
                float: "number",
                bool: "boolean",
                type(None): "null",
            }[type(value)]
            entry = {"parsed": True, "type": json_type}
        except (ValueError, RecursionError) as error:
            entry = {"parsed": False, "error": str(error)}
        self.json_ld.append(entry)
        self._json_ld_text = None

    def result(self, document_url):
        self.finish_text("title")
        self.finish_text("h1")
        self.finish_json_ld()
        href_base = resolve_href(document_url, self.base_href)
        try:
            effective_base = require_http_url(href_base, "base URL")
        except ValueError:
            effective_base = document_url

        return {
            "titles": self.titles,
            "h1": self.h1,
            "base_href": self.base_href,
            "canonical": [
                {"href": href, "resolved_url": resolve_href(effective_base, href)}
                for href in self.canonical
            ],
            "meta_robots": self.meta_robots,
            "json_ld": self.json_ld,
            "links": [
                dict(link, resolved_url=resolve_href(effective_base, link["href"]))
                for link in self.links
            ],
        }


def inspect_html(value, field, document_url):
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{field} must be an HTML string or null")
    parser = PageHTML()
    parser.feed(value)
    parser.close()
    return parser.result(document_url)


def inspect_http(value, field):
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError(f"{field} must be an object or null")
    status = value.get("status")
    if status is not None and (type(status) is not int or not 100 <= status <= 599):
        raise ValueError(f"{field}.status must be an integer from 100 to 599 or null")
    final_url = value.get("final_url")
    if final_url is not None:
        require_http_url(final_url, f"{field}.final_url")
    headers = value.get("headers")
    if headers is not None:
        if not isinstance(headers, dict) or not all(
            isinstance(item, str) for item in headers.values()
        ):
            raise ValueError(f"{field}.headers must be an object of strings or null")
        normalized = {key.lower(): item for key, item in headers.items()}
        if len(normalized) != len(headers):
            raise ValueError(f"{field}.headers contains case-insensitive duplicate names")
        headers = normalized
    return {"status": status, "final_url": final_url, "headers": headers}


def inspect_page(page, index):
    field = f"pages[{index}]"
    if not isinstance(page, dict):
        raise ValueError(f"{field} must be an object")
    url = require_http_url(page.get("url"), f"{field}.url")
    http = inspect_http(page.get("http"), f"{field}.http")
    document_url = (http["final_url"] if http else None) or url
    return {
        "url": url,
        "http": http,
        "source": inspect_html(page.get("html"), f"{field}.html", document_url),
        "rendered": inspect_html(
            page.get("rendered_html"), f"{field}.rendered_html", document_url
        ),
    }


def audit(manifest):
    version = manifest.get("schema_version") if isinstance(manifest, dict) else None
    if type(version) is not int or version != 1:
        raise ValueError("schema_version must be 1")
    pages = manifest.get("pages")
    if not isinstance(pages, list):
        raise ValueError("pages must be an array")
    return {"schema_version": 1, "pages": [
        inspect_page(page, index) for index, page in enumerate(pages)
    ]}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("input", type=Path, help="JSON manifest containing local captures")
    args = cli.parse_args()
    try:
        manifest = parse_json(args.input.read_text(encoding="utf-8-sig"))
        report = audit(manifest)
    except (OSError, ValueError, RecursionError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
