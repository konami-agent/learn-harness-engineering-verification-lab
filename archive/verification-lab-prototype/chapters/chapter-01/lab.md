# Chapter 01 Verification Lab

This is the local verification lab for Chapter 01. It does not replace the upstream Project 01 exercise.

Read the course there. Run verification labs here.

Upstream Project 01 is the learning exercise. It asks learners to compare a weak harness starter setup with a stronger harness solution setup. This local lab is narrower: it runs deterministic checks that prove the harness rejects weak completion evidence.

Run commands from the repository root.

## 1. Run the deterministic validator on all fixtures

```bash
python3 -m harness_lab.validators.chapter01 validate \
  chapters/chapter-01/fixtures/positive/report.json \
  chapters/chapter-01/fixtures/negative-missing-artifact/report.json \
  chapters/chapter-01/fixtures/negative-self-report-only/report.json \
  chapters/chapter-01/fixtures/negative-placeholder-evidence/report.json \
  --json
```

Expected shape:

- total: 4
- passed: 1
- failed: 3

Read `expected-results.md` for the specific error each negative fixture should produce.

## 2. Run the deterministic smoke with AGENTS.md

```bash
python3 -m harness_lab.smoke run chapters/chapter-01/smoke/deterministic/manifest-with-agents.json --json
```

This deterministic smoke is CI-safe. It uses a deterministic Python adapter, not Copilot. The important behavior is that the workspace contains `AGENTS.md`, the adapter creates `definition-of-done-check.txt`, and the deterministic validator accepts concrete evidence.

## 3. Run the no-AGENTS.md control

```bash
python3 -m harness_lab.smoke run chapters/chapter-01/smoke/deterministic/manifest-no-agents.json --json
```

This command is expected to exit non-zero at the wrapper level. The deterministic adapter exits 0, but without the harness instruction layer it writes self-report evidence, and the validator rejects it.

## 4. Run the self-report-only negative smoke

```bash
python3 -m harness_lab.smoke run chapters/chapter-01/smoke/deterministic/manifest-self-report-only.json --json
```

This is another expected failure. It demonstrates that a successful agent process is not enough when evidence is only `self_report`.

## 5. Optional: run the live GitHub Copilot CLI smoke

```bash
python3 -m harness_lab.smoke run chapters/chapter-01/smoke/live/github-copilot-cli/manifest.json --json
```

This live GitHub Copilot CLI smoke path actually invokes the standalone `copilot` CLI through `chapters/chapter-01/smoke/live/github-copilot-cli/run.sh`. It is opt-in because it depends on local installation, authentication, network access, and Copilot quota/subscription availability.

## Relationship to upstream Project 01

After running this local lab, the broader manual exercise remains upstream:

- run or inspect upstream `projects/project-01/starter/` for the weak-harness scenario;
- run or inspect upstream `projects/project-01/solution/` for the stronger harness scenario;
- compare the qualitative and quantitative outcomes described by upstream Project 01;
- return here only when you want executable validators and smoke contracts for a smaller claim.

## Reflection questions

- Which failures are caused by missing artifacts?
- Which failures are caused by untrusted self-report evidence?
- What changes when `AGENTS.md` is present in the smoke workspace?
- Why does the validator, rather than the agent final message, decide whether the task is complete?
- Which upstream Project 01 observations are still manual observation rather than deterministic proof?
