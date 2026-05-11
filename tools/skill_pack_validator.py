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
WEAK_SOURCE_LABELS = set(["community", "inferred", "unknown"])
REQUIRED_STRONG_SOURCE_LABELS = set(["official", "bibliographic"])
CONCRETE_UNKNOWN_TARGETS = [
    "quota",
    "opening",
    "openings",
    "funding",
    "advising style",
    "advising",
    "project availability",
    "project",
    "application path",
    "eligibility",
    "current students",
    "current student",
    "preparation gap",
    "preparation",
    "identity ambiguity",
    "identity",
    "availability",
    "capacity",
    "supervision structure",
    "supervision",
]
CONSERVATIVE_VERIFICATION_PHRASES = [
    "must be verified",
    "should be verified",
    "needs verification",
    "need verification",
    "requires verification",
    "require verification",
    "requires direct verification",
    "require direct verification",
    "verify",
    "unknown",
    "unverified",
    "does not confirm",
    "do not confirm",
    "not confirmed",
    "no public evidence",
    "public evidence does not",
    "public pages do not",
]
UNKNOWN_TARGET_GROUPS = [
    (
        "capacity_path",
        [
            "quota",
            "opening",
            "openings",
            "funding",
            "application path",
            "eligibility",
            "availability",
            "capacity",
            "admissions",
            "admission",
            "direct phd",
            "mphil",
            "master's",
            "masters",
        ],
    ),
    (
        "project_availability",
        [
            "project availability",
            "project openings",
            "project opening",
            "current projects",
            "current project",
            "available projects",
            "available project",
            "first-year projects",
            "first-year project",
            "can join",
            "join projects",
            "join project",
        ],
    ),
    (
        "project",
        [
            "project",
            "projects",
            "first-year",
            "topic",
            "topics",
            "current work",
        ],
    ),
    (
        "advising_lab",
        [
            "advising style",
            "advising",
            "current students",
            "current student",
            "alumni",
            "lab culture",
            "student outcomes",
            "supervision structure",
            "supervision",
            "cadence",
            "publication cadence",
            "ownership",
        ],
    ),
    (
        "preparation",
        [
            "preparation gap",
            "preparation",
            "preferred applicant background",
            "expected background",
            "background",
            "coding",
            "programming",
            "ml",
            "machine learning",
            "deep learning",
            "systems",
            "benchmark",
            "evaluation",
            "publication readiness",
        ],
    ),
    (
        "identity",
        [
            "identity ambiguity",
            "identity",
            "name ambiguity",
            "affiliation",
            "unit",
        ],
    ),
]
REAL_REPORT_SYNTHETIC_PHRASES = [
    "synthetic fixture notice",
    "synthetic validation fixture",
    "supervisor names, papers, labs, and urls are fictional",
    "supervisor names, papers, seminars, and urls are fictional",
    "must not be used as real application advice",
    "prof. synthetic",
    "synthetic sources",
]
REAL_REPORT_CERTAINTY_PHRASES = [
    "guaranteed admission",
    "definitely accepts",
    "safe supervisor",
    "bad supervisor",
    "will admit",
    "一定录取",
    "稳录",
    "必收",
]
REPORT_OVERCLAIM_PATTERNS = [
    ("has quota", r"\bhas\s+(?:a\s+)?quota\b"),
    ("has funding", r"\bhas\s+funding\b"),
    ("is accepting students", r"\bis\s+accepting\s+students\b"),
    ("will take", r"\bwill\s+take\b"),
    ("easy admission", r"\beasy\s+admission\b"),
    ("likely admission", r"\blikely\s+admission\b"),
    ("guaranteed offer", r"\bguaranteed\s+offer\b"),
    ("guaranteed admission", r"\bguaranteed\s+admission\b|\badmission\s+is\s+guaranteed\b"),
    ("toxic", r"\btoxic\b"),
    ("avoid", r"\bavoid\b"),
    ("bad supervisor", r"\bbad\s+supervisor\b"),
    ("safe supervisor", r"\bsafe\s+supervisor\b"),
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


def remove_markdown_links(text):
    output = []
    index = 0
    length = len(text)
    while index < length:
        if text[index] != "[":
            output.append(text[index])
            index += 1
            continue
        close_bracket = text.find("]", index + 1)
        if close_bracket == -1 or close_bracket + 1 >= length or text[close_bracket + 1] != "(":
            output.append(text[index])
            index += 1
            continue
        cursor = close_bracket + 2
        depth = 1
        while cursor < length:
            char = text[cursor]
            if char == "\\":
                cursor += 2
                continue
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    cursor += 1
                    break
            cursor += 1
        if depth == 0:
            index = cursor
        else:
            output.append(text[index])
            index += 1
    return "".join(output)


def extract_section_after_heading(text, heading):
    pattern = r"(?im)^{}\s*$".format(re.escape(heading))
    match = re.search(pattern, text)
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


def count_source_labels_in_text(text, allowed_source_labels):
    count = 0
    for label_match in re.finditer(r"\[([^\[\]]+)\]", remove_markdown_links(text)):
        labels = [label.strip() for label in label_match.group(1).split("/")]
        for label in labels:
            if label in allowed_source_labels and label not in WEAK_SOURCE_LABELS:
                count += 1
    return count


def extract_source_labels_in_text(text, allowed_source_labels):
    labels = []
    for label_match in re.finditer(r"\[([^\[\]]+)\]", remove_markdown_links(text)):
        for label in label_match.group(1).split("/"):
            atomic_label = label.strip()
            if atomic_label in allowed_source_labels:
                labels.append(atomic_label)
    return labels


def has_source_label(text, allowed_source_labels):
    return bool(extract_source_labels_in_text(text, allowed_source_labels))


def has_conservative_verification_language(text):
    lowered = text.lower()
    for phrase in CONSERVATIVE_VERIFICATION_PHRASES:
        if phrase in lowered:
            return True
    return False


def has_exploratory_uncertainty_language(text):
    lowered = text.lower()
    phrases = [
        "only one public source",
        "maybe list",
        "exploratory",
        "insufficient evidence",
        "source coverage is limited",
    ]
    for phrase in phrases:
        if phrase in lowered:
            return True
    return False


def validate_ranked_evidence_signals(text, location, allowed_source_labels):
    issues = []
    rank_sections = extract_rank_sections(text)
    if not rank_sections:
        rank_sections = [text]
    for section in rank_sections:
        if count_source_labels_in_text(section, allowed_source_labels) < 2 and not has_exploratory_uncertainty_language(section):
            issues.append(ValidationIssue(location, "ranked supervisor has fewer than two source-labeled evidence mentions"))
    return issues


def validate_ranked_source_sufficiency(text, location, allowed_source_labels):
    issues = []
    rank_sections = extract_rank_sections(text)
    if not rank_sections:
        rank_sections = [text]
    for section in rank_sections:
        labels = extract_source_labels_in_text(section, allowed_source_labels)
        strong_labels = [label for label in labels if label not in WEAK_SOURCE_LABELS]
        if len(strong_labels) < 2:
            issues.append(
                ValidationIssue(
                    location,
                    "ranked supervisor has fewer than two strong source-labeled evidence mentions",
                )
            )
        if not REQUIRED_STRONG_SOURCE_LABELS.intersection(set(labels)):
            issues.append(
                ValidationIssue(
                    location,
                    "ranked supervisor lacks official or bibliographic source support",
                )
            )
    return issues


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
        label_text = remove_markdown_links(stripped)
        label_matches = list(re.finditer(r"\[([^\[\]]+)\]", label_text))
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


def extract_source_appendix_labels(text, allowed_source_labels):
    appendix = extract_source_appendix(text)
    return set(extract_source_labels_in_text(appendix, allowed_source_labels))


def validate_ranked_source_appendix_coverage(text, location, allowed_source_labels):
    issues = []
    appendix_labels = extract_source_appendix_labels(text, allowed_source_labels)
    ranked_labels = set()
    for section in extract_rank_sections(text):
        ranked_labels.update(extract_source_labels_in_text(section, allowed_source_labels))
    for label in sorted(ranked_labels):
        if label not in appendix_labels:
            issues.append(
                ValidationIssue(
                    location,
                    "ranked source label missing from source appendix: {}".format(label),
                )
            )
    return issues


def extract_subsection(text, heading_text):
    pattern = r"(?im)^\s*#{{2,6}}\s*{}\s*$".format(re.escape(heading_text))
    match = re.search(pattern, text)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"(?im)^\s*#{2,6}\s+", text[start:])
    if next_heading:
        return text[start : start + next_heading.start()]
    return text[start:]


