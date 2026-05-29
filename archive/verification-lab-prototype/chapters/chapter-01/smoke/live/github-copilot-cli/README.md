# GitHub Copilot CLI adapter for Chapter 01 smoke

This guide explains how to use the standalone GitHub Copilot CLI from https://github.com/github/copilot-cli as the real agent behind the Chapter 01 smoke wrapper.

Important: this guide is about the `copilot` command from `github/copilot-cli`, not the older GitHub CLI extension invoked as `gh copilot`.

## Investigation notes

This guide was rebuilt against upstream release `v1.0.54` by checking:

- `github/copilot-cli` README and changelog;
- the latest release assets;
- `copilot --help` from the `copilot-linux-arm64.tar.gz` release binary;
- `copilot help permissions`;
- `copilot help environment`.

The key correction is that GitHub Copilot CLI does support non-interactive execution:

```bash
copilot -p "Fix the bug in main.js" --allow-all-tools
```

The CLI help describes `-p, --prompt <text>` as: `Execute a prompt in non-interactive mode (exits after completion)`.

It also states that `--allow-all-tools` allows tools to run automatically without confirmation and is required for non-interactive mode. For a smoke adapter this matters because the harness cannot answer approval prompts.

## Prerequisites

You need:

- Linux, macOS, or Windows;
- an active Copilot subscription;
- access not disabled by your organization or enterprise policy;
- the standalone `copilot` command from `github/copilot-cli`.

Install options from the upstream README include:

```bash
curl -fsSL https://gh.io/copilot-install | bash
```

or:

```bash
wget -qO- https://gh.io/copilot-install | bash
```

or npm:

```bash
npm install -g @github/copilot
```

or Homebrew:

```bash
brew install copilot-cli
```

Verify the installed command and version:

```bash
command -v copilot
copilot --version
copilot --help
copilot help permissions
copilot help environment
```

Authenticate once interactively:

```bash
copilot
```

If you are not logged in, use the `/login` slash command inside the Copilot CLI and follow the browser flow.

For headless/scripted environments, upstream documents token authentication through:

```text
COPILOT_GITHUB_TOKEN, GH_TOKEN, GITHUB_TOKEN
```

`COPILOT_GITHUB_TOKEN` has the highest precedence. A fine-grained PAT must include the Copilot Requests permission. Do not commit tokens to this repository or write them into smoke summaries.

Useful environment isolation option:

```text
COPILOT_HOME
```

Set `COPILOT_HOME` to a dedicated directory when you want smoke runs to avoid reusing your normal `~/.copilot` state.

## Smoke contract

The smoke runner sets these environment variables for the agent command:

```bash
HARNESS_SMOKE_REPO_ROOT      # repository root
HARNESS_SMOKE_WORKSPACE      # isolated workspace for this smoke run
HARNESS_SMOKE_REPORT_PATH    # exact path the agent must write
HARNESS_SMOKE_SCENARIO_ID    # manifest id
```

The Copilot-driven agent must write a JSON report to `$HARNESS_SMOKE_REPORT_PATH`. The report must satisfy the Chapter 01 validator and must not use self-report as evidence.

Minimum report shape:

```json
{
  "task_id": "chapter-01-github-copilot-cli-smoke",
  "chapter": "01",
  "claimed_status": "completed",
  "artifact": {
    "kind": "json-report",
    "path": "definition-of-done-check.txt"
  },
  "evidence": [
    {
      "id": "evidence:file:definition-of-done-check",
      "type": "file",
      "detail": "GitHub Copilot CLI created definition-of-done-check.txt after following AGENTS.md as the authoritative harness instructions."
    }
  ],
  "checks": [
    {
      "name": "external-artifact-present",
      "status": "passed",
      "evidence_ref": "evidence:file:definition-of-done-check"
    }
  ]
}
```

Do not use self_report evidence. The validator rejects evidence such as:

```json
{"type": "self_report", "detail": "Copilot said the task is complete."}
```

## Recommended integration shape

Keep two layers separate:

