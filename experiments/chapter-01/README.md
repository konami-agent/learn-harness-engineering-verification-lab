# Chapter 01 Experiment: Capability does not imply reliability

## Source grounding

This experiment is grounded in `docs/source-map.md` for Chapter 01: 「第一講. 模型能力強，不等於執行可靠」.

Source claim used here: model capability and engineering reliability are different. A coding agent can report success or produce plausible output while still failing an externally verifiable completion contract.

Project interpretation: the harness must not trust an agent's final message. Completion must be decided by a deterministic validator reading concrete artifacts.

## What this experiment proves

This experiment does not try to prove whether a model is intelligent or whether a specific agent can solve a large real-world task.

Instead, it turns the Chapter 01 engineering claim into a small executable contract:

- an agent or workflow may claim `completed`;
- the harness must still inspect concrete artifacts;
- self-report alone is not acceptable evidence;
- placeholder evidence is not acceptable evidence;
- completion must be decided by a repeatable validator, not by the model's final message.

In other words, the experiment validates the Chapter 01 idea that model capability and engineering reliability are separate. A plausible success narrative can still fail the harness if it lacks externally checkable evidence.

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

This implements a minimal Definition of Done for Chapter 01: a task is not complete because an agent says it is complete. It is complete only when the report artifact exists, parses, satisfies the contract, contains non-placeholder external evidence, and links passed checks to that evidence.

## Mapping from Chapter 01 concepts to validator behavior

| Chapter 01 concept | Validator behavior |
| --- | --- |
| Model capability is not the same as execution reliability. | A report can say `claimed_status: completed` and still fail validation. |
| Do not trust an agent's self-assessment as proof of completion. | `evidence.type == "self_report"` is rejected. |
| Completion needs external verification. | `artifact.path` must exist, `checks` must pass, and each check must reference real evidence. |
| Definition of Done should be command-verifiable. | The report is validated by `python3 -m harness_lab.chapter01 validate ...`. |
| Failures should point to harness gaps. | The validator returns concrete errors such as `artifact.path does not exist`, `evidence[0].type cannot be self_report`, or `evidence[0].detail is placeholder text`. |

## Why JSON report artifacts

The first Chapter 01 proof should be deterministic and small. JSON reports are useful here because they:

- produce the same validation result every time;
- make positive and negative fixtures easy to compare;
- separate `claimed_status` from `evidence` and `checks`;
- can become the contract that a later real-agent smoke test must satisfy.

This order is intentional: first define the completion contract, then later let a real agent attempt to satisfy it. If the project starts with unstructured real-agent output, the result is too easy to judge subjectively.

## Positive fixture

`experiments/chapter-01/fixtures/positive/report.json` is the passing case. It contains a machine-checkable JSON report with external file/validator evidence.

It passes because:

- the report exists and parses as JSON;
- `claimed_status` is `completed`;
- the artifact path exists;
- evidence is not a self-report and not placeholder text;
- checks are marked `passed` and reference valid evidence.

## Negative fixtures

The negative fixtures demonstrate the Chapter 01 failure mode: a report may claim success while the harness rejects it.

- `negative-missing-artifact/report.json`: claims completion but points to a missing artifact.
- `negative-self-report-only/report.json`: claims completion using only agent self-report evidence.
- `negative-placeholder-evidence/report.json`: claims completion with placeholder evidence.

These cases are deliberately small. Their purpose is to prove that the harness rejects false or weak completion evidence even when the report is shaped like a plausible success artifact.

## What this experiment does not prove yet

This deterministic seed does not yet validate every claim discussed in Chapter 01.

It does not prove:

- that a real agent fails more often without a harness;
- that the same real agent succeeds more often with a harness;
- that cross-session state improves long-running tasks;
- that `AGENTS.md` improves coding performance;
- that SWE-bench or large-repository success rates improve.

Those require later real-agent smoke tests or larger experiments. This experiment is the first layer: it proves that the repository has an executable completion contract that refuses to confuse self-report with verified success.

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

More precisely, `harness_lab/chapter01.py` is the minimal executable form of the Chapter 01 claim: it accepts externally grounded completion evidence and rejects self-report, missing artifacts, and placeholder evidence. It is not a full benchmark; it is the deterministic proof seed that later real-agent experiments can reuse.
