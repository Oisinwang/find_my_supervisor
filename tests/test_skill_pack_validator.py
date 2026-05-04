import tempfile
import unittest
from pathlib import Path

from tools.skill_pack_validator import (
    ValidationIssue,
    load_json,
    require_keys,
    validate_report_quality,
    validate_markdown_sections,
)

ROOT = Path(__file__).resolve().parents[1]


def load_report_fixture(filename):
    path = ROOT / "tests" / "fixtures" / "report_quality" / filename
    return path.read_text(encoding="utf-8")


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

    def test_quality_fixture_good_minimal_report_passes(self):
        text = load_report_fixture("good_minimal_report.md")
        self.assertEqual(
            validate_report_quality(
                text,
                "real_good_minimal_report.md",
                set(["official", "bibliographic"]),
            ),
            [],
        )

    def test_quality_fixture_overclaim_report_fails(self):
        text = load_report_fixture("overclaim_admissions_report.md")
        issues = validate_report_quality(
            text,
            "real_overclaim_admissions_report.md",
            set(["official", "bibliographic"]),
        )
        self.assertIn(
            ValidationIssue(
                "real_overclaim_admissions_report.md",
                "real demo report contains admissions-certainty language: guaranteed admission",
            ),
            issues,
        )

    def test_quality_fixture_weak_cross_field_report_fails_evidence_signal_check(self):
        text = load_report_fixture("weak_cross_field_report.md")
        issues = validate_report_quality(
            text,
            "real_weak_cross_field_report.md",
            set(["official", "bibliographic"]),
        )
        self.assertIn(
            ValidationIssue(
                "real_weak_cross_field_report.md",
                "ranked supervisor has fewer than two source-labeled evidence mentions",
            ),
            issues,
        )

    def test_validate_report_quality_requires_all_fit_scores(self):
        text = """# Demo

## Generation Note

Public-source demo.

## Student Profile

## Ranked Shortlist

- Risk level: medium

#### Fit Scores

- Research fit: 4/5
- Path fit: 4/5
- Career fit: 4/5
- Evidence strength: 4/5

Fact: supported by official source [official].
Inference: likely fit [official].
Unknown: quota.

## Risks And Unknowns

## Source Appendix

- Demo source [official]

## Maybe List

## Excluded List

## Next Actions
"""
        self.assertEqual(
            validate_report_quality(text, "demo.md", set(["official"])),
            [
                ValidationIssue(
                    "demo.md",
                    "missing fit score: Risk and uncertainty",
                )
            ],
        )

    def test_validate_report_quality_scopes_fit_scores_to_fit_score_block(self):
        text = """# Demo

## Generation Note

Public-source demo.

## Student Profile

## Ranked Shortlist

- Evidence strength: high

- Risk level: medium

#### Fit Scores

- Research fit: 4/5
- Path fit: 4/5
- Career fit: 4/5
- Risk and uncertainty: 3/5

Fact: supported by official source [official].
Inference: likely fit [official].
Unknown: quota.

## Risks And Unknowns

## Source Appendix

- Demo source [official]

## Maybe List

## Excluded List

## Next Actions
"""
        self.assertEqual(
            validate_report_quality(text, "demo.md", set(["official"])),
            [
                ValidationIssue(
                    "demo.md",
                    "missing fit score: Evidence strength",
                )
            ],
        )

    def test_validate_report_quality_checks_second_rank_fit_scores(self):
        text = """# Demo

## Generation Note

Public-source demo.

## Student Profile

## Ranked Shortlist

### Rank 1: Prof. One

- Risk level: medium

#### Fit Scores

- Research fit: 4/5
- Path fit: 4/5
- Career fit: 4/5
- Evidence strength: 4/5
- Risk and uncertainty: 3/5

Fact: supported by official source [official].
Inference: likely fit [official].
Unknown: quota.

### Rank 2: Prof. Two

- Risk level: medium

#### Fit Scores

- Research fit: 4/5
- Path fit: 4/5
- Career fit: 4/5
- Risk and uncertainty: 3/5

Fact: supported by official source [official].
Inference: likely fit [official].
Unknown: quota.

## Maybe List

- Maybe entries do not need fit scores.

## Risks And Unknowns

## Source Appendix

- Demo source [official]

## Excluded List

## Next Actions
"""
        self.assertEqual(
            validate_report_quality(text, "demo.md", set(["official"])),
            [
                ValidationIssue(
                    "demo.md",
                    "missing fit score: Evidence strength",
                )
            ],
        )

    def test_validate_report_quality_requires_fact_inference_unknown(self):
        text = """# Demo

## Generation Note

Public-source demo.

## Student Profile

## Ranked Shortlist

- Risk level: medium

#### Fit Scores

- Research fit: 4/5
- Path fit: 4/5
- Career fit: 4/5
- Evidence strength: 4/5
- Risk and uncertainty: 3/5

## Risks And Unknowns

## Source Appendix

- Demo source [official]

## Maybe List

## Excluded List

## Next Actions
"""
        self.assertEqual(
            validate_report_quality(text, "demo.md", set(["official"])),
            [
                ValidationIssue(
                    "demo.md",
                    "missing fact/inference/unknown evidence lines",
                )
            ],
        )

    def test_validate_report_quality_checks_second_rank_fact_inference_unknown(self):
        text = """# Demo

## Generation Note

Public-source demo.

## Student Profile

## Ranked Shortlist

### Rank 1: Prof. One

- Risk level: medium

#### Fit Scores

- Research fit: 4/5
- Path fit: 4/5
- Career fit: 4/5
- Evidence strength: 4/5
- Risk and uncertainty: 3/5

Fact: supported by official source [official].
Inference: likely fit [official].
Unknown: quota.

### Rank 2: Prof. Two

- Risk level: medium

#### Fit Scores

- Research fit: 4/5
- Path fit: 4/5
- Career fit: 4/5
- Evidence strength: 4/5
- Risk and uncertainty: 3/5

This paragraph has no evidence distinction labels, but cites available sources [official] [bibliographic].

## Excluded List

- Excluded entries do not need evidence lines.

## Risks And Unknowns

## Source Appendix

- Demo source [official]

## Maybe List

## Next Actions
"""
        self.assertEqual(
            validate_report_quality(text, "demo.md", set(["official", "bibliographic"])),
            [
                ValidationIssue(
                    "demo.md",
                    "missing fact/inference/unknown evidence lines",
                )
            ],
        )

    def test_validate_report_quality_accepts_fact_inference_unknown_sections(self):
        text = """# Demo

## Generation Note

Public-source demo.

## Student Profile

## Ranked Shortlist

- Risk level: medium

#### Fit Scores

- Research fit: 4/5
- Path fit: 4/5
- Career fit: 4/5
- Evidence strength: 4/5
- Risk and uncertainty: 3/5

#### Facts

Supported by official source [official].

#### Inferences

Likely fit [official].

#### Unknowns

Quota.

## Risks And Unknowns

## Source Appendix

- Demo source [official]

## Maybe List

## Excluded List

## Next Actions
"""
        self.assertEqual(
            validate_report_quality(text, "demo.md", set(["official"])),
            [],
        )

    def test_validate_report_quality_allows_slash_separated_source_labels(self):
        text = """# Demo

## Generation Note

Public-source demo.

## Student Profile

## Ranked Shortlist

- Risk level: medium

#### Fit Scores

- Research fit: 4/5
- Path fit: 4/5
- Career fit: 4/5
- Evidence strength: 4/5
- Risk and uncertainty: 3/5

Fact: supported by official source [official].
Inference: likely fit [official].
Unknown: quota.

## Risks And Unknowns

## Source Appendix

- Demo source [official/bibliographic]

## Maybe List

## Excluded List

## Next Actions
"""
        self.assertEqual(
            validate_report_quality(
                text,
                "demo.md",
                set(["official", "bibliographic"]),
            ),
            [],
        )

    def test_validate_report_quality_rejects_unknown_source_label(self):
        text = """# Demo

## Generation Note

Public-source demo.

## Student Profile

## Ranked Shortlist

- Risk level: medium

#### Fit Scores

- Research fit: 4/5
- Path fit: 4/5
- Career fit: 4/5
- Evidence strength: 4/5
- Risk and uncertainty: 3/5

Fact: supported by official source [official].
Inference: likely fit [official].
Unknown: quota.

## Risks And Unknowns

## Source Appendix

- Demo source [official/blog]

## Maybe List

## Excluded List

## Next Actions
"""
        self.assertEqual(
            validate_report_quality(text, "demo.md", set(["official"])),
            [ValidationIssue("demo.md", "invalid source label: blog")],
        )

    def test_validate_report_quality_checks_source_labels_before_line_end(self):
        text = """# Demo

## Generation Note

Public-source demo.

## Student Profile

## Ranked Shortlist

- Risk level: medium

#### Fit Scores

- Research fit: 4/5
- Path fit: 4/5
- Career fit: 4/5
- Evidence strength: 4/5
- Risk and uncertainty: 3/5

Fact: supported by official source [official].
Inference: likely fit [official].
Unknown: quota.

## Risks And Unknowns

## Source Appendix

- [blog] source details

## Maybe List

## Excluded List

## Next Actions
"""
        self.assertEqual(
            validate_report_quality(text, "demo.md", set(["official"])),
            [ValidationIssue("demo.md", "invalid source label: blog")],
        )

    def test_validate_report_quality_requires_source_appendix_entry_label(self):
        text = """# Demo

## Generation Note

Public-source demo.

## Student Profile

## Ranked Shortlist

- Risk level: medium

#### Fit Scores

- Research fit: 4/5
- Path fit: 4/5
- Career fit: 4/5
- Evidence strength: 4/5
- Risk and uncertainty: 3/5

Fact: supported by official source [official].
Inference: likely fit [official].
Unknown: quota.

## Risks And Unknowns

## Source Appendix

- Demo source without label

## Maybe List

## Excluded List

## Next Actions
"""
        self.assertEqual(
            validate_report_quality(text, "demo.md", set(["official"])),
            [ValidationIssue("demo.md", "source appendix entry missing label")],
        )

    def test_validate_report_quality_rejects_synthetic_language_in_real_demo(self):
        text = """# Demo

## Generation Note

This public-source demo mentions a synthetic validation fixture.

## Student Profile

## Ranked Shortlist

- Risk level: medium

#### Fit Scores

- Research fit: 4/5
- Path fit: 4/5
- Career fit: 4/5
- Evidence strength: 4/5
- Risk and uncertainty: 3/5

Fact: supported by official source [official].
Inference: likely fit [official].
Unknown: quota.

## Risks And Unknowns

## Source Appendix

- Demo source [official]

## Maybe List

## Excluded List

## Next Actions
"""
        self.assertEqual(
            validate_report_quality(
                text,
                "real_hkust_trustworthy_llm_demo.md",
                set(["official"]),
            ),
            [
                ValidationIssue(
                    "real_hkust_trustworthy_llm_demo.md",
                    "real demo report contains synthetic fixture language",
                )
            ],
        )

    def test_validate_report_quality_rejects_admissions_certainty_in_real_demo(self):
        text = """# Demo

## Generation Note

Public-source demo.

## Student Profile

## Ranked Shortlist

### Rank 1: Prof. One

- Risk level: medium

#### Fit Scores

- Research fit: 4/5
- Path fit: 4/5
- Career fit: 4/5
- Evidence strength: 4/5
- Risk and uncertainty: 3/5

Fact: supported by official source [official].
Inference: This report says guaranteed admission [official].
Unknown: quota.

## Maybe List

## Excluded List

## Risks And Unknowns

## Source Appendix

- Faculty profile [official]
- Publication page [bibliographic]

## Next Actions
"""
        self.assertEqual(
            validate_report_quality(
                text,
                "real_demo.md",
                set(["official", "bibliographic"]),
            ),
            [
                ValidationIssue(
                    "real_demo.md",
                    "real demo report contains admissions-certainty language: guaranteed admission",
                )
            ],
        )

    def test_validate_report_quality_ignores_markdown_link_text_for_source_labels(self):
        text = """# Demo

## Generation Note

Public-source demo.

## Student Profile

## Ranked Shortlist

### Rank 1: Prof. One

- Risk level: medium

#### Fit Scores

- Research fit: 4/5
- Path fit: 4/5
- Career fit: 4/5
- Evidence strength: 4/5
- Risk and uncertainty: 3/5

Fact: supported by official source [official].
Inference: likely fit [official].
Unknown: quota.

## Maybe List

## Excluded List

## Risks And Unknowns

## Source Appendix

- [Faculty profile](https://example.edu/faculty) [official]
- [Publication page](https://example.org/paper) [bibliographic]

## Next Actions
"""
        self.assertEqual(
            validate_report_quality(
                text,
                "real_demo.md",
                set(["official", "bibliographic"]),
            ),
            [],
        )

    def test_validate_report_quality_requires_maybe_and_excluded_lists(self):
        text = """# Demo

## Generation Note

Public-source demo.

## Student Profile

## Ranked Shortlist

### Rank 1: Prof. One

- Risk level: medium

#### Fit Scores

- Research fit: 4/5
- Path fit: 4/5
- Career fit: 4/5
- Evidence strength: 4/5
- Risk and uncertainty: 3/5

Fact: supported by official source [official].
Inference: likely fit [official].
Unknown: quota.

## Risks And Unknowns

## Source Appendix

- Demo source [official/bibliographic]

## Next Actions
"""
        self.assertEqual(
            validate_report_quality(
                text,
                "real_demo.md",
                set(["official", "bibliographic"]),
            ),
            [
                ValidationIssue("real_demo.md", "missing section: ## Maybe List"),
                ValidationIssue("real_demo.md", "missing section: ## Excluded List"),
            ],
        )

    def test_validate_report_quality_rejects_invalid_risk_level(self):
        text = """# Demo

## Generation Note

Public-source demo.

## Student Profile

## Ranked Shortlist

### Rank 1: Prof. One

- Risk level: safe

#### Fit Scores

- Research fit: 4/5
- Path fit: 4/5
- Career fit: 4/5
- Evidence strength: 4/5
- Risk and uncertainty: 3/5

Fact: supported by official source [official].
Inference: likely fit [official].
Unknown: quota.

## Risks And Unknowns

## Source Appendix

- Demo source [official/bibliographic]

## Maybe List

## Excluded List

## Next Actions
"""
        self.assertEqual(
            validate_report_quality(
                text,
                "demo.md",
                set(["official", "bibliographic"]),
            ),
            [ValidationIssue("demo.md", "invalid risk level: safe")],
        )

    def test_validate_report_quality_accepts_medium_high_risk_level(self):
        text = """# Demo

## Generation Note

Public-source demo.

## Student Profile

## Ranked Shortlist

### Rank 1: Prof. One

- Risk level: medium_high

#### Fit Scores

- Research fit: 4/5
- Path fit: 4/5
- Career fit: 4/5
- Evidence strength: 4/5
- Risk and uncertainty: 3/5

Fact: supported by official source [official].
Inference: likely fit [official].
Unknown: quota.

## Risks And Unknowns

## Source Appendix

- Demo source [official/bibliographic]

## Maybe List

## Excluded List

## Next Actions
"""
        self.assertEqual(
            validate_report_quality(
                text,
                "demo.md",
                set(["official", "bibliographic"]),
            ),
            [],
        )

    def test_validate_report_quality_requires_risk_level(self):
        text = """# Demo

## Generation Note

Public-source demo.

## Student Profile

## Ranked Shortlist

### Rank 1: Prof. One

#### Fit Scores

- Research fit: 4/5
- Path fit: 4/5
- Career fit: 4/5
- Evidence strength: 4/5
- Risk and uncertainty: 3/5

Fact: supported by official source [official].
Inference: likely fit [official].
Unknown: quota.

## Risks And Unknowns

## Source Appendix

- Demo source [official/bibliographic]

## Maybe List

## Excluded List

## Next Actions
"""
        self.assertEqual(
            validate_report_quality(
                text,
                "demo.md",
                set(["official", "bibliographic"]),
            ),
            [ValidationIssue("demo.md", "missing risk level")],
        )


if __name__ == "__main__":
    unittest.main()
