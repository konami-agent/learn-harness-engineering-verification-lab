---
title: "Project 01 / Deck 01: Why capable agents still fail"
module: "project-01-baseline-vs-minimal-harness"
source: "walkinglabs/learn-harness-engineering"
---

# Project 01 / Deck 01

## Why capable agents still fail

Core question: why can a capable coding agent still fail a simple project?

---

# The project task

Build a minimal Electron knowledge-base shell:

- a window starts;
- the left side shows a document list;
- the right side shows a Q&A panel;
- the app creates and uses a local data directory.

The product slice is intentionally small. The real experiment is how we ask the
agent to complete it.

---

# The trap

A strong model can still fail because the task environment is under-specified.

Common failure symptoms:

- plausible code that does not start;
- missing required UI regions;
- no local data directory behavior;
- agent claims completion before running the app;
- final summary sounds confident but lacks evidence.

---

# Capability is not reliability

Model capability answers:

> Can the model, in principle, produce the right kind of solution?

Engineering reliability asks:

> Can this run produce, verify, and hand off the expected result under real
> constraints?

Project 01 compares these two questions.

---

# Baseline run

In the first run, the agent receives only the task prompt.

No extra repository structure:

- no `AGENTS.md`;
- no `init.sh`;
- no `feature_list.json`;
- no explicit completion contract.

The baseline asks: what does the agent infer on its own?

---

# What to watch during baseline

Look for missing harness signals:

- Does the agent discover how to start the app?
- Does it know the expected feature list?
- Does it run the app before claiming completion?
- Does it record evidence or just summarize?
- Does it spend time rediscovering basic project facts?

---

# Discussion prompt

Before showing the improved run, ask learners:

1. Which failures are model mistakes?
2. Which failures are missing instructions?
3. Which failures are missing executable checks?
4. Which failures would a better repository setup prevent?

The point is not to excuse the model. The point is to locate the engineering
boundary.

---

# Takeaway

A capable agent needs a harness to become a reliable engineering component.

Project 01 starts with the weakest useful condition: same task, same agent, but
only a prompt.
