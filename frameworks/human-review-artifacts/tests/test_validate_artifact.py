from __future__ import annotations

import base64
import hashlib
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

    def validate_source(self, source: str):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "artifact.html"
            path.write_text(source, encoding="utf-8")
            return VALIDATOR.validate_file(path)

    def validate_modified_template(self, old: str, new: str):
        source = TEMPLATE_PATH.read_text(encoding="utf-8")
        self.assertIn(old, source)
        return self.validate_source(source.replace(old, new, 1))

    def test_reference_template_is_valid(self) -> None:
        result = VALIDATOR.validate_file(TEMPLATE_PATH)
        self.assertTrue(result.valid, result.as_json())
        self.assertEqual("core", result.conformance["runtime"])

    def test_interactive_and_static_examples_are_valid(self) -> None:
        self.assertGreaterEqual(len(EXAMPLES), 2)
        results = [VALIDATOR.validate_file(path) for path in EXAMPLES]
        self.assertTrue(all(item.valid for item in results), [item.as_json() for item in results])
        self.assertEqual({"core", "none"}, {item.conformance["runtime"] for item in results})

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

    def test_manifest_title_status_and_revision_must_match_visible_values(self) -> None:
        cases = [
            ("<title>Human Review Artifact</title>", "<title>Different title</title>", "HRA216"),
            ('data-manifest-field="status">draft', 'data-manifest-field="status">accepted', "HRA220"),
            ('data-manifest-field="revision">r1', 'data-manifest-field="revision">r2', "HRA225"),
        ]
        for old, new, code in cases:
            with self.subTest(code=code):
                result = self.validate_modified_template(old, new)
                self.assertIn(code, {item.code for item in result.errors})

    def test_review_mode_requires_target_and_matching_item(self) -> None:
        result = self.validate_modified_template('"targets": ["review-core"]', '"targets": []')
        self.assertIn("HRA116", {item.code for item in result.errors})
        result = self.validate_modified_template('"targets": ["review-core"]', '"targets": ["missing-target"]')
        self.assertIn("HRA226", {item.code for item in result.errors})

    def test_review_options_must_be_unique_and_nested(self) -> None:
        result = self.validate_modified_template('value="compare-alternatives"', 'value="clarify-evidence"')
        self.assertIn("HRA223", {item.code for item in result.errors})
        result = self.validate_modified_template('data-review-option value="clarify-evidence"', 'data-review-option value=""')
        self.assertIn("HRA222", {item.code for item in result.errors})

    def test_core_runtime_tamper_breaks_digest_reference_and_csp(self) -> None:
        result = self.validate_modified_template("const manifest = JSON.parse", "const manifest = JSON.parse /* tampered */")
        codes = {item.code for item in result.errors}
        self.assertTrue({"HRA307", "HRA309", "HRA310"}.issubset(codes), result.as_json())

    def test_undeclared_script_is_rejected(self) -> None:
        result = self.validate_modified_template("</body>", '<script id="extra">void 0;</script>\n</body>')
        self.assertIn("HRA304", {item.code for item in result.errors})

    def test_unknown_profile_runtime_warns_without_invalidating_core(self) -> None:
        source = TEMPLATE_PATH.read_text(encoding="utf-8")
        body = '(() => { "use strict"; })();'
        digest = "sha256-" + base64.b64encode(hashlib.sha256(body.encode()).digest()).decode("ascii")
        source = source.replace(
            '"profiles": [],',
            '"profiles": [{"name": "future-profile", "version": "0.1"}],',
            1,
        )
        source = source.replace(
            '      {\n        "id": "artifact-runtime",\n        "owner": "core",\n        "version": "0.2",\n        "digest": "sha256-TjxWU3h1KXnnD44jodr7cK4FcLVLh9rUJtsWTG9psIY="\n      }',
            '      {\n        "id": "artifact-runtime",\n        "owner": "core",\n        "version": "0.2",\n        "digest": "sha256-TjxWU3h1KXnnD44jodr7cK4FcLVLh9rUJtsWTG9psIY="\n      },\n'
            f'      {{"id": "future-runtime", "owner": "profile", "profile": "future-profile", "version": "0.1", "digest": "{digest}"}}',
            1,
        )
        source = source.replace(
            "script-src 'sha256-TjxWU3h1KXnnD44jodr7cK4FcLVLh9rUJtsWTG9psIY='",
            f"script-src 'sha256-TjxWU3h1KXnnD44jodr7cK4FcLVLh9rUJtsWTG9psIY=' '{digest}'",
            1,
        )
        source = source.replace("</body>", f'<script id="future-runtime" data-artifact-runtime="profile:future-profile@0.1">{body}</script>\n</body>')
        result = self.validate_source(source)
        self.assertTrue(result.valid, result.as_json())
        self.assertEqual("profile", result.conformance["runtime"])
        self.assertTrue({"HRA901", "HRA902"}.issubset({item.code for item in result.warnings}))

    def test_updated_at_cannot_precede_created_at(self) -> None:
        result = self.validate_modified_template(
            '"updatedAt": "2026-08-06T00:00:00+09:00"',
            '"updatedAt": "2026-08-05T00:00:00+09:00"',
        )
        self.assertIn("HRA113", {item.code for item in result.errors})

    def test_json_cli_contract_and_exit_codes(self) -> None:
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
        self.assertEqual("human-review-artifacts/core@0.2", payload["specVersion"])
        self.assertEqual("valid", payload["conformance"]["core"])
        invalid = subprocess.run(
            [sys.executable, str(VALIDATOR_PATH), str(FIXTURES / "missing-manifest.html"), "--json"],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(1, invalid.returncode)
        missing = subprocess.run(
            [sys.executable, str(VALIDATOR_PATH), "does-not-exist.html", "--json"],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(2, missing.returncode)


if __name__ == "__main__":
    unittest.main()
