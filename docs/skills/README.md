# Skill catalog

Authoritative runtime text lives in `skills/<name>/SKILL.md`. This page is
the map.

## Loop

| Skill | Side effects | Notes |
| --- | --- | --- |
| `se-setup` | Yes | Bindings + missing doc homes |
| `se-brief` | Optional write | Conversation or ledger |
| `se-review-brief` | No | Plan-readiness |
| `se-plan` | Temp write | Discarded after ship |
| `se-deliver` | Yes | Orchestrator |
| `se-execute` | Yes | TDD |
| `se-review` | No | Report only |
| `se-review-loop` | Yes | Gate |
| `se-ship` | Yes | Uses bindings |
| `se-reflect` | Yes | Evidence + frontier |

## Around the loop

| Skill | Side effects | Notes |
| --- | --- | --- |
| `se-challenge-scope` | No | |
| `se-commit` | Yes | |
| `se-handoff` | Temp write | |
| `se-investigate` | No | |
| `se-prototype` | Write (throwaway) | |
| `se-create-skill` | Yes | |
| `se-review-codebase` | Docs only | Dated report + plan after pause |
| `se-deliver-remediation-plan` | Yes | One `se-deliver` per pending item |
