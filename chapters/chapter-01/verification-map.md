# Chapter 01 Verification Map

This file maps upstream source claims to this repository's verification design.

It exists to prevent the verification lab from drifting into ungrounded agent-generated design. A chapter map is considered source-grounded only when it has entries here.

## Upstream anchors

- Upstream repository: https://github.com/walkinglabs/learn-harness-engineering
- Upstream Lecture 01: `docs/zh-TW/lectures/lecture-01-why-capable-agents-still-fail/`
- Upstream Project 01: `docs/zh-TW/projects/project-01-baseline-vs-minimal-harness/`
- Upstream Project 01 code: `projects/project-01/`

## Chapter 01

- Source title: 第一講. 模型能力強，不等於執行可靠
- Source URL: https://walkinglabs.github.io/learn-harness-engineering/zh-TW/lectures/lecture-01-why-capable-agents-still-fail/
- Source page title: 第一講. 模型能力強，不等於執行可靠 | Learn Harness Engineering
- Grounding status: grounded draft
- Confidence: high for the chapter title and main claim; medium for the exact experiment design, which is this repo's interpretation.

## Source claim summary

The upstream Lecture 01 argues that model capability and engineering reliability are different things. A strong coding agent can still fail in real development settings when the task, context, environment, validation loop, or cross-session state is underspecified.

The upstream Project 01 exercise already asks learners to compare a weak-harness starter setup with a stronger harness solution setup. This verification lab does not replace that exercise. It extracts a smaller executable subset: a harness should reject completion claims that lack concrete evidence.

## Claim-to-verification table

| Source claim | Upstream location | Project interpretation | Verification hypothesis | Implemented artifact | Status |
| --- | --- | --- | --- | --- | --- |
| Model capability does not imply execution reliability. | upstream Lecture 01 | A plausible success narrative must still be checked by a harness. | A report can claim `completed` and still fail if evidence is missing or weak. | `harness_lab/validators/chapter01.py`; negative fixtures | implemented |
| Agent self-report is not enough evidence. | upstream Lecture 01 | The validator should reject self-assessment as completion proof. | Any report using only `self_report` evidence fails. | `chapters/chapter-01/fixtures/negative-self-report-only/report.json`; `manifest-self-report-only.json` | implemented |
| Definition of Done should be command-verifiable. | upstream Lecture 01 | Completion should be decided by a repeatable command, not by reading the agent's final message. | `python3 -m harness_lab.validators.chapter01 validate ...` returns pass/fail with explicit errors. | `harness_lab/validators/chapter01.py`; `tests/chapter_01/test_validator.py` | implemented |
| Workspace instructions such as `AGENTS.md` are a harness layer. | upstream Lecture 01 and upstream Project 01 | The smoke workspace can show a small contrast between a harness-instructed path and a no-AGENTS.md control path. | `manifest-with-agents.json` passes; `manifest-no-agents.json` exits non-zero at wrapper validation because evidence falls back to `self_report`. | deterministic smoke manifests and adapters | implemented |
| Baseline-vs-minimal-harness project work should compare weak and strong harness setups. | upstream Project 01 | Full project comparison remains broader than this deterministic report contract. | The local lab can point to manual observation, but should not claim to fully prove the upstream project result. | `lab.md`; this `verification-map.md` | manual observation |
| A live coding agent can be placed behind the same completion contract. | local extension from upstream claim | A live adapter should be opt-in and still feed artifacts into the deterministic validator. | GitHub Copilot CLI must produce `definition-of-done-check.txt` and a report accepted by the validator. | `chapters/chapter-01/smoke/live/github-copilot-cli/manifest.json`; `run.sh` | contract implemented; live run opt-in |

## Boundary between source and interpretation

Source-grounded:

- the chapter title;
- the claim that capability and reliability are different;
- the emphasis on harness layers, verification, definitions of done, and failure diagnosis;
- the existence of upstream Project 01's baseline-vs-minimal-harness exercise.

Project interpretation:

- JSON report as the first artifact;
- exact schema requirements;
- positive/negative fixture structure;
- deterministic `AGENTS.md` vs no-`AGENTS.md` smoke manifests;
- whether later real-agent smoke tests reuse this scenario.

## Manual observation items

The following are still manual observation or future larger experiments:

1. Whether a real agent fails more often without a harness on upstream Project 01.
2. Whether the same real agent succeeds more often with upstream Project 01's solution harness.
3. Whether `AGENTS.md` improves broad coding performance rather than this narrow smoke scenario.
4. Whether cross-session state improves long-running tasks.
5. Whether large-repository or benchmark success rates improve.

## Open design questions

1. Should future labs directly import upstream Project 01 starter/solution, or keep only source links?
2. Should Chapter 01 add a live Codex/Claude Code adapter parallel to the GitHub Copilot CLI adapter?
3. Should the deterministic validator evolve from JSON report validation into actual file-tree diff validation?
4. How much upstream project execution evidence can be captured without duplicating upstream curriculum?

## Deferred chapters

The following chapters are not yet source-grounded in this repo. They should not be expanded into detailed experiments until Chapter 01's mapping has been reviewed.

- 02. Harness 到底是什麼
- 03. 讓程式碼儲存庫成為唯一的事實來源
- 04. 把指令拆分到不同檔案裡
- 05. 讓跨工作階段的任務保持脈絡連續
- 06. 讓 agent 每次工作前先初始化
- 07. 給 agent 劃清每次任務的邊界
- 08. 用功能清單約束 agent 該做什麼
- 09. 防止 agent 提前宣告完成
- 10. 跑通完整流程才算真正驗證
- 11. 讓 agent 的執行過程可觀測
- 12. 每次工作階段結束前都做好交接
