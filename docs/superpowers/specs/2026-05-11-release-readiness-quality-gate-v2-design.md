# Release Readiness And Quality Gate V2 Design

## Goal

Prepare Find My Supervisor for an open-source skills beta by making release readiness auditable and strengthening the report validator so it catches weak, overconfident, or non-actionable reports before publication.

## Scope

This work stays on the skills/productized-agent route. It does not add a website, UI, database, crawler, ranking platform, or outreach automation.

In scope:

- Release-readiness documentation for the current skills package.
- Release tree safety for protected local temporary paths.
- Validator checks for source sufficiency, appendix coverage, non-decorative unknowns, actionable next steps, overclaim language, and cross-field readiness.
- Wording fixes where release materials could sound like a cold-email or admissions-prediction product.
- Install/validator consistency checks for required packaged files.

Out of scope:

- Deleting or moving existing protected untracked temporary files.
- Publishing a GitHub release or tag in this task.
- Expanding beyond the CS/AI and mathematics vertical.
- Adding a website or UI.

## Release Readiness Design

Add a release audit document that records the current release state in three buckets:

- blockers that must be fixed before a public beta,
- acceptable beta risks that should be disclosed,
- future v0.1/v0.2 improvements.

Add a release checklist that can be run before tagging. The checklist should include test commands, validator commands, install-integrity checks, git status expectations, source-backed demo requirements, and wording boundaries.

The protected old untracked paths should be ignored in `.gitignore` to reduce accidental staging risk. The files and directories themselves must not be moved, edited, or deleted.

## Quality Gate V2 Design

The validator should continue to be Python 3.6 compatible and dependency-free.

For each ranked supervisor report section:

- Require at least two non-weak source-labeled evidence mentions.
- Require at least one `official` or `bibliographic` source signal.
- Reject source support made only from `community`, `unknown`, or `inferred` labels.
- Require key judgment fields such as eligibility and recent work to include source labels or explicit unknown/verification language.
- Require source labels used in the report to appear in the Source Appendix.

For unknowns:

- Reject decorative unknown lines such as `Unknown: none`, `N/A`, `TBD`, or generic filler.
- Require concrete verification targets such as quota, openings, funding, advising style, project availability, application path, eligibility, current students, preparation gaps, or identity ambiguity.
- Require question or next-action text to address concrete unknown categories.

For next actions:

- Require at least three numbered actions.
- Require coverage of paper-reading, official admissions/path/quota verification, and student-controlled communication preparation.
- If advising style, student outcomes, or lab culture risks appear, require current-student or alumni verification.
- Reject only-generic actions such as `Read papers`, `Contact professors`, `Apply`, or `Do more research`.

For overclaim language:

- Apply admissions-certainty and judgmental-language checks to all reports, not only real demo filenames.
- Reject claims that imply guaranteed admission, easy admission, current quota, funding, current acceptance, or defamatory labels unless the text is explicitly framed as unverified or not confirmed by public evidence.

For cross-field readiness:

- Detect math/statistics-to-CS/AI scenarios from the student profile and ranked shortlist context.
- Require AI/CS readiness evidence or explicit preparation gaps, such as ML coursework, deep learning, coding projects, research projects, papers, lab experience, systems experience, or benchmark/evaluation work.
- Reject claims that mathematics/statistics coursework alone proves a strong AI fit.

## Testing Design

Use TDD for validator behavior:

- Add focused unit tests for each new validator rule.
- Keep tests deterministic, fixture-based, and fast.
- Run the full test suite and both validators after each subtask.

The final verification commands are:

```powershell
python -m unittest discover -s tests -v
python tools\skill_pack_validator.py
python tools\install_integrity_check.py skills\find-my-supervisor
```

## Release Decision After This Work

After this work, the project should be closer to a public beta but still require a final release pass before tagging. Expected remaining release work:

- Decide whether to keep, archive, or remove tracked internal `docs/superpowers/` planning artifacts before public release.
- Add a changelog or release notes if tagging `v0.1.0-beta`.
- Optionally add the Beihang math-to-AI cross-field real demo as another proof point.
