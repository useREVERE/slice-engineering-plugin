# Agent Conventions

Skills are provider-neutral. When a skill needs a provider-specific value,
resolve it from this table. Identify the provider from your own system
prompt or harness.

| Convention | Codex | Claude Code | Cursor |
| --- | --- | --- | --- |
| Skill invocation | `$se-name` | `/se-name` | `/se-name` |
| Task branch prefix | `codex/` | `claude/` | `cursor/` |
| Task worktree root | `~/.codex/worktrees/<id>/` | `.claude/worktrees/<name>/` | `.cursor/worktrees/<name>/` |
| Grounding docs | `AGENTS.md` | `CLAUDE.md` + `AGENTS.md` | `AGENTS.md` |
| Fresh-context review | new session or delegated reviewer | `context: fork` or subagent | subagent / Task, no caller rationale |
| Exploration subagent | cheaper available tier | cheaper available tier (Sonnet-class) | cheaper available tier |
| Adversarial judgment | same tier as the lead, fresh context | inherit lead model, fresh context | inherit lead model, fresh context |

The primary checkout stays on the host `default_branch` when worktrees are
enabled. Derive locations with `git worktree list` and
`git rev-parse --show-toplevel`. Never embed machine-specific absolute paths
in tracked files.

This file is not a skill. Skills that touch branches, worktrees, or review
dispatch reference it.
