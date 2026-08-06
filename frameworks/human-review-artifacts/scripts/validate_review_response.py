#!/usr/bin/env python3
"""Validate Human Review Artifacts Review Response 0.1 JSON."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from validate_artifact import (
    ArtifactParser,
    Diagnostic,
    parse_manifest,
    validate_file as validate_artifact_file,
    validate_schema_node,
)


FRAMEWORK_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = FRAMEWORK_ROOT / "schemas" / "review-response-0.1.schema.json"


@dataclass
class ResponseValidationResult:
    response: str
    errors: list[Diagnostic]
    warnings: list[Diagnostic]

    @property
    def valid(self) -> bool:
        return not self.errors

    def as_json(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "response": self.response,
            "errors": [asdict(item) for item in self.errors],
            "warnings": [asdict(item) for item in self.warnings],
        }


def add(errors: list[Diagnostic], code: str, message: str, location: str) -> None:
    errors.append(Diagnostic(code, message, location))


def validate_semantics(payload: dict[str, Any], errors: list[Diagnostic]) -> None:
    responses = payload.get("responses")
    if not isinstance(responses, list):
        return
    target_ids: list[str] = []
    for index, response in enumerate(responses):
        if not isinstance(response, dict):
            continue
        target = response.get("targetId")
        if isinstance(target, str):
            target_ids.append(target)
        disposition = response.get("disposition")
        selections = response.get("selectionIds")
        comment = response.get("comment")
        if disposition == "selected" and (not isinstance(selections, list) or not selections):
            add(errors, "HRR116", "selected disposition requires at least one selectionId", f"response.responses[{index}]")
        if disposition in {"commented", "changes-requested"} and not (isinstance(comment, str) and comment.strip()):
            add(errors, "HRR117", f"{disposition} disposition requires comment", f"response.responses[{index}]")
    duplicates = sorted({item for item in target_ids if target_ids.count(item) > 1})
    if duplicates:
        add(errors, "HRR118", f"duplicate target responses: {', '.join(duplicates)}", "response.responses")


def cross_validate(payload: dict[str, Any], artifact_path: Path, errors: list[Diagnostic]) -> None:
    artifact_result = validate_artifact_file(artifact_path)
    if not artifact_result.valid:
        add(errors, "HRR201", "referenced Artifact is not Core 0.2 valid", "artifact")
        return
    parser = ArtifactParser()
    parser.feed(artifact_path.read_text(encoding="utf-8"))
    parser.close()
    manifest_errors: list[Diagnostic] = []
    manifest = parse_manifest(parser, manifest_errors)
    if not manifest:
        add(errors, "HRR201", "referenced Artifact has no readable Manifest", "artifact")
        return
    reference = payload.get("artifact")
    if isinstance(reference, dict):
        for field in ("id", "spec", "revision"):
            if reference.get(field) != manifest.get(field):
                add(errors, "HRR202", f"Artifact {field} does not match", f"response.artifact.{field}")
    targets = set(manifest.get("review", {}).get("targets", []))
    options_by_target: dict[str, set[str]] = {}
    for target, value, _ in parser.review_options:
        if target and value:
            options_by_target.setdefault(target, set()).add(value)
    for index, response in enumerate(payload.get("responses", [])):
        if not isinstance(response, dict):
            continue
        target = response.get("targetId")
        if target not in targets:
            add(errors, "HRR203", f"unknown review target {target!r}", f"response.responses[{index}].targetId")
        for selection in response.get("selectionIds", []) if isinstance(response.get("selectionIds"), list) else []:
            if selection not in options_by_target.get(target, set()):
                add(errors, "HRR204", f"unknown selection {selection!r} for target {target!r}", f"response.responses[{index}].selectionIds")


def validate_file(path: Path, artifact_path: Path | None = None) -> ResponseValidationResult:
    errors: list[Diagnostic] = []
    warnings: list[Diagnostic] = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add(errors, "HRR102", f"invalid Response JSON: {exc.msg}", f"response:{exc.lineno}:{exc.colno}")
        return ResponseValidationResult(str(path), errors, warnings)
    if not isinstance(payload, dict):
        add(errors, "HRR103", "Review Response must be an object", "response")
        return ResponseValidationResult(str(path), errors, warnings)
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validate_schema_node(payload, schema, "response", errors, prefix="HRR")
    validate_semantics(payload, errors)
    if artifact_path:
        cross_validate(payload, artifact_path, errors)
    return ResponseValidationResult(str(path), errors, warnings)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("response", type=Path)
    parser.add_argument("--artifact", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    missing = next((path for path in (args.response, args.artifact) if path is not None and not path.is_file()), None)
    if missing:
        message = f"input file not found: {missing}"
        if args.as_json:
            print(json.dumps({"valid": False, "response": str(args.response), "errors": [{"code": "HRR001", "message": message, "location": "input"}], "warnings": []}, ensure_ascii=False))
        else:
            print(message, file=sys.stderr)
        return 2
    try:
        result = validate_file(args.response, args.artifact)
    except (OSError, UnicodeError) as exc:
        message = f"cannot read input: {exc}"
        if args.as_json:
            print(json.dumps({"valid": False, "response": str(args.response), "errors": [{"code": "HRR002", "message": message, "location": "input"}], "warnings": []}, ensure_ascii=False))
        else:
            print(message, file=sys.stderr)
        return 2
    if args.as_json:
        print(json.dumps(result.as_json(), ensure_ascii=False, indent=2))
    else:
        print(f"{'VALID' if result.valid else 'INVALID'}: {result.response}")
        for item in result.errors:
            print(f"ERROR {item.code} [{item.location}] {item.message}")
        for item in result.warnings:
            print(f"WARN  {item.code} [{item.location}] {item.message}")
    return 0 if result.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
