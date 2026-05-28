from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from harness_lab.chapter01 import validate_many


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_manifest(path: str | Path) -> dict[str, Any]:
    manifest_path = Path(path)
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("smoke manifest must be a JSON object")
    for field in ["id", "chapter", "agent_command", "expected_report"]:
        if field not in payload:
            raise ValueError(f"smoke manifest missing required field: {field}")
    if payload["chapter"] != "01":
        raise ValueError("this smoke wrapper currently supports Chapter 01 manifests")
    if not isinstance(payload["agent_command"], list) or not payload["agent_command"]:
        raise ValueError("agent_command must be a non-empty argv list")
    return payload


def _expand_arg(arg: str, *, repo_root: Path, workspace: Path, report_path: Path) -> str:
    return (
        arg.replace("{repo_root}", str(repo_root))
        .replace("{workspace}", str(workspace))
        .replace("{report_path}", str(report_path))
    )


def _write_workspace_files(workspace: Path, files: dict[str, str]) -> None:
    for relative, content in files.items():
        target = workspace / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


def run_smoke_manifest(path: str | Path, workspace_root: str | Path | None = None) -> dict[str, Any]:
    manifest_path = Path(path)
    manifest = _load_manifest(manifest_path)
    repo_root = REPO_ROOT

    root = Path(workspace_root) if workspace_root is not None else Path(tempfile.mkdtemp(prefix="harness-smoke-"))
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(prefix=f"{manifest['id']}-", dir=root))
    report_path = workspace / manifest["expected_report"]

    workspace_files = manifest.get("workspace_files", {})
    if workspace_files:
        if not isinstance(workspace_files, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in workspace_files.items()):
            raise ValueError("workspace_files must be an object mapping relative paths to text content")
        _write_workspace_files(workspace, workspace_files)

    command = [
        _expand_arg(str(part), repo_root=repo_root, workspace=workspace, report_path=report_path)
        for part in manifest["agent_command"]
    ]
    timeout = int(manifest.get("timeout_seconds", 30))
    env = os.environ.copy()
    env.update(
        {
            "HARNESS_SMOKE_REPO_ROOT": str(repo_root),
            "HARNESS_SMOKE_WORKSPACE": str(workspace),
            "HARNESS_SMOKE_REPORT_PATH": str(report_path),
            "HARNESS_SMOKE_SCENARIO_ID": str(manifest["id"]),
        }
    )

    try:
        completed = subprocess.run(
            command,
            cwd=workspace,
            env=env,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        agent_exit_code: int | None = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        agent_exit_code = None
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        timed_out = True

    validator = validate_many([report_path])
    ok = (not timed_out) and agent_exit_code == 0 and validator["failed"] == 0
    return {
        "scenario_id": manifest["id"],
        "chapter": manifest["chapter"],
        "ok": ok,
        "workspace": str(workspace),
        "report_path": str(report_path),
        "agent_command": command,
        "agent_exit_code": agent_exit_code,
        "agent_timed_out": timed_out,
        "stdout": stdout,
        "stderr": stderr,
        "validator": validator,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run sandboxed real-agent smoke scenarios.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run = subparsers.add_parser("run", help="Run a smoke manifest.")
    run.add_argument("manifest", help="Path to smoke manifest JSON.")
    run.add_argument("--workspace-root", help="Directory where isolated smoke workspaces are created.")
    run.add_argument("--summary-file", help="Write the JSON smoke summary to this path.")
    run.add_argument("--json", action="store_true", help="Print the JSON smoke summary.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command != "run":
        raise AssertionError(f"unexpected command: {args.command}")

    summary = run_smoke_manifest(args.manifest, workspace_root=args.workspace_root)
    if args.summary_file:
        summary_path = Path(args.summary_file)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        status = "PASS" if summary["ok"] else "FAIL"
        print(f"{status} {summary['scenario_id']}")
        print(f"workspace={summary['workspace']}")
        print(f"report={summary['report_path']}")
        print(f"agent_exit_code={summary['agent_exit_code']}")
        print(f"validator_passed={summary['validator']['passed']} validator_failed={summary['validator']['failed']}")

    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
