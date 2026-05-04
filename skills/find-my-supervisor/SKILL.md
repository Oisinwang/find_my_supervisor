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

Currently available references:

- `references/workflow.md`
- `references/intake-protocol.md`
- `references/source-protocol.md`
- `references/risk-policy.md`
- `references/report-template.md`
- `references/rubrics/cs-ai.md`
- `references/rubrics/math-subfields.md`
- `schemas/student-search-profile.schema.json`
- `schemas/report-summary.schema.json`
