---
name: se-review-codebase
description: Recurring Farley-lens codebase review that writes a dated report and updates the tech-debt remediation plan after a pause. Use weekly or on a cadence to keep the codebase changeable, and when the user asks to review the whole tree or what changed since the last sweep.
disable-model-invocation: true
---

# Review Codebase

Assess how safely and quickly this system can be changed. Judge against
the product's actual stage — do not apply enterprise ceremony to a small
codebase, and do not excuse sloppiness as "moving fast."

This skill does not modify application code. It produces:

1. A dimensional assessment in the conversation
2. A dated report under `knowledge_homes.debt` (default `docs/tech-debt/`)
3. An updated `remediation-plan.md` in that same home — **only after**
   the Phase 3 pause

Treat `$ARGUMENTS` as scope ("frontend", "since last review", "full") or
an explicit debt-directory override.

Read `skills/_shared/bindings.md` and
`skills/_shared/agent-conventions.md`. Resolve the default branch, verify
command, ship mode, and `knowledge_homes.debt`. If `config.yaml` is
missing, continue with `docs/tech-debt/` and git-derived `main`, and say
so.

Start with a short update stating the Phase 1 scope boundary.

## Phase 1: Exploration

**Pin the review anchor.** Fetch origin. Fast-forward to
`origin/<default_branch>` when the tree is clean (`git merge --ff-only`).
If the checkout has diverged, stop. Record the anchor SHA — the report
Scope line and every new entry's `As-of` cite it.

**Calibrate to cadence.** If `remediation-plan.md` or a dated review
exists and is recent, this run is *incremental*:

- Explore what changed since that review (`git log` / `git diff`), plus
  the changed modules' integration points
- Verify the last cycle's refactors held. Where a pending entry has an
  `As-of` SHA, run `git diff <sha>..HEAD -- <files>` and re-confirm
  moved files against current source. A reintroduced problem is a finding
- Check whether recorded promotion triggers fired without action
- Trace one or two recent changes from intent through files, tests, and
  verification to test locality, feedback speed, and reversibility

Fall back to a full sweep when there is no recent review, it was long
ago, or changes since then are pervasive. Honor an explicit user scope.

**Explore with the exploration-tier subagents** from Agent Conventions.
Require file paths, line numbers, and excerpts. Do not default to the
lead model for this pass.

**What to look at:**

