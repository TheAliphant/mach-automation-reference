import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_FILES = [ROOT / "sidecar.py", ROOT / "lab" / "runner.py", ROOT / "lab" / "analyze.py"]

FORBIDDEN_RUNTIME_TOKENS = [
    "import requests",
    "from requests",
    "import httpx",
    "import aiohttp",
    "urllib.request",
    "import socket",
    "import subprocess",
    "mach.gallery",
]


class IsolationTests(unittest.TestCase):
    def test_runtime_has_no_outbound_network_or_prod_hostname(self):
        for path in RUNTIME_FILES:
            text = path.read_text(encoding="utf-8").lower()
            for token in FORBIDDEN_RUNTIME_TOKENS:
                self.assertNotIn(token.lower(), text, f"{token} found in {path}")

    def test_catalog_is_lab_only(self):
        catalog = json.loads((ROOT / "capabilities.snapshot.json").read_text())
        self.assertEqual(catalog["mode"], "lab_only")
        self.assertIs(catalog["production_connected"], False)
        for cap in catalog["capabilities"]:
            self.assertTrue(cap["id"].startswith("lab.mock."))
            self.assertEqual(cap["status"], "lab_only")

    def test_execute_is_hard_disabled(self):
        text = (ROOT / "sidecar.py").read_text(encoding="utf-8")
        self.assertIn('"production_execution_disabled"', text)
        self.assertIn("PRODUCTION_CONNECTED = False", text)


if __name__ == "__main__":
    unittest.main()
