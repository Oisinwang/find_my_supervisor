import json
import re
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
REPORT_COMMON_REQUIRED_SECTIONS = [
    "## Student Profile",
    "## Ranked Shortlist",
    "#### Fit Scores",
    "## Risks And Unknowns",
    "## Source Appendix",
    "## Next Actions",
]
REPORT_REQUIRED_LIST_SECTIONS = ["## Maybe List", "## Excluded List"]
REPORT_NOTE_SECTIONS = ["## Synthetic Fixture Notice", "## Generation Note"]
ALLOWED_RISK_LEVELS = set(["low", "medium", "medium_high", "high", "unknown"])
FIT_SCORE_LABELS = [
    "Research fit",
    "Path fit",
    "Career fit",
    "Evidence strength",
    "Risk and uncertainty",
]
EVIDENCE_LINE_LABELS = ["Fact", "Inference", "Unknown"]
REAL_REPORT_SYNTHETIC_PHRASES = [
    "synthetic fixture notice",
    "synthetic validation fixture",
    "supervisor names, papers, labs, and urls are fictional",
    "supervisor names, papers, seminars, and urls are fictional",
    "must not be used as real application advice",
    "prof. synthetic",
    "synthetic sources",
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
RUBRIC_REQUIRED_FILES = {
    "cs-ai.md": ["## Core Dimensions", "## Subfield Notes", "## Common Misreads"],
    "math-subfields.md": [
        "## Common Math Dimensions",
        "## Pure Mathematics",
        "## Applied Mathematics",
        "## Computational Mathematics",
        "## Operations Research And Optimization",
        "## Statistics And Probability",
    ],
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


def validate_required_report_lists(text, location):
    return validate_markdown_sections(text, REPORT_REQUIRED_LIST_SECTIONS, location)


def extract_risk_level(section):
    match = re.search(r"(?im)^\s*[-*]\s*Risk level\s*:\s*([^\s]+)\s*$", section)
    if not match:
        return None
    return match.group(1).lower()


def validate_risk_levels(text, location):
    issues = []
    rank_sections = extract_rank_sections(text)
    if not rank_sections:
        rank_sections = [text]
    for section in rank_sections:
        risk_level = extract_risk_level(section)
        if risk_level is None:
            issues.append(ValidationIssue(location, "missing risk level"))
        elif risk_level not in ALLOWED_RISK_LEVELS:
            issues.append(
                ValidationIssue(location, "invalid risk level: {}".format(risk_level))
            )
    return issues


def extract_allowed_source_labels(text):
    labels = set()
    in_labels = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "## Evidence Labels":
            in_labels = True
            continue
        if in_labels and stripped.startswith("## "):
            break
        if in_labels:
            match = re.match(r"^-\s+([A-Za-z0-9_]+)\s*$", stripped)
            if match:
                labels.add(match.group(1))
    return labels


def load_allowed_source_labels(root):
    path = root / "skills" / "find-my-supervisor" / "references" / "source-protocol.md"
    if not path.exists():
        return set()
    return extract_allowed_source_labels(path.read_text(encoding="utf-8"))


def extract_source_appendix(text):
    match = re.search(r"(?im)^## Source Appendix\s*$", text)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"(?im)^##\s+", text[start:])
    if next_heading:
        return text[start : start + next_heading.start()]
    return text[start:]


def extract_ranked_shortlist(text):
    match = re.search(r"(?im)^## Ranked Shortlist\s*$", text)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"(?im)^##\s+", text[start:])
    if next_heading:
        return text[start : start + next_heading.start()]
    return text[start:]


def extract_rank_sections(text):
    ranked_shortlist = extract_ranked_shortlist(text)
    if not ranked_shortlist:
        return []
    matches = list(re.finditer(r"(?im)^### Rank\s+", ranked_shortlist))
    sections = []
    for index, match in enumerate(matches):
        start = match.start()
        if index + 1 < len(matches):
            end = matches[index + 1].start()
        else:
            end = len(ranked_shortlist)
        sections.append(ranked_shortlist[start:end])
    return sections


def extract_fit_scores_block(text):
    match = re.search(r"(?im)^#### Fit Scores\s*$", text)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"(?im)^#{2,4}\s+", text[start:])
    if next_heading:
        return text[start : start + next_heading.start()]
    return text[start:]


