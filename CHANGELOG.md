# Changelog

## 0.5.0

Plan readiness, ledger lifecycle, worktree hygiene, and a Claude wrapper.

- `/se-review-plan` — Farley verdict (`ready` / `ready after minor edits` /
  `not ready`) plus `/se-challenge-scope`
- `/se-plan-loop` — adaptive review tiers; `/se-plan` is now an alias
- `/se-deliver` runs `/se-plan-loop` before `/se-execute`
- `/se-publish` — named ledger paths, ordinary git, never force-push
- `/se-compact-brief` — shrink a multi-slice arc in place; then cold
  `/se-review-brief`
- `/se-prep`, `/se-sync-worktree`, `/se-settle-worktree`, `/se-tidy-worktree`
  — portable worktree cycle using bound `default_branch`
- `templates/CLAUDE.md` — thin `@AGENTS.md` wrapper; `/se-setup` offers it
  when missing and never overwrites

## 0.4.0

Evidence-backed skill improvement.

- `/se-improve-skill-from-run` — two-phase review-then-apply from one
  real run (Claude JSONL exporter, Codex recorder if present, Cursor
  current conversation)
- Does not require Entire or a product session store

## 0.3.0

Weekly changeability loop.

- `/se-review-codebase` — Farley-lens sweep, dated report, pause before
  writing the remediation plan
- `/se-deliver-remediation-plan` — one `/se-deliver` per pending item
- `/se-setup` copies missing `remediation-plan.md` and
  `remediation-history.md` (never overwrites an existing queue)

## 0.2.0

Host documentation scaffolding.

- `/se-setup` copies missing philosophy, engineering-guide, documentation-placement, and empty SOP/ADR/changelog/tech-debt/ledger homes
- Existing host docs are never overwritten
- `knowledge_homes` now names philosophy, guide, and debt paths

## 0.1.0

First public release.

- Thin-slice loop: brief, review-brief, deliver, execute, review gate, ship, reflect
- Host bindings via `/se-setup` and `.slice-engineering/config.yaml`
- Cursor, Claude Code, and Codex manifests
- Supporting skills: challenge-scope, commit, handoff, investigate, prototype, create-skill
