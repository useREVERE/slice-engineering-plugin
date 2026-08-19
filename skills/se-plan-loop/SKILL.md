---
name: se-plan-loop
description: Generate, review, and refine a temp implementation plan from a ledger brief or conversation task with adaptive review depth. Use when a slice is plan-ready and needs a reviewed how before se-execute.
disable-model-invocation: false
---

# Plan Loop

Turn an accepted ledger brief or clear conversation task into a temp
implementation plan that is ready for `se-execute`. Success means the plan
is concrete, commit-sized, test-driven, risk-ordered, and reviewed at a
depth proportional to its complexity.

`se-plan` is an alias of this skill. There is one planning behavior.

## Inputs and Outputs

**Input:** Prefer a ledger arc and its current frontier slice. Fallback
inputs are an existing plan, a remediation item, or a clear conversation
task.

**Output:** A temp plan path from `mktemp`, review/refinement results, and a
readiness verdict. Plans are working memory; do not save new plans into the
repo unless the user explicitly asks.

Treat `$ARGUMENTS` as the ledger path, existing plan, task description, or
requested autonomy/review depth.

Start with a short update before tool calls. State autonomy and review tier
before writing or overwriting files.

Read `skills/_shared/bindings.md` and
`skills/_shared/agent-conventions.md` first.

## Autonomy

Default: **normal**.

- **guided:** Ground and outline; stop before overwriting or making unsettled
  trade-offs.
- **normal:** Generate, review, apply mechanical refinements, and ask about
  product/design decisions.
- **autonomous:** Continue review/refinement until ready, capped, or blocked
  by user judgment.

## Review Tier

Choose the lightest tier that protects the work:

- **Tier 1 - minimal:** obvious single-area additive work. Generate plan and
  skip formal review.
- **Tier 2 - structural:** default. Generate plan, run one `se-review-plan`,
  fix mechanical findings.
- **Tier 3 - full:** external service, durable data contract, new
  architecture, three or more subsystems, explicit uncertainty, or research
  notes that need verification. Review, refine, and re-review until ready or
  3 passes.

If the user asks for `full`, `deep`, or equivalent, use Tier 3.

Signals that force **Tier 3**:

- external API, service, OAuth, webhook, or SDK integration
- new table, migration with data transformation, or durable data contract
- new architectural pattern such as caching, background jobs, queues, or
  streaming
- three or more subsystems
- explicit uncertainty such as `TBD`, multiple options, or unresolved
  product/design trade-off
- research notes that materially affect the implementation approach and need
  verification

Signals that support **Tier 1**:

- purely additive behavior
- named existing pattern in one area
- no schema changes or external dependencies
- acceptance criteria concrete enough that the implementation path is obvious

Classification logic:

- **Any single Tier 3 signal forces Tier 3.** Don't weigh them; one is enough.
- **Tier 1 requires a clear pattern match** — the input must look like the
  Tier 1 signals, not merely lack Tier 3 signals. Absence of complexity is not
  presence of triviality.
- **When in doubt, Tier 2.** Unnecessary review costs latency; skipped review
  costs a bad plan locked in.

Calibration examples:

- "Add a `published_at` column to an existing resource, following the shape
  of `updated_at`" → **Tier 1**
- "Rework how ranking combines scores to emphasize recency over volume" →
  **Tier 2**
- "Add Stripe webhook handling for `subscription.updated` events" →
  **Tier 3** (external service integration)
- "Build a background job that nightly snapshots state into a new history
  table" → **Tier 3** (new table + new architectural pattern)

Announce the tier and the signals that drove it before proceeding, then
continue immediately; the user can redirect if they disagree.

## Grounding Budget

Read:

- provider grounding docs from `skills/_shared/agent-conventions.md`
- host `AGENTS.md`
- `knowledge_homes.guide` and `knowledge_homes.philosophy` via bindings
- the ledger arc, frontier slice, and referenced artifacts when present
- the conversation context, remediation item, or existing plan when that is
  the input
- files, prior artifacts, research notes, prototypes, or spikes referenced by
  the input

Use delegated exploration for independent codebase questions when it saves
time. Stop exploring when the plan can name relevant files, patterns, risks,
tests, and verification.

## Planning Discipline

Explore first, ask second. Resolve discoverable facts through the repo,
ledger, and referenced artifacts before asking the user. Ask only when the
answer is a product/design choice, a meaningful trade-off, or a genuinely
ambiguous candidate that cannot be resolved from available context.

Separate missing information into two passes:

- **Intent:** goal, success criteria, audience, scope, non-goals, constraints,
  and current state.
- **Implementation:** interfaces, data flow, edge cases, failure modes, test
  strategy, rollout/compatibility, and operational verification.

