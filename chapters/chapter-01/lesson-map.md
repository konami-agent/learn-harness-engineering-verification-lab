# Source Map

This file maps source-course claims to this repository's verification design.

It exists to prevent the verification lab from drifting into ungrounded agent-generated design. A chapter map is considered source-grounded only when it has an entry here.

## Chapter 01

- Source title: 第一講. 模型能力強，不等於執行可靠
- Source URL: https://walkinglabs.github.io/learn-harness-engineering/zh-TW/lectures/lecture-01-why-capable-agents-still-fail/
- Source page title: 第一講. 模型能力強，不等於執行可靠 | Learn Harness Engineering
- Grounding status: grounded draft
- Confidence: high for the chapter title and main claim; medium for the exact experiment design, which is this repo's interpretation.

### Source claim summary

The chapter argues that model capability and engineering reliability are different things. A strong coding agent can still fail in real development settings when the task, context, environment, validation loop, or cross-session state is underspecified.

The chapter frames many failures as harness problems rather than immediate evidence that the model itself is inadequate. It emphasizes that a well-designed harness can change the same model's behavior from unreliable to reliable by supplying rules, tools, context, environment, state, and verification.

### Source points used by this repository

- Benchmark success does not directly imply reliability on messy everyday engineering tasks.
- Agent self-reports such as “completed” are not enough; independent verification is required.
- Common failure causes include incomplete task specifications, missing project conventions, broken or unclear environments, absent validation commands, and lost cross-session state.
- Workspace instructions such as `AGENTS.md` are treated as a harness layer: they turn implicit project conventions and definitions of done into explicit agent-facing context before execution.
- When an agent fails, first diagnose which harness layer is missing or weak before concluding that the model is incapable.
- A definition of done should be command-verifiable, for example tests, lint, type checks, or another explicit validator.

### Project interpretation

For this verification lab, Chapter 01 becomes the claim that an agent's apparent capability and success narrative must be separated from externally verifiable completion.

A harness should therefore make completion observable and machine-checkable. The repo should not accept the agent's final message as evidence. It should require explicit workspace instructions, concrete artifacts, and deterministic validators.

### Verification hypothesis

A deterministic validator can distinguish between:

1. a task that merely receives a plausible agent success report, and
2. a task that produces an artifact satisfying a machine-checkable completion contract.

If the validator rejects missing, malformed, placeholder, or contradictory artifacts, the lab can demonstrate the Chapter 01 claim without depending on subjective model-output judgment.

### Initial artifact proposal

Use a small JSON report as the first machine-checkable artifact because it is easy to validate deterministically in a public repo.

The first Chapter 01 experiment should include both:

- a positive case: the report exists, parses, satisfies the schema, and contains non-placeholder evidence;
- a negative case: the agent or fixture claims success but the artifact is absent, malformed, or lacks acceptable evidence.

### Boundary between source and interpretation

Source-grounded:

- the chapter title;
- the claim that capability and reliability are different;
- the emphasis on harness layers, verification, definitions of done, and failure diagnosis.

Project interpretation:

- JSON report as the first artifact;
- exact schema requirements;
- positive/negative fixture structure;
- whether later real-agent smoke tests reuse this scenario.

### Open design questions

1. Is JSON the best first artifact, or should the first artifact be a file-tree mutation, a generated test, or command output?
2. How strict should evidence validation be in the first deterministic validator?
3. Should the real-agent smoke test reuse the deterministic scenario or use a slightly more realistic task?
4. Should Chapter 01 include an explicit “definition of done” fixture copied from the source theme before any smoke test exists?

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
