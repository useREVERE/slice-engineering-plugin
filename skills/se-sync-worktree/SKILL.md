---
name: se-sync-worktree
description: Safely synchronize a clean current checkout with origin/default_branch before planning or delivery. Use when starting or resuming a workflow that must load current code and canonical skill instructions.
disable-model-invocation: true
---

# Sync Worktree

Bring one clean checkout onto the current `origin/<default_branch>`
lineage before a planning or delivery workflow relies on its code or
versioned skill instructions. Success means the checkout is current enough
to proceed, any history rewrite is explicit in the result, and the caller
knows whether to reload skills and invalidate earlier verification.

This skill is a narrow workflow preflight, not repository cleanup or
shipping. Use `se-prep` for the primary repository's broader hygiene and
`se-ship` for finished work that is ready to integrate and push.

It does not create worktrees. Hosts with `worktrees: false` still use it to
fast-forward or rebase the current checkout.

Resolve `<default_branch>` from `skills/_shared/bindings.md`.

## Input and Boundary

Treat `$ARGUMENTS` as the task or workflow boundary whose commits are
expected in this checkout. The caller should provide that boundary when the
branch has local commits. Do not infer that unrelated commits belong to the
current task.

Start by recording:

```bash
git status --short --branch
git branch --show-current
git rev-parse HEAD
git fetch origin
git rev-parse origin/<default_branch>
git rev-list --left-right --count origin/<default_branch>...HEAD
git log --oneline --decorate --left-right origin/<default_branch>...HEAD
```

Stop before changing history when fetch fails, the checkout is detached,
the tree has staged, unstaged, or untracked changes,
`origin/<default_branch>` is unavailable, or local-only commits cannot be
attributed confidently to the supplied task. Do not stash, commit, reset,
merge non-fast-forward, or discard files.

When staged, unstaged, or untracked changes are the blocker, route the
caller to `se-settle-worktree` with the supplied task boundary and the
exact status. This skill does not invoke `se-settle-worktree` itself:
settlement is a separate preservation decision, and the caller must decide
whether the changes are task-owned or ambiguous. After successful
settlement, the caller must invoke this skill again from the beginning
rather than continuing from partial preflight evidence.

## Synchronization Policy

If `HEAD` already contains current `origin/<default_branch>`, make no
change. Local task commits ahead of current `origin/<default_branch>` are
already synchronized.

If the current branch is `<default_branch>`, only a behind-only
fast-forward is allowed:

```bash
git merge --ff-only origin/<default_branch>
```

Stop on ahead or diverged `<default_branch>`; route that state through
`se-prep` or `se-ship` instead of rewriting the shared base.

For a named task branch whose clean local-only commits belong to the
supplied task, replay them onto current production history:

```bash
git rebase origin/<default_branch>
```

If the rebase conflicts, do not resolve it speculatively. Abort the rebase
to restore the preflight state, then report the conflicting paths and stop:

```bash
git diff --name-only --diff-filter=U
git rebase --abort
```

Never force-push. This skill updates only local checkout history and does
not stage, commit, test, push, or modify another worktree.

## Verification and Handoff

After a no-op, fast-forward, rebase, or aborted conflict, report and verify:

```bash
git status --short --branch
git rev-parse HEAD
git rev-parse origin/<default_branch>
git rev-list --left-right --count origin/<default_branch>...HEAD
```

Return:

- branch and old/new `HEAD`;
- `origin/<default_branch>` SHA;
- outcome: already current, fast-forwarded, rebased, or blocked;
- ahead/behind counts after the operation;
- whether commit SHAs or the tree changed;
- blocking paths or ambiguous commits, if any; and
- `reload_required: true|false` and `verification_invalidated: true|false`.

Any successful fast-forward or rebase sets `reload_required: true`: the
caller must reread its own current skill plus every component skill needed
for the next phase before routing. A rebase also invalidates commit-SHA-based
evidence; a changed tree invalidates tree-based verification. The caller
owns those reload and revalidation decisions because this skill does not
know which workflow phases it will invoke.

$ARGUMENTS
