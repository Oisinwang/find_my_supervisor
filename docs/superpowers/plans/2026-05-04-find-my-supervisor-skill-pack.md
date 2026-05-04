# Find My Supervisor Skill Pack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local, portable `Find My Supervisor` skill pack that produces evidence-backed supervisor shortlist reports for CS/AI and math applicants targeting 985, CAS/UCAS, and HKU/CUHK/HKUST.

**Architecture:** The project ships as Markdown skill instructions plus structured reference files, JSON schemas, synthetic examples, and a Python standard-library validator. The top-level skill orchestrates intake, target resolution, supervisor discovery, evidence profiling, fit scoring, risk scanning, and report writing; subfield-specific rubrics live in references so they can evolve without bloating the orchestration file.

**Tech Stack:** Markdown, JSON Schema-like contracts, Python 3 standard library, `unittest`, local git.

---

## File Structure

Create this structure under `D:\find_my_supervisor`:

```text
D:\find_my_supervisor\
  AGENTS.md
  README.md
  docs\
    superpowers\
      specs\
        2026-05-04-find-my-supervisor-skills-design.md
      plans\
        2026-05-04-find-my-supervisor-skill-pack.md
  skills\
    find-my-supervisor\
      SKILL.md
      references\
        workflow.md
        intake-protocol.md
        source-protocol.md
        risk-policy.md
        report-template.md
        rubrics\
          cs-ai.md
          math-subfields.md
      schemas\
        student-search-profile.schema.json
        target-institution.schema.json
        candidate-supervisor.schema.json
        supervisor-evidence-profile.schema.json
        supervisor-fit-assessment.schema.json
        report-summary.schema.json
      examples\
        profiles\
          cs_ai_direct_phd_llm_eval.json
          math_computational_research_master.json
          math_statistics_master_quant.json
        reports\
          synthetic_cs_ai_shortlist.md
          synthetic_math_shortlist.md
  tools\
    __init__.py
    skill_pack_validator.py
  tests\
    test_project_baseline.py
    test_skill_pack_validator.py
    test_skill_contracts.py
```

Responsibilities:

- `skills/find-my-supervisor/SKILL.md`: top-level productized agent skill.
- `references/*.md`: workflow, evidence rules, output rules, and rubrics.
- `schemas/*.json`: machine-readable shape of the skill inputs and outputs.
- `examples/*`: synthetic fixtures used for validation and demos.
- `tools/skill_pack_validator.py`: no-network local validator for files, schemas, examples, and reports.
- `tests/*`: regression checks for project structure and skill contracts.

## Task 0: Initialize Repository And Baseline Policy

**Files:**
- Create: `D:\find_my_supervisor\AGENTS.md`
- Create: `D:\find_my_supervisor\README.md`
- Create: `D:\find_my_supervisor\tests\test_project_baseline.py`

- [ ] **Step 1: Initialize local git repository**

Run:

```powershell
git init
```

Expected:

```text
Initialized empty Git repository in D:/find_my_supervisor/.git/
```

- [ ] **Step 2: Write the failing baseline test**

Create `D:\find_my_supervisor\tests\test_project_baseline.py` with exactly:

```python
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_agents_policy_exists_and_preserves_delete_rule():
    agents = ROOT / "AGENTS.md"
    assert agents.exists()
    text = agents.read_text(encoding="utf-8")
    assert "D:\\rubbish" in text
    assert "requested deletion" in text


def test_readme_defines_skills_route_scope():
    readme = ROOT / "README.md"
    assert readme.exists()
    text = readme.read_text(encoding="utf-8")
    assert "skills route" in text.lower()
    assert "CS/AI" in text
    assert "mathematics" in text.lower()
    assert "985" in text
    assert "CAS/UCAS" in text
    assert "HKU" in text and "CUHK" in text and "HKUST" in text
```

- [ ] **Step 3: Run test to verify it fails**

Run:

```powershell
python -m unittest tests.test_project_baseline -v
```

Expected: FAIL because `AGENTS.md` and `README.md` do not exist.

- [ ] **Step 4: Create `AGENTS.md`**

Create `D:\find_my_supervisor\AGENTS.md` with exactly:

```markdown
# AGENTS.md

## Workspace Rules

- When the user requests deletion of any file, move that file to `D:\rubbish` instead of permanently deleting it. The user will manually delete files from there.
- Keep this project focused on the skills route for Find My Supervisor. Do not switch to a website route unless the user explicitly changes the product direction.
- Prefer source-backed research, structured reports, and reproducible skill workflows over unverified community claims.
```

- [ ] **Step 5: Create `README.md`**

Create `D:\find_my_supervisor\README.md` with exactly:

```markdown
# Find My Supervisor

Find My Supervisor is an early-stage skills route project for helping graduate applicants screen and compare potential research supervisors.

The first vertical focuses on:

- CS/AI and mathematics
- Mainland China 985 universities
- CAS/UCAS institutes and labs
- Hong Kong research universities: HKU, CUHK, and HKUST
- Recommendation-based master's admission, direct PhD, and research master's paths

The project is not a website, public rating platform, or cold-email automation tool in v1. It is a productized agent skill pack that generates evidence-backed supervisor due diligence reports from public sources.

## MVP Output

Given a student's target field, subfield, application path, target institutions, research interests, and background, the skill pack produces a ranked shortlist report with:

- supervisor basics
- recent publications or representative work
- research fit explanation
- path and career fit
- source-backed evidence
- risks and unknowns
- next-step questions for supervisors and current students
```

- [ ] **Step 6: Run baseline test to verify it passes**

Run:

```powershell
python -m unittest tests.test_project_baseline -v
```

Expected: PASS.

- [ ] **Step 7: Commit baseline**

Run:

```powershell
git add AGENTS.md README.md tests/test_project_baseline.py docs/superpowers/specs/2026-05-04-find-my-supervisor-skills-design.md docs/superpowers/plans/2026-05-04-find-my-supervisor-skill-pack.md
git commit -m "chore: initialize supervisor skill pack project"
```

Expected: commit succeeds.

## Task 1: Add Validator Harness

**Files:**
- Create: `D:\find_my_supervisor\tools\__init__.py`
- Create: `D:\find_my_supervisor\tools\skill_pack_validator.py`
- Create: `D:\find_my_supervisor\tests\test_skill_pack_validator.py`

- [ ] **Step 1: Write failing validator tests**

Create `D:\find_my_supervisor\tests\test_skill_pack_validator.py` with exactly:

