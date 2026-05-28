# GitHub Copilot CLI adapter for Chapter 01 smoke

This guide explains how to use the standalone GitHub Copilot CLI from https://github.com/github/copilot-cli as the real agent behind the Chapter 01 smoke wrapper.

Important correction: this guide is about the `copilot` command from `github/copilot-cli`, not the older GitHub CLI extension invoked as `gh copilot`.

The smoke boundary is unchanged: GitHub Copilot CLI runs as the real agent and may edit files, run commands, and produce artifacts, but the smoke run only passes when `harness_lab.chapter01` validates the resulting `report.json`. The agent's final answer is never enough.

## What this CLI is

According to the upstream project, GitHub Copilot CLI brings the Copilot coding agent directly to the terminal. It is an agentic terminal application: it can plan, inspect a repository, propose actions, and execute work locally with user approval. It is therefore a better fit for real-agent smoke testing than the old `gh copilot suggest` shell-command helper.

However, it is still an interactive terminal program. For smoke integration, assume an interactive TTY unless a later version documents a stable non-interactive mode. The smoke wrapper currently uses `subprocess.run` without a PTY, so fully unattended execution may require either:

- running the adapter manually in a terminal/tmux session, or
- extending `harness_lab.smoke` to support PTY-backed agent commands.

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

Verify the installed command:

```bash
command -v copilot
copilot --help
```

Launch it once and authenticate:

```bash
copilot
```

If you are not logged in, use the `/login` slash command inside the Copilot CLI and follow the browser flow.

For headless or scripted environments, upstream also documents PAT authentication through `GH_TOKEN or GITHUB_TOKEN`, using a fine-grained token with the Copilot Requests permission enabled. Do not commit tokens to this repository.

Optional experimental mode:

```bash
copilot --experimental
```

