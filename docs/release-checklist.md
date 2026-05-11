# Release Checklist

Use this checklist before an open-source skills beta release.

## Pre-Release Commands

```powershell
python -m unittest discover -s tests -v
python tools\skill_pack_validator.py
python tools\install_integrity_check.py skills\find-my-supervisor
git status --short --branch
git log --oneline -8
```

## Expected Status

- Branch is synced with upstream before release.
- `git status --short --branch` shows no tracked changes.
- Protected old temporary paths are ignored and not staged:
  - `_tmp_agents_md_output.md`
  - `_tmp_legacy_agents_md_output.md`
  - `_tmp_gsd_agents_key/`
  - `get-shit-done-codex/`
- Release remains skills/productized-agent only, with no website, UI, or platform route added.
