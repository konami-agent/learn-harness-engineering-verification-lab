import json
import os
from pathlib import Path


report_path = Path(os.environ["HARNESS_SMOKE_REPORT_PATH"])
payload = {
    "task_id": os.environ.get("HARNESS_SMOKE_SCENARIO_ID", "chapter-01-self-report-only-smoke"),
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
            "detail": "The agent said it completed the task.",
        }
    ],
    "checks": [
        {
            "name": "agent-said-done",
            "status": "passed",
            "evidence_ref": "evidence:self-report",
        }
    ],
}
report_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
print(f"wrote self-report-only {report_path}")
