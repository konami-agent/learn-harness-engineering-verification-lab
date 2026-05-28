# Chapter 01 Experiment: Capability does not imply reliability

## Source grounding

This experiment is grounded in `docs/source-map.md` for Chapter 01: 「第一講. 模型能力強，不等於執行可靠」.

Source claim used here: model capability and engineering reliability are different. A coding agent can report success or produce plausible output while still failing an externally verifiable completion contract.

Project interpretation: the harness must not trust an agent's final message. Completion must be decided by a deterministic validator reading concrete artifacts.

## Deterministic validator

The Chapter 01 deterministic validator lives at `harness_lab/chapter01.py`.

It validates JSON report artifacts and rejects reports when:

- the report file is missing or malformed;
- required fields are absent;
- `claimed_status` is not `completed`;
- the artifact path does not exist;
- evidence is placeholder text;
- evidence depends only on `self_report`;
- checks are skipped, missing, or reference nonexistent evidence.

## Positive fixture

`experiments/chapter-01/fixtures/positive/report.json` is the passing case. It contains a machine-checkable JSON report with external file/validator evidence.

## Negative fixtures

The negative fixtures demonstrate the Chapter 01 failure mode: a report may claim success while the harness rejects it.

- `negative-missing-artifact/report.json`: claims completion but points to a missing artifact.
- `negative-self-report-only/report.json`: claims completion using only agent self-report evidence.
- `negative-placeholder-evidence/report.json`: claims completion with placeholder evidence.

## Run the experiment

Validate all Chapter 01 fixtures:

```bash
python3 -m harness_lab.chapter01 validate \
  experiments/chapter-01/fixtures/positive/report.json \
  experiments/chapter-01/fixtures/negative-missing-artifact/report.json \
  experiments/chapter-01/fixtures/negative-self-report-only/report.json \
  experiments/chapter-01/fixtures/negative-placeholder-evidence/report.json \
  --json
```

Expected result:

- total: 4
- passed: 1
- failed: 3

Write a machine-readable summary file:

```bash
python3 -m harness_lab.chapter01 validate \
  experiments/chapter-01/fixtures/positive/report.json \
  --json \
  --summary-file reports/chapter-01-summary.json
```

Run the full local verification suite:

```bash
python3 -m unittest discover -s tests -v
```

## Why this satisfies Chapter 01

This experiment separates agent capability claims from independently verifiable reliability. The positive fixture passes only because a concrete report artifact satisfies the validator contract. The negative fixtures fail even though they contain plausible completion claims.

That is the core Chapter 01 point: success must be defined by the harness, not by the model's self-assessment.
