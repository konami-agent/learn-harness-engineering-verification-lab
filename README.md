# Learn Harness Engineering Verification Lab

This repository is a verification-focused companion to the Learn Harness Engineering course.

Goal:
- Turn each chapter's core claim into a reproducible experiment, test, or smoke scenario.
- Distinguish between deterministic harness verification and real-agent smoke testing.
- Track the project entirely through GitHub Issues with explicit status labels.

Current Chapter 01 deliverables:
- `docs/source-material.md` records the source course and citation policy.
- `docs/source-map.md` maps Chapter 01 source claims to project interpretations and verification hypotheses.
- `docs/chapter-map.md` records the Chapter 01 verification design.
- `harness_lab/chapter01.py` implements the Chapter 01 deterministic validator.
- `experiments/chapter-01/fixtures` contains one positive fixture and three negative fixtures for the Chapter 01 experiment.
- `smoke/chapter-01/manifest.json` defines the first sandboxed real-agent smoke wrapper for Chapter 01.
- `harness_lab/smoke.py` runs external agent commands in isolated workspaces and validates their reports with the deterministic validator.
- `tests/` contains executable checks for the validator, fixtures, smoke wrapper, CLI, and documentation contract.

Planned structure:
- `docs/` — chapter map, experiment notes, source grounding, and verification criteria
- `experiments/` — one folder per chapter / claim
- `harness_lab/` — deterministic validators and supporting code
- `smoke/` — small real-agent scenarios
- `tests/` — deterministic verification suite
- `reports/` — generated summaries from runs

Status model:
- `status:ready`
- `status:in-progress`
- `status:blocked`
- `status:review`
- `status:done`

Run local verification:

```bash
python3 -m unittest discover -s tests -v
```

Run the Chapter 01 validator manually:

```bash
python3 -m harness_lab.chapter01 validate experiments/chapter-01/fixtures/positive/report.json --json
```

Run the Chapter 01 smoke wrapper:

```bash
python3 -m harness_lab.smoke run smoke/chapter-01/manifest.json --json
```

This repo is intended to be public.
