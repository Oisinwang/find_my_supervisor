# Release Readiness And Quality Gate V2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Find My Supervisor more release-ready and strengthen the report quality gate for the current CS/AI and mathematics skills vertical.

**Architecture:** Keep the package as a folder-based skill pack. Add release docs, tighten `.gitignore`, and extend the existing dependency-free Python validator with focused helper functions and unit tests.

**Tech Stack:** Python 3.6-compatible standard library, `unittest`, Markdown skill/reference files.

---

## Task 1: Release Readiness Docs And Tree Safety

**Files:**

- Create: `docs/release-readiness-audit.md`
- Create: `docs/release-checklist.md`
- Modify: `.gitignore`

- [ ] Add release-readiness audit with current beta status, blockers, acceptable beta risks, and future work.
- [ ] Add release checklist with exact verification commands and release-tree expectations.
- [ ] Add protected old temporary paths to `.gitignore` without editing, moving, or deleting those paths.
- [ ] Run:

```powershell
python -m unittest discover -s tests -v
python tools\skill_pack_validator.py
python tools\install_integrity_check.py skills\find-my-supervisor
```

- [ ] Commit:

```powershell
git add .gitignore docs/release-readiness-audit.md docs/release-checklist.md
git commit -m "Add release readiness audit"
```

## Task 2: Quality Gate V2 Validator

**Files:**

- Modify: `tools/skill_pack_validator.py`
- Modify: `tests/test_skill_pack_validator.py`
- Optional modify: `tests/fixtures/report_quality/*.md`

- [ ] Write failing tests for required `official` or `bibliographic` source support per ranked supervisor.
- [ ] Write failing tests for appendix coverage of labels used in ranked sections.
- [ ] Write failing tests for `Eligibility` and `Recent Work` source-label expectations.
- [ ] Write failing tests for decorative unknowns and unknowns not covered by questions or next actions.
- [ ] Write failing tests for generic next actions and missing action-class coverage.
- [ ] Write failing tests showing overclaim checks apply to all reports.
- [ ] Write failing tests for math/statistics-to-CS/AI cross-field readiness.
- [ ] Implement validator helpers with Python 3.6-compatible syntax only.
- [ ] Run:

```powershell
python -m unittest discover -s tests -v
python tools\skill_pack_validator.py
python tools\install_integrity_check.py skills\find-my-supervisor
```

- [ ] Commit:

```powershell
git add tools/skill_pack_validator.py tests/test_skill_pack_validator.py tests/fixtures/report_quality
git commit -m "Strengthen report quality gate v2"
```

## Task 3: Release Wording And Install/Validator Sync

**Files:**

- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `skills/find-my-supervisor/SKILL.md`
- Modify: `skills/find-my-supervisor/examples/reports/real_hkust_trustworthy_llm_demo.md`
- Modify: `skills/find-my-supervisor/examples/reports/real_mainland_math_demo.md`
- Modify: `tools/skill_pack_validator.py`
- Modify: `tools/install_integrity_check.py`
- Modify: `tests/test_install_integrity.py`
- Modify: `tests/test_skill_pack_validator.py`

- [ ] Replace cold-email-adjacent wording with student-controlled communication-preparation wording.
- [ ] Keep the safety boundary that the skill does not send or automate messages.
- [ ] Make validator and install integrity use the same canonical required report list, or add tests that fail if they diverge.
- [ ] Ensure `real_mainland_math_demo.md` is required by the validator.
- [ ] Add tests for missing required quality references and required reports.
- [ ] Run:

```powershell
python -m unittest discover -s tests -v
python tools\skill_pack_validator.py
python tools\install_integrity_check.py skills\find-my-supervisor
```

- [ ] Commit:

```powershell
git add README.md README.zh-CN.md skills/find-my-supervisor/SKILL.md skills/find-my-supervisor/examples/reports/real_hkust_trustworthy_llm_demo.md skills/find-my-supervisor/examples/reports/real_mainland_math_demo.md tools/skill_pack_validator.py tools/install_integrity_check.py tests/test_install_integrity.py tests/test_skill_pack_validator.py
git commit -m "Align release wording and required files"
```

## Task 4: Final Review And Push

**Files:** no planned edits unless reviewers find blockers.

- [ ] Run final spec reviewer over Tasks 1-3.
- [ ] Run final quality reviewer over Tasks 1-3.
- [ ] Run:

```powershell
python -m unittest discover -s tests -v
python tools\skill_pack_validator.py
python tools\install_integrity_check.py skills\find-my-supervisor
git status --short --branch
git log --oneline -8
```

- [ ] Commit any reviewer-required fixes.
- [ ] Push:

```powershell
git push origin main
```

## Notes

- Do not delete, move, edit, or stage the protected old untracked paths:
  - `_tmp_agents_md_output.md`
  - `_tmp_legacy_agents_md_output.md`
  - `_tmp_gsd_agents_key/`
  - `get-shit-done-codex/`
- If a deletion is explicitly requested later, move the file to `D:\rubbish` instead of permanently deleting it.
- Do not add website, UI, rating-platform, crawler-platform, or mass-outreach functionality.
