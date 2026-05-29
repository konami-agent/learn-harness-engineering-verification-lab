# Project 01 module: Baseline vs minimal harness

## Upstream project

- Course: `walkinglabs/learn-harness-engineering`
- Project: Project 01. 只寫提示詞讓代理做，和定好規則再讓它做，差多少
- Project page: https://walkinglabs.github.io/learn-harness-engineering/zh-TW/projects/project-01-baseline-vs-minimal-harness/
- Source repository path: https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-01

## Module purpose

This module helps a facilitator teach Project 01 as a workshop: run the same
small Electron app task once with weak harness support and once with a minimal
harness, then compare the outcomes.

The goal is not to retell every paragraph of the upstream lesson. The goal is to
prepare learners to run the project, observe the difference, and discuss why the
harness changed the agent's behavior.

## Learning outcomes

After this module, learners should be able to:

1. Explain why model capability does not guarantee reliable task execution.
2. Identify the difference between a prompt-only task and a minimal harness.
3. Describe the role of `AGENTS.md`, `init.sh`, and `feature_list.json` in Project 01.
4. Run or review a baseline-vs-harness comparison using consistent constraints.
5. Turn the comparison into a short reflection about missing harness support.

## Required concepts

- Capability vs reliability.
- Harness as model-external engineering infrastructure.
- Repository as visible context for an agent.
- Definition of Done and executable verification.
- Controlled comparison: same task, same agent, different harness support.

## Source lectures

- Lecture 01: 模型能力強，不等於執行可靠.
- Lecture 02: Harness 到底是什麼.
- Lecture 06: 為什麼初始化需要單獨一個階段, as supporting context for `init.sh`.

## Deck breakdown

### Deck 01: Why capable agents still fail

- File: `decks/01-problem-framing.md`
- Core question: why can a capable coding agent still fail a simple project?
- Use when: opening the workshop and motivating the comparison.
- Project bridge: introduces the Electron app task and the baseline run.

### Deck 02: What the minimal harness adds

- File: `decks/02-minimal-harness.md`
- Core question: what changes when the repository contains explicit instructions,
  initialization, and feature expectations?
- Use when: preparing the improved run.
- Project bridge: explains `AGENTS.md`, `init.sh`, and `feature_list.json`.

### Deck 03: Compare runs and extract lessons

- File: `decks/03-comparison-and-reflection.md`
- Core question: how do we compare the two runs without turning the exercise into
  a vague impression?
- Use when: after both runs or while reviewing recorded runs.
- Project bridge: produces the final comparison table and reflection.

## Learner deliverable

A short project note containing:

- baseline run evidence: prompt, log/summary, diff, startup result;
- minimal-harness run evidence: prompt, harness files, log/summary, startup result;
- comparison table using the upstream metrics;
- 3-5 bullet reflection on which harness artifacts mattered most.

## Speaker notes

See `notes/speaker-notes.md`.

## Boundary

The upstream project is the canonical assignment. This module is only the slide
and facilitation layer for teaching it.
