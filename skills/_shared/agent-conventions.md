# Agent Conventions

Skills are provider-neutral. When a skill needs a provider-specific value,
resolve it from this table. Identify the provider from your own system
prompt or harness.

| Convention | Codex | Claude Code | Cursor |
| --- | --- | --- | --- |
| Skill invocation | `$se-name` | `/se-name` | `/se-name` |
| Nested skill call | invoke `$se-name` when the harness allows | compose the target `SKILL.md`; do not search for a nested `/` invoke when `disable-model-invocation` is true | compose the target `SKILL.md` when the harness cannot nest skill calls |
| Goal mode | create a Codex goal for multi-item queues | unavailable — report it and continue under stop rules | unavailable — report it and continue under stop rules |
| Temp artifacts | runtime temp or task worktree | `~/.claude/` (sandbox may block `/tmp` and paths outside the repo) | workspace temp or `.cursor/` — not a guessed `/tmp` |
| Assessor label | `Codex ({model})` | `Claude Code ({model})` | `Cursor ({model})` |
| Task branch prefix | `codex/` | `claude/` | `cursor/` |
| Task worktree root | `~/.codex/worktrees/<id>/` | `.claude/worktrees/<name>/` | `.cursor/worktrees/<name>/` |
| Grounding docs | `AGENTS.md` | `CLAUDE.md` + `AGENTS.md` | `AGENTS.md` |
| Fresh-context review | new session or delegated reviewer | `context: fork` or subagent | subagent / Task, no caller rationale |
| Exploration subagent | cheaper available tier | cheaper available tier (Sonnet-class) | cheaper available tier |
| Adversarial judgment | same tier as the lead, fresh context | inherit lead model, fresh context | inherit lead model, fresh context |

## Run evidence

`se-improve-skill-from-run` reads compact indexes, never raw transcripts.

| Provider | Default source | Compact exporter |
| --- | --- | --- |
| Codex | Current conversation, a user-supplied path, or a session recorder already on `PATH` | None bundled. Do not install a recorder as part of the skill. |
| Claude Code | `~/.claude/projects/<encoded-cwd>/*.jsonl` | `skills/se-improve-skill-from-run/scripts/export_claude_run.sh` |
| Cursor | Current conversation; else a user-supplied path | None bundled. Cloud-agent transcript files are valid input if already on disk. |

Default compact indexes: `metadata.json`, `user-messages.txt`,
`agent-messages.txt`, `tool-calls.tsv` or `function-calls.tsv`,
`tool-failures.txt`, and `skill-spans.txt` when attribution exists.

The primary checkout stays on the host `default_branch` when worktrees are
enabled. Derive locations with `git worktree list` and
`git rev-parse --show-toplevel`. Never embed machine-specific absolute paths
in tracked files.

This file is not a skill. Skills that touch branches, worktrees, or review
dispatch reference it.