1. Stable harness smoke, committed and CI-safe: `chapters/chapter-01/smoke/deterministic/manifest-with-agents.json` uses deterministic Python adapters.
2. Live Copilot smoke: `chapters/chapter-01/smoke/live/github-copilot-cli/manifest.json` uses the real `copilot -p` non-interactive agent.

This avoids making every test run depend on subscription state, quota, login state, model availability, and network availability.

## Live non-interactive manifest

The committed live manifest is `chapters/chapter-01/smoke/live/github-copilot-cli/manifest.json`:

```json
{
  "id": "chapter-01-github-copilot-cli-smoke",
  "chapter": "01",
  "description": "Run github/copilot-cli in non-interactive mode and validate the produced Chapter 01 report externally.",
  "timeout_seconds": 900,
  "sandbox": {
    "isolate_workspace": true
  },
  "expected_report": "report.json",
  "workspace_files": {
    "AGENTS.md": "# Chapter 01 smoke harness instructions\n\nUse AGENTS.md as the authoritative harness instructions.\n\nDefinition of done:\n- Read task.md before acting.\n- Create definition-of-done-check.txt.\n- The artifact must explicitly mention AGENTS.md and the definition of done.\n- Write report.json to HARNESS_SMOKE_REPORT_PATH.\n- Do not use self_report evidence.\n",
    "task.md": "Use AGENTS.md as the authoritative harness instructions. Demonstrate Chapter 01 by creating definition-of-done-check.txt and a report.json that references concrete file evidence, not self_report evidence."
  },
  "agent_command": [
    "bash",
    "{repo_root}/chapters/chapter-01/smoke/live/github-copilot-cli/run.sh"
  ]
}
```

## Non-interactive adapter

The committed live adapter is `chapters/chapter-01/smoke/live/github-copilot-cli/run.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

cd "$HARNESS_SMOKE_WORKSPACE"

cat > copilot-smoke-prompt.md <<EOF
You are GitHub Copilot CLI running as the real agent for a Chapter 01 smoke test.

Repository root:
$HARNESS_SMOKE_REPO_ROOT

Isolated workspace:
$HARNESS_SMOKE_WORKSPACE

Task:
1. Read AGENTS.md as the authoritative harness instructions.
2. Read task.md.
3. Create concrete evidence in this workspace: definition-of-done-check.txt.
4. definition-of-done-check.txt must explicitly mention AGENTS.md and the definition of done.
5. Write a valid Chapter 01 JSON report to this exact path:
   $HARNESS_SMOKE_REPORT_PATH

Report requirements:
- task_id: $HARNESS_SMOKE_SCENARIO_ID
- chapter: 01
- claimed_status: completed
- artifact.path should point to a concrete workspace artifact such as definition-of-done-check.txt
- evidence must be file, command, validator, or similarly external evidence
- do not use self_report evidence
- keep all side effects inside the isolated workspace

After writing the report, run this validation command yourself:
PYTHONPATH="$HARNESS_SMOKE_REPO_ROOT" python3 -m harness_lab.validators.chapter01 validate "$HARNESS_SMOKE_REPORT_PATH" --json

If validation fails, fix the artifact/report and rerun validation until it passes.
EOF

# Optional but recommended for repeatable smoke runs: keep Copilot state separate
# from your normal interactive ~/.copilot state. Remove this if you explicitly
# want to reuse the logged-in default profile.
export COPILOT_HOME="${COPILOT_HOME:-$HARNESS_SMOKE_WORKSPACE/.copilot-home}"

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
  python3 -m harness_lab.validators.chapter01 validate "$HARNESS_SMOKE_REPORT_PATH" --json
```

Make it executable:

```bash
chmod +x chapters/chapter-01/smoke/live/github-copilot-cli/run.sh
```

Run the live smoke:

```bash
python3 -m harness_lab.smoke run chapters/chapter-01/smoke/live/github-copilot-cli/manifest.json \
  --summary-file reports/chapter-01-github-copilot-cli-smoke-summary.json \
  --json
```

Expected passing summary:

- wrapper exit code `0`;
- `ok: true`;
- `agent_exit_code: 0`;
- `validator.passed: 1`;
- `validator.failed: 0`.

