# Learn Harness Engineering Verification Lab

This repository is a verification-focused companion to the Learn Harness Engineering course.

Goal:
- Turn each chapter's core claim into a reproducible experiment, test, or smoke scenario.
- Distinguish deterministic harness verification from live real-agent smoke testing.
- Keep the repo readable for practice: start from a chapter folder, then inspect shared harness code only when needed.
- Track project work through GitHub Issues with explicit status labels.

## Chapter 01 learning path

Start here:

1. `chapters/chapter-01/README.md` — chapter overview and concept map.
2. `chapters/chapter-01/source.md` — source grounding and citation policy for the chapter.
3. `chapters/chapter-01/lesson-map.md` — source claim → verification hypothesis mapping.
4. `chapters/chapter-01/exercise.md` — hands-on commands to run while practicing.
5. `chapters/chapter-01/expected-results.md` — expected pass/fail outcomes for each command.

Chapter 01 deliverables:
- `chapters/chapter-01/fixtures/` contains one positive fixture and three negative fixtures.
- `chapters/chapter-01/smoke/deterministic/` contains CI-safe deterministic smoke scenarios.
- `chapters/chapter-01/smoke/live/github-copilot-cli/` contains the opt-in live GitHub Copilot CLI smoke adapter.
- `harness_lab/validators/chapter01.py` is the canonical Chapter 01 deterministic validator.
- `harness_lab/chapter01.py` remains as a backward-compatible CLI/import shim.
- `tests/chapter_01/` contains Chapter 01 engineering tests and documentation-contract tests.

## Repository layout

- `chapters/` — learning-first chapter folders: source notes, lesson maps, exercises, fixtures, and smoke scenarios.
- `harness_lab/` — reusable harness code, smoke runner, and validators.
- `harness_lab/validators/` — canonical validator implementations.
- `tests/` — engineering tests; chapter-specific tests live under `tests/chapter_01/`, `tests/chapter_02/`, etc.
- `docs/` — project-level architecture, issue seeds, and migration notes.
- `reports/` — generated summaries from runs.

## Run local verification

```bash
python3 -m unittest discover -s tests -v
```

## Run Chapter 01 manually

Canonical validator module:

```bash
python3 -m harness_lab.validators.chapter01 validate chapters/chapter-01/fixtures/positive/report.json --json
```

Backward-compatible validator shim:

```bash
python3 -m harness_lab.chapter01 validate chapters/chapter-01/fixtures/positive/report.json --json
```

Deterministic smoke with `AGENTS.md`:

```bash
python3 -m harness_lab.smoke run chapters/chapter-01/smoke/deterministic/manifest-with-agents.json --json
```

No-`AGENTS.md` control smoke, expected to fail wrapper validation while the deterministic adapter exits 0:

```bash
python3 -m harness_lab.smoke run chapters/chapter-01/smoke/deterministic/manifest-no-agents.json --json
```

Opt-in live GitHub Copilot CLI smoke:

```bash
python3 -m harness_lab.smoke run chapters/chapter-01/smoke/live/github-copilot-cli/manifest.json --json
```

The live Copilot smoke requires the standalone `copilot` CLI, authentication, network access, and Copilot quota/subscription availability. It is not a mandatory CI path.

This repo is intended to be public.
