---
name: se-deliver-remediation-plan
description: Deliver every pending item in the tech-debt remediation plan, one se-deliver per item, until the queue is empty or a real blocker. Use after se-review-codebase, or when draining docs/tech-debt/remediation-plan.md.
disable-model-invocation: true
---

# Deliver Remediation Plan

Run `se-deliver` once per pending remediation item. This skill keeps the
queue honest; `se-deliver` still owns each item's phases and gates.

Success means every item that was pending at the start was delivered as
its own slice, reviewed, shipped under host bindings, and recorded back
in the plan per its "How to use this file" contract.

Treat `$ARGUMENTS` as a plan path, expected pending count, or autonomy
note. Default plan: `<knowledge_homes.debt>/remediation-plan.md`
(usually `docs/tech-debt/remediation-plan.md`).

Read `skills/_shared/bindings.md`,
`skills/_shared/agent-conventions.md`, host `AGENTS.md`, the engineering
guide, `se-deliver`, and the plan before starting.

When the harness cannot nest a skill call, compose `se-plan-loop` →
`se-execute` → `se-review-loop` → `se-ship` → `se-reflect` for that
item. Do not duplicate or weaken those skills.

## Goal Mode

If the harness exposes goal tools (Codex), create a goal: deliver every
item in the *initial* pending queue, one at a time, until that queue is
empty or blocked. Do not mark the goal complete because items were
skipped, deferred, renamed, or promoted from Deferred.

If goal tools are unavailable (Claude Code, Cursor), continue under the
same stop rules and report goal mode unavailable.

## Autonomy

Default: **autonomous** for clear pending items. Ask when queue shape,
item boundary, intended guarantee, verification, git state, or shipping
safety is ambiguous.

## Queue Inventory

Before delivering anything:

- Inventory `Pending Refactors` into a numbered queue. Preserve original
  titles and origin references
- Collect every item that requires a delivery-time user decision and
  surface them **once** before the first item
- If the user gave an expected count, require an exact match

If there are no pending items, or the count does not match, stop. Do not
manufacture work from deferred or completed entries.

## Per-Item Contract

For each pending item, in priority order:

1. Treat exactly one item as the `se-deliver` input.
2. Restate the exact guarantee the item promises. Treat every checkable
   claim (commands, paths, tests, premises) as unverified until confirmed
   against the current tree. Correct the item text where reality
   disagrees.
3. Require a falsifiable acceptance check that would fail if that
   guarantee were not met.
4. Run `se-deliver` in autonomous mode for that single item.
5. After a successful ship, update the plan per its Completing work
   section: leave the queue, current-cycle table row, full spec moved to
   `remediation-history.md`. Replace placeholders like `current change`
   with shipped short SHAs.
6. If the slice created an architectural precedent, update the guide/ADR
   in the same delivery or record an explicit follow-up.
7. If the premise is disproven, record Invalidated with the disproof and
   fold the missed check into `se-review-codebase` Phase 2 vetting in
   the same change, or record a follow-up. Invalidation is a
   review-process finding, not just a skipped delivery.
8. Refresh before the next item. `origin/<default_branch>` should point
   at the shipped commit. Fast-forward a primary checkout only when it
   is clean.

Do not batch items unless the user explicitly approves a merged scope.

## Acceptance Guardrails

Do not accept tautological evidence. Prefer tests that prove the
intended guarantee, not plumbing or self-injected round-trips.

For CI, harness, eval, or quality-gate items, require a negative control
or mutation-style check for the intended regression class.

If the slice can only deliver wiring, rescope the claim before marking
the item complete.

When a guard command conflicts with a good regression test, narrow the
guard rather than contorting the test.

When extracting a helper, enumerate new branches first. Each maps to an
existing caller spec or a new direct helper spec.

## Review Requirements

During `se-review-loop`, review the diff against the original pending
item and its origin review, not just internal consistency. A narrower
guarantee than the item claims is a finding.

## Queue Closure Audit

Before declaring the run complete, audit against current
`origin/<default_branch>`, not the local narrative:

- remote default-branch SHA matches the last shipped commit
- `Pending Refactors` is empty of the *initial* queue
- every initial item has a history entry with a shipped short SHA
  reachable from the default branch, or an explicit blocker/deferral
- CI conclusions for the run's final pushes; deploy probe if bound
- rerun machine-checkable guards on the remote default branch, scoped
  tightly enough to ignore history and tests that legitimately mention
  the old shape

## Stop Rules

Stop when the queue is empty or count-mismatched; an item is too broad
or not falsifiable; acceptance is tautological; plan-history movement is
missing after a supposed completion; `se-deliver` reports blocked;
verification fails; git state is unsafe; or the same blocker recurs.

Do not mark a goal complete. Report current item, completed items, the
blocker, and the next safest user decision.

If `se-ship` is rejected because the default branch advanced, follow
`se-ship`'s rebase/re-verify path and record the **final** shipped SHA.

## Output

```markdown
## Remediation Delivery Summary
- **Plan:** path
- **Goal mode:** active | unavailable | skipped, with reason
- **Autonomy:** guided | normal | autonomous
- **Initial pending queue:** titles/count
- **Completed items:** titles and SHAs
- **Current item:** delivered | blocked | skipped, with reason
- **Guarantee evidence:** acceptance checks and negative controls
- **Tests:** commands and results
- **Plan updates:** paths
- **Blockers/deferrals:** exact decisions
```

$ARGUMENTS
