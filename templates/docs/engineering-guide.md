# Engineering Guide

Shared engineering rules for this repository. How to slice work lives in
`docs/engineering-philosophy.md`. Where a new fact goes lives in
`docs/sops/documentation-placement.md`. The Slice Engineering loop itself
lives in the plugin — do not copy plugin skills or `CONCEPTS.md` here;
link them.

Host bindings: `.slice-engineering/config.yaml`.

## Essential Context

- **`docs/engineering-philosophy.md`** — thin slices, hypotheses, architectural coaching
- **`docs/sops/documentation-placement.md`** — knowledge homes and promotion
- **Bound ledger** — queue, frontiers, and delivery records (`knowledge_homes.queue`)
- **`docs/completed/changelog.md`** — shipped capability narrative
- **`docs/adrs/`** — decisions worth keeping
- **`docs/tech-debt/`** — review findings and remediation
- **`docs/sops/`** — repeatable procedures

Add product or architecture vision docs here when this repo has them.

## Commands

<!-- se-setup: replace this section with detected install / dev / test / lint commands. Leave a short list, not a tour. -->

Record the commands people and agents actually run. At minimum, name the
bound `verify_command`.

```text
verify: <verify_command from bindings>
```

## Architecture

<!-- se-setup: leave this section as a stub unless the host already has an obvious one-paragraph shape. Do not invent a stack. -->

Describe the runtime shape in a short paragraph and a directory tree.
Dependency direction belongs here once it exists. Empty is honest.

## Testing

Tests are specifications. Each test names one behavior. When current
behavior is unclear, run the smallest relevant existing test first. For
behavior changes, write a failing test, then implement.

Use the bound `verify_command` for the full gate when the change touches
shared contracts, schema, cross-module behavior, or before shipping. A
docs-only or mechanical change may use a focused check — say why.

This TDD rule is also in `AGENTS.md`. The duplication is intentional;
keep the two in sync.

## Boy Scouting

Leave code you are already touching a little better.

In scope: dead imports, unclear names in edited code, trivially clearer
logic, minor duplication you are already editing.

Out of scope: files you are not already changing, structural refactors,
anything that needs new tests or changes existing expectations.

Boy-scout work is a **separate commit** from the feature. If the cleanup
is larger than that, record it in the ledger instead of doing it now.

## Keeping Docs in Sync

Follow `docs/sops/documentation-placement.md`.

After a slice ships, `/se-reflect` updates the ledger and promotes only
the facts that belong in a broader home. Once an arc is fully delivered,
the code is the source of truth — do not backport routine follow-on
tweaks into the brief.

## Deployment

<!-- se-setup: fill from ship_mode / deploy / deploy_command / deploy_url. -->

- Default branch: `<default_branch>`
- Ship mode: `<ship_mode>`
- Deploy: `<deploy>`
