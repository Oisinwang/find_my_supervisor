# Report Quality System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a human-readable and machine-checkable quality system for Find My Supervisor reports.

**Architecture:** Add quality reference docs for human review, benchmark fixtures for report-quality regression tests, and focused Python 3.6-compatible validator checks for the parts that can be checked deterministically. Keep the project on the skills/productized-agent route only.

**Tech Stack:** Markdown references and fixtures, Python 3.6-compatible stdlib, `unittest`, existing `tools/skill_pack_validator.py`, existing install-integrity script.

---

## File Structure

- Create `skills/find-my-supervisor/references/report-quality-rubric.md`: human scoring rubric for strong/acceptable/weak reports.
- Create `skills/find-my-supervisor/references/failure-modes.md`: catalog of common report failures and correct handling.
- Create `tests/fixtures/report_quality/good_minimal_report.md`: compact valid quality fixture.
- Create `tests/fixtures/report_quality/overclaim_admissions_report.md`: fixture with admissions-certainty language.
- Create `tests/fixtures/report_quality/weak_cross_field_report.md`: fixture with cross-field overconfidence and weak evidence.
- Modify `tools/skill_pack_validator.py`: add deterministic checks for required lists, risk levels, real-report overclaim language, Markdown-aware source-label parsing, ranked evidence signals, and new reference files.
- Modify `tests/test_skill_pack_validator.py`: add unit tests for new validator rules and fixtures.
- Modify `skills/find-my-supervisor/references/report-template.md`: point report authors to rubric/failure modes and clarify risk levels.
- Modify `skills/find-my-supervisor/SKILL.md`: include quality references in the skill reference list and output expectations.
- Modify `tools/install_integrity_check.py`: require the two new reference docs in installed skill packs.
- Modify `README.md` and `README.zh-CN.md`: small quality-system links, no release framing and no website/UI route.

---

### Task 1: Add Human Quality References

**Files:**
- Create: `skills/find-my-supervisor/references/report-quality-rubric.md`
- Create: `skills/find-my-supervisor/references/failure-modes.md`
- Modify: `skills/find-my-supervisor/references/report-template.md`
- Modify: `skills/find-my-supervisor/SKILL.md`
- Modify: `tools/install_integrity_check.py`

- [ ] **Step 1: Add the report quality rubric**

Create `skills/find-my-supervisor/references/report-quality-rubric.md` with these sections:

```markdown
# Report Quality Rubric

## Purpose

Use this rubric to review Find My Supervisor reports. A validator pass means the report has required structure; it does not prove the report is strong.

## Overall Ratings

- strong: source-backed, specific, cautious, and actionable.
- acceptable: mostly source-backed and useful, with clearly labeled gaps.
- weak: generic, under-sourced, overconfident, or hard for the applicant to act on.

## Dimensions

### Source Sufficiency And Traceability

- strong: each ranked supervisor has at least two public evidence signals, with at least one official or bibliographic source.
- acceptable: source coverage is uneven, but limits are explicit and weaker candidates are placed in Maybe List.
- weak: ranks candidates from one weak source, missing links, or unlabeled sources.

### Research Fit

- strong: connects recent work, research tags, and the student's stated interests.
- acceptable: direction match is plausible but needs more paper-level verification.
- weak: relies on supervisor fame, broad department labels, or generic keywords.

### Application Path Fit

- strong: separates program-level eligibility from individual quota or availability.
- acceptable: identifies the path but leaves quota and supervisor availability as unknowns.
- weak: claims a supervisor accepts students or that admission is likely without evidence.

### Career Fit

- strong: explains why the group fits the student's academic or industry research path.
- acceptable: gives a reasonable but brief career-fit link.
- weak: ignores the student's career orientation.

### Evidence Strength

- strong: distinguishes official, bibliographic, lab/homepage, inferred, unknown, and community evidence.
- acceptable: uses labels correctly but has limited source diversity.
- weak: mixes fact and inference or treats community claims as hard evidence.

### Risk And Uncertainty

- strong: names concrete risks and turns them into questions to verify.
- acceptable: names the main unknowns without much prioritization.
- weak: hides uncertainty or uses judgmental labels such as safe supervisor or bad supervisor.

### Fact / Inference / Unknown Separation

- strong: every ranked supervisor separates what public sources show, what the report infers, and what remains unknown.
- acceptable: separation exists but is brief.
- weak: blends claims together so the reader cannot audit them.

### Next Actions

- strong: gives paper-reading, admissions-checking, and communication-preparation steps specific to the shortlist.
- acceptable: gives useful but somewhat generic steps.
- weak: gives vague advice such as contact professors or read papers without priorities.

## Cross-Field Transfer Checks

For math-to-AI, statistics-to-CS, or similar transitions, a strong report must separate mathematical preparation from AI research readiness. It should name preparation gaps such as machine learning coursework, deep learning projects, coding artifacts, papers, lab experience, or systems experience.
```

