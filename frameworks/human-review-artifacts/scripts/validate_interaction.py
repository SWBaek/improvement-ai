#!/usr/bin/env python3
"""Validate a Core 0.3 Artifact against its declared Interaction Pattern."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from validate_artifact import ArtifactParser, Diagnostic, parse_manifest, validate_file as validate_core


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "interactions" / "catalog-0.1.json"


@dataclass
class InteractionResult:
    artifact: str
    pattern: dict[str, str] | None
    errors: list[Diagnostic]

    @property
    def valid(self) -> bool: return not self.errors
    def as_json(self) -> dict[str, Any]: return {"valid": self.valid, "artifact": self.artifact, "pattern": self.pattern, "errors": [asdict(x) for x in self.errors]}


def validate_file(path: Path) -> InteractionResult:
    errors: list[Diagnostic] = []
    core = validate_core(path)
    if not core.valid:
        errors.append(Diagnostic("HRI201", "Artifact is not Core 0.3 valid", "artifact")); return InteractionResult(str(path), None, errors)
    parser = ArtifactParser(); parser.feed(path.read_text(encoding="utf-8")); parser.close()
    manifest = parse_manifest(parser, []) or {}; declared = manifest.get("interaction", {}).get("pattern")
    patterns = {(p["name"], p["version"]): p for p in json.loads(CATALOG.read_text(encoding="utf-8"))["patterns"]}
    key = (declared.get("name"), declared.get("version")) if isinstance(declared, dict) else (None, None)
    contract = patterns.get(key)
    if not contract:
        errors.append(Diagnostic("HRI101", "unknown Interaction Pattern", "manifest.interaction.pattern")); return InteractionResult(str(path), declared, errors)
    components = [name for name, _ in parser.components]
    duplicates = sorted(name for name, count in Counter(components).items() if count > 1)
    if duplicates: errors.append(Diagnostic("HRI102", f"duplicate components: {', '.join(duplicates)}", "[data-hra-component]"))
    missing = sorted(set(contract["requiredComponents"]) - set(components))
    if missing: errors.append(Diagnostic("HRI103", f"missing required components: {', '.join(missing)}", "main"))
    allowed = set(contract["allowedActions"])
    for index, target in enumerate(manifest["interaction"]["targets"]):
        invalid = sorted(set(target["allowedActions"]) - allowed)
        if invalid: errors.append(Diagnostic("HRI104", f"actions not allowed by {key[0]}: {', '.join(invalid)}", f"manifest.interaction.targets[{index}]"))
    if key[0] in {"compare", "decide"}:
        for target in parser.interaction_targets:
            count = len([value for owner, value, _ in parser.interaction_options if owner == target and value])
            if count < 2: errors.append(Diagnostic("HRI105", f"{key[0]} target requires at least two options", target or "target"))
    return InteractionResult(str(path), declared, errors)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("artifact", type=Path); parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if not args.artifact.is_file(): print(f"input file not found: {args.artifact}", file=sys.stderr); return 2
    result = validate_file(args.artifact)
    if args.json: print(json.dumps(result.as_json(), ensure_ascii=False, indent=2))
    else:
        print(f"{'VALID' if result.valid else 'INVALID'}: {result.artifact}")
        for item in result.errors: print(f"ERROR {item.code} [{item.location}] {item.message}")
    return 0 if result.valid else 1


if __name__ == "__main__": raise SystemExit(main())
