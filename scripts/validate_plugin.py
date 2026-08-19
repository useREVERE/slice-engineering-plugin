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
REQUIRED_KNOWLEDGE_HOMES = {
    "agent_rules",
    "philosophy",
    "guide",
    "procedures",
    "decisions",
    "shipped",
    "queue",
    "debt",
}
REQUIRED_DOC_TEMPLATES = (
    "templates/docs/README.md",
    "templates/docs/engineering-philosophy.md",
    "templates/docs/engineering-guide.md",
    "templates/docs/sops/README.md",
    "templates/docs/sops/documentation-placement.md",
    "templates/docs/adrs/README.md",
    "templates/docs/adrs/TEMPLATE.md",
    "templates/docs/completed/changelog.md",
    "templates/docs/tech-debt/README.md",
    "templates/docs/tech-debt/remediation-plan.md",
    "templates/docs/tech-debt/remediation-history.md",
    "templates/docs/ledger/README.md",
)
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
    homes_missing = [
        key for key in REQUIRED_KNOWLEDGE_HOMES if f"{key}:" not in template
    ]
    if homes_missing:
        fail(f"templates/config.yaml missing knowledge_homes: {homes_missing}")
    for relative in REQUIRED_DOC_TEMPLATES:
        path = ROOT / relative
        if not path.is_file():
            fail(f"missing doc template {relative}")
    philosophy = (ROOT / "templates/docs/engineering-philosophy.md").read_text()
    if re.search(r"\bRevere\b", philosophy):
        fail("engineering-philosophy template must not name Revere")
    placement = (ROOT / "templates/docs/sops/documentation-placement.md").read_text()
    if "revere-ledger" in placement:
        fail("documentation-placement must use bound ledger paths")
    if "knowledge_homes" not in placement:
        fail("documentation-placement must mention knowledge_homes")
    setup = (ROOT / "skills/se-setup/SKILL.md").read_text()
    if "Never overwrite" not in setup:
        fail("se-setup must refuse to overwrite existing host docs")
    if "templates/docs/README.md" not in setup:
        fail("se-setup must treat templates/docs/README.md as the inventory")
    if "remediation-plan.md" not in setup:
        fail("se-setup must copy missing remediation-plan.md")
    if "remediation-history.md" not in setup:
        fail("se-setup must copy missing remediation-history.md")
    if "templates/CLAUDE.md" not in setup:
        fail("se-setup must offer templates/CLAUDE.md")
    if "Never overwrite an existing `CLAUDE.md`" not in setup:
        fail("se-setup must refuse to overwrite existing CLAUDE.md")


def validate_weekly_loop() -> None:
    review = (ROOT / "skills/se-review-codebase/SKILL.md").read_text()
    if "Then stop" not in review:
        fail("se-review-codebase must pause before writing the plan")
    if "remediation-plan.md" not in review:
        fail("se-review-codebase must update remediation-plan.md")
    if "origin/main" in review or "render.yaml" in review:
        fail("se-review-codebase must not hardcode origin/main or render.yaml")
    deliver = (ROOT / "skills/se-deliver-remediation-plan/SKILL.md").read_text()
    if "se-deliver" not in deliver:
        fail("se-deliver-remediation-plan must run se-deliver per item")
    if "origin/main" in deliver or "render.yaml" in deliver:
        fail(
            "se-deliver-remediation-plan must not hardcode origin/main "
            "or render.yaml"
        )
    conventions = (ROOT / "skills/_shared/agent-conventions.md").read_text()
    if "Goal mode" not in conventions:
        fail("agent-conventions must define Goal mode")
    if "Assessor label" not in conventions:
        fail("agent-conventions must define Assessor label")


def validate_improve_skill_from_run() -> None:
    skill = (ROOT / "skills/se-improve-skill-from-run/SKILL.md").read_text()
    if "Do not edit any skill file" not in skill:
        fail("se-improve-skill-from-run must be review-only until approval")
    if "awaiting approval" not in skill:
        fail("se-improve-skill-from-run must stop for proposal approval")
    if "origin/main" in skill:
        fail("se-improve-skill-from-run must not hardcode origin/main")
    if "make entire-enable" in skill:
        fail("se-improve-skill-from-run must not require Entire enablement")
    exporter = (
        ROOT / "skills/se-improve-skill-from-run/scripts/export_claude_run.sh"
    )
    if not exporter.is_file():
        fail("missing Claude compact-run exporter")
    conventions = (ROOT / "skills/_shared/agent-conventions.md").read_text()
    if "Run evidence" not in conventions:
        fail("agent-conventions must define Run evidence")
    if "Cursor" not in conventions.split("## Run evidence", 1)[-1]:
        fail("Run evidence must include Cursor")


