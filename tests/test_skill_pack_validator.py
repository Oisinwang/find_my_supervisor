import tempfile
import unittest
from pathlib import Path

from tools.skill_pack_validator import (
    ValidationIssue,
    load_json,
    require_keys,
    validate_report_quality,
    validate_markdown_sections,
    validate_reports,
)
from tools.skill_pack_manifest import REQUIRED_REPORT_EXAMPLES
from tools.install_integrity_check import REQUIRED_FILES

ROOT = Path(__file__).resolve().parents[1]


def load_report_fixture(filename):
    path = ROOT / "tests" / "fixtures" / "report_quality" / filename
    return path.read_text(encoding="utf-8")


def quality_report(rank_body, next_actions=None, risks=None, profile_extra=None, appendix=None):
    if next_actions is None:
        next_actions = """1. Read the recent official or bibliographic paper and write a short fit note.
2. Verify the official admissions path, quota, eligibility, and timing.
3. Prepare a student-controlled outreach note with project fit and contact the supervisor."""
    if risks is None:
        risks = "- Public sources do not confirm current quota."
    if profile_extra is None:
        profile_extra = "- Field: mathematics\n- Background signals: numerical analysis coursework"
    if appendix is None:
        appendix = "- Faculty profile [official]\n- Publication record [bibliographic]"
    return """# Demo

## Generation Note

Public-source demo.

## Student Profile

{profile_extra}

## Ranked Shortlist

{rank_body}

## Risks And Unknowns

{risks}

## Source Appendix

{appendix}

## Maybe List

- Maybe candidate.

## Excluded List

- Excluded candidate.

## Next Actions

{next_actions}
""".format(
        rank_body=rank_body,
        next_actions=next_actions,
        risks=risks,
        profile_extra=profile_extra,
        appendix=appendix,
    )


def valid_rank_body(extra=None):
    lines = [
        "### Rank 1: Prof. One",
        "",
        "- Institution: Example University",
        "- Eligibility: official profile confirms doctoral-supervisor status [official].",
        "- Risk level: medium",
        "",
        "#### Fit Scores",
        "",
        "- Research fit: 4/5 because official and bibliographic evidence align.",
        "- Path fit: 3/5 because current quota is unknown.",
        "- Career fit: 4/5 because the topic supports research preparation.",
        "- Evidence strength: 4/5 because the section uses official and bibliographic evidence.",
        "- Risk and uncertainty: 3/5 because quota and project availability remain unknown.",
        "",
        "#### Recent Work",
        "",
        "- 2025 representative paper [bibliographic]",
        "- Official faculty profile [official]",
        "",
        "#### Why This Fit",
        "",
        "Fact: official profile supports the role [official].",
        "Inference: bibliographic work supports the research fit [bibliographic].",
        "Unknown: current quota and project availability require direct verification.",
        "",
        "#### Questions To Ask",
        "",
        "- Are there current quota or project openings for incoming students?",
    ]
    if extra:
        lines.extend(["", extra])
    return "\n".join(lines)