def validate_key_judgment_source_signals(text, location, allowed_source_labels):
    issues = []
    rank_sections = extract_rank_sections(text)
    if not rank_sections:
        rank_sections = [text]
    for section in rank_sections:
        for line in section.splitlines():
            stripped = line.strip()
            if re.match(r"(?i)^[-*]\s*Eligibility\s*:", stripped):
                if (
                    not has_source_label(stripped, allowed_source_labels)
                    and not has_conservative_verification_language(stripped)
                ):
                    issues.append(
                        ValidationIssue(
                            location,
                            "eligibility line lacks source label or conservative verification language",
                        )
                    )
        recent_work = extract_subsection(section, "Recent Work")
        for line in recent_work.splitlines():
            stripped = line.strip()
            if not stripped.startswith(("-", "*")):
                continue
            if (
                not has_source_label(stripped, allowed_source_labels)
                and not has_conservative_verification_language(stripped)
            ):
                issues.append(
                    ValidationIssue(
                        location,
                        "recent work item lacks source label or conservative verification language",
                    )
                )
    return issues


def extract_next_actions(text):
    actions = []
    section = extract_section_after_heading(text, "## Next Actions")
    for line in section.splitlines():
        match = re.match(r"^\s*\d+\.\s+(.+?)\s*$", line)
        if match:
            actions.append(match.group(1))
    return actions


