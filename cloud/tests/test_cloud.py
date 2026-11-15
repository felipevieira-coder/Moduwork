import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from worker import RuntimeState, bounded_int, missing_config


class CloudTests(unittest.TestCase):
    def test_bounded_limits(self):
        with patch.dict(os.environ, {"MODU_MAX_ROWS": "9999"}):
            self.assertEqual(bounded_int("MODU_MAX_ROWS", 10, 1, 100), 100)
        with patch.dict(os.environ, {"MODU_MAX_ROWS": "abc"}):
            self.assertEqual(bounded_int("MODU_MAX_ROWS", 10, 1, 100), 10)

    def test_start_paused_without_secrets(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertIn("OPENAI_API_KEY", missing_config())
            self.assertIn("MODU_SPREADSHEET_ID", missing_config())

    def test_status_durable_and_aggregate(self):
        with tempfile.TemporaryDirectory() as d:
            a = RuntimeState(d)
            a.update(state="idle", cycles=3, last_batch={"processed": 2})
            b = RuntimeState(d)
            self.assertEqual(b.snapshot()["cycles"], 3)
            self.assertEqual(b.snapshot()["last_batch"]["processed"], 2)
            self.assertNotIn("company", json.dumps(b.snapshot()).lower())

    def test_dashboard_contains_protected_api(self):
        html = Path(__file__).resolve().parents[1].joinpath("dashboard.html").read_text()
        self.assertIn("Authorization", html)
        self.assertIn("/api/status", html)
        self.assertIn("20000", html)


if __name__ == "__main__":
    unittest.main()
