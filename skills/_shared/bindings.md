# Host Bindings

Skills that need a host-project fact read this file's contract, then load
`.slice-engineering/config.yaml` from the current repository root. An optional
`.slice-engineering/config.local.yaml` overlays it and must stay untracked.

If a required key is missing or empty, stop and ask. Do not invent values
from another project, and do not assume `make test`, `origin/main`, Render,
or an external ledger.

## Discovery

```text
repo root = git rev-parse --show-toplevel
config    = <repo>/.slice-engineering/config.yaml
local     = <repo>/.slice-engineering/config.local.yaml
```

If `config.yaml` is missing, tell the user to run `/se-setup` and stop any
phase that needs a binding (verify, ship, durable brief write). Read-only
review may continue with git-derived defaults: the default branch from
`origin/HEAD` or `main`, and no verify command.

## Keys

| Key | Meaning | Default if `/se-setup` has not been run |
| --- | --- | --- |
| `default_branch` | Integration branch | `main` if `origin/HEAD` is unset |
| `verify_command` | Command that must pass before ship | *required for ship of runtime changes* |
| `ship_mode` | `trunk` or `pull-request` | `pull-request` |
| `deploy` | `none`, `command`, or `url` | `none` |
| `deploy_command` | Host deploy or health command | empty |
| `deploy_url` | Public health URL to fetch after ship | empty |
| `ledger` | `in-repo`, `external`, or `none` | `in-repo` |
| `ledger_root` | Repo-relative ledger directory | `docs/ledger` |
| `external_ledger_path` | Absolute or `~/` path to an external ledger checkout | empty |
| `worktrees` | Whether delivery uses git worktrees | `false` |
| `knowledge_homes` | Map of knowledge kinds to paths | see template |

## Ledger paths

When `ledger` is `in-repo`:

```text
<ledger_root>/arcs/<slug>/brief.md
<ledger_root>/README.md
```

When `ledger` is `external`, use `external_ledger_path` the same way.
When `ledger` is `none`, keep briefs in the conversation. Do not create a
ledger directory.

## Skill invocation

Resolve the host agent's invocation syntax from
`skills/_shared/agent-conventions.md`. In this document, `/se-name` means
"invoke the `se-name` skill."
