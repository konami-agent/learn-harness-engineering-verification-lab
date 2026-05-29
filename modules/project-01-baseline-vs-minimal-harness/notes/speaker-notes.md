# Speaker notes: Project 01 module

## Session goal

Help learners experience Project 01 as a controlled comparison between a
prompt-only run and a minimal-harness run.

The facilitator should keep returning to this distinction:

- upstream course = canonical instructions;
- this module = slides and discussion prompts for teaching those instructions.

## Before the session

Prepare or confirm:

- access to the upstream Project 01 materials;
- one chosen agent for both runs;
- a clean repository state for both branches;
- a visible timer or turn limit;
- a place to record observations.

## Deck 01 facilitation

Main teaching move: do not start by saying "the model is bad." Start by showing
how many assumptions are hidden in a small software task.

Useful questions:

- What would a human new hire need before doing this task?
- Which of those things does the agent actually see?
- What does "done" mean for this Electron shell?

## Deck 02 facilitation

Main teaching move: present the harness as a small set of visible affordances,
not as a heavy framework.

Emphasize:

- `AGENTS.md` gives orientation;
- `init.sh` gives an executable recovery path;
- `feature_list.json` gives scope and completion expectations.

Avoid over-teaching later course mechanisms here. The point is a minimal useful
harness, not a complete harness platform.

## Deck 03 facilitation

Main teaching move: force comparison from evidence, not vibes.

If the improved run still fails, that is a good discussion point. Ask which
harness subsystem is still too weak rather than treating the project as a binary
success/failure demo.

## Suggested timing

- 10 minutes: Deck 01 and baseline framing.
- 20-30 minutes: baseline run or recorded-run review.
- 10 minutes: Deck 02 and improved-run setup.
- 20-30 minutes: improved run or recorded-run review.
- 15 minutes: Deck 03 comparison and reflection.

## Common pitfalls

- Changing the task prompt between runs.
- Giving the baseline hidden help.
- Fixing generated code manually before recording evidence.
- Treating the agent's final summary as proof.
- Turning the module into a line-by-line copy of the upstream project page.

## Closing question

What is the smallest harness artifact you would add to your own repository
before asking an agent to do real work?