- [ ] **Step 2: Add the failure modes catalog**

Create `skills/find-my-supervisor/references/failure-modes.md` with these sections:

```markdown
# Report Failure Modes

## Purpose

This catalog lists common ways a supervisor shortlist report can become misleading. Use it before trusting or publishing a report.

## Fame As Fit

Failure: ranking a supervisor because they are famous, senior, or in a prestigious lab.

Correct handling: explain the topic-level fit using public research evidence, or place the candidate in Maybe List.

## Paper Topic Equals Recruiting Interest

Failure: treating one recent paper as proof that the supervisor is recruiting in that topic.

Correct handling: write that the paper supports research activity, while quota, project availability, and recruiting interest remain unknown.

## Community Claim As Fact

Failure: repeating forum, social media, or anonymous claims as factual risk.

Correct handling: either omit the claim or label it as low-confidence community information that should be checked with current students.

## Invented Availability

Failure: claiming a supervisor has quota, accepts students, funds students, or will admit the applicant without public evidence.

Correct handling: use phrases such as public evidence does not confirm current quota.

## Overconfident Cross-Field Fit

Failure: saying a mathematics applicant is a strong AI fit only because they have math coursework.

Correct handling: identify AI-readiness evidence and preparation gaps separately.

## Hidden Unknowns

Failure: making a recommendation without stating the missing information.

Correct handling: write Unknown lines and turn them into Next Actions.

## Weak Source Ranking

Failure: ranking a candidate from one source or from a source that does not identify the supervisor clearly.

Correct handling: keep the candidate in Maybe List unless the user explicitly asked for exploratory leads.

## Generic Next Actions

Failure: ending with generic advice that does not help the applicant verify the specific shortlist.

Correct handling: prioritize official admissions checks, recent papers, targeted questions, and current-student verification.

## Defamatory Or Judgmental Language

Failure: using labels such as bad supervisor, safe supervisor, toxic, or guaranteed admission.

Correct handling: describe public evidence, uncertainty, and verification questions without making public accusations.
```

- [ ] **Step 3: Update report template quality references**

Modify `skills/find-my-supervisor/references/report-template.md`:

Add after `## Ranked Shortlist`:

```markdown
Use `report-quality-rubric.md` and `failure-modes.md` before finalizing a report. A ranked candidate should have enough source evidence to support the recommendation, and uncertainty should be explicit rather than hidden.
```

Add under the `- Risk level:` line:

```markdown
  Allowed values: low, medium, medium_high, high, unknown.
```

- [ ] **Step 4: Update SKILL.md references**

Open `skills/find-my-supervisor/SKILL.md` and add the new reference files under its References section. If the file has an Output or Evidence Rules section, add one concise sentence:

```markdown
Before finalizing a report, check it against `references/report-quality-rubric.md` and avoid the patterns in `references/failure-modes.md`.
```

- [ ] **Step 5: Update install integrity required files**

In `tools/install_integrity_check.py`, add these strings to `REQUIRED_FILES` near the other reference files:

```python
    "references/report-quality-rubric.md",
    "references/failure-modes.md",
```