```python
import json
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
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```powershell
python -m unittest tests.test_skill_pack_validator -v
```

Expected: FAIL because `tools.skill_pack_validator` does not exist.

- [ ] **Step 3: Create package marker**

Create `D:\find_my_supervisor\tools\__init__.py` with exactly:

```python
"""Project validation helpers for the Find My Supervisor skill pack."""
```

- [ ] **Step 4: Implement validator helpers**

Create `D:\find_my_supervisor\tools\skill_pack_validator.py` with exactly:

```python
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def require_keys(data: dict, required_keys: Iterable[str], location: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for key in required_keys:
        if key not in data:
            issues.append(ValidationIssue(location, f"missing required key: {key}"))
    return issues


def validate_markdown_sections(text: str, required_sections: Iterable[str], location: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for section in required_sections:
        if section not in text:
            issues.append(ValidationIssue(location, f"missing section: {section}"))
    return issues


def validate_json_file(path: Path) -> list[ValidationIssue]:
    try:
        load_json(path)
    except json.JSONDecodeError as exc:
        return [ValidationIssue(str(path), f"invalid JSON: {exc.msg}")]
    return []
```

- [ ] **Step 5: Run validator unit tests**

Run:

```powershell
python -m unittest tests.test_skill_pack_validator -v
```

Expected: PASS.

- [ ] **Step 6: Commit validator harness**

Run:

```powershell
git add tools/__init__.py tools/skill_pack_validator.py tests/test_skill_pack_validator.py
git commit -m "test: add skill pack validator harness"
```

Expected: commit succeeds.

## Task 2: Add Schemas And Profile Examples

**Files:**
- Modify: `D:\find_my_supervisor\tools\skill_pack_validator.py`
- Create: `D:\find_my_supervisor\tests\test_skill_contracts.py`
- Create: `D:\find_my_supervisor\skills\find-my-supervisor\schemas\student-search-profile.schema.json`
- Create: `D:\find_my_supervisor\skills\find-my-supervisor\schemas\target-institution.schema.json`
- Create: `D:\find_my_supervisor\skills\find-my-supervisor\schemas\candidate-supervisor.schema.json`
- Create: `D:\find_my_supervisor\skills\find-my-supervisor\schemas\supervisor-evidence-profile.schema.json`
- Create: `D:\find_my_supervisor\skills\find-my-supervisor\schemas\supervisor-fit-assessment.schema.json`
- Create: `D:\find_my_supervisor\skills\find-my-supervisor\schemas\report-summary.schema.json`
- Create: `D:\find_my_supervisor\skills\find-my-supervisor\examples\profiles\cs_ai_direct_phd_llm_eval.json`
- Create: `D:\find_my_supervisor\skills\find-my-supervisor\examples\profiles\math_computational_research_master.json`
- Create: `D:\find_my_supervisor\skills\find-my-supervisor\examples\profiles\math_statistics_master_quant.json`

- [ ] **Step 1: Extend failing contract tests**

Create `D:\find_my_supervisor\tests\test_skill_contracts.py` with exactly:

```python
import unittest
from pathlib import Path

from tools.skill_pack_validator import run_all


ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def test_skill_pack_files_validate(self):
        self.assertEqual(run_all(ROOT), [])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run contract test to verify it fails**

Run:

```powershell
python -m unittest tests.test_skill_contracts -v
```

Expected: FAIL because `run_all` is not implemented and contract files are missing.

- [ ] **Step 3: Extend validator with project-level checks**

Replace `D:\find_my_supervisor\tools\skill_pack_validator.py` with exactly:

```python
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


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
    "## Risks And Unknowns",
    "## Source Appendix",
    "## Next Actions",
]


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def require_keys(data: dict, required_keys: Iterable[str], location: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for key in required_keys:
        if key not in data:
            issues.append(ValidationIssue(location, f"missing required key: {key}"))
    return issues


def validate_markdown_sections(text: str, required_sections: Iterable[str], location: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for section in required_sections:
        if section not in text:
            issues.append(ValidationIssue(location, f"missing section: {section}"))
    return issues


def validate_json_file(path: Path) -> list[ValidationIssue]:
    try:
        load_json(path)
    except json.JSONDecodeError as exc:
        return [ValidationIssue(str(path), f"invalid JSON: {exc.msg}")]
    return []


def validate_schema_files(root: Path) -> list[ValidationIssue]:
    schema_dir = root / "skills" / "find-my-supervisor" / "schemas"
    expected = [
        "student-search-profile.schema.json",
        "target-institution.schema.json",
        "candidate-supervisor.schema.json",
        "supervisor-evidence-profile.schema.json",
        "supervisor-fit-assessment.schema.json",
        "report-summary.schema.json",
    ]
    issues: list[ValidationIssue] = []
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


def validate_profile_examples(root: Path) -> list[ValidationIssue]:
    profile_dir = root / "skills" / "find-my-supervisor" / "examples" / "profiles"
    expected = [
        "cs_ai_direct_phd_llm_eval.json",
        "math_computational_research_master.json",
        "math_statistics_master_quant.json",
    ]
    issues: list[ValidationIssue] = []
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


def validate_skill_file(root: Path) -> list[ValidationIssue]:
    skill_path = root / "skills" / "find-my-supervisor" / "SKILL.md"
    if not skill_path.exists():
        return [ValidationIssue(str(skill_path), "missing skill file")]
    text = skill_path.read_text(encoding="utf-8")
    issues = validate_markdown_sections(text, SKILL_REQUIRED_SECTIONS, str(skill_path))
    for phrase in ["985", "CAS/UCAS", "HKU", "CUHK", "HKUST", "CS/AI", "mathematics"]:
        if phrase not in text:
            issues.append(ValidationIssue(str(skill_path), f"missing scope phrase: {phrase}"))
    return issues


def validate_reports(root: Path) -> list[ValidationIssue]:
    report_dir = root / "skills" / "find-my-supervisor" / "examples" / "reports"
    expected = ["synthetic_cs_ai_shortlist.md", "synthetic_math_shortlist.md"]
    issues: list[ValidationIssue] = []
    for filename in expected:
        path = report_dir / filename
        if not path.exists():
            issues.append(ValidationIssue(str(path), "missing report example"))
            continue
        text = path.read_text(encoding="utf-8")
        issues.extend(validate_markdown_sections(text, REPORT_REQUIRED_SECTIONS, str(path)))
    return issues


def run_all(root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(validate_schema_files(root))
    issues.extend(validate_profile_examples(root))
    issues.extend(validate_skill_file(root))
    issues.extend(validate_reports(root))
    return issues


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    issues = run_all(root)
    if issues:
        for issue in issues:
            print(f"{issue.location}: {issue.message}")
        return 1
    print("Skill pack validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Create schema files**

Create `D:\find_my_supervisor\skills\find-my-supervisor\schemas\student-search-profile.schema.json` with exactly:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "StudentSearchProfile",
  "type": "object",
  "required": ["field", "subfield", "application_path", "target_scope", "research_interests", "career_orientation", "background_summary"],
  "properties": {
    "field": {"type": "string", "enum": ["cs_ai", "math"]},
    "subfield": {"type": "string"},
    "application_path": {"type": "string", "enum": ["master_recommendation", "direct_phd", "research_master", "unsure"]},
    "target_scope": {"type": "array", "items": {"type": "string"}},
    "research_interests": {"type": "array", "items": {"type": "string"}},
    "career_orientation": {"type": "string", "enum": ["academic", "industry_research", "industry_engineering", "quant_finance", "teaching", "unsure"]},
    "background_summary": {"type": "string"},
    "preferences": {"type": "object"}
  }
}
```

Create `D:\find_my_supervisor\skills\find-my-supervisor\schemas\target-institution.schema.json` with exactly:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "TargetInstitution",
  "type": "object",
  "required": ["canonical_name", "aliases", "region", "institution_type"],
  "properties": {
    "canonical_name": {"type": "string"},
    "aliases": {"type": "array", "items": {"type": "string"}},
    "region": {"type": "string"},
    "institution_type": {"type": "string", "enum": ["mainland_985", "cas_ucas", "hong_kong_research_university", "other_user_requested"]},
    "departments_or_institutes": {"type": "array", "items": {"type": "string"}}
  }
}
```

Create `D:\find_my_supervisor\skills\find-my-supervisor\schemas\candidate-supervisor.schema.json` with exactly:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "CandidateSupervisor",
  "type": "object",
  "required": ["name", "institution", "unit", "source_urls", "research_tags"],
  "properties": {
    "name": {"type": "string"},
    "institution": {"type": "string"},
    "unit": {"type": "string"},
    "title": {"type": "string"},
    "supervisor_eligibility": {"type": "string"},
    "contact": {"type": "string"},
    "source_urls": {"type": "array", "items": {"type": "string"}},
    "research_tags": {"type": "array", "items": {"type": "string"}}
  }
}
```

Create `D:\find_my_supervisor\skills\find-my-supervisor\schemas\supervisor-evidence-profile.schema.json` with exactly:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "SupervisorEvidenceProfile",
  "type": "object",
  "required": ["candidate", "recent_work", "research_summary", "evidence", "unknowns"],
  "properties": {
    "candidate": {"$ref": "candidate-supervisor.schema.json"},
    "recent_work": {"type": "array", "items": {"type": "object"}},
    "research_summary": {"type": "string"},
    "evidence": {"type": "array", "items": {"type": "object"}},
    "unknowns": {"type": "array", "items": {"type": "string"}}
  }
}
```

Create `D:\find_my_supervisor\skills\find-my-supervisor\schemas\supervisor-fit-assessment.schema.json` with exactly:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "SupervisorFitAssessment",
  "type": "object",
  "required": ["name", "overall_recommendation", "scores", "rationale", "risks", "next_questions"],
  "properties": {
    "name": {"type": "string"},
    "overall_recommendation": {"type": "string", "enum": ["strong_recommend", "recommend", "maybe", "exclude"]},
    "scores": {"type": "object"},
    "rationale": {"type": "string"},
    "risks": {"type": "array", "items": {"type": "string"}},
    "next_questions": {"type": "array", "items": {"type": "string"}}
  }
}
```

