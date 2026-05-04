import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProjectBaselineTests(unittest.TestCase):
    def test_agents_policy_exists_and_preserves_delete_rule(self):
        agents = ROOT / "AGENTS.md"
        self.assertTrue(agents.exists())
        text = agents.read_text(encoding="utf-8")
        self.assertIn("D:\\rubbish", text)
        self.assertIn("requested deletion", text)

    def test_readme_defines_skills_route_scope(self):
        readme = ROOT / "README.md"
        self.assertTrue(readme.exists())
        text = readme.read_text(encoding="utf-8")
        self.assertIn("skills route", text.lower())
        self.assertIn("CS/AI", text)
        self.assertIn("mathematics", text.lower())
        self.assertIn("985", text)
        self.assertIn("CAS/UCAS", text)
        self.assertIn("HKU", text)
        self.assertIn("CUHK", text)
        self.assertIn("HKUST", text)


if __name__ == "__main__":
    unittest.main()
