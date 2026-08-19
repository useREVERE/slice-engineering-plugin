# Changelog

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
