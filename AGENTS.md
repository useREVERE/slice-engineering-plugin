# Slice Engineering plugin

This repository *is* the plugin. Changes here are changes to the workflow
other projects will run.

## Rules

- Skills stay provider-neutral. Resolve Claude Code, Codex, and Cursor
  differences from `skills/_shared/agent-conventions.md`.
- Skills that need a host fact read `.slice-engineering/config.yaml` via
  `skills/_shared/bindings.md`. Do not hardcode a product's test command,
  default branch, deploy probe, or ledger path.
- Do not add Revere product skills, Render runbooks, or private ledger paths.
- Side-effect skills use `disable-model-invocation: true` unless the skill
  is meant to fire from inside another workflow (for example `se-commit`).
- Review skills do not get edit tools.
- Every skill includes `$ARGUMENTS` explicitly.
- Keep always-on rules in `rules/` small. Detail lives in the skill that
  needs it.
- Version numbers in plugin manifests stay in lockstep. Bump them together.

## Verification

```bash
python3 scripts/validate_plugin.py
python3 -m unittest discover -s tests -q
```

## Commits

One logical change per commit. Do not commit secrets. Do not mix a skill
behavior change with a mechanical rename.
