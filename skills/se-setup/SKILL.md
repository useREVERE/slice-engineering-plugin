---
name: se-setup
description: Bind Slice Engineering to this repository by writing .slice-engineering/config.yaml and scaffolding missing documentation homes. Use when installing the plugin in a new or existing project, or when test/ship/ledger/docs conventions are missing or wrong.
disable-model-invocation: true
---

# Setup

Write host bindings and, when missing, the documentation homes those
bindings name. Success means `.slice-engineering/config.yaml` matches this
repository, missing doc homes were created from plugin templates, existing
docs were left alone, and the user knows what was chosen and why.

Treat `$ARGUMENTS` as an explicit default branch, verify command, ship mode,
ledger location, or "docs only" / "skip docs".

## Inspect

From the repository root (`git rev-parse --show-toplevel`):

- default branch from `origin/HEAD`, else `main`
- existing test entry points: `Makefile` (`test` target), `package.json`
  scripts, `pyproject.toml`, `go.mod`, `Cargo.toml`
- whether `AGENTS.md` already exists
- whether `docs/engineering-guide.md`, `docs/engineering-philosophy.md`,
  `docs/sops/`, `docs/adrs/`, `docs/completed/`, `docs/tech-debt/`,
  `docs/ledger/`, or `.slice-engineering/` already exist
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

## Write bindings

1. Create `.slice-engineering/` if needed.
2. Write `config.yaml` without clobbering a file that already looks
   intentional — update only empty or still-template keys, and report what
   you left alone.
3. Ensure `.slice-engineering/config.local.yaml` is gitignored.

## Scaffold documentation

Read `templates/docs/README.md` as the inventory. Copy a template to the
host path only when the destination is **missing**. Never overwrite an
existing file, even if it looks thin or outdated. Report each skip.

Default is to scaffold missing homes. Skip this entire step if the user
said "skip docs". If they said "docs only", write docs and leave bindings
untouched unless `config.yaml` is missing.

For each missing file:

| Host path | Template |
| --- | --- |
| `docs/engineering-philosophy.md` | `templates/docs/engineering-philosophy.md` |
| `docs/engineering-guide.md` | `templates/docs/engineering-guide.md` |
| `docs/sops/documentation-placement.md` | `templates/docs/sops/documentation-placement.md` |
| `docs/sops/README.md` | `templates/docs/sops/README.md` |
| `docs/adrs/README.md` | `templates/docs/adrs/README.md` |
| `docs/adrs/TEMPLATE.md` | `templates/docs/adrs/TEMPLATE.md` |
| `docs/completed/changelog.md` | `templates/docs/completed/changelog.md` |
| `docs/tech-debt/README.md` | `templates/docs/tech-debt/README.md` |
| `docs/tech-debt/remediation-plan.md` | `templates/docs/tech-debt/remediation-plan.md` |
| `docs/tech-debt/remediation-history.md` | `templates/docs/tech-debt/remediation-history.md` |
| `<ledger_root>/README.md` | `templates/docs/ledger/README.md` — only if `ledger` is `in-repo` |

Do not create a sample ledger arc. Do not copy plugin `CONCEPTS.md` or
skills into the host.

### Fill slots, do not invent a stack

When creating `docs/engineering-guide.md`, replace the marked placeholders
with detected facts only:

- Commands: the detected install/dev/test commands and `verify_command`
- Deployment: `default_branch`, `ship_mode`, `deploy` / `deploy_command` /
  `deploy_url`
- Architecture: leave the stub unless a one-paragraph shape is already
  obvious from the tree. Do not invent layers or a framework.

When `docs/engineering-guide.md` already exists, do not merge philosophy,
boy scouting, or placement into it. Add at most a one-line pointer to
`.slice-engineering/config.yaml` if that pointer is absent — and only if
the user wants the pointer.

### AGENTS.md

If `AGENTS.md` is missing, offer `templates/AGENTS.md` and write it only
when the user wants a starter. If it exists, add at most a short pointer
to `.slice-engineering/config.yaml` and `docs/sops/documentation-placement.md`
when those files now exist. Do not rewrite their rules.

## Output

Report:

- bindings written or left alone, with detection evidence
- each doc path created
- each doc path skipped because it already existed
- the next command: `/se-brief` for new work, `/se-deliver` if a
  frontier already exists, or `/se-review-codebase` for the weekly
  changeability loop
