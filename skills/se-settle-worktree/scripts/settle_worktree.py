#!/usr/bin/env python3
"""Safely inspect or checkpoint a dirty git worktree."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


SECRET_PATH_RE = re.compile(
    r"(^|/)(\.env($|[./_-])|.*(secret|credential|token|private[_-]?key).*)"
    r"|.*\.(pem|key|p12|pfx)$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class GitResult:
    stdout: str
    stderr: str
    returncode: int


def git(*args: str, check: bool = True) -> GitResult:
    result = subprocess.run(
        ["git", *args],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and result.returncode != 0:
        raise SystemExit(
            f"git {' '.join(args)} failed\n{result.stderr.strip() or result.stdout.strip()}"
        )
    return GitResult(result.stdout.rstrip("\n"), result.stderr.strip(), result.returncode)


def porcelain_entries() -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for line in git("status", "--porcelain=v1", "-uall").stdout.splitlines():
        if not line:
            continue
        status = line[:2]
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        entries.append((status, path))
    return entries


def has_staged_change(status: str) -> bool:
    return status[0] not in {" ", "?"}


def has_conflict(status: str) -> bool:
    return status in {"DD", "AU", "UD", "UA", "DU", "AA", "UU"}


def inspect_state() -> dict:
    entries = porcelain_entries()
    paths = [path for _, path in entries]
    conflicts = [(status, path) for status, path in entries if has_conflict(status)]
    staged = [(status, path) for status, path in entries if has_staged_change(status)]
    secret_paths = [path for path in paths if SECRET_PATH_RE.search(path)]
    branch = git("branch", "--show-current").stdout
    head = git("rev-parse", "--short", "HEAD").stdout
    root = git("rev-parse", "--show-toplevel").stdout
    status_branch = git("status", "--short", "--branch").stdout

    blockers: list[str] = []
    if not entries:
        blockers.append("no_changes")
    if conflicts:
        blockers.append("merge_conflicts")
    if staged:
        blockers.append("staged_changes")
    if secret_paths:
        blockers.append("possible_secret_paths")

    return {
        "checkpoint_safe": not blockers,
        "blockers": blockers,
        "root": root,
        "branch": branch or None,
        "detached": not bool(branch),
        "head": head,
        "status_branch": status_branch,
        "entries": [{"status": status, "path": path} for status, path in entries],
        "conflicts": [{"status": status, "path": path} for status, path in conflicts],
        "staged": [{"status": status, "path": path} for status, path in staged],
        "possible_secret_paths": secret_paths,
        "diff_stat": git("diff", "--stat").stdout,
        "untracked": git("ls-files", "--others", "--exclude-standard").stdout.splitlines(),
        "recent_commits": git("log", "--oneline", "-5").stdout,
    }


def slug(text: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_.-]+", "-", text.strip().lower()).strip("-")
    return value[:48] or "worktree-checkpoint"


def git_common_dir() -> Path:
    raw = git("rev-parse", "--git-common-dir").stdout
    path = Path(raw)
    if not path.is_absolute():
        path = Path.cwd() / path
    return path.resolve()


def recovery_note_dir() -> Path:
    path = git_common_dir() / "slice-engineering" / "checkpoints"
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_note(state: dict, stash_ref: str, reason: str) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    note_path = (
        recovery_note_dir()
        / f"se-worktree-checkpoint-{timestamp}-{slug(reason)}.md"
    )
    restore_command = f"git stash apply {stash_ref}"
    lines = [
        "# Slice Engineering Worktree Checkpoint",
        "",
        f"- Reason: {reason}",
        f"- Repository: {state['root']}",
        f"- Branch: {state['branch'] or '(detached HEAD)'}",
        f"- HEAD: {state['head']}",
        f"- Stash: {stash_ref}",
        f"- Restore: `{restore_command}`",
        "",
        "## Status Before Checkpoint",
        "",
        "```text",
        state["status_branch"],
        "```",
        "",
        "## Diff Stat Before Checkpoint",
        "",
        "```text",
        state["diff_stat"] or "(no tracked diff stat)",
        "```",
        "",
        "## Untracked Files Before Checkpoint",
        "",
        "```text",
        "\n".join(state["untracked"]) or "(none)",
        "```",
        "",
        "## Recent Commits",
        "",
        "```text",
        state["recent_commits"],
        "```",
        "",
        "## Machine-Readable State",
        "",
        "```json",
        json.dumps(state, indent=2, sort_keys=True),
        "```",
        "",
    ]
    note_path.write_text("\n".join(lines), encoding="utf-8")
    return note_path


def checkpoint(reason: str) -> dict:
    before = inspect_state()
    if not before["checkpoint_safe"]:
        return {"checkpointed": False, **before}

    message = f"se-settle-worktree: {reason}"
    stash_result = git(
        "stash",
        "push",
        "--include-untracked",
        "-m",
        message,
        check=False,
    )
    if stash_result.returncode != 0:
        return {
            **before,
            "checkpointed": False,
            "checkpoint_safe": False,
            "blockers": ["git_stash_failed"],
            "git_stash_stdout": stash_result.stdout,
            "git_stash_stderr": stash_result.stderr,
            "retry_hint": (
                "Rerun the same checkpoint command with elevated sandbox "
                "permissions if the error says Git could not write the index."
            ),
        }
    stash_line = git("stash", "list", "--format=%gd%x09%s", "-n", "1").stdout
    stash_ref = stash_line.split("\t", 1)[0]
    after_entries = porcelain_entries()
    note_path = write_note(before, stash_ref, reason)

    return {
        "checkpointed": True,
        "stash_ref": stash_ref,
        "recovery_note": str(note_path),
        "restore_command": f"git stash apply {stash_ref}",
        "clean_after_checkpoint": not after_entries,
        "after_entries": [
            {"status": status, "path": path} for status, path in after_entries
        ],
        **before,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--inspect", action="store_true")
    mode.add_argument("--checkpoint", action="store_true")
    parser.add_argument(
        "--reason",
        default="dirty worktree blocked workflow",
        help="Short human reason recorded in the stash message and recovery note.",
    )
    args = parser.parse_args()

    result = checkpoint(args.reason) if args.checkpoint else inspect_state()
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.checkpoint and not result.get("checkpointed"):
        raise SystemExit(2)
    if args.checkpoint and not result.get("clean_after_checkpoint"):
        raise SystemExit(3)


if __name__ == "__main__":
    main()