- [ ] **Step 6: Verify Task 1**

Run:

```powershell
python tools\install_integrity_check.py skills\find-my-supervisor
python tools\skill_pack_validator.py
```

Expected:

```text
Installation integrity check passed.
Skill pack validation passed.
```

- [ ] **Step 7: Commit Task 1**

```powershell
git add -- skills\find-my-supervisor\references\report-quality-rubric.md skills\find-my-supervisor\references\failure-modes.md skills\find-my-supervisor\references\report-template.md skills\find-my-supervisor\SKILL.md tools\install_integrity_check.py
git commit -m "Add report quality references"
```

---

### Task 2: Add Report Quality Fixtures

**Files:**
- Create: `tests/fixtures/report_quality/good_minimal_report.md`
- Create: `tests/fixtures/report_quality/overclaim_admissions_report.md`
- Create: `tests/fixtures/report_quality/weak_cross_field_report.md`

- [ ] **Step 1: Create fixture directory**

Create `tests/fixtures/report_quality/`.

- [ ] **Step 2: Add good minimal fixture**

Create `tests/fixtures/report_quality/good_minimal_report.md`:

```markdown
# Quality Fixture: Good Minimal Report

## Generation Note

This is a quality fixture for validator tests. It is not application advice.

## Student Profile

- Field: mathematics
- Subfield: computational mathematics
- Application path: direct PhD
- Target scope: one school cluster
- Research interests: inverse problems, scientific computing
- Career orientation: academic
- Background signals: math major with PDE and numerical analysis preparation

## Ranked Shortlist

### Rank 1: Example Supervisor

- Institution: Example University
- Unit: School of Mathematical Sciences
- Eligibility: doctoral-supervisor status appears on official pages; current quota is unknown
- Research tags: inverse problems, numerical PDEs
- Recommendation: recommend
- Best fit for: applicant with PDE and numerical-computing preparation
- Evidence strength: high
- Risk level: medium

#### Fit Scores

- Research fit: 4/5 because official and bibliographic evidence align with inverse problems.
- Path fit: 3/5 because program-level path exists but individual quota is unknown.
- Career fit: 4/5 because the topic supports academic applied mathematics.
- Evidence strength: 4/5 because the section uses official and bibliographic evidence.
- Risk and uncertainty: 3/5 because quota, advising style, and current project openings remain unknown.

#### Recent Work

- 2025 representative inverse-problem paper [bibliographic]
- Official faculty profile [official]

#### Why This Fit

Fact: public official and bibliographic sources support the inverse-problem research direction.

Inference: the supervisor appears relevant for a student focused on numerical inverse problems.

Unknown: current quota, project availability, and advising fit require direct verification.

#### Questions To Ask

- Are there current projects for incoming direct PhD students in inverse problems?
- What preparation should the applicant strengthen before applying?

## Maybe List

- Example Maybe Candidate: relevant keyword overlap but only one public source.

## Excluded List

- Example Excluded Candidate: strong applied math profile but no source-backed inverse-problem evidence.

## Risks And Unknowns

- Public sources do not confirm current quota.
- Recent publications do not establish advising style.

## Source Appendix

- https://example.edu/faculty [official]
- https://example.org/paper [bibliographic]

## Next Actions

1. Read the recent paper and write a short fit note.
2. Verify official admissions path and timing.
3. Ask the supervisor about current openings and project fit.
```

- [ ] **Step 3: Add admissions overclaim fixture**

Create `tests/fixtures/report_quality/overclaim_admissions_report.md` by copying the good fixture and replacing the Rank 1 `Eligibility` and `Unknown` lines with:

```markdown
- Eligibility: this supervisor definitely accepts direct PhD students and will admit strong applicants.
```

```markdown
Unknown: none; admission is guaranteed if the applicant has good grades.
```

- [ ] **Step 4: Add weak cross-field fixture**

Create `tests/fixtures/report_quality/weak_cross_field_report.md` with a math-to-AI profile and an overconfident rank section:

