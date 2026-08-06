from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
SPEC = importlib.util.spec_from_file_location("validate_interaction", SCRIPT_DIR / "validate_interaction.py")
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC); sys.modules[SPEC.name] = VALIDATOR; SPEC.loader.exec_module(VALIDATOR)
TEMPLATE = ROOT / "templates" / "artifact.html"


class InteractionValidatorTests(unittest.TestCase):
    def modified(self, old: str, new: str):
        source=TEMPLATE.read_text(encoding="utf-8"); self.assertIn(old,source)
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"artifact.html"; path.write_text(source.replace(old,new,1),encoding="utf-8")
            return VALIDATOR.validate_file(path)

    def test_known_pattern_is_valid(self) -> None:
        result=VALIDATOR.validate_file(TEMPLATE); self.assertTrue(result.valid,result.as_json())

    def test_unknown_pattern_and_missing_component_fail(self) -> None:
        self.assertIn("HRI101",{x.code for x in self.modified('"name": "decide"','"name": "unknown"').errors})
        self.assertIn("HRI103",{x.code for x in self.modified('data-hra-component="evidence-list"','data-hra-component="other"').errors})

    def test_disallowed_action_and_too_few_options_fail(self) -> None:
        self.assertIn("HRI104",{x.code for x in self.modified('"allowedActions": ["select", "request-changes", "defer", "comment"]','"allowedActions": ["rank"]').errors})
        source=TEMPLATE.read_text(encoding="utf-8").replace('<label><input type="checkbox" data-interaction-option data-response-selection value="split-bundle"> 분리 bundle</label>',"")
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"artifact.html"; path.write_text(source,encoding="utf-8")
            self.assertIn("HRI105",{x.code for x in VALIDATOR.validate_file(path).errors})


if __name__ == "__main__": unittest.main()