Create `D:\find_my_supervisor\skills\find-my-supervisor\schemas\report-summary.schema.json` with exactly:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ReportSummary",
  "type": "object",
  "required": ["student_profile", "ranked_shortlist", "maybe_list", "excluded_list", "source_count", "generated_at"],
  "properties": {
    "student_profile": {"$ref": "student-search-profile.schema.json"},
    "ranked_shortlist": {"type": "array", "items": {"$ref": "supervisor-fit-assessment.schema.json"}},
    "maybe_list": {"type": "array", "items": {"$ref": "supervisor-fit-assessment.schema.json"}},
    "excluded_list": {"type": "array", "items": {"$ref": "supervisor-fit-assessment.schema.json"}},
    "source_count": {"type": "integer"},
    "generated_at": {"type": "string"}
  }
}
```

- [ ] **Step 5: Create profile examples**

Create `D:\find_my_supervisor\skills\find-my-supervisor\examples\profiles\cs_ai_direct_phd_llm_eval.json` with exactly:

```json
{
  "field": "cs_ai",
  "subfield": "nlp_llm_evaluation",
  "application_path": "direct_phd",
  "target_scope": ["985 universities", "HKUST"],
  "research_interests": ["LLM evaluation", "trustworthy AI", "reasoning benchmarks"],
  "career_orientation": "industry_research",
  "background_summary": "985 computer science student, rank top 10%, one NLP research project, strong Python and machine learning foundation.",
  "preferences": {
    "advisor_style": "active lab with visible student publication record",
    "risk_tolerance": "medium"
  }
}
```

Create `D:\find_my_supervisor\skills\find-my-supervisor\examples\profiles\math_computational_research_master.json` with exactly:

```json
{
  "field": "math",
  "subfield": "computational_mathematics",
  "application_path": "research_master",
  "target_scope": ["Zhejiang University", "Fudan University", "CAS/UCAS institutes"],
  "research_interests": ["numerical analysis", "scientific computing", "inverse problems"],
  "career_orientation": "academic",
  "background_summary": "985 mathematics student, rank top 15%, completed numerical analysis and PDE coursework, comfortable with MATLAB and Python.",
  "preferences": {
    "advisor_style": "method-focused group with active seminars",
    "risk_tolerance": "low"
  }
}
```

Create `D:\find_my_supervisor\skills\find-my-supervisor\examples\profiles\math_statistics_master_quant.json` with exactly:

```json
{
  "field": "math",
  "subfield": "statistics",
  "application_path": "master_recommendation",
  "target_scope": ["Shanghai 985 universities", "HKU", "CUHK"],
  "research_interests": ["high-dimensional statistics", "causal inference", "statistical machine learning"],
  "career_orientation": "quant_finance",
  "background_summary": "985 mathematics major, rank top 20%, one statistics course project, strong probability background, good Python and R skills.",
  "preferences": {
    "advisor_style": "balanced theory and application",
    "risk_tolerance": "medium"
  }
}
```

- [ ] **Step 6: Run contract test to observe remaining failures**

Run:

```powershell
python -m unittest tests.test_skill_contracts -v
```

Expected: FAIL because `SKILL.md` and report examples are still missing.

- [ ] **Step 7: Run validator unit tests to verify no regression**

Run:

```powershell
python -m unittest tests.test_skill_pack_validator -v
```

Expected: PASS.

- [ ] **Step 8: Commit schemas and examples**

Run:

```powershell
git add tools/skill_pack_validator.py tests/test_skill_contracts.py skills/find-my-supervisor/schemas skills/find-my-supervisor/examples/profiles
git commit -m "feat: add supervisor skill data contracts"
```

Expected: commit succeeds.

## Task 3: Add Top-Level Skill And Workflow References

**Files:**
- Create: `D:\find_my_supervisor\skills\find-my-supervisor\SKILL.md`
- Create: `D:\find_my_supervisor\skills\find-my-supervisor\references\workflow.md`
- Create: `D:\find_my_supervisor\skills\find-my-supervisor\references\intake-protocol.md`

- [ ] **Step 1: Create top-level skill file**

Create `D:\find_my_supervisor\skills\find-my-supervisor\SKILL.md` with exactly:

```markdown
---
name: find-my-supervisor
description: Use when a student wants evidence-backed supervisor screening or recommendation for CS/AI or mathematics graduate applications targeting Mainland China 985 universities, CAS/UCAS institutes, HKU, CUHK, or HKUST.
---

