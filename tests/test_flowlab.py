from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from flowlab.discovery import discover
from flowlab.metrics import compute_metrics
from flowlab.normalize import normalize

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "sample-auditctl.ndjson"
MAPPING = ROOT / "config" / "auditctl-map.example.json"
GATES = ROOT / "config" / "gates.default.json"


class FlowLabTests(unittest.TestCase):
    def test_discovery_is_safe_by_default(self) -> None:
        result = discover(FIXTURE)
        self.assertEqual(result["input"]["records"], 17)
        self.assertFalse(result["profile_safety"]["includes_raw_value_samples"])
        self.assertFalse(any(item["samples"] for item in result["fields"].values()))

    def test_normalize_and_measure(self) -> None:
        mapping = json.loads(MAPPING.read_text(encoding="utf-8"))
        gates = json.loads(GATES.read_text(encoding="utf-8"))
        events, errors = normalize(FIXTURE, mapping)
        self.assertEqual(errors, [])
        self.assertEqual(len(events), 17)
        self.assertEqual(sum(event["event"] == "edit.meaningful" for event in events), 3)

        report = compute_metrics(events, gates)
        self.assertEqual(report["summary"]["sessions"], 3)
        self.assertEqual(report["summary"]["resolved_blockers"], 2)
        self.assertAlmostEqual(report["orientation"]["fraction"]["median"], 1 / 6, places=5)
        self.assertAlmostEqual(
            report["blockers"]["classified_seconds"]["exogenous_share_of_classified"],
            0.5,
            places=5,
        )
        self.assertEqual(report["decision_signals"]["context_warming"]["outcome"], "UNMEASURABLE")

    def test_bad_timestamp_is_reported_not_crashed(self) -> None:
        mapping = json.loads(MAPPING.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "bad.ndjson"
            path.write_text('{"ts":"not-a-time","type":"session.started","session_id":"s"}\n', encoding="utf-8")
            events, errors = normalize(path, mapping)
            self.assertEqual(events, [])
            self.assertEqual(len(errors), 1)


if __name__ == "__main__":
    unittest.main()
