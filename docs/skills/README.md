# Skill catalog

Authoritative runtime text lives in `skills/<name>/SKILL.md`. This page is
the map.

## Loop

| Skill | Side effects | Notes |
| --- | --- | --- |
| `se-setup` | Yes | Bindings + missing doc homes |
| `se-brief` | Optional write | Conversation or ledger |
| `se-review-brief` | No | Plan-readiness |
| `se-plan-loop` | Temp write | Adaptive review; runs `se-review-plan` |
| `se-plan` | Temp write | Alias of `se-plan-loop` |
| `se-review-plan` | No | Farley verdict before execute |
| `se-deliver` | Yes | Orchestrator |
| `se-execute` | Yes | TDD |
| `se-review` | No | Report only |
| `se-review-loop` | Yes | Gate |
| `se-ship` | Yes | Uses bindings |
| `se-reflect` | Yes | Evidence + frontier; may compact |

## Ledger

| Skill | Side effects | Notes |
| --- | --- | --- |
| `se-publish` | Yes | Named paths; never force-push |
| `se-compact-brief` | Brief edit | No commit/push; then cold `se-review-brief` |

## Worktrees

| Skill | Side effects | Notes |
| --- | --- | --- |
| `se-prep` | Yes | Primary `<default_branch>` hygiene |
| `se-sync-worktree` | Yes | Does not invoke settle |
| `se-settle-worktree` | Maybe | Commit, checkpoint, or stop |
| `se-tidy-worktree` | Yes | After ship; never force-delete |

## Around the loop

| Skill | Side effects | Notes |
| --- | --- | --- |
| `se-challenge-scope` | No | |
| `se-commit` | Yes | |
| `se-handoff` | Temp write | |
| `se-investigate` | No | |
| `se-prototype` | Write (throwaway) | |
| `se-create-skill` | Yes | |
| `se-improve-skill-from-run` | After approval | Two-phase; compact indexes only |
| `se-review-codebase` | Docs only | Dated report + plan after pause |
| `se-deliver-remediation-plan` | Yes | One `se-deliver` per pending item |
