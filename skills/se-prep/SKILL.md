---
name: se-prep
description: Prepare the primary repo default branch as a clean, current base for spinning off parallel delivery worktrees. Use on the primary checkout before creating task worktrees.
disable-model-invocation: true
---

# Prep

Prepare the primary repo so new task worktrees can branch from current
`origin/<default_branch>` without inheriting stale commits, duplicate local
history, or confusing worktree/branch leftovers.

Success means the primary worktree is clean, on `<default_branch>`, fetched
from `origin`, local `<default_branch>` matches `origin/<default_branch>`,
local-only commits have been classified and handled safely, stale Git
worktree metadata is pruned when safe, inactive worktrees and stale
branches are reported or cleaned up according to the safety rules below,
and the repo is ready to serve as the base for one or many delivery
sessions.

Task worktree roots and branch prefixes are provider-specific; resolve them
from `skills/_shared/agent-conventions.md`. Resolve `<default_branch>` from
`skills/_shared/bindings.md`.

This skill prepares the base. It does not create task branches or task
worktrees. Hosts with `worktrees: false` may still run it to align the
primary default branch; they must not then create worktrees unless
bindings change.

## Inputs and Outputs

**Input:** Usually none. Run from the primary repo, not from a task
worktree.

**Output:** Ready status with local `<default_branch>` SHA,
`origin/<default_branch>` SHA, local commit classification, cleanup status
for worktrees/branches, any ship status, and any blocker that must be
resolved before creating task worktrees.

Treat `$ARGUMENTS` as any explicit cleanup or checkpoint qualification.

Start with a short update before tool calls.

## Workflow

Inspect:

```bash
pwd
git status --short --branch
git branch --show-current
git worktree list --porcelain
git worktree prune --dry-run
git fetch --prune origin
git status --short --branch
git rev-parse <default_branch>
git rev-parse origin/<default_branch>
git log --oneline --left-right <default_branch>...origin/<default_branch>
git cherry origin/<default_branch> <default_branch>
```

Then:

- If the current worktree is dirty, inspect the status before settlement.
  If any untracked files are present (`??` in `git status --short --branch`),
  stop before checkpointing unless the user explicitly asked this prep run
  to checkpoint untracked changes. Report the untracked paths and the next
  safe choices: commit them intentionally, move them out of the repo, or
  explicitly approve checkpointing. Rationale: `git stash --include-untracked`
  preserves the content but removes new files from the visible worktree,
  which is an unacceptable surprise during prep.
- For dirty worktrees without untracked files, or when the user explicitly
  approved checkpointing untracked files for this run, invoke
  `se-settle-worktree` immediately before refusing. Let
  `se-settle-worktree` decide whether the changes are commit-ready, safe to
  checkpoint, or risky enough to stop. Continue prep only when
  `se-settle-worktree` leaves the worktree clean; otherwise stop and report
  its blocker and recovery guidance.
- If settlement creates a stash checkpoint, carry that state through the
  final answer. Do not describe the run as simply "clean" or "ready"
  without also saying user work is hidden in a stash, naming the stash
  ref, recovery note, restore command, and whether the checkpoint included
  untracked files.
- Refuse if the current branch is not `<default_branch>`.
- Refuse if this appears to be a task worktree instead of the primary repo.
- Classify local-only commits before deciding to ship:
  - `git cherry origin/<default_branch> <default_branch>` lines starting
    with `-` are patch-equivalent to commits already on
    `origin/<default_branch>`; treat them as duplicate local history, not
    work to ship.
  - lines starting with `+` are genuinely local patches. Inspect their
    subjects and changed files before deciding whether they are intentional
    work.
- If local `<default_branch>` is behind `origin/<default_branch>` and has
  no genuine local-only commits, fast-forward to
  `origin/<default_branch>`. If duplicate-only local commits prevent a
  fast-forward, move local `<default_branch>` to
  `origin/<default_branch>` only after confirming the working tree is clean
  and every local-only patch is patch-equivalent upstream.
- If local `<default_branch>` has genuine local-only commits, load and run
  `se-ship` only when they are clearly intentional and ready to publish.
  Let `se-ship` own rebase, verification, push, remote SHA verification,
  and primary-base refresh. Stop if `se-ship` stops.
- If local `<default_branch>` is both ahead and behind, do not merge
  blindly. Classify the ahead commits as duplicate vs genuine, then either
  drop duplicate-only history by aligning to `origin/<default_branch>`, or
  preserve genuine commits by replaying/shipping them from a temporary
  branch.
- After a fast-forward, duplicate cleanup, or ship, fetch again and confirm
  local `<default_branch>` and `origin/<default_branch>` point to the same
  SHA.
