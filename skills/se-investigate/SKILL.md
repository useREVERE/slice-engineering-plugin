---
name: se-investigate
description: Investigate defects, regressions, and production failures with evidence-driven hypothesis testing. Use when behavior is wrong and the user wants cause, countermeasures, and a deliver-ready handoff — not an immediate fix.
disable-model-invocation: false
---

# Investigate

Find the immediate cause and the useful root causes. Do not implement the
fix unless the user explicitly converts this into `/se-deliver`.

Treat `$ARGUMENTS` as the symptom, report, or reproduction.

## Method

1. Restate the failing behavior and the expected behavior.
2. Reproduce or bound where reproduction is impossible. Write down the
   evidence, not the theory.
3. Form two or three hypotheses that could produce that evidence.
4. Design the cheapest observation that would kill a hypothesis.
5. Run it. Drop dead hypotheses. Do not add a new one until one dies.
6. Separate immediate cause (what to change) from root causes (why the
   defect was easy to ship).

Prefer existing tests, logs, and git archaeology over new instrumentation.
Read `skills/_shared/bindings.md` if you need `verify_command`.

## Handoff

End with a brief-shaped recommendation:

- the behavior fix as one slice
- acceptance (the failing case now passes; nearby cases still pass)
- exclusions (the cleanup that is not required to restore the behavior)
- suggested first test

Invite `/se-deliver` rather than starting it.
