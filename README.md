# Learn Harness Engineering Verification Lab

This repository is an executable verification companion to the upstream course `walkinglabs/learn-harness-engineering`:

https://github.com/walkinglabs/learn-harness-engineering

Read the course there. Run verification labs here.

This repo does not replace the upstream course. The upstream repository remains the source of truth for curriculum, lectures, exercises, projects, templates, and learning sequence. This repository turns selected upstream claims into reproducible validators, deterministic smoke scenarios, live-agent smoke contracts, and regression tests.

## Repository role

Upstream course:
- explains Harness Engineering concepts;
- provides Traditional Chinese lectures under `docs/zh-TW/`;
- provides projects such as Project 01 baseline-vs-minimal-harness;
- provides reusable templates such as `AGENTS.md`, `init.sh`, and `feature_list.json`.

This verification lab:
- maps upstream source claims to verification hypotheses;
- implements deterministic validators and fixtures;
- runs CI-safe smoke scenarios;
- keeps opt-in live-agent smoke adapters separate from deterministic tests;
- records what remains manual observation rather than pretending every learning claim is already mechanically proven.

## Chapter 01 verification lab path

Start here:

1. `chapters/chapter-01/README.md` — verification lab overview and boundary with upstream Lecture 01 / Project 01.
2. `chapters/chapter-01/source.md` — source grounding and upstream URLs.
3. `chapters/chapter-01/verification-map.md` — source claim → verification hypothesis → implemented artifact mapping.
4. `chapters/chapter-01/lab.md` — local verification lab commands.
5. `chapters/chapter-01/expected-results.md` — expected pass/fail outcomes for each command.

Chapter 01 deliverables:
- `chapters/chapter-01/fixtures/` contains one positive fixture and three negative fixtures.
- `chapters/chapter-01/smoke/deterministic/` contains CI-safe deterministic smoke scenarios.
- `chapters/chapter-01/smoke/live/github-copilot-cli/` contains the opt-in live GitHub Copilot CLI smoke adapter.
- `harness_lab/validators/chapter01.py` is the canonical Chapter 01 deterministic validator.
- `harness_lab/chapter01.py` remains as a backward-compatible CLI/import shim.
- `tests/chapter_01/` contains Chapter 01 engineering tests and documentation-contract tests.

## Repository layout

- `chapters/` — chapter-oriented verification lab folders: source notes, verification maps, lab commands, fixtures, and smoke scenarios.
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
