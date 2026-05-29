# Migration Notes

## Chapter 01 chapter-oriented layout

Chapter 01 was reorganized from a technology-type layout into a learning-first layout.

Old locations:

- `experiments/chapter-01/`
- `smoke/chapter-01/`
- `harness_lab/chapter01.py` as canonical implementation
- top-level `tests/test_chapter01_*.py`

New locations:

- `chapters/chapter-01/`
- `chapters/chapter-01/smoke/deterministic/`
- `chapters/chapter-01/smoke/live/github-copilot-cli/`
- `harness_lab/validators/chapter01.py` as canonical implementation
- `harness_lab/chapter01.py` as backward-compatible shim
- `tests/chapter_01/`

The compatibility shim lets existing commands such as this continue to work temporarily:

```bash
python3 -m harness_lab.chapter01 validate chapters/chapter-01/fixtures/positive/report.json --json
```

New documentation and exercises should prefer:

```bash
python3 -m harness_lab.validators.chapter01 validate chapters/chapter-01/fixtures/positive/report.json --json
```
