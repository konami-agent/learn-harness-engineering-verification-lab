import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "experiments" / "chapter-01" / "fixtures"


def run_validator(*paths: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "harness_lab.chapter01", "validate", *map(str, paths), "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class Chapter01FixturesAndCliTest(unittest.TestCase):
    def test_chapter01_fixtures_define_positive_and_negative_cases(self):
        positive = FIXTURES / "positive" / "report.json"
        missing_artifact = FIXTURES / "negative-missing-artifact" / "report.json"
        self_report_only = FIXTURES / "negative-self-report-only" / "report.json"
        placeholder = FIXTURES / "negative-placeholder-evidence" / "report.json"

        for path in [positive, missing_artifact, self_report_only, placeholder]:
            self.assertTrue(path.exists(), f"missing fixture: {path}")

        result = run_validator(positive, missing_artifact, self_report_only, placeholder)

        self.assertEqual(result.returncode, 1, result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["total"], 4)
        self.assertEqual(summary["passed"], 1)
        self.assertEqual(summary["failed"], 3)
        by_name = {Path(item["path"]).parent.name: item for item in summary["results"]}
        self.assertTrue(by_name["positive"]["ok"])
        self.assertFalse(by_name["negative-missing-artifact"]["ok"])
        self.assertIn("artifact.path does not exist", by_name["negative-missing-artifact"]["errors"])
        self.assertIn("evidence[0].type cannot be self_report", by_name["negative-self-report-only"]["errors"])
        self.assertIn("evidence[0].detail is placeholder text", by_name["negative-placeholder-evidence"]["errors"])

    def test_cli_writes_machine_readable_summary_file(self):
        positive = FIXTURES / "positive" / "report.json"
        with tempfile.TemporaryDirectory() as tmp:
            summary_path = Path(tmp) / "summary.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "harness_lab.chapter01",
                    "validate",
                    str(positive),
                    "--json",
                    "--summary-file",
                    str(summary_path),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertEqual(summary["total"], 1)
            self.assertEqual(summary["passed"], 1)
            self.assertEqual(summary["failed"], 0)


if __name__ == "__main__":
    unittest.main()
