---
name: se-review-loop
description: Run fresh-context review, address valid findings, and re-review until ship-it or a bounded stop. Use after implementation and before shipping.
disable-model-invocation: true
---

# Review Loop

Create an unbiased review / fix / re-review cycle. Success means valid
findings are fixed and tested, invalid findings are explained, and the loop
converges on `ship it` or a clear stop.

Treat `$ARGUMENTS` as diff scope, autonomy, or prior-review context.

Read `skills/_shared/bindings.md` and
`skills/_shared/agent-conventions.md`.

## Autonomy

Default: **normal**.

- **guided:** review and triage only.
- **normal:** review, fix valid findings, test, commit via `se-commit`.
- **autonomous:** continue until `ship it`, 3 fix rounds, or a blocker.

## Scope

Default to the full branch vs `origin/<default_branch>` after
implementation. Fetch first. If fetch fails, stop rather than reviewing a
stale baseline.

## Passes

1. Local fresh-eyes pass over every changed file. Fix obvious issues when
   autonomy permits, then look again once.
2. Delegated `se-review` in fresh context when the harness can. Pass only
   the scope, prior findings, and review instructions — not the
   implementation story.
3. Triage: act on correctness, unclear intent, missing coverage, hidden
   coupling, broken host conventions. Note preferences. Do not loop on them.
4. Fix, verify with the smallest relevant tests, commit.
5. Re-review the new diff with prior-review context.

Stop at `ship it`, 3 fix rounds, or a product/design disagreement that
needs the user.

## Output

Verdict, rounds used, fix commits, residual notes, and whether `se-ship`
may start.