def validate_plan_gate() -> None:
    review = (ROOT / "skills/se-review-plan/SKILL.md").read_text()
    if "se-challenge-scope" not in review:
        fail("se-review-plan must invoke se-challenge-scope")
    if "**Verdict:**" not in review:
        fail("se-review-plan must emit a Farley verdict")
    if "Do not edit" not in review:
        fail("se-review-plan must be report-only")
    if "origin/main" in review:
        fail("se-review-plan must not hardcode origin/main")
    loop = (ROOT / "skills/se-plan-loop/SKILL.md").read_text()
    if "se-review-plan" not in loop:
        fail("se-plan-loop must invoke se-review-plan")
    if "se-execute" not in loop:
        fail("se-plan-loop must hand off to se-execute")
    if "/tmp/revere-plan" in loop:
        fail("se-plan-loop must not use a product-specific temp path")
    if "mktemp" not in loop:
        fail("se-plan-loop must create a temp plan with mktemp")
    if "XXXXXX" not in loop:
        fail("se-plan-loop mktemp template must keep XXXXXX at the end")
    plan = (ROOT / "skills/se-plan/SKILL.md").read_text()
    if "se-plan-loop" not in plan:
        fail("se-plan must compose se-plan-loop")
    deliver = (ROOT / "skills/se-deliver/SKILL.md").read_text()
    if "se-plan-loop" not in deliver:
        fail("se-deliver must route through se-plan-loop")
    if "se-review-plan" not in deliver:
        fail("se-deliver must name se-review-plan")
    if "se-sync-worktree" not in deliver:
        fail("se-deliver must mention se-sync-worktree for stale checkouts")


def validate_ledger_lifecycle() -> None:
    publish = (ROOT / "skills/se-publish/SKILL.md").read_text()
    if "ledger_publish.py" in publish:
        fail("se-publish must not require ledger_publish.py")
    if "never force-push" not in publish.lower():
        fail("se-publish must forbid force-push")
    if "ledger: none" not in publish:
        fail("se-publish must stop when ledger is none")
    if "origin/<default_branch>" not in publish:
        fail("se-publish must use bound default_branch")
    compact = (ROOT / "skills/se-compact-brief/SKILL.md").read_text()
    if "ledger_edit.py" in compact:
        fail("se-compact-brief must not require ledger_edit.py")
    if "Preservation Contract" not in compact:
        fail("se-compact-brief must keep the Preservation Contract")
    if "Never publish, commit, push" not in compact:
        fail("se-compact-brief must not publish")
    if "se-review-brief" not in compact:
        fail("se-compact-brief must hand off to se-review-brief")
    reflect = (ROOT / "skills/se-reflect/SKILL.md").read_text()
    if "se-compact-brief" not in reflect:
        fail("se-reflect must point at se-compact-brief")


def validate_worktrees() -> None:
    for name in (
        "se-prep",
        "se-sync-worktree",
        "se-settle-worktree",
        "se-tidy-worktree",
    ):
        text = (ROOT / "skills" / name / "SKILL.md").read_text()
        if "origin/main" in text:
            fail(f"{name} must not hardcode origin/main")
        if "origin/<default_branch>" not in text and name != "se-settle-worktree":
            fail(f"{name} must use origin/<default_branch>")
    sync = (ROOT / "skills/se-sync-worktree/SKILL.md").read_text()
    if "does not invoke `se-settle-worktree`" not in sync:
        fail("se-sync-worktree must not invoke settle")
    script = ROOT / "skills/se-settle-worktree/scripts/settle_worktree.py"
    if not script.is_file():
        fail("missing se-settle-worktree checkpoint script")
    script_text = script.read_text()
    if "revere" in script_text.lower():
        fail("settle_worktree.py must not contain Revere coupling")
    if "/private/tmp" in script_text:
        fail("settle_worktree.py must not write recovery notes to /private/tmp")
    if "slice-engineering" not in script_text:
        fail("settle_worktree.py must write notes under a plugin-owned path")


def validate_claude_md_template() -> None:
    path = ROOT / "templates" / "CLAUDE.md"
    if not path.is_file():
        fail("missing templates/CLAUDE.md")
    text = path.read_text()
    if "@AGENTS.md" not in text:
        fail("CLAUDE.md template must wrap AGENTS.md")
    if "CLAUDE_PROJECT_DIR" not in text:
        fail("CLAUDE.md template must document hook invocation")
    if "Do not write local memories" not in text:
        fail("CLAUDE.md template must forbid local memories")
    if "origin/main" in text:
        fail("CLAUDE.md template must not hardcode origin/main")


def validate_skills_do_not_hardcode_origin_main() -> None:
    for directory in skill_dirs():
        text = (directory / "SKILL.md").read_text()
        if "origin/main" in text:
            fail(f"{directory.name} must not hardcode origin/main")


def validate_forbidden() -> None:
    skip_parts = {".git", "__pycache__"}
    skip_suffixes = {".pyc", ".pyo"}
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip_parts for part in path.parts):
            continue
        if path.suffix in skip_suffixes:
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
    validate_weekly_loop()
    validate_improve_skill_from_run()
    validate_plan_gate()
    validate_ledger_lifecycle()
    validate_worktrees()
    validate_claude_md_template()
    validate_skills_do_not_hardcode_origin_main()
    validate_forbidden()
    print(f"ok {len(names)} skills, version {version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
