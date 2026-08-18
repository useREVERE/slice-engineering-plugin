#!/usr/bin/env python3
"""Validate Slice Engineering plugin package contracts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
FORBIDDEN = (
    "revere-ledger",
    "userevere.com",
    "~/.claude/revere-ledger",
    "FEDERAL_REGULATOR",
    "make entire-enable",
    "AUTH_DISABLED",
)
ALLOWED_FORBIDDEN_RELATIVE = {
    "README.md",
    "CONCEPTS.md",
    "CHANGELOG.md",
    "scripts/validate_plugin.py",
    "tests/test_plugin_contract.py",
}
REQUIRED_CONFIG_KEYS = {
    "default_branch",
    "verify_command",
    "ship_mode",
    "deploy",
    "ledger",
    "ledger_root",
    "worktrees",
    "knowledge_homes",
}
MANIFESTS = (
    ROOT / "plugin.json",
    ROOT / ".cursor-plugin" / "plugin.json",
    ROOT / ".claude-plugin" / "plugin.json",
    ROOT / ".codex-plugin" / "plugin.json",
)


def fail(message: str) -> None:
    raise SystemExit(f"validate_plugin: {message}")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        fail("SKILL.md frontmatter is not closed")
    fields: dict[str, str] = {}
    for raw_line in parts[1].splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            fail(f"invalid frontmatter line: {raw_line!r}")
        fields[key.strip()] = value.strip()
    return fields, parts[2]


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        fail(f"{path.relative_to(ROOT)} is not valid JSON: {exc}")
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)} must be a JSON object")
    return data


def skill_dirs() -> list[Path]:
    return sorted(
        path
        for path in SKILLS_DIR.iterdir()
        if path.is_dir() and not path.name.startswith("_")
    )


def validate_manifests() -> str:
    versions = {}
    names = {}
    for path in MANIFESTS:
        if not path.is_file():
            fail(f"missing manifest {path.relative_to(ROOT)}")
        data = load_json(path)
        names[str(path.relative_to(ROOT))] = data.get("name")
        versions[str(path.relative_to(ROOT))] = data.get("version")
        if data.get("name") != "slice-engineering":
            fail(f"{path.relative_to(ROOT)} name must be slice-engineering")
        if not data.get("version"):
            fail(f"{path.relative_to(ROOT)} is missing version")
    if len(set(versions.values())) != 1:
        fail(f"manifest versions drifted: {versions}")
    marketplace = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        fail("Claude marketplace.json must list plugins")
    if plugins[0].get("name") != "slice-engineering":
        fail("Claude marketplace plugin name must be slice-engineering")
    return str(next(iter(versions.values())))


def validate_skills() -> list[str]:
    names: list[str] = []
    for directory in skill_dirs():
        skill = directory / "SKILL.md"
        if not skill.is_file():
            fail(f"{directory.name} is missing SKILL.md")
        fields, body = parse_frontmatter(skill.read_text())
        name = fields.get("name")
        if name != directory.name:
            fail(f"{directory.name} frontmatter name {name!r} must match folder")
        if not fields.get("description"):
            fail(f"{directory.name} is missing description")
        if "$ARGUMENTS" not in body:
            fail(f"{directory.name} must mention $ARGUMENTS")
        names.append(name)
    if not names:
        fail("no skills found")
    return names


def validate_catalog(skill_names: list[str]) -> None:
    readme = (ROOT / "README.md").read_text()
    catalog = (ROOT / "docs" / "skills" / "README.md").read_text()
    for name in skill_names:
        if name not in readme:
            fail(f"README.md does not mention {name}")
        if name not in catalog:
            fail(f"docs/skills/README.md does not mention {name}")


def validate_template() -> None:
    template = (ROOT / "templates" / "config.yaml").read_text()
    missing = [key for key in REQUIRED_CONFIG_KEYS if f"{key}:" not in template]
    if missing:
        fail(f"templates/config.yaml missing keys: {missing}")


def validate_forbidden() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        relative = str(path.relative_to(ROOT))
        if relative in ALLOWED_FORBIDDEN_RELATIVE:
            continue
        text = path.read_text(errors="replace")
        for token in FORBIDDEN:
            if token in text:
                fail(f"{relative} contains forbidden host coupling: {token}")


def main() -> None:
    version = validate_manifests()
    names = validate_skills()
    validate_catalog(names)
    validate_template()
    validate_forbidden()
    print(f"ok {len(names)} skills, version {version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
