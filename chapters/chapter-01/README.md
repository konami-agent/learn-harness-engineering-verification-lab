# Chapter 01 Verification Lab: Capability does not imply reliability

This folder is a verification lab for the upstream Lecture 01 and Project 01 material. It does not replace the upstream course.

Upstream course source of truth:
- Repository: https://github.com/walkinglabs/learn-harness-engineering
- Upstream Lecture 01: https://github.com/walkinglabs/learn-harness-engineering/tree/main/docs/zh-TW/lectures/lecture-01-why-capable-agents-still-fail
- Upstream Project 01: https://github.com/walkinglabs/learn-harness-engineering/tree/main/docs/zh-TW/projects/project-01-baseline-vs-minimal-harness
- Upstream Project 01 code: https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-01

Read the course there. Run verification labs here.

## Chapter 01 verification lab path

Recommended order:

1. Read this overview.
2. Read `source.md` for upstream source grounding.
3. Read `verification-map.md` to see how upstream claims become local verification hypotheses.
4. Run `lab.md` for local executable checks.
5. Compare your output with `expected-results.md`.
6. Inspect `harness_lab/validators/chapter01.py` and `harness_lab/smoke.py` only after the verification flow is clear.

## Source grounding

This verification lab is grounded in upstream Lecture 01: 「第一講. 模型能力強，不等於執行可靠」.

Source claim used here: model capability and engineering reliability are different. A coding agent can report success or produce plausible output while still failing an externally verifiable completion contract.

Project interpretation: the harness must not trust an agent's final message. Completion must be decided by a deterministic validator reading concrete artifacts.

## Boundary with upstream Project 01

Upstream Project 01 already provides the learning exercise:

- `projects/project-01/starter/` demonstrates a weaker harness setup.
- `projects/project-01/solution/` demonstrates a stronger harness setup using artifacts such as `AGENTS.md`, `init.sh`, and `feature_list.json`.

This local lab does not duplicate that curriculum. Instead, it converts one subset of the learning claim into executable checks:

- deterministic validator behavior;
- positive and negative report fixtures;
- deterministic smoke with and without `AGENTS.md`;
- live-agent smoke contract for GitHub Copilot CLI;
- explicit notes about what remains manual observation.

## What this verification lab proves

This lab does not try to prove whether a model is intelligent or whether a specific agent can solve a large real-world task.

Instead, it turns the Chapter 01 engineering claim into a small executable contract:

- an agent or workflow may claim `completed`;
- the harness must still inspect concrete artifacts;
- self-report alone is not acceptable evidence;
- placeholder evidence is not acceptable evidence;
- completion must be decided by a repeatable validator, not by the model's final message.

In other words, the lab validates the Chapter 01 idea that model capability and engineering reliability are separate. A plausible success narrative can still fail the harness if it lacks externally checkable evidence.

## Deterministic validator

The Chapter 01 deterministic validator lives at `harness_lab/validators/chapter01.py`.

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
| Definition of Done should be command-verifiable. | The report is validated by `python3 -m harness_lab.validators.chapter01 validate ...`. |
| Failures should point to harness gaps. | The validator returns concrete errors such as `artifact.path does not exist`, `evidence[0].type cannot be self_report`, or `evidence[0].detail is placeholder text`. |

## Positive fixture

`chapters/chapter-01/fixtures/positive/report.json` is the passing case. It contains a machine-checkable JSON report with external file/validator evidence.

## Negative fixtures

The negative fixtures demonstrate the Chapter 01 failure mode: a report may claim success while the harness rejects it.

- `negative-missing-artifact/report.json`: claims completion but points to a missing artifact.
- `negative-self-report-only/report.json`: claims completion using only agent self-report evidence.
- `negative-placeholder-evidence/report.json`: claims completion with placeholder evidence.

## What remains manual observation

The deterministic validator and smoke scenarios do not prove the full upstream Project 01 comparison by themselves. These remain manual observation or future larger experiments:

- whether a real agent fails more often without a harness;
- whether the same real agent succeeds more often with a harness;
- whether cross-session state improves long-running tasks;
- whether `AGENTS.md` improves broad coding performance rather than this small scenario;
- whether SWE-bench or large-repository success rates improve.

## Run the lab

Validate all Chapter 01 fixtures:

```bash
python3 -m harness_lab.validators.chapter01 validate \
  chapters/chapter-01/fixtures/positive/report.json \
  chapters/chapter-01/fixtures/negative-missing-artifact/report.json \
  chapters/chapter-01/fixtures/negative-self-report-only/report.json \
  chapters/chapter-01/fixtures/negative-placeholder-evidence/report.json \
  --json
```

Run the full local verification suite:

```bash
python3 -m unittest discover -s tests -v
```

## Why this satisfies the local lab scope

This verification lab separates agent capability claims from independently verifiable reliability. The positive fixture passes only because a concrete report artifact satisfies the validator contract. The negative fixtures fail even though they contain plausible completion claims.

That is the executable subset of the Chapter 01 point: success must be defined by the harness, not by the model's self-assessment.
