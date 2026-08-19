import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_plugin.py"


class PluginContractTests(unittest.TestCase):
    def test_validator_passes_on_this_checkout(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=result.stdout + result.stderr,
        )
        self.assertIn("ok ", result.stdout)

    def test_setup_skill_points_at_bindings_template(self) -> None:
        text = (ROOT / "skills" / "se-setup" / "SKILL.md").read_text()
        self.assertIn("templates/config.yaml", text)
        self.assertIn(".slice-engineering/config.yaml", text)

    def test_setup_scaffolds_docs_without_overwriting(self) -> None:
        text = (ROOT / "skills" / "se-setup" / "SKILL.md").read_text()
        self.assertIn("templates/docs/README.md", text)
        self.assertIn("Never overwrite", text)
        self.assertIn("docs/engineering-philosophy.md", text)
        self.assertIn("docs/engineering-guide.md", text)
        self.assertIn("documentation-placement.md", text)
        self.assertIn("docs/tech-debt/remediation-plan.md", text)
        self.assertIn("docs/tech-debt/remediation-history.md", text)
        self.assertIn("do not invent a stack", text)
        self.assertIn("templates/CLAUDE.md", text)
        self.assertIn("CLAUDE.md", text)

    def test_doc_templates_are_host_agnostic(self) -> None:
        philosophy = (
            ROOT / "templates" / "docs" / "engineering-philosophy.md"
        ).read_text()
        self.assertIn("thin vertical slices", philosophy)
        self.assertNotIn("Revere", philosophy)
        placement = (
            ROOT / "templates" / "docs" / "sops" / "documentation-placement.md"
        ).read_text()
        self.assertIn("knowledge_homes", placement)
        self.assertIn("bound ledger", placement)
        guide = (ROOT / "templates" / "docs" / "engineering-guide.md").read_text()
        self.assertIn("se-setup:", guide)
        self.assertIn("documentation-placement.md", guide)

    def test_deliver_does_not_absorb_phase_skills(self) -> None:
        text = (ROOT / "skills" / "se-deliver" / "SKILL.md").read_text()
        for name in (
            "se-plan-loop",
            "se-review-plan",
            "se-execute",
            "se-review-loop",
            "se-ship",
            "se-reflect",
        ):
            self.assertIn(name, text)
        self.assertIn("Do not duplicate or weaken", text)
        self.assertIn("se-sync-worktree", text)

    def test_plan_is_an_alias_of_plan_loop(self) -> None:
        plan = (ROOT / "skills" / "se-plan" / "SKILL.md").read_text()
        loop = (ROOT / "skills" / "se-plan-loop" / "SKILL.md").read_text()
        review = (ROOT / "skills" / "se-review-plan" / "SKILL.md").read_text()
        self.assertIn("se-plan-loop", plan)
        self.assertIn("se-review-plan", loop)
        self.assertIn("se-challenge-scope", review)
        self.assertIn("**Verdict:**", review)
        self.assertIn("Do not edit", review)
        self.assertNotIn("/tmp/revere-plan", loop)
        self.assertIn("mktemp", loop)
        self.assertNotIn("origin/main", loop)
        self.assertNotIn("origin/main", review)

    def test_publish_and_compact_are_portable_git_and_file_edits(self) -> None:
        publish = (ROOT / "skills" / "se-publish" / "SKILL.md").read_text()
        compact = (ROOT / "skills" / "se-compact-brief" / "SKILL.md").read_text()
        reflect = (ROOT / "skills" / "se-reflect" / "SKILL.md").read_text()
        self.assertIn("ledger: none", publish)
        self.assertIn("origin/<default_branch>", publish)
        self.assertNotIn("ledger_publish.py", publish)
        self.assertIn("Preservation Contract", compact)
        self.assertNotIn("ledger_edit.py", compact)
        self.assertIn("Never publish, commit, push", compact)
        self.assertIn("se-compact-brief", reflect)
        self.assertNotIn("origin/main", publish)
        self.assertNotIn("origin/main", compact)

    def test_worktree_skills_use_bound_default_branch(self) -> None:
        for name in (
            "se-prep",
            "se-sync-worktree",
            "se-tidy-worktree",
        ):
            text = (ROOT / "skills" / name / "SKILL.md").read_text()
            self.assertIn("origin/<default_branch>", text)
            self.assertNotIn("origin/main", text)
        sync = (ROOT / "skills" / "se-sync-worktree" / "SKILL.md").read_text()
        self.assertIn("does not invoke `se-settle-worktree`", sync)
        settle = (ROOT / "skills" / "se-settle-worktree" / "SKILL.md").read_text()
        self.assertIn("settle_worktree.py", settle)
        self.assertIn("se-commit", settle)
        script = (
            ROOT / "skills" / "se-settle-worktree" / "scripts" / "settle_worktree.py"
        ).read_text()
        self.assertNotIn("/private/tmp", script)
        self.assertNotIn("revere", script.lower())
        self.assertIn("slice-engineering", script)

    def test_claude_md_template_is_a_thin_agents_wrapper(self) -> None:
        text = (ROOT / "templates" / "CLAUDE.md").read_text()
        self.assertIn("@AGENTS.md", text)
        self.assertIn("CLAUDE_PROJECT_DIR", text)
        self.assertIn("Do not write local memories", text)
        self.assertNotIn("origin/main", text)
        self.assertNotIn("revere-ledger", text)

    def test_review_skill_is_report_only(self) -> None:
        text = (ROOT / "skills" / "se-review" / "SKILL.md").read_text()
        self.assertIn("Do not edit code", text)
        self.assertIn("ship it", text)

    def test_review_codebase_pauses_before_writing_the_plan(self) -> None:
        text = (ROOT / "skills" / "se-review-codebase" / "SKILL.md").read_text()
        self.assertIn("Then stop", text)
        self.assertIn("remediation-plan.md", text)
        self.assertNotIn("origin/main", text)
        self.assertNotIn("render.yaml", text)
        self.assertIn("se-challenge-scope", text)

    def test_deliver_remediation_plan_runs_se_deliver_per_item(self) -> None:
        text = (
            ROOT / "skills" / "se-deliver-remediation-plan" / "SKILL.md"
        ).read_text()
        self.assertIn("se-deliver", text)
        self.assertIn("one at a time", text)
        self.assertNotIn("origin/main", text)
        self.assertNotIn("render.yaml", text)
        self.assertIn("se-review-codebase", text)

    def test_remediation_plan_template_is_a_queue_contract(self) -> None:
        text = (
            ROOT / "templates" / "docs" / "tech-debt" / "remediation-plan.md"
        ).read_text()
        self.assertIn("How to use this file", text)
        self.assertIn("Pending Refactors", text)
        self.assertIn("remediation-history.md", text)
        self.assertNotIn("origin/main", text)

    def test_improve_skill_from_run_is_two_phase(self) -> None:
        text = (
            ROOT / "skills" / "se-improve-skill-from-run" / "SKILL.md"
        ).read_text()
        self.assertIn("Do not edit any skill file", text)
        self.assertIn("awaiting approval", text)
        self.assertNotIn("origin/main", text)
        self.assertNotIn("make entire-enable", text)
        self.assertIn("export_claude_run.sh", text)
        conventions = (
            ROOT / "skills" / "_shared" / "agent-conventions.md"
        ).read_text()
        self.assertIn("Run evidence", conventions)
        self.assertIn("current conversation", conventions.lower())


if __name__ == "__main__":
    unittest.main()