```markdown
# Quality Fixture: Weak Cross-Field Report

## Generation Note

This is a quality fixture for validator tests. It is not application advice.

## Student Profile

- Field: mathematics
- Subfield: mathematics and applied mathematics
- Application path: recommendation-based master's or direct PhD
- Target scope: AI school
- Research interests: artificial intelligence, machine learning
- Career orientation: AI research
- Background signals: mathematics coursework

## Ranked Shortlist

### Rank 1: Example AI Supervisor

- Institution: Example University
- Unit: School of Artificial Intelligence
- Eligibility: current quota unknown
- Research tags: artificial intelligence
- Recommendation: strong_recommend
- Best fit for: math student moving into AI
- Evidence strength: low
- Risk level: low

#### Fit Scores

- Research fit: 5/5 because mathematics is the foundation of AI.
- Path fit: 5/5 because math students can transfer to AI easily.
- Career fit: 5/5 because AI is a strong career direction.
- Evidence strength: 2/5 because only one broad official profile is available.
- Risk and uncertainty: 1/5 because there is little risk.

#### Recent Work

- Official AI profile [official]

#### Why This Fit

Fact: the supervisor is in an AI school.

Inference: a math student should be a strong fit for any AI lab.

Unknown: current projects, ML preparation expectations, coding artifacts, lab experience, and direct PhD quota.

#### Questions To Ask

- Are math students accepted?

## Maybe List

- No maybe candidates.

## Excluded List

- No excluded candidates.

## Risks And Unknowns

- The report does not verify AI-readiness evidence.

## Source Appendix

- https://example.edu/ai-profile [official]

## Next Actions

1. Contact the supervisor.
```

- [ ] **Step 5: Commit Task 2**

```powershell
git add -- tests\fixtures\report_quality
git commit -m "Add report quality fixtures"
```

---

### Task 3: Add Core Validator Quality Checks

**Files:**
- Modify: `tools/skill_pack_validator.py`
- Modify: `tests/test_skill_pack_validator.py`

- [ ] **Step 1: Write tests for required lists and risk levels**

Add imports in `tests/test_skill_pack_validator.py` if needed:

```python
from tools.skill_pack_validator import validate_report_quality
```

Add these tests:

```python
    def test_validate_report_quality_requires_maybe_and_excluded_lists(self):
        text = """# Demo

## Generation Note

Public-source demo.

## Student Profile

## Ranked Shortlist

### Rank 1: Prof. One

- Risk level: medium

#### Fit Scores

- Research fit: 4/5
- Path fit: 4/5
- Career fit: 4/5
- Evidence strength: 4/5
- Risk and uncertainty: 3/5

Fact: supported by official source.
Inference: likely fit.
Unknown: quota.

## Risks And Unknowns

## Source Appendix

- Demo source [official]
- Demo paper [bibliographic]

## Next Actions
"""
        self.assertEqual(
            validate_report_quality(text, "real_demo.md", set(["official", "bibliographic"])),
            [
                ValidationIssue("real_demo.md", "missing section: ## Maybe List"),
                ValidationIssue("real_demo.md", "missing section: ## Excluded List"),
            ],
        )

    def test_validate_report_quality_rejects_invalid_risk_level(self):
        text = """# Demo

## Generation Note

Public-source demo.

## Student Profile

## Ranked Shortlist

### Rank 1: Prof. One

- Risk level: safe

#### Fit Scores

- Research fit: 4/5
- Path fit: 4/5
- Career fit: 4/5
- Evidence strength: 4/5
- Risk and uncertainty: 3/5

Fact: supported by official source.
Inference: likely fit.
Unknown: quota.

## Maybe List

- No maybe candidates.

## Excluded List

- No excluded candidates.

## Risks And Unknowns

## Source Appendix

- Demo source [official]
- Demo paper [bibliographic]

## Next Actions
"""
        self.assertEqual(
            validate_report_quality(text, "demo.md", set(["official", "bibliographic"])),
            [ValidationIssue("demo.md", "invalid risk level: safe")],
        )
```

- [ ] **Step 2: Implement allowed risk level checks**

