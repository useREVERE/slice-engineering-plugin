---
name: se-settle-worktree
description: Preserve dirty worktree changes safely when they block planning, shipping, delivery, or other workflow skills; inspect, commit-ready hand off, checkpoint to stash with a recovery note, or stop on risky state without losing work.
disable-model-invocation: false
---

# Settle Worktree

Resolve a dirty worktree as a preservation decision, not as cleanup.
Success means all current changes are either committed through the
`se-commit` skill, checkpointed with a verified recovery path, or left
untouched with a precise reason the agent should ask the user.

Use this when another workflow is blocked by uncommitted changes,
especially `se-plan-loop`, `se-deliver`, `se-ship`, `se-prep`,
`se-review-loop`, or `se-tidy-worktree`.

Treat `$ARGUMENTS` as explicit context about the changes or preservation
mode.

## Default Posture

Prefer preserving work over making the tree clean. Never discard changes.
Never use destructive commands. Never stage or commit secrets.

## Paths

1. **Commit-ready**
   - Use when the changes are coherent, reviewed enough to describe, and
     belong to the just-finished task.
   - Invoke the `se-commit` skill.
   - Do not use the checkpoint script as a substitute for a meaningful
     commit.

2. **Checkpoint**
   - Use when changes are valuable but not commit-ready, and the next
     workflow needs a clean tree.
   - Run the bundled script in inspect mode first:

     ```bash
     python3 skills/se-settle-worktree/scripts/settle_worktree.py --inspect
     ```

   - If it reports `checkpoint_safe: true`, run:

     ```bash
     python3 skills/se-settle-worktree/scripts/settle_worktree.py --checkpoint --reason "<short reason>"
     ```

   - Report the stash ref and recovery note path.
   - If `git stash` fails with an index or permission error, rerun the same
     checkpoint command with the normal escalation flow. Do not copy files
     or invent a separate backup path.

3. **Stop**
   - Stop and ask the user when the script reports conflicts, staged
     changes, possible secret-bearing files, no changes, or another risk.
   - Also stop if the dirty state appears unrelated to the current task and
     cannot be confidently described.

## Script Guarantees

The checkpoint script:

- refuses merge conflicts and staged changes
- refuses likely secret-bearing paths such as `.env`, credential files, and
  private keys
- captures branch/detached state, `HEAD`, status, diff stats, changed
  paths, untracked files, and recent commits
- creates `git stash push --include-untracked` only in `--checkpoint` mode
- verifies the worktree is clean after checkpointing
- writes a recovery note under the Git-private directory
  (`.git/slice-engineering/checkpoints/` or the common dir for a worktree),
  not a guessed `/tmp`
- reports stash-write failures as structured JSON with the Git stderr and a
  retry hint

The script does not decide whether changes deserve a real commit. That
remains agent judgment via the `se-commit` skill.

## Output

When checkpointed, say:

- checkpoint created: `<stash-ref>`
- recovery note: `<path>`
- restore command: `git stash apply <stash-ref>`
- next workflow may continue from the clean tree

When refused, say which safety check blocked settlement and include the
relevant paths or status lines.

When another workflow invoked settlement, return control to that caller
after the tree is verified clean. The caller must rerun the blocked
workflow's preflight; settlement never proves that the branch is current,
safe to rebase, or otherwise ready for the next phase.

$ARGUMENTS
