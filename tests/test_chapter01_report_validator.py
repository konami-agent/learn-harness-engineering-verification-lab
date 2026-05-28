import json
import unittest
from pathlib import Path

from harness_lab.chapter01 import validate_report


def write_report(tmp_path: Path, payload: object) -> Path:
    path = tmp_path / "report.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def valid_payload() -> dict:
    return {
        "task_id": "chapter-01-positive-case",
        "chapter": "01",
        "claimed_status": "completed",
        "artifact": {
            "kind": "json-report",
            "path": "experiments/chapter-01/fixtures/positive/report.json",
        },
        "evidence": [
            {
                "id": "evidence:file:report",
                "type": "file",
                "detail": "The report artifact exists and was parsed by the deterministic validator.",
            },
            {
                "id": "evidence:validator:chapter01",
                "type": "validator",
                "detail": "validate_report returned a passing result for the positive fixture.",
            },
        ],
        "checks": [
            {
                "name": "artifact-contract",
                "status": "passed",
                "evidence_ref": "evidence:validator:chapter01",
            }
        ],
    }


class Chapter01ReportValidatorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(self._testMethodName)
        self.tmp.mkdir(exist_ok=True)

    def tearDown(self) -> None:
        for child in self.tmp.glob("*"):
            child.unlink()
        self.tmp.rmdir()

    def test_accepts_report_with_external_evidence(self):
        result = validate_report(write_report(self.tmp, valid_payload()))

        self.assertTrue(result.ok)
        self.assertEqual(result.errors, [])

    def test_rejects_reports_that_depend_on_self_report_or_weak_evidence(self):
        cases = [
            (lambda p: p.pop("evidence"), "missing required field: evidence"),
            (lambda p: p.update({"claimed_status": "done"}), "claimed_status must be 'completed'"),
            (lambda p: p["evidence"][0].update({"detail": "TODO"}), "evidence[0].detail is placeholder text"),
            (lambda p: p["evidence"][0].update({"type": "self_report"}), "evidence[0].type cannot be self_report"),
            (lambda p: p["checks"][0].update({"status": "skipped"}), "checks[0].status must be 'passed'"),
            (lambda p: p["checks"][0].update({"evidence_ref": "missing"}), "checks[0].evidence_ref does not reference evidence"),
        ]
        for mutation, expected_error in cases:
            with self.subTest(expected_error=expected_error):
                payload = valid_payload()
                mutation(payload)

                result = validate_report(write_report(self.tmp, payload))

                self.assertFalse(result.ok)
                self.assertIn(expected_error, result.errors)

    def test_rejects_missing_report_file(self):
        result = validate_report(self.tmp / "missing.json")

        self.assertFalse(result.ok)
        self.assertIn("report file does not exist", result.errors)

    def test_rejects_malformed_json(self):
        path = self.tmp / "report.json"
        path.write_text("{not json", encoding="utf-8")

        result = validate_report(path)

        self.assertFalse(result.ok)
        self.assertTrue(any(error.startswith("invalid json:") for error in result.errors))


if __name__ == "__main__":
    unittest.main()
