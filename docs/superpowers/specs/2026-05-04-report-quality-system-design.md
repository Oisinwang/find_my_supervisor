# Find My Supervisor Report Quality System Design

## Purpose

This phase strengthens Find My Supervisor as a focused vertical skill pack before any release push. The goal is to make report quality both readable by humans and checkable by local tooling.

The project remains a skills/productized-agent route. It does not include a website, UI, public rating platform, cold-email automation, or general-purpose supervisor search product.

## Product Positioning

Find My Supervisor should be treated as a public-source supervisor due-diligence skill for graduate applicants in the current vertical scope:

- CS/AI and mathematics.
- Mainland China 985 universities.
- CAS/UCAS institutes and labs.
- HKU, CUHK, and HKUST.
- Recommendation-based master's admission, direct PhD, and research master's paths.

The quality system should make the skill stronger inside this vertical rather than prematurely expanding to every discipline, country, or application model.

## Quality System Layers

### 1. Human-Readable Report Rubric

Add `skills/find-my-supervisor/references/report-quality-rubric.md`.

The rubric will define what makes a report `strong`, `acceptable`, or `weak` across the dimensions that matter for this skill:

- Source sufficiency and traceability.
- Research fit.
- Application path fit.
- Career fit.
- Evidence strength.
- Risk and uncertainty handling.
- Fact / Inference / Unknown separation.
- Practical next actions.
- Cross-field transfer caution.

This document is for humans reviewing generated reports and for future eval work. It should not pretend that all quality can be reduced to a validator pass.

### 2. Failure Modes Catalog

Add `skills/find-my-supervisor/references/failure-modes.md`.

The failure catalog will name common report mistakes and show how they should be handled. Initial failure modes:

- Treating supervisor fame as fit.
- Treating a paper topic as proof of current recruiting interest.
- Turning community reputation into fact.
- Inventing quota, availability, student outcomes, or admissions certainty.
- Overstating cross-field fit, especially math-to-AI transitions.
- Hiding uncertainty instead of writing actionable unknowns.
- Ranking a candidate with only one weak source.
- Recommending broad institutional targets without identity matching.
- Producing generic next actions that do not help the applicant verify fit.

The catalog should use cautious, non-defamatory language and stay aligned with `risk-policy.md`.

### 3. Eval Benchmark Fixtures

Add `tests/fixtures/report_quality/` with small Markdown snippets or mini reports that exercise quality rules.

Initial fixtures:

- `good_minimal_report.md`: a compact report that meets the quality contract.
- `overclaim_admissions_report.md`: includes admissions-certainty language that should fail.
- `weak_cross_field_report.md`: math-to-AI style report with weak evidence and overconfident transfer claims.

These fixtures are test data, not user-facing demo reports. They can be synthetic but must be clearly marked as quality fixtures.

### 4. Validator Upgrade

Extend `tools/skill_pack_validator.py` to check more machine-verifiable quality rules while staying Python 3.6-compatible.

Planned checks:

- Every real report must include `## Maybe List` and `## Excluded List`.
- `Risk level` must exist for each ranked supervisor and use an allowed value.
- Real reports must reject admissions-certainty and reputation-judgment phrases such as:
  - `guaranteed admission`
  - `definitely accepts`
  - `safe supervisor`
  - `bad supervisor`
  - `will admit`
- Source Appendix parsing should distinguish Markdown link text from evidence labels so entries like `[Faculty profile](https://...) [official]` do not falsely fail.
- Ranked supervisors should have enough evidence signals to support ranking. The check should be conservative and avoid pretending it can fully prove source sufficiency from prose. The first version can require each ranked section to include at least two source-labeled evidence mentions in its section or clear uncertainty language that explains why the recommendation is exploratory.
- Fixture tests should prove the validator catches overclaiming, bad risk levels, missing required lists, and weak cross-field evidence language.

The validator should remain a guardrail, not the whole evaluation system. Some quality issues will stay in the human rubric.

## Cross-Field Demo Implications

The user wants a future cross-field demo: a 2023 undergraduate student in mathematics and applied mathematics, aiming for recommendation-based master's or direct PhD admission into an AI school, with Beihang University as a precise undergraduate/graduate-school context.

This phase will prepare the quality rules for that demo but will not add the demo yet. The key design implication is that cross-field reports need stricter language:

- Math-to-AI fit must separate mathematical preparation from AI research readiness.
- The report must not assume that math coursework alone proves AI lab fit.
- It should identify preparation gaps such as ML systems, deep learning projects, coding artifacts, publications, or lab experience.
- It should be explicit about whether the target path is master's, direct PhD, or both.

## Non-Goals

This phase will not:

- Add the Beihang cross-field real demo yet.
- Write formal release notes.
- Expand beyond the existing CS/AI and mathematics vertical.
- Build or revive any website route.
- Add UI work.
- Add cold-email automation.
- Modify user-global `~/.codex/skills`, `~/.claude/skills`, or other runtime directories.
- Delete or clean old untracked temporary files.

## Files To Change

Expected additions:

- `skills/find-my-supervisor/references/report-quality-rubric.md`
- `skills/find-my-supervisor/references/failure-modes.md`
- `tests/fixtures/report_quality/good_minimal_report.md`
- `tests/fixtures/report_quality/overclaim_admissions_report.md`
- `tests/fixtures/report_quality/weak_cross_field_report.md`

Expected updates:

- `tools/skill_pack_validator.py`
- `tests/test_skill_pack_validator.py`
- `skills/find-my-supervisor/references/report-template.md`
- `skills/find-my-supervisor/SKILL.md`
- `README.md`
- `README.zh-CN.md`

The README updates should be small and should point readers to the new quality references without turning this into a launch/release task.

## Verification

Required verification after implementation:

```powershell
python -m unittest discover -s tests -v
python tools\skill_pack_validator.py
python tools\install_integrity_check.py skills\find-my-supervisor
```

The existing four protected untracked legacy paths may remain untracked:

- `_tmp_agents_md_output.md`
- `_tmp_legacy_agents_md_output.md`
- `_tmp_gsd_agents_key/`
- `get-shit-done-codex/`

No implementation commit should include those paths.

## Open Decisions Resolved

- Quality-system work is prioritized over immediate release.
- The next implementation should follow path 1: human-readable quality rubric plus machine-checkable validator rules plus benchmark fixtures.
- Website and UI work are not part of the product route, not merely deferred tasks.
