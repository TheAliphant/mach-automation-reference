import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import sidecar


class LogicTests(unittest.TestCase):
    def test_discover_json(self):
        results = sidecar.discover("normalize json stable structure")
        self.assertTrue(results)
        self.assertEqual(results[0]["id"], "lab.mock.json-normalize")

    def test_unknown_live_chain_request_does_not_fake_capability(self):
        results = sidecar.discover("query live blockchain rpc token balance")
        ids = {r["id"] for r in results}
        self.assertNotIn("lab.mock.wallet-format", ids)

    def test_quote_is_lab_only(self):
        result = sidecar.quote("lab.mock.json-normalize")
        self.assertTrue(result["found"])
        self.assertEqual(result["mode"], "lab_only")
        self.assertIs(result["production_connected"], False)

    def test_json_probe_is_deterministic(self):
        a = sidecar.probe_payload("lab.mock.json-normalize", {"value":{"z":1,"a":2}})
        b = sidecar.probe_payload("lab.mock.json-normalize", {"value":{"a":2,"z":1}})
        self.assertEqual(a["result"], b["result"])

    def test_non_lab_capability_rejected(self):
        result = sidecar.probe_payload("production.real", {})
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"], "only_lab_mock_capabilities_allowed")


if __name__ == "__main__":
    unittest.main()
