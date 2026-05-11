# Find My Supervisor

Evidence-backed supervisor due diligence for graduate applicants.

[中文说明](README.zh-CN.md)

Find My Supervisor is the skills route version of a productized agent workflow for helping students screen and compare potential research supervisors from public sources. It starts with the high-demand China/Hong Kong graduate application scenario: CS/AI and mathematics applicants targeting Mainland China 985 universities, CAS/UCAS institutes, and HKU/CUHK/HKUST.

It is not a website, a public rating platform, or a message-sending tool. It is a reproducible research workflow that turns a student's goals into a source-backed supervisor shortlist and student-controlled communication preparation.

## Why This Exists

Choosing a graduate supervisor is not just "find a famous professor". Students need to know:

- whether the supervisor's recent work matches their direction
- whether the path fits master's recommendation, direct PhD, or research master's
- whether the evidence is official, bibliographic, inferred, or missing
- what risks and unknowns still need to be checked with current students
- what to ask before committing to a shortlist

This skill pack is designed to make that investigation structured, cautious, and repeatable.

## Quick Start

Clone the repository:

```powershell
git clone https://github.com/Oisinwang/find_my_supervisor.git
cd find_my_supervisor
```

Open the main skill directly:

```text
skills/find-my-supervisor/SKILL.md
```

Or install the skill into a folder-based agent runtime.

Codex-style local install on Windows PowerShell:

```powershell
$target = "$HOME\.codex\skills\find-my-supervisor"
New-Item -ItemType Directory -Force $target | Out-Null
Copy-Item -Recurse -Force ".\skills\find-my-supervisor\*" $target
```

Codex-style local install on macOS/Linux:

```bash
mkdir -p ~/.codex/skills/find-my-supervisor
cp -R skills/find-my-supervisor/. ~/.codex/skills/find-my-supervisor/
```

Claude-style or other folder-based runtimes use the same idea: copy `skills/find-my-supervisor/` into the runtime's skills directory, preserving the `SKILL.md`, `references/`, `schemas/`, and `examples/` files together.

## Verify Installation

After copying the skill pack, validate that the installed directory is complete:

Windows PowerShell:

```powershell
$target = "$HOME\.codex\skills\find-my-supervisor"
python .\tools\install_integrity_check.py $target
```

macOS/Linux:

```bash
target="$HOME/.codex/skills/find-my-supervisor"
python tools/install_integrity_check.py "$target"
```

For a full temporary-directory install trial that does not write to global skill
directories, see [docs/install-test.md](docs/install-test.md).

Then ask your agent to use `find-my-supervisor` with a profile like:

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

## Invocation Template

```text
Use the find-my-supervisor skill to create an evidence-backed supervisor
shortlist report.

Profile:
- field:
- subfield:
- application_path:
- target_scope:
- research_interests:
- career_orientation:
- background_summary:

Requirements:
- use public sources only
- label facts, inferences, and unknowns
- include source links
- include the five fit scores
- do not use community reputation unless clearly labeled as low-confidence
```

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
- next-step shortlist and communication-preparation plan

## Report Quality

The skill pack includes a human review rubric and failure-mode catalog:

- [report-quality-rubric.md](skills/find-my-supervisor/references/report-quality-rubric.md)
- [failure-modes.md](skills/find-my-supervisor/references/failure-modes.md)

These references are meant to keep reports source-backed, cautious, and useful inside the current CS/AI and mathematics vertical scope.

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
  install_integrity_check.py
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

Real public-source demos:

- `skills/find-my-supervisor/examples/reports/real_hkust_trustworthy_llm_demo.md`
- `skills/find-my-supervisor/examples/reports/real_mainland_math_demo.md`

## Local Validation

Run:

```powershell
python -m unittest discover -s tests -v
python tools/skill_pack_validator.py
```

Expected:

```text
Ran ... tests
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
- avoid sending or automating messages; the skill only helps the student prepare questions and communication notes

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
