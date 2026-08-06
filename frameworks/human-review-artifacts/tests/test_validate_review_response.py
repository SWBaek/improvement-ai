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
SCRIPT_DIRECTORY = FRAMEWORK_ROOT / "scripts"
VALIDATOR_PATH = SCRIPT_DIRECTORY / "validate_review_response.py"
ARTIFACT_PATH = FRAMEWORK_ROOT / "examples" / "decision-review.html"
sys.path.insert(0, str(SCRIPT_DIRECTORY))
SPEC = importlib.util.spec_from_file_location("validate_review_response", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


def valid_payload() -> dict:
    return {
        "spec": "human-review-artifacts/review-response@0.1",
        "artifact": {
            "id": "artifact:example:decision-review",
            "spec": "human-review-artifacts/core@0.2",
            "revision": "r1",
        },
        "createdAt": "2026-08-06T01:00:00+09:00",
        "responses": [
            {
                "targetId": "review-delivery-format",
                "disposition": "selected",
                "selectionIds": ["single-html-manifest"],
            }
        ],
    }


class ReviewResponseValidatorTests(unittest.TestCase):
    def validate_payload(self, payload: object, artifact: Path | None = None):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "response.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            return VALIDATOR.validate_file(path, artifact)

    def test_valid_response_passes_schema_and_artifact_cross_check(self) -> None:
        result = self.validate_payload(valid_payload(), ARTIFACT_PATH)
        self.assertTrue(result.valid, result.as_json())

    def test_selected_requires_selection_and_comment_actions_require_comment(self) -> None:
        payload = valid_payload()
        payload["responses"][0].pop("selectionIds")
        result = self.validate_payload(payload)
        self.assertIn("HRR116", {item.code for item in result.errors})
        payload = valid_payload()
        payload["responses"][0] = {"targetId": "review-delivery-format", "disposition": "changes-requested"}
        result = self.validate_payload(payload)
        self.assertIn("HRR117", {item.code for item in result.errors})

    def test_duplicate_targets_are_rejected(self) -> None:
        payload = valid_payload()
        payload["responses"].append(dict(payload["responses"][0]))
        result = self.validate_payload(payload)
        self.assertIn("HRR118", {item.code for item in result.errors})

    def test_cross_check_rejects_stale_revision_target_and_selection(self) -> None:
        payload = valid_payload()
        payload["artifact"]["revision"] = "stale"
        payload["responses"][0]["targetId"] = "unknown-target"
        payload["responses"][0]["selectionIds"] = ["unknown-option"]
        result = self.validate_payload(payload, ARTIFACT_PATH)
        codes = {item.code for item in result.errors}
        self.assertTrue({"HRR202", "HRR203", "HRR204"}.issubset(codes), result.as_json())

    def test_cli_contract_and_missing_input_exit_code(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "response.json"
            path.write_text(json.dumps(valid_payload()), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), str(path), "--artifact", str(ARTIFACT_PATH), "--json"],
                cwd=REPOSITORY_ROOT,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertTrue(json.loads(completed.stdout)["valid"])
        missing = subprocess.run(
            [sys.executable, str(VALIDATOR_PATH), "does-not-exist.json", "--json"],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(2, missing.returncode)


if __name__ == "__main__":
    unittest.main()
