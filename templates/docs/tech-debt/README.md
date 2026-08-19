# Tech debt

Codebase review findings and the active remediation plan live here.

Weekly changeability loop:

1. `/se-review-codebase` — Farley-lens assessment, dated report, then a
   pause before any plan write
2. `/se-deliver-remediation-plan` — one `/se-deliver` per pending item
   until the queue is empty or blocked

Files:

- One dated review document per pass (`YYYY-MM-DD-codebase-review.md`)
- `remediation-plan.md` — the pending-item queue
- `remediation-history.md` — closed-item archive

Review findings are not the planning ledger. Promote a finding onto a
ledger frontier when it is time to deliver it as product work rather
than a bounded refactor.
