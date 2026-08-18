# Host documentation templates

`/se-setup` copies these into a host repository only when the destination
is missing. It never overwrites a file that already exists.

| Template | Host path | When to create |
| --- | --- | --- |
| `engineering-philosophy.md` | `docs/engineering-philosophy.md` | Missing |
| `engineering-guide.md` | `docs/engineering-guide.md` | Missing. Fill Commands / Testing / Deploy from detected bindings. Leave Architecture empty if unknown. |
| `sops/documentation-placement.md` | `docs/sops/documentation-placement.md` | Missing |
| `sops/README.md` | `docs/sops/README.md` | Missing |
| `adrs/README.md` | `docs/adrs/README.md` | Missing |
| `adrs/TEMPLATE.md` | `docs/adrs/TEMPLATE.md` | Missing |
| `completed/changelog.md` | `docs/completed/changelog.md` | Missing |
| `tech-debt/README.md` | `docs/tech-debt/README.md` | Missing |
| `ledger/README.md` | `<ledger_root>/README.md` | Missing and `ledger` is `in-repo` |

Do not copy plugin `CONCEPTS.md` or skill files into the host. Workflow
design stays in the plugin. The host gets a pointer from
`docs/engineering-guide.md` and `AGENTS.md`.
