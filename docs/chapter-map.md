# Chapter-to-Verification Map

This document maps course chapters to verification artifacts.

Current design rule: start with Chapter 01 only, use it as the pilot, and do not expand the full 12-chapter matrix until the Chapter 01 design has been reviewed.

Source-grounding rule: this file is downstream of `docs/source-map.md`. A chapter entry should not be treated as ready for implementation unless the corresponding source claim, project interpretation, and verification hypothesis have first been recorded in `docs/source-map.md`.

For each chapter, we will record:
- the chapter claim
- the failure mode the harness should expose
- the verification type
- the minimal reproducible scenario
- the pass/fail criterion
- whether a real-agent smoke test is required
- open design questions

## Chapter 01 pilot: Capability does not imply reliability

| Field | Draft |
| --- | --- |
| Source grounding | `docs/source-map.md`, Chapter 01 entry. |
| Source title | 第一講. 模型能力強，不等於執行可靠 |
| Source URL | https://walkinglabs.github.io/learn-harness-engineering/zh-TW/lectures/lecture-01-why-capable-agents-still-fail/ |
| Chapter claim | A model or agent can be capable of solving a task in principle while still being unreliable as an engineering component unless its behavior is constrained and externally verified by a harness. |
| Failure mode | The agent reports completion or produces plausible-looking output even though the required artifact is missing, malformed, incomplete, or not independently validated. |
| Primary verification type | Deterministic verification. The first proof should not depend on LLM randomness or subjective output quality. |
| Minimal reproducible scenario | A task requires producing a concrete artifact with a machine-checkable contract, for example a JSON report containing required keys, schema-valid values, and evidence fields. The harness checks the artifact directly instead of trusting the agent's final message. |
| Pass criterion | The validator confirms that the expected artifact exists, parses successfully, satisfies the schema, and contains evidence tied to the task result. |
| Fail criterion | Any of these fail: artifact missing, invalid schema, placeholder evidence, contradiction between reported success and validator result, or self-report without external evidence. |
| Real-agent smoke test need | Done for Chapter 01: `smoke/chapter-01/manifest.json` runs an external agent command in an isolated workspace, then validates the resulting report with `harness_lab.chapter01`. |
| Downstream tasks shaped by this chapter | #3 built the deterministic validator around this contract. #4 wraps the same scenario as a bounded smoke test. #5 includes the Chapter 01 experiment as the first experiment case. |

## Dependency note

Issue #2 depends on the source-grounding gap tracked by #9. The Chapter 01 map can be reviewed only after `docs/source-material.md` and `docs/source-map.md` exist and clearly separate source claims from this repository's verification design choices.

## Design decisions after Chapter 01 implementation

1. First machine-checkable artifact: JSON report.
2. Fixture coverage: include one positive case and three negative cases from the start.
3. Evidence strictness: reject missing artifacts, placeholder evidence, skipped checks, broken evidence references, and self-report-only evidence.
4. Smoke-test boundary: the deterministic scenario is now stable enough for a later real-agent smoke wrapper, but no real-agent runtime is required for the Chapter 01 deterministic proof.

## Deferred chapters

The following chapters remain intentionally deferred until the Chapter 01 pilot is approved:

- 02. What a harness actually is
- 03. Repository as the system of record
- 04. Split instructions across files
- 05. Cross-session continuity
- 06. Explicit initialization phase
- 07. Clear task boundaries
- 08. Feature list as the control surface
- 09. Prevent premature completion claims
- 10. End-to-end verification
- 11. Observability inside the harness
- 12. Clean handoff at session end
