# Installation End-to-End Test

Use these steps to validate that a fresh user can copy and use the
`find-my-supervisor` skill pack without writing to global skill directories.

These commands copy `skills/find-my-supervisor` into a temporary directory only.
They do not write to `~/.codex/skills`, `~/.claude/skills`, or any other global
agent runtime directory.

## Windows PowerShell

Run from the repository root:

```powershell
$repo = (Get-Location).Path
$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("find-my-supervisor-install-test-" + [guid]::NewGuid())
$skillsRoot = Join-Path $tempRoot "skills"
$target = Join-Path $skillsRoot "find-my-supervisor"

New-Item -ItemType Directory -Force $skillsRoot | Out-Null
Copy-Item -Recurse -Force ".\skills\find-my-supervisor" $target

python .\tools\install_integrity_check.py $target
```

Expected output:

```text
Installation integrity check passed.
```

Confirm the installed skill directory contains the complete pack:

```powershell
Test-Path (Join-Path $target "SKILL.md")
Test-Path (Join-Path $target "references")
Test-Path (Join-Path $target "schemas")
Test-Path (Join-Path $target "examples")
Test-Path (Join-Path $target "examples\profiles")
Test-Path (Join-Path $target "examples\reports")
```

Each command should print `True`.

## macOS/Linux

Run from the repository root:

```bash
repo="$(pwd)"
temp_root="$(mktemp -d "${TMPDIR:-/tmp}/find-my-supervisor-install-test.XXXXXX")"
skills_root="$temp_root/skills"
target="$skills_root/find-my-supervisor"

mkdir -p "$skills_root"
cp -R "$repo/skills/find-my-supervisor" "$target"

python tools/install_integrity_check.py "$target"
```

Expected output:

```text
Installation integrity check passed.
```

Confirm the installed skill directory contains the complete pack:

```bash
test -f "$target/SKILL.md" && echo "SKILL.md ok"
test -d "$target/references" && echo "references ok"
test -d "$target/schemas" && echo "schemas ok"
test -d "$target/examples" && echo "examples ok"
test -d "$target/examples/profiles" && echo "examples/profiles ok"
test -d "$target/examples/reports" && echo "examples/reports ok"
```

## What Is Checked

The integrity check verifies the installed `find-my-supervisor` directory has:

- `SKILL.md`
- `references/`, including workflow, intake, source, risk, report template, and rubric files
- `schemas/`, including the profile, supervisor, evidence, fit, institution, and report schemas
- `examples/profiles/`, including the packaged profile JSON files
- `examples/reports/`, including the synthetic and public-source demo reports

After this passes, a folder-based agent runtime can load the copied
`find-my-supervisor` directory as a complete skill pack.
