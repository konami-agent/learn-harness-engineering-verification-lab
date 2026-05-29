# Chapter 01 real-agent smoke wrapper

This directory contains the first real-agent smoke wrapper for Chapter 01.

The wrapper is intentionally small. It does not judge a model's natural-language output. Instead, it executes an external agent command in an isolated workspace and then asks the deterministic Chapter 01 validator to decide whether the produced report is acceptable.

## Boundary

The smoke runner is `harness_lab.smoke`.

For each manifest, it:

1. creates an isolated workspace;
2. writes any manifest-provided task files into that workspace;
3. runs the configured external agent command with smoke-specific environment variables;
4. expects the agent command to write a report artifact;
5. validates that report with `harness_lab.chapter01`;
6. records a machine-readable summary.

The important rule is unchanged from the deterministic experiment: success is still decided by `harness_lab.chapter01`, not by the external agent command saying that it succeeded.

## Manifests

Chapter 01 smoke is now an `AGENTS.md` presence/absence comparison. The positive path shows the agent being shaped by a workspace-local harness instruction layer; the control path uses the same agent command without `AGENTS.md` and must fail deterministic validation rather than relying on a self-report.

- `manifest.json`: positive smoke scenario. The external agent command receives both `task.md` and `AGENTS.md`, treats AGENTS.md as the harness instruction layer, writes `definition-of-done-check.txt`, and then writes a valid Chapter 01 report.
- `manifest-no-agents.json`: negative/control smoke scenario. The same external agent command receives `task.md` but no `AGENTS.md`, exits successfully, and writes only self-report-style completion evidence, so the validator rejects it.
- `manifest-self-report-only.json`: negative smoke scenario. The external agent command exits successfully and writes a plausible report, but the report uses only self-report evidence, so the validator rejects it.

## Agent command adapter

The current checked-in agent commands are deterministic Python adapters under `agents/`. They stand in for a real coding agent process during local and CI-safe verification.

A later Codex, Claude Code, or other real-agent adapter can reuse the same manifest shape as long as it writes the expected report file. The wrapper contract is the same:

- the agent receives an isolated workspace;
- the agent writes the report path declared by `HARNESS_SMOKE_REPORT_PATH`;
- the wrapper validates the report externally.

This keeps the smoke harness testable even on machines where the Codex CLI or another live agent is unavailable.

## GitHub Copilot CLI adapter

For a complete GitHub Copilot CLI adapter method for the standalone `copilot` command from `github/copilot-cli`, including installation checks, `copilot -p` non-interactive execution, permissions, live manifest shape, and the fallback path, see `docs/github-copilot-cli-smoke-agent.md`.

## Run the positive smoke scenario

```bash
python3 -m harness_lab.smoke run smoke/chapter-01/manifest.json --json
```

Expected result:

- wrapper exit code: 0
- `ok`: true
- `validator.passed`: 1
- `validator.failed`: 0

## Run the no-AGENTS.md control smoke scenario

```bash
python3 -m harness_lab.smoke run smoke/chapter-01/manifest-no-agents.json --json
```

Expected result:

- wrapper exit code: 1
- agent exit code: 0
- `ok`: false
- `validator.failed`: 1
- validator error includes `evidence[0].type cannot be self_report`

## Run the negative smoke scenario

```bash
python3 -m harness_lab.smoke run smoke/chapter-01/manifest-self-report-only.json --json
```

Expected result:

- wrapper exit code: 1
- `ok`: false
- `validator.failed`: 1
- validator error includes `evidence[0].type cannot be self_report`

## Write a summary file

```bash
python3 -m harness_lab.smoke run \
  smoke/chapter-01/manifest.json \
  --summary-file reports/chapter-01-smoke-summary.json \
  --json
```

## Relation to Chapter 01

This wrapper adds the real-agent execution layer that the deterministic Chapter 01 validator deliberately avoided.

The experiment now has four layers:

1. `AGENTS.md` harness instructions: define the workspace-local definition of done before the agent acts;
2. no-`AGENTS.md` control: runs the same adapter without the instruction layer and expects validation failure despite successful process exit;
3. deterministic validator: decides whether a report satisfies the completion contract;
4. real-agent smoke wrapper: runs an external agent command in a sandbox and feeds the resulting report to that validator.

That separation is the key Chapter 01 harness lesson. Agent execution is allowed to be messy, stochastic, or tool-driven. Completion is still decided by a reproducible external validator, and the agent's behavior is shaped by repo-local instructions instead of an underspecified prompt. The presence/absence comparison makes the lesson explicit: the harness instruction layer is part of the reliability mechanism, not incidental documentation.
