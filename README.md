# Find My Supervisor

Evidence-backed supervisor due diligence for graduate applicants.

Find My Supervisor is the skills route version of a productized agent workflow for helping students screen and compare potential research supervisors from public sources. It starts with the high-demand China/Hong Kong graduate application scenario: CS/AI and mathematics applicants targeting Mainland China 985 universities, CAS/UCAS institutes, and HKU/CUHK/HKUST.

It is not a website, a public rating platform, or a cold-email bot. It is a reproducible research workflow that turns a student's goals into a source-backed supervisor shortlist.

## Why This Exists

Choosing a graduate supervisor is not just "find a famous professor". Students need to know:

- whether the supervisor's recent work matches their direction
- whether the path fits master's recommendation, direct PhD, or research master's
- whether the evidence is official, bibliographic, inferred, or missing
- what risks and unknowns still need to be checked with current students
- what to ask before committing to a shortlist

This skill pack is designed to make that investigation structured, cautious, and repeatable.

## Quick Start

Open the main skill:

```text
skills/find-my-supervisor/SKILL.md
```

Use it with a compatible agent runtime by giving the agent a profile like:

```yaml
field: math
subfield: computational_mathematics
application_path: research_master
target_scope:
  - Zhejiang University
  - Fudan University
  - CAS/UCAS institutes
research_interests:
  - numerical analysis
  - scientific computing
  - inverse problems
career_orientation: academic
background_summary: >
  985 mathematics student, top 15%, completed numerical analysis and PDE
  coursework, comfortable with MATLAB and Python.
```

The expected output is a Markdown shortlist report with evidence, fit scores, risks, unknowns, and next actions.

## What The Report Includes

For each recommended supervisor, the report should include:

- basic supervisor profile: institution, unit, title, eligibility, homepage/contact source
- recent work or representative publications, prioritizing the last three calendar years
- research tags and source-backed direction summary
- five fit scores: research fit, path fit, career fit, evidence strength, risk/uncertainty
- recommendation rationale separated into facts, inferences, and unknowns
- source appendix with labels such as `official`, `bibliographic`, `lab_or_homepage`, `community`, or `unknown`
- questions to ask the supervisor
- questions to ask current students or alumni
- next-step shortlist and outreach plan

## Supported Scope

First vertical:

- CS/AI
- mathematics
- Mainland China 985 universities
- CAS/UCAS institutes and labs
- Hong Kong research universities: HKU, CUHK, and HKUST
- recommendation-based master's admission, direct PhD, and research master's paths

Mathematics is subfield-aware. The rubric separates:

- pure mathematics
- applied mathematics
- computational mathematics
- operations research and optimization
- statistics and probability

## Repository Layout

```text
skills/find-my-supervisor/
  SKILL.md
  references/
    workflow.md
    intake-protocol.md
    source-protocol.md
    risk-policy.md
    report-template.md
    rubrics/
      cs-ai.md
      math-subfields.md
  schemas/
    *.schema.json
  examples/
    profiles/
      *.json
    reports/
      *.md

tools/
  skill_pack_validator.py

tests/
  test_*.py
```

## Demo Fixtures

Synthetic examples are included for structure validation only:

- `skills/find-my-supervisor/examples/profiles/cs_ai_direct_phd_llm_eval.json`
- `skills/find-my-supervisor/examples/profiles/math_computational_research_master.json`
- `skills/find-my-supervisor/examples/profiles/math_statistics_master_quant.json`
- `skills/find-my-supervisor/examples/reports/synthetic_cs_ai_shortlist.md`
- `skills/find-my-supervisor/examples/reports/synthetic_math_shortlist.md`

The synthetic reports use fictional supervisors, papers, labs, and URLs. Real reports must use real public sources and must label evidence quality.

Real public-source demo:

- `skills/find-my-supervisor/examples/reports/real_hkust_trustworthy_llm_demo.md`

## Local Validation

Run:

```powershell
python -m unittest discover -s tests -v
python tools/skill_pack_validator.py
```

Expected:

```text
Ran 6 tests
OK

Skill pack validation passed.
```

## Safety Boundaries

The skill pack should:

- use public sources only
- prefer official, department, lab, admissions, homepage, and bibliographic sources
- label community reputation as optional and low-confidence unless corroborated
- avoid anonymous claims as factual recommendations
- avoid inventing papers, venues, student outcomes, or admissions certainty
- avoid mass-email automation

It should not claim to predict admission results or guarantee supervisor response.

## License

MIT. See `LICENSE`.

## Roadmap

Near-term:

- tighten JSON schemas for source labels and the five fit-score dimensions
- validate workflow and intake protocol sections
- add real public-source demo reports for one narrow school cluster
- package the skill for multiple agent runtimes

Later:

- add more fields beyond CS/AI and mathematics
- add Hong Kong-specific English-page handling
- add optional PDF report export
- add a lightweight benchmark set for report quality review
