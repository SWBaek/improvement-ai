#!/usr/bin/env python3
"""Validate Human Review Artifacts Core 0.1 files."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


FRAMEWORK_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = FRAMEWORK_ROOT / "schemas" / "manifest-0.1.schema.json"
TEMPLATE_PATH = FRAMEWORK_ROOT / "templates" / "artifact.html"
CORE_SPEC = "human-review-artifacts/core@0.1"
CORE_VERSION = "0.1"
REQUIRED_SECTIONS = {"summary", "content", "provenance"}
REVIEW_MODES = {"comment", "decide", "approve"}
ARTIFACT_KINDS = {
    "fact",
    "assumption",
    "proposal",
    "decision",
    "question",
    "risk",
    "evidence",
}
FORBIDDEN_ELEMENTS = {"iframe", "object", "embed"}
AUTOMATIC_URL_ATTRIBUTES = {
    "audio": ("src",),
    "img": ("src", "srcset"),
    "link": ("href",),
    "script": ("src",),
    "source": ("src", "srcset"),
    "video": ("src", "poster"),
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

    @property
    def valid(self) -> bool:
        return not self.errors

    def as_json(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "artifact": self.artifact,
            "specVersion": self.specVersion,
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
        self.runtime_parts: list[list[str]] = []
        self.executable_scripts: list[dict[str, str]] = []
        self.sections: list[tuple[str, str | None, bool]] = []
        self.main_roots = 0
        self.artifact_kinds: list[tuple[str, str | None]] = []
        self.forbidden_elements: list[str] = []
        self.security_issues: list[tuple[str, str]] = []
        self.images_without_alt: list[str] = []
        self.svg_without_text: list[str] = []
        self.heading_levels: list[int] = []
        self.h1_texts: list[str] = []
        self.title_texts: list[str] = []
        self.manifest_field_texts: dict[str, list[str]] = {}
        self.styles: list[str] = []
        self._capture: str | None = None
        self._capture_index = -1
        self._text_stack: list[tuple[str, str | None, list[str]]] = []
        self._svg_stack: list[dict[str, bool]] = []

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
            name = attributes.get("name", "").lower()
            equiv = attributes.get("http-equiv", "").lower()
            if name == "human-review-artifact":
                self.core_meta.append(attributes.get("content", ""))
            if equiv == "content-security-policy":
                self.csp_meta.append(attributes.get("content", ""))
        elif tag == "main" and "data-artifact-root" in attributes:
            self.main_roots += 1
        elif tag == "section" and "data-artifact-section" in attributes:
            self.sections.append(
                (
                    attributes["data-artifact-section"],
                    element_id,
                    "hidden" in attributes,
                )
            )
        elif tag == "script":
            script_type = attributes.get("type", "").lower()
            if script_type == "application/json" and element_id == "artifact-manifest":
                self.manifest_parts.append([])
                self._capture = "manifest"
                self._capture_index = len(self.manifest_parts) - 1
            else:
                self.executable_scripts.append(attributes)
                if element_id == "artifact-runtime":
                    self.runtime_parts.append([])
                    self._capture = "runtime"
                    self._capture_index = len(self.runtime_parts) - 1
        elif tag == "style":
            self.styles.append("")
            self._capture = "style"
            self._capture_index = len(self.styles) - 1
        elif tag == "title":
            self._text_stack.append(("title", None, []))
        elif re.fullmatch(r"h[1-6]", tag):
            level = int(tag[1])
            self.heading_levels.append(level)
            self._text_stack.append((tag, None, []))
        elif "data-manifest-field" in attributes:
            self._text_stack.append(("manifest-field", attributes["data-manifest-field"], []))

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
            if attributes.get("target") == "_blank":
                rel = set(attributes.get("rel", "").split())
                if not {"noopener", "noreferrer"}.issubset(rel):
                    self.security_issues.append(("a[target=_blank]", "missing noopener noreferrer"))

        if tag in AUTOMATIC_URL_ATTRIBUTES:
            for name in AUTOMATIC_URL_ATTRIBUTES[tag]:
                value = attributes.get(name)
                if not value:
                    continue
                if tag == "img" and name == "src" and value.startswith("data:"):
                    continue
                self.security_issues.append((f"{tag}[{name}]", "external or automatic resource"))

        if tag == "img" and not attributes.get("alt"):
            self.images_without_alt.append(element_id or "img")

        if tag == "svg":
            self._svg_stack.append({"title": False, "desc": False})
        elif self._svg_stack and tag in {"title", "desc"}:
            self._svg_stack[-1][tag] = True

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "script" and self._capture in {"manifest", "runtime"}:
            self._capture = None
            self._capture_index = -1
        elif tag == "style" and self._capture == "style":
            self._capture = None
            self._capture_index = -1

        if self._text_stack and (
            tag == self._text_stack[-1][0]
            or (self._text_stack[-1][0] == "manifest-field" and tag not in {"span", "strong", "time"})
        ):
            kind, key, parts = self._text_stack.pop()
            text = "".join(parts).strip()
            if kind == "title":
                self.title_texts.append(text)
            elif kind == "h1":
                self.h1_texts.append(text)
            elif kind == "manifest-field" and key:
                self.manifest_field_texts.setdefault(key, []).append(text)

        if tag == "svg" and self._svg_stack:
            state = self._svg_stack.pop()
            if not (state["title"] and state["desc"]):
                self.svg_without_text.append("svg")

    def handle_data(self, data: str) -> None:
        if self._capture == "manifest":
            self.manifest_parts[self._capture_index].append(data)
        elif self._capture == "runtime":
            self.runtime_parts[self._capture_index].append(data)
        elif self._capture == "style":
            self.styles[self._capture_index] += data
        if self._text_stack:
            self._text_stack[-1][2].append(data)


def add(errors: list[Diagnostic], code: str, message: str, location: str) -> None:
    errors.append(Diagnostic(code, message, location))


def matches_type(value: Any, expected: str) -> bool:
    return {
        "array": isinstance(value, list),
        "object": isinstance(value, dict),
        "string": isinstance(value, str),
    }.get(expected, True)


def validate_format(value: str, format_name: str) -> bool:
    if format_name == "date-time":
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return False
        return parsed.tzinfo is not None
    if format_name == "uri":
        parsed = urlparse(value)
        return bool(parsed.scheme and (parsed.netloc or parsed.scheme == "urn"))
    return True


def validate_schema_node(
    value: Any,
    schema: dict[str, Any],
    path: str,
    errors: list[Diagnostic],
) -> None:
    expected_type = schema.get("type")
    if expected_type and not matches_type(value, expected_type):
        add(errors, "HRA103", f"expected {expected_type}", path)
        return

    if "const" in schema and value != schema["const"]:
        add(errors, "HRA104", f"must equal {schema['const']!r}", path)
    if "enum" in schema and value not in schema["enum"]:
        add(errors, "HRA105", f"must be one of {schema['enum']}", path)

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            add(errors, "HRA106", "string is shorter than allowed", path)
        if len(value) > schema.get("maxLength", sys.maxsize):
            add(errors, "HRA107", "string is longer than allowed", path)
        pattern = schema.get("pattern")
        if pattern and not re.fullmatch(pattern, value):
            add(errors, "HRA108", f"does not match {pattern!r}", path)
        format_name = schema.get("format")
        if format_name and not validate_format(value, format_name):
            add(errors, "HRA109", f"is not a valid {format_name}", path)

    if isinstance(value, list):
        if schema.get("uniqueItems"):
            serialized = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in value]
            if len(serialized) != len(set(serialized)):
                add(errors, "HRA110", "array items must be unique", path)
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                validate_schema_node(item, item_schema, f"{path}[{index}]", errors)

    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                add(errors, "HRA111", f"missing required property {key!r}", path)

        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        property_names = schema.get("propertyNames")
        for key, item in value.items():
            if property_names:
                validate_schema_node(key, property_names, f"{path}.<property-name>", errors)
            if key in properties:
                validate_schema_node(item, properties[key], f"{path}.{key}", errors)
            elif additional is False:
                add(errors, "HRA112", f"unexpected property {key!r}", path)
            elif isinstance(additional, dict):
                validate_schema_node(item, additional, f"{path}.{key}", errors)


def parse_manifest(parser: ArtifactParser, errors: list[Diagnostic]) -> dict[str, Any] | None:
    if len(parser.manifest_parts) != 1:
        add(errors, "HRA101", "exactly one artifact Manifest is required", "head")
        return None
    raw = "".join(parser.manifest_parts[0])
    try:
        manifest = json.loads(raw)
    except json.JSONDecodeError as exc:
        add(errors, "HRA102", f"invalid Manifest JSON: {exc.msg}", f"manifest:{exc.lineno}:{exc.colno}")
        return None
    if not isinstance(manifest, dict):
        add(errors, "HRA103", "Manifest must be an object", "manifest")
        return None
    return manifest


def validate_manifest(manifest: dict[str, Any], errors: list[Diagnostic]) -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validate_schema_node(manifest, schema, "manifest", errors)
    created = manifest.get("createdAt")
    updated = manifest.get("updatedAt")
    if isinstance(created, str) and isinstance(updated, str):
        try:
            created_at = datetime.fromisoformat(created.replace("Z", "+00:00"))
            updated_at = datetime.fromisoformat(updated.replace("Z", "+00:00"))
            if updated_at < created_at:
                add(errors, "HRA113", "updatedAt cannot be earlier than createdAt", "manifest.updatedAt")
        except (TypeError, ValueError):
            pass


def validate_document(
    parser: ArtifactParser,
    manifest: dict[str, Any] | None,
    errors: list[Diagnostic],
    warnings: list[Diagnostic],
) -> None:
    if parser.core_meta != ["core@0.1"]:
        add(errors, "HRA201", "exactly one Core 0.1 meta declaration is required", "head")
    if len(parser.html_langs) != 1 or not parser.html_langs[0]:
        add(errors, "HRA202", "html must declare one non-empty lang", "html")
    if parser.main_roots != 1:
        add(errors, "HRA203", "exactly one main[data-artifact-root] is required", "main")

    duplicate_ids = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
    if duplicate_ids:
        add(errors, "HRA204", f"duplicate ids: {', '.join(duplicate_ids)}", "document")

    section_names = [name for name, _, _ in parser.sections]
    missing = sorted(REQUIRED_SECTIONS - set(section_names))
    if missing:
        add(errors, "HRA205", f"missing required sections: {', '.join(missing)}", "main")
    duplicate_sections = sorted({item for item in section_names if section_names.count(item) > 1})
    if duplicate_sections:
        add(errors, "HRA206", f"duplicate sections: {', '.join(duplicate_sections)}", "main")
    for name, section_id, hidden in parser.sections:
        if not section_id:
            add(errors, "HRA207", f"section {name!r} requires an id", "main")
        if hidden:
            add(errors, "HRA208", f"section {name!r} cannot be hidden in source", section_id or "section")

    if len(parser.h1_texts) != 1 or not parser.h1_texts[0]:
        add(errors, "HRA209", "exactly one non-empty h1 is required", "document")
    if parser.heading_levels:
        for previous, current in zip(parser.heading_levels, parser.heading_levels[1:]):
            if current > previous + 1:
                add(errors, "HRA210", f"heading level jumps from h{previous} to h{current}", "document")
                break

    for kind, element_id in parser.artifact_kinds:
        if kind not in ARTIFACT_KINDS:
            add(errors, "HRA211", f"unknown artifact kind {kind!r}", element_id or "document")

    if parser.images_without_alt:
        add(errors, "HRA212", "images require non-empty alt text", ", ".join(parser.images_without_alt))
    if parser.svg_without_text:
        add(errors, "HRA213", "svg requires title and desc", "svg")

    if manifest:
        spec = manifest.get("spec")
        if spec != CORE_SPEC:
            add(errors, "HRA214", f"unsupported Core spec {spec!r}", "manifest.spec")
        if parser.html_langs and manifest.get("language") != parser.html_langs[0]:
            add(errors, "HRA215", "Manifest language does not match html lang", "html[lang]")
        if len(parser.title_texts) != 1 or manifest.get("title") != parser.title_texts[0]:
            add(errors, "HRA216", "Manifest title does not match title element", "title")
        if len(parser.h1_texts) == 1 and manifest.get("title") != parser.h1_texts[0]:
            add(errors, "HRA217", "Manifest title does not match visible h1", "h1")
        if len(parser.body_statuses) != 1 or manifest.get("status") != parser.body_statuses[0]:
            add(errors, "HRA218", "Manifest status does not match body status", "body")
        visible_statuses = parser.manifest_field_texts.get("status", [])
        if len(visible_statuses) != 1 or manifest.get("status") != visible_statuses[0]:
            add(errors, "HRA220", "Manifest status does not match visible status", "[data-manifest-field=status]")
        mode = manifest.get("review", {}).get("mode") if isinstance(manifest.get("review"), dict) else None
        if mode in REVIEW_MODES and "review-request" not in section_names:
            add(errors, "HRA219", f"review mode {mode!r} requires review-request", "main")
        profiles = manifest.get("profiles", [])
        if isinstance(profiles, list):
            known_profiles = {path.name for path in (FRAMEWORK_ROOT / "profiles").iterdir() if path.is_dir()}
            for profile in profiles:
                if isinstance(profile, dict) and profile.get("name") not in known_profiles:
                    warnings.append(Diagnostic("HRA901", f"unknown profile {profile.get('name')!r}", "manifest.profiles"))


def validate_security(
    parser: ArtifactParser,
    errors: list[Diagnostic],
) -> None:
    if parser.forbidden_elements:
        add(errors, "HRA301", f"forbidden elements: {', '.join(sorted(set(parser.forbidden_elements)))}", "document")
    for location, issue in parser.security_issues:
        add(errors, "HRA302", issue, location)

    for index, style in enumerate(parser.styles):
        for match in re.finditer(r"url\((.*?)\)", style, re.IGNORECASE | re.DOTALL):
            target = match.group(1).strip(" \t\r\n\"'")
            if not target.startswith("data:"):
                add(errors, "HRA303", f"style contains non-data URL {target!r}", f"style[{index}]")

    if len(parser.executable_scripts) != 1:
        add(errors, "HRA304", "exactly one executable Core runtime script is required", "document")
    else:
        runtime = parser.executable_scripts[0]
        if runtime.get("id") != "artifact-runtime" or runtime.get("data-core-runtime") != CORE_VERSION:
            add(errors, "HRA305", "executable script must be Core runtime 0.1", "script")
        if runtime.get("src"):
            add(errors, "HRA306", "Core runtime must be inline", "script[src]")

    if len(parser.runtime_parts) != 1:
        add(errors, "HRA307", "exactly one inline Core runtime body is required", "script#artifact-runtime")
        return

    if len(parser.csp_meta) != 1:
        add(errors, "HRA308", "exactly one Content-Security-Policy meta is required", "head")
        return

    runtime = "".join(parser.runtime_parts[0]).encode("utf-8")
    digest = base64.b64encode(hashlib.sha256(runtime).digest()).decode("ascii")
    if TEMPLATE_PATH.is_file():
        reference_parser = ArtifactParser()
        reference_parser.feed(TEMPLATE_PATH.read_text(encoding="utf-8"))
        reference_parser.close()
        if len(reference_parser.runtime_parts) == 1:
            reference_runtime = "".join(reference_parser.runtime_parts[0]).encode("utf-8")
            reference_digest = base64.b64encode(hashlib.sha256(reference_runtime).digest()).decode("ascii")
            if digest != reference_digest:
                add(errors, "HRA310", "runtime does not match the Core 0.1 reference runtime", "script#artifact-runtime")

    csp = parser.csp_meta[0]
    directives: dict[str, list[str]] = {}
    for directive in csp.split(";"):
        parts = directive.strip().split()
        if parts:
            directives[parts[0]] = parts[1:]
    expected_directives = {
        "default-src": ["'none'"],
        "img-src": ["data:"],
        "style-src": ["'unsafe-inline'"],
        "script-src": [f"'sha256-{digest}'"],
        "connect-src": ["'none'"],
        "font-src": ["data:"],
        "object-src": ["'none'"],
        "base-uri": ["'none'"],
        "form-action": ["'none'"],
    }
    if directives != expected_directives:
        add(errors, "HRA309", "CSP directives do not match the Core 0.1 security policy", "meta[http-equiv=Content-Security-Policy]")


def validate_file(path: Path) -> ValidationResult:
    errors: list[Diagnostic] = []
    warnings: list[Diagnostic] = []
    text = path.read_text(encoding="utf-8")
    parser = ArtifactParser()
    parser.feed(text)
    parser.close()

    manifest = parse_manifest(parser, errors)
    if manifest:
        validate_manifest(manifest, errors)
    validate_document(parser, manifest, errors, warnings)
    validate_security(parser, errors)
    spec_version = manifest.get("spec") if manifest and isinstance(manifest.get("spec"), str) else None
    return ValidationResult(str(path), spec_version, errors, warnings)


def render_human(result: ValidationResult) -> str:
    if result.valid:
        headline = f"artifact validation passed: {result.artifact}"
    else:
        headline = f"artifact validation failed: {result.artifact}"
    lines = [headline]
    for diagnostic in result.errors:
        lines.append(f"ERROR {diagnostic.code} [{diagnostic.location}] {diagnostic.message}")
    for diagnostic in result.warnings:
        lines.append(f"WARNING {diagnostic.code} [{diagnostic.location}] {diagnostic.message}")
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path, help="self-contained HTML Artifact to validate")
    parser.add_argument("--json", action="store_true", dest="json_output", help="emit machine-readable JSON")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.artifact.is_file():
        message = f"artifact is not a file: {args.artifact}"
        if args.json_output:
            print(json.dumps({"valid": False, "artifact": str(args.artifact), "specVersion": None, "errors": [{"code": "HRA001", "message": message, "location": "input"}], "warnings": []}, ensure_ascii=False))
        else:
            print(message, file=sys.stderr)
        return 2
    try:
        result = validate_file(args.artifact)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        message = f"could not validate artifact: {exc}"
        if args.json_output:
            print(json.dumps({"valid": False, "artifact": str(args.artifact), "specVersion": None, "errors": [{"code": "HRA002", "message": message, "location": "input"}], "warnings": []}, ensure_ascii=False))
        else:
            print(message, file=sys.stderr)
        return 2

    if args.json_output:
        print(json.dumps(result.as_json(), ensure_ascii=False, indent=2))
    else:
        stream = sys.stdout if result.valid else sys.stderr
        print(render_human(result), file=stream)
    return 0 if result.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
