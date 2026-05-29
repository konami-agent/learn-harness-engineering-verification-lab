# Chapter 01 Expected Results

Run commands from the repository root.

## Fixture validation

Command:

```bash
python3 -m harness_lab.validators.chapter01 validate \
  chapters/chapter-01/fixtures/positive/report.json \
  chapters/chapter-01/fixtures/negative-missing-artifact/report.json \
  chapters/chapter-01/fixtures/negative-self-report-only/report.json \
  chapters/chapter-01/fixtures/negative-placeholder-evidence/report.json \
  --json
```

Expected process exit code: `1`, because not all fixtures pass.

Expected summary:

```text
total=4
passed=1
failed=3
```

Expected per-fixture behavior:

- `positive/report.json`: passes.
- `negative-missing-artifact/report.json`: fails with `artifact.path does not exist`.
- `negative-self-report-only/report.json`: fails with `evidence[0].type cannot be self_report`.
- `negative-placeholder-evidence/report.json`: fails with `evidence[0].detail is placeholder text`.

## Deterministic smoke with AGENTS.md

Command:

```bash
python3 -m harness_lab.smoke run chapters/chapter-01/smoke/deterministic/manifest-with-agents.json --json
```

Expected process exit code: `0`.

Expected summary:

```text
ok=true
agent_exit_code=0
validator.passed=1
validator.failed=0
```

Expected workspace artifact:

```text
definition-of-done-check.txt
```

The artifact should mention `AGENTS.md` and the definition of done.

## No-AGENTS.md control smoke

Command:

```bash
python3 -m harness_lab.smoke run chapters/chapter-01/smoke/deterministic/manifest-no-agents.json --json
```

Expected process exit code: `1`.

Important distinction:

```text
agent_exit_code=0
validator.failed=1
```

Expected validator error:

```text
evidence[0].type cannot be self_report
```

This demonstrates the Chapter 01 lesson: a successful agent process is not the same as harness acceptance.

## Self-report-only negative smoke

Command:

```bash
python3 -m harness_lab.smoke run chapters/chapter-01/smoke/deterministic/manifest-self-report-only.json --json
```

Expected process exit code: `1`.

Expected validator error:

```text
evidence[0].type cannot be self_report
```

## Live GitHub Copilot CLI smoke

Command:

```bash
python3 -m harness_lab.smoke run chapters/chapter-01/smoke/live/github-copilot-cli/manifest.json --json
```

Expected behavior depends on local environment:

- If `copilot` is not installed, the adapter exits with a setup error.
- If Copilot is installed and authenticated, the adapter invokes `copilot -p`, asks it to follow `AGENTS.md`, and then validates the generated `report.json`.
- This path is not a mandatory CI gate.
