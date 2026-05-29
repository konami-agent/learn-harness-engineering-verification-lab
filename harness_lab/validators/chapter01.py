from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PLACEHOLDER_TEXT = {"", "todo", "tbd", "n/a", "na", "placeholder", "lorem", "..."}
ALLOWED_EVIDENCE_TYPES = {"file", "command", "validator"}
REQUIRED_FIELDS = ["task_id", "chapter", "claimed_status", "artifact", "evidence", "checks"]


@dataclass(frozen=True)
class ValidationResult:
    path: str
    ok: bool
    errors: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {"path": self.path, "ok": self.ok, "errors": self.errors}


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_placeholder(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    return value.strip().lower() in PLACEHOLDER_TEXT


def _artifact_path_exists(report_path: Path, artifact_path: str) -> bool:
    candidate = Path(artifact_path)
    if candidate.is_absolute():
        return candidate.exists()
    repo_relative = Path.cwd() / candidate
    report_relative = report_path.parent / candidate
    return repo_relative.exists() or report_relative.exists()


def validate_report(path: str | Path) -> ValidationResult:
    report_path = Path(path)
    errors: list[str] = []

    if not report_path.exists():
        return ValidationResult(str(report_path), False, ["report file does not exist"])

    try:
        payload = json.loads(report_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return ValidationResult(str(report_path), False, [f"invalid json: {exc.msg}"])

    if not isinstance(payload, dict):
        return ValidationResult(str(report_path), False, ["report must be a JSON object"])

    for field in REQUIRED_FIELDS:
        if field not in payload:
            errors.append(f"missing required field: {field}")

    if payload.get("chapter") != "01":
        errors.append("chapter must be '01'")
    if payload.get("claimed_status") != "completed":
        errors.append("claimed_status must be 'completed'")
    if not _is_nonempty_string(payload.get("task_id")):
        errors.append("task_id must be a non-empty string")

    artifact = payload.get("artifact")
    if isinstance(artifact, dict):
        if artifact.get("kind") != "json-report":
            errors.append("artifact.kind must be 'json-report'")
        artifact_path = artifact.get("path")
        if not _is_nonempty_string(artifact_path):
            errors.append("artifact.path must be a non-empty string")
        else:
            assert isinstance(artifact_path, str)
            if not _artifact_path_exists(report_path, artifact_path):
                errors.append("artifact.path does not exist")
    elif "artifact" in payload:
        errors.append("artifact must be an object")

    evidence = payload.get("evidence")
    evidence_ids: set[str] = set()
    if isinstance(evidence, list):
        if not evidence:
            errors.append("evidence must contain at least one item")
        for index, item in enumerate(evidence):
            if not isinstance(item, dict):
                errors.append(f"evidence[{index}] must be an object")
                continue
            evidence_id = item.get("id")
            evidence_type = item.get("type")
            detail = item.get("detail")
            if not _is_nonempty_string(evidence_id):
                errors.append(f"evidence[{index}].id must be a non-empty string")
            else:
                assert isinstance(evidence_id, str)
                evidence_ids.add(evidence_id)
            if evidence_type == "self_report":
                errors.append(f"evidence[{index}].type cannot be self_report")
            elif evidence_type not in ALLOWED_EVIDENCE_TYPES:
                errors.append(f"evidence[{index}].type must be one of: command, file, validator")
            if not _is_nonempty_string(detail):
                errors.append(f"evidence[{index}].detail must be a non-empty string")
            elif _is_placeholder(detail):
                errors.append(f"evidence[{index}].detail is placeholder text")
    elif "evidence" in payload:
        errors.append("evidence must be a list")

    checks = payload.get("checks")
    if isinstance(checks, list):
        if not checks:
            errors.append("checks must contain at least one item")
        for index, item in enumerate(checks):
            if not isinstance(item, dict):
                errors.append(f"checks[{index}] must be an object")
                continue
            if not _is_nonempty_string(item.get("name")):
                errors.append(f"checks[{index}].name must be a non-empty string")
            if item.get("status") != "passed":
                errors.append(f"checks[{index}].status must be 'passed'")
            evidence_ref = item.get("evidence_ref")
            if not _is_nonempty_string(evidence_ref):
                errors.append(f"checks[{index}].evidence_ref must be a non-empty string")
            elif evidence_ref not in evidence_ids:
                errors.append(f"checks[{index}].evidence_ref does not reference evidence")
    elif "checks" in payload:
        errors.append("checks must be a list")

    return ValidationResult(str(report_path), not errors, errors)


def validate_many(paths: list[str | Path]) -> dict[str, Any]:
    results = [validate_report(path) for path in paths]
    passed = sum(1 for result in results if result.ok)
    failed = len(results) - passed
    return {
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "results": [result.to_dict() for result in results],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate Chapter 01 report artifacts.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate", help="Validate one or more report JSON files.")
    validate.add_argument("reports", nargs="+", help="Report JSON file paths.")
    validate.add_argument("--json", action="store_true", help="Emit machine-readable JSON summary.")
    validate.add_argument("--summary-file", help="Write the JSON summary to this path.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command != "validate":
        raise AssertionError(f"unexpected command: {args.command}")

    summary = validate_many(args.reports)
    if args.summary_file:
        summary_path = Path(args.summary_file)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        for item in summary["results"]:
            status = "PASS" if item["ok"] else "FAIL"
            print(f"{status} {item['path']}")
            for error in item["errors"]:
                print(f"  - {error}")
        print(f"total={summary['total']} passed={summary['passed']} failed={summary['failed']}")

    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
