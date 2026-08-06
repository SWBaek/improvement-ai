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
SCRIPT_DIR = ROOT / "scripts"
VALIDATOR_PATH = SCRIPT_DIR / "validate_review_response.py"
ARTIFACT = ROOT / "examples" / "decide-review.html"
sys.path.insert(0, str(SCRIPT_DIR))
SPEC = importlib.util.spec_from_file_location("validate_review_response", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC); sys.modules[SPEC.name] = VALIDATOR; SPEC.loader.exec_module(VALIDATOR)


def valid_payload() -> dict:
    return {"spec":"human-review-artifacts/review-response@0.2","artifact":{"id":"artifact:example:decide","spec":"human-review-artifacts/core@0.3","revision":"r2"},"interaction":{"pattern":{"name":"decide","version":"0.1"}},"createdAt":"2026-08-06T02:00:00+09:00","responses":[{"targetId":"decide-target","action":"select","selectionIds":["hybrid"]}]}


class ReviewResponseTests(unittest.TestCase):
    def validate(self, payload: object, artifact: Path | None = None):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "response.json"; path.write_text(json.dumps(payload), encoding="utf-8")
            return VALIDATOR.validate_file(path, artifact)

    def test_valid_response_roundtrip(self) -> None:
        result = self.validate(valid_payload(), ARTIFACT)
        self.assertTrue(result.valid, result.as_json())

    def test_rank_response_roundtrip(self) -> None:
        artifact = ROOT / "examples" / "compare-review.html"
        payload = {"spec":"human-review-artifacts/review-response@0.2","artifact":{"id":"artifact:example:compare","spec":"human-review-artifacts/core@0.3","revision":"r1"},"interaction":{"pattern":{"name":"compare","version":"0.1"}},"createdAt":"2026-08-06T02:00:00+09:00","responses":[{"targetId":"compare-target","action":"rank","rankingIds":["hybrid","cloud","external-ssd"]}]}
        result = self.validate(payload, artifact)
        self.assertTrue(result.valid, result.as_json())

    def test_action_payload_rules(self) -> None:
        payload = valid_payload(); payload["responses"][0] = {"targetId":"decide-target","action":"request-changes"}
        self.assertIn("HRR116", {x.code for x in self.validate(payload).errors})
        payload = valid_payload(); payload["responses"][0].pop("selectionIds")
        self.assertIn("HRR117", {x.code for x in self.validate(payload).errors})
        payload = valid_payload(); payload["responses"][0] = {"targetId":"decide-target","action":"rank","rankingIds":["hybrid"]}
        self.assertIn("HRR118", {x.code for x in self.validate(payload).errors})

    def test_duplicate_and_missing_required_targets(self) -> None:
        payload = valid_payload(); payload["responses"].append(dict(payload["responses"][0]))
        self.assertIn("HRR119", {x.code for x in self.validate(payload).errors})
        payload = valid_payload(); payload["responses"] = []
        self.assertIn("HRR207", {x.code for x in self.validate(payload, ARTIFACT).errors})

    def test_cross_check_rejects_stale_pattern_target_action_and_option(self) -> None:
        payload = valid_payload(); payload["artifact"]["revision"]="old"; payload["interaction"]["pattern"]["name"]="compare"; payload["responses"][0]={"targetId":"decide-target","action":"rank","rankingIds":["unknown","hybrid"]}
        codes = {x.code for x in self.validate(payload, ARTIFACT).errors}
        self.assertTrue({"HRR202","HRR205","HRR206","HRR204"}.issubset(codes), codes)

    def test_cli_and_missing_input(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"response.json"; path.write_text(json.dumps(valid_payload()),encoding="utf-8")
            completed=subprocess.run([sys.executable,str(VALIDATOR_PATH),str(path),"--artifact",str(ARTIFACT),"--json"],cwd=REPO,capture_output=True,text=True,encoding="utf-8")
            self.assertEqual(0,completed.returncode,completed.stderr); self.assertTrue(json.loads(completed.stdout)["valid"])
        missing=subprocess.run([sys.executable,str(VALIDATOR_PATH),"missing.json","--json"],cwd=REPO,capture_output=True,text=True)
        self.assertEqual(2,missing.returncode)


if __name__ == "__main__": unittest.main()
