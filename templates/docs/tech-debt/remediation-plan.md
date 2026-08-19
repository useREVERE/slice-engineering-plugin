# Remediation Plan

**Last updated:** YYYY-MM-DD
**Status:** No pending entries. `/se-review-codebase` has not queued work
yet, or the last cycle already shipped.

Item numbers renumber as entries ship; cite entries by title, not
number, in anything that outlives one delivery.

This is the active queue for high-priority technical debt surfaced by
codebase reviews. Keep it short enough that a fresh agent can read it
before starting a refactor.

---

## How to use this file

`/se-review-codebase` surfaces debt. After triage, add only the
refactors selected for near-term work here. This section is the queue
contract — `se-review-codebase` and `se-deliver-remediation-plan`
reference it rather than restating it.

### Entry format

Each pending refactor must be:

- **Self-contained:** a fresh session can implement it from this
  section alone
- **Concrete:** file paths, line numbers, excerpts
- **Honest about scope:** all files that need changing
- **Machine-checkable:** a command plus expected output, never "confirm
  it works"
- **Anchored:** **Origin** (dated review `§` section) and **As-of**
  (short SHA). A future session runs `git diff <sha>..HEAD -- <files>`
  before trusting the entry
- **Right-sized:** one session; break larger work into numbered
  sub-refactors

### Routing

Every surviving structural finding has one destination here:

- **Pending:** independently valuable now. Ordered by leverage; work
  top-down
- **Delegated to ledger work:** only with the user's approval, naming
  the owning arc; reactivate if that arc is abandoned or ships without
  resolving the finding
- **Deferred:** valid but not yet justified. Every deferral records a
  **named promotion trigger**
- **Invalidated:** premise disproven. Record the disproof so it is not
  re-derived

### Completing work

After a refactor ships, in the same change: remove the entry from its
queue section, add a row to the current-cycle table, and move the full
completed spec — with delivery evidence — to `remediation-history.md`
in this same directory. Never edit completed records retroactively.

---

## Pending Refactors

None.

---

## Delegated to ledger work

None.

---

## Deferred After Scope Challenge

None.

---

## Invalidated

None.

---

## Source reviews

None yet.

---

## Current cycle

| Shipped | Title | SHA |
| --- | --- | --- |
| — | — | — |
