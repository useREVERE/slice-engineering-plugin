# CLAUDE.md

@AGENTS.md

Everything in `AGENTS.md` applies; this file adds only Claude Code-specific
workflow. If the two ever disagree, fix the drift — do not maintain
parallel policy here.

Host bindings live in `.slice-engineering/config.yaml`. Slice Engineering
skills resolve host facts from those bindings and provider differences
from the plugin's `skills/_shared/agent-conventions.md`.

## Claude Code Mechanics

- **Temp artifacts:** write under `~/.claude/` (the sandbox may block
  `/tmp` and paths outside the repo). Keep `XXXXXX` at the end of `mktemp`
  templates.
- **Hooks:** a hook `command` must invoke its script as
  `python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/<name>.py"`, never by
  relative path. Claude Code resolves a relative command against the Bash
  tool's working directory, which persists across calls, so one command
  ending in `cd <subdir>` breaks every later Bash/Write/Edit call — and
  because a missing script exits 2, that reads as a *deny*, leaving no
  in-session way out. `$CLAUDE_PROJECT_DIR` is the session's startup
  directory, does not follow the Bash cwd, and in a worktree is the
  worktree root rather than the primary checkout.
- **Testing:** no hook enforces test-first. Follow the TDD guidance in
  `AGENTS.md` and the host engineering guide. The bound `verify_command`
  is the real gate.
- **Skills:** when creating or modifying skills, follow the plugin's
  `se-create-skill` contract. Never replace a skill mount symlink with a
  real file.

## Asking vs. Deciding

Default to deciding. Before asking, check whether the answer is already
discoverable — in the code, git history, ledger, docs, config, or earlier
in this conversation. Never ask the user to supply a fact you could look
up.

Only ask when all three hold: the answer is not derivable from the repo or
the conversation; different answers produce materially different work, not
just different style; and it is a product, priority, or preference call
that is genuinely the user's to make. Otherwise take the sensible default,
state in one line which default you took and why, and keep going — a
reversible wrong default costs far less than a blocked turn.

When you do ask, give the user enough to answer: say what you already
found, why it does not settle the question, and lead with your
recommendation. If answering would require the user to go read code, that
is a sign you should have answered it yourself.

## Auto-Memory Policy

**Do not write local memories.** Local memory is an anti-pattern here:
anything worth remembering must be structured into the repo or the bound
ledger where every teammate and agent can see it. When you learn something
durable mid-task, write it to its shared home as part of the work instead
of saving a memory. A truly machine- or user-specific quirk may go in
`CLAUDE.local.md` at the primary repo root (auto-loaded by Claude Code,
gitignored) — if a quirk affects Codex or Cursor too, it belongs in a
shared home.

## Task Delegation

Follow the provider-neutral delegation contract in `AGENTS.md`. For Claude
Code, dispatch exploration subagents with a cheaper available tier and let
adversarial-judgment subagents inherit the lead model. Resolve the mapping
from `skills/_shared/agent-conventions.md`; do not duplicate the general
delegation policy or transient supported-model lists here.
