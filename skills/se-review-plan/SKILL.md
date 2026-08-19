---
name: se-review-plan
description: Review an implementation plan through the lens of Dave Farley's Modern Software Engineering, including a scope challenge. Use after a temp plan exists and before se-execute.
disable-model-invocation: false
---

# Review Plan

Evaluate whether an implementation plan can guide safe, incremental,
test-driven delivery. Success means sequencing risks, scope creep, hidden
dependencies, and missing feedback loops are surfaced before execution.

This skill is report-only. Do not edit the plan, the brief, or product
code.

## Inputs and Outputs

**Input:** An implementation plan and, when available, its brief.

**Output:** Unified prioritized findings and a verdict: `ready`,
`ready after minor edits`, or `not ready`.

Treat `$ARGUMENTS` as the plan path, brief context, or review qualification.

Read `skills/_shared/bindings.md`. Load `knowledge_homes.philosophy` (default
`docs/engineering-philosophy.md`) before judging. If that file is missing,
say so and continue with the evaluation lens below rather than inventing
host policy.

## Review Model

Use two perspectives:

- **Structural review:** sequencing, TDD, feedback loops, independence, and
  reversibility. Run this directly.
- **Scope challenge:** unnecessary work disguised as implementation detail.
  Invoke `se-challenge-scope` with the plan content so it judges in fresh
  context, independent of your structural reasoning.

Synthesize both into one prioritized set of findings. Where they agree, say
so — that is high-confidence signal. Where they disagree, present both
perspectives and your judgment on which is right.

## Evaluation Lens

- each step starts with or names a failing behavioral test unless docs-only
- planned mocks are limited to external boundaries or explicitly justified as
  boundary-contract tests
- steps are independently committable and leave the codebase green
- riskiest assumptions and external walking skeletons happen early; if an
  external-service walking skeleton is bundled with additional integration
  points in the same slice, flag it — the skeleton should be proven alone
- behavior changes, refactors, and boy-scout cleanup are separated; do not
  flag small boy-scout cleanup in already-touched files as scope creep
- data flows between steps without redundant re-fetching or hidden coupling
- durable interfaces/contracts are introduced deliberately, before
  implementations that depend on them
- blast radius: if a step turns out wrong, how much rework follows? Could
  steps be reordered to fail cheaper?
- plan acknowledges where it follows or departs from brief Research Notes;
  silent inheritance of brief assumptions is a red flag
- verification commands and failure behavior are explicit
- privacy/security considerations appear when relevant

Review the plan; do not extend the product scope or redesign without a
finding.

## Finding Format

```markdown
### [P1|P2|P3] Short finding title

**Evidence:** plan step or omission
**Why it matters:** feedback, testability, scope, or reversibility risk
**Suggested fix:** smallest plan change that addresses it
```

Priorities:

- **P1:** plan cannot safely guide implementation
- **P2:** likely to create rework or hide risk
- **P3:** useful improvement with limited risk impact

## Output

Findings first. Say when structural review and scope challenge agree. If the
plan is solid, explain why the sequencing works.

End with:

```markdown
**Verdict:** ready | ready after minor edits | not ready
```

When findings require plan changes, follow the verdict with:
`**Refine the plan based on the feedback above.**` Omit that instruction when
the verdict is `ready` and there are no findings.

## Stop Rules

Stop searching when the plan and linked brief provide enough evidence for the
verdict. Do not invent requirements or implementation steps; flag missing
decisions instead.

$ARGUMENTS
