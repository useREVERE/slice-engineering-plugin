---
name: se-compact-brief
description: Compact a multi-slice ledger brief after delivery by collapsing shipped specifications and stale context while preserving evidence, decisions, and its active or closed frontier. Use during delivery reflection, immediately before publish, or when a brief has accumulated obsolete history.
disable-model-invocation: true
---

# Compact Brief

Compact an evolving ledger arc so a fresh session can understand its
frontier without carrying the full specifications of work that already
shipped. An active arc must remain faithful to its recorded readiness.
A completed arc must remain a trustworthy historical record. Shortness is
useful only when it preserves the applicable job.

Run this after the just-shipped slice's reflection has been written and
before `se-publish`. Run it once more after final reflection when an arc
is closing. It may also be invoked explicitly against an accumulated
brief.

This is an ordinary file edit of the bound brief. There is no guarded
external writer in this plugin. Do not commit, push, publish, or archive.

Treat `$ARGUMENTS` as the brief path, caller-supplied compaction or
preservation directives, and any delivery slice, frontier, and reflection
context. Directives do not override the Preservation Contract or Material
Changes rules; ask on conflict.

Read `skills/_shared/bindings.md`. Resolve the brief under `ledger_root`
or `external_ledger_path`. If `ledger` is `none`, only compact a path the
user explicitly supplied.

## Central Test

First choose the mode from frontmatter and delivery state:

- **Active arc:** preserve the full active frontier so a fresh session can
  plan it confidently when ready, or identify the recorded gate or missing
  definition without inventing one.
- **Completed arc:** preserve the exact closed frontier and enough history
  to reconstruct what shipped, what proved it, what remains unverified, and
  where follow-on work belongs. Do not invent an active frontier.

In either mode, keep a fact when a fresh session would need it to:

- understand why the arc and its frontier matter;
- plan an active frontier without rediscovering a constraint or settled
  decision;
- distinguish delivered capability from proposed behavior;
- recover delivery evidence or understand a hypothesis outcome; or
- avoid repeating a failed approach, violating an unresolved prerequisite,
  or mistaking an operational evidence gap for unfinished implementation.

Everything else is a candidate for removal or condensation. Do not
optimize for a fixed word or line count.

## Preservation Contract

Preserve:

- frontmatter status and the exact active or closed `frontier`;
- the current problem, outcome, and hypothesis needed to judge frontier
  edge cases;
- for a plan-ready frontier, its complete behavior, acceptance criteria,
  done signal, and explicit exclusions; for a gated or directional
  frontier, its owner, prerequisites, resolution or parking condition, and
  no-build boundary without inventing missing specification;
- for a closed frontier, unresolved operational evidence separately from
  implementation status;
- unresolved decisions, prerequisites, ownership boundaries, and deferrals
  that still constrain the frontier; retain their owner or label them
  `unowned`, and preserve unresolved alternatives without choosing one;
- future slices at their current level of commitment;
- one compact delivery record per shipped slice containing the shipped date
  and SHA, delivered contract, grounded evidence summary, hypothesis
  outcome, next-slice verdict, and durable learnings needed later;
- durable contract semantics that affect callers or operators, including
  numeric defaults and windows, eligibility boundaries, lifecycle effects,
  idempotency, retry behavior, exact operator invocation shapes when they
  are the supported interface, and typed error or command exit semantics;
- the hypothesis's recorded status, including when a slice used acceptance
  criteria instead of a hypothesis or when an arc-level premise remains
  untested;
- negative knowledge as a compact chain: observed failure or limitation,
  current mitigation, accepted residual risk, escalation trigger, and
  whether that trigger remains prospective or was already satisfied; and
- links to an existing changelog, ADR, SOP, or owning arc when it is now
  the authoritative home.

Do not rewrite the frontier's meaning under the banner of compaction. Do
not turn an acceptance criterion into evidence that it passed. Attribute
evidence as an empirical observation, named test coverage, executed test
result, deployment check, or operational record; when the source does not
record proof, say `not recorded` rather than infer it. Do not add temporal
or causal framing the source does not support.

## Compaction Candidates

Collapse or remove material when its useful content survives elsewhere in
the brief or an authoritative linked document:

- full behavior and acceptance specifications for shipped slices;
- test-by-test, deploy-by-deploy, or prototype evidence already summarized
  in a delivery record;
- settled prototype comparisons and rejected cosmetic alternatives;
- design decisions and exclusions that constrain only shipped behavior;
- stale implementation research, old line numbers, and source-shape notes a
  frontier planner no longer needs;