# Find My Supervisor

## When To Use

Use this skill when the user wants to find, compare, shortlist, or investigate potential research supervisors for recommendation-based master's admission, direct PhD, or research master's paths.

The first supported scope is:

- CS/AI
- mathematics
- Mainland China 985 universities
- CAS/UCAS institutes and labs
- Hong Kong research universities: HKU, CUHK, and HKUST

Do not use this skill to create a website, scrape private data, mass-email supervisors, or publish anonymous reputation claims.

## Required Inputs

Collect or infer the following before ranking supervisors:

- field: `cs_ai` or `math`
- subfield: controlled phrase plus any user-specific wording
- application path: `master_recommendation`, `direct_phd`, `research_master`, or `unsure`
- target scope: schools, institutes, cities, or regions
- research interests: 2-8 concrete phrases
- career orientation: academic, industry research, industry engineering, quant finance, teaching, or unsure
- background summary: school tier, major, rank/GPA, research experience, papers, competitions, tools, and relevant coursework

If required inputs are missing, ask concise questions before searching.

## Workflow

Follow `references/workflow.md` exactly:

1. Intake and normalize the student profile.
2. Resolve target institutions and units.
3. Discover candidate supervisors from official and bibliographic sources.
4. Build evidence profiles for each candidate.
5. Score fit with CS/AI or math subfield rubrics.
6. Run optional reputation and risk scan with credibility labels.
7. Write a shortlist report with sources, risks, unknowns, and next actions.

## Evidence Rules

Use public sources only. Prefer official university, department, lab, admissions, supervisor list, homepage, and bibliographic sources. Treat community reviews, forum posts, and social media as optional low-confidence signals unless corroborated.

Never present anonymous or weakly sourced claims as fact. Separate facts, inferences, and unknowns.

## Output

Produce a Markdown report using `references/report-template.md`. Include:

- student profile summary
- ranked shortlist of 5-12 supervisors when enough candidates exist
- maybe list
- excluded list with concise reasons when enough candidates exist
- evidence table with source URLs
- fit scores and explanations
- risks and unknowns
- questions to ask supervisors
- questions to ask current students or alumni
- next action plan

## References

- `references/workflow.md`
- `references/intake-protocol.md`
- `references/source-protocol.md`
- `references/risk-policy.md`
- `references/report-template.md`
- `references/rubrics/cs-ai.md`
- `references/rubrics/math-subfields.md`
- `schemas/student-search-profile.schema.json`
- `schemas/report-summary.schema.json`
```

- [ ] **Step 2: Create workflow reference**

Create `D:\find_my_supervisor\skills\find-my-supervisor\references\workflow.md` with exactly:

```markdown
# Find My Supervisor Workflow

## Operating Principle

The skill recommends supervisors only when it can explain the recommendation with public evidence. A report should be useful even when the answer is "the public evidence is insufficient".

## Step 1: Intake

Normalize the user request into a `StudentSearchProfile`.

Minimum usable profile:

- field
- subfield
- application path
- target scope
- research interests
- career orientation
- background summary

When the user is unsure, make a conservative assumption and label it.

## Step 2: Target Resolution

Convert target scope into institution and unit queries.

Examples:

- "985 in Shanghai" maps to Shanghai Jiao Tong University, Fudan University, Tongji University, and East China Normal University only if the user accepts broader local coverage.
- "CAS/UCAS computational math" maps to relevant CAS institutes, UCAS schools, and labs rather than treating UCAS as one normal university.
- "港三" maps to HKU, CUHK, and HKUST.

## Step 3: Supervisor Discovery

Search official supervisor lists, department pages, lab pages, graduate admissions pages, and bibliographic sources.

Capture excluded candidates when a profile is close but fails a material constraint such as application path, subfield, or source evidence.

## Step 4: Evidence Profiling

For each candidate, collect:

- official profile source
- lab or personal homepage
- recent papers or representative works
- research tags
- eligibility evidence
- current activity evidence
- unknowns

Recent work means the last three calendar years when public metadata allows it.

## Step 5: Fit Scoring

Use `references/rubrics/cs-ai.md` for CS/AI and `references/rubrics/math-subfields.md` for math.

Score:

- research fit
- path fit
- career fit
- evidence strength
- risk and uncertainty

Explain every score in one or two sentences.

## Step 6: Risk Scan

Use `references/risk-policy.md`. Reputation data is optional and must be credibility-labeled.

## Step 7: Report Writing

Use `references/report-template.md`.

The report must distinguish:

- fact: directly sourced statement
- inference: reasonable conclusion from sources
- unknown: important missing information
```

- [ ] **Step 3: Create intake protocol**

Create `D:\find_my_supervisor\skills\find-my-supervisor\references\intake-protocol.md` with exactly:

```markdown
# Intake Protocol

## Goal

Turn a student's vague application goal into a structured `StudentSearchProfile` without asking for unnecessary personal details.

## Required Questions

Ask only for missing required fields:

