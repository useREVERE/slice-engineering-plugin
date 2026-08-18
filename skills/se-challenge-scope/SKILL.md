---
name: se-challenge-scope
description: Challenge a proposal's scope and abstraction level — find the simplest implementation that preserves the right architectural commitment. Use when a plan or brief looks over-built.
disable-model-invocation: false
---

# Challenge Scope

Review a proposal for essential complexity. Success means separating current
need from speculative work, then naming the smallest architectural
commitment that preserves future optionality.

This is not a code review. Do not edit files.

Treat `$ARGUMENTS` as the proposal, brief, plan, or design sketch.

## Lens

1. **What can be removed?** Work that solves a future problem disguised as
   a current requirement. For each candidate: what problem are we solving
   *right now*?
2. **What decision is hard to reverse?** Preserve the interface, boundary,
   or data contract other code will depend on. Keep the implementation as
   simple as possible.

Overbuild signals: tables for data that does not exist, UI for unused
workflows, abstractions with one implementation, configuration systems for
speculative benefit, "while we're at it" extras.

Boy-scout cleanup in files already being modified is not scope creep when
it is small, separately committed, and needs no new tests or interface
changes.

## Output

```markdown
## Strip
- <item>: future need it pretended to serve; trigger that would make it real

## Keep
- <commitment>: why it is harder to reverse than the details around it

## Verdict
right-sized | over-built | under-committed
```

"YAGNI" alone is not enough. Name the trigger.
