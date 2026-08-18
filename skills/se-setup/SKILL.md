---
name: se-setup
description: Bind Slice Engineering to this repository by writing .slice-engineering/config.yaml. Use when installing the plugin in a new or existing project, or when test/ship/ledger conventions are missing or wrong.
disable-model-invocation: true
---

# Setup

Write host bindings so every other skill can run without guessing. Success
means `.slice-engineering/config.yaml` exists, matches this repository, and
the user knows what was chosen and why.

Treat `$ARGUMENTS` as an explicit default branch, verify command, ship mode,
or ledger location.

## Inspect

From the repository root (`git rev-parse --show-toplevel`):

- default branch from `origin/HEAD`, else `main`
- existing test entry points: `Makefile` (`test` target), `package.json`
  scripts, `pyproject.toml`, `go.mod`, `Cargo.toml`
- whether `AGENTS.md` already exists
- whether `docs/ledger/`, `.slice-engineering/`, or another planning tree
  already exists
- whether the project already opens pull requests or pushes a default branch

Do not read secrets. Do not source `.env`.

## Choose bindings

Start from `templates/config.yaml` in this plugin. Prefer detected values
over the template defaults. Defaults when nothing is detected:

- `ship_mode: pull-request` (safer for an unknown host)
- `ledger: in-repo` at `docs/ledger`
- `deploy: none`
- `worktrees: false`
- `verify_command` left empty only if there is no test runner; say so

If `$ARGUMENTS` or the user names a value, use it.

## Write

1. Create `.slice-engineering/` if needed.
2. Write `config.yaml` without clobbering a file that already looks
   intentional — update only empty or still-template keys, and report what
   you left alone.
3. Ensure `.slice-engineering/config.local.yaml` is gitignored.
4. If `ledger` is `in-repo` and the ledger root is missing, create
   `<ledger_root>/README.md` that says arcs live in `arcs/<slug>/brief.md`.
   Do not create a sample arc.
5. If `AGENTS.md` is missing, offer the plugin `templates/AGENTS.md` and
   write it only when the user wants a starter. If `AGENTS.md` exists, add
   at most a short pointer to `.slice-engineering/config.yaml` — do not
   rewrite their rules.

## Output

Report the bindings you wrote, the detection evidence for each non-default,
and the next command: `/se-brief` for new work or `/se-deliver` if a
frontier already exists.
