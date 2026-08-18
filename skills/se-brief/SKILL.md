---
name: se-brief
description: Draft a conversation-scoped quick brief or a durable ledger brief for one thin vertical slice. Use when shaping what to build, starting a slice, or refining an existing brief.
disable-model-invocation: false
---

# Brief

Understand the codebase and the problem at a depth proportional to the
change, then produce a brief an implementation session can use without
re-deriving the why.

You do not write application code. Explore, decide, and write the brief.

Treat `$ARGUMENTS` as the topic, an existing brief path, or a refinement
focus. Resolve it before exploring. When it names an existing brief, update
that artifact rather than creating a replacement.

Read `skills/_shared/bindings.md` before writing a durable brief.

## Autonomy

Default: **normal**.

- **guided:** draft in conversation; do not write a ledger file unless asked.
- **normal:** write or update the brief when the slice is clear; run
  `se-review-brief` and apply mechanical fixes; ask only about product scope.
- **autonomous:** continue brief → review-brief until plan-ready or blocked.

## Lane

### Quick brief

Stay in the conversation when all of these are true:

- one clear user- or developer-visible behavior
- concrete acceptance criteria and explicit exclusions
- the change matches an existing pattern and fits one session
- no cross-session coordination or delivery record is needed

### Durable ledger brief

Use a ledger arc when any of these are true:

- more than one slice
- work must survive this session
- more than one agent will pick it up
- a delivery record is wanted

Honor the host `ledger` binding. If `ledger` is `none`, stay in conversation
and say why. If the binding file is missing and a durable brief is required,
stop and tell the user to run `/se-setup`.

## What a brief contains

- **Why** this slice now
- **Outcome** in user-visible terms
- **Acceptance criteria** that can be checked after ship
- **Exclusions**
- **Hypothesis** only when the value is genuinely uncertain
- **Frontier** — the one next slice — when the brief is a multi-slice arc

Do not prescribe implementation. Do not smuggle a plan into the brief.

Use `templates/ledger/arc-brief.md` for durable arcs. Slug the directory from
the outcome, not the implementation idea.

## Shape the slice

If the request is larger than one session, split it and put only the first
increment on the frontier. Invoke `se-challenge-scope` when the proposal
looks over-built.

Ground in the host's `AGENTS.md`, `docs/engineering-philosophy.md`, and
`docs/engineering-guide.md` when those files exist. Search the codebase
for the existing seam before inventing a new one.

## Output

For a quick brief, write the brief in the conversation under a clear heading.
For a durable brief, write `<ledger_root>/arcs/<slug>/brief.md` and report
the path, the frontier name, and whether it is plan-ready.
