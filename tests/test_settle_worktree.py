import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "se-settle-worktree" / "scripts" / "settle_worktree.py"


class SettleWorktreeScriptTests(unittest.TestCase):
    def _git(self, cwd: Path, *args: str) -> None:
        subprocess.run(
            ["git", *args],
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )

    def _repo(self) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        cwd = Path(tmp.name)
        self._git(cwd, "init")
        self._git(cwd, "config", "user.email", "settle@example.com")
        self._git(cwd, "config", "user.name", "Settle Test")
        (cwd / "readme.txt").write_text("hi\n", encoding="utf-8")
        self._git(cwd, "add", "readme.txt")
        self._git(cwd, "commit", "-m", "init")
        return cwd

    def test_inspect_reports_checkpoint_safe_for_unstaged_edit(self) -> None:
        cwd = self._repo()
        (cwd / "readme.txt").write_text("changed\n", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--inspect"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data["checkpoint_safe"])

    def test_inspect_blocks_env_files(self) -> None:
        cwd = self._repo()
        (cwd / ".env").write_text("SECRET=1\n", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--inspect"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        data = json.loads(result.stdout)
        self.assertFalse(data["checkpoint_safe"])
        self.assertIn("possible_secret_paths", data["blockers"])

    def test_checkpoint_writes_note_under_git_dir(self) -> None:
        cwd = self._repo()
        (cwd / "readme.txt").write_text("changed\n", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--checkpoint", "--reason", "test"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data["checkpointed"])
        note = Path(data["recovery_note"])
        self.assertTrue(note.is_file())
        self.assertIn("slice-engineering", str(note))
        self.assertNotIn("/private/tmp", str(note))
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(status.stdout.strip(), "")


if __name__ == "__main__":
    unittest.main()