class ValidatorUnitTests(unittest.TestCase):
    def test_validator_required_reports_include_mainland_math_demo(self):
        self.assertIn(
            "examples/reports/real_mainland_math_demo.md",
            REQUIRED_REPORT_EXAMPLES,
        )

    def test_validator_and_install_required_reports_stay_in_sync(self):
        install_reports = sorted(
            path for path in REQUIRED_FILES if path.startswith("examples/reports/")
        )
        self.assertEqual(sorted(REQUIRED_REPORT_EXAMPLES), install_reports)

    def test_validate_reports_reports_missing_required_mainland_math_demo(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report_dir = root / "skills" / "find-my-supervisor" / "examples" / "reports"
            report_dir.mkdir(parents=True)
            (root / "skills" / "find-my-supervisor" / "references").mkdir()
            (root / "skills" / "find-my-supervisor" / "references" / "source-protocol.md").write_text(
                "## Evidence Labels\n- official\n- bibliographic\n",
                encoding="utf-8",
            )
            for relative_path in REQUIRED_REPORT_EXAMPLES:
                if relative_path.endswith("real_mainland_math_demo.md"):
                    continue
                (root / "skills" / "find-my-supervisor" / relative_path).write_text(
                    "# placeholder\n",
                    encoding="utf-8",
                )

            issues = validate_reports(root)

            self.assertIn(
                ValidationIssue(
                    str(
                        root
                        / "skills"
                        / "find-my-supervisor"
                        / "examples"
                        / "reports"
                        / "real_mainland_math_demo.md"
                    ),
                    "missing report example",
                ),
                issues,
            )

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
1. Read the recent paper and write a short fit note.
2. Verify official admissions path, eligibility, quota, and timing.
3. Prepare a research-fit outreach note and contact the supervisor.
"""
        self.assertEqual(
            validate_report_quality(text, "demo.md", set(["official", "bibliographic"])),
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
1. Read the recent paper and write a short fit note.
2. Verify official admissions path, eligibility, quota, and timing.
3. Prepare a research-fit outreach note and contact the supervisor.
"""
        self.assertEqual(
            validate_report_quality(text, "demo.md", set(["official", "bibliographic"])),
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
1. Read the recent paper and write a short fit note.
2. Verify official admissions path, eligibility, quota, and timing.
3. Prepare a research-fit outreach note and contact the supervisor.
"""
        self.assertEqual(
            validate_report_quality(text, "demo.md", set(["official", "bibliographic"])),
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

Public profile and publication evidence are available [official] [bibliographic].

## Risks And Unknowns

## Source Appendix

- Demo source [official]
- Publication source [bibliographic]

## Maybe List

## Excluded List

## Next Actions
1. Read the recent paper and write a short fit note.
2. Verify official admissions path, eligibility, quota, and timing.
3. Prepare a research-fit outreach note and contact the supervisor.
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
- Publication source [bibliographic]

## Maybe List

## Next Actions
1. Read the recent paper and write a short fit note.
2. Verify official admissions path, eligibility, quota, and timing.
3. Prepare a research-fit outreach note and contact the supervisor.
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
1. Read the recent paper and write a short fit note.
2. Verify official admissions path, eligibility, quota, and timing.
3. Prepare a research-fit outreach note and contact the supervisor.
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
1. Read the recent paper and write a short fit note.
2. Verify official admissions path, eligibility, quota, and timing.
3. Prepare a research-fit outreach note and contact the supervisor.
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
1. Read the recent paper and write a short fit note.
2. Verify official admissions path, eligibility, quota, and timing.
3. Prepare a research-fit outreach note and contact the supervisor.
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
1. Read the recent paper and write a short fit note.
2. Verify official admissions path, eligibility, quota, and timing.
3. Prepare a research-fit outreach note and contact the supervisor.
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
1. Read the recent paper and write a short fit note.
2. Verify official admissions path, eligibility, quota, and timing.
3. Prepare a research-fit outreach note and contact the supervisor.
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
1. Read the recent paper and write a short fit note.
2. Verify official admissions path, eligibility, quota, and timing.
3. Prepare a research-fit outreach note and contact the supervisor.
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
1. Read the recent paper and write a short fit note.
2. Verify official admissions path, eligibility, quota, and timing.
3. Prepare a research-fit outreach note and contact the supervisor.
"""
        issues = validate_report_quality(
            text,
            "real_demo.md",
            set(["official", "bibliographic"]),
        )
        self.assertIn(
            ValidationIssue(
                "real_demo.md",
                "real demo report contains admissions-certainty language: guaranteed admission",
            ),
            issues,
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
1. Read the recent paper and write a short fit note.
2. Verify official admissions path, eligibility, quota, and timing.
3. Prepare a research-fit outreach note and contact the supervisor.
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
1. Read the recent paper and write a short fit note.
2. Verify official admissions path, eligibility, quota, and timing.
3. Prepare a research-fit outreach note and contact the supervisor.
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
1. Read the recent paper and write a short fit note.
2. Verify official admissions path, eligibility, quota, and timing.
3. Prepare a research-fit outreach note and contact the supervisor.
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
1. Read the recent paper and write a short fit note.
2. Verify official admissions path, eligibility, quota, and timing.
3. Prepare a research-fit outreach note and contact the supervisor.
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
1. Read the recent paper and write a short fit note.
2. Verify official admissions path, eligibility, quota, and timing.
3. Prepare a research-fit outreach note and contact the supervisor.
"""
        self.assertEqual(
            validate_report_quality(
                text,
                "demo.md",
                set(["official", "bibliographic"]),
            ),
            [ValidationIssue("demo.md", "missing risk level")],
        )

    def test_validate_report_quality_requires_two_strong_sources_per_rank(self):
        rank_body = """### Rank 1: Prof. One

- Institution: Example University
- Eligibility: current quota must be verified.
- Risk level: medium

#### Fit Scores

- Research fit: 4/5 because one official source and community notes are available.
- Path fit: 3/5 because current quota is unknown.
- Career fit: 4/5 because the topic supports research preparation.
- Evidence strength: 2/5 because only one strong public source is available.
- Risk and uncertainty: 3/5 because quota and project availability remain unknown.

#### Recent Work

- Official faculty profile [official]
- Community discussion [community]

#### Why This Fit

Fact: official profile supports the role.
Inference: community discussion is not strong support [community].
Unknown: current quota and project availability require direct verification.

#### Questions To Ask

- Are there current quota or project openings for incoming students?"""
        issues = validate_report_quality(
            quality_report(
                rank_body,
                appendix="- Faculty profile [official]\n- Community note [community]",
            ),
            "demo.md",
            set(["official", "bibliographic", "community"]),
        )
        self.assertIn(
            ValidationIssue(
                "demo.md",
                "ranked supervisor has fewer than two strong source-labeled evidence mentions",
            ),
            issues,
        )

    def test_validate_report_quality_requires_official_or_bibliographic_per_rank(self):
        rank_body = valid_rank_body().replace("[official]", "[lab_or_homepage]").replace(
            "[bibliographic]", "[project_or_repository]"
        )
        issues = validate_report_quality(
            quality_report(
                rank_body,
                appendix="- Lab page [lab_or_homepage]\n- Repository [project_or_repository]",
            ),
            "demo.md",
            set(["official", "bibliographic", "lab_or_homepage", "project_or_repository"]),
        )
        self.assertIn(
            ValidationIssue(
                "demo.md",
                "ranked supervisor lacks official or bibliographic source support",
            ),
            issues,
        )

    def test_validate_report_quality_requires_ranked_labels_in_source_appendix(self):
        issues = validate_report_quality(
            quality_report(
                valid_rank_body(),
                appendix="- [Faculty profile](https://example.edu/profile) [official]",
            ),
            "demo.md",
            set(["official", "bibliographic"]),
        )
        self.assertIn(
            ValidationIssue(
                "demo.md",
                "ranked source label missing from source appendix: bibliographic",
            ),
            issues,
        )

    def test_validate_report_quality_requires_key_judgment_source_signal(self):
        rank_body = valid_rank_body().replace(
            "- Eligibility: official profile confirms doctoral-supervisor status [official].",
            "- Eligibility: doctoral-supervisor status is confirmed.",
        ).replace(
            "- 2025 representative paper [bibliographic]",
            "- 2025 representative paper",
        )
        issues = validate_report_quality(
            quality_report(rank_body),
            "demo.md",
            set(["official", "bibliographic"]),
        )
        self.assertIn(
            ValidationIssue(
                "demo.md",
                "eligibility line lacks source label or conservative verification language",
            ),
            issues,
        )
        self.assertIn(
            ValidationIssue(
                "demo.md",
                "recent work item lacks source label or conservative verification language",
            ),
            issues,
        )

    def test_validate_report_quality_rejects_decorative_unknowns(self):
        rank_body = valid_rank_body().replace(
            "Unknown: current quota and project availability require direct verification.",
            "Unknown: N/A.",
        )
        issues = validate_report_quality(
            quality_report(rank_body),
            "demo.md",
            set(["official", "bibliographic"]),
        )
        self.assertIn(
            ValidationIssue("demo.md", "unknown evidence line is decorative or non-actionable"),
            issues,
        )

    def test_validate_report_quality_requires_questions_or_actions_cover_unknowns(self):
        rank_body = valid_rank_body().replace(
            "- Are there current quota or project openings for incoming students?",
            "- Is this a good fit?",
        )
        issues = validate_report_quality(
            quality_report(
                rank_body,
                next_actions="1. Read the recent paper and write a short fit note.\n2. Verify official admissions path and timing.\n3. Prepare a research-fit outreach note and contact the supervisor.",
            ),
            "demo.md",
            set(["official", "bibliographic"]),
        )
        self.assertIn(
            ValidationIssue(
                "demo.md",
                "questions or next actions do not address concrete unknown categories",
            ),
            issues,
        )

    def test_validate_report_quality_rejects_generic_next_actions(self):
        issues = validate_report_quality(
            quality_report(
                valid_rank_body(),
                next_actions="1. Read papers.\n2. Contact professors.\n3. Apply.",
            ),
            "demo.md",
            set(["official", "bibliographic"]),
        )
        self.assertIn(
            ValidationIssue("demo.md", "next actions are too generic"),
            issues,
        )

    def test_validate_report_quality_rejects_single_generic_next_action(self):
        issues = validate_report_quality(
            quality_report(
                valid_rank_body(),
                next_actions="1. Read papers.\n2. Verify official admissions path, eligibility, quota, and timing.\n3. Prepare a research-fit outreach note and contact the supervisor.",
            ),
            "demo.md",
            set(["official", "bibliographic"]),
        )
        self.assertIn(
            ValidationIssue("demo.md", "next actions are too generic"),
            issues,
        )

    def test_validate_report_quality_requires_current_student_action_for_advising_risk(self):
        issues = validate_report_quality(
            quality_report(
                valid_rank_body(),
                risks="- Recent publications do not establish advising style.",
            ),
            "demo.md",
            set(["official", "bibliographic"]),
        )
        self.assertIn(
            ValidationIssue(
                "demo.md",
                "advising or lab-culture risks require current-student/alumni verification action",
            ),
            issues,
        )

    def test_validate_report_quality_applies_overclaim_checks_to_all_reports(self):
        rank_body = valid_rank_body().replace(
            "- Eligibility: official profile confirms doctoral-supervisor status [official].",
            "- Eligibility: the supervisor has quota and will take strong students [official].",
        )
        issues = validate_report_quality(
            quality_report(rank_body),
            "non_real_demo.md",
            set(["official", "bibliographic"]),
        )
        self.assertIn(
            ValidationIssue(
                "non_real_demo.md",
                "report contains overclaim or judgmental language: has quota",
            ),
            issues,
        )

    def test_validate_report_quality_allows_conservative_quota_statement(self):
        text = quality_report(valid_rank_body())
        self.assertNotIn(
            ValidationIssue(
                "demo.md",
                "report contains overclaim or judgmental language: has quota",
            ),
            validate_report_quality(text, "demo.md", set(["official", "bibliographic"])),
        )

    def test_validate_report_quality_rejects_math_to_ai_coursework_only_claim(self):
        profile = """- Field: mathematics
- Target scope: CS/AI lab
- Research interests: artificial intelligence and machine learning
- Background signals: mathematics and statistics coursework"""
        rank_body = valid_rank_body().replace(
            "- Research fit: 4/5 because official and bibliographic evidence align.",
            "- Research fit: 5/5 because mathematics/statistics coursework alone proves strong AI fit.",
        )
        issues = validate_report_quality(
            quality_report(rank_body, profile_extra=profile),
            "demo.md",
            set(["official", "bibliographic"]),
        )
        self.assertIn(
            ValidationIssue(
                "demo.md",
                "math/statistics-to-CS/AI report lacks AI/CS readiness evidence or explicit preparation gaps",
            ),
            issues,
        )

    def test_validate_report_quality_rejects_exploratory_rank_with_fewer_than_two_strong_sources(self):
        rank_body = """### Rank 1: Prof. One

- Institution: Example University
- Eligibility: current quota must be verified.
- Risk level: medium

#### Fit Scores

- Research fit: 3/5 because this is exploratory and source coverage is limited.
- Path fit: 3/5 because current quota is unknown.
- Career fit: 4/5 because the topic supports research preparation.
- Evidence strength: 2/5 because only one strong public source is available.
- Risk and uncertainty: 3/5 because quota and project availability remain unknown.

#### Recent Work

- Official faculty profile [official]
- Community discussion [community]

#### Why This Fit

Fact: official profile supports the role.
Inference: community discussion is not strong support [community].
Unknown: current quota and project availability require direct verification.

#### Questions To Ask

- Are there current quota or project openings for incoming students?"""
        issues = validate_report_quality(
            quality_report(
                rank_body,
                appendix="- Faculty profile [official]\n- Community note [community]",
            ),
            "demo.md",
            set(["official", "bibliographic", "community"]),
        )
        self.assertIn(
            ValidationIssue(
                "demo.md",
                "ranked supervisor has fewer than two strong source-labeled evidence mentions",
            ),
            issues,
        )

    def test_validate_report_quality_requires_every_unknown_group_to_be_addressed(self):
        rank_body = valid_rank_body().replace(
            "Unknown: current quota and project availability require direct verification.",
            "Unknown: current quota, funding, and advising style require direct verification.",
        ).replace(
            "- Are there current quota or project openings for incoming students?",
            "- Are there current quota or openings for incoming students?",
        )
        issues = validate_report_quality(
            quality_report(
                rank_body,
                next_actions="1. Read the recent paper and write a short fit note.\n2. Verify official admissions path, eligibility, quota, and timing.\n3. Prepare a research-fit outreach note and contact the supervisor.",
            ),
            "demo.md",
            set(["official", "bibliographic"]),
        )
        self.assertIn(
            ValidationIssue(
                "demo.md",
                "questions or next actions do not address concrete unknown categories",
            ),
            issues,
        )

    def test_validate_report_quality_cross_field_readiness_ignores_generic_next_action_paper(self):
        profile = """- Field: mathematics
- Target scope: CS/AI lab
- Research interests: artificial intelligence and machine learning
- Background signals: mathematics and statistics coursework"""
        issues = validate_report_quality(
            quality_report(
                valid_rank_body(),
                profile_extra=profile,
                next_actions="1. Read the recent paper and write a short fit note.\n2. Verify official admissions path, eligibility, quota, and timing.\n3. Prepare a research-fit outreach note and contact the supervisor.",
            ),
            "demo.md",
            set(["official", "bibliographic"]),
        )
        self.assertIn(
            ValidationIssue(
                "demo.md",
                "math/statistics-to-CS/AI report lacks AI/CS readiness evidence or explicit preparation gaps",
            ),
            issues,
        )

    def test_validate_report_quality_overclaim_unknown_quota_does_not_exempt_will_take(self):
        rank_body = valid_rank_body().replace(
            "- Eligibility: official profile confirms doctoral-supervisor status [official].",
            "- Eligibility: Current quota is unknown, but the supervisor will take strong students this year [official].",
        )
        issues = validate_report_quality(
            quality_report(rank_body),
            "demo.md",
            set(["official", "bibliographic"]),
        )
        self.assertIn(
            ValidationIssue(
                "demo.md",
                "report contains overclaim or judgmental language: will take",
            ),
            issues,
        )

    def test_validate_report_quality_overclaim_before_unknown_quota_still_fails(self):
        rank_body = valid_rank_body().replace(
            "- Eligibility: official profile confirms doctoral-supervisor status [official].",
            "- Eligibility: The supervisor will take strong students, but current quota is unknown [official].",
        )
        issues = validate_report_quality(
            quality_report(rank_body),
            "demo.md",
            set(["official", "bibliographic"]),
        )
        self.assertIn(
            ValidationIssue(
                "demo.md",
                "report contains overclaim or judgmental language: will take",
            ),
            issues,
        )

    def test_validate_report_quality_allows_avoid_in_safety_instruction(self):
        issues = validate_report_quality(
            quality_report(
                valid_rank_body(),
                risks="- Avoid relying on unsourced community claims.",
            ),
            "demo.md",
            set(["official", "bibliographic"]),
        )
        self.assertNotIn(
            ValidationIssue(
                "demo.md",
                "report contains overclaim or judgmental language: avoid",
            ),
            issues,
        )

    def test_validate_report_quality_rejects_generic_next_action_variants(self):
        issues = validate_report_quality(
            quality_report(
                valid_rank_body(),
                next_actions="1. Read more papers.\n2. Contact professors about fit.\n3. Apply to programs.\n4. Do more research on supervisors.",
            ),
            "demo.md",
            set(["official", "bibliographic"]),
        )
        self.assertIn(
            ValidationIssue("demo.md", "next actions are too generic"),
            issues,
        )

    def test_validate_report_quality_allows_specific_paper_reading_action(self):
        issues = validate_report_quality(
            quality_report(
                valid_rank_body(),
                next_actions="1. Read one recent paper from each ranked supervisor and write a 3-5 sentence fit note.\n2. Verify official admissions path, eligibility, quota, and timing.\n3. Prepare a research-fit outreach note and contact the supervisor.",
            ),
            "demo.md",
            set(["official", "bibliographic"]),
        )
        self.assertNotIn(
            ValidationIssue("demo.md", "next actions are too generic"),
            issues,
        )

    def test_validate_report_quality_project_availability_needs_availability_response(self):
        rank_body = valid_rank_body().replace(
            "Unknown: current quota and project availability require direct verification.",
            "Unknown: project availability requires direct verification.",
        ).replace(
            "- Are there current quota or project openings for incoming students?",
            "- Is there project fit for incoming students?",
        )
        issues = validate_report_quality(
            quality_report(
                rank_body,
                next_actions="1. Read the recent paper and write a short fit note.\n2. Verify official admissions path, eligibility, quota, and timing.\n3. Prepare a research-fit outreach note and contact the supervisor about project fit.",
            ),
            "demo.md",
            set(["official", "bibliographic"]),
        )
        self.assertIn(
            ValidationIssue(
                "demo.md",
                "questions or next actions do not address concrete unknown categories",
            ),
            issues,
        )

    def test_validate_report_quality_ignores_markdown_link_text_with_destination_parentheses(self):
        text = quality_report(
            valid_rank_body(),
            appendix="- [official profile](https://example.edu/a_(b)) [official]\n- Publication record [bibliographic]",
        )
        self.assertEqual(
            validate_report_quality(text, "demo.md", set(["official", "bibliographic"])),
            [],
        )

    def test_validate_report_quality_rejects_broad_conservative_eligibility_language(self):
        rank_body = valid_rank_body().replace(
            "- Eligibility: official profile confirms doctoral-supervisor status [official].",
            "- Eligibility: current quota.",
        ).replace(
            "- 2025 representative paper [bibliographic]",
            "- Current quota",
        )
        issues = validate_report_quality(
            quality_report(rank_body),
            "demo.md",
            set(["official", "bibliographic"]),
        )
        self.assertIn(
            ValidationIssue(
                "demo.md",
                "eligibility line lacks source label or conservative verification language",
            ),
            issues,
        )
        self.assertIn(
            ValidationIssue(
                "demo.md",
                "recent work item lacks source label or conservative verification language",
            ),
            issues,
        )


if __name__ == "__main__":
    unittest.main()
