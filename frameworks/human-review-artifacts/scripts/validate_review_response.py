#!/usr/bin/env python3
"""Validate Human Review Artifacts Review Response 0.2 JSON."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from validate_artifact import ArtifactParser, Diagnostic, parse_manifest, validate_file as validate_artifact_file, validate_schema_node


FRAMEWORK_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = FRAMEWORK_ROOT / "schemas" / "review-response-0.2.schema.json"
COMMENT_REQUIRED = {"answer", "comment", "request-changes", "challenge"}


@dataclass
class ResponseValidationResult:
    response: str
    errors: list[Diagnostic]
    warnings: list[Diagnostic]

    @property
    def valid(self) -> bool:
        return not self.errors

    def as_json(self) -> dict[str, Any]:
        return {"valid": self.valid, "response": self.response, "errors": [asdict(x) for x in self.errors], "warnings": [asdict(x) for x in self.warnings]}


def add(errors: list[Diagnostic], code: str, message: str, location: str) -> None:
    errors.append(Diagnostic(code, message, location))


def validate_semantics(payload: dict[str, Any], errors: list[Diagnostic]) -> None:
    responses = payload.get("responses")
    if not isinstance(responses, list): return
    targets: list[str] = []
    for index, response in enumerate(responses):
        if not isinstance(response, dict): continue
        target = response.get("targetId")
        if isinstance(target, str): targets.append(target)
        action, comment = response.get("action"), response.get("comment")
        if action in COMMENT_REQUIRED and not (isinstance(comment, str) and comment.strip()):
            add(errors, "HRR116", f"{action} action requires comment", f"response.responses[{index}]")
        if action == "select" and not response.get("selectionIds"):
            add(errors, "HRR117", "select action requires selectionIds", f"response.responses[{index}]")
        if action == "rank" and (not isinstance(response.get("rankingIds"), list) or len(response["rankingIds"]) < 2):
            add(errors, "HRR118", "rank action requires at least two rankingIds", f"response.responses[{index}]")
    duplicates = sorted(item for item, count in __import__("collections").Counter(targets).items() if count > 1)
    if duplicates: add(errors, "HRR119", f"duplicate target responses: {', '.join(duplicates)}", "response.responses")


def cross_validate(payload: dict[str, Any], artifact_path: Path, errors: list[Diagnostic]) -> None:
    artifact_result = validate_artifact_file(artifact_path)
    if not artifact_result.valid:
        add(errors, "HRR201", "referenced Artifact is not Core 0.3 valid", "artifact"); return
    parser = ArtifactParser(); parser.feed(artifact_path.read_text(encoding="utf-8")); parser.close()
    manifest_errors: list[Diagnostic] = []; manifest = parse_manifest(parser, manifest_errors)
    if not manifest:
        add(errors, "HRR201", "referenced Artifact has no readable Manifest", "artifact"); return
    reference = payload.get("artifact", {})
    for field in ("id", "spec", "revision"):
        if reference.get(field) != manifest.get(field): add(errors, "HRR202", f"Artifact {field} does not match", f"response.artifact.{field}")
    if payload.get("interaction", {}).get("pattern") != manifest.get("interaction", {}).get("pattern"):
        add(errors, "HRR205", "Interaction Pattern does not match", "response.interaction.pattern")
    declared = {item["id"]: item for item in manifest["interaction"]["targets"]}
    options: dict[str, set[str]] = {}
    for target, value, _ in parser.interaction_options:
        if target and value: options.setdefault(target, set()).add(value)
    seen: set[str] = set()
    for index, response in enumerate(payload.get("responses", [])):
        if not isinstance(response, dict): continue
        target, action = response.get("targetId"), response.get("action"); seen.add(target)
        if target not in declared:
            add(errors, "HRR203", f"unknown interaction target {target!r}", f"response.responses[{index}].targetId"); continue
        if action not in declared[target]["allowedActions"]:
            add(errors, "HRR206", f"action {action!r} is not allowed for {target!r}", f"response.responses[{index}].action")
        for field in ("selectionIds", "rankingIds"):
            for value in response.get(field, []) if isinstance(response.get(field), list) else []:
                if value not in options.get(target, set()): add(errors, "HRR204", f"unknown option {value!r} for target {target!r}", f"response.responses[{index}].{field}")
    missing = sorted(item["id"] for item in manifest["interaction"]["targets"] if item["required"] and item["id"] not in seen)
    if missing: add(errors, "HRR207", f"missing required target responses: {', '.join(missing)}", "response.responses")


def validate_file(path: Path, artifact_path: Path | None = None) -> ResponseValidationResult:
    errors: list[Diagnostic] = []; warnings: list[Diagnostic] = []
    try: payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add(errors, "HRR102", f"invalid Response JSON: {exc.msg}", "response"); return ResponseValidationResult(str(path), errors, warnings)
    if not isinstance(payload, dict):
        add(errors, "HRR103", "Review Response must be an object", "response"); return ResponseValidationResult(str(path), errors, warnings)
    validate_schema_node(payload, json.loads(SCHEMA_PATH.read_text(encoding="utf-8")), "response", errors, prefix="HRR")
    validate_semantics(payload, errors)
    if artifact_path: cross_validate(payload, artifact_path, errors)
    return ResponseValidationResult(str(path), errors, warnings)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("response", type=Path); parser.add_argument("--artifact", type=Path); parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    missing = next((p for p in (args.response, args.artifact) if p is not None and not p.is_file()), None)
    if missing:
        message = f"input file not found: {missing}"
        if args.json: print(json.dumps({"valid": False, "response": str(args.response), "errors": [{"code": "HRR001", "message": message, "location": "input"}], "warnings": []}))
        else: print(message, file=sys.stderr)
        return 2
    result = validate_file(args.response, args.artifact)
    if args.json: print(json.dumps(result.as_json(), ensure_ascii=False, indent=2))
    else:
        print(f"{'VALID' if result.valid else 'INVALID'}: {result.response}")
        for item in result.errors: print(f"ERROR {item.code} [{item.location}] {item.message}")
        for item in result.warnings: print(f"WARN  {item.code} [{item.location}] {item.message}")
    return 0 if result.valid else 1


if __name__ == "__main__": raise SystemExit(main())