If Copilot says it is done but the validator fails, the smoke fails. Fix the artifact or report; do not override the validator.

## Permission choices

The upstream help says `--allow-all-tools` is required for non-interactive mode. Without it, Copilot may need confirmation and the smoke run cannot continue.

This guide also uses:

```bash
--allow-all-paths
```

Reason: the prompt includes absolute paths such as `$HARNESS_SMOKE_REPORT_PATH` and `$HARNESS_SMOKE_REPO_ROOT`. You may remove this flag if you rewrite the adapter so Copilot only touches files under the current workspace and never reads the repo root.

Additional safety flags:

```bash
--no-ask-user
--no-auto-update
--no-remote
--stream off
--output-format json
--silent
```

- `--no-ask-user`: prevents the agent from trying to ask a human during a smoke run.
- `--no-auto-update`: avoids changing the CLI version during a smoke run.
- `--no-remote`: avoids remote session control during smoke.
- `--stream off`: makes output easier to capture.
- `--output-format json`: emits JSONL events for machine inspection.
- `--silent`: keeps scripting output smaller.

For stricter local runs, add deny rules after `--allow-all-tools`. Deny rules take precedence over allow rules according to `copilot help permissions`:

```bash
--deny-tool='shell(git push)' \
--deny-tool='shell(gh pr create)' \
--deny-tool='shell(gh pr merge)'
```

Do not use `--allow-all` or `--yolo` unless you intentionally want all tools, all paths, and all URLs approved.

## Authentication for unattended runs

For a real unattended smoke, prefer a token injected by the environment rather than storing credentials in the repo:

```bash
export COPILOT_GITHUB_TOKEN='[REDACTED]'
```

or:

```bash
export GH_TOKEN='[REDACTED]'
```

or:

```bash
export GITHUB_TOKEN='[REDACTED]'
```

Never commit token values. In docs and test fixtures, use `[REDACTED]`.

If you use a dedicated `COPILOT_HOME`, remember that it may not contain your previous browser login. In that case, token-based auth is the cleaner path.

## Validation commands

Validate the report directly:

```bash
PYTHONPATH="$HARNESS_SMOKE_REPO_ROOT" \
  python3 -m harness_lab.validators.chapter01 validate "$HARNESS_SMOKE_REPORT_PATH" --json
```

Run the full smoke wrapper:

```bash
python3 -m harness_lab.smoke run chapters/chapter-01/smoke/live/github-copilot-cli/manifest.json --json
```

Run the stable deterministic fallback path:

```bash
python3 -m harness_lab.smoke run chapters/chapter-01/smoke/deterministic/manifest-with-agents.json --json
```

## Failure triage

Use the JSON summary from the smoke runner:

- `agent_exit_code != 0`: the Copilot adapter failed before validation.
- `agent_timed_out: true`: Copilot exceeded the smoke timeout or waited on a permission/authentication issue.
- `validator.failed > 0`: Copilot wrote a report, but the report did not satisfy the Chapter 01 contract.
- validator error includes `evidence[0].type cannot be self_report`: Copilot produced only a claim of completion; ask it to create concrete file or validator evidence.
- report file is missing: Copilot did not write `$HARNESS_SMOKE_REPORT_PATH` exactly.
- output includes authentication failure: run `/login` interactively or provide `COPILOT_GITHUB_TOKEN`, `GH_TOKEN`, or `GITHUB_TOKEN` with Copilot Requests permission.

## Fallback path

When GitHub Copilot CLI is unavailable, unauthenticated, quota-limited, or impractical in the current environment, keep the committed deterministic smoke manifest as the stable fallback path:

```bash
python3 -m harness_lab.smoke run chapters/chapter-01/smoke/deterministic/manifest-with-agents.json --json
```

That fallback path proves the harness runner and validator still work. It does not prove live Copilot integration.

## Why this is useful

This integration tests the important engineering property: a real terminal coding agent can operate in a sandbox, create artifacts, and be judged by an external deterministic validator.

The smoke harness therefore measures the agent loop around artifacts, not the agent's confidence or final prose.