In `tools/skill_pack_validator.py`, add near other constants:

```python
REPORT_REQUIRED_LIST_SECTIONS = ["## Maybe List", "## Excluded List"]
ALLOWED_RISK_LEVELS = set(["low", "medium", "medium_high", "high", "unknown"])
```

Add helper functions:

```python
def validate_required_report_lists(text, location):
    return validate_markdown_sections(text, REPORT_REQUIRED_LIST_SECTIONS, location)


def extract_risk_level(section):
    match = re.search(r"(?im)^\s*[-*]\s*Risk level\s*:\s*([A-Za-z_]+)\s*$", section)
    if not match:
        return None
    return match.group(1).strip().lower()


def validate_risk_levels(text, location):
    issues = []
    rank_sections = extract_rank_sections(text)
    if not rank_sections:
        rank_sections = [text]
    for section in rank_sections:
        risk_level = extract_risk_level(section)
        if risk_level is None:
            issues.append(ValidationIssue(location, "missing risk level"))
        elif risk_level not in ALLOWED_RISK_LEVELS:
            issues.append(ValidationIssue(location, "invalid risk level: {}".format(risk_level)))
    return issues
```

Update `validate_report_quality` to call:

```python
    issues.extend(validate_required_report_lists(text, location))
    issues.extend(validate_risk_levels(text, location))
```

- [ ] **Step 3: Run focused tests**

Run:

```powershell
python -m unittest tests.test_skill_pack_validator -v
```

Expected: all tests pass after implementation.

- [ ] **Step 4: Commit Task 3**

```powershell
git add -- tools\skill_pack_validator.py tests\test_skill_pack_validator.py
git commit -m "Validate report lists and risk levels"
```

---

### Task 4: Add Overclaim And Source Label Robustness Checks

**Files:**
- Modify: `tools/skill_pack_validator.py`
- Modify: `tests/test_skill_pack_validator.py`

- [ ] **Step 1: Add tests for admissions certainty language**

Add to `tests/test_skill_pack_validator.py`:

```python
    def test_validate_report_quality_rejects_admissions_certainty_language_in_real_reports(self):
        text = """# Demo

## Generation Note

Public-source demo.

## Student Profile

## Ranked Shortlist

### Rank 1: Prof. One

- Risk level: medium

#### Fit Scores

- Research fit: 4/5
- Path fit: 4/5
- Career fit: 4/5
- Evidence strength: 4/5
- Risk and uncertainty: 3/5

Fact: supported by official source.
Inference: this supervisor appears relevant.
Unknown: current quota.

## Maybe List

- No maybe candidates.

## Excluded List

- No excluded candidates.

## Risks And Unknowns

- This report says guaranteed admission.

## Source Appendix

- Demo source [official]
- Demo paper [bibliographic]

## Next Actions
"""
        self.assertEqual(
            validate_report_quality(text, "real_demo.md", set(["official", "bibliographic"])),
            [ValidationIssue("real_demo.md", "real demo report contains admissions-certainty language: guaranteed admission")],
        )
```

- [ ] **Step 2: Add tests for Markdown source links**

Add:

```python
    def test_validate_report_quality_allows_markdown_links_with_trailing_source_label(self):
        text = """# Demo

## Generation Note

Public-source demo.

## Student Profile

## Ranked Shortlist

### Rank 1: Prof. One

- Risk level: medium

#### Fit Scores

- Research fit: 4/5
- Path fit: 4/5
- Career fit: 4/5
- Evidence strength: 4/5
- Risk and uncertainty: 3/5

Fact: supported by official source.
Inference: likely fit.
Unknown: quota.

## Maybe List

- No maybe candidates.

## Excluded List

- No excluded candidates.

## Risks And Unknowns

## Source Appendix

- [Faculty profile](https://example.edu/faculty) [official]
- [Publication page](https://example.org/paper) [bibliographic]

## Next Actions
"""
        self.assertEqual(
            validate_report_quality(text, "demo.md", set(["official", "bibliographic"])),
            [],
        )
```

