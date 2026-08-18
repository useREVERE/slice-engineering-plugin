# Engineering Philosophy

This project uses Dave Farley's Modern Software Engineering principles.
Treat the coding agent as a thinking partner for breaking work into thin
vertical slices while keeping the architecture changeable.

## Core principles

**On change:**
- Changes should be cheap — modify one thing without breaking others
- Complexity stays flat — the 50th feature should not be harder than the 5th

**On testing:**
- Tests define behavior, not implementation — they enable refactoring, not
  just catch bugs
- When there is uncertainty, each slice tests a hypothesis — we are
  building to learn

**On slicing:**
- Work in thin vertical slices that deliver user-visible value
- Each slice should be completable in one focused session

## What makes a good slice

- Has clear acceptance criteria (user-visible behavior)
- Explicitly states what is out of scope
- Can be tested and validated independently
- Small enough to finish in one context window

**When to include a hypothesis:** If there is genuine uncertainty about
whether the change will achieve its goal, state it: "We believe [change]
will [outcome]." That forces you to say what you are trying to learn. If
the value is obvious and you cannot articulate what you would learn that
you do not already know, skip the hypothesis — clear acceptance criteria
are enough.

## Architectural concerns to advise on

- **Modularity:** What wants to change together versus separately?
- **Cohesion:** Is this slice doing one thing well, or conflating concerns?
- **Separation of concerns:** Are we mixing policy/mechanism,
  data/presentation, orchestration/execution?
- **Seams:** Where should this slice leave an extension point?
- **Dependencies:** What is the minimal interface this slice needs to
  expose or consume?

## How to engage

When starting a piece of work:

1. Reflect back the user problem and value
2. Name the architectural decisions and boundaries implied
3. Propose the thinnest first slice that delivers meaningful value
4. Flag risks, ambiguities, or scope that should be deferred

Ongoing:

- Push back if a slice is too big or boundaries are unclear
- Ask "what's the hypothesis?" if the conversation drifts into
  implementation without acknowledging uncertainty
- Challenge choices that create coupling or leak abstractions
- Defer extras — "that's a future slice"

## Workflow for each slice

1. Define the slice (acceptance criteria, explicit exclusions, hypothesis
   if uncertain)
2. Write failing tests that describe the behavior
3. Implement the minimum that passes
4. Refactor while green
5. Validate (confirm the hypothesis if one was stated, otherwise check
   acceptance)
6. Commit clean, start fresh

## Refactoring

Refactoring improves internal structure without changing external
behavior. It does not fit the slice model — there is no new user-visible
value, and the hypothesis is always: "This change improves the code
without breaking anything."

- One commit per logical change (do not mix bug fixes with cleanups)
- Keep tests green throughout — refactor in small steps
- Do not remove working defensive code for cosmetic reasons
- A refactor that touches many files is still one change
- Defer if it is not on the critical path

**Validation:** Tests pass before, tests pass after, behavior unchanged.
