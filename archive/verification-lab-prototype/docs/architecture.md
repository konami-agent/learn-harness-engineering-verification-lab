# Repository Architecture

The repository uses a chapter-oriented learning layout with a small reusable harness library.

## Learning folders

`chapters/<chapter>/` is the primary reader entrypoint. Each chapter should contain:

- `README.md` — overview and reading order.
- `source.md` — source grounding for the chapter.
- `verification-map.md` — source claim → project interpretation → verification hypothesis.
- `lab.md` — hands-on commands.
- `expected-results.md` — expected command outcomes.
- `fixtures/` — deterministic input/output examples.
- `smoke/` — chapter-specific smoke scenarios.

## Reusable code

`harness_lab/` contains code intended to be imported or invoked across chapters.

- `harness_lab/smoke.py` runs smoke manifests in isolated workspaces.
- `harness_lab/validators/` contains canonical validators.
- Legacy modules such as `harness_lab/chapter01.py` may remain as compatibility shims during migrations.

## Tests

Engineering tests live under `tests/`.

- Chapter tests use `tests/chapter_01/`, `tests/chapter_02/`, etc.
- Top-level tests such as `tests/test_repo_structure.py` enforce repository-wide layout invariants.

This separation keeps the verification lab path readable while preserving importable, reusable harness code.
