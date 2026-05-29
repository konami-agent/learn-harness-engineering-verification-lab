import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from harness_lab.smoke import run_smoke_manifest


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "chapters" / "chapter-01" / "smoke" / "deterministic" / "manifest-with-agents.json"
NO_AGENTS_MANIFEST = ROOT / "chapters" / "chapter-01" / "smoke" / "deterministic" / "manifest-no-agents.json"
BAD_MANIFEST = ROOT / "chapters" / "chapter-01" / "smoke" / "deterministic" / "manifest-self-report-only.json"
LIVE_COPILOT_MANIFEST = ROOT / "chapters" / "chapter-01" / "smoke" / "live" / "github-copilot-cli" / "manifest.json"
LIVE_COPILOT_ADAPTER = ROOT / "chapters" / "chapter-01" / "smoke" / "live" / "github-copilot-cli" / "run.sh"


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
        workspace_files = manifest.get("workspace_files", {})
        self.assertIn("AGENTS.md", workspace_files)
        self.assertIn("definition of done", workspace_files["AGENTS.md"])
        self.assertIn("AGENTS.md", workspace_files.get("task.md", ""))

    def test_runner_demonstrates_agents_md_as_harness_layer(self):
        with tempfile.TemporaryDirectory() as tmp:
            summary = run_smoke_manifest(MANIFEST, workspace_root=Path(tmp))

            self.assertTrue(summary["ok"], summary)
            workspace = Path(summary["workspace"])
            agents_file = workspace / "AGENTS.md"
            compliance_artifact = workspace / "definition-of-done-check.txt"
            report = json.loads(Path(summary["report_path"]).read_text(encoding="utf-8"))
            evidence_details = "\n".join(item["detail"] for item in report["evidence"])

            self.assertTrue(agents_file.exists())
            self.assertTrue(compliance_artifact.exists())
            self.assertIn("AGENTS.md", compliance_artifact.read_text(encoding="utf-8"))
            self.assertIn("definition of done", compliance_artifact.read_text(encoding="utf-8"))
            self.assertIn("AGENTS.md", evidence_details)
            self.assertIn("definition-of-done-check.txt", evidence_details)

    def test_runner_compares_agents_md_presence_against_no_agents_control(self):
        self.assertTrue(NO_AGENTS_MANIFEST.exists(), "missing no-AGENTS.md control manifest")
        with_agents_manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        no_agents_manifest = json.loads(NO_AGENTS_MANIFEST.read_text(encoding="utf-8"))

        self.assertEqual(no_agents_manifest["id"], "chapter-01-no-agents-control-smoke")
        self.assertNotIn("AGENTS.md", no_agents_manifest.get("workspace_files", {}))
        self.assertEqual(no_agents_manifest["agent_command"], with_agents_manifest["agent_command"])

        with tempfile.TemporaryDirectory() as tmp:
            summary = run_smoke_manifest(NO_AGENTS_MANIFEST, workspace_root=Path(tmp))

        self.assertFalse(summary["ok"], summary)
        self.assertEqual(summary["agent_exit_code"], 0)
        self.assertEqual(summary["validator"]["failed"], 1)
        errors = summary["validator"]["results"][0]["errors"]
        self.assertIn("evidence[0].type cannot be self_report", errors)

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
        doc = ROOT / "chapters" / "chapter-01" / "smoke" / "README.md"
        self.assertTrue(doc.exists(), "missing Chapter 01 smoke README")
        text = doc.read_text(encoding="utf-8")
        for phrase in [
            "real-agent smoke wrapper",
            "isolated workspace",
            "external agent command",
            "success is still decided by `harness_lab.validators.chapter01`",
            "python3 -m harness_lab.smoke run chapters/chapter-01/smoke/deterministic/manifest-with-agents.json",
            "GitHub Copilot CLI adapter",
            "live/github-copilot-cli/README.md",
            "AGENTS.md as the harness instruction layer",
            "presence/absence comparison",
            "manifest-no-agents.json",
            "definition-of-done-check.txt",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_live_github_copilot_cli_manifest_points_to_real_adapter(self):
        self.assertTrue(LIVE_COPILOT_MANIFEST.exists(), "missing live GitHub Copilot CLI manifest")
        manifest = json.loads(LIVE_COPILOT_MANIFEST.read_text(encoding="utf-8"))

        self.assertEqual(manifest["id"], "chapter-01-github-copilot-cli-smoke")
        self.assertEqual(manifest["chapter"], "01")
        self.assertGreaterEqual(manifest.get("timeout_seconds", 0), 300)
        self.assertTrue(manifest.get("sandbox", {}).get("isolate_workspace"))
        self.assertEqual(manifest["expected_report"], "report.json")
        self.assertEqual(
            manifest["agent_command"],
            ["bash", "{repo_root}/chapters/chapter-01/smoke/live/github-copilot-cli/run.sh"],
        )
        workspace_files = manifest.get("workspace_files", {})
        self.assertIn("AGENTS.md", workspace_files)
        self.assertIn("definition of done", workspace_files["AGENTS.md"])
        self.assertIn("task.md", workspace_files)
        self.assertIn("AGENTS.md", workspace_files["task.md"])

    def test_live_github_copilot_cli_adapter_really_invokes_copilot(self):
        self.assertTrue(LIVE_COPILOT_ADAPTER.exists(), "missing live GitHub Copilot CLI adapter")
        text = LIVE_COPILOT_ADAPTER.read_text(encoding="utf-8")
        for phrase in [
            "#!/usr/bin/env bash",
            "set -euo pipefail",
            "command -v copilot",
            "copilot \\",
            "-p \"$(cat copilot-smoke-prompt.md)\"",
            "--allow-all-tools",
            "--allow-all-paths",
            "--no-ask-user",
            "--output-format json",
            "--silent",
            "HARNESS_SMOKE_WORKSPACE",
            "HARNESS_SMOKE_REPORT_PATH",
            "HARNESS_SMOKE_SCENARIO_ID",
            "AGENTS.md",
            "task.md",
            "definition-of-done-check.txt",
            "python3 -m harness_lab.validators.chapter01 validate",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_readme_distinguishes_deterministic_fixtures_from_live_copilot(self):
        doc = ROOT / "chapters" / "chapter-01" / "smoke" / "README.md"
        text = doc.read_text(encoding="utf-8")
        for phrase in [
            "deterministic Python adapters",
            "do not invoke GitHub Copilot CLI",
            "live GitHub Copilot CLI smoke",
            "live/github-copilot-cli/manifest.json",
            "live/github-copilot-cli/run.sh",
            "requires Copilot authentication",
            "not a mandatory CI path",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_github_copilot_cli_smoke_agent_guide_is_complete(self):
        doc = ROOT / "chapters" / "chapter-01" / "smoke" / "live" / "github-copilot-cli" / "README.md"
        self.assertTrue(doc.exists(), "missing GitHub Copilot CLI smoke agent guide")
        text = doc.read_text(encoding="utf-8")
        required_phrases = [
            "GitHub Copilot CLI adapter",
            "https://github.com/github/copilot-cli",
            "curl -fsSL https://gh.io/copilot-install | bash",
            "npm install -g @github/copilot",
            "copilot --help",
            "copilot -p",
            "non-interactive mode",
            "--allow-all-tools",
            "--allow-all-paths",
            "--no-ask-user",
            "--output-format json",
            "--silent",
            "COPILOT_HOME",
            "/login",
            "COPILOT_GITHUB_TOKEN, GH_TOKEN, GITHUB_TOKEN",
            "active Copilot subscription",
            "HARNESS_SMOKE_WORKSPACE",
            "HARNESS_SMOKE_REPORT_PATH",
            "HARNESS_SMOKE_SCENARIO_ID",
            "live/github-copilot-cli/run.sh",
            "report.json",
            "python3 -m harness_lab.validators.chapter01 validate",
            "python3 -m harness_lab.smoke run chapters/chapter-01/smoke/live/github-copilot-cli/manifest.json",
            "do not use self_report evidence",
            "fallback path",
            "AGENTS.md as the authoritative harness instructions",
            "definition-of-done-check.txt",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
