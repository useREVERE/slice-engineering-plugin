---
name: se-execute
description: Implement an accepted plan step by step with TDD, scoped commits, and a review handoff. Use when a plan is ready and code needs to be written.
disable-model-invocation: true
---

# Execute

Implement an accepted plan while keeping the codebase shippable. Success
means each completed step is test-driven (or honestly exempt), verified,
committed, and ready for `se-review-loop`.

Treat `$ARGUMENTS` as the plan path plus autonomy or scope.

Read `skills/_shared/bindings.md` and host `AGENTS.md` before editing.

## Autonomy

Default: **normal**.

- **guided:** decompose, then stop before production edits.
- **normal:** edit, test, and commit each step. Ask for unsettled product
  or design decisions.
- **autonomous:** continue through the plan until complete, a verify
  failure, or user judgment is required.

## Freshness

Fetch the default remote. If this branch is behind `origin/<default_branch>`
and the tree is clean, rebase. If the tree is dirty or rebase needs
judgment, stop.

## Each commit-sized step

1. Run the smallest relevant existing test when the area is risky or
   current behavior is unclear. Use the host `verify_command` when the
   change is broad or the safe subset is unclear.
2. Write a failing behavioral test first unless the step is docs-only or a
   mechanical rename. Name the test as a sentence that states the rule.
3. For config-like changes, prefer a characterization or regression test
   that protects the operational contract.
4. Implement the minimum that passes.
5. Commit with `se-commit`. One purpose per commit. Boy-scout cleanups in
   files already touched go in a **separate** commit.

Never commit a red test ahead of the change that makes it pass. Never
commit secrets or machine-specific absolute paths.

## After the last step

Run the host `verify_command` when the change is behavioral, touches shared
contracts, or the safe subset is unclear. If `verify_command` is empty,
say what you ran instead and why that is enough — or stop and ask.

Do not start `se-review-loop` when this run is already inside `se-deliver`.
Otherwise hand off to `se-review-loop`.

## Output

Commits made, tests run, remaining plan steps, and the review handoff.
