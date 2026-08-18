---
name: se-deliver
description: Orchestrate plan, execute, review-loop, ship, and reflect for one slice — or slice-by-slice across a ledger arc. Use when a brief or frontier is ready to implement and ship.
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

## Control flow

```text
se-plan → se-execute → se-review-loop → se-ship → se-reflect
```

Route from observed state:

| Observed state | Action |
| --- | --- |
| No accepted plan | `se-plan` |
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
