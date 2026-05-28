import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from harness_lab.smoke import run_smoke_manifest


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "smoke" / "chapter-01" / "manifest.json"
BAD_MANIFEST = ROOT / "smoke" / "chapter-01" / "manifest-self-report-only.json"


class Chapter01RealAgentSmokeWrapperTest(unittest.TestCase):
    def test_manifest_defines_sandboxed_chapter01_smoke_scenario(self):
        self.assertTrue(MANIFEST.exists(), "missing Chapter 01 smoke manifest")
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

        self.assertEqual(manifest["id"], "chapter-01-real-agent-smoke")
        self.assertEqual(manifest["chapter"], "01")
        self.assertIn("agent_command", manifest)
        self.assertIn("expected_report", manifest)
        self.assertEqual(manifest["expected_report"], "report.json")
        self.assertTrue(manifest.get("sandbox", {}).get("isolate_workspace"))
        self.assertLessEqual(manifest.get("timeout_seconds", 999), 30)

    def test_runner_executes_agent_in_isolated_workspace_and_validates_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            summary = run_smoke_manifest(MANIFEST, workspace_root=Path(tmp))

            self.assertTrue(summary["ok"], summary)
            self.assertEqual(summary["scenario_id"], "chapter-01-real-agent-smoke")
            self.assertEqual(summary["agent_exit_code"], 0)
            self.assertEqual(summary["validator"]["total"], 1)
            self.assertEqual(summary["validator"]["passed"], 1)
            self.assertEqual(summary["validator"]["failed"], 0)
            self.assertIn("workspace", summary)
            self.assertIn("report_path", summary)
            self.assertTrue(Path(summary["workspace"]).exists())
            self.assertTrue(Path(summary["report_path"]).exists())

    def test_runner_rejects_agent_that_only_self_reports_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            summary = run_smoke_manifest(BAD_MANIFEST, workspace_root=Path(tmp))

        self.assertFalse(summary["ok"], summary)
        self.assertEqual(summary["agent_exit_code"], 0)
        self.assertEqual(summary["validator"]["failed"], 1)
        errors = summary["validator"]["results"][0]["errors"]
        self.assertIn("evidence[0].type cannot be self_report", errors)

    def test_cli_runs_manifest_and_writes_summary_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            summary_file = Path(tmp) / "summary.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "harness_lab.smoke",
                    "run",
                    str(MANIFEST),
                    "--workspace-root",
                    tmp,
                    "--summary-file",
                    str(summary_file),
                    "--json",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            summary = json.loads(summary_file.read_text(encoding="utf-8"))
            self.assertTrue(summary["ok"], summary)
            self.assertEqual(summary["validator"]["passed"], 1)

    def test_documentation_explains_wrapper_boundary_and_manual_command(self):
        doc = ROOT / "smoke" / "chapter-01" / "README.md"
        self.assertTrue(doc.exists(), "missing Chapter 01 smoke README")
        text = doc.read_text(encoding="utf-8")
        for phrase in [
            "real-agent smoke wrapper",
            "isolated workspace",
            "external agent command",
            "success is still decided by `harness_lab.chapter01`",
            "python3 -m harness_lab.smoke run smoke/chapter-01/manifest.json",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
