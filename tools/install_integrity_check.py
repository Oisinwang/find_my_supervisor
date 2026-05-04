from __future__ import print_function

import argparse
from pathlib import Path


REQUIRED_DIRECTORIES = [
    "references",
    "references/rubrics",
    "schemas",
    "examples",
    "examples/profiles",
    "examples/reports",
]

REQUIRED_FILES = [
    "SKILL.md",
    "references/workflow.md",
    "references/intake-protocol.md",
    "references/source-protocol.md",
    "references/risk-policy.md",
    "references/report-template.md",
    "references/rubrics/cs-ai.md",
    "references/rubrics/math-subfields.md",
    "schemas/student-search-profile.schema.json",
    "schemas/target-institution.schema.json",
    "schemas/candidate-supervisor.schema.json",
    "schemas/supervisor-evidence-profile.schema.json",
    "schemas/supervisor-fit-assessment.schema.json",
    "schemas/report-summary.schema.json",
    "examples/profiles/cs_ai_direct_phd_llm_eval.json",
    "examples/profiles/math_computational_research_master.json",
    "examples/profiles/math_statistics_master_quant.json",
    "examples/reports/synthetic_cs_ai_shortlist.md",
    "examples/reports/synthetic_math_shortlist.md",
    "examples/reports/real_hkust_trustworthy_llm_demo.md",
    "examples/reports/real_mainland_math_demo.md",
]


def validate_installation(path):
    """Return install completeness issues for a find-my-supervisor skill directory."""
    root = Path(path)
    issues = []

    if not root.exists():
        return ["installation path does not exist: {}".format(root)]
    if not root.is_dir():
        return ["installation path is not a directory: {}".format(root)]

    for relative_path in REQUIRED_DIRECTORIES:
        if not (root / relative_path).is_dir():
            issues.append("missing required directory: {}".format(relative_path))

    for relative_path in REQUIRED_FILES:
        if not (root / relative_path).is_file():
            issues.append("missing required file: {}".format(relative_path))

    return issues


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate an installed find-my-supervisor skill directory."
    )
    parser.add_argument(
        "path",
        help="Path to an installed find-my-supervisor skill directory.",
    )
    args = parser.parse_args(argv)

    issues = validate_installation(args.path)
    if issues:
        for issue in issues:
            print(issue)
        return 1

    print("Installation integrity check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
