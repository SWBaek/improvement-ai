from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_artifact.py"
INTERACTION_PATH = ROOT / "scripts" / "validate_interaction.py"
TEMPLATE = ROOT / "templates" / "artifact.html"
EXAMPLES = sorted((ROOT / "examples").glob("*.html"))
FIXTURES = ROOT / "tests" / "fixtures"

SPEC = importlib.util.spec_from_file_location("validate_artifact", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC); sys.modules[SPEC.name] = VALIDATOR; SPEC.loader.exec_module(VALIDATOR)
sys.path.insert(0, str(ROOT / "scripts"))
ISPEC = importlib.util.spec_from_file_location("validate_interaction", INTERACTION_PATH)
assert ISPEC and ISPEC.loader
INTERACTION = importlib.util.module_from_spec(ISPEC); sys.modules[ISPEC.name] = INTERACTION; ISPEC.loader.exec_module(INTERACTION)


class ArtifactValidatorTests(unittest.TestCase):
    def validate_source(self, source: str):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "artifact.html"; path.write_text(source, encoding="utf-8")
            return VALIDATOR.validate_file(path)

    def modified(self, old: str, new: str):
        source = TEMPLATE.read_text(encoding="utf-8"); self.assertIn(old, source)
        return self.validate_source(source.replace(old, new, 1))

    def test_template_and_five_examples_are_core_and_pattern_valid(self) -> None:
        self.assertTrue(VALIDATOR.validate_file(TEMPLATE).valid)
        self.assertEqual(5, len(EXAMPLES))
        for path in EXAMPLES:
            with self.subTest(path=path.name):
                self.assertTrue(VALIDATOR.validate_file(path).valid, VALIDATOR.validate_file(path).as_json())
                self.assertTrue(INTERACTION.validate_file(path).valid, INTERACTION.validate_file(path).as_json())

    def test_missing_manifest_and_schema_errors_are_reported(self) -> None:
        self.assertIn("HRA101", {x.code for x in VALIDATOR.validate_file(FIXTURES / "missing-manifest.html").errors})
        self.assertIn("HRA111", {x.code for x in VALIDATOR.validate_file(FIXTURES / "invalid-schema.html").errors})

    def test_unsafe_content_is_reported(self) -> None:
        codes = {x.code for x in VALIDATOR.validate_file(FIXTURES / "unsafe-content.html").errors}
        self.assertTrue({"HRA301", "HRA302"}.issubset(codes))

    def test_identity_fields_and_target_contract_are_visible(self) -> None:
        self.assertIn("HRA204", {x.code for x in self.modified('id="content"', 'id="summary"').errors})
        self.assertIn("HRA216", {x.code for x in self.modified("<title>Human Review Artifact</title>", "<title>Changed</title>").errors})
        self.assertIn("HRA220", {x.code for x in self.modified('data-manifest-field="status">draft', 'data-manifest-field="status">accepted').errors})
        self.assertIn("HRA225", {x.code for x in self.modified('data-manifest-field="revision">r1', 'data-manifest-field="revision">r2').errors})
        self.assertIn("HRA226", {x.code for x in self.modified('"id": "decision-target"', '"id": "missing-target"').errors})

    def test_options_are_non_empty_unique_and_target_scoped(self) -> None:
        self.assertIn("HRA222", {x.code for x in self.modified('value="single-file"', 'value=""').errors})
        self.assertIn("HRA223", {x.code for x in self.modified('value="split-bundle"', 'value="single-file"').errors})
        self.assertIn("HRA224", {x.code for x in self.modified('<fieldset id="decision-target" data-interaction-target data-hra-component="response-panel">', '<fieldset id="decision-target" data-hra-component="response-panel">').errors})

    def test_unknown_pattern_warns_but_core_remains_valid(self) -> None:
        result = self.modified('"name": "decide"', '"name": "future-pattern"')
        self.assertTrue(result.valid, result.as_json())
        self.assertIn("HRA901", {x.code for x in result.warnings})

    def test_runtime_tamper_and_undeclared_script_are_rejected(self) -> None:
        result = self.modified("const manifest = JSON.parse", "const manifest = JSON.parse /* tampered */")
        self.assertTrue({"HRA307", "HRA309", "HRA310"}.issubset({x.code for x in result.errors}))
        result = self.modified("</body>", '<script id="extra">void 0;</script></body>')
        self.assertIn("HRA304", {x.code for x in result.errors})

    def test_updated_at_order_and_cli_contract(self) -> None:
        result = self.modified('"updatedAt": "2026-08-06T00:00:00+09:00"', '"updatedAt": "2026-08-05T00:00:00+09:00"')
        self.assertIn("HRA113", {x.code for x in result.errors})
        completed = subprocess.run([sys.executable, str(VALIDATOR_PATH), str(TEMPLATE), "--json"], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual("human-review-artifacts/core@0.3", json.loads(completed.stdout)["specVersion"])
        missing = subprocess.run([sys.executable, str(VALIDATOR_PATH), "missing.html", "--json"], cwd=REPO, capture_output=True, text=True)
        self.assertEqual(2, missing.returncode)


if __name__ == "__main__": unittest.main()
