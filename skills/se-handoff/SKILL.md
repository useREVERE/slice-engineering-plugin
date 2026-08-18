---
name: se-handoff
description: Compact the current session into a handoff document for a fresh agent. Use when switching sessions, providers, or people mid-slice.
disable-model-invocation: false
---

# Handoff

Write a self-contained handoff a new agent can pick up without this
conversation. Success means the next agent knows the goal, the current
phase, the evidence so far, and the first safe action.

Treat `$ARGUMENTS` as a destination path or "conversation only".

Default destination is a temp file. Do not commit the handoff. Do not
write it into the ledger unless the user asks.

## Contents

- outcome and acceptance (or a pointer to the brief path)
- phase: briefing, planning, executing, reviewing, shipping, reflecting
- branch, dirty files, last commits
- verify commands already run and their results
- open product decisions
- first safe next command (`se-deliver`, `se-review-loop`, …)
- what not to redo

Do not include secrets, `.env` values, or paste entire diffs.

## Output

The handoff path or the full handoff in conversation, plus the recommended
next skill.
