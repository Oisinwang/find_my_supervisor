from __future__ import print_function

import argparse
from pathlib import Path

try:
    from tools.skill_pack_manifest import REQUIRED_DIRECTORIES, REQUIRED_FILES
except ImportError:
    from skill_pack_manifest import REQUIRED_DIRECTORIES, REQUIRED_FILES


def validate_installation(path):
    """Return install completeness issues for a find-my-supervisor skill directory."""
    root = Path(path)
    issues = []

    if not root.exists():
        return ["installation path does not exist: {}".format(root)]
    if not root.is_dir():
        return ["installation path is not a directory: {}".format(root)]

    for relative_path in REQUIRED_DIRECTORIES:
        if not (root / relative_path).is_dir():
            issues.append("missing required directory: {}".format(relative_path))

    for relative_path in REQUIRED_FILES:
        if not (root / relative_path).is_file():
            issues.append("missing required file: {}".format(relative_path))

    return issues


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate an installed find-my-supervisor skill directory."
    )
    parser.add_argument(
        "path",
        help="Path to an installed find-my-supervisor skill directory.",
    )
    args = parser.parse_args(argv)

    issues = validate_installation(args.path)
    if issues:
        for issue in issues:
            print(issue)
        return 1

    print("Installation integrity check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
