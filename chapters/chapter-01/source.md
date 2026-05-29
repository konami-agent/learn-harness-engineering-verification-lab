# Source Material

This repository is an executable verification companion to the Traditional Chinese Learn Harness Engineering course. It is not a mirror of the source material and does not replace the upstream course.

Read the course there. Run verification labs here.

## Primary upstream source

- Upstream repository: https://github.com/walkinglabs/learn-harness-engineering
- Course title: Learn Harness Engineering
- Language version: Traditional Chinese (`zh-TW`)
- Course URL: https://walkinglabs.github.io/learn-harness-engineering/zh-TW/
- Source tree: https://github.com/walkinglabs/learn-harness-engineering/tree/main/docs/zh-TW
- Verified page title: `歡迎來到 Learn Harness Engineering | Learn Harness Engineering`
- Verification date: 2026-05-28

## Chapter 01 upstream references

- Upstream Lecture 01 source: https://github.com/walkinglabs/learn-harness-engineering/tree/main/docs/zh-TW/lectures/lecture-01-why-capable-agents-still-fail
- Upstream Lecture 01 website: https://walkinglabs.github.io/learn-harness-engineering/zh-TW/lectures/lecture-01-why-capable-agents-still-fail/
- Upstream Project 01 guide: https://github.com/walkinglabs/learn-harness-engineering/tree/main/docs/zh-TW/projects/project-01-baseline-vs-minimal-harness
- Upstream Project 01 code: https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-01

The upstream Project 01 code already contains:

- `projects/project-01/starter/`: weaker harness / baseline scenario.
- `projects/project-01/solution/`: stronger harness scenario with `AGENTS.md`, `CLAUDE.md`, `init.sh`, `feature_list.json`, and `claude-progress.md`.

## Source references listed by the course

The course introduction lists these upstream references:

- OpenAI: Harness engineering: leveraging Codex in an agent-first world
- Anthropic: Effective harnesses for long-running agents
- Anthropic: Harness design for long-running application development
- Awesome Harness Engineering

## Public-repo citation policy

This repository should not copy the full course text.

Allowed:

- stable source URLs
- chapter titles
- short source-grounding notes
- concise paraphrases of source claims
- project-specific interpretations
- verification hypotheses derived from the source

Avoid:

- mirroring full pages
- storing long verbatim excerpts
- mixing source claims with our own engineering interpretations without labeling the boundary

## Traceability rule

Every verification artifact should eventually trace back to a row in `chapters/chapter-01/verification-map.md`.

For each chapter, distinguish:

1. Source claim: what the course appears to argue.
2. Project interpretation: how this repo translates the claim into an engineering proposition.
3. Verification hypothesis: what this repo can test or demonstrate.
4. Implemented artifact: the local validator, fixture, smoke manifest, or doc that embodies the test.
5. Confidence / open questions: whether the mapping is grounded enough to build on.

If a chapter is not yet source-grounded, its experiment or framework work should remain in design/review rather than being treated as completed evidence.