1. Which field and subfield are you targeting?
2. Which path are you applying for: recommendation-based master's, direct PhD, research master's, or unsure?
3. Which schools, institutes, cities, or regions should be searched?
4. What are your 2-8 research interest phrases?
5. What is your career orientation?
6. What background should the report consider?

## Background Guidance

Useful background fields:

- current school tier
- major
- GPA or rank
- relevant coursework
- research projects
- publications or preprints
- competitions
- programming or software skills
- English ability when targeting Hong Kong

## Privacy Guidance

Do not request real name, student ID, phone number, private transcripts, or identity documents. If the user shares sensitive data, summarize only the relevant academic signal and do not repeat unnecessary personal identifiers in the report.

## Normalization Rules

Map user wording to controlled values:

- "保研" or "推免" -> `master_recommendation`
- "直博" -> `direct_phd`
- "港三" -> HKU, CUHK, HKUST
- "中科院" -> CAS/UCAS institutes and labs
- "就业导向" -> `industry_engineering` or `industry_research`, ask once if the distinction matters
- "量化" -> `quant_finance`
```

- [ ] **Step 4: Run contract test to observe remaining failures**

Run:

```powershell
python -m unittest tests.test_skill_contracts -v
```

Expected: FAIL because report examples are missing.

- [ ] **Step 5: Commit skill shell**

Run:

```powershell
git add skills/find-my-supervisor/SKILL.md skills/find-my-supervisor/references/workflow.md skills/find-my-supervisor/references/intake-protocol.md
git commit -m "feat: add supervisor skill workflow shell"
```

Expected: commit succeeds.

## Task 4: Add Source Protocol, Risk Policy, And Report Template

**Files:**
- Create: `D:\find_my_supervisor\skills\find-my-supervisor\references\source-protocol.md`
- Create: `D:\find_my_supervisor\skills\find-my-supervisor\references\risk-policy.md`
- Create: `D:\find_my_supervisor\skills\find-my-supervisor\references\report-template.md`

- [ ] **Step 1: Create source protocol**

Create `D:\find_my_supervisor\skills\find-my-supervisor\references\source-protocol.md` with exactly:

```markdown
# Source Protocol

## Source Priority

Use sources in this order:

1. University, department, graduate school, institute, and official lab pages.
2. Faculty homepages and personal academic pages.
3. Bibliographic records, publication indexes, preprint pages, and venue pages.
4. Seminar pages, group pages, student pages, alumni pages, project pages, and repositories.
5. Community reviews, forums, social media, and commercial summaries.

## Minimum Evidence For Recommendation

A candidate can appear in the ranked shortlist only if at least two public sources support the profile and at least one source is official or bibliographic.

If only one source exists, place the candidate in "maybe" unless the user explicitly asked for exploratory leads.

## Publication Handling

Prioritize the last three calendar years. When publication metadata is incomplete, use representative works and label the recency limitation.

Do not invent paper titles, venues, years, coauthors, or student placements.

## Identity Matching

Confirm identity by matching institution, department, homepage, research area, email domain, or publication profile. If multiple scholars share a name, label ambiguity and avoid ranking until the identity is resolved.

## Evidence Labels

Use these labels:

- official
- bibliographic
- lab_or_homepage
- project_or_repository
- student_or_alumni
- community
- inferred
- unknown
```

- [ ] **Step 2: Create risk policy**

Create `D:\find_my_supervisor\skills\find-my-supervisor\references\risk-policy.md` with exactly:

```markdown
# Risk And Reputation Policy

## Purpose

Risk scanning helps the student decide what to verify next. It is not a public accusation system.

## Allowed Risk Categories

- information_missing
- identity_ambiguous
- direction_mismatch
- path_uncertain
- recent_activity_unclear
- student_outcome_unknown
- community_signal_low_confidence
- community_signal_corroborated
- funding_or_project_unclear
- preparation_gap

## Credibility Levels

- high: official or bibliographic evidence
- medium: public lab, student, alumni, project, or repository evidence
- low: unverified community or social media claim
- unknown: important question with no available evidence

## Handling Community Information

Community information is optional. Include it only when it is relevant to a concrete application decision.

When using community information:

- quote or paraphrase narrowly
- provide the source link when available
- label credibility
- avoid naming private students
- avoid repeating defamatory claims as fact

Write "I found a low-confidence community signal that should be checked with current students" rather than "this supervisor has problem X".

## Report Language

Use careful language:

- "public evidence supports"
- "public evidence does not yet confirm"
- "this is a question to verify"
- "this appears suitable for"
- "this appears risky for"

Avoid:

- "safe supervisor"
- "bad supervisor"
- "guaranteed admission"
- "definitely accepts students"
- "community says"
```

- [ ] **Step 3: Create report template**

Create `D:\find_my_supervisor\skills\find-my-supervisor\references\report-template.md` with exactly:

```markdown
# Report Template

## Synthetic Fixture Notice

For examples only, state that names and sources are synthetic. For real reports, replace this section with a generation note that states the search date and source limitations.

## Student Profile

- Field:
- Subfield:
- Application path:
- Target scope:
- Research interests:
- Career orientation:
- Background signals:

## Ranked Shortlist

For each recommended supervisor:

### Rank N: Supervisor Name

- Institution:
- Unit:
- Eligibility:
- Research tags:
- Recommendation:
- Best fit for:
- Evidence strength:
- Risk level:

#### Recent Work

List up to five recent or representative works with source labels.

#### Why This Fit

Separate facts, inferences, and unknowns.

#### Questions To Ask

List questions for the supervisor and current students.

## Maybe List

Include candidates with promising but incomplete evidence.

## Excluded List

Include candidates excluded due to path mismatch, direction mismatch, weak evidence, or identity ambiguity.

## Risks And Unknowns

List cross-cutting risks for the shortlist.

## Source Appendix

List all sources with labels.

## Next Actions

