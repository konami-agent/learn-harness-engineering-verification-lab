# GitHub Copilot CLI adapter for Chapter 01 smoke

This guide explains how to use GitHub Copilot CLI as the real agent behind the Chapter 01 smoke wrapper.

The important boundary is the same as the rest of the smoke harness: GitHub Copilot CLI may produce the commands, shell script, or report content, but the smoke run only passes when `harness_lab.chapter01` validates the resulting `report.json`. The agent's final answer is never enough.

## Current limitation

The public GitHub Copilot command that most users have is the GitHub CLI extension, invoked as `gh copilot`. That tool is useful for suggesting and explaining shell commands, but it is not a fully autonomous coding agent in the same sense as a tool-running agent that can freely edit files until the validator passes.

That means there are two practical integration paths:

1. Human-in-the-loop `gh copilot` path: use Copilot CLI to generate the exact shell/script steps, then paste or save those steps into the smoke workspace. This is a real-agent smoke because a real Copilot model participates, but it is not unattended automation.
2. Fully automated adapter path: use a Copilot-compatible autonomous CLI, if your environment provides one, and make it write `$HARNESS_SMOKE_REPORT_PATH` directly. Some environments expose an ACP-style command such as `copilot --acp --stdio`; that is different from the `gh copilot` extension and must be verified on the target machine.

Use path 1 as the baseline because it works with the standard GitHub CLI extension. Use path 2 only after verifying that your machine has an actual non-interactive Copilot agent CLI.

## Prerequisites

Install and authenticate GitHub CLI:

```bash
gh auth login
gh auth status
```

Install the Copilot extension if it is not present:

```bash
gh extension install github/gh-copilot
```

Verify the command surface before writing an adapter, because installed versions and subcommands may differ:

```bash
gh copilot --help
gh copilot suggest --help
gh copilot explain --help
```

If `gh copilot --help` is missing, stop and fix the installation first. Do not mark a live Copilot smoke as complete by falling back silently to the deterministic Python adapter.

## Smoke contract

The smoke runner sets these environment variables for the agent command:

```bash
HARNESS_SMOKE_REPO_ROOT      # repository root
HARNESS_SMOKE_WORKSPACE      # isolated workspace for this smoke run
HARNESS_SMOKE_REPORT_PATH    # exact path the agent must write
HARNESS_SMOKE_SCENARIO_ID    # manifest id
```

The Copilot-driven step must write a JSON report to `$HARNESS_SMOKE_REPORT_PATH`. The report must satisfy the Chapter 01 validator and must not use self-report as evidence.

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
      "detail": "The Copilot-generated command created evidence.txt in the isolated workspace."
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

## Path 1: human-in-the-loop `gh copilot` copy-paste loop

This path is the safest complete method for the standard GitHub Copilot CLI extension.

### 1. Create a live manifest

Create `smoke/chapter-01/manifest-github-copilot-cli.json`:

```json
{
  "id": "chapter-01-github-copilot-cli-smoke",
  "chapter": "01",
  "description": "Use GitHub Copilot CLI in a human-in-the-loop adapter, then validate the produced report externally.",
  "timeout_seconds": 300,
  "sandbox": {
    "isolate_workspace": true
  },
  "expected_report": "report.json",
  "workspace_files": {
    "task.md": "Use GitHub Copilot CLI to help create evidence.txt and a Chapter 01 report.json. The report must reference concrete file evidence and must not rely on self_report evidence."
  },
  "agent_command": [
    "bash",
    "{repo_root}/smoke/chapter-01/agents/run_github_copilot_cli_manual.sh"
  ]
}
```

### 2. Create the manual adapter

