import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "skills/seo-geo-aeo/scripts/summarize_answers.py"
SAMPLE = ROOT / "examples/answers.json"


class AnswerSummaries(unittest.TestCase):
    def test_unknown_and_failed_are_separate(self):
        result = subprocess.check_output([sys.executable, str(CLI), str(SAMPLE)])
        group, = json.loads(result)["groups"]
        self.assertEqual((group["observed"], group["failed"], group["not_run"]), (2, 1, 1))
        self.assertEqual(group["mentioned"], {"yes":1, "scored":1, "unknown":1, "rate":1.0})
        self.assertEqual(group["cited"], {"yes":1, "scored":2, "unknown":0, "rate":0.5})

    def test_duplicate_run_is_rejected(self):
        document = json.loads(SAMPLE.read_text(encoding="utf-8"))
        document["runs"].append(document["runs"][0])
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "duplicate.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            process = subprocess.run([sys.executable, str(CLI), str(path)], capture_output=True)
        self.assertEqual(process.returncode, 2)
        self.assertIn(b"Duplicate run", process.stderr)