- [ ] **Step 3: Implement admissions-certainty phrase checks**

Add constants:

```python
REAL_REPORT_CERTAINTY_PHRASES = [
    "guaranteed admission",
    "definitely accepts",
    "safe supervisor",
    "bad supervisor",
    "will admit",
    "一定录取",
    "稳录",
    "必收",
]
```

Add:

```python
def validate_real_demo_certainty_language(text, location):
    if not is_real_demo_report(location):
        return []
    lowered = text.lower()
    for phrase in REAL_REPORT_CERTAINTY_PHRASES:
        if phrase.lower() in lowered:
            return [
                ValidationIssue(
                    location,
                    "real demo report contains admissions-certainty language: {}".format(phrase),
                )
            ]
    return []
```

Call it from `validate_report_quality` after `validate_real_demo_language`.

- [ ] **Step 4: Implement Markdown-aware source labels**

Replace label extraction inside `validate_source_appendix_labels` with a helper:

```python
def remove_markdown_links(text):
    return re.sub(r"\[[^\[\]]+\]\([^\(\)]+\)", "", text)
```

Then inside the line loop:

```python
        label_text = remove_markdown_links(stripped)
        label_matches = list(re.finditer(r"\[([^\[\]]+)\]", label_text))
```

This keeps `[official]` while ignoring `[Faculty profile](https://...)`.

- [ ] **Step 5: Run focused tests**

Run:

```powershell
python -m unittest tests.test_skill_pack_validator -v
```

Expected: all tests pass.

- [ ] **Step 6: Commit Task 4**

```powershell
git add -- tools\skill_pack_validator.py tests\test_skill_pack_validator.py
git commit -m "Reject report overclaims and parse source links"
```

---

### Task 5: Add Ranked Evidence Signal And Fixture Tests

**Files:**
- Modify: `tools/skill_pack_validator.py`
- Modify: `tests/test_skill_pack_validator.py`

- [ ] **Step 1: Add fixture-loading helper to tests**

In `tests/test_skill_pack_validator.py`, add near imports:

```python
ROOT = Path(__file__).resolve().parents[1]


def load_report_fixture(filename):
    path = ROOT / "tests" / "fixtures" / "report_quality" / filename
    return path.read_text(encoding="utf-8")
```

- [ ] **Step 2: Add fixture tests**

Add:

```python
    def test_quality_fixture_good_minimal_report_passes(self):
        text = load_report_fixture("good_minimal_report.md")
        self.assertEqual(
            validate_report_quality(text, "real_good_minimal_report.md", set(["official", "bibliographic"])),
            [],
        )

    def test_quality_fixture_overclaim_report_fails(self):
        text = load_report_fixture("overclaim_admissions_report.md")
        issues = validate_report_quality(text, "real_overclaim_admissions_report.md", set(["official", "bibliographic"]))
        self.assertIn(
            ValidationIssue(
                "real_overclaim_admissions_report.md",
                "real demo report contains admissions-certainty language: guaranteed admission",
            ),
            issues,
        )

    def test_quality_fixture_weak_cross_field_report_fails_evidence_signal_check(self):
        text = load_report_fixture("weak_cross_field_report.md")
        issues = validate_report_quality(text, "real_weak_cross_field_report.md", set(["official", "bibliographic"]))
        self.assertIn(
            ValidationIssue(
                "real_weak_cross_field_report.md",
                "ranked supervisor has fewer than two source-labeled evidence mentions",
            ),
            issues,
        )
```

- [ ] **Step 3: Implement source-label counting**

In `tools/skill_pack_validator.py`, add:

