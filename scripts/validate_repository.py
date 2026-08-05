#!/usr/bin/env python3
"""Validate the repository's initial structural contracts without dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    ".github/issue-labels.json",
    ".github/ISSUE_TEMPLATE/config.yml",
    "docs/architecture.md",
    "docs/github/issues.md",
    "external/catalog.yaml",
    "templates/skill/SKILL.md",
]
REQUIRED_DIRECTORIES = [
    "skills",
    "tools",
    "packages",
    "configs/shared",
    "configs/codex",
    "configs/claude",
    "external",
    "scripts",
    "tests",
    "docs/decisions",
]
ISSUE_FORM_KEYS = ("name", "description", "title", "labels", "body")
KEBAB_CASE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
HEX_COLOR = re.compile(r"^[0-9A-Fa-f]{6}$")


def validate_paths(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")
    for relative in REQUIRED_DIRECTORIES:
        if not (ROOT / relative).is_dir():
            errors.append(f"missing required directory: {relative}")


def load_label_names(errors: list[str]) -> set[str]:
    path = ROOT / ".github" / "issue-labels.json"
    if not path.is_file():
        return set()
    try:
        catalog = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        errors.append(f"invalid label catalog: {exc}")
        return set()

    labels = catalog.get("labels")
    if catalog.get("version") != 1 or not isinstance(labels, list):
        errors.append("label catalog must have version 1 and a labels array")
        return set()

    names: set[str] = set()
    for index, label in enumerate(labels):
        if not isinstance(label, dict):
            errors.append(f"label entry {index} must be an object")
            continue
        name = label.get("name")
        color = label.get("color")
        description = label.get("description")
        if not isinstance(name, str) or not name:
            errors.append(f"label entry {index} has no name")
        elif name in names:
            errors.append(f"duplicate label: {name}")
        else:
            names.add(name)
        if not isinstance(color, str) or not HEX_COLOR.fullmatch(color):
            errors.append(f"label {name!r} must use a six-digit hex color")
        if not isinstance(description, str) or not description.strip():
            errors.append(f"label {name!r} has no description")
    return names


def validate_issue_forms(label_names: set[str], errors: list[str]) -> None:
    directory = ROOT / ".github" / "ISSUE_TEMPLATE"
    for path in sorted(directory.glob("*.yml")):
        if path.name == "config.yml":
            continue
        text = path.read_text(encoding="utf-8")
        for key in ISSUE_FORM_KEYS:
            if not re.search(rf"^{key}:\s*\S", text, re.MULTILINE):
                errors.append(f"{path.relative_to(ROOT)} is missing top-level {key}")

        labels_match = re.search(r"^labels:\s*(\[.*\])\s*$", text, re.MULTILINE)
        if labels_match:
            try:
                form_labels = json.loads(labels_match.group(1))
            except json.JSONDecodeError as exc:
                errors.append(f"{path.relative_to(ROOT)} has invalid inline labels: {exc}")
            else:
                for label in form_labels:
                    if label not in label_names:
                        errors.append(
                            f"{path.relative_to(ROOT)} references unknown label: {label}"
                        )
        else:
            errors.append(f"{path.relative_to(ROOT)} must use an inline labels array")

        ids = re.findall(r"^\s+id:\s*([a-z0-9_-]+)\s*$", text, re.MULTILINE)
        duplicates = sorted({item for item in ids if ids.count(item) > 1})
        if duplicates:
            errors.append(
                f"{path.relative_to(ROOT)} has duplicate field ids: {', '.join(duplicates)}"
            )


def validate_skills(errors: list[str]) -> None:
    skills_directory = ROOT / "skills"
    for directory in sorted(path for path in skills_directory.iterdir() if path.is_dir()):
        skill_file = directory / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"skill directory has no SKILL.md: {directory.relative_to(ROOT)}")
            continue
        text = skill_file.read_text(encoding="utf-8")
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
        if not match:
            errors.append(f"skill has invalid frontmatter: {skill_file.relative_to(ROOT)}")
            continue
        frontmatter = match.group(1)
        name_match = re.search(r"^name:\s*([^\s]+)\s*$", frontmatter, re.MULTILINE)
        description_match = re.search(
            r"^description:\s*(\S.*)$", frontmatter, re.MULTILINE
        )
        if not name_match or not KEBAB_CASE.fullmatch(name_match.group(1)):
            errors.append(f"skill name must be kebab-case: {skill_file.relative_to(ROOT)}")
        elif name_match.group(1) != directory.name:
            errors.append(
                f"skill name must match directory: {skill_file.relative_to(ROOT)}"
            )
        if not description_match:
            errors.append(f"skill has no description: {skill_file.relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []
    validate_paths(errors)
    label_names = load_label_names(errors)
    validate_issue_forms(label_names, errors)
    validate_skills(errors)

    if errors:
        print("repository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    issue_form_count = len(
        [
            path
            for path in (ROOT / ".github" / "ISSUE_TEMPLATE").glob("*.yml")
            if path.name != "config.yml"
        ]
    )
    skill_count = len([path for path in (ROOT / "skills").iterdir() if path.is_dir()])
    print(
        f"repository validation passed: {len(label_names)} labels, "
        f"{issue_form_count} issue forms, {skill_count} skills"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
