---
name: se-review-brief
description: Review a brief for behavioral clarity, slice focus, scope discipline, and plan-readiness, or review a completed brief for delivery-record fidelity. Use before planning or delivering, and after reflection.
disable-model-invocation: false
---

# Review Brief

This is feedback only. Do not edit the brief unless the caller is
`se-brief` applying mechanical fixes the user already authorized.

Treat `$ARGUMENTS` as the brief path, conversation-brief marker, or review
focus.

## Lenses

1. **Behavior.** Can an implementer tell what will be true for a user or
   operator without inventing product decisions?
2. **Slice.** Is this one increment? If two independently shippable
   behaviors are bundled, say so.
3. **Exclusions.** Are the tempting extras named and out of scope?
4. **Testability.** Could acceptance be checked without reading the
   author's mind?
5. **Frontier.** For an arc, is exactly one next slice named, and does it
   match the delivery record?
6. **Plan leakage.** Implementation sequencing belongs in `se-plan`, not
   here. Flag it.

After a shipped slice, also check that the delivery record names evidence
(SHA, verify command, acceptance) and that the new frontier is still
plan-ready — or that the arc is honestly closed.

## Verdicts

- **plan-ready** — `/se-deliver` or `/se-plan` can start
- **needs shaping** — name the missing decisions
- **too big** — propose the split
- **closed and trustworthy** — post-ship record only

Do not loop on wording preferences. Act on missing acceptance, hidden
second slices, and a frontier that disagrees with the record.