```python
def count_source_labels_in_text(text, allowed_source_labels):
    count = 0
    for label_match in re.finditer(r"\[([^\[\]]+)\]", remove_markdown_links(text)):
        labels = [label.strip() for label in label_match.group(1).split("/")]
        for label in labels:
            if label in allowed_source_labels and label not in set(["inferred", "unknown", "community"]):
                count += 1
    return count


def has_exploratory_uncertainty_language(text):
    lowered = text.lower()
    phrases = [
        "only one public source",
        "maybe list",
        "exploratory",
        "insufficient evidence",
        "source coverage is limited",
    ]
    for phrase in phrases:
        if phrase in lowered:
            return True
    return False


def validate_ranked_evidence_signals(text, location, allowed_source_labels):
    issues = []
    rank_sections = extract_rank_sections(text)
    if not rank_sections:
        rank_sections = [text]
    for section in rank_sections:
        if count_source_labels_in_text(section, allowed_source_labels) < 2 and not has_exploratory_uncertainty_language(section):
            issues.append(
                ValidationIssue(
                    location,
                    "ranked supervisor has fewer than two source-labeled evidence mentions",
                )
            )
    return issues
```

Call from `validate_report_quality`:

```python
    issues.extend(validate_ranked_evidence_signals(text, location, allowed_source_labels))
```

- [ ] **Step 4: Adjust existing real reports if validator exposes real quality gaps**

Run:

```powershell
python tools\skill_pack_validator.py
```

If a real report fails because a ranked section has fewer than two source-labeled evidence mentions, update that report section by adding source labels to existing `Recent Work` or `Why This Fit` evidence. Do not invent new sources. Use only sources already present in the report's Source Appendix.

- [ ] **Step 5: Run focused and full tests**

Run:

```powershell
python -m unittest tests.test_skill_pack_validator -v
python -m unittest discover -s tests -v
python tools\skill_pack_validator.py
```

Expected: all pass.

- [ ] **Step 6: Commit Task 5**

```powershell
git add -- tools\skill_pack_validator.py tests\test_skill_pack_validator.py skills\find-my-supervisor\examples\reports
git commit -m "Validate ranked evidence signals"
```

---

### Task 6: Wire Quality System Into Docs

**Files:**
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `tools/install_integrity_check.py` if Task 1 did not already update it

- [ ] **Step 1: Add small English README quality reference**

In `README.md`, add a short subsection near `What The Report Includes`:

```markdown
## Report Quality

The skill pack includes a human review rubric and failure-mode catalog:

- `skills/find-my-supervisor/references/report-quality-rubric.md`
- `skills/find-my-supervisor/references/failure-modes.md`

These references are meant to keep reports source-backed, cautious, and useful inside the current CS/AI and mathematics vertical scope.
```

- [ ] **Step 2: Add small Chinese README quality reference**

In `README.zh-CN.md`, add a short subsection near `报告会包含什么`:

```markdown
## 报告质量体系

这个 skill pack 现在包含一份人工评审 rubric 和一份失败模式清单：

- `skills/find-my-supervisor/references/report-quality-rubric.md`
- `skills/find-my-supervisor/references/failure-modes.md`

它们的作用是让报告保持公开来源支撑、谨慎表达和可核查性。当前目标仍然是 CS/AI 与数学方向的强垂类工具，不是通用导师搜索平台，也不是网站路线。
```

- [ ] **Step 3: Run final verification**

Run:

```powershell
python -m unittest discover -s tests -v
python tools\skill_pack_validator.py
python tools\install_integrity_check.py skills\find-my-supervisor
```

Expected:

```text
OK
Skill pack validation passed.
Installation integrity check passed.
```

- [ ] **Step 4: Commit Task 6**

```powershell
git add -- README.md README.zh-CN.md tools\install_integrity_check.py
git commit -m "Document report quality system"
```

---

## Final Verification

After all tasks:

```powershell
python -m unittest discover -s tests -v
python tools\skill_pack_validator.py
python tools\install_integrity_check.py skills\find-my-supervisor
git status --short --branch
git log --oneline -8
```

Expected:

- Unit tests pass.
- Skill pack validation passes.
- Install integrity check passes.
- `git status --short --branch` shows only the known protected untracked legacy paths:
  - `_tmp_agents_md_output.md`
  - `_tmp_legacy_agents_md_output.md`
  - `_tmp_gsd_agents_key/`
  - `get-shit-done-codex/`

Do not delete or move those protected paths.
