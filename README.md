# Learn Harness Engineering Slide Board

This repository is a project-driven slide board for
[`walkinglabs/learn-harness-engineering`](https://github.com/walkinglabs/learn-harness-engineering).

The upstream project is the canonical course: lectures, projects, examples, and
learning sequence live there. This repository is a presentation companion for
study groups, workshops, and project walkthroughs.

It is not a replacement for the upstream course. Read and use the upstream
materials first; use this repository when you want to teach, review, or present
the ideas through project-centered slide modules.

## Repository role

Upstream course:

- explains Harness Engineering concepts;
- provides lectures in Traditional Chinese and English;
- provides hands-on projects and code examples;
- remains the source of truth for curriculum and exercise details.

This slide board:

- reorganizes course material around upstream projects rather than one deck per
  lecture;
- turns each upstream project into a teaching module;
- splits each module into the number of slide decks needed for the project's
  concepts, workshop phases, and reflection points;
- keeps speaker notes and facilitation prompts close to the decks.

## Why project-driven modules?

Lectures are knowledge input. Projects are skill output.

A one-to-one lecture deck can easily become a rewritten article. A project-driven
module instead asks: what does a learner need to understand, do, and discuss in
order to complete this project well?

That means one upstream project may use concepts from several lectures, and the
number of decks in a module is determined by the learning path, not by the
upstream chapter count.

## Current modules

Start here:

- [`modules/project-01-baseline-vs-minimal-harness/`](modules/project-01-baseline-vs-minimal-harness/) — teaching module for upstream Project 01.

Project 01 deck sequence:

1. [`01-problem-framing.md`](modules/project-01-baseline-vs-minimal-harness/decks/01-problem-framing.md) — why capable agents still fail.
2. [`02-minimal-harness.md`](modules/project-01-baseline-vs-minimal-harness/decks/02-minimal-harness.md) — what the minimal harness adds.
3. [`03-comparison-and-reflection.md`](modules/project-01-baseline-vs-minimal-harness/decks/03-comparison-and-reflection.md) — how to compare runs and extract lessons.

## Repository layout

- `modules/` — project-driven teaching modules.
- `modules/TEMPLATE.md` — reusable module template.
- `docs/module-design.md` — module design rules and boundaries.
- `archive/verification-lab-prototype/` — archived material from the previous verification-lab prototype.

## Working convention

For each new upstream project module:

1. Create a folder under `modules/`.
2. Fill in `module.md` using `modules/TEMPLATE.md`.
3. Add only the decks needed to teach that project.
4. Keep source links to the upstream course.
5. Keep this repository as a slide board, not a duplicate textbook.

## Source

- Upstream course repository: https://github.com/walkinglabs/learn-harness-engineering
- Upstream Project 01: https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-01
- Project 01 lecture/project page: https://walkinglabs.github.io/learn-harness-engineering/zh-TW/projects/project-01-baseline-vs-minimal-harness/