Give a practical sequence for verification, outreach, and shortlist refinement.
```

- [ ] **Step 4: Run targeted tests**

Run:

```powershell
python -m unittest tests.test_skill_pack_validator tests.test_skill_contracts -v
```

Expected: FAIL only because rubrics and report examples are missing.

- [ ] **Step 5: Commit source and report policies**

Run:

```powershell
git add skills/find-my-supervisor/references/source-protocol.md skills/find-my-supervisor/references/risk-policy.md skills/find-my-supervisor/references/report-template.md
git commit -m "feat: add evidence and report policies"
```

Expected: commit succeeds.

## Task 5: Add Field And Subfield Rubrics

**Files:**
- Create: `D:\find_my_supervisor\skills\find-my-supervisor\references\rubrics\cs-ai.md`
- Create: `D:\find_my_supervisor\skills\find-my-supervisor\references\rubrics\math-subfields.md`
- Modify: `D:\find_my_supervisor\tools\skill_pack_validator.py`

- [ ] **Step 1: Add rubric validation**

In `D:\find_my_supervisor\tools\skill_pack_validator.py`, add this constant below `REPORT_REQUIRED_SECTIONS`:

```python
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
```

Add this function above `run_all`:

```python
def validate_rubrics(root: Path) -> list[ValidationIssue]:
    rubric_dir = root / "skills" / "find-my-supervisor" / "references" / "rubrics"
    issues: list[ValidationIssue] = []
    for filename, sections in RUBRIC_REQUIRED_FILES.items():
        path = rubric_dir / filename
        if not path.exists():
            issues.append(ValidationIssue(str(path), "missing rubric file"))
            continue
        text = path.read_text(encoding="utf-8")
        issues.extend(validate_markdown_sections(text, sections, str(path)))
    return issues
```

Then update `run_all` to include:

```python
    issues.extend(validate_rubrics(root))
