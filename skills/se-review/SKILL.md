---
name: se-review
description: Fresh-context, report-only review of recent code changes for correctness, changeability, and test confidence. Use when a diff needs a ship-it or findings before merge.
disable-model-invocation: false
---

# Review

Review a diff for correctness, changeability, and test confidence. Success
means actionable risks are reported with evidence, and clean changes receive
an explicit `ship it`.

This is feedback only. Do not edit code.

Treat `$ARGUMENTS` as a commit range, branch, or review focus. When omitted,
review the staged diff if present, otherwise `git diff HEAD~1`. For a full
branch, use `git diff <default_branch>...HEAD` after reading bindings.

Run in fresh context when the harness can. If it cannot, inspect the diff
before reconstructing how the code was written.

## Lens

- correctness, data loss, security, behavior regressions
- hidden coupling and locality of change
- comprehensible intent and contracts
- behavioral tests for new branches, error paths, and contracts
- accidental complexity beyond current need
- clean revert path
- boy-scout cleanup mixed into a behavior commit
- a new test that cannot fail for the mutation it claims to catch

Judge against this project's current stage. Do not manufacture enterprise
process.

## Prior review

If the caller passes prior findings, do not re-raise settled points. Revisit
only when the fix introduced a new issue or the disagreement is clearly
wrong.

## Verdict

- `ship it` — remaining notes are preferences
- `fix` — numbered findings with file, evidence, and why it matters
- `blocked` — missing context or an unsafe diff scope

Do not loop on style.
