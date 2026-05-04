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
