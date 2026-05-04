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