def text_mentions_any(text, terms):
    lowered = text.lower()
    for term in terms:
        if term in lowered:
            return True
    return False


def extract_unknown_targets(text):
    targets = set()
    lowered = text.lower()
    for target in CONCRETE_UNKNOWN_TARGETS:
        if target in lowered:
            targets.add(target)
    return targets


def extract_unknown_groups(text):
    groups = set()
    lowered = text.lower()
    for group_name, terms in UNKNOWN_TARGET_GROUPS:
        for term in terms:
            if term in lowered:
                groups.add(group_name)
                break
    return groups


def extract_unknown_evidence_texts(section):
    unknowns = []
    for match in re.finditer(r"(?im)^\s*(?:[-*]\s*)?Unknowns?\s*:\s*(.+?)\s*$", section):
        unknowns.append(match.group(1).strip())
    subsection = extract_subsection(section, "Unknowns")
    if subsection:
        for line in subsection.splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                unknowns.append(stripped.lstrip("-* ").strip())
    return unknowns


def is_decorative_unknown(text):
    lowered = text.strip().lower().strip(".:; ")
    if lowered in set(["none", "n/a", "na", "tbd", "unknown", "no unknowns"]):
        return True
    if len(lowered.split()) <= 2 and not extract_unknown_groups(lowered):
        return True
    return not bool(extract_unknown_groups(lowered))


def extract_questions_text(section):
    questions = []
    questions_section = extract_subsection(section, "Questions To Ask")
    for line in questions_section.splitlines():
        stripped = line.strip()
        if stripped.startswith(("-", "*")):
            questions.append(stripped.lstrip("-* ").strip())
    return "\n".join(questions)


def validate_unknown_quality(text, location):
    issues = []
    rank_sections = extract_rank_sections(text)
    if not rank_sections:
        rank_sections = [text]
    next_actions_text = "\n".join(extract_next_actions(text))
    for section in rank_sections:
        unknowns = extract_unknown_evidence_texts(section)
        section_groups = set()
        for unknown in unknowns:
            if is_decorative_unknown(unknown):
                issues.append(
                    ValidationIssue(
                        location,
                        "unknown evidence line is decorative or non-actionable",
                    )
                )
            section_groups.update(extract_unknown_groups(unknown))
        if section_groups:
            response_text = extract_questions_text(section) + "\n" + next_actions_text
            response_groups = extract_unknown_groups(response_text)
            if not section_groups.issubset(response_groups):
                issues.append(
                    ValidationIssue(
                        location,
                        "questions or next actions do not address concrete unknown categories",
                    )
                )
    return issues


def is_generic_action(action):
    normalized = re.sub(r"[^a-z0-9 ]+", "", action.lower()).strip()
    normalized = re.sub(r"\s+", " ", normalized)
    generic_patterns = [
        r"^read\s+(?:more\s+)?papers?$",
        r"^contact\s+professors?(?:\s+about\s+fit)?$",
        r"^apply(?:\s+to\s+programs?)?$",
        r"^do\s+more\s+research(?:\s+on\s+supervisors?)?$",
        r"^research\s+more(?:\s+supervisors?)?$",
    ]
    for pattern in generic_patterns:
        if re.match(pattern, normalized):
            return True
    return False


