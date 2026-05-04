import unittest
from pathlib import Path

from tools.skill_pack_validator import run_all


ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def test_skill_pack_files_validate(self):
        self.assertEqual(run_all(ROOT), [])


if __name__ == "__main__":
    unittest.main()