Treat the plan as **decision complete** when another agent can run
`se-execute` without inventing product behavior, interface policy,
sequencing, or test strategy. Record explicit assumptions and conservative
defaults chosen from repo patterns.

## Freshness Gate

Before planning from the current codebase, invoke `se-sync-worktree` with
the current task boundary so the plan reflects `origin/<default_branch>`.
This skill does not create worktrees. If sync stops because the tree is
dirty, do not stash or commit here: report the status and tell the caller to
run `se-settle-worktree`, then invoke this skill again from the beginning.
If the branch has unexpected divergence, stop rather than planning from
stale or rewritten context.

## Temp plan path

Create the plan in a named temp file and keep the exact path in working
memory. Choose a short, human-readable `PLAN_SLUG` (`lowercase-kebab-case`,
letters/numbers/hyphens only). Use `task` only when no meaningful name is
available.

Resolve `PLAN_DIR` from the Temp artifacts row in
`skills/_shared/agent-conventions.md` (Claude Code: `~/.claude/`; Cursor:
workspace temp or `.cursor/`; Codex: runtime temp). Create the directory if
missing. Do not guess `/tmp`.

```bash
PLAN_SLUG=short-task-name
PLAN_PATH=$(mktemp "${PLAN_DIR}/se-plan-${PLAN_SLUG}-XXXXXX")
printf '%s\n' "$PLAN_PATH"
```

Use the printed `PLAN_PATH` for every later reference, handoff, and summary.
Never report the literal template path as the plan path; it is only the
pattern `mktemp` expands. Keep `XXXXXX` at the end of the template for
BSD/macOS `mktemp` compatibility.

If an existing plan is provided, read it first. In guided mode, ask before
overwriting. In normal/autonomous mode, prefer creating a fresh temp plan and
preserve useful context where possible.

## Plan Contract

The plan covers the current slice only and should:

- reference the ledger arc or source brief instead of duplicating it
- for remediation, CI, eval, or test-infrastructure work, map each source
  finding to the specific failure mode the implementation will catch; if the
  proposed test or gate only proves wiring, naming, or plumbing, say so
  explicitly and do not present it as a behavioral or quality guarantee
- for a changed shared contract (identity, dedupe, validation, response, or
  persistence), inventory its producers, consumers, public entry points, and
  contract-facing docs/tests; state intended behavior for each, including
  deliberate non-goals and aliases
- name relevant files, interfaces, and existing patterns
- sequence commit-sized TDD steps
- include at least one falsifiable acceptance check for the promised
  behavioral, structural, or operational guarantee
- put risky assumptions and external dependencies early
- keep the codebase green after each step
- separate behavior changes from refactors and boy-scout cleanup
- show where each source acceptance criterion is covered by a plan step or
  verification check, flag deliberate deferrals, and name expected test areas
  for each step
- explain how it uses or departs from Research Notes or prototype learnings
- list explicit assumptions/defaults and unresolved user decisions, if any
- identify affected docs or ledger records, or state that none need updating
- end with verification commands and review handoff

If acceptance criteria or design decisions are missing, stop and ask rather
than inventing them.

## Refinement Rules

- Preserve the brief's intent.
- Apply mechanical findings directly in normal/autonomous mode. Mechanical
  means sequencing issues, TDD discipline, missing tests, step ordering,
  independence problems, or redundant data flow.
- Ask before product behavior, durable data model, compatibility, or
  irreversible interface decisions — anywhere reasonable engineers could
  disagree. Present design decisions grouped separately from mechanical
  issues and wait for the user's call before refining around them.
- If discovered coupling contradicts a source non-goal, surface a scope
  decision rather than preserving it mechanically.
- Record a short rationale for disagreed reviewer findings.
- When revising, produce one complete current plan instead of layered
  amendments that require the next agent to reconcile old and new
  instructions.
- Upgrade to Tier 3 if review exposes Tier 3 risk.
- For Tier 3, after convergence (not on cap-out), this plugin does **not**
  ship a second-opinion skill. Record `Second opinion: unavailable` unless
  the user names a host review to run instead. Do not pretend a second
  opinion ran.

## Output

```markdown
## Plan Loop Complete
- **Plan:** concrete temp path printed by `mktemp`, not the template pattern
- **Autonomy:** guided | normal | autonomous
- **Tier:** 1 | 2 | 3, with rationale
- **Review passes:** N
- **Second opinion:** unavailable | skipped | run (host-named), with reason
- **Status:** ready | ready with deferrals | blocked
- **Next:** se-execute, revise brief, or user decision
```

## Stop Rules

Stop when the brief is not plan-ready, refinement would materially change
the agreed slice, findings conflict in a way that needs judgment, or Tier 3
reaches 3 review passes without convergence.

$ARGUMENTS
