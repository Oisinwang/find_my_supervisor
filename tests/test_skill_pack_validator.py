import tempfile
import unittest
from pathlib import Path

from tools.skill_pack_validator import (
    ValidationIssue,
    load_json,
    require_keys,
    validate_markdown_sections,
)


class ValidatorUnitTests(unittest.TestCase):
    def test_load_json_reads_utf8_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.json"
            path.write_text('{"name": "demo", "tags": ["math"]}', encoding="utf-8")
            self.assertEqual(load_json(path), {"name": "demo", "tags": ["math"]})

    def test_require_keys_reports_missing_keys(self):
        issues = require_keys({"name": "demo"}, ["name", "field"], "profile")
        self.assertEqual(
            issues,
            [ValidationIssue("profile", "missing required key: field")],
        )

    def test_validate_markdown_sections_reports_missing_section(self):
        issues = validate_markdown_sections(
            "# Demo\n\n## Present\n",
            ["## Present", "## Missing"],
            "demo.md",
        )
        self.assertEqual(
            issues,
            [ValidationIssue("demo.md", "missing section: ## Missing")],
        )


if __name__ == "__main__":
    unittest.main()
