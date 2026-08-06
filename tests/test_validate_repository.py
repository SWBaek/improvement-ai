from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_repository.py"
SPEC = importlib.util.spec_from_file_location("validate_repository", SCRIPT_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


VALID_SKILL = """---
name: sample-skill
description: Use when a sample capability needs to be verified.
---

# Sample Skill
"""
VALID_LICENSE = "MIT test license\n"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def skill_index(*rows: str) -> str:
    body = "\n".join(rows)
    return f"""# Skills

<!-- skill-index:start -->
| Skill | Version | Status | Release | Tracking |
|---|---|---|---|---|
{body}
<!-- skill-index:end -->
"""


def catalog(version: str = "0.1.0") -> str:
    return json.dumps(
        {
            "schemaVersion": 1,
            "skills": [
                {
                    "name": "sample-skill",
                    "version": version,
                    "status": "In Progress",
                    "trackingIssue": 1,
                    "changelog": "docs/releases/sample-skill.md",
                    "support": {
                        "codex": "supported",
                        "otherAgentSkillsClients": "unverified",
                    },
                    "workspaceSchemaVersion": 1,
                }
            ],
        },
        indent=2,
    )


def index_row(version: str = "0.1.0") -> str:
    tag = f"sample-skill-v{version}"
    return (
        f"| [sample-skill](sample-skill/SKILL.md) | `{version}` | In Progress | "
        f"[{tag}](https://github.com/SWBaek/improvement-ai/releases/tag/{tag}) | "
        "[#1](https://github.com/SWBaek/improvement-ai/issues/1) |"
    )


def write_skill_environment(root: Path, rows: list[str], skill_text: str = VALID_SKILL, version: str = "0.1.0") -> None:
    write(root / "LICENSE", VALID_LICENSE)
    write(root / "skills" / "catalog.json", catalog(version))
    write(root / "skills" / "README.md", skill_index(*rows))
    write(root / "skills" / "sample-skill" / "SKILL.md", skill_text)
    write(root / "skills" / "sample-skill" / "LICENSE.txt", VALID_LICENSE)
    write(root / "docs" / "releases" / "sample-skill.md", f"# History\n\n## {version}\n")


def decision(number: str = "0001", include_result: bool = True) -> str:
    result = "\n## 결과\n\n결과를 기록한다.\n" if include_result else ""
    return f"""# {number}. Test decision

- 상태: Accepted
- 날짜: 2026-08-06

## 결정

결정을 기록한다.

## 이유

이유를 기록한다.
{result}"""


class SkillValidationTests(unittest.TestCase):
    def run_validation(self, root: Path) -> list[str]:
        errors: list[str] = []
        with patch.object(VALIDATOR, "ROOT", root):
            VALIDATOR.validate_skills(errors)
        return errors

    def test_valid_flat_skill_and_index_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_skill_environment(root, [index_row()])

            self.assertEqual([], self.run_validation(root))

    def test_unindexed_skill_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_skill_environment(root, [])

            errors = self.run_validation(root)
            self.assertTrue(any("missing from skills/README.md" in error for error in errors))

    def test_duplicate_skill_index_entry_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            row = index_row()
            write_skill_environment(root, [row, row])

            errors = self.run_validation(root)
            self.assertTrue(any("duplicate skill index" in error for error in errors))

    def test_invalid_frontmatter_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_skill_environment(root, [index_row()], skill_text="# Missing frontmatter")

            errors = self.run_validation(root)
            self.assertTrue(any("invalid frontmatter" in error for error in errors))

    def test_invalid_semver_and_license_drift_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_skill_environment(root, [index_row("01.0.0")], version="01.0.0")
            write(root / "skills" / "sample-skill" / "LICENSE.txt", "different\n")

            errors = self.run_validation(root)
            self.assertTrue(any("invalid Semantic Version" in error for error in errors))
            self.assertTrue(any("license differs" in error for error in errors))


class DecisionValidationTests(unittest.TestCase):
    def run_validation(self, root: Path) -> list[str]:
        errors: list[str] = []
        with patch.object(VALIDATOR, "ROOT", root):
            VALIDATOR.validate_decisions(errors)
        return errors

    def test_valid_decision_and_index_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            filename = "0001-test-decision.md"
            write(
                root / "docs" / "decisions" / "README.md",
                f"[0001]({filename})",
            )
            write(root / "docs" / "decisions" / filename, decision())

            self.assertEqual([], self.run_validation(root))

    def test_invalid_decision_name_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            filename = "invalid-name.md"
            write(root / "docs" / "decisions" / "README.md", "# Decisions")
            write(root / "docs" / "decisions" / filename, decision())

            errors = self.run_validation(root)
            self.assertTrue(any("numbered kebab-case" in error for error in errors))

    def test_missing_decision_section_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            filename = "0001-test-decision.md"
            write(
                root / "docs" / "decisions" / "README.md",
                f"[0001]({filename})",
            )
            write(
                root / "docs" / "decisions" / filename,
                decision(include_result=False),
            )

            errors = self.run_validation(root)
            self.assertTrue(any("## 결과" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
