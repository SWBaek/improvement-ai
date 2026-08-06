from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "release_skills.py"
SPEC = importlib.util.spec_from_file_location("release_skills", SCRIPT_PATH)
assert SPEC and SPEC.loader
RELEASE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = RELEASE
SPEC.loader.exec_module(RELEASE)


def run_git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, text=True, encoding="utf-8", capture_output=True, check=True
    ).stdout.strip()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def catalog(version: str) -> str:
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
                    "support": {"codex": "supported", "otherAgentSkillsClients": "unverified"},
                    "workspaceSchemaVersion": 1,
                }
            ],
        }
    )


class SemanticVersionTests(unittest.TestCase):
    def test_release_and_prerelease_order(self) -> None:
        self.assertLess(RELEASE.Version.parse("0.1.0-alpha.2"), RELEASE.Version.parse("0.1.0-alpha.10"))
        self.assertLess(RELEASE.Version.parse("0.1.0-rc.1"), RELEASE.Version.parse("0.1.0"))
        self.assertLess(RELEASE.Version.parse("0.1.0"), RELEASE.Version.parse("0.2.0"))

    def test_invalid_versions_fail(self) -> None:
        for value in ("1", "01.0.0", "1.0.0-01"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                RELEASE.Version.parse(value)


class ReleaseChangeTests(unittest.TestCase):
    def test_initial_release_and_missing_followup_bump(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            run_git(root, "init")
            run_git(root, "config", "user.email", "test@example.com")
            run_git(root, "config", "user.name", "Test")
            write(root / "skills" / "sample-skill" / "SKILL.md", "initial\n")
            run_git(root, "add", ".")
            run_git(root, "commit", "-m", "base")
            base = run_git(root, "rev-parse", "HEAD")

            write(root / "skills" / "sample-skill" / "SKILL.md", "release content\n")
            write(root / "skills" / "catalog.json", catalog("0.1.0"))
            write(root / "docs" / "releases" / "sample-skill.md", "# History\n\n## 0.1.0\n\nInitial.\n")
            run_git(root, "add", ".")
            run_git(root, "commit", "-m", "release")
            release_commit = run_git(root, "rev-parse", "HEAD")

            with patch.object(RELEASE, "ROOT", root):
                releases = RELEASE.evaluate_changes(base, release_commit, merge_base=False)
            self.assertEqual(
                [{"skill": "sample-skill", "version": "0.1.0", "tag": "sample-skill-v0.1.0"}],
                releases,
            )

            write(root / "skills" / "sample-skill" / "SKILL.md", "unversioned change\n")
            run_git(root, "add", ".")
            run_git(root, "commit", "-m", "missing bump")
            head = run_git(root, "rev-parse", "HEAD")
            with patch.object(RELEASE, "ROOT", root), self.assertRaisesRegex(
                ValueError, "requires a higher catalog version"
            ):
                RELEASE.evaluate_changes(release_commit, head, merge_base=False)

    def test_release_notes_extract_only_requested_version(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "history.md"
            write(path, "# History\n\n## 0.2.0\n\nNew.\n\n## 0.1.0\n\nOld.\n")
            self.assertEqual("New.", RELEASE.extract_release_section(path, "0.2.0"))


if __name__ == "__main__":
    unittest.main()