Create `smoke/chapter-01/agents/run_github_copilot_cli_manual.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

cd "$HARNESS_SMOKE_WORKSPACE"

cat > copilot-prompt.txt <<EOF
You are helping complete a smoke test in an isolated workspace.

Write shell commands that:
1. create evidence.txt in the current directory;
2. write a valid Chapter 01 report JSON to this exact path:
   $HARNESS_SMOKE_REPORT_PATH
3. ensure the report uses concrete file evidence, not self_report evidence;
4. keep all output local to this workspace.

The report must use task_id "$HARNESS_SMOKE_SCENARIO_ID" and chapter "01".
EOF

printf '\n=== Copilot prompt ===\n'
cat copilot-prompt.txt
printf '\n=== Ask GitHub Copilot CLI ===\n'
printf 'Run this in another terminal if interactive prompts are easier:\n'
printf '  cd %q && gh copilot suggest -t shell < copilot-prompt.txt\n' "$HARNESS_SMOKE_WORKSPACE"
printf '\nPaste the Copilot-suggested shell commands below, then press Ctrl-D.\n'

cat > copilot-suggested-commands.sh
chmod +x copilot-suggested-commands.sh
bash ./copilot-suggested-commands.sh

python3 -m harness_lab.chapter01 validate "$HARNESS_SMOKE_REPORT_PATH" --json
```

This adapter is intentionally interactive: it pauses for the copy-paste loop. It lets the real Copilot CLI produce the commands while keeping the final decision in the deterministic validator.

### 3. Run the live smoke

From the repo root:

```bash
python3 -m harness_lab.smoke run smoke/chapter-01/manifest-github-copilot-cli.json \
  --summary-file reports/chapter-01-github-copilot-cli-smoke-summary.json \
  --json
```

A passing run should have:

- wrapper exit code `0`;
- `ok: true`;
- `agent_exit_code: 0`;
- `validator.passed: 1`;
- `validator.failed: 0`.

If the adapter exits nonzero or the validator fails, treat the smoke as failed even if Copilot's text claimed success.

## Path 2: fully automated Copilot-compatible agent CLI

Use this path only if your machine has a non-interactive Copilot agent command. Verify it first:

```bash
command -v copilot
copilot --help
```

If the CLI supports an ACP server mode, verify that explicitly:

```bash
copilot --acp --stdio --help
```

If these commands are unavailable, this path is not available on that machine. Use the `gh copilot` copy-paste loop instead.

A future fully automated adapter can follow this shape:

```bash
#!/usr/bin/env bash
set -euo pipefail

cd "$HARNESS_SMOKE_WORKSPACE"

cat > prompt.md <<EOF
You are running as the real agent for a Chapter 01 smoke test.

Read task.md. Create concrete workspace evidence and write a valid JSON report to:
$HARNESS_SMOKE_REPORT_PATH

Requirements:
- task_id: $HARNESS_SMOKE_SCENARIO_ID
- chapter: 01
- claimed_status: completed
- include at least one file or validator evidence item
- do not use self_report evidence
- keep all side effects inside $HARNESS_SMOKE_WORKSPACE
EOF

# Replace this placeholder with the exact non-interactive Copilot command
# available in your environment.
copilot run --workspace "$HARNESS_SMOKE_WORKSPACE" --prompt-file prompt.md

python3 -m harness_lab.chapter01 validate "$HARNESS_SMOKE_REPORT_PATH" --json
```

The placeholder `copilot run` is not assumed to exist. It is a template slot for whichever Copilot-compatible autonomous CLI your environment actually provides.

## Fallback path

When GitHub Copilot CLI is unavailable or only supports interactive shell suggestions, keep the committed deterministic smoke manifest as the stable fallback path:

```bash
python3 -m harness_lab.smoke run smoke/chapter-01/manifest.json --json
```

That fallback path proves the harness runner and validator still work. It does not prove live Copilot integration.

## Failure triage

Use the JSON summary from the smoke runner:

- `agent_exit_code != 0`: the Copilot adapter failed before validation.
- `agent_timed_out: true`: the adapter waited too long, often because `gh copilot` required interaction.
- `validator.failed > 0`: the agent wrote a report, but the report did not satisfy the Chapter 01 contract.
- validator error includes `evidence[0].type cannot be self_report`: Copilot produced only a claim of completion; ask it to create concrete file or validator evidence.
- report file is missing: the adapter did not write `$HARNESS_SMOKE_REPORT_PATH` exactly.

## Why this is still useful

Even with the human-in-the-loop copy-paste loop, this integration tests the important engineering property: the model can suggest real commands, those commands can operate in a sandbox, and success is determined by an external validator.

The smoke harness therefore measures the agent loop around artifacts, not the agent's confidence or final prose.
