#!/usr/bin/env python3
"""Validate Skill version changes and prepare deterministic GitHub Release data."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = "skills/catalog.json"
SEMVER = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
REPOSITORY = "SWBaek/improvement-ai"


@dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int
    prerelease: tuple[str, ...]

    @classmethod
    def parse(cls, value: str) -> "Version":
        match = SEMVER.fullmatch(value)
        if not match:
            raise ValueError(f"invalid Semantic Version: {value}")
        prerelease = tuple(match.group(4).split(".")) if match.group(4) else ()
        for identifier in prerelease:
            if identifier.isdigit() and len(identifier) > 1 and identifier.startswith("0"):
                raise ValueError(f"numeric prerelease identifiers must not have leading zeroes: {value}")
        return cls(int(match.group(1)), int(match.group(2)), int(match.group(3)), prerelease)

    def __lt__(self, other: "Version") -> bool:
        core = (self.major, self.minor, self.patch)
        other_core = (other.major, other.minor, other.patch)
        if core != other_core:
            return core < other_core
        if not self.prerelease:
            return False
        if not other.prerelease:
            return True
        for left, right in zip(self.prerelease, other.prerelease):
            if left == right:
                continue
            if left.isdigit() and right.isdigit():
                return int(left) < int(right)
            if left.isdigit() != right.isdigit():
                return left.isdigit()
            return left < right
        return len(self.prerelease) < len(other.prerelease)


def run_git(*args: str, allow_failure: bool = False) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=False
    )
    if result.returncode and not allow_failure:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout


def catalog_entries(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["name"]: item for item in payload.get("skills", [])}


def read_catalog_at(ref: str) -> dict[str, dict[str, Any]]:
    raw = run_git("show", f"{ref}:{CATALOG_PATH}", allow_failure=True)
    if not raw:
        return {}
    return catalog_entries(json.loads(raw))


def changed_files(base: str, head: str, merge_base: bool) -> set[str]:
    separator = "..." if merge_base else ".."
    return {line.strip().replace("\\", "/") for line in run_git("diff", "--name-only", f"{base}{separator}{head}").splitlines() if line.strip()}


def changed_skill_names(files: set[str]) -> set[str]:
    names: set[str] = set()
    for path in files:
        parts = path.split("/")
        if len(parts) >= 3 and parts[0] == "skills" and parts[1] not in {"catalog.json", "README.md"}:
            names.add(parts[1])
    return names


def version_bumps(before: dict[str, dict[str, Any]], after: dict[str, dict[str, Any]]) -> dict[str, str]:
    bumps: dict[str, str] = {}
    for name, current in after.items():
        current_text = current["version"]
        current_version = Version.parse(current_text)
        previous = before.get(name)
        if previous is None:
            bumps[name] = current_text
            continue
        previous_version = Version.parse(previous["version"])
        if current_text != previous["version"]:
            if not previous_version < current_version:
                raise ValueError(f"{name} version must increase: {previous['version']} -> {current_text}")
            bumps[name] = current_text
    return bumps


def evaluate_changes(base: str, head: str, merge_base: bool) -> list[dict[str, str]]:
    before = read_catalog_at(base)
    after = read_catalog_at(head)
    files = changed_files(base, head, merge_base)
    changed_skills = changed_skill_names(files)
    bumps = version_bumps(before, after)
    errors: list[str] = []

    for name in sorted(changed_skills):
        if name not in after:
            errors.append(f"changed Skill is absent from catalog: {name}")
        elif name not in bumps:
            errors.append(f"changed Skill requires a higher catalog version: {name}")

    for name, version in sorted(bumps.items()):
        if name not in changed_skills:
            errors.append(f"version changed without Skill content change: {name} {version}")
            continue
        changelog = after[name]["changelog"]
        if changelog not in files:
            errors.append(f"release history must change with {name} {version}: {changelog}")

    if errors:
        raise ValueError("\n".join(errors))

    return [
        {"skill": name, "version": version, "tag": f"{name}-v{version}"}
        for name, version in sorted(bumps.items())
    ]


def extract_release_section(path: Path, version: str) -> str:
    text = path.read_text(encoding="utf-8")
    heading = re.compile(rf"^##\s+{re.escape(version)}\s*$", re.MULTILINE)
    match = heading.search(text)
    if not match:
        raise ValueError(f"release history has no section for {version}: {path}")
    next_heading = re.search(r"^##\s+\S.*$", text[match.end():], re.MULTILINE)
    end = match.end() + next_heading.start() if next_heading else len(text)
    return text[match.end():end].strip()


def build_notes(skill: str, version: str) -> str:
    catalog = catalog_entries(json.loads((ROOT / CATALOG_PATH).read_text(encoding="utf-8")))
    if skill not in catalog or catalog[skill]["version"] != version:
        raise ValueError(f"catalog does not declare {skill} {version}")
    section = extract_release_section(ROOT / catalog[skill]["changelog"], version)
    tag = f"{skill}-v{version}"
    prerelease = " prerelease" if Version.parse(version).prerelease else ""
    return f"""{section}

## Install

```powershell
npx skills@latest add {REPOSITORY} --skill {skill} --agent codex -y
```

## Update

```powershell
npx skills@latest update {skill} --project -y
```

## Reproducible install / rollback

```powershell
npx skills@latest add https://github.com/{REPOSITORY}/tree/{tag}/skills/{skill} --agent codex -y
```

Codex is the supported client for this{prerelease} release. Other Agent Skills clients are unverified.
"""


def write_github_outputs(path: Path, releases: list[dict[str, str]]) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(f"has_releases={'true' if releases else 'false'}\n")
        stream.write(f"releases={json.dumps(releases, separators=(',', ':'))}\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("check-changes", help="Enforce version and release-history changes")
    check.add_argument("--base", required=True)
    check.add_argument("--head", default="HEAD")

    detect = subparsers.add_parser("detect", help="Detect releases between two pushed commits")
    detect.add_argument("--before", required=True)
    detect.add_argument("--after", required=True)
    detect.add_argument("--github-output", type=Path)

    notes = subparsers.add_parser("notes", help="Build GitHub Release notes")
    notes.add_argument("--skill", required=True)
    notes.add_argument("--version", required=True)
    notes.add_argument("--output", required=True, type=Path)

    args = parser.parse_args()
    try:
        if args.command == "check-changes":
            releases = evaluate_changes(args.base, args.head, merge_base=True)
            print(json.dumps(releases, indent=2))
        elif args.command == "detect":
            releases = evaluate_changes(args.before, args.after, merge_base=False)
            if args.github_output:
                write_github_outputs(args.github_output, releases)
            print(json.dumps(releases, indent=2))
        else:
            notes_text = build_notes(args.skill, args.version)
            args.output.write_text(notes_text, encoding="utf-8", newline="\n")
            print(args.output)
        return 0
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError, KeyError) as exc:
        print(f"release error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
