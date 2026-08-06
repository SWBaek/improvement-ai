#!/usr/bin/env python3
"""Validate Human Review Artifacts Core 0.3 files."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


FRAMEWORK_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = FRAMEWORK_ROOT / "schemas" / "manifest-0.3.schema.json"
TEMPLATE_PATH = FRAMEWORK_ROOT / "templates" / "artifact.html"
CATALOG_PATH = FRAMEWORK_ROOT / "interactions" / "catalog-0.1.json"
CORE_SPEC = "human-review-artifacts/core@0.3"
CORE_VERSION = "0.3"
REQUIRED_SECTIONS = {"summary", "content", "interaction", "provenance"}
ARTIFACT_KINDS = {"fact", "assumption", "proposal", "decision", "question", "risk", "evidence"}
FORBIDDEN_ELEMENTS = {"iframe", "object", "embed"}
AUTOMATIC_URL_ATTRIBUTES = {
    "audio": ("src",), "img": ("src", "srcset"), "link": ("href",),
    "script": ("src",), "source": ("src", "srcset"), "video": ("src", "poster"),
}
CSP_BASELINE = {
    "default-src": {"'none'"}, "img-src": {"data:"},
    "style-src": {"'unsafe-inline'"}, "connect-src": {"'none'"},
    "font-src": {"data:"}, "object-src": {"'none'"},
    "base-uri": {"'none'"}, "form-action": {"'none'"},
}


@dataclass(frozen=True)
class Diagnostic:
    code: str
    message: str
    location: str


@dataclass
class ValidationResult:
    artifact: str
    specVersion: str | None
    errors: list[Diagnostic]
    warnings: list[Diagnostic]
    conformance: dict[str, Any]

    @property
    def valid(self) -> bool:
        return not self.errors

    def as_json(self) -> dict[str, Any]:
        return {
            "valid": self.valid, "artifact": self.artifact,
            "specVersion": self.specVersion, "conformance": self.conformance,
            "errors": [asdict(item) for item in self.errors],
            "warnings": [asdict(item) for item in self.warnings],
        }


class ArtifactParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.ids: list[str] = []
        self.html_langs: list[str] = []
        self.body_statuses: list[str] = []
        self.core_meta: list[str] = []
        self.csp_meta: list[str] = []
        self.manifest_parts: list[list[str]] = []
        self.executable_scripts: list[dict[str, Any]] = []
        self.styles: list[str] = []
        self.sections: list[tuple[str, str | None, bool]] = []
        self.main_roots = 0
        self.artifact_kinds: list[tuple[str, str | None]] = []
        self.interaction_targets: list[str | None] = []
        self.interaction_options: list[tuple[str | None, str, str | None]] = []
        self.components: list[tuple[str, str | None]] = []
        self.forbidden_elements: list[str] = []
        self.security_issues: list[tuple[str, str]] = []
        self.images_without_alt: list[str] = []
        self.svg_without_text: list[str] = []
        self.heading_levels: list[int] = []
        self.h1_texts: list[str] = []
        self.title_texts: list[str] = []
        self.manifest_field_texts: dict[str, list[str]] = {}
        self._capture: tuple[str, int] | None = None
        self._text_stack: list[tuple[str, str, str | None, list[str]]] = []
        self._svg_stack: list[dict[str, bool]] = []
        self._target_stack: list[tuple[str, str | None]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {key.lower(): value or "" for key, value in attrs}
        tag = tag.lower()
        element_id = attributes.get("id")
        if element_id:
            self.ids.append(element_id)
        if tag == "html":
            self.html_langs.append(attributes.get("lang", ""))
        elif tag == "body":
            self.body_statuses.append(attributes.get("data-artifact-status", ""))
        elif tag == "meta":
            if attributes.get("name", "").lower() == "human-review-artifact":
                self.core_meta.append(attributes.get("content", ""))
            if attributes.get("http-equiv", "").lower() == "content-security-policy":
                self.csp_meta.append(attributes.get("content", ""))
        elif tag == "main" and "data-artifact-root" in attributes:
            self.main_roots += 1
        elif tag == "section" and "data-artifact-section" in attributes:
            self.sections.append((attributes["data-artifact-section"], element_id, "hidden" in attributes))
        elif tag == "script":
            script_type = attributes.get("type", "").lower()
            if script_type == "application/json" and element_id == "artifact-manifest":
                self.manifest_parts.append([])
                self._capture = ("manifest", len(self.manifest_parts) - 1)
            elif script_type != "application/json":
                self.executable_scripts.append({"attrs": attributes, "parts": []})
                self._capture = ("script", len(self.executable_scripts) - 1)
        elif tag == "style":
            self.styles.append("")
            self._capture = ("style", len(self.styles) - 1)
        if tag == "title":
            self._text_stack.append((tag, "title", None, []))
        elif re.fullmatch(r"h[1-6]", tag):
            self.heading_levels.append(int(tag[1]))
            self._text_stack.append((tag, tag, None, []))
        if "data-manifest-field" in attributes:
            self._text_stack.append((tag, "manifest-field", attributes["data-manifest-field"], []))
        if "data-interaction-target" in attributes:
            self.interaction_targets.append(element_id)
            self._target_stack.append((tag, element_id))
        if "data-interaction-option" in attributes:
            target = self._target_stack[-1][1] if self._target_stack else None
            self.interaction_options.append((target, attributes.get("value", ""), element_id))
        if "data-hra-component" in attributes:
            self.components.append((attributes["data-hra-component"], element_id))
        kind = attributes.get("data-artifact-kind")
        if kind is not None:
            self.artifact_kinds.append((kind, element_id))
        if tag in FORBIDDEN_ELEMENTS:
            self.forbidden_elements.append(tag)
        for name, value in attributes.items():
            if name.startswith("on"):
                self.security_issues.append((f"{tag}[{name}]", "inline event handler"))
            if value.strip().lower().startswith("javascript:"):
                self.security_issues.append((f"{tag}[{name}]", "javascript URL"))
        if tag == "form" and "action" in attributes:
            self.security_issues.append(("form[action]", "form action"))
        if tag == "a":
            href = attributes.get("href", "")
            if href and not (href.startswith("#") or href.startswith("https://")):
                self.security_issues.append(("a[href]", f"unsupported link target {href!r}"))
            if attributes.get("target") == "_blank" and not {"noopener", "noreferrer"}.issubset(set(attributes.get("rel", "").split())):
                self.security_issues.append(("a[target=_blank]", "missing noopener noreferrer"))
        for name in AUTOMATIC_URL_ATTRIBUTES.get(tag, ()):
            value = attributes.get(name)
            if value and not (tag == "img" and name == "src" and value.startswith("data:")):
                self.security_issues.append((f"{tag}[{name}]", "external or automatic resource"))
        if tag == "img" and not attributes.get("alt"):
            self.images_without_alt.append(element_id or "img")
        if tag == "svg":
            self._svg_stack.append({"title": False, "desc": False})
        elif self._svg_stack and tag in {"title", "desc"}:
            self._svg_stack[-1][tag] = True

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style"}:
            self._capture = None
        while self._text_stack and self._text_stack[-1][0] == tag:
            _, kind, key, parts = self._text_stack.pop()
            value = "".join(parts).strip()
            if kind == "title":
                self.title_texts.append(value)
            elif kind == "h1":
                self.h1_texts.append(value)
            elif kind == "manifest-field" and key:
                self.manifest_field_texts.setdefault(key, []).append(value)
        if tag == "svg" and self._svg_stack:
            state = self._svg_stack.pop()
            if not (state["title"] and state["desc"]):
                self.svg_without_text.append("svg")
        if self._target_stack and tag == self._target_stack[-1][0]:
            self._target_stack.pop()

    def handle_data(self, data: str) -> None:
        if self._capture:
            kind, index = self._capture
            if kind == "manifest":
                self.manifest_parts[index].append(data)
            elif kind == "script":
                self.executable_scripts[index]["parts"].append(data)
            else:
                self.styles[index] += data
        for index in range(len(self._text_stack)):
            self._text_stack[index][3].append(data)


def add(items: list[Diagnostic], code: str, message: str, location: str) -> None:
    items.append(Diagnostic(code, message, location))


def matches_type(value: Any, expected: str | list[str]) -> bool:
    if isinstance(expected, list):
        return any(matches_type(value, item) for item in expected)
    mapping = {
        "array": list, "object": dict, "string": str, "integer": int,
        "number": (int, float), "boolean": bool,
    }
    if expected == "null":
        return value is None
    result = isinstance(value, mapping.get(expected, object))
    return result and not (expected in {"integer", "number"} and isinstance(value, bool))


def validate_format(value: str, format_name: str) -> bool:
    if format_name == "date-time":
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).tzinfo is not None
        except ValueError:
            return False
    if format_name == "uri":
        parsed = urlparse(value)
        return bool(parsed.scheme and (parsed.netloc or parsed.scheme in {"urn", "file"}))
    return True


def validate_schema_node(value: Any, schema: dict[str, Any], path: str, errors: list[Diagnostic], prefix: str = "HRA") -> None:
    expected = schema.get("type")
    if expected and not matches_type(value, expected):
        add(errors, f"{prefix}103", f"expected {expected}", path)
        return
    if "const" in schema and value != schema["const"]:
        add(errors, f"{prefix}104", f"must equal {schema['const']!r}", path)
    if "enum" in schema and value not in schema["enum"]:
        add(errors, f"{prefix}105", f"must be one of {schema['enum']}", path)
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0): add(errors, f"{prefix}106", "string is shorter than allowed", path)
        if len(value) > schema.get("maxLength", sys.maxsize): add(errors, f"{prefix}107", "string is longer than allowed", path)
        if schema.get("pattern") and not re.fullmatch(schema["pattern"], value): add(errors, f"{prefix}108", "string does not match pattern", path)
        if schema.get("format") and not validate_format(value, schema["format"]): add(errors, f"{prefix}109", f"invalid {schema['format']}", path)
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0): add(errors, f"{prefix}114", "array has fewer items than allowed", path)
        if schema.get("uniqueItems"):
            encoded = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in value]
            if len(encoded) != len(set(encoded)): add(errors, f"{prefix}110", "array items must be unique", path)
        if schema.get("items"):
            for index, item in enumerate(value): validate_schema_node(item, schema["items"], f"{path}[{index}]", errors, prefix)
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value: add(errors, f"{prefix}111", f"missing required property {key!r}", path)
        properties, additional = schema.get("properties", {}), schema.get("additionalProperties", True)
        for key, item in value.items():
            if schema.get("propertyNames"): validate_schema_node(key, schema["propertyNames"], f"{path}.<property-name>", errors, prefix)
            if key in properties: validate_schema_node(item, properties[key], f"{path}.{key}", errors, prefix)
            elif additional is False: add(errors, f"{prefix}112", f"unexpected property {key!r}", path)
            elif isinstance(additional, dict): validate_schema_node(item, additional, f"{path}.{key}", errors, prefix)


def parse_manifest(parser: ArtifactParser, errors: list[Diagnostic]) -> dict[str, Any] | None:
    if len(parser.manifest_parts) != 1:
        add(errors, "HRA101", "exactly one artifact Manifest is required", "head")
        return None
    try:
        value = json.loads("".join(parser.manifest_parts[0]))
    except json.JSONDecodeError as exc:
        add(errors, "HRA102", f"invalid Manifest JSON: {exc.msg}", "manifest")
        return None
    if not isinstance(value, dict):
        add(errors, "HRA103", "Manifest must be an object", "manifest")
        return None
    return value


def validate_manifest(manifest: dict[str, Any], errors: list[Diagnostic]) -> None:
    validate_schema_node(manifest, json.loads(SCHEMA_PATH.read_text(encoding="utf-8")), "manifest", errors)
    created, updated = manifest.get("createdAt"), manifest.get("updatedAt")
    if isinstance(created, str) and isinstance(updated, str):
        try:
            if datetime.fromisoformat(updated.replace("Z", "+00:00")) < datetime.fromisoformat(created.replace("Z", "+00:00")):
                add(errors, "HRA113", "updatedAt cannot be earlier than createdAt", "manifest.updatedAt")
        except ValueError:
            pass
    targets = manifest.get("interaction", {}).get("targets", [])
    ids = [item.get("id") for item in targets if isinstance(item, dict)]
    if len(ids) != len(set(ids)):
        add(errors, "HRA116", "interaction target ids must be unique", "manifest.interaction.targets")
    profiles = {item.get("name"): item.get("version") for item in manifest.get("profiles", []) if isinstance(item, dict)}
    for index, script in enumerate(manifest.get("runtime", {}).get("scripts", [])):
        if not isinstance(script, dict): continue
        if script.get("owner") == "core" and script.get("version") != CORE_VERSION:
            add(errors, "HRA118", "Core runtime version must match Core spec", f"manifest.runtime.scripts[{index}]")
        if script.get("owner") == "profile" and profiles.get(script.get("profile")) != script.get("version"):
            add(errors, "HRA119", "Profile runtime must match a declared Profile", f"manifest.runtime.scripts[{index}]")


def parse_csp(value: str) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for part in value.split(";"):
        tokens = part.strip().split()
        if tokens: result[tokens[0].lower()] = set(tokens[1:])
    return result


def digest(body: str) -> str:
    return "sha256-" + base64.b64encode(hashlib.sha256(body.encode("utf-8")).digest()).decode("ascii")


def reference_runtime_body() -> str | None:
    if not TEMPLATE_PATH.is_file(): return None
    parser = ArtifactParser(); parser.feed(TEMPLATE_PATH.read_text(encoding="utf-8")); parser.close()
    for script in parser.executable_scripts:
        if script["attrs"].get("data-artifact-runtime") == "core@0.3": return "".join(script["parts"])
    return None


def validate_document(parser: ArtifactParser, manifest: dict[str, Any] | None, errors: list[Diagnostic], warnings: list[Diagnostic]) -> None:
    if parser.core_meta != ["core@0.3"]: add(errors, "HRA201", "exactly one Core 0.3 meta declaration is required", "head")
    if len(parser.html_langs) != 1 or not parser.html_langs[0]: add(errors, "HRA202", "html must declare one non-empty lang", "html")
    if parser.main_roots != 1: add(errors, "HRA203", "exactly one main[data-artifact-root] is required", "main")
    duplicates = sorted(item for item, count in Counter(parser.ids).items() if count > 1)
    if duplicates: add(errors, "HRA204", f"duplicate ids: {', '.join(duplicates)}", "document")
    names = [name for name, _, _ in parser.sections]
    missing = sorted(REQUIRED_SECTIONS - set(names))
    if missing: add(errors, "HRA205", f"missing required sections: {', '.join(missing)}", "main")
    dup_sections = sorted(item for item, count in Counter(names).items() if count > 1)
    if dup_sections: add(errors, "HRA206", f"duplicate sections: {', '.join(dup_sections)}", "main")
    for name, section_id, hidden in parser.sections:
        if not section_id: add(errors, "HRA207", f"section {name!r} requires id", "main")
        if hidden: add(errors, "HRA208", f"section {name!r} cannot be hidden", section_id or "section")
    if len(parser.h1_texts) != 1 or not parser.h1_texts[0]: add(errors, "HRA209", "exactly one non-empty h1 is required", "document")
    for previous, current in zip(parser.heading_levels, parser.heading_levels[1:]):
        if current > previous + 1:
            add(errors, "HRA210", f"heading level jumps from h{previous} to h{current}", "document"); break
    for kind, element_id in parser.artifact_kinds:
        if kind not in ARTIFACT_KINDS: add(errors, "HRA211", f"unknown artifact kind {kind!r}", element_id or "document")
    if parser.images_without_alt: add(errors, "HRA212", "images require non-empty alt text", ", ".join(parser.images_without_alt))
    if parser.svg_without_text: add(errors, "HRA213", "svg requires title and desc", "svg")
    for target in parser.interaction_targets:
        if not target: add(errors, "HRA221", "data-interaction-target requires id", "[data-interaction-target]")
    for component, element_id in parser.components:
        if not component or not element_id: add(errors, "HRA229", "data-hra-component requires a value and id", element_id or "[data-hra-component]")
    options_by_target: dict[str | None, list[str]] = {}
    for target, value, _ in parser.interaction_options: options_by_target.setdefault(target, []).append(value)
    if any(not value for values in options_by_target.values() for value in values): add(errors, "HRA222", "interaction option requires non-empty value", "[data-interaction-option]")
    if None in options_by_target: add(errors, "HRA224", "interaction options must be inside a target", "[data-interaction-option]")
    for target, values in options_by_target.items():
        duplicates = sorted(item for item, count in Counter(values).items() if item and count > 1)
        if duplicates: add(errors, "HRA223", f"duplicate option values in {target}: {', '.join(duplicates)}", "[data-interaction-option]")
    if not manifest: return
    if manifest.get("spec") != CORE_SPEC: add(errors, "HRA214", f"unsupported Core spec {manifest.get('spec')!r}", "manifest.spec")
    if parser.html_langs and manifest.get("language") != parser.html_langs[0]: add(errors, "HRA215", "Manifest language does not match html lang", "html[lang]")
    if len(parser.title_texts) != 1 or manifest.get("title") != parser.title_texts[0]: add(errors, "HRA216", "Manifest title does not match title", "title")
    if len(parser.h1_texts) == 1 and manifest.get("title") != parser.h1_texts[0]: add(errors, "HRA217", "Manifest title does not match h1", "h1")
    if len(parser.body_statuses) != 1 or manifest.get("status") != parser.body_statuses[0]: add(errors, "HRA218", "Manifest status does not match body", "body")
    for field in ("status", "revision"):
        values = parser.manifest_field_texts.get(field, [])
        if len(values) != 1 or values[0] != manifest.get(field): add(errors, "HRA220" if field == "status" else "HRA225", f"visible {field} does not match Manifest", field)
    declared = {item.get("id") for item in manifest.get("interaction", {}).get("targets", []) if isinstance(item, dict)}
    actual = {item for item in parser.interaction_targets if item}
    if declared != actual: add(errors, "HRA226", "Manifest targets must exactly match data-interaction-target ids", "manifest.interaction.targets")
    known = {(item["name"], item["version"]) for item in json.loads(CATALOG_PATH.read_text(encoding="utf-8"))["patterns"]}
    pattern = manifest.get("interaction", {}).get("pattern", {})
    if (pattern.get("name"), pattern.get("version")) not in known: add(warnings, "HRA901", "unknown Interaction Pattern; Core remains independently valid", "manifest.interaction.pattern")


def validate_security(parser: ArtifactParser, manifest: dict[str, Any] | None, errors: list[Diagnostic], warnings: list[Diagnostic]) -> str:
    for location, issue in parser.security_issues: add(errors, "HRA301", issue, location)
    if parser.forbidden_elements: add(errors, "HRA302", f"forbidden elements: {', '.join(parser.forbidden_elements)}", "document")
    if len(parser.csp_meta) != 1:
        add(errors, "HRA308", "exactly one Content-Security-Policy meta is required", "head"); return "invalid"
    csp = parse_csp(parser.csp_meta[0])
    for directive, required in CSP_BASELINE.items():
        if csp.get(directive) != required: add(errors, "HRA309", f"CSP {directive} must equal {sorted(required)}", "CSP")
    declared = {item.get("id"): item for item in (manifest or {}).get("runtime", {}).get("scripts", []) if isinstance(item, dict)}
    actual_ids: set[str] = set(); runtime_kind = "none"
    expected_hashes: set[str] = set()
    reference = reference_runtime_body()
    for script in parser.executable_scripts:
        attrs, body = script["attrs"], "".join(script["parts"])
        script_id = attrs.get("id")
        if not script_id or script_id not in declared:
            add(errors, "HRA304", "executable script must be declared", script_id or "script"); continue
        actual_ids.add(script_id)
        actual_digest = digest(body); expected_hashes.add(f"'{actual_digest}'")
        if declared[script_id].get("digest") != actual_digest: add(errors, "HRA307", "script digest mismatch", script_id)
        runtime = attrs.get("data-artifact-runtime", "")
        if declared[script_id].get("owner") == "core":
            runtime_kind = "core"
            if runtime != "core@0.3" or reference is None or body != reference: add(errors, "HRA310", "Core runtime does not match Core 0.3 reference runtime", script_id)
        else:
            runtime_kind = "profile"; add(warnings, "HRA902", "Profile runtime behavior is not verified by Core", script_id)
    if set(declared) != actual_ids: add(errors, "HRA305", "declared runtime scripts must exactly match executable scripts", "manifest.runtime")
    actual_hashes = {item for item in csp.get("script-src", set()) if item.startswith("'sha256-")}
    if expected_hashes != actual_hashes: add(errors, "HRA309", "CSP script hashes do not match executable scripts", "CSP")
    return runtime_kind


def validate_file(path: Path) -> ValidationResult:
    errors: list[Diagnostic] = []; warnings: list[Diagnostic] = []
    parser = ArtifactParser(); parser.feed(path.read_text(encoding="utf-8")); parser.close()
    manifest = parse_manifest(parser, errors)
    if manifest: validate_manifest(manifest, errors)
    validate_document(parser, manifest, errors, warnings)
    runtime = validate_security(parser, manifest, errors, warnings)
    return ValidationResult(str(path), manifest.get("spec") if manifest else None, errors, warnings, {
        "core": "valid" if not errors else "invalid", "runtime": runtime,
        "interaction": manifest.get("interaction", {}).get("pattern") if manifest else None,
        "profiles": (manifest or {}).get("profiles", []),
    })


def render_human(result: ValidationResult) -> str:
    lines = [f"{'VALID' if result.valid else 'INVALID'}: {result.artifact}"]
    lines += [f"ERROR {item.code} [{item.location}] {item.message}" for item in result.errors]
    lines += [f"WARN  {item.code} [{item.location}] {item.message}" for item in result.warnings]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("artifact", type=Path); parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if not args.artifact.is_file():
        message = f"input file not found: {args.artifact}"
        if args.json: print(json.dumps({"valid": False, "artifact": str(args.artifact), "errors": [{"code": "HRA001", "message": message, "location": "input"}], "warnings": []}))
        else: print(message, file=sys.stderr)
        return 2
    try: result = validate_file(args.artifact)
    except (OSError, UnicodeError) as exc:
        print(f"cannot read input: {exc}", file=sys.stderr); return 2
    print(json.dumps(result.as_json(), ensure_ascii=False, indent=2) if args.json else render_human(result))
    return 0 if result.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
