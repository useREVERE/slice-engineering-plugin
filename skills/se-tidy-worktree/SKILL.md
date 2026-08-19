---
name: se-tidy-worktree
description: Remove a shipped task worktree and its merged local task branch using a safe external Git context. Use after se-ship when worktrees are bound and the current session directory should go away.
disable-model-invocation: false
---

# Tidy Worktree

Remove the current task worktree after it has shipped to
`origin/<default_branch>`. Success means the current worktree is clean, the
task branch or detached HEAD is reachable from `origin/<default_branch>`,
the worktree is removed from an external Git context, and the merged local
task branch is deleted without force.

This is a terminal action. Removing the current worktree deletes the
directory the session is running in, so cleanup must end with the external
`worktree remove` and `branch -d` commands. Do not run repo commands from
the removed worktree after cleanup.

Do not create worktrees. Do not run this against the primary checkout.
Hosts with `worktrees: false` should not need this skill.

Resolve `<default_branch>` from `skills/_shared/bindings.md`. Task worktree
roots and branch prefixes come from
`skills/_shared/agent-conventions.md`.

## Inputs and Outputs

**Input:** Current task worktree, usually under your provider's worktree
root, on a task branch with your provider's prefix, after a successful
`se-ship`.

**Output:** Removed worktree, deleted merged local task branch, or a
refusal with the exact safety check that failed.

Treat `$ARGUMENTS` as an explicit worktree, branch, or cleanup
qualification.

Start with a short update before tool calls.

## Safety Checks

Refuse unless all of these are true:

- `git status --porcelain` is empty.
- `git fetch origin` succeeds.
- current branch is not `<default_branch>`.
- a task branch can be identified.
- current `HEAD` is reachable from `origin/<default_branch>`.
- task branch is reachable from `origin/<default_branch>`.
- `git worktree list` shows a safe external Git context, such as the
  primary repo worktree, that is not the current worktree.

Never force-delete a branch. Never remove a worktree with uncommitted
changes. Do not switch the current worktree to `<default_branch>`.

## Required Evidence

Gather the cleanup facts before the terminal action:

```bash
git status --porcelain
git fetch origin
git rev-parse --show-toplevel
git branch --show-current
git rev-parse --short HEAD
git merge-base --is-ancestor HEAD origin/<default_branch>
git merge-base --is-ancestor <task-branch> origin/<default_branch>
git worktree list --porcelain
```

Identify:

- current worktree path
- task branch, usually `<provider-prefix>/<task>` per Agent Conventions
- safe external Git context, preferably the primary repo path from
  `git worktree list --porcelain`

If `git branch --show-current` is empty, inspect
`git worktree list --porcelain` and local branch refs to identify whether a
task branch points at the current HEAD. Refuse if no unambiguous task
branch can be identified.

## Terminal Cleanup

Run the terminal cleanup from the external Git context:

```bash
git -C <external-git-context> worktree remove <current-worktree-path>
git -C <external-git-context> branch -d <task-branch>
```

These two commands should be the final repo operations. The worktree
removal is the final filesystem operation involving the current worktree;
branch deletion follows from the external context. Do not run `git status`
afterward from the removed worktree.

## Output

After the terminal action, say:

- worktree removed: `<current-worktree-path>`
- branch deleted: `<task-branch>`
- external Git context used: `<external-git-context>`

If cleanup is refused, say which safety check failed and the command
output that proves it.

## Stop Rules

Stop before removing anything if the worktree is dirty, fetch fails, the
current branch is `<default_branch>`, the task branch is missing or
ambiguous, either HEAD or task branch is not merged into
`origin/<default_branch>`, no safe external context is available, or
branch deletion would require force.

$ARGUMENTS
