---
name: se-commit
description: Create a well-crafted git commit that a future agent can understand. Use when staged or unstaged work should become one logical commit.
disable-model-invocation: false
---

# Commit

Create a clean git commit. The history is primarily read by future agents.

Treat `$ARGUMENTS` as optional scope or message qualification.

Own the process. Do not pause for approval unless committing safely needs
a user decision.

## Evidence

```bash
git branch --show-current
git diff --cached --stat
git diff --stat
git ls-files --others --exclude-standard
git log --oneline -5
```

Read the relevant diffs. If the diff does not explain why the change
matters, read the surrounding files.

## Scope

- One commit when all changes serve one purpose, including tests for that
  purpose.
- Split when feature, fix, refactor, and docs are mixed.
- Stage explicit paths. Avoid `git add -A`.
- Never stage `.env`, credentials, or files that look secret-bearing.
- Never commit a red test ahead of the fix that makes it pass.
- Do not commit machine-specific absolute paths.
- If the change only completes the previous unpublished commit (typo,
  missing test), prefer amending and rewrite the message so it still
  describes the combined change. If that commit may be published, ask
  before rewriting history.

## Message

Match the host repository's style (`git log -5`). If the host has no
obvious convention, use an imperative subject that states the behavior
change, not the files touched.

## Output

Commit SHA, subject, and whether anything was left unstaged and why.
