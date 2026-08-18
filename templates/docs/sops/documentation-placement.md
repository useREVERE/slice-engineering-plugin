# Documentation Placement

Use this procedure when adding, moving, promoting, or deliberately
duplicating durable knowledge. Ordinary edits within an established
canonical home do not need a placement review.

Read host bindings from `.slice-engineering/config.yaml` before treating
the default paths below as literal. If a `knowledge_homes` entry exists,
that path wins.

## 1. Decide Whether the Knowledge Should Persist

Ask whether a future teammate or agent needs the information to avoid
repeated work or a wrong assumption. If not, keep it in the current
conversation or working notes. Agent memory and IDE state are caches, not
durable team knowledge.

If the information is machine- or user-specific, put it in a gitignored
root-level local note (`CLAUDE.local.md` or the host's equivalent). Do not
place team knowledge there.

## 2. Choose the Narrowest Canonical Home

Choose the home whose readers need the knowledge while doing their work:

| Knowledge | Canonical home |
| --- | --- |
| Broadly applicable or safety-critical agent behavior | `AGENTS.md` (`knowledge_homes.agent_rules`) |
| Provider-specific workflow integration | Thin `CLAUDE.md` wrapper or the host's provider sidecar |
| Instructions needed while performing a workflow | A skill — in this plugin, or a host skill if the host has one |
| Agent workflow design and skill composition | The Slice Engineering plugin (`CONCEPTS.md` and `skills/`). Do not copy those into the host. |
| How we slice and challenge scope | `docs/engineering-philosophy.md` (`knowledge_homes.philosophy`) |
| Repeatable task or maintenance procedure | `docs/sops/` (`knowledge_homes.procedures`) |
| Stable architecture, commands, testing, or deployment | `docs/engineering-guide.md` (`knowledge_homes.guide`) |
| Consequential architectural decision or retired alternative | `docs/adrs/` (`knowledge_homes.decisions`) |
| Codebase review finding and active remediation plan | `docs/tech-debt/` (`knowledge_homes.debt`) |
| Queue, frontier, or delivery record | The bound ledger (`knowledge_homes.queue` / `ledger_root`) |
| Shipped capability narrative | `docs/completed/changelog.md` (`knowledge_homes.shipped`) |
| Machine- or user-specific quirk | Gitignored root-level local note |

Prefer the relevant existing document over creating a new one. If no
existing home fits, create the narrowest focused document in the
appropriate category and give it one clear owner.

## 3. Add the Smallest Useful Pointer

Do not copy narrow detail into a broader or auto-loaded file merely to
improve discovery. Leave a short routing pointer at the place where a
reader will decide they need the detail. Auto-loaded files such as
`AGENTS.md` should carry the rule or routing decision needed in every
relevant session, not the full procedure or history behind it.

Before adding a pointer, search for an existing route and extend it:

```bash
rg -n '<topic-or-destination>' AGENTS.md CLAUDE.md docs
```

## 4. Duplicate Only for Deliberate Emphasis

Links are the default. Duplicate policy only when missing either copy
would create enough safety or execution risk to justify maintaining both.
Each copy must say that the duplication is intentional, name the other
copy, and require the two to stay in sync.

Do not remove sanctioned duplication as cleanup. The TDD rule
intentionally appears in both `AGENTS.md` and `docs/engineering-guide.md`;
both locations carry the keep-in-sync contract.

## 5. Promote Only When the Recurring Cost Is Justified

Move or summarize knowledge into a broader context when at least one of
these is true:

- it applies across most repository work
- missing it could cause material safety, data, or deployment harm
- repeated misses show that the existing pointer or narrow home is not
  discoverable enough

Try a better pointer before promoting detailed content solely because it
was hard to find once. When promoting, keep the detailed canonical home
and move only the minimum rule or routing signal needed by the broader
audience.

## 6. Verify the Placement

Before finishing:

1. Search for overlapping guidance and reconcile contradictions.
2. Confirm broader documents link to the canonical home instead of
   restating it.
3. Confirm any intentional duplicate names its counterpart and
   keep-in-sync obligation.
4. Add or update a focused contract test when losing a routing pointer
   would silently orphan important guidance.