- superseded assumptions and queue language, retaining a short explanation
  only when the change itself informs the frontier;
- named learnings only after classifying them as irrelevant to this arc,
  superseded, or relocated to a linked authoritative home;
- shipped capability prose duplicated in the host shipped changelog; and
- deferred ideas that already have a clear owning arc.

Do not create a new document merely to make the current one shorter. A
future slice that now represents a different coherent outcome may deserve
its own parked arc, but moving it changes queue and ownership boundaries:
report that candidate and require confirmation.

## Workflow

1. Read the entire brief cold. Choose active or completed mode. Classify an
   active frontier as `plan-ready`, `gated`, or `directional`. Identify
   shipped slices, later slices, unresolved evidence and decisions,
   ownership, and references to authoritative homes. Stop if the frontier
   or delivery state is contradictory.
2. Record the current line and word count. Inspect `git status` / diff for
   the brief path. **Stop if the brief file is already dirty with edits
   that are not this compaction** — do not overwrite unrelated work.
3. Build a temporary keep/collapse/remove inventory. Classify every caller
   directive as `apply`, `defer`, or `blocked`, explaining the latter two.
   For each shipped slice, separately inventory (a) contract statements
   from the shipped specification, (b) evidence stated in its delivery
   record, and (c) verification required by the specification but absent
   from the delivery record. Label contract summaries as
   specification-derived when that is their source, and record missing
   required proof as `not recorded`. Do not infer an executed test category
   from planned coverage. Classify each hypothesis as supported, refuted,
   inconclusive, or not tested from the recorded outcome. For each
   removal, classify it as `duplicated elsewhere`, `superseded`, `shipped
   specification`, or `no longer constrains frontier`. Classify every named
   learning as kept, irrelevant, superseded, or authoritatively relocated.
4. Write the complete compacted document in one replacement of the brief
   file. Keep the complete intended document in working context so a
   concurrent edit is visible in `git status` / diff before you save.
   Prefer compact prose over moving historical bulk into another section.
   Preserve the document's established voice and structure where useful.
5. Audit the diff against the Preservation Contract:
   - frontmatter and frontier still agree, whether active or closed;
   - the active frontier's behavioral contract or recorded gate is
     unchanged, or the completed arc's delivered contracts remain
     historically reconstructable;
   - every shipped slice retains a sufficient delivery record;
   - specification-derived contracts remain distinct from recorded
     evidence, and required-but-unrecorded verification remains explicit;
   - contract thresholds, lifecycle effects, retry, supported invocation,
     typed error, and exit semantics remain;
   - every evidence claim has source-appropriate provenance;
   - hypotheses retain their recorded tested or untested status without an
     unsupported outcome;
   - negative knowledge retains mitigation, residual risk, escalation
     trigger, and the trigger's prospective or already-satisfied state
     where the source supplied them;
   - every unresolved decision, owner, alternative, and relevant
     prerequisite remains;
   - every explicit caller directive was applied or is explicitly deferred
     or blocked;
   - no new product decision, acceptance criterion, or ownership boundary
     was introduced, and no unsupported temporal or causal claim was added;
     and
   - unrelated pre-existing edits remain untouched.
6. Record the resulting line and word count. Do not report ready until
   every caller directive is applied or has a recorded block. The caller
   must run `se-review-brief` cold before `se-publish`.

## Material Changes

Compaction is mechanical when it removes duplication or condenses settled
history without changing meaning. Stop and ask before:

- changing the frontier, slice order, acceptance criteria, exclusions,
  hypothesis, or definition of done;
- moving a future slice or deferred idea to a new or different arc;
- deleting an unresolved decision, operational prerequisite, delivery SHA,
  or hypothesis outcome;
- replacing a durable decision with an inference from current code; or
- reconciling contradictory history by choosing one account.

When safe compaction can proceed around a material question, leave the
questioned content unchanged and report it separately.

## Output

Report:

- brief path, mode, and unchanged active or closed frontier;
- before/after line and word counts;
- shipped sections compacted;
- authoritative links retained;
- unresolved decisions and later slices preserved;
- explicit caller directives applied, deferred, or blocked, with reasons;
- material split or deletion candidates left untouched; and
- whether the brief is ready for a cold `se-review-brief`.

## Stop Rules

Stop without editing when the artifact does not identify a trustworthy
active or closed frontier, shipped status cannot be reconciled, the brief
file is already dirty with unrelated edits, or compaction would require a
product or ownership decision. Stop after safe partial compaction when
only a material candidate remains. Never publish, commit, push, archive,
or modify the application repository as part of this skill except the
named brief file.

$ARGUMENTS
