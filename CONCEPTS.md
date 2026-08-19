# Concepts

Slice Engineering is a way of letting coding agents do real work without
letting them do unbounded work. The plugin is the portable form of a loop
that was first made concrete while building Revere.

## Thin slice

The unit of work is one independently testable, user-visible behavior with
explicit exclusions. If a slice cannot finish in one focused session, it is
two slices. Thin slices are not a project-management aesthetic. They are the
blast-radius control that makes autonomous review and delivery safe.

## Brief, not a durable plan

A **brief** is the why and what: behavior, acceptance criteria, exclusions,
and an optional hypothesis when the value is genuinely uncertain.

A **plan** is the how for one slice. It is a temp file. It is discarded after
the slice ships. Plans that become the system of record rot, and then agents
implement against fiction.

When work must survive a session or coordinate across agents, the brief lives
in a **ledger arc**. The arc has a **frontier**: the next undelivered slice.
`/se-deliver` runs against that frontier. It does not silently pick a
different slice.

## Skills compose

`/se-deliver` is an orchestrator. Each phase skill is the source of truth for
that phase. Duplicating a gate inside the orchestrator is how gates weaken.
If a phase needs to change, change the phase skill.

This is also why review cannot edit, and why shipping cannot hide inside
implementation. The reviewer must not be the person who just wrote the code,
and the implementer must not certify their own ship.

## Review is a gate

A review that produces a report and moves on is optional commentary.
Slice Engineering treats review as a stop condition:

- act on correctness, unclear intent, missing behavioral coverage, hidden
  coupling, and broken host conventions
- note, and do not loop on, style preferences and equally valid alternatives
- stop at `ship it` when remaining observations are preferences

Fresh context is the bias firewall. The reviewer inspects the diff, not the
story of how it was written. When the host cannot fork a subagent, the same
discipline is simulated: read the diff before reconstructing rationale.

## Tests are specifications

A test names one behavior. It specifies a business rule, not an
implementation. Awkward tests are design feedback. Config-like changes get a
characterization or regression test that protects the operational contract,
not a restatement of the edited line.

When current behavior is unclear, run the smallest relevant existing test
first, then write the failing spec, then implement.

## Knowledge promotion

Local agent memory is a cache. If a future teammate or another agent needs a
fact to avoid repeating work or making a wrong assumption, it belongs in a
shared home the host names in `.slice-engineering/config.yaml`.

Typical homes:

| Knowledge | Default home |
| --- | --- |
| Always-on agent rules | `AGENTS.md` |
| How we slice | `docs/engineering-philosophy.md` |
| Commands, architecture, testing, deploy | `docs/engineering-guide.md` |
| Repeatable procedures | `docs/sops/` |
| Architectural decisions | `docs/adrs/` |
| Shipped capability narrative | `docs/completed/changelog.md` |
| Queue, frontier, delivery record | ledger (`docs/ledger/` by default) |
| Review findings | `docs/tech-debt/` |

`/se-setup` scaffolds these homes from `templates/docs/` when they are
missing. It never overwrites a host file that already exists. The
placement procedure itself is `docs/sops/documentation-placement.md`.

`/se-reflect` writes evidence to the ledger and promotes only the facts that
belong in a broader home. It does not create a parallel `docs/solutions/`
corpus unless the host binds one.

## Bindings, not assumptions

The plugin does not know how you test, whether you ship to a default branch
or open a pull request, or where briefs live. `/se-setup` writes those
bindings. Skills that need a host fact read the bindings file. If a required
binding is missing, they stop and ask — they do not invent Revere's
conventions.

## What this is not

It is not Compound Engineering with the labels sanded off.

Compound Engineering's loop is brainstorm → plan → work → simplify →
report-only review → write `docs/solutions/`. That is a strong product. This
plugin's loop is brief → review-brief → deliver (TDD, review *gate*, bindable
ship) → reflect into the host's knowledge map.

Use Compound Engineering if you want a large catalog and a solutions corpus.
Use Slice Engineering if you want a small closed loop, compositional skills,
and a ship gate.

## Weekly changeability loop

Thin slices keep *new* work small. They do not by themselves stop a tree
from accumulating coupling, dead paths, and tests that no longer specify
behavior. `/se-review-codebase` and `/se-deliver-remediation-plan` are
the maintenance loop:

1. Assess changeability against Farley's dimensions. Incremental when a
   recent review exists; full when it does not.
2. Pause. The dated report and `remediation-plan.md` are written only
   after triage — the reviewer does not quietly queue deletions.
3. Deliver each pending item as its own `/se-deliver` slice. Invalidated
   premises fold back into the review skill's vetting rules.

The debt home is a queue, not a solutions corpus. Findings that are
really product work go on a ledger frontier instead.

## Skills improve from runs

A skill that grows from taste will rot. `/se-improve-skill-from-run`
treats one recorded run as evidence, proposes generalizable and
instruction-economical changes, and **stops**. Nothing is applied until
proposal IDs are approved. Recorders are provider-specific and optional;
the current conversation is valid Cursor evidence. Raw transcripts are
never dumped into the review.