def validate_fit_scores_in_text(text, location):
    issues = []
    fit_scores_block = extract_fit_scores_block(text)
    for label in FIT_SCORE_LABELS:
        pattern = r"(?im)^\s*(?:[-*]\s*)?{}\s*:".format(re.escape(label))
        if not re.search(pattern, fit_scores_block):
            issues.append(ValidationIssue(location, "missing fit score: {}".format(label)))
    return issues


def validate_fit_scores(text, location):
    issues = []
    rank_sections = extract_rank_sections(text)
    if not rank_sections:
        rank_sections = [text]
    for section in rank_sections:
        issues.extend(validate_fit_scores_in_text(section, location))
    return issues


def validate_evidence_lines_in_text(text, location):
    missing = []
    for label in EVIDENCE_LINE_LABELS:
        escaped_label = re.escape(label)
        heading_pattern = r"(?im)^\s*#{{2,6}}\s*{}s?\s*$".format(escaped_label)
        line_pattern = r"(?im)^\s*(?:[-*]\s*)?{}s?\s*:".format(escaped_label)
        if not (
            re.search(heading_pattern, text)
            or re.search(line_pattern, text)
        ):
            missing.append(label)
    if missing:
        return [
            ValidationIssue(
                location,
                "missing fact/inference/unknown evidence lines",
            )
        ]
    return []


def validate_evidence_lines(text, location):
    issues = []
    rank_sections = extract_rank_sections(text)
    if not rank_sections:
        rank_sections = [text]
    for section in rank_sections:
        issues.extend(validate_evidence_lines_in_text(section, location))
    return issues


def validate_source_appendix_labels(text, location, allowed_source_labels):
    issues = []
    appendix = extract_source_appendix(text)
    seen_invalid = set()
    missing_label = False
    for line in appendix.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or not stripped.startswith(("-", "*")):
            continue
        label_matches = list(re.finditer(r"\[([^\[\]]+)\]", stripped))
        if not label_matches:
            missing_label = True
            continue
        for label_match in label_matches:
            for label in label_match.group(1).split("/"):
                atomic_label = label.strip()
                if atomic_label and atomic_label not in allowed_source_labels:
                    seen_invalid.add(atomic_label)
    if missing_label:
        issues.append(ValidationIssue(location, "source appendix entry missing label"))
    for label in sorted(seen_invalid):
        issues.append(ValidationIssue(location, "invalid source label: {}".format(label)))
    return issues


def is_real_demo_report(location):
    return Path(location).name.startswith("real_")


def validate_real_demo_language(text, location):
    if not is_real_demo_report(location):
        return []
    lowered = text.lower()
    for phrase in REAL_REPORT_SYNTHETIC_PHRASES:
        if phrase in lowered:
            return [
                ValidationIssue(
                    location,
                    "real demo report contains synthetic fixture language",
                )
            ]
    return []


def validate_report_quality(text, location, allowed_source_labels):
    issues = []
    issues.extend(validate_markdown_sections(text, REPORT_COMMON_REQUIRED_SECTIONS, location))
    if not any(section in text for section in REPORT_NOTE_SECTIONS):
        issues.append(
            ValidationIssue(
                location,
                "missing section: ## Synthetic Fixture Notice or ## Generation Note",
            )
        )
    issues.extend(validate_required_report_lists(text, location))
    issues.extend(validate_risk_levels(text, location))
    issues.extend(validate_fit_scores(text, location))
    issues.extend(validate_evidence_lines(text, location))
    issues.extend(validate_source_appendix_labels(text, location, allowed_source_labels))
    issues.extend(validate_real_demo_language(text, location))
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
    expected = [
        "synthetic_cs_ai_shortlist.md",
        "synthetic_math_shortlist.md",
        "real_hkust_trustworthy_llm_demo.md",
    ]
    issues = []
    allowed_source_labels = load_allowed_source_labels(root)
    for filename in expected:
        path = report_dir / filename
        if not path.exists():
            issues.append(ValidationIssue(str(path), "missing report example"))
    if not report_dir.exists():
        return issues
    for path in sorted(report_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        issues.extend(validate_report_quality(text, str(path), allowed_source_labels))
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


def validate_rubrics(root):
    rubric_dir = root / "skills" / "find-my-supervisor" / "references" / "rubrics"
    issues = []
    for filename, sections in RUBRIC_REQUIRED_FILES.items():
        path = rubric_dir / filename
        if not path.exists():
            issues.append(ValidationIssue(str(path), "missing rubric file"))
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
    issues.extend(validate_rubrics(root))
    issues.extend(validate_reports(root))
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
