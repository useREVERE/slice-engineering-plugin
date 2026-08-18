---
name: se-ship
description: Integrate finished work with the default branch, verify, and publish using host bindings (trunk push or pull request). Use when review has converged on ship-it.
disable-model-invocation: true
---

# Ship

Publish reviewed work using this repository's bindings. Success means the
change is integrated with the current default branch, verified, and
published in the bound `ship_mode`.

Treat `$ARGUMENTS` as a qualification (docs-only, skip-verify with reason,
or pull-request title).

Read `skills/_shared/bindings.md`. If `config.yaml` is missing, stop and
run `/se-setup` first.

## Preconditions

- working tree is clean, or the user explicitly scoped the leftover files
- review verdict is `ship it` or the user explicitly overrides
- `git fetch` succeeded

If the branch is behind `origin/<default_branch>`, rebase. Prefer the
default branch for unrelated conflicts. Stop if the rebase needs product
judgment.

## Verify

Run `verify_command` when runtime behavior changed. Docs-only, comments,
mechanical renames, and narrow config already protected by a focused test
may skip the full command — state the rationale.

If `verify_command` is empty and the change is behavioral, stop and ask.
Do not invent a test runner.

## Publish

**`ship_mode: trunk`**

- integrate onto `<default_branch>`
- push to `origin/<default_branch>`
- never force-push or amend a published commit without explicit approval
- never skip hooks (`--no-verify`)

**`ship_mode: pull-request`**

- push the task branch
- open a pull request against `<default_branch>`
- do not merge unless the user asked

## Deploy

- `none` — shipping is git publication
- `command` — run `deploy_command` and report output
- `url` — fetch `deploy_url` after publication and report status

A failed deploy probe does not silently count as accepted. Say so.

## Output

Published SHA or PR URL, verify evidence, deploy evidence, and the
rationale if verification was skipped.
