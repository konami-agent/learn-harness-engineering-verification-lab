---
title: "Project 01 / Deck 03: Compare runs and extract lessons"
module: "project-01-baseline-vs-minimal-harness"
source: "walkinglabs/learn-harness-engineering"
---

# Project 01 / Deck 03

## Compare runs and extract lessons

Core question: how do we compare two agent runs without relying on vibes?

---

# The comparison rule

Keep the model and task stable.

Change the harness condition:

- baseline branch: prompt only;
- improved branch: minimal harness files prepared before the run.

The comparison is useful only if the constraints are visible and fair.

---

# Evidence to collect

For each run, collect:

- task prompt;
- time or turn limit;
- transcript or agent summary;
- final diff;
- startup command output;
- whether each required feature exists;
- any premature completion claim.

Do not fix the code after the run and then count the fixed state as agent output.

---

# Suggested comparison table

| Metric | Baseline | Minimal harness |
| --- | --- | --- |
| App starts? | | |
| Window present? | | |
| Document list present? | | |
| Q&A panel present? | | |
| Local data directory behavior? | | |
| Verification command run? | | |
| Premature completion? | | |
| Manual intervention needed? | | |

---

# Reading the result

Do not reduce the result to "model good" or "model bad".

Ask:

- Which failures were caused by missing task scope?
- Which failures were caused by missing startup instructions?
- Which failures were caused by missing verification?
- Which failures remained even with the minimal harness?

The last category is where deeper course topics begin.

---

# Reflection prompts

Ask learners to write 3-5 bullets:

1. What did the agent infer correctly in the baseline?
2. What did the baseline miss?
3. Which harness artifact helped most?
4. What was still unclear after adding the minimal harness?
5. What would you improve before running a longer project?

---

# What this project teaches

The project does not prove that every harness always improves every task.

It teaches a more practical habit:

> When an agent fails, inspect the task environment and feedback loop before
> blaming only model capability.

---

# Takeaway

Project 01 turns a slogan into a visible comparison:

same task, same agent, different harness support.

The learning comes from the evidence you collect and the failures you can name.