def validate_next_actions(text, location):
    issues = []
    actions = extract_next_actions(text)
    actions_text = "\n".join(actions).lower()
    if len(actions) < 3:
        issues.append(ValidationIssue(location, "next actions require at least three numbered items"))
    if actions and any(is_generic_action(action) for action in actions):
        issues.append(ValidationIssue(location, "next actions are too generic"))
    has_paper_reading = bool(re.search(r"\bread\b.*\b(paper|publication|work|article)s?\b", actions_text))
    has_official_verification = (
        bool(re.search(r"\b(verify|check|confirm)\b", actions_text))
        and text_mentions_any(actions_text, ["official", "admission", "application", "path", "quota", "eligibility"])
    )
    has_communication_prep = (
        bool(re.search(r"\b(prepare|draft|write)\b", actions_text))
        and text_mentions_any(actions_text, ["email", "outreach", "contact", "note"])
    ) or (
        text_mentions_any(actions_text, ["contact", "email", "ask"])
        and text_mentions_any(actions_text, ["fit", "project", "preparation", "opening"])
    ) or (
        text_mentions_any(actions_text, ["ask", "speak"])
        and text_mentions_any(actions_text, ["current student", "current students", "alumni", "lab member", "lab members"])
    )
    if not has_paper_reading:
        issues.append(ValidationIssue(location, "next actions missing paper-reading step"))
    if not has_official_verification:
        issues.append(
            ValidationIssue(
                location,
                "next actions missing official admissions/path/quota verification step",
            )
        )
    if not has_communication_prep:
        issues.append(
            ValidationIssue(
                location,
                "next actions missing student-controlled communication preparation/contact step",
            )
        )
    risks = extract_section_after_heading(text, "## Risks And Unknowns").lower()
    if text_mentions_any(risks, ["advising style", "student outcomes", "lab culture"]):
        if not (
            text_mentions_any(actions_text, ["current student", "current students", "alumni", "lab member", "lab members"])
            and text_mentions_any(actions_text, ["verify", "ask", "contact", "speak"])
        ):
            issues.append(
                ValidationIssue(
                    location,
                    "advising or lab-culture risks require current-student/alumni verification action",
                )
            )
    return issues


def extract_line_containing_offset(text, offset):
    line_start = text.rfind("\n", 0, offset) + 1
    line_end = text.find("\n", offset)
    if line_end == -1:
        line_end = len(text)
    return text[line_start:line_end], offset - line_start


def extract_clause_containing_offset(line, offset):
    clause_start = 0
    for separator in [".", ";", "?", "!"]:
        found = line.rfind(separator, 0, offset)
        if found != -1:
            clause_start = max(clause_start, found + 1)
    for separator in [", but ", " but "]:
        found = line.lower().rfind(separator, 0, offset)
        if found != -1:
            clause_start = max(clause_start, found + len(separator))
    for separator in [", but ", " but "]:
        found = line.lower().find(separator, offset)
        if found != -1:
            return line[clause_start:found]
    for separator in [".", ";", "?", "!"]:
        found = line.find(separator, offset)
        if found != -1:
            return line[clause_start:found]
    return line[clause_start:]


def is_conservative_context(text, start, end):
    line, line_offset = extract_line_containing_offset(text, start)
    clause = extract_clause_containing_offset(line, line_offset).lower()
    conservative_terms = [
        "does not claim",
        "do not claim",
        "not claim",
        "does not confirm",
        "do not confirm",
        "not confirm",
        "unknown",
        "unverified",
        "must be verified",
        "should be verified",
        "verify",
        "no public evidence",
        "public evidence does not",
        "public pages do not",
    ]
    return text_mentions_any(clause, conservative_terms)


def is_safety_avoid_context(text, start):
    line, line_offset = extract_line_containing_offset(text, start)
    clause = extract_clause_containing_offset(line, line_offset).lower()
    safety_patterns = [
        r"\bavoid\s+relying\s+on\b",
        r"\bavoid\s+using\b",
        r"\bavoid\s+treating\b",
        r"\bavoid\s+ranking\b",
        r"\bavoid\s+overclaiming\b",
    ]
    for pattern in safety_patterns:
        if re.search(pattern, clause):
            return True
    return False


