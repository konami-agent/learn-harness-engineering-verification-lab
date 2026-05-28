# Chapter-to-Verification Map

This document maps course chapters to verification artifacts.

Current design rule: start with Chapter 01 only, use it as the pilot, and do not expand the full 12-chapter matrix until the Chapter 01 design has been reviewed.

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
| Chapter claim | A model or agent can be capable of solving a task in principle while still being unreliable as an engineering component unless its behavior is constrained and externally verified by a harness. |
| Failure mode | The agent reports completion or produces plausible-looking output even though the required artifact is missing, malformed, incomplete, or not independently validated. |
| Primary verification type | Deterministic verification. The first proof should not depend on LLM randomness or subjective output quality. |
| Minimal reproducible scenario | A task requires producing a concrete artifact with a machine-checkable contract, for example a JSON report containing required keys, schema-valid values, and evidence fields. The harness checks the artifact directly instead of trusting the agent's final message. |
| Pass criterion | The validator confirms that the expected artifact exists, parses successfully, satisfies the schema, and contains evidence tied to the task result. |
| Fail criterion | Any of these fail: artifact missing, invalid schema, placeholder evidence, contradiction between reported success and validator result, or self-report without external evidence. |
| Real-agent smoke test need | Yes, but only after the deterministic validator exists. The smoke test should run a tiny real-agent task and prove that success is decided by the validator, not by the agent's self-report. |
| Downstream tasks shaped by this chapter | #3 should first build the deterministic validator around this contract. #4 should later wrap the same scenario as a bounded real-agent smoke test. #5 should include the Chapter 01 experiment as the first experiment case. |

## Open design questions for review

1. What should the first machine-checkable artifact be: JSON report, file tree mutation, test file, or command output?
2. Should Chapter 01 include both a positive case and a negative/self-report-only case from the start?
3. How strict should the evidence field be in the first validator?
4. Should the smoke test use the same scenario as the deterministic test, or a slightly more realistic task with the same contract?

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
