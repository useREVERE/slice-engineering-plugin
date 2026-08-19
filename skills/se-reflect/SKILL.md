---
name: se-reflect
description: Capture post-ship acceptance evidence, decide the hypothesis outcome and next-slice verdict, update the ledger, and promote durable knowledge to the host's named homes. Use after a slice ships.
disable-model-invocation: true
---

# Reflect

Turn a shipped, accepted slice into evidence and a next frontier. Success
means evidence is captured before interpretation, the hypothesis outcome
is decided, the ledger (if any) records the slice, and only facts that
belong in a broader home are promoted.

Treat `$ARGUMENTS` as the brief path, shipped slice name, and acceptance
evidence.

Read `skills/_shared/bindings.md`. Honor `ledger` and `knowledge_homes`.

## Evidence first

Record, omitting fields that do not apply:

```text
acceptance time (naive UTC if the host uses it, otherwise ISO-8601 UTC)
shipped SHA and ancestry vs default branch
verify command and result
deploy probe, if bound
user-visible behavior checked
```

Do not interpret until this block exists.

## Decisions

- **Hypothesis:** confirmed, rejected, or none. One sentence why.
- **Next-slice verdict:** plan-ready frontier, needs shaping, or arc
  closed.
- **Facts not to rediscover:** only things a future agent would get wrong
  without them.

## Ledger write

If `ledger` is `none` or the work was a conversation brief, write the
reflection in the conversation. Do not create a ledger.

If a ledger is bound, append a delivery-record entry to the arc brief and
update `Frontier`. Do not rewrite earlier delivery entries.

When a multi-slice arc has accumulated shipped specifications, invoke
`se-compact-brief` so the next session can plan the frontier without
carrying obsolete history. Do not compact a conversation brief. Do not
run `se-publish` from reflection — publishing is an explicit user verb.

There is no guarded external writer in this plugin. Write the brief file
directly and keep the complete intended document in working context so a
concurrent edit is visible in `git status` / diff before you save.

## Knowledge promotion

Follow `docs/sops/documentation-placement.md` when that file exists.
For each durable fact, choose the narrowest home in `knowledge_homes`:

- always-on agent rule → `agent_rules`
- repeatable procedure → `procedures`
- architectural decision → `decisions`
- shipped capability narrative → `shipped`
- queue / frontier / record → `queue` (the ledger)

Do not invent a `docs/solutions/` corpus. Do not copy the same policy into
two homes unless missing either copy is a safety risk; if you duplicate,
say that the copies must stay in sync.

## Output

Evidence block, hypothesis outcome, next frontier or closed, paths written,
and promotions made.
