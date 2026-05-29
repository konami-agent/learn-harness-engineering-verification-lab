import json
import os
from pathlib import Path


workspace = Path(os.environ["HARNESS_SMOKE_WORKSPACE"])
report_path = Path(os.environ["HARNESS_SMOKE_REPORT_PATH"])
agents_path = workspace / "AGENTS.md"
task_path = workspace / "task.md"
compliance_path = workspace / "definition-of-done-check.txt"

task_text = task_path.read_text(encoding="utf-8")

if agents_path.exists():
    agents_text = agents_path.read_text(encoding="utf-8")
    compliance_path.write_text(
        "Chapter 01 harness compliance evidence\n"
        "Read task.md and AGENTS.md before producing the report.\n"
        "AGENTS.md supplied the definition of done for this smoke run.\n"
        "The agent produced this concrete artifact so the validator does not need to trust self-report.\n\n"
        "Task excerpt:\n"
        f"{task_text.strip()}\n\n"
        "AGENTS.md excerpt:\n"
        f"{agents_text.strip()}\n",
        encoding="utf-8",
    )

    payload = {
        "task_id": os.environ.get("HARNESS_SMOKE_SCENARIO_ID", "chapter-01-real-agent-smoke"),
        "chapter": "01",
        "claimed_status": "completed",
        "artifact": {
            "kind": "json-report",
            "path": "definition-of-done-check.txt",
        },
        "evidence": [
            {
                "id": "evidence:file:definition-of-done-check",
                "type": "file",
                "detail": "definition-of-done-check.txt records that the agent followed AGENTS.md as the harness instruction layer.",
            },
            {
                "id": "evidence:file:agents-md",
                "type": "file",
                "detail": "AGENTS.md supplied the workspace definition of done before the report was accepted.",
            },
            {
                "id": "evidence:command:agent-executed",
                "type": "command",
                "detail": "The smoke wrapper executed an external agent command rather than accepting a static model message.",
            },
        ],
        "checks": [
            {
                "name": "agents-md-definition-of-done-followed",
                "status": "passed",
                "evidence_ref": "evidence:file:definition-of-done-check",
            },
            {
                "name": "external-artifact-present",
                "status": "passed",
                "evidence_ref": "evidence:file:definition-of-done-check",
            },
        ],
    }
else:
    payload = {
        "task_id": os.environ.get("HARNESS_SMOKE_SCENARIO_ID", "chapter-01-no-agents-control-smoke"),
        "chapter": "01",
        "claimed_status": "completed",
        "artifact": {
            "kind": "json-report",
            "path": "report.json",
        },
        "evidence": [
            {
                "id": "evidence:self-report",
                "type": "self_report",
                "detail": "No AGENTS.md instruction layer was present, so this control can only claim completion without harness-provided definition-of-done evidence.",
            }
        ],
        "checks": [
            {
                "name": "agent-said-done-without-agents-md",
                "status": "passed",
                "evidence_ref": "evidence:self-report",
            }
        ],
    }

report_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
print(f"wrote {report_path}")
