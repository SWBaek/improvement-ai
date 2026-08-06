#!/usr/bin/env python3
"""Validate repository, Skill catalog, distribution, and documentation contracts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "AGENTS.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "README.md",
    "README.ko.md",
    "SECURITY.md",
    ".github/CODEOWNERS",
    ".github/issue-labels.json",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/skill_request.yml",
    ".github/ISSUE_TEMPLATE/tool_request.yml",
    ".github/workflows/release.yml",
    ".github/workflows/validate.yml",
    "configs/README.md",
    "docs/architecture.md",
    "docs/decisions/README.md",
    "docs/github/issues.md",
    "docs/github/repository-settings.md",
    "docs/releases/README.md",
    "external/README.md",
    "external/catalog.yaml",
    "frameworks/README.md",
    "packages/README.md",
    "scripts/release_skills.py",
    "scripts/render_skill_index.py",
    "scripts/smoke_install.py",
    "skills/catalog.json",
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
SEMVER = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
DECISION_FILE = re.compile(r"^[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
SKILL_INDEX_ROW = re.compile(
    r"^\|\s*\[([a-z0-9]+(?:-[a-z0-9]+)*)\]\(([^)]+)\)\s*"
    r"\|\s*`([^`]+)`\s*\|\s*(In Progress|Promoted|Deprecated)\s*"
    r"\|\s*\[([^]]+)\]\(([^)]+)\)\s*"
    r"\|\s*\[#([0-9]+)\]\(([^)]+)\)\s*\|$"
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


def load_skill_catalog(errors: list[str]) -> dict[str, dict[str, object]]:
    path = ROOT / "skills" / "catalog.json"
    if not path.is_file():
        errors.append("missing Skill catalog: skills/catalog.json")
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        errors.append(f"invalid Skill catalog: {exc}")
        return {}

    if payload.get("schemaVersion") != 1 or not isinstance(payload.get("skills"), list):
        errors.append("Skill catalog must have schemaVersion 1 and a skills array")
        return {}

    entries: dict[str, dict[str, object]] = {}
    required = {
        "name",
        "version",
        "status",
        "trackingIssue",
        "changelog",
        "support",
        "workspaceSchemaVersion",
    }
    for index, item in enumerate(payload["skills"]):
        if not isinstance(item, dict):
            errors.append(f"Skill catalog entry {index} must be an object")
            continue
        unknown = set(item) - required
        missing = required - set(item)
        if missing or unknown:
            errors.append(
                f"Skill catalog entry {index} has missing {sorted(missing)} and unknown {sorted(unknown)} fields"
            )
            continue
        name = item["name"]
        if not isinstance(name, str) or not KEBAB_CASE.fullmatch(name):
            errors.append(f"Skill catalog entry {index} has invalid name: {name!r}")
            continue
        if name in entries:
            errors.append(f"duplicate Skill catalog entry: {name}")
            continue
        version = item["version"]
        if not isinstance(version, str) or not SEMVER.fullmatch(version):
            errors.append(f"Skill catalog {name} has invalid Semantic Version: {version!r}")
        if item["status"] not in {"In Progress", "Promoted", "Deprecated"}:
            errors.append(f"Skill catalog {name} has invalid status: {item['status']!r}")
        if not isinstance(item["trackingIssue"], int) or item["trackingIssue"] <= 0:
            errors.append(f"Skill catalog {name} must have a positive trackingIssue")
        support = item["support"]
        if support != {"codex": "supported", "otherAgentSkillsClients": "unverified"}:
            errors.append(f"Skill catalog {name} has unsupported client declaration")
        if not isinstance(item["workspaceSchemaVersion"], int) or item["workspaceSchemaVersion"] <= 0:
            errors.append(f"Skill catalog {name} has invalid workspaceSchemaVersion")
        changelog = item["changelog"]
        if not isinstance(changelog, str) or not changelog.startswith("docs/releases/"):
            errors.append(f"Skill catalog {name} has invalid changelog path")
        else:
            changelog_path = ROOT / changelog
            if not changelog_path.is_file():
                errors.append(f"Skill catalog {name} references missing changelog: {changelog}")
            elif isinstance(version, str) and not re.search(
                rf"^##\s+{re.escape(version)}\s*$", changelog_path.read_text(encoding="utf-8"), re.MULTILINE
            ):
                errors.append(f"Skill catalog {name} changelog has no {version} section")
        entries[name] = item
    return entries


def load_skill_index(errors: list[str]) -> dict[str, tuple[str, str, str, str, str, int, str]]:
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
    entries: dict[str, tuple[str, str, str, str, str, int, str]] = {}
    for line in block.splitlines():
        stripped = line.strip()
        if not stripped.startswith("| ["):
            continue
        match = SKILL_INDEX_ROW.fullmatch(stripped)
        if not match:
            errors.append(f"malformed skill index row: {stripped}")
            continue
        name, target, version, status, tag, release_url, issue_number, issue_url = match.groups()
        if name in entries:
            errors.append(f"duplicate skill index entry: {name}")
            continue
        expected_target = f"{name}/SKILL.md"
        if target != expected_target:
            errors.append(
                f"skill index target for {name} must be {expected_target}: {target}"
            )
        entries[name] = (target, version, status, tag, release_url, int(issue_number), issue_url)
    return entries


def validate_skills(errors: list[str]) -> None:
    skills_directory = ROOT / "skills"
    if not skills_directory.is_dir():
        return

    catalog = load_skill_catalog(errors)
    index = load_skill_index(errors)
    directories = {
        path.name: path for path in skills_directory.iterdir() if path.is_dir()
    }
    for name in sorted(set(directories) - set(catalog)):
        errors.append(f"skill is not registered in skills/catalog.json: {name}")
    for name in sorted(set(catalog) - set(directories)):
        errors.append(f"Skill catalog references missing directory: {name}")
    for name in sorted(set(catalog) - set(index)):
        errors.append(f"Skill catalog entry is missing from skills/README.md: {name}")
    for name in sorted(set(index) - set(catalog)):
        errors.append(f"Skill index entry is missing from skills/catalog.json: {name}")

    repository_url = "https://github.com/SWBaek/improvement-ai"
    for name in sorted(set(catalog) & set(index)):
        target, version, status, tag, release_url, issue_number, issue_url = index[name]
        metadata = catalog[name]
        expected_target = f"{name}/SKILL.md"
        expected_tag = f"{name}-v{metadata['version']}"
        expected_release = f"{repository_url}/releases/tag/{expected_tag}"
        expected_issue = f"{repository_url}/issues/{metadata['trackingIssue']}"
        if target != expected_target:
            errors.append(f"skill index target for {name} must be {expected_target}: {target}")
        if version != metadata["version"] or status != metadata["status"]:
            errors.append(f"skill index metadata is out of sync for {name}")
        if tag != expected_tag or release_url != expected_release:
            errors.append(f"skill index Release link is out of sync for {name}")
        if issue_number != metadata["trackingIssue"] or issue_url != expected_issue:
            errors.append(f"skill index tracking link is out of sync for {name}")

    root_license = ROOT / "LICENSE"
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
        frontmatter_keys = set(re.findall(r"^([A-Za-z][A-Za-z0-9_-]*):", frontmatter, re.MULTILINE))
        if frontmatter_keys != {"name", "description"}:
            errors.append(
                f"skill frontmatter must contain only name and description: {skill_file.relative_to(ROOT)}"
            )
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

        bundled_license = directory / "LICENSE.txt"
        if not bundled_license.is_file():
            errors.append(f"distributed skill has no LICENSE.txt: {directory.relative_to(ROOT)}")
        elif root_license.is_file() and bundled_license.read_bytes() != root_license.read_bytes():
            errors.append(f"distributed skill license differs from root LICENSE: {directory.relative_to(ROOT)}")

        forbidden = {"readme.md", "changelog.md", "installation_guide.md", "quick_reference.md"}
        for child in directory.iterdir():
            if child.is_file() and child.name.lower() in forbidden:
                errors.append(f"auxiliary documentation must stay outside Skill folders: {child.relative_to(ROOT)}")

        schema_path = directory / "references" / "workspace-input.schema.json"
        if schema_path.is_file():
            try:
                schema = json.loads(schema_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as exc:
                errors.append(f"invalid Workspace schema {schema_path.relative_to(ROOT)}: {exc}")
            else:
                if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
                    errors.append(f"Workspace schema must use JSON Schema 2020-12: {schema_path.relative_to(ROOT)}")
                expected_version = catalog.get(directory.name, {}).get("workspaceSchemaVersion")
                if schema.get("properties", {}).get("schemaVersion", {}).get("enum") != [expected_version]:
                    errors.append(f"Workspace schema version is out of sync for {directory.name}")


def validate_external_sources(errors: list[str]) -> None:
    catalog_path = ROOT / "external" / "catalog.yaml"
    workspace = ROOT / "skills" / "manage-focus-cycle" / "assets" / "focus-cycle-workspace.html"
    if not catalog_path.is_file() or not workspace.is_file():
        return
    catalog = catalog_path.read_text(encoding="utf-8")
    html_source = workspace.read_text(encoding="utf-8")
    pinned_url = "https://cdn.jsdelivr.net/npm/mermaid@11.16.1/dist/mermaid.esm.min.mjs"
    for required in ("version: 11.16.1", "license: MIT", pinned_url):
        if required not in catalog:
            errors.append(f"external Mermaid catalog is missing: {required}")
    if pinned_url not in html_source:
        errors.append("Workspace must use the cataloged, pinned Mermaid URL")
    if "mermaid@11/" in html_source:
        errors.append("Workspace must not use a moving Mermaid major-version URL")
    smoke_test = (ROOT / "scripts" / "smoke_install.py").read_text(encoding="utf-8")
    for required in ("distribution: npm:skills@1.5.22", "version: 1.5.22"):
        if required not in catalog:
            errors.append(f"external skills CLI catalog is missing: {required}")
    if 'SKILLS_CLI = "skills@1.5.22"' not in smoke_test:
        errors.append("installation smoke test must use the cataloged skills CLI version")


def validate_workflows(errors: list[str]) -> None:
    workflow_directory = ROOT / ".github" / "workflows"
    for path in sorted(workflow_directory.glob("*.yml")):
        text = path.read_text(encoding="utf-8")
        for action in re.findall(r"^\s*uses:\s*([^\s#]+)", text, re.MULTILINE):
            if action.startswith("./"):
                continue
            if "@" not in action or not re.fullmatch(r"[0-9a-f]{40}", action.rsplit("@", 1)[1]):
                errors.append(f"workflow action must be pinned to a full commit SHA: {path.relative_to(ROOT)}: {action}")

    release_path = workflow_directory / "release.yml"
    if release_path.is_file():
        release = release_path.read_text(encoding="utf-8")
        for required in ("gh auth status", "gh release create", "contents: write"):
            if required not in release:
                errors.append(f"Release workflow is missing authenticated GitHub operation: {required}")
        if re.search(r"\bcurl\b", release):
            errors.append("Release workflow must use authenticated gh instead of curl")


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
    validate_external_sources(errors)
    validate_workflows(errors)
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
