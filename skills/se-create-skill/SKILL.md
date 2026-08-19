---
name: se-create-skill
description: Create a new Slice Engineering skill package with valid frontmatter, a trigger description, and catalog updates. Use when adding or porting a workflow skill to this plugin.
disable-model-invocation: true
---

# Create Skill

Create one concise skill that a fresh agent can run. Success means the
package validates, the description says when to use it, and the catalog
lists it.

Treat `$ARGUMENTS` as the skill name and purpose.

## Contract

- Folder `skills/<name>/SKILL.md` with `name` matching the folder
- `name` is lowercase kebab-case and should start with `se-` in this plugin
- `description` states what it does *and* when to invoke it
- Include `$ARGUMENTS` in the body
- Side-effect skills set `disable-model-invocation: true`
- Review / read-only skills do not receive edit tools
- Behavior-focused instructions; fragile mechanics go in `scripts/`
- Provider-specific values resolve from
  `skills/_shared/agent-conventions.md`
- Host facts resolve from `skills/_shared/bindings.md`
- Do not hardcode a single product's paths

## After writing

1. Add a row to `docs/skills/README.md` and the README skill table.
2. Run `python3 scripts/validate_plugin.py`.
3. Do not add README, changelog, or install guides inside the skill
   folder.
4. After a real run exposes friction, use `se-improve-skill-from-run`
   rather than expanding the skill speculatively.

## Output

Paths created and validator result.
