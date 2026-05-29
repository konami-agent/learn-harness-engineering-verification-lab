# Project-driven module design

This repository organizes teaching material by upstream project, not by upstream
lecture number.

## Principle

Each module corresponds to one `walkinglabs/learn-harness-engineering` project.
The module's deck count is decided by what a learner must understand and do to
complete that project, not by how many lectures mention the topic.

## Module responsibilities

A module should provide:

- a source-grounded reference to the upstream project;
- learning outcomes for the workshop or study session;
- the lecture concepts needed for the project;
- a deck breakdown with one core question per deck;
- speaker-note prompts for discussion and facilitation;
- a concrete learner deliverable.

A module should not:

- copy the full upstream project text;
- become an independent replacement for the upstream course;
- add verification-lab validators or claim-coverage systems;
- introduce export/build tooling before the slide content needs it.

## How to decide deck count

Use this rule of thumb:

```text
deck count = 1 problem-framing deck
           + 1..N mechanism or preparation decks
           + 1 comparison / reflection / walkthrough deck
```

Add a deck only when it answers a distinct teaching question. If two slides can
be taught in the same discussion without overloading the learner, keep them in
one deck.

## Recommended deck shape

Each deck should be short enough for a focused teaching segment:

1. title and learning question;
2. concrete failure story or project context;
3. core concept;
4. diagram or structured model;
5. practical checklist;
6. bridge to the project step;
7. takeaway.

## Source boundary

The upstream course remains canonical. This repository may reorganize and
summarize material, but every module should point learners back to the upstream
project and lectures for full details.
