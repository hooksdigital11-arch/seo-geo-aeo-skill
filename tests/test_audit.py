import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


TESTS = Path(__file__).resolve().parent
SCRIPT = TESTS.parent / "skills" / "seo-geo-aeo" / "scripts" / "audit.py"
FIXTURE = TESTS / "fixtures" / "audit-input.json"


def run_cli(path):
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(path)],
        capture_output=True,
        encoding="utf-8",
        check=False,
        timeout=5,
    )


class AuditCLITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = run_cli(FIXTURE)
        if cls.result.returncode != 0:
            raise RuntimeError(cls.result.stderr)
        cls.report = json.loads(cls.result.stdout)

    def test_captured_http_and_raw_signals(self):
        self.assertEqual(self.report["schema_version"], 1)
        page = self.report["pages"][0]
        self.assertEqual(page["http"], {
            "status": 200,
            "final_url": "https://example.test/catalog/item",
            "headers": {"content-type": "text/html", "x-robots-tag": "noindex"},
        })
        source = page["source"]
        self.assertEqual(source["titles"], ["Sample & Catalogue"])
        self.assertEqual(source["h1"], ["Sample Item", "Specifications"])
        self.assertEqual(source["canonical"], [
            {"href": "../product", "resolved_url": "https://example.test/product"},
            {"href": None, "resolved_url": None},
        ])
        self.assertEqual(source["meta_robots"], [
            {"name": "robots", "content": "index,follow"},
            {"name": "googlebot-news", "content": "nosnippet"},
        ])
        self.assertEqual(source["json_ld"], [])
        self.assertEqual(source["links"], [
            {
                "href": "manual",
                "resolved_url": "https://example.test/catalog/manual",
                "rel": ["nofollow", "sponsored"],
            },
            {"href": "/locator", "resolved_url": "https://example.test/locator", "rel": []},
        ])

    def test_rendered_capture_stays_separate(self):
        rendered = self.report["pages"][0]["rendered"]
        self.assertEqual(rendered["titles"], ["Rendered item"])
        self.assertEqual(rendered["base_href"], "/docs/")
        self.assertEqual(rendered["canonical"], [])
        self.assertEqual(rendered["json_ld"][:2], [
            {"parsed": True, "type": "object"},
            {"parsed": True, "type": "array"},
        ])
        self.assertFalse(rendered["json_ld"][2]["parsed"])
        self.assertTrue(rendered["json_ld"][2]["error"])
        self.assertEqual(rendered["links"][0]["resolved_url"],
                         "https://example.test/docs/detail#part")

    def test_missing_is_distinct_from_empty(self):
        page = self.report["pages"][1]
        self.assertIsNone(page["http"])
        self.assertIsNone(page["rendered"])
        self.assertEqual(page["source"]["titles"], [])
        self.assertEqual(page["source"]["json_ld"], [])

    def test_malformed_href_and_unclosed_heading(self):
        page = self.report["pages"][2]
        self.assertEqual(page["http"], {"status": 503, "final_url": None, "headers": None})
        source = page["source"]
        self.assertEqual(source["canonical"], [{"href": "http://[bad", "resolved_url": None}])
        self.assertEqual(source["links"][0]["resolved_url"], "https://example.test/help")
        self.assertEqual(source["h1"], ["Still here"])

    def test_deterministic_output(self):
        again = run_cli(FIXTURE)
        self.assertEqual(again.returncode, 0)
        self.assertEqual(again.stdout, self.result.stdout)
        self.assertEqual(again.stderr, "")

    def test_input_errors_are_reported_on_stderr(self):
        cases = [
            ("{oops", "Expecting property name"),
            ('{"schema_version":1,"schema_version":1,"pages":[]}', "duplicate JSON key"),
            ('{"schema_version":true,"pages":[]}', "schema_version"),
            ('{"schema_version":1,"pages":{}}', "pages must be an array"),
            ('{"schema_version":1,"pages":[{"url":"file:///bad"}]}', "pages[0].url"),
            ('{"schema_version":1,"pages":[{"url":"https://example.test","html":[] }]}',
             "pages[0].html"),
            ('{"schema_version":1,"pages":[{"url":"https://example.test","http":{"status":true}}]}',
             "pages[0].http.status"),
        ]
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "input.json"
            for content, error in cases:
                with self.subTest(error=error):
                    path.write_text(content, encoding="utf-8")
                    result = run_cli(path)
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(result.stdout, "")
                    self.assertIn(error, json.loads(result.stderr)["error"])
            result = run_cli(path.with_name("absent.json"))
            self.assertEqual(result.returncode, 2)
            self.assertIn("absent.json", json.loads(result.stderr)["error"])


if __name__ == "__main__":
    unittest.main()
