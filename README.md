# Slice Engineering

AI skills that keep each unit of work a **thin vertical slice** — briefed as
behavior, delivered through a review gate, then reflected so the next frontier
is ready.

This plugin packages the agentic development loop used to build
[Revere](https://github.com/useREVERE/revere-policy-intelligence). It is
intentionally not a clone of [Compound Engineering](https://github.com/EveryInc/compound-engineering-plugin).
The packaging is similar (Cursor, Claude Code, Codex). The methodology is not.
See [CONCEPTS.md](CONCEPTS.md).

## Install

### Cursor

In Cursor Agent chat:

```text
/add-plugin slice-engineering
```

Or add this repository from the plugin marketplace once it is listed. Until
then, load a local checkout:

```bash
cursor-agent --plugin-dir "$PWD"
```

### Claude Code

```text
/plugin marketplace add useREVERE/slice-engineering-plugin
/plugin install slice-engineering
```

Local checkout:

```bash
claude --plugin-dir "$PWD"
```

### Codex

Add this repository as a custom marketplace, then install
`slice-engineering@slice-engineering-plugin`.

CLI:

```bash
codex plugin marketplace add useREVERE/slice-engineering-plugin
codex plugin add slice-engineering@slice-engineering-plugin
```

In Codex, invoke skills with `$se-brief` rather than `/se-brief`.

### After install

In any host project:

```text
/se-setup
```

That writes `.slice-engineering/config.yaml` — the bindings file that tells
every skill how *this* repo tests, ships, and records work — and copies
missing documentation homes from `templates/docs/` (philosophy, engineering
guide skeleton, documentation-placement, empty SOP/ADR/changelog/tech-debt
directories). Existing docs are left alone. Do not skip it.

## Philosophy

**A thin slice is the precondition for letting an agent run.**

Autonomous review and delivery are only safe when the blast radius is small.
Slice Engineering makes that the unit of work:

- one user-visible behavior
- explicit exclusions
- independently testable
- finishable in one focused session

Skills compose. `/se-deliver` orchestrates `/se-plan`, `/se-execute`,
`/se-review-loop`, `/se-ship`, and `/se-reflect`. It does not absorb them.
A review skill cannot edit. A planning skill cannot ship. Prose is a
suggestion; tool boundaries are the guarantee.

Review is a **ship gate**, not a report. The loop converges on `ship it` or
stops. Preferences are noted and left alone.

Knowledge is promoted to the **narrowest durable home** the host names —
agent rules, procedures, decisions, shipped history, or the planning ledger —
not dumped into a single solutions folder.

## Workflow

```text
brief → review-brief → deliver
                          ├─ plan          (temp)
                          ├─ execute       (TDD)
                          ├─ review-loop   (fresh-context gate)
                          ├─ ship          (bindings)
                          └─ reflect       (evidence + next frontier)
```

| Skill | Purpose |
| --- | --- |
| [`/se-setup`](skills/se-setup/SKILL.md) | Bind this repo and scaffold missing docs homes |
| [`/se-brief`](skills/se-brief/SKILL.md) | Shape one thin slice as a quick brief or a durable ledger arc |
| [`/se-review-brief`](skills/se-review-brief/SKILL.md) | Pressure-test a brief for plan-readiness or delivery-record fidelity |
| [`/se-plan`](skills/se-plan/SKILL.md) | Write a throwaway implementation plan for one slice |
| [`/se-deliver`](skills/se-deliver/SKILL.md) | Orchestrate plan → execute → review → ship → reflect |
| [`/se-execute`](skills/se-execute/SKILL.md) | Implement with TDD and scoped commits |
| [`/se-review`](skills/se-review/SKILL.md) | Fresh-context, report-only review of a diff |
| [`/se-review-loop`](skills/se-review-loop/SKILL.md) | Review → fix → re-review until `ship it` or a bounded stop |
| [`/se-ship`](skills/se-ship/SKILL.md) | Integrate, verify, and publish using host bindings |
| [`/se-reflect`](skills/se-reflect/SKILL.md) | Capture evidence, decide the next frontier, promote knowledge |
| [`/se-challenge-scope`](skills/se-challenge-scope/SKILL.md) | Strip speculative work; keep the hard-to-reverse commitment |
| [`/se-commit`](skills/se-commit/SKILL.md) | One logical git commit a future agent can understand |
| [`/se-handoff`](skills/se-handoff/SKILL.md) | Compact the session for a fresh agent |
| [`/se-investigate`](skills/se-investigate/SKILL.md) | Evidence-driven diagnosis with a deliver-ready handoff |
| [`/se-prototype`](skills/se-prototype/SKILL.md) | Throwaway prototype to answer a state or UI question |
| [`/se-create-skill`](skills/se-create-skill/SKILL.md) | Author a new skill without recreating provider drift |

A small, low-risk change may skip the durable ledger and use a
conversation-scoped brief. `/se-deliver` still runs the same gates.

## Quick example

```text
/se-setup
/se-brief make retry exhaustion visible to the operator
/se-review-brief
/se-deliver
```

Or, when the slice is already clear:

```text
/se-deliver the frontier
```

When the input is a bug rather than a new behavior:

```text
/se-investigate checkout creates duplicate invoices
/se-deliver
```

## What this plugin does not include

Revere-specific product skills (source onboarding, hearing upload, customer
provisioning) stay in the product repo. This plugin ships the **operating
system**, not the product.

It also does not assume trunk-based `main`, Render, a separate ledger
repository, or a particular language. Those are bindings `/se-setup` writes.

## Local development

```bash
python3 scripts/validate_plugin.py
python3 -m unittest discover -s tests -q
```

## License

[MIT](LICENSE)
