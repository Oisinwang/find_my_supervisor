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

Use CS/AI and math subfield rubrics once those references are added.

Score:

- research fit
- path fit
- career fit
- evidence strength
- risk and uncertainty

Explain every score in one or two sentences.

## Step 6: Risk Scan

Use the risk policy once that reference is added. Reputation data is optional and must be credibility-labeled.

## Step 7: Report Writing

Use the report template once that reference is added.

The report must distinguish:

- fact: directly sourced statement
- inference: reasonable conclusion from sources
- unknown: important missing information
