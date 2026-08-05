from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


FRAMEWORK_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = FRAMEWORK_ROOT.parents[1]
VALIDATOR_PATH = FRAMEWORK_ROOT / "scripts" / "validate_artifact.py"
TEMPLATE_PATH = FRAMEWORK_ROOT / "templates" / "artifact.html"
EXAMPLES = sorted((FRAMEWORK_ROOT / "examples").glob("*.html"))
FIXTURES = FRAMEWORK_ROOT / "tests" / "fixtures"

SPEC = importlib.util.spec_from_file_location("validate_artifact", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


class ArtifactValidatorTests(unittest.TestCase):
    def assert_has_error(self, path: Path, code: str) -> None:
        result = VALIDATOR.validate_file(path)
        self.assertIn(code, {item.code for item in result.errors}, result.as_json())

    def validate_modified_template(self, old: str, new: str):
        source = TEMPLATE_PATH.read_text(encoding="utf-8")
        self.assertIn(old, source)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "artifact.html"
            path.write_text(source.replace(old, new, 1), encoding="utf-8")
            return VALIDATOR.validate_file(path)

    def test_reference_template_is_valid(self) -> None:
        result = VALIDATOR.validate_file(TEMPLATE_PATH)
        self.assertTrue(result.valid, result.as_json())

    def test_examples_are_valid(self) -> None:
        self.assertGreaterEqual(len(EXAMPLES), 2)
        for path in EXAMPLES:
            with self.subTest(path=path.name):
                result = VALIDATOR.validate_file(path)
                self.assertTrue(result.valid, result.as_json())

    def test_missing_manifest_is_reported(self) -> None:
        self.assert_has_error(FIXTURES / "missing-manifest.html", "HRA101")

    def test_schema_errors_are_reported(self) -> None:
        self.assert_has_error(FIXTURES / "invalid-schema.html", "HRA111")

    def test_unsafe_content_is_reported(self) -> None:
        result = VALIDATOR.validate_file(FIXTURES / "unsafe-content.html")
        codes = {item.code for item in result.errors}
        self.assertIn("HRA301", codes)
        self.assertIn("HRA302", codes)

    def test_duplicate_id_is_reported(self) -> None:
        result = self.validate_modified_template('id="content"', 'id="summary"')
        self.assertIn("HRA204", {item.code for item in result.errors})

    def test_manifest_and_visible_title_must_match(self) -> None:
        result = self.validate_modified_template("<title>Human Review Artifact</title>", "<title>Different title</title>")
        self.assertIn("HRA216", {item.code for item in result.errors})

    def test_manifest_and_visible_status_must_match(self) -> None:
        result = self.validate_modified_template(
            '<strong data-manifest-field="status">draft</strong>',
            '<strong data-manifest-field="status">accepted</strong>',
        )
        self.assertIn("HRA220", {item.code for item in result.errors})

    def test_review_mode_requires_review_section(self) -> None:
        source = TEMPLATE_PATH.read_text(encoding="utf-8")
        start = source.index('      <section id="review-request"')
        end = source.index('      <section id="provenance"', start)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "artifact.html"
            path.write_text(source[:start] + source[end:], encoding="utf-8")
            result = VALIDATOR.validate_file(path)
        self.assertIn("HRA219", {item.code for item in result.errors})

    def test_runtime_change_breaks_csp_hash(self) -> None:
        result = self.validate_modified_template('const manifest = JSON.parse', 'const manifest = JSON.parse /* tampered */')
        self.assertIn("HRA309", {item.code for item in result.errors})

    def test_runtime_cannot_be_replaced_even_with_matching_csp(self) -> None:
        source = TEMPLATE_PATH.read_text(encoding="utf-8")
        tampered = source.replace(
            'const manifest = JSON.parse',
            'const manifest = JSON.parse /* tampered */',
            1,
        )
        parser = VALIDATOR.ArtifactParser()
        parser.feed(tampered)
        runtime = "".join(parser.runtime_parts[0]).encode("utf-8")
        import base64
        import hashlib

        digest = base64.b64encode(hashlib.sha256(runtime).digest()).decode("ascii")
        tampered = tampered.replace(
            "LwlSJfZzUimSkcsvNPpB8SVEJIVVRhefs/WoUbDWHy4=",
            digest,
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "artifact.html"
            path.write_text(tampered, encoding="utf-8")
            result = VALIDATOR.validate_file(path)
        self.assertIn("HRA310", {item.code for item in result.errors})

    def test_updated_at_cannot_precede_created_at(self) -> None:
        result = self.validate_modified_template(
            '"updatedAt": "2026-08-06T00:00:00+09:00"',
            '"updatedAt": "2026-08-05T00:00:00+09:00"',
        )
        self.assertIn("HRA113", {item.code for item in result.errors})

    def test_unknown_profile_warns_without_invalidating_core(self) -> None:
        result = self.validate_modified_template(
            '"profiles": []',
            '"profiles": [{"name": "future-profile", "version": "0.1"}]',
        )
        self.assertTrue(result.valid, result.as_json())
        self.assertIn("HRA901", {item.code for item in result.warnings})

    def test_json_cli_contract_and_exit_code(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(VALIDATOR_PATH), str(TEMPLATE_PATH), "--json"],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["valid"])
        self.assertEqual("human-review-artifacts/core@0.1", payload["specVersion"])
        self.assertEqual([], payload["errors"])

    def test_invalid_cli_uses_exit_code_one(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(VALIDATOR_PATH), str(FIXTURES / "missing-manifest.html"), "--json"],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(1, completed.returncode)
        self.assertFalse(json.loads(completed.stdout)["valid"])

    def test_missing_input_uses_exit_code_two(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(VALIDATOR_PATH), "does-not-exist.html", "--json"],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(2, completed.returncode)


if __name__ == "__main__":
    unittest.main()
