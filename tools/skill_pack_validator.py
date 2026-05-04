import json
from pathlib import Path


class ValidationIssue(object):
    def __init__(self, location, message):
        self.location = location
        self.message = message

    def __eq__(self, other):
        return (
            isinstance(other, ValidationIssue)
            and self.location == other.location
            and self.message == other.message
        )

    def __repr__(self):
        return "ValidationIssue(location={!r}, message={!r})".format(
            self.location,
            self.message,
        )


SCHEMA_REQUIRED_KEYS = ["$schema", "title", "type", "required", "properties"]
PROFILE_REQUIRED_KEYS = [
    "field",
    "subfield",
    "application_path",
    "target_scope",
    "research_interests",
    "career_orientation",
    "background_summary",
]
SKILL_REQUIRED_SECTIONS = [
    "## When To Use",
    "## Required Inputs",
    "## Workflow",
    "## Evidence Rules",
    "## Output",
    "## References",
]
REPORT_REQUIRED_SECTIONS = [
    "## Synthetic Fixture Notice",
    "## Student Profile",
    "## Ranked Shortlist",
    "#### Fit Scores",
    "## Risks And Unknowns",
    "## Source Appendix",
    "## Next Actions",
]
REFERENCE_REQUIRED_FILES = {
    "source-protocol.md": [
        "## Source Priority",
        "## Minimum Evidence For Recommendation",
        "## Publication Handling",
        "## Identity Matching",
        "## Evidence Labels",
    ],
    "risk-policy.md": [
        "## Purpose",
        "## Allowed Risk Categories",
        "## Credibility Levels",
        "## Handling Community Information",
        "## Report Language",
    ],
    "report-template.md": REPORT_REQUIRED_SECTIONS,
}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def require_keys(data, required_keys, location):
    issues = []
    for key in required_keys:
        if key not in data:
            issues.append(ValidationIssue(location, "missing required key: {}".format(key)))
    return issues


def validate_markdown_sections(text, required_sections, location):
    issues = []
    for section in required_sections:
        if section not in text:
            issues.append(ValidationIssue(location, "missing section: {}".format(section)))
    return issues


def validate_json_file(path):
    try:
        load_json(path)
    except ValueError as exc:
        return [ValidationIssue(str(path), "invalid JSON: {}".format(exc))]
    return []


def validate_schema_files(root):
    schema_dir = root / "skills" / "find-my-supervisor" / "schemas"
    expected = [
        "student-search-profile.schema.json",
        "target-institution.schema.json",
        "candidate-supervisor.schema.json",
        "supervisor-evidence-profile.schema.json",
        "supervisor-fit-assessment.schema.json",
        "report-summary.schema.json",
    ]
    issues = []
    for filename in expected:
        path = schema_dir / filename
        if not path.exists():
            issues.append(ValidationIssue(str(path), "missing schema file"))
            continue
        issues.extend(validate_json_file(path))
        data = load_json(path)
        if isinstance(data, dict):
            issues.extend(require_keys(data, SCHEMA_REQUIRED_KEYS, str(path)))
        else:
            issues.append(ValidationIssue(str(path), "schema root must be an object"))
    return issues


def validate_profile_examples(root):
    profile_dir = root / "skills" / "find-my-supervisor" / "examples" / "profiles"
    expected = [
        "cs_ai_direct_phd_llm_eval.json",
        "math_computational_research_master.json",
        "math_statistics_master_quant.json",
    ]
    issues = []
    for filename in expected:
        path = profile_dir / filename
        if not path.exists():
            issues.append(ValidationIssue(str(path), "missing profile example"))
            continue
        issues.extend(validate_json_file(path))
        data = load_json(path)
        if isinstance(data, dict):
            issues.extend(require_keys(data, PROFILE_REQUIRED_KEYS, str(path)))
        else:
            issues.append(ValidationIssue(str(path), "profile root must be an object"))
    return issues


def validate_skill_file(root):
    skill_path = root / "skills" / "find-my-supervisor" / "SKILL.md"
    if not skill_path.exists():
        return [ValidationIssue(str(skill_path), "missing skill file")]
    text = skill_path.read_text(encoding="utf-8")
    issues = validate_markdown_sections(text, SKILL_REQUIRED_SECTIONS, str(skill_path))
    for phrase in ["985", "CAS/UCAS", "HKU", "CUHK", "HKUST", "CS/AI", "mathematics"]:
        if phrase not in text:
            issues.append(ValidationIssue(str(skill_path), "missing scope phrase: {}".format(phrase)))
    return issues


def validate_reports(root):
    report_dir = root / "skills" / "find-my-supervisor" / "examples" / "reports"
    expected = ["synthetic_cs_ai_shortlist.md", "synthetic_math_shortlist.md"]
    issues = []
    for filename in expected:
        path = report_dir / filename
        if not path.exists():
            issues.append(ValidationIssue(str(path), "missing report example"))
            continue
        text = path.read_text(encoding="utf-8")
        issues.extend(validate_markdown_sections(text, REPORT_REQUIRED_SECTIONS, str(path)))
    return issues


def validate_reference_files(root):
    reference_dir = root / "skills" / "find-my-supervisor" / "references"
    issues = []
    for filename, sections in REFERENCE_REQUIRED_FILES.items():
        path = reference_dir / filename
        if not path.exists():
            issues.append(ValidationIssue(str(path), "missing reference file"))
            continue
        text = path.read_text(encoding="utf-8")
        issues.extend(validate_markdown_sections(text, sections, str(path)))
    return issues


def run_all(root):
    issues = []
    issues.extend(validate_schema_files(root))
    issues.extend(validate_profile_examples(root))
    issues.extend(validate_skill_file(root))
    issues.extend(validate_reference_files(root))
    return issues


def main():
    root = Path(__file__).resolve().parents[1]
    issues = run_all(root)
    if issues:
        for issue in issues:
            print("{}: {}".format(issue.location, issue.message))
        return 1
    print("Skill pack validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