- Application code (detect `src/`, `app/`, `lib/`, or the host's tree)
- Tests and test harness
- Config, CI, deploy manifests, task runners
- Host docs (`AGENTS.md`, engineering guide, ADRs, philosophy)
- **The debt home first** — pending, deferred triggers, invalidated
  entries, prior dated reviews — so tracked or deliberately deferred
  issues are not rediscovered

**Empirical delivery evidence.** Collect what already exists: test
timings, CI *run conclusions* (not just workflow YAML), recent
regressions, deploy/rollback evidence. `gh run list --branch
<default_branch>` before asserting a gate works. Do not create a metrics
program. Label unavailable evidence as unavailable.

**Evidence budget.** Every substantive observation carries location
(`path:line`), a sentence of why it matters, dimension(s), and valence:
earning its keep, problem, or **watch item** with a named revisit
trigger.

## Phase 2: Aggregate and Verify

Draft prioritized candidates: one-line problem and fix, plus
high/medium/low confidence. Order by leverage discounted by confidence.
Separate a small **active tier** (why now, not merely cleaner) from
lower-priority findings.

**Vet before you list.** Re-read cited code. Drop anything already
mitigated or ungroundable.

**Dead-code claims need a deployment-surface check.** Application
callers are not enough. Grep CI workflows, deploy manifests, task
runners, and package-script entry points before asserting something
never runs.

**Refute destructive claims.** Any "dead / unused / zero callers /
never runs" finding gets a fresh-context refuter on the adversarial
judgment tier before it may enter the candidate list. Ungrounded either
way → low confidence; refuted → drop or reclassify.

**Challenge survivors.** Persist the full candidate packet (evidence,
paths, excerpts) to a temp file via Agent Conventions, then run
`se-challenge-scope` in fresh context against that file. Apply verdicts.
**Every cut or deferral records a named promotion trigger.**

**Correctness bugs are not refactors.** Call them out first and route
them through `se-deliver` / `se-investigate`, not the remediation queue.

**History claims need hunk-level evidence.** "X since commit C" cites
the hunk (`git log -p -S` — read the hunk, not the subject) or
`git show <sha>:<file>`.

**Duplicate-looking writes need reachability and condition.** Same
assignment at two sites is not redundant unless both are reachable from
the same callers *and* fire under the same conditions.

**Redundant-test claims need an exercise diff.** Compare fixtures,
injected dependencies, and parametrization, not names.

**Symbol-move lists follow ownership and import direction**, not a
shared name prefix.

If there are no significant structural issues, say so. Still write the
dated report. Skip only the plan update.

## Phase 3: Present and Pause

Present:

- **Dimensional assessment** (both sides, grounded in Phase 1 evidence).
  Depth proportional to evidence. "No meaningful new evidence" is valid
  on an incremental run.

  1. Comprehensibility
  2. Locality of Change
  3. Feedback Loops
  4. Reversibility
  5. Accidental Complexity
  6. Implicit Dependencies
  7. Test Quality

- **Emergent themes** that do not fit one dimension
- **Trajectory** since the previous review
- **Synthesis** — one honest paragraph, not a grade
- **Post-challenge candidate list** with confidence, plus the challenge
  record (cut / merged / deferred-with-trigger / strengthened)
- Bugs, ledger-delegated items, and watch items, separately

Own triage. Present confident dispositions as **decisions made**. Ask
only for a real product decision, a hard-to-reverse data-model change, a
destructive action the refuter could not ground, or genuinely low
confidence with expensive unwind.

**Then stop. End the message and wait.** Do not write the report or
touch the remediation plan before they respond.

## Phase 4: Write the Dated Report

Re-sync: fetch again. If `<default_branch>` moved past the anchor, diff
`<anchor>..origin/<default_branch>` against cited files and drop or
refresh invalidated items.

Write `<debt>/YYYY-MM-DD-codebase-review.md`. If that name exists, use
`-2` or a scoped slug. Analytical findings and decisions only —
refactor entries go in the plan.

````markdown
# Codebase Review — Month Day, Year

**Created:** YYYY-MM-DD
**Source:** Comprehensive codebase review (Dave Farley assessment dimensions)
**Assessor:** {provider} ({model})
**Scope:** full codebase | incremental since {ref} | {user-provided scope}
**Codebase size:** ~{N} lines of application code, {N} tests
**Context:** {one sentence}

## Relationship to Existing Tech Debt
## Assessment Summary
## Delivery Evidence and Trajectory
## Dimensional Findings
## What's Earning Its Keep
## What's Not Earning Its Keep
## Scope-Challenge Record
## Watch Items
````

## Phase 5: Update the Remediation Plan

Only after the pause (go-ahead, corrections, or decisions delegated
back), and only with entries that survived refutation, challenge, and
overrides.

If `remediation-plan.md` is missing, copy
`templates/docs/tech-debt/remediation-plan.md` first. Its "How to use
this file" section is the queue contract — do not restate it here.

Route each surviving structural finding to pending, delegated to ledger
work (user approval, named arc), deferred with a named trigger, or
invalidated. Watch items stay in the dated report.

**A verification command is only a guard if it discriminates.** Run it
on the anchor tree, record what it returns now, and state what it must
return after the fix. A command that is green before and after is a
false proof.

Hold new entries to the plan's format (Problem, Fix, Files, Edge cases,
Verification, Origin, As-of). Grep current import/usage sites before
writing "Files to change." Integrate into priority order and renumber
pending items. Update "Last updated" and Source reviews. Do not edit
completed records or duplicate tracked items.

Commit **only** the dated report and the plan (plus history file if the
contract requires moving a completed spec). Explicit pathspec — never
`git add -A`. Concurrent dirty or staged work is possibly-intentional;
leave it untouched. Publish with `se-commit` then `se-ship` (docs-only
rationale is valid). Confirm CI conclusions on `<default_branch>` before
declaring the cycle closed.

## Agent Conventions

- Exploration subagents: exploration tier. Refuter and `se-challenge-scope`:
  adversarial judgment tier.
- Temp packet: the runtime's approved temp, not a guessed `/tmp`.
- Assessor label: provider and model from the harness.

$ARGUMENTS
