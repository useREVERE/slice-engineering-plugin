---
name: se-improve-skill-from-run
description: Review a skill against evidence from one real run and improve it in two phases — propose evidence-backed, generalizable, instruction-economical changes, then apply only later-approved proposals. Use after a skill run felt sticky, failed a stop rule, or needed a workaround, or when given a session id, transcript path, or skill name.
disable-model-invocation: true
---

# Improve Skill From Run

Treat the recorded run as the evidence layer for a skill feedback loop.
Success means the target skill becomes easier, safer, or more reliable based
on **what actually happened in a run** — not abstract preference — without
overfitting one incident or accumulating instructions indefinitely.

Each provider reads its own recorder. Resolve the evidence source from
`skills/_shared/agent-conventions.md`. Do not invent a product's session
store, and do not require a recorder the host does not have.

Treat `$ARGUMENTS` as the target skill name, a session id, a transcript
path, or an autonomy note.

## Two-Phase Contract

Always separate review from implementation:

1. **Review:** inspect the evidence, complete the finding sweep, propose
   changes, and stop for user approval. Do not edit any skill file.
2. **Apply:** only after a later user message explicitly approves all or
   selected proposal IDs, apply that subset and validate it.

The initial request never counts as implementation approval, including
requests to "review and improve." State the active phase. If the target
changes between phases, refresh affected findings before editing.

## Guardrails

- The run is the evidence layer, not the reviewer. You do the judging.
- **Never dump whole transcript lines** — they carry full system prompts and
  large tool outputs that swamp the review. Work from compact indexes; go
  deeper only with bounded `jq` filters, never `cat` or unbounded search
  across the raw file.
- Separate skill issues from code bugs, tool/MCP failures, model mistakes,
  and user preference. Only genuine skill issues belong in a proposal.
- Stay inside the target skill package and its directly associated tests or
  validator fixtures. A production bug exposed by the trace is a non-skill
  finding — route it to `se-investigate`, do not fix application code you
  happened to read.
- Do not treat one observed workaround as a reusable workflow rule.
- Keep incident-specific paths, IDs, commands, and error strings in the
  evidence report unless the target skill inherently owns them.
- **Preserve validation integrity:** hand any sanity-checker the skill, the
  trace, and the diff — never your diagnosis of what the fix should be.
- Use local evidence only. Do not log in, configure remotes, or push
  session data unless explicitly asked.
- If evidence must leave the machine, transfer compact indexes after the
  user inspects them — never a raw transcript.

## Phase 1: Review

1. **Identify the target and the run.**
   Resolve the target skill directory. Search, in order, and follow
   symlinks to the real path:
   - `skills/<name>/`
   - `.cursor/skills/<name>/`
   - `.claude/skills/<name>/`
   - `.agents/skills/<name>/`
   Never replace a mount symlink with a real file. Edit the canonical
   path the symlink points at.

   Resolve the run from `$ARGUMENTS` or Agent Conventions (session id,
   current conversation, named skill's last run, or an explicit file).
   If multiple skills or runs are plausible and the choice would change
   the review, ask one concise question.

2. **Export evidence and set the boundary.**
   Use the provider exporter from Agent Conventions. Read compact indexes
   in this order: metadata, skill spans (if present), user messages, tool
   calls, failures.

   **Claude Code:** bundled
   `skills/se-improve-skill-from-run/scripts/export_claude_run.sh`
   (`--help` owns selectors). Default output is under `~/.claude/`.

   **Codex:** if a session recorder is on `PATH`, use it to list/export
   a run into compact indexes. If none is installed, ask for a transcript
   path or treat the current conversation as **partial** evidence and say
   so. Do not install a recorder as part of this skill.

   **Cursor:** the current conversation is first-class evidence. Build
   compact indexes in the runtime temp dir (user prompts, tool failures,
   files touched, stop-rule hits). An explicit path or cloud-agent
   transcript file is valid; still never dump it raw.

   State the review boundary before analysis: the smallest completed run
   the user named, plus follow-up corrections about that same outcome.

3. **Read the target skill.**
   Read `SKILL.md`; check frontmatter for stale description or trigger
   wording and wrong tool scoping. Read bundled scripts or references only
   when the trace shows they were used or should have existed. Record
   the repository HEAD SHA as the review anchor — Phase 2 diffs the
   target against it.

4. **Sweep for friction — all categories, not just the first hit:**
   triggering, preflight, workflow order, stop rules, validation, reusable
   tooling, context economy, hook and permission friction, and safety.
   Classify every category as `patch candidate`, `proposal`, `non-skill
   issue`, or `no finding`.

5. **Complete the evidence inventory.**
   Check at least user prompts, the final answer, tool failures,
   validation output, files touched, and available commit or diff
   summaries. If evidence is incomplete, say which part is missing and
   whether that makes the review partial.

6. **Pass the causal and generalization gate.**
   For each candidate: the friction and mechanism; how the target caused,
   permitted, or failed to prevent it; the missing control and general
   failure class; a materially different run the change would help; one
   case where it does not apply. High confidence requires a supported
   causal link addressing the general class, not the last command or error.

7. **Pass the instruction-economy gate.**
   Prefer, in order: tighten or replace an existing rule; remove wording
   made obsolete by the change; move conditional detail to a direct
   reference; encode deterministic mechanics in a script or validator;
   add core prose only for a genuine judgment or safety requirement.
   Report the approximate size delta per edit and justify growth; default
   to net-neutral or smaller. Then assess the accumulated file: when the
   target has grown materially since its last consolidation, emit a
   consolidation proposal alongside the others.

8. **Stop for approval.**
   Return stable proposal IDs, the finding sweep, causal and
   generalization evidence, instruction deltas, and non-skill findings.
   State explicitly that nothing was applied. Ask the user to approve
   all, approve selected IDs, or request revisions. End the turn.

## Phase 2: Apply Approved Changes

1. Check branch attachment, worktree status, HEAD, and the target
   directory against the Phase 1 anchor; fetch origin when permitted.
   Fast-forward only a clean attached branch. In a detached or dirty
   worktree, compare the target against both the anchor and fetched
   `origin/<default_branch>` without changing unrelated state. Surface
   conflicting target changes, and refresh or drop proposals already
   applied or invalidated.
2. Tell the user which approved files and proposal IDs you are applying.
3. Apply only the approved subset. If adding or changing a bundled
   script, run a representative invocation to prove it works. Validate:
   - Slice Engineering plugin skills: `python3 scripts/validate_plugin.py`
   - Other host skills: name matches folder, description present; run the
     host's skill validator if one is documented. `git diff --check` on
     every skill edit. For text-only changes no app suite is required —
     state the checks used and their scope.
4. Run a short second pass over the original inventory: consolidate
   duplication the patch introduced or exposed, but add no unapproved
   behavioral changes.

If the improved skill lives in this plugin, update the catalog only when
the trigger description or side-effect boundary changed.

## Output

Phase 1:

```markdown
## Skill Improvement Summary
- **Target skill:** name/path
- **Evidence:** run/session id + exported artifact dir, and the review boundary
- **Finding sweep:** categories reviewed, with patch/proposal/non-skill counts
- **Proposals:** IDs, causal mechanism, generalization test, instruction delta
- **Applied:** none — awaiting approval
- **Non-skill findings:** code/tool/process issues, if any
- **Next loop:** what to watch in the next run

Approve all proposal IDs, selected IDs, or request revisions.
```

Phase 2 adds the approved changes, validation commands and results, final
size delta, deferred proposals, and next-run signals.

$ARGUMENTS
