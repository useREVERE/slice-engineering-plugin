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

    def test_deliver_does_not_absorb_phase_skills(self) -> None:
        text = (ROOT / "skills" / "se-deliver" / "SKILL.md").read_text()
        for name in (
            "se-plan",
            "se-execute",
            "se-review-loop",
            "se-ship",
            "se-reflect",
        ):
            self.assertIn(name, text)
        self.assertIn("Do not duplicate or weaken", text)

    def test_review_skill_is_report_only(self) -> None:
        text = (ROOT / "skills" / "se-review" / "SKILL.md").read_text()
        self.assertIn("Do not edit code", text)
        self.assertIn("ship it", text)


if __name__ == "__main__":
    unittest.main()