def validate_overclaim_language(text, location):
    issues = []
    lowered = text.lower()
    seen = set()
    for label, pattern in REPORT_OVERCLAIM_PATTERNS:
        for match in re.finditer(pattern, lowered):
            if label == "avoid" and is_safety_avoid_context(lowered, match.start()):
                continue
            if is_conservative_context(lowered, match.start(), match.end()):
                continue
            if label in seen:
                continue
            seen.add(label)
            issues.append(
                ValidationIssue(
                    location,
                    "report contains overclaim or judgmental language: {}".format(label),
                )
            )
    return issues


def is_math_to_ai_report(text):
    profile = extract_section_after_heading(text, "## Student Profile").lower()
    ranked = extract_ranked_shortlist(text).lower()
    combined = profile + "\n" + ranked
    has_math = text_mentions_any(profile, ["mathematics", "math", "statistics", "statistical"])
    has_ai = text_mentions_any(
        combined,
        [
            "cs/ai",
            "computer science",
            "artificial intelligence",
            "machine learning",
            " ai lab",
            " ai school",
            "school of artificial intelligence",
        ],
    )
    return has_math and has_ai


def extract_cross_field_readiness_text(text):
    parts = [extract_section_after_heading(text, "## Student Profile")]
    rank_sections = extract_rank_sections(text)
    if not rank_sections:
        rank_sections = [extract_ranked_shortlist(text)]
    for section in rank_sections:
        parts.append(extract_fit_scores_block(section))
        parts.append(extract_subsection(section, "Why This Fit"))
    return "\n".join(parts).lower()


def validate_cross_field_readiness(text, location):
    if not is_math_to_ai_report(text):
        return []
    readiness_text = extract_cross_field_readiness_text(text)
    coursework_alone_claims = [
        "coursework alone proves strong ai fit",
        "coursework alone proves",
        "mathematics is the foundation of ai",
        "math students can transfer to ai easily",
        "strong fit for any ai lab",
    ]
    readiness_terms = [
        "ml coursework",
        "machine learning coursework",
        "machine learning foundation",
        "deep learning coursework",
        "deep learning project",
        "deep learning preparation",
        "coding project",
        "code artifact",
        "software artifact",
        "github artifact",
        "research project",
        "ai research project",
        "cs research project",
        "machine learning project",
        "llm evaluation project",
        "first-author paper",
        "ai paper",
        "cs paper",
        "machine learning paper",
        "deep learning paper",
        "lab experience",
        "systems experience",
        "benchmark project",
        "benchmark experience",
        "evaluation experience",
        "preparation gap",
        "missing ml",
        "missing ai",
        "missing cs",
        "missing coding",
        "missing programming",
        "missing deep learning",
        "no ai",
        "no cs",
        "no ml",
        "limited ai",
        "limited cs",
        "limited ml",
        "limited coding",
        "limited programming",
    ]
    has_bad_claim = text_mentions_any(readiness_text, coursework_alone_claims)
    has_readiness = text_mentions_any(readiness_text, readiness_terms)
    if has_bad_claim or not has_readiness:
        return [
            ValidationIssue(
                location,
                "math/statistics-to-CS/AI report lacks AI/CS readiness evidence or explicit preparation gaps",
            )
        ]
    return []


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


def validate_real_demo_certainty_language(text, location):
    if not is_real_demo_report(location):
        return []
    lowered = text.lower()
    issues = []
    for phrase in REAL_REPORT_CERTAINTY_PHRASES:
        if phrase.lower() in lowered:
            issues.append(
                ValidationIssue(
                    location,
                    "real demo report contains admissions-certainty language: {}".format(phrase),
                )
            )
    if "admission is guaranteed" in lowered and "guaranteed admission" not in lowered:
        issues.append(
            ValidationIssue(
                location,
                "real demo report contains admissions-certainty language: guaranteed admission",
            )
        )
    return issues


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
    issues.extend(validate_ranked_evidence_signals(text, location, allowed_source_labels))
    issues.extend(validate_ranked_source_sufficiency(text, location, allowed_source_labels))
    issues.extend(validate_source_appendix_labels(text, location, allowed_source_labels))
    issues.extend(validate_ranked_source_appendix_coverage(text, location, allowed_source_labels))
    issues.extend(validate_key_judgment_source_signals(text, location, allowed_source_labels))
    issues.extend(validate_unknown_quality(text, location))
    issues.extend(validate_next_actions(text, location))
    issues.extend(validate_overclaim_language(text, location))
    issues.extend(validate_cross_field_readiness(text, location))
    issues.extend(validate_real_demo_language(text, location))
    issues.extend(validate_real_demo_certainty_language(text, location))
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
