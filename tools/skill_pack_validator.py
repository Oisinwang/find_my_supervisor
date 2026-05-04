import json
from pathlib import Path


class ValidationIssue(object):
    def __init__(self, location, message):
        self.location = location
        self.message = message

    def __eq__(self, other):
        return (
            isinstance(other, ValidationIssue)
            and self.location == other.location
            and self.message == other.message
        )

    def __repr__(self):
        return "ValidationIssue(location={!r}, message={!r})".format(
            self.location,
            self.message,
        )


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def require_keys(data, required_keys, location):
    issues = []
    for key in required_keys:
        if key not in data:
            issues.append(ValidationIssue(location, "missing required key: {}".format(key)))
    return issues


def validate_markdown_sections(text, required_sections, location):
    issues = []
    for section in required_sections:
        if section not in text:
            issues.append(ValidationIssue(location, "missing section: {}".format(section)))
    return issues


def validate_json_file(path):
    try:
        load_json(path)
    except ValueError as exc:
        return [ValidationIssue(str(path), "invalid JSON: {}".format(exc))]
    return []
