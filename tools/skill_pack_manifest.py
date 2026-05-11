"""Canonical file lists for the find-my-supervisor skill pack."""

REQUIRED_DIRECTORIES = [
    "references",
    "references/rubrics",
    "schemas",
    "examples",
    "examples/profiles",
    "examples/reports",
]

REQUIRED_REFERENCE_FILES = [
    "references/workflow.md",
    "references/intake-protocol.md",
    "references/source-protocol.md",
    "references/risk-policy.md",
    "references/report-template.md",
    "references/report-quality-rubric.md",
    "references/failure-modes.md",
    "references/rubrics/cs-ai.md",
    "references/rubrics/math-subfields.md",
]

REQUIRED_SCHEMA_FILES = [
    "schemas/student-search-profile.schema.json",
    "schemas/target-institution.schema.json",
    "schemas/candidate-supervisor.schema.json",
    "schemas/supervisor-evidence-profile.schema.json",
    "schemas/supervisor-fit-assessment.schema.json",
    "schemas/report-summary.schema.json",
]

REQUIRED_PROFILE_EXAMPLES = [
    "examples/profiles/cs_ai_direct_phd_llm_eval.json",
    "examples/profiles/math_computational_research_master.json",
    "examples/profiles/math_statistics_master_quant.json",
]

REQUIRED_REPORT_EXAMPLES = [
    "examples/reports/synthetic_cs_ai_shortlist.md",
    "examples/reports/synthetic_math_shortlist.md",
    "examples/reports/real_hkust_trustworthy_llm_demo.md",
    "examples/reports/real_mainland_math_demo.md",
]

REQUIRED_FILES = (
    ["SKILL.md"]
    + REQUIRED_REFERENCE_FILES
    + REQUIRED_SCHEMA_FILES
    + REQUIRED_PROFILE_EXAMPLES
    + REQUIRED_REPORT_EXAMPLES
)
