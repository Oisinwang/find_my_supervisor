import shutil
import tempfile
import unittest
from pathlib import Path

from tools.install_integrity_check import validate_installation


ROOT = Path(__file__).resolve().parents[1]
SKILL_SOURCE = ROOT / "skills" / "find-my-supervisor"


class InstallIntegrityTests(unittest.TestCase):
    def test_copied_skill_installation_has_no_integrity_issues(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp) / "skills" / "find-my-supervisor"
            shutil.copytree(str(SKILL_SOURCE), str(skill_dir))

            self.assertEqual(validate_installation(skill_dir), [])

    def test_missing_skill_file_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp) / "skills" / "find-my-supervisor"
            (skill_dir / "references").mkdir(parents=True)
            (skill_dir / "schemas").mkdir()
            (skill_dir / "examples" / "profiles").mkdir(parents=True)
            (skill_dir / "examples" / "reports").mkdir()

            issues = validate_installation(skill_dir)

            self.assertIn("missing required file: SKILL.md", issues)

    def test_missing_reports_directory_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp) / "skills" / "find-my-supervisor"
            (skill_dir / "references").mkdir(parents=True)
            (skill_dir / "schemas").mkdir()
            (skill_dir / "examples" / "profiles").mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("# Find My Supervisor\n", encoding="utf-8")

            issues = validate_installation(skill_dir)

            self.assertIn("missing required directory: examples/reports", issues)


if __name__ == "__main__":
    unittest.main()
