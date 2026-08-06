from __future__ import annotations

import importlib.util
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


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def skill_index(*rows: str) -> str:
    body = "\n".join(rows)
    return f"""# Skills

<!-- skill-index:start -->
| Skill | Status | Tracking |
|---|---|---|
{body}
<!-- skill-index:end -->
"""


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
            write(
                root / "skills" / "README.md",
                skill_index(
                    "| [sample-skill](sample-skill/SKILL.md) | In Progress | #1 |"
                ),
            )
            write(root / "skills" / "sample-skill" / "SKILL.md", VALID_SKILL)

            self.assertEqual([], self.run_validation(root))

    def test_unindexed_skill_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(root / "skills" / "README.md", skill_index())
            write(root / "skills" / "sample-skill" / "SKILL.md", VALID_SKILL)

            errors = self.run_validation(root)
            self.assertTrue(any("not registered" in error for error in errors))

    def test_duplicate_skill_index_entry_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            row = "| [sample-skill](sample-skill/SKILL.md) | Promoted | #1 |"
            write(root / "skills" / "README.md", skill_index(row, row))
            write(root / "skills" / "sample-skill" / "SKILL.md", VALID_SKILL)

            errors = self.run_validation(root)
            self.assertTrue(any("duplicate skill index" in error for error in errors))

    def test_invalid_frontmatter_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(
                root / "skills" / "README.md",
                skill_index(
                    "| [sample-skill](sample-skill/SKILL.md) | In Progress | #1 |"
                ),
            )
            write(root / "skills" / "sample-skill" / "SKILL.md", "# Missing frontmatter")

            errors = self.run_validation(root)
            self.assertTrue(any("invalid frontmatter" in error for error in errors))


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
