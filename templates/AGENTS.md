# Agentic coding

This project uses [Slice Engineering](https://github.com/useREVERE/slice-engineering-plugin).
Host bindings live in `.slice-engineering/config.yaml`.

## Thin slices

Work in one independently testable, user-visible behavior at a time. State
what is out of scope. If it cannot finish in one focused session, split it.

## Tests are specifications

When current behavior is unclear, run the smallest relevant existing test
first. For behavior changes, write a failing test that names the rule, then
implement. Use the host `verify_command` for the full gate when the change
touches shared contracts or before shipping.

## Review before ship

Every behavior change gets a fresh-context review before it ships. Review is
a gate: fix correctness and missing coverage; do not loop on preferences.

## Knowledge promotion

Do not store team knowledge only in agent memory. Put durable facts in the
homes named under `knowledge_homes` in `.slice-engineering/config.yaml`.
How to choose a home: `docs/sops/documentation-placement.md`. How to
slice work: `docs/engineering-philosophy.md`. Host handbook:
`docs/engineering-guide.md`. The Slice Engineering loop stays in the
plugin — do not copy it into this repo.

## Secrets

Never commit credentials, `.env` files, or machine-specific absolute paths.