- Do not create task branches or task worktrees.

## Parallel Inspection

When the repo has many branches or worktrees, use background agents only
for read-only audits while the main session handles primary default-branch
state and all mutating Git operations. Safe delegated audits include:

- worktree cleanup candidates and blockers
- stale branch cleanup candidates and blockers
- local commit classification, including `git cherry` and commit stats
- process/doc drift that may need preserving before aligning
  `<default_branch>`

Agents must not run `git fetch`, switch branches, reset, merge, rebase,
prune, remove worktrees, delete branches, stage, commit, or push. They
should return the commands inspected, candidate lists, safety reasons, and
blockers. The main session owns every state transition and the final
readiness gate.

## Worktree Cleanup

Always inspect worktrees during prep. Distinguish three cases:

- **Primary worktree:** the current repo on `<default_branch>`; never
  remove it.
- **Stale metadata:** `git worktree prune --dry-run` reports entries whose
  directories are already gone. Run `git worktree prune` when the dry run
  only reports prunable metadata. This does not delete live files.
- **Inactive task worktrees:** existing directories under the task worktree
  roots (see Agent Conventions). Do not remove by default. A worktree is
  eligible for cleanup only when all of these are true:
  - its working tree is clean
  - it is not on `<default_branch>`
  - its branch/HEAD is reachable from `origin/<default_branch>`
  - the branch is not ahead of `origin/<default_branch>`
  - it is not the current worktree

For eligible inactive task worktrees, report them as cleanup candidates.
Remove one only when the user explicitly asks prep to clean inactive
worktrees or has already granted that intent for this run. Use the same
safety posture as `se-tidy-worktree`: remove from a safe external Git
context and delete only merged branches with `git branch -d`, never force.

If a task worktree is dirty, unmerged, detached ambiguously, or has
local-only commits, leave it alone and report the reason.

## Branch Cleanup

After `git fetch --prune origin`, inspect local branches:

```bash
git branch --format="%(refname:short) %(upstream:short) %(upstream:track)"
git branch --merged origin/<default_branch>
```

Safe branch cleanup is opt-in unless the user explicitly asked prep to
clean stale branches. Delete a local branch with `git branch -d` only when
all are true:

- it is not `<default_branch>`
- it is not checked out in any worktree
- it is merged/reachable from `origin/<default_branch>`
- it has no unpushed commits
- it is clearly a task branch or its upstream was pruned/deleted

Never force-delete stale branches. If a branch is unmerged, checked out, or
has local-only commits, report it instead of deleting it.

## Final Readiness Gate

Before declaring the repo ready for new work, prove:

```bash
git status --short --branch
git rev-parse <default_branch>
git rev-parse origin/<default_branch>
git log --oneline --left-right <default_branch>...origin/<default_branch>
git cherry origin/<default_branch> <default_branch>
git worktree list --porcelain
```

Ready means:

- primary repo path is unambiguous
- current branch is `<default_branch>`
- working tree is clean
- local `<default_branch>` SHA equals `origin/<default_branch>` SHA
- ahead/behind log is empty
- no genuine local-only commits remain
- stale worktree metadata was pruned or reported
- inactive worktrees and stale branches were cleaned up when explicitly
  allowed, or listed with reasons they were left untouched

## Output

Report:

- primary repo path
- local `<default_branch>` SHA
- `origin/<default_branch>` SHA
- local commit classification: none | duplicate-only | genuine local commits
- whether a fast-forward or duplicate-history alignment was performed
- whether `se-ship` ran, and the remote default-branch SHA if it shipped
- worktree cleanup: pruned metadata, inactive candidates removed, candidates
  left
- branch cleanup: branches deleted, candidates left, blockers
- dirty-work settlement: none | committed | checkpointed tracked changes |
  checkpointed with explicitly-approved untracked changes | blocked on
  untracked changes, including stash ref and restore command when applicable
- readiness verdict for spinning off delivery worktrees
- blocker and next safe action, if not ready

## Stop Rules

Stop before changing anything if fetch fails, `se-settle-worktree` cannot
safely preserve a dirty worktree, the branch is not `<default_branch>`, or
the repo context is ambiguous. Stop before deleting live worktrees or local
branches unless the user explicitly requested that cleanup and every safety
check passes. Stop after invoking `se-ship` if integration conflicts,
verification fails, push is unsafe, or `se-ship` reports any blocker. Stop
before stash-checkpointing untracked files unless the user explicitly
approved that for this prep run. Stop if the final local
`<default_branch>` SHA does not match `origin/<default_branch>`.

$ARGUMENTS
