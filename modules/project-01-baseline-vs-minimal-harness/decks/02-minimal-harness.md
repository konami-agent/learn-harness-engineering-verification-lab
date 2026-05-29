---
title: "Project 01 / Deck 02: What the minimal harness adds"
module: "project-01-baseline-vs-minimal-harness"
source: "walkinglabs/learn-harness-engineering"
---

# Project 01 / Deck 02

## What the minimal harness adds

Core question: what changes when the repository gives the agent explicit support?

---

# Minimal harness in Project 01

The improved run adds three visible artifacts before the agent starts:

- `AGENTS.md` — project rules, boundaries, and commands;
- `init.sh` — one command for setup / startup recovery;
- `feature_list.json` — expected features and completion evidence.

This is not a giant framework. It is a small amount of structure in the right
place.

---

# `AGENTS.md`

`AGENTS.md` answers questions the agent would otherwise infer:

- What is this project?
- What stack and commands should be used?
- What boundaries should not be crossed?
- How should the agent verify work before stopping?

Good `AGENTS.md` acts like a map, not a long manual.

---

# `init.sh`

`init.sh` makes the environment path explicit.

It should answer:

- how to install dependencies;
- how to start the app;
- what command proves the basic app path is alive.

Without this, the agent may waste time guessing commands or may stop without
having ever run the application.

---

# `feature_list.json`

`feature_list.json` turns vague scope into checkable work.

For Project 01, the feature list should represent the required product slice:

- window startup;
- document list area;
- Q&A panel area;
- local data directory behavior.

The list helps the agent and the reviewer agree on what "done" means.

---

# What changes between runs?

The prompt can stay the same.

The difference is the repository context:

```text
baseline: prompt only
improved: prompt + visible project rules + startup path + feature expectations
```

This isolates the teaching point: the harness changes execution reliability
without changing the model.

---

# Facilitator checklist

Before running the improved condition, confirm:

- both runs use the same agent;
- both runs use the same task prompt;
- time / turn limits are comparable;
- improved branch contains the harness artifacts before the agent starts;
- after the run, verification uses the documented command rather than the
  agent's final summary alone.

---

# Takeaway

A minimal harness reduces guessing.

It gives the agent visible context, a recovery path, and a concrete definition of
what must be completed.
