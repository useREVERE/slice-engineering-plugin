---
name: se-plan
description: Generate, review, and refine a temporary implementation plan for one briefed slice. Use when the brief is plan-ready and the how is not yet sequenced.
disable-model-invocation: false
---

# Plan

Turn a plan-ready brief into a throwaway implementation sequence. Success
means each step is independently committable, risks surface early, and the
plan does not re-justify the work.

Treat `$ARGUMENTS` as the brief path, conversation task, or autonomy note.

Write the plan to a temp file (`mktemp` or the host's temp directory). Do
not commit it. Do not store it under the ledger unless the user explicitly
asks to keep a spike.

## Autonomy

Default: **normal**. Refine once after a self-review. Stop when sequencing
works, not when every alternative ordering has been considered.

## Grounding

Read the brief (or conversation brief), host `AGENTS.md`, and only the code
needed to name real modules and tests. Read
`skills/_shared/bindings.md` for `verify_command` and `default_branch`.

Invoke `se-challenge-scope` when the first draft adds tables, abstractions,
or configuration systems that the slice does not need.

## Plan shape

For each step:

- the behavior or refactor outcome
- the failing test or characterization that specifies it (or why the step
  is docs-only / mechanical)
- the code likely to change
- a commit boundary
- the smallest verify command (prefer a focused subset of `verify_command`)

Put the riskiest unknown in an early step. Do not defer integration to the
end. Do not bundle a boy-scout refactor into a behavior step.

## Convergence

Act on: steps that cannot be tested or committed alone, risks deferred to
the end, coupled steps that should be split.

Note but do not loop on: equally valid orderings, stylistic step wording.

Signal: **the sequencing works**.

## Output

Temp plan path, step count, first-step verify command, and whether
`se-deliver` / `se-execute` can start.
