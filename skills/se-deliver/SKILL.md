---
name: se-deliver
description: Orchestrate plan-loop, execute, review-loop, ship, and reflect for one slice — or slice-by-slice across a ledger arc. Use when a brief or frontier is ready to implement and ship.
disable-model-invocation: true
---

# Deliver

Run the standard delivery workflow. Each component skill is the source of
truth. Do not duplicate or weaken its gates.

Success means the requested slice is planned, implemented, reviewed, shipped
under host bindings, and reflected when a ledger is in use.

Treat `$ARGUMENTS` as the brief path, frontier name, conversation task, and
any autonomy or slice-boundary ("first slice only").

Read `skills/_shared/bindings.md` and
`skills/_shared/agent-conventions.md` before routing.

## Autonomy

Default: **normal**.

- **guided:** stop before edits, commits, shipping, or reflection writes.
- **normal:** run clear phases; ask for product judgment, unsafe git state,
  or irreversible choices.
- **autonomous:** continue through reflection until delivered or blocked.

## Invariants

- Follow each component skill.
- Stop on failing verification, unsafe git state, or unresolved product scope.
- An explicit user boundary overrides multi-slice continuation.
- Production or integration acceptance precedes reflection.
- Reflection precedes declaring a ledger slice complete.
- Do not create worktrees unless bindings set `worktrees: true`.

## Freshness

If the checkout may be stale, invoke `se-sync-worktree` before planning.
If sync stops because the tree is dirty, invoke `se-settle-worktree` only
when the changes are task-owned, then rerun `se-sync-worktree` from the
beginning. Do not stash inside this orchestrator.

When `worktrees: true`, the primary checkout should already have been
prepared with `se-prep`; this skill still does not create worktrees. After
ship, `se-tidy-worktree` is opt-in cleanup of the current task worktree —
do not run it unless the user asked and every tidy safety check passes.

When `worktrees: false`, do not run `se-prep` or `se-tidy-worktree` as
mandatory phases.

## Control flow

```text
se-plan-loop → se-execute → se-review-loop → se-ship → se-reflect
```

`se-plan-loop` runs `se-review-plan` at the tier that protects the work.
`se-plan` is an alias of `se-plan-loop`; do not use a lighter planning
path.

Route from observed state:

| Observed state | Action |
| --- | --- |
| No accepted plan | `se-plan-loop` |
| Plan ready, implementation absent | `se-execute` |
| Implementation present, review not converged | `se-review-loop` |
| `ship it`, clean tree | `se-ship` |
| Shipped slice | Verify acceptance, then `se-reflect` if a ledger is bound |
| Ledger `none` or conversation brief | Reflect in conversation; do not invent a ledger |

When the input is a ledger arc, deliver the slice named by its `frontier`.
Reconcile that name against the delivery record and git. Stop if they
disagree. Do not silently pick a different slice.

After a successful slice, continue to the newly exposed frontier only when
it is already plan-ready and the user did not limit the run to one slice.
If the next frontier needs shaping, stop with a `needs shaping` handoff.

## Output

Phase reached, evidence (commits, verify, ship result), remaining frontier,
and any user decision that blocked progress.
