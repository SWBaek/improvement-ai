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
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/skill_request.yml",
    ".github/ISSUE_TEMPLATE/tool_request.yml",
    ".github/workflows/validate.yml",
    "configs/README.md",
    "docs/architecture.md",
    "docs/decisions/README.md",
    "docs/github/issues.md",
    "external/README.md",
    "external/catalog.yaml",
    "frameworks/README.md",
    "packages/README.md",
    "skills/README.md",
    "templates/skill/SKILL.md",
    "tests/README.md",
    "tools/README.md",
]
REQUIRED_DIRECTORIES = [
    "configs",
    "docs/decisions",
    "external",
    "frameworks",
    "packages",
    "scripts",
    "skills",
    "tests",
    "tools",
]
ISSUE_FORM_KEYS = ("name", "description", "title", "labels", "body")
KEBAB_CASE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
HEX_COLOR = re.compile(r"^[0-9A-Fa-f]{6}$")
DECISION_FILE = re.compile(r"^[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
SKILL_INDEX_ROW = re.compile(
    r"^\|\s*\[([a-z0-9]+(?:-[a-z0-9]+)*)\]\(([^)]+)\)\s*"
    r"\|\s*(In Progress|Promoted|Deprecated)\s*\|\s*(\S.*?)\s*\|$"
)


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


def load_skill_index(errors: list[str]) -> dict[str, tuple[str, str]]:
    path = ROOT / "skills" / "README.md"
    if not path.is_file():
        return {}

    text = path.read_text(encoding="utf-8")
    start_marker = "<!-- skill-index:start -->"
    end_marker = "<!-- skill-index:end -->"
    if text.count(start_marker) != 1 or text.count(end_marker) != 1:
        errors.append("skills/README.md must contain one skill index marker pair")
        return {}

    block = text.split(start_marker, 1)[1].split(end_marker, 1)[0]
    entries: dict[str, tuple[str, str]] = {}
    for line in block.splitlines():
        stripped = line.strip()
        if not stripped.startswith("| ["):
            continue
        match = SKILL_INDEX_ROW.fullmatch(stripped)
        if not match:
            errors.append(f"malformed skill index row: {stripped}")
            continue
        name, target, status, _tracking = match.groups()
        if name in entries:
            errors.append(f"duplicate skill index entry: {name}")
            continue
        expected_target = f"{name}/SKILL.md"
        if target != expected_target:
            errors.append(
                f"skill index target for {name} must be {expected_target}: {target}"
            )
        entries[name] = (target, status)
    return entries


def validate_skills(errors: list[str]) -> None:
    skills_directory = ROOT / "skills"
    if not skills_directory.is_dir():
        return

    index = load_skill_index(errors)
    directories = {
        path.name: path for path in skills_directory.iterdir() if path.is_dir()
    }
    for name in sorted(set(directories) - set(index)):
        errors.append(f"skill is not registered in skills/README.md: {name}")
    for name in sorted(set(index) - set(directories)):
        errors.append(f"skill index references missing directory: {name}")

    for directory in sorted(directories.values()):
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


def validate_decisions(errors: list[str]) -> None:
    directory = ROOT / "docs" / "decisions"
    index_path = directory / "README.md"
    if not directory.is_dir() or not index_path.is_file():
        return

    decision_paths = sorted(
        path for path in directory.glob("*.md") if path.name != "README.md"
    )
    index_text = index_path.read_text(encoding="utf-8")
    index_entries = re.findall(r"\[([0-9]{4})\]\(([^)]+\.md)\)", index_text)
    indexed_targets = [target for _number, target in index_entries]

    for number, target in index_entries:
        if not target.startswith(f"{number}-"):
            errors.append(f"decision index number {number} does not match target: {target}")
        if not (directory / target).is_file():
            errors.append(f"decision index references missing file: {target}")
    for target in sorted({item for item in indexed_targets if indexed_targets.count(item) > 1}):
        errors.append(f"duplicate decision index entry: {target}")

    for path in decision_paths:
        relative = path.relative_to(ROOT)
        if not DECISION_FILE.fullmatch(path.name):
            errors.append(f"decision must use numbered kebab-case filename: {relative}")
        if indexed_targets.count(path.name) != 1:
            errors.append(f"decision must appear exactly once in index: {relative}")

        text = path.read_text(encoding="utf-8")
        if not re.search(r"^- 상태:\s*\S.*$", text, re.MULTILINE):
            errors.append(f"decision has no status: {relative}")
        if not re.search(r"^- 날짜:\s*[0-9]{4}-[0-9]{2}-[0-9]{2}\s*$", text, re.MULTILINE):
            errors.append(f"decision has invalid date: {relative}")
        for heading in ("## 결정", "## 이유", "## 결과"):
            if heading not in text:
                errors.append(f"decision is missing {heading}: {relative}")


def validate_frameworks(errors: list[str]) -> None:
    frameworks_directory = ROOT / "frameworks"
    if not frameworks_directory.is_dir():
        return

    required_children = {"README.md"}
    for directory in sorted(path for path in frameworks_directory.iterdir() if path.is_dir()):
        # Git does not track empty directories; ignore local remnants with no files.
        if not any(path.is_file() for path in directory.rglob("*")):
            continue
        relative = directory.relative_to(ROOT)
        if not KEBAB_CASE.fullmatch(directory.name):
            errors.append(f"framework name must be kebab-case: {relative}")
        missing = sorted(item for item in required_children if not (directory / item).exists())
        if missing:
            errors.append(f"framework {relative} is missing: {', '.join(missing)}")

        for schema_path in sorted((directory / "schemas").glob("*.json")):
            try:
                schema = json.loads(schema_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as exc:
                errors.append(f"invalid framework schema {schema_path.relative_to(ROOT)}: {exc}")
                continue
            if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
                errors.append(
                    f"framework schema must use JSON Schema 2020-12: "
                    f"{schema_path.relative_to(ROOT)}"
                )
            if not isinstance(schema.get("$id"), str) or not schema["$id"].startswith("urn:"):
                errors.append(
                    f"framework schema must use an offline URN id: "
                    f"{schema_path.relative_to(ROOT)}"
                )

        for decision_path in sorted((directory / "decisions").glob("*.md")):
            if not DECISION_FILE.fullmatch(decision_path.name):
                errors.append(
                    f"framework decision must use numbered kebab-case filename: "
                    f"{decision_path.relative_to(ROOT)}"
                )
            decision_text = decision_path.read_text(encoding="utf-8")
            for heading in ("## 결정", "## 이유", "## 결과"):
                if heading not in decision_text:
                    errors.append(
                        f"framework decision is missing {heading}: "
                        f"{decision_path.relative_to(ROOT)}"
                    )


def main() -> int:
    errors: list[str] = []
    validate_paths(errors)
    label_names = load_label_names(errors)
    validate_issue_forms(label_names, errors)
    validate_skills(errors)
    validate_decisions(errors)
    validate_frameworks(errors)

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
    framework_count = len(
        [
            path
            for path in (ROOT / "frameworks").iterdir()
            if path.is_dir() and any(item.is_file() for item in path.rglob("*"))
        ]
    )
    print(
        f"repository validation passed: {len(label_names)} labels, "
        f"{issue_form_count} issue forms, {skill_count} skills, "
        f"{framework_count} frameworks"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