Experimental mode enables features that may change. One relevant feature is Autopilot mode, which encourages the agent to continue working until the task is complete. Because behavior can change, use it for local live smoke runs first, not as a required CI path.

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
    "path": "evidence.txt"
  },
  "evidence": [
    {
      "id": "evidence:file:evidence-txt",
      "type": "file",
      "detail": "GitHub Copilot CLI created evidence.txt in the isolated smoke workspace."
    }
  ],
  "checks": [
    {
      "name": "external-artifact-present",
      "status": "passed",
      "evidence_ref": "evidence:file:evidence-txt"
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

1. Stable harness smoke, committed and CI-safe: `smoke/chapter-01/manifest.json` uses deterministic Python adapters.
2. Live Copilot smoke, local/manual or PTY-backed: `smoke/chapter-01/manifest-github-copilot-cli.json` uses the real `copilot` terminal agent.

This avoids making every test run depend on a subscription, quota, login state, model availability, and an interactive terminal.

## Live manifest

Create `smoke/chapter-01/manifest-github-copilot-cli.json`:

```json
{
  "id": "chapter-01-github-copilot-cli-smoke",
  "chapter": "01",
  "description": "Run the standalone github/copilot-cli terminal agent in an isolated workspace and validate the produced Chapter 01 report externally.",
  "timeout_seconds": 600,
  "sandbox": {
    "isolate_workspace": true
  },
  "expected_report": "report.json",
  "workspace_files": {
    "task.md": "Create evidence.txt and a Chapter 01 report.json. The report must reference concrete file evidence and must not rely on self_report evidence."
  },
  "agent_command": [
    "bash",
    "{repo_root}/smoke/chapter-01/agents/run_github_copilot_cli.sh"
  ]
}
```

## Manual TTY adapter

Because GitHub Copilot CLI is an interactive terminal agent, the most reliable first adapter is a manual TTY adapter. It prints the exact smoke context, opens a shell command you can run in a terminal/tmux pane, and then validates the report after you return.

Create `smoke/chapter-01/agents/run_github_copilot_cli.sh`:

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
1. Read task.md.
2. Create concrete evidence in this workspace, for example evidence.txt.
3. Write a valid Chapter 01 JSON report to this exact path:
   $HARNESS_SMOKE_REPORT_PATH

Report requirements:
- task_id: $HARNESS_SMOKE_SCENARIO_ID
- chapter: 01
- claimed_status: completed
- artifact.path should point to a concrete workspace artifact such as evidence.txt
- evidence must be file, command, validator, or similarly external evidence
- do not use self_report evidence
- keep all side effects inside the isolated workspace

After writing the report, run:
python3 -m harness_lab.chapter01 validate "$HARNESS_SMOKE_REPORT_PATH" --json

If validation fails, fix the report and rerun validation until it passes.
EOF

printf '\n=== Copilot smoke workspace ===\n%s\n' "$HARNESS_SMOKE_WORKSPACE"
printf '\n=== Prompt file ===\n%s/copilot-smoke-prompt.md\n' "$HARNESS_SMOKE_WORKSPACE"
printf '\nOpen a real terminal or tmux pane and run:\n\n'
printf '  cd %q && copilot --experimental\n\n' "$HARNESS_SMOKE_WORKSPACE"
printf 'Then paste or reference copilot-smoke-prompt.md inside Copilot CLI. If Autopilot mode is available, enable Autopilot mode so Copilot keeps working until the validator passes.\n'
printf '\nWhen Copilot has written report.json, return here and press Enter.\n'
read -r _

python3 -m harness_lab.chapter01 validate "$HARNESS_SMOKE_REPORT_PATH" --json
```

Make it executable:

```bash
chmod +x smoke/chapter-01/agents/run_github_copilot_cli.sh
```

Run the live smoke:

```bash
python3 -m harness_lab.smoke run smoke/chapter-01/manifest-github-copilot-cli.json \
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

## PTY-backed future adapter

For unattended live smoke, the harness should grow a PTY execution mode. The manifest could eventually contain a field such as:

```json
{
  "pty": true,
  "agent_command": ["copilot", "--experimental"]
}
```

The runner would then need to:

1. allocate an interactive TTY;
2. start `copilot --experimental` in `$HARNESS_SMOKE_WORKSPACE`;
3. send the prompt from `copilot-smoke-prompt.md`;
4. watch until the report file appears or a timeout expires;
5. validate with `python3 -m harness_lab.chapter01 validate`.

Do not fake this with plain `subprocess.run` unless the installed Copilot CLI version documents a non-interactive mode that works without a TTY.

## Validation commands

Validate the report directly:

```bash
python3 -m harness_lab.chapter01 validate "$HARNESS_SMOKE_REPORT_PATH" --json
```

Run the full smoke wrapper:

```bash
python3 -m harness_lab.smoke run smoke/chapter-01/manifest-github-copilot-cli.json --json
```

Run the stable deterministic fallback path:

```bash
python3 -m harness_lab.smoke run smoke/chapter-01/manifest.json --json
```

## Failure triage

Use the JSON summary from the smoke runner:

- `agent_exit_code != 0`: the Copilot adapter failed before validation.
- `agent_timed_out: true`: the adapter waited too long, often because Copilot CLI required interaction.
- `validator.failed > 0`: Copilot wrote a report, but the report did not satisfy the Chapter 01 contract.
- validator error includes `evidence[0].type cannot be self_report`: Copilot produced only a claim of completion; ask it to create concrete file or validator evidence.
- report file is missing: Copilot did not write `$HARNESS_SMOKE_REPORT_PATH` exactly.

## Fallback path

When GitHub Copilot CLI is unavailable, unauthenticated, quota-limited, or impractical in the current environment, keep the committed deterministic smoke manifest as the stable fallback path:

```bash
python3 -m harness_lab.smoke run smoke/chapter-01/manifest.json --json
```

That fallback path proves the harness runner and validator still work. It does not prove live Copilot integration.

## Why this is useful

This integration tests the important engineering property: a real terminal coding agent can operate in a sandbox, create artifacts, and be judged by an external deterministic validator.

The smoke harness therefore measures the agent loop around artifacts, not the agent's confidence or final prose.
