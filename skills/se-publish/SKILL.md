---
name: se-publish
description: Commit and non-force push named ledger artifacts in the bound ledger checkout. Use when a workshopped brief or named investigation/asset should become the durable git record.
disable-model-invocation: true
---

# Publish

Publish named ledger artifacts with ordinary git. Success means the named
paths are committed in the bound ledger checkout and pushed without force.
This skill does not decide readiness — explicit user authorization does.

There is no snapshot publisher, isolated worktree, or index generator in
this plugin. Do not invent one.

Treat `$ARGUMENTS` as the ledger artifact path or explicit publication
scope.

Read `skills/_shared/bindings.md`. Honor `ledger`, `ledger_root`,
`external_ledger_path`, and `default_branch`.

## Ledger checkout

- `ledger: none` — stop. Do not create a ledger.
- `ledger: in-repo` — git repo is the host repository; artifacts live under
  `ledger_root`.
- `ledger: external` — git repo is `external_ledger_path` (expand `~/`).
  Use `git -C <external_ledger_path>` for every command.

If a required ledger path is missing, stop and ask. Do not assume a
product-specific ledger location.

## What this skill handles

- **Arc briefs** — `<ledger_root>/arcs/<slug>/brief.md`
- **Investigations** — only when the user explicitly names
  `<ledger_root>/investigations/...`
- **Arc assets** — only when the user explicitly names files under
  `<ledger_root>/arcs/<slug>/assets/`

Handoff docs and temp plans stay ephemeral. Do not publish them unless the
user names a durable ledger path.

If the user names a specific brief, publish that brief. A clean named
brief is a successful no-op. If they ask to publish dirty briefs without
naming one, list candidate `arcs/*/brief.md` paths and wait for
confirmation. Do not silently mix artifact classes in one publication.

## Preflight

Work in the ledger git checkout:

```bash
git -C "$LEDGER_GIT" status --short --branch
git -C "$LEDGER_GIT" fetch origin
git -C "$LEDGER_GIT" rev-parse HEAD
git -C "$LEDGER_GIT" rev-parse origin/<default_branch>
git -C "$LEDGER_GIT" rev-list --left-right --count origin/<default_branch>...HEAD
```

`$LEDGER_GIT` is the host root for `in-repo`, or `external_ledger_path`
for `external`.

Then:

- Stop if fetch fails, the checkout is detached, or
  `origin/<default_branch>` is unavailable.
- If the current branch is `<default_branch>` and HEAD is behind only,
  fast-forward with `git merge --ff-only origin/<default_branch>` when
  that would not overwrite uncommitted work. Stop on ahead+behind
  divergence; do not merge or rebase speculatively.
- Stop if the working tree has staged, unstaged, or untracked changes
  **outside** the named publication paths. Unrelated dirty files are not
  part of this commit.
- For `in-repo`, report whether the current branch is a task branch. Stop
  if pushing it would publish unrelated product commits unless the user
  confirmed that.

Invoking this skill with a named path is authorization for that path.
Do not invent additional targets.

## Git flow

Inspect exact scope, then:

```bash
git -C "$LEDGER_GIT" add -- <named-paths>
git -C "$LEDGER_GIT" diff --cached --stat
git -C "$LEDGER_GIT" commit -m "Publish <slug-or-scope>"
git -C "$LEDGER_GIT" push origin HEAD:<remote-ref>
```

`<remote-ref>` is the current branch's upstream when it exists, otherwise
`<default_branch>` only when HEAD is already that branch. Never force-push.
Never `--force`. Never `--no-verify`. Never amend a published commit.

Do not run a host-specific publisher script. Do not regenerate a ledger
index unless the user asks to update `<ledger_root>/README.md` as an
additional named path.

If `git commit` is a no-op because the named paths match HEAD, report
success and do not push an empty publication.

## What this skill doesn't do

- **Doesn't draft the artifact.** That's `se-brief`, `se-reflect`,
  `se-compact-brief`, or ordinary editing.
- **Doesn't compact history.** That's `se-compact-brief`.
- **Doesn't archive arcs** or move files between directories unless the
  user named that move as the publication scope.
- **Doesn't manage external trackers.**

## Output

Quiet. Report:

- ledger git checkout and `ledger` binding
- named paths
- commit SHA or no-op
- remote ref pushed, or the exact reason push did not run
- unrelated dirty paths left untouched

## Stop Rules

Stop before changing git state if bindings say `ledger: none`, fetch
fails, named paths sit outside `ledger_root`, unrelated files are dirty,
history has diverged, or a non-fast-forward push would be required.

$ARGUMENTS
