#!/usr/bin/env bash
set -euo pipefail

if ! command -v copilot >/dev/null 2>&1; then
  echo "error: GitHub Copilot CLI 'copilot' was not found on PATH" >&2
  echo "Install github/copilot-cli and authenticate before running this live smoke." >&2
  exit 127
fi

: "${HARNESS_SMOKE_REPO_ROOT:?HARNESS_SMOKE_REPO_ROOT is required}"
: "${HARNESS_SMOKE_WORKSPACE:?HARNESS_SMOKE_WORKSPACE is required}"
: "${HARNESS_SMOKE_REPORT_PATH:?HARNESS_SMOKE_REPORT_PATH is required}"
: "${HARNESS_SMOKE_SCENARIO_ID:?HARNESS_SMOKE_SCENARIO_ID is required}"

cd "$HARNESS_SMOKE_WORKSPACE"

cat > copilot-smoke-prompt.md <<EOF
You are GitHub Copilot CLI running as the live real agent for a Chapter 01 smoke test.

Repository root:
$HARNESS_SMOKE_REPO_ROOT

Isolated workspace:
$HARNESS_SMOKE_WORKSPACE

Task:
1. Read AGENTS.md as the authoritative harness instructions before acting.
2. Read task.md.
3. Create concrete evidence in this workspace: definition-of-done-check.txt.
4. definition-of-done-check.txt must explicitly mention AGENTS.md and the definition of done.
5. Write a valid Chapter 01 JSON report to this exact path:
   $HARNESS_SMOKE_REPORT_PATH

Report requirements:
- task_id: $HARNESS_SMOKE_SCENARIO_ID
- chapter: 01
- claimed_status: completed
- artifact.kind: json-report
- artifact.path should point to a concrete workspace artifact such as definition-of-done-check.txt
- evidence must use external evidence types accepted by the validator, such as file, command, or validator
- do not use self_report evidence
- keep all side effects inside the isolated workspace

After writing the report, run this validation command yourself:
PYTHONPATH="$HARNESS_SMOKE_REPO_ROOT" python3 -m harness_lab.chapter01 validate "$HARNESS_SMOKE_REPORT_PATH" --json

If validation fails, fix the artifact/report and rerun validation until it passes.
EOF

# By default this reuses the user's normal Copilot login state. Set COPILOT_HOME
# before invoking the smoke runner if you want a dedicated live-smoke profile.
copilot \
  -p "$(cat copilot-smoke-prompt.md)" \
  -C "$HARNESS_SMOKE_WORKSPACE" \
  --allow-all-tools \
  --allow-all-paths \
  --no-ask-user \
  --no-auto-update \
  --no-remote \
  --stream off \
  --output-format json \
  --silent

PYTHONPATH="$HARNESS_SMOKE_REPO_ROOT" \
  python3 -m harness_lab.chapter01 validate "$HARNESS_SMOKE_REPORT_PATH" --json