```

The final `run_all` function should be:

```python
def run_all(root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(validate_schema_files(root))
    issues.extend(validate_profile_examples(root))
    issues.extend(validate_skill_file(root))
    issues.extend(validate_reports(root))
    issues.extend(validate_rubrics(root))
    return issues
```

- [ ] **Step 2: Run contract test to verify rubric failure**

Run:

```powershell
python -m unittest tests.test_skill_contracts -v
```

Expected: FAIL because rubric files are missing.

- [ ] **Step 3: Create CS/AI rubric**

Create `D:\find_my_supervisor\skills\find-my-supervisor\references\rubrics\cs-ai.md` with exactly:

```markdown
# CS/AI Supervisor Fit Rubric

## Core Dimensions

Score each dimension from 1 to 5 and explain the score.

- Research fit: direct match between the student's interests and the supervisor's recent work.
- Recent activity: visible output in the last three calendar years.
- Student training signal: public evidence of student first-author papers, lab activity, theses, or alumni.
- Path fit: suitability for master's recommendation, direct PhD, or research master's.
- Career fit: alignment with academic, industry research, engineering, or other career goals.
- Evidence strength: quality and quantity of public sources.
- Risk and uncertainty: missing information, identity ambiguity, path mismatch, or weak recent activity.

## Subfield Notes

Machine learning and deep learning:

- Value method depth, venue fit, student authorship patterns, and benchmark or theory contribution.
- Penalize generic "AI" labels without recent concrete work.

NLP and LLM:

- Value recent NLP or LLM activity, evaluation rigor, data access realism, safety constraints, and publication continuity.
- Check whether the group is doing model research, applications, evaluation, or infrastructure.

Computer vision:

- Value top-venue output, dataset or task relevance, real-world deployment, and student first-author patterns.
- Check whether the user's interest is perception, generation, medical imaging, robotics, or multimodal work.

Systems and architecture:

- Value systems venue relevance, artifact quality, infrastructure access, and long-cycle project fit.
- Do not over-rank groups that only use systems as an application label.

Security:

- Value responsible disclosure signals, security venue fit, ethics awareness, and compliance sensitivity.
- Clarify whether the user wants systems security, AI security, cryptography-adjacent work, or privacy.

HCI:

- Value user study rigor, design/research balance, interdisciplinary collaboration, and publication venue fit.
- Check whether the user prefers empirical research, design systems, social computing, or accessibility.

## Common Misreads

- A hot topic label is not evidence of fit.
- Paper count alone is not a training signal.
- Industry collaboration helps industry-oriented users but may not help academic fit.
- A famous supervisor may be a poor fit if the student's subfield or path does not match.
- Recent work must be identity-matched; common Chinese names require extra care.
```

- [ ] **Step 4: Create math subfield rubric**

Create `D:\find_my_supervisor\skills\find-my-supervisor\references\rubrics\math-subfields.md` with exactly:

```markdown
# Mathematics Supervisor Fit Rubric

## Common Math Dimensions

Score each dimension from 1 to 5 and explain the score.

- Direction match: proximity between the student's subfield and the supervisor's actual recent work.
- Mathematical preparation fit: whether the student's coursework and project background match the expected level.
- Research continuity: whether recent publications, seminars, or projects show a coherent program.
- Advising and training signal: student theses, group activity, seminars, or alumni evidence when public.
- Path fit: suitability for recommendation-based master's, direct PhD, or research master's.
- Career fit: academic, industry research, quant finance, teaching, or engineering.
- Evidence strength: official, bibliographic, and group-level public evidence.
- Risk and uncertainty: sparse information, direction ambiguity, path uncertainty, or preparation gap.

## Pure Mathematics

Includes algebra, geometry, topology, number theory, analysis, PDE theory, and adjacent theoretical areas.

Weight more:

- depth and continuity of research program
- exact subarea alignment
- publication quality and collaborator network
- seminar participation and academic community signals
- suitability for direct PhD and long apprenticeship
- student's proof maturity and advanced coursework

Weight less:

- raw paper count
- short-term industry relevance
- applied project visibility

Risks:

- broad labels such as "geometry" or "analysis" hide large subfield gaps
- sparse public advising evidence
- direct PhD path may require stronger proof background than the student has

## Applied Mathematics

Includes mathematical modeling, interdisciplinary applied math, mathematical biology, data-driven modeling, and application-facing theory.

Weight more:

- problem domain clarity
- mathematical depth behind applications
- collaboration with science, engineering, medicine, or industry groups
- recent funded projects or active lab work
- student outcomes across academia and industry research

Risks:

- application domain is interesting but math content is shallow
- project depends on external data access
- student wants theory but the group is mostly application execution

## Computational Mathematics

Includes numerical analysis, scientific computing, computational PDEs, inverse problems, simulation, and high-performance computation.

Weight more:

- algorithmic and computational output
- numerical analysis or scientific computing publication fit
- software, benchmark, or reproducible computation evidence
- connection between numerical method and application domain
- fit with the student's programming and numerical analysis preparation

Risks:

- "AI plus scientific computing" label without mathematical substance
- heavy engineering implementation with weak research training
- project requires PDE or numerical background the student lacks

## Operations Research And Optimization

Includes operations research, mathematical optimization, combinatorial optimization, stochastic optimization, game theory, decision science, supply chain, revenue management, and ML optimization.

Weight more:

- match between theory, algorithms, and application layer
- recent work in optimization, OR, decision systems, or ML optimization
- publication venues appropriate to OR, math, CS, or business-school boundary areas
- industry relevance for quant, logistics, platform, or decision science goals
- evidence that students train in modeling, proof, and implementation

Sub-orientation handling:

- Theory-oriented OR: emphasize proof depth, optimization theory, and math maturity.
- Applied OR: emphasize modeling quality, data access, and real decision problems.
- ML optimization: emphasize modern ML connection while checking mathematical substance.

Risks:

- business-school OR and math-department OR have different expectations
- some groups are excellent for industry but less ideal for academic math goals
- some groups require strong programming, probability, or convex analysis preparation

## Statistics And Probability

Includes statistics, probability theory, statistical learning, causal inference, high-dimensional statistics, Bayesian statistics, biostatistics, econometrics-adjacent statistics, and data science theory.

Weight more:

- subfield match: theory, methodology, computation, or applied statistics
- recent papers and preprints in the target topic
- balance between statistical rigor and application area
- placement potential for academia, industry research, quant, or data science
- evidence of active collaboration and advising

Sub-orientation handling:

- Theoretical statistics and probability: emphasize mathematical depth, proof training, and journal quality.
- Methodological statistics: emphasize method novelty, reproducibility, and domain relevance.
- Applied statistics and biostatistics: emphasize data access, collaboration networks, and publication pipeline.
- Statistical ML: emphasize overlap with CS/AI while checking statistical substance.

Risks:

- "data science" label may hide weak statistical training
- user wants AI jobs but supervisor is mostly pure probability, or vice versa
- applied projects may depend on restricted datasets
```

- [ ] **Step 5: Run contract test to observe report failure only**

Run:

```powershell
python -m unittest tests.test_skill_contracts -v
```

Expected: FAIL because report examples are still missing.

- [ ] **Step 6: Commit rubrics**

Run:

```powershell
git add tools/skill_pack_validator.py skills/find-my-supervisor/references/rubrics
git commit -m "feat: add field-specific supervisor rubrics"
```

Expected: commit succeeds.

## Task 6: Add Synthetic Report Fixtures

**Files:**
- Create: `D:\find_my_supervisor\skills\find-my-supervisor\examples\reports\synthetic_cs_ai_shortlist.md`
- Create: `D:\find_my_supervisor\skills\find-my-supervisor\examples\reports\synthetic_math_shortlist.md`

- [ ] **Step 1: Create CS/AI synthetic report**

Create `D:\find_my_supervisor\skills\find-my-supervisor\examples\reports\synthetic_cs_ai_shortlist.md` with exactly:

```markdown
# Synthetic CS/AI Supervisor Shortlist

## Synthetic Fixture Notice

This is a synthetic validation fixture. Supervisor names, papers, labs, and URLs are fictional and must not be used as real application advice.

## Student Profile

- Field: CS/AI
- Subfield: NLP and LLM evaluation
- Application path: direct PhD
- Target scope: 985 universities and HKUST
- Research interests: LLM evaluation, trustworthy AI, reasoning benchmarks
- Career orientation: industry research
- Background signals: 985 CS student, top 10%, NLP project, strong Python and machine learning foundation

## Ranked Shortlist

### Rank 1: Prof. Synthetic Chen

- Institution: Example 985 University
- Unit: School of Computer Science
- Eligibility: direct PhD appears plausible; verify current admissions quota
- Research tags: LLM evaluation, trustworthy NLP, benchmark design
- Recommendation: recommend
- Best fit for: direct PhD with industry research orientation
- Evidence strength: medium
- Risk level: medium

#### Recent Work

- 2026 synthetic paper on reasoning benchmark robustness [bibliographic]
- 2025 synthetic paper on LLM evaluator calibration [bibliographic]
- 2024 synthetic lab project on trustworthy NLP [lab_or_homepage]

#### Why This Fit

Fact: synthetic sources show recent LLM evaluation work and a lab project aligned with trustworthy NLP.

Inference: the group appears more suitable for evaluation and methodology than general LLM application development.

Unknown: direct PhD quota and student first-author publication pattern need verification.

#### Questions To Ask

- Ask the supervisor whether the group has a direct PhD slot for the coming cycle.
- Ask current students how benchmark projects are scoped and credited.

## Maybe List

- Prof. Synthetic Wang: relevant trustworthy AI label but only one synthetic source confirms recent LLM evaluation work.

## Excluded List

- Prof. Synthetic Liu: strong general AI profile but recent work is mostly computer vision, not NLP or LLM evaluation.

## Risks And Unknowns

- Direct PhD quota is not confirmed.
- Student publication and alumni signals are incomplete.
- Some candidates use broad "AI" labels that require source-level verification.

## Source Appendix

- synthetic official profile URL [official]
- synthetic lab page URL [lab_or_homepage]
- synthetic publication index URL [bibliographic]

## Next Actions

1. Verify current direct PhD quota through the official admissions page.
2. Read two recent papers from each ranked supervisor.
3. Contact current students with questions about advising cadence, authorship, and project ownership.
4. Draft outreach that highlights evaluation experience and research fit.
```

- [ ] **Step 2: Create math synthetic report**

Create `D:\find_my_supervisor\skills\find-my-supervisor\examples\reports\synthetic_math_shortlist.md` with exactly:

```markdown
# Synthetic Mathematics Supervisor Shortlist

## Synthetic Fixture Notice

This is a synthetic validation fixture. Supervisor names, papers, seminars, and URLs are fictional and must not be used as real application advice.

## Student Profile

- Field: mathematics
- Subfield: computational mathematics
- Application path: research master's
- Target scope: Zhejiang University, Fudan University, CAS/UCAS institutes
- Research interests: numerical analysis, scientific computing, inverse problems
- Career orientation: academic
- Background signals: 985 math student, top 15%, numerical analysis and PDE coursework, MATLAB and Python

## Ranked Shortlist

### Rank 1: Prof. Synthetic Zhang

- Institution: Example CAS Institute
- Unit: Computational Mathematics Group
- Eligibility: research master's appears plausible; verify current supervisor list
- Research tags: inverse problems, numerical PDEs, scientific computing
- Recommendation: strong_recommend
- Best fit for: research master's leading to PhD preparation
- Evidence strength: medium
- Risk level: low

#### Recent Work

- 2026 synthetic paper on inverse problem regularization [bibliographic]
- 2025 synthetic paper on numerical PDE solvers [bibliographic]
- 2024 synthetic seminar series on scientific computing [official]

#### Why This Fit

Fact: synthetic sources show continuity across inverse problems and numerical PDEs.

Inference: the group appears well aligned with a student who has numerical analysis and PDE preparation.

Unknown: master's student funding and current project openings need verification.

#### Questions To Ask

- Ask whether master's students can join inverse-problem projects in the first year.
- Ask current students what programming stack and PDE preparation are expected.

## Maybe List

- Prof. Synthetic Huang: strong applied math profile but synthetic sources suggest the group is more biology modeling than numerical analysis.

## Excluded List

- Prof. Synthetic Lin: excellent pure analysis profile but subfield fit is weak for computational mathematics.

## Risks And Unknowns

- Public student outcome evidence is limited.
- Some groups mix applied modeling and computational mathematics; verify the mathematical depth of available projects.
- CAS/UCAS naming requires institute-level identity checks.

## Source Appendix

- synthetic official institute page [official]
- synthetic group page [lab_or_homepage]
- synthetic publication page [bibliographic]
- synthetic seminar page [official]

## Next Actions

1. Verify current master's eligibility in official supervisor lists.
2. Read one recent numerical analysis paper from each ranked supervisor.
3. Ask current students about seminar rhythm, code expectations, and thesis topic assignment.
4. Decide whether the student's preparation gap is PDE theory, numerical implementation, or both.
```

- [ ] **Step 3: Run full test suite**

Run:

```powershell
python -m unittest discover -s tests -v
```

Expected: PASS.

- [ ] **Step 4: Run validator CLI**

Run:

```powershell
python tools/skill_pack_validator.py
```

Expected:

```text
Skill pack validation passed.
```

- [ ] **Step 5: Commit report fixtures**

Run:

```powershell
git add skills/find-my-supervisor/examples/reports
git commit -m "test: add synthetic supervisor report fixtures"
```

Expected: commit succeeds.

## Task 7: Add README Usage Instructions And Final Verification

**Files:**
- Modify: `D:\find_my_supervisor\README.md`

- [ ] **Step 1: Extend README with usage instructions**

Append this content to `D:\find_my_supervisor\README.md`:

```markdown

## Skill Pack Layout

The main skill is stored at:

`skills/find-my-supervisor/SKILL.md`

Supporting files:

- `references/workflow.md`
- `references/intake-protocol.md`
- `references/source-protocol.md`
- `references/risk-policy.md`
- `references/report-template.md`
- `references/rubrics/cs-ai.md`
- `references/rubrics/math-subfields.md`
- `schemas/*.json`
- `examples/profiles/*.json`
- `examples/reports/*.md`

## Local Validation

Run:

```powershell
python -m unittest discover -s tests -v
python tools/skill_pack_validator.py
```

Both commands should pass before changing or sharing the skill pack.

## First Demo Scenarios

Use synthetic examples for structure validation. Use real public web sources only when generating a real report for a specific user.

Suggested demos:

- CS/AI direct PhD: LLM evaluation, trustworthy AI, 985 plus HKUST
- Computational mathematics research master's: numerical analysis, scientific computing, CAS/UCAS plus selected 985 universities
- Statistics recommendation-based master's: high-dimensional statistics, causal inference, quant finance, Shanghai 985 plus HKU/CUHK
```

- [ ] **Step 2: Run baseline tests**

Run:

```powershell
python -m unittest tests.test_project_baseline -v
```

Expected: PASS.

- [ ] **Step 3: Run full test suite**

Run:

```powershell
python -m unittest discover -s tests -v
```

Expected: PASS.

- [ ] **Step 4: Run validator CLI**

Run:

```powershell
python tools/skill_pack_validator.py
```

Expected:

```text
Skill pack validation passed.
```

- [ ] **Step 5: Check git status**

Run:

```powershell
git status --short
```

Expected: only `README.md` is modified.

- [ ] **Step 6: Commit README updates**

Run:

```powershell
git add README.md
git commit -m "docs: document supervisor skill pack usage"
```

Expected: commit succeeds.

## Task 8: Final Review And Optional GitHub Publishing Preparation

**Files:**
- No required file changes.

- [ ] **Step 1: Run final verification**

Run:

```powershell
python -m unittest discover -s tests -v
python tools/skill_pack_validator.py
git status --short
```

Expected:

- test suite passes
- validator prints `Skill pack validation passed.`
- git status is clean

- [ ] **Step 2: Inspect commit history**

Run:

```powershell
git log --oneline -5
```

Expected: latest commits include:

```text
docs: document supervisor skill pack usage
test: add synthetic supervisor report fixtures
feat: add field-specific supervisor rubrics
feat: add evidence and report policies
feat: add supervisor skill workflow shell
```

- [ ] **Step 3: Decide whether to create a remote**

If the user wants GitHub publishing, use GitHub CLI after confirming the repository name and visibility.

Recommended command shape after confirmation:

```powershell
gh repo create find-my-supervisor --private --source . --remote origin --push
```

Expected: GitHub CLI creates the remote repository and pushes the current branch.

If the user does not want GitHub publishing yet, leave the project as a clean local git repository.

## Self-Review Checklist

Spec coverage:

- Productized skill route: Task 3 creates top-level skill and workflow references.
- CS/AI scope: Task 5 creates CS/AI rubric.
- Math subfield-aware evaluation: Task 5 creates pure math, applied math, computational math, OR/optimization, statistics/probability rubrics.
- 985, CAS/UCAS, HKU/CUHK/HKUST scope: Tasks 0, 2, and 3 encode scope in README, examples, and skill file.
- Evidence-backed reports: Tasks 4 and 6 create source protocol, risk policy, report template, and synthetic report fixtures.
- No website route: Task 0 encodes scope in README and AGENTS.
- Community reputation as optional: Task 4 creates risk policy.
- Testable MVP: Tasks 1, 2, 5, 6, and 7 create validator and tests.

Red-flag scan:

- No task uses empty filler instructions or unresolved markers.
- Every code-writing step includes exact file content or exact code insertion.
- Every verification step includes a command and expected result.

Type consistency:

- `StudentSearchProfile` keys match profile examples and validator required keys.
- `run_all(root)` is defined before contract tests expect it.
- Report fixtures include all sections required by `REPORT_REQUIRED_SECTIONS`.
- Rubric files include all sections required by `RUBRIC_REQUIRED_FILES`.

## Execution Handoff

Plan complete. Use one of these execution modes:

1. **Subagent-Driven (recommended)** - dispatch a fresh subagent per task, review between tasks, fast iteration.
2. **Inline Execution** - execute tasks in this session using executing-plans, batch execution with checkpoints.
