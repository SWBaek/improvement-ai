#!/usr/bin/env python3
"""Validate Human Review Artifacts Core 0.2 files."""

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
SCHEMA_PATH = FRAMEWORK_ROOT / "schemas" / "manifest-0.2.schema.json"
TEMPLATE_PATH = FRAMEWORK_ROOT / "templates" / "artifact.html"
CORE_SPEC = "human-review-artifacts/core@0.2"
CORE_VERSION = "0.2"
REQUIRED_SECTIONS = {"summary", "content", "provenance"}
REVIEW_MODES = {"comment", "decide", "approve"}
ARTIFACT_KINDS = {
    "fact", "assumption", "proposal", "decision", "question", "risk", "evidence"
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
CSP_BASELINE = {
    "default-src": {"'none'"},
    "img-src": {"data:"},
    "style-src": {"'unsafe-inline'"},
    "connect-src": {"'none'"},
    "font-src": {"data:"},
    "object-src": {"'none'"},
    "base-uri": {"'none'"},
    "form-action": {"'none'"},
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
            "valid": self.valid,
            "artifact": self.artifact,
            "specVersion": self.specVersion,
            "conformance": self.conformance,
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
        self.sections: list[tuple[str, str | None, bool]] = []
        self.main_roots = 0
        self.artifact_kinds: list[tuple[str, str | None]] = []
        self.review_items: list[str | None] = []
        self.review_options: list[tuple[str | None, str, str | None]] = []
        self.forbidden_elements: list[str] = []
        self.security_issues: list[tuple[str, str]] = []
        self.images_without_alt: list[str] = []
        self.svg_without_text: list[str] = []
        self.heading_levels: list[int] = []
        self.h1_texts: list[str] = []
        self.title_texts: list[str] = []
        self.manifest_field_texts: dict[str, list[str]] = {}
        self.styles: list[str] = []
        self._capture: tuple[str, int] | None = None
        self._text_stack: list[tuple[str, str | None, list[str]]] = []
        self._svg_stack: list[dict[str, bool]] = []
        self._review_stack: list[tuple[str, str | None]] = []

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
        elif tag == "title":
            self._text_stack.append(("title", None, []))
        elif re.fullmatch(r"h[1-6]", tag):
            self.heading_levels.append(int(tag[1]))
            self._text_stack.append((tag, None, []))
        elif "data-manifest-field" in attributes:
            self._text_stack.append(("manifest-field", attributes["data-manifest-field"], []))

        if "data-review-item" in attributes:
            self.review_items.append(element_id)
            self._review_stack.append((tag, element_id))
        if "data-review-option" in attributes:
            target = self._review_stack[-1][1] if self._review_stack else None
            self.review_options.append((target, attributes.get("value", ""), element_id))

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
        if self._review_stack and tag == self._review_stack[-1][0]:
            self._review_stack.pop()

    def handle_data(self, data: str) -> None:
        if self._capture:
            kind, index = self._capture
            if kind == "manifest":
                self.manifest_parts[index].append(data)
            elif kind == "script":
                self.executable_scripts[index]["parts"].append(data)
            elif kind == "style":
                self.styles[index] += data
        if self._text_stack:
            self._text_stack[-1][2].append(data)


def add(errors: list[Diagnostic], code: str, message: str, location: str) -> None:
    errors.append(Diagnostic(code, message, location))


def matches_type(value: Any, expected: str | list[str]) -> bool:
    if isinstance(expected, list):
        return any(matches_type(value, item) for item in expected)
    return {
        "array": isinstance(value, list),
        "object": isinstance(value, dict),
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
        "null": value is None,
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
        return bool(parsed.scheme and (parsed.netloc or parsed.scheme in {"urn", "file"}))
    return True


def validate_schema_node(value: Any, schema: dict[str, Any], path: str, errors: list[Diagnostic], prefix: str = "HRA") -> None:
    expected_type = schema.get("type")
    if expected_type and not matches_type(value, expected_type):
        add(errors, f"{prefix}103", f"expected {expected_type}", path)
        return
    if "const" in schema and value != schema["const"]:
        add(errors, f"{prefix}104", f"must equal {schema['const']!r}", path)
    if "enum" in schema and value not in schema["enum"]:
        add(errors, f"{prefix}105", f"must be one of {schema['enum']}", path)
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            add(errors, f"{prefix}106", "string is shorter than allowed", path)
        if len(value) > schema.get("maxLength", sys.maxsize):
            add(errors, f"{prefix}107", "string is longer than allowed", path)
        pattern = schema.get("pattern")
        if pattern and not re.fullmatch(pattern, value):
            add(errors, f"{prefix}108", f"does not match {pattern!r}", path)
        if schema.get("format") and not validate_format(value, schema["format"]):
            add(errors, f"{prefix}109", f"is not a valid {schema['format']}", path)
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            add(errors, f"{prefix}114", "array has fewer items than allowed", path)
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            add(errors, f"{prefix}115", "array has more items than allowed", path)
        if schema.get("uniqueItems"):
            serialized = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in value]
            if len(serialized) != len(set(serialized)):
                add(errors, f"{prefix}110", "array items must be unique", path)
        if schema.get("items"):
            for index, item in enumerate(value):
                validate_schema_node(item, schema["items"], f"{path}[{index}]", errors, prefix)
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                add(errors, f"{prefix}111", f"missing required property {key!r}", path)
        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        for key, item in value.items():
            if schema.get("propertyNames"):
                validate_schema_node(key, schema["propertyNames"], f"{path}.<property-name>", errors, prefix)
            if key in properties:
                validate_schema_node(item, properties[key], f"{path}.{key}", errors, prefix)
            elif additional is False:
                add(errors, f"{prefix}112", f"unexpected property {key!r}", path)
            elif isinstance(additional, dict):
                validate_schema_node(item, additional, f"{path}.{key}", errors, prefix)


def parse_manifest(parser: ArtifactParser, errors: list[Diagnostic]) -> dict[str, Any] | None:
    if len(parser.manifest_parts) != 1:
        add(errors, "HRA101", "exactly one artifact Manifest is required", "head")
        return None
    try:
        manifest = json.loads("".join(parser.manifest_parts[0]))
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
    created, updated = manifest.get("createdAt"), manifest.get("updatedAt")
    if isinstance(created, str) and isinstance(updated, str):
        try:
            if datetime.fromisoformat(updated.replace("Z", "+00:00")) < datetime.fromisoformat(created.replace("Z", "+00:00")):
                add(errors, "HRA113", "updatedAt cannot be earlier than createdAt", "manifest.updatedAt")
        except ValueError:
            pass
    review = manifest.get("review")
    if isinstance(review, dict):
        targets = review.get("targets")
        if review.get("mode") in REVIEW_MODES and isinstance(targets, list) and not targets:
            add(errors, "HRA116", f"review mode {review.get('mode')!r} requires at least one target", "manifest.review.targets")
    profiles = {
        item.get("name"): item.get("version")
        for item in manifest.get("profiles", []) if isinstance(item, dict)
    }
    runtime = manifest.get("runtime")
    if isinstance(runtime, dict) and isinstance(runtime.get("scripts"), list):
        for index, script in enumerate(runtime["scripts"]):
            if not isinstance(script, dict):
                continue
            owner = script.get("owner")
            profile = script.get("profile")
            if owner == "core":
                if profile is not None:
                    add(errors, "HRA117", "Core runtime cannot declare profile", f"manifest.runtime.scripts[{index}]")
                if script.get("version") != CORE_VERSION:
                    add(errors, "HRA118", "Core runtime version must match Core spec", f"manifest.runtime.scripts[{index}].version")
            elif owner == "profile":
                if not isinstance(profile, str) or profiles.get(profile) != script.get("version"):
                    add(errors, "HRA119", "Profile runtime must match a declared Profile name and version", f"manifest.runtime.scripts[{index}]")


def validate_document(parser: ArtifactParser, manifest: dict[str, Any] | None, errors: list[Diagnostic], warnings: list[Diagnostic]) -> None:
    if parser.core_meta != ["core@0.2"]:
        add(errors, "HRA201", "exactly one Core 0.2 meta declaration is required", "head")
    if len(parser.html_langs) != 1 or not parser.html_langs[0]:
        add(errors, "HRA202", "html must declare one non-empty lang", "html")
    if parser.main_roots != 1:
        add(errors, "HRA203", "exactly one main[data-artifact-root] is required", "main")
    duplicates = sorted(item for item, count in Counter(parser.ids).items() if count > 1)
    if duplicates:
        add(errors, "HRA204", f"duplicate ids: {', '.join(duplicates)}", "document")
    section_names = [name for name, _, _ in parser.sections]
    missing = sorted(REQUIRED_SECTIONS - set(section_names))
    if missing:
        add(errors, "HRA205", f"missing required sections: {', '.join(missing)}", "main")
    duplicate_sections = sorted(item for item, count in Counter(section_names).items() if count > 1)
    if duplicate_sections:
        add(errors, "HRA206", f"duplicate sections: {', '.join(duplicate_sections)}", "main")
    for name, section_id, hidden in parser.sections:
        if not section_id:
            add(errors, "HRA207", f"section {name!r} requires an id", "main")
        if hidden:
            add(errors, "HRA208", f"section {name!r} cannot be hidden in source", section_id or "section")
    if len(parser.h1_texts) != 1 or not parser.h1_texts[0]:
        add(errors, "HRA209", "exactly one non-empty h1 is required", "document")
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
    for item_id in parser.review_items:
        if not item_id:
            add(errors, "HRA221", "data-review-item requires an id", "[data-review-item]")
    option_values = [value for _, value, _ in parser.review_options]
    if any(not value for value in option_values):
        add(errors, "HRA222", "data-review-option requires a non-empty value", "[data-review-option]")
    duplicate_options = sorted(item for item, count in Counter(option_values).items() if item and count > 1)
    if duplicate_options:
        add(errors, "HRA223", f"duplicate review option values: {', '.join(duplicate_options)}", "[data-review-option]")
    if any(target is None for target, _, _ in parser.review_options):
        add(errors, "HRA224", "review options must be inside data-review-item", "[data-review-option]")

    if not manifest:
        return
    if manifest.get("spec") != CORE_SPEC:
        add(errors, "HRA214", f"unsupported Core spec {manifest.get('spec')!r}", "manifest.spec")
    if parser.html_langs and manifest.get("language") != parser.html_langs[0]:
        add(errors, "HRA215", "Manifest language does not match html lang", "html[lang]")
    if len(parser.title_texts) != 1 or manifest.get("title") != parser.title_texts[0]:
        add(errors, "HRA216", "Manifest title does not match title element", "title")
    if len(parser.h1_texts) == 1 and manifest.get("title") != parser.h1_texts[0]:
        add(errors, "HRA217", "Manifest title does not match visible h1", "h1")
    if len(parser.body_statuses) != 1 or manifest.get("status") != parser.body_statuses[0]:
        add(errors, "HRA218", "Manifest status does not match body status", "body")
    for field, code in (("status", "HRA220"), ("revision", "HRA225")):
        visible = parser.manifest_field_texts.get(field, [])
        if len(visible) != 1 or str(manifest.get(field)) != visible[0]:
            add(errors, code, f"Manifest {field} does not match visible {field}", f"[data-manifest-field={field}]")
    review = manifest.get("review", {})
    mode = review.get("mode") if isinstance(review, dict) else None
    targets = review.get("targets", []) if isinstance(review, dict) else []
    if mode in REVIEW_MODES and "review-request" not in section_names:
        add(errors, "HRA219", f"review mode {mode!r} requires review-request", "main")
    for target in targets if isinstance(targets, list) else []:
        if target not in parser.review_items:
            add(errors, "HRA226", f"review target {target!r} is not a data-review-item", "manifest.review.targets")
    known_profiles = {path.name for path in (FRAMEWORK_ROOT / "profiles").iterdir() if path.is_dir()}
    for profile in manifest.get("profiles", []):
        if isinstance(profile, dict) and profile.get("name") not in known_profiles:
            warnings.append(Diagnostic("HRA901", f"unknown profile {profile.get('name')!r}", "manifest.profiles"))


def script_digest(body: str) -> str:
    encoded = base64.b64encode(hashlib.sha256(body.encode("utf-8")).digest()).decode("ascii")
    return f"sha256-{encoded}"


def parse_csp(raw: str) -> dict[str, set[str]]:
    directives: dict[str, set[str]] = {}
    for part in raw.split(";"):
        tokens = part.strip().split()
        if tokens:
            directives[tokens[0].lower()] = set(tokens[1:])
    return directives


def reference_core_body() -> str | None:
    if not TEMPLATE_PATH.is_file():
        return None
    parser = ArtifactParser()
    parser.feed(TEMPLATE_PATH.read_text(encoding="utf-8"))
    parser.close()
    for script in parser.executable_scripts:
        if script["attrs"].get("data-artifact-runtime") == f"core@{CORE_VERSION}":
            return "".join(script["parts"])
    return None


def validate_security(parser: ArtifactParser, manifest: dict[str, Any] | None, errors: list[Diagnostic], warnings: list[Diagnostic]) -> None:
    if parser.forbidden_elements:
        add(errors, "HRA301", f"forbidden elements: {', '.join(sorted(set(parser.forbidden_elements)))}", "document")
    for location, issue in parser.security_issues:
        add(errors, "HRA302", issue, location)
    for index, style in enumerate(parser.styles):
        for match in re.finditer(r"url\((.*?)\)", style, re.IGNORECASE | re.DOTALL):
            target = match.group(1).strip(" \t\r\n\"'")
            if not target.startswith("data:"):
                add(errors, "HRA303", f"style contains non-data URL {target!r}", f"style[{index}]")
    if len(parser.csp_meta) != 1:
        add(errors, "HRA308", "exactly one Content-Security-Policy meta is required", "head")
        return
    descriptors = []
    if manifest and isinstance(manifest.get("runtime"), dict):
        value = manifest["runtime"].get("scripts")
        if isinstance(value, list):
            descriptors = [item for item in value if isinstance(item, dict)]
    descriptor_by_id = {item.get("id"): item for item in descriptors if isinstance(item.get("id"), str)}
    if len(descriptor_by_id) != len(descriptors):
        add(errors, "HRA304", "runtime script ids must be unique", "manifest.runtime.scripts")
    actual_ids: set[str] = set()
    actual_digests: set[str] = set()
    reference_body = reference_core_body()
    profile_versions = {
        item.get("name"): item.get("version")
        for item in (manifest or {}).get("profiles", []) if isinstance(item, dict)
    }
    for script in parser.executable_scripts:
        attrs = script["attrs"]
        script_id = attrs.get("id")
        if attrs.get("src"):
            add(errors, "HRA306", "runtime must be inline", f"script#{script_id or '?'}")
        if not script_id or script_id not in descriptor_by_id:
            add(errors, "HRA304", "every executable script must be declared in Manifest runtime.scripts", f"script#{script_id or '?'}")
            continue
        actual_ids.add(script_id)
        descriptor = descriptor_by_id[script_id]
        body = "".join(script["parts"])
        digest = script_digest(body)
        actual_digests.add(digest)
        if descriptor.get("digest") != digest:
            add(errors, "HRA307", "runtime digest does not match script body", f"script#{script_id}")
        owner, version = descriptor.get("owner"), descriptor.get("version")
        declared_runtime = attrs.get("data-artifact-runtime")
        if owner == "core":
            if declared_runtime != f"core@{version}":
                add(errors, "HRA305", "Core runtime declaration does not match Manifest", f"script#{script_id}")
            if reference_body is not None and body != reference_body:
                add(errors, "HRA310", "Core runtime does not match the Core 0.2 reference runtime", f"script#{script_id}")
        elif owner == "profile":
            profile = descriptor.get("profile")
            if declared_runtime != f"profile:{profile}@{version}":
                add(errors, "HRA305", "Profile runtime declaration does not match Manifest", f"script#{script_id}")
            if profile_versions.get(profile) == version:
                warnings.append(Diagnostic("HRA902", f"Profile runtime {profile!r}@{version} is integrity-checked but behavior is unverified", f"script#{script_id}"))
    missing_scripts = sorted(set(descriptor_by_id) - actual_ids)
    if missing_scripts:
        add(errors, "HRA311", f"declared runtime scripts are missing: {', '.join(missing_scripts)}", "manifest.runtime.scripts")

    directives = parse_csp(parser.csp_meta[0])
    expected = dict(CSP_BASELINE)
    expected["script-src"] = {f"'{item}'" for item in actual_digests} or {"'none'"}
    if directives != expected:
        add(errors, "HRA309", "CSP directives do not match the Core 0.2 security policy and runtime hashes", "meta[http-equiv=Content-Security-Policy]")


def build_conformance(manifest: dict[str, Any] | None, parser: ArtifactParser, errors: list[Diagnostic]) -> dict[str, Any]:
    profiles = []
    for item in (manifest or {}).get("profiles", []):
        if isinstance(item, dict):
            profiles.append({"name": item.get("name"), "version": item.get("version"), "status": "unverified"})
    owners = {
        item.get("owner")
        for item in ((manifest or {}).get("runtime", {}).get("scripts", []) if isinstance((manifest or {}).get("runtime"), dict) else [])
        if isinstance(item, dict)
    }
    runtime = "profile" if "profile" in owners else "core" if "core" in owners else "none"
    return {"core": "invalid" if errors else "valid", "runtime": runtime, "profiles": profiles}


def validate_file(path: Path) -> ValidationResult:
    parser = ArtifactParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    errors: list[Diagnostic] = []
    warnings: list[Diagnostic] = []
    manifest = parse_manifest(parser, errors)
    if manifest:
        validate_manifest(manifest, errors)
    validate_document(parser, manifest, errors, warnings)
    validate_security(parser, manifest, errors, warnings)
    spec_version = manifest.get("spec") if manifest and isinstance(manifest.get("spec"), str) else None
    return ValidationResult(str(path), spec_version, errors, warnings, build_conformance(manifest, parser, errors))


def render_human(result: ValidationResult) -> str:
    lines = [f"{'VALID' if result.valid else 'INVALID'}: {result.artifact}"]
    for item in result.errors:
        lines.append(f"ERROR {item.code} [{item.location}] {item.message}")
    for item in result.warnings:
        lines.append(f"WARN  {item.code} [{item.location}] {item.message}")
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.artifact.is_file():
        message = f"input file not found: {args.artifact}"
        if args.as_json:
            print(json.dumps({"valid": False, "artifact": str(args.artifact), "specVersion": None, "conformance": {"core": "invalid", "runtime": "none", "profiles": []}, "errors": [{"code": "HRA001", "message": message, "location": "input"}], "warnings": []}, ensure_ascii=False))
        else:
            print(message, file=sys.stderr)
        return 2
    try:
        result = validate_file(args.artifact)
    except (OSError, UnicodeError) as exc:
        message = f"cannot read input: {exc}"
        if args.as_json:
            print(json.dumps({"valid": False, "artifact": str(args.artifact), "specVersion": None, "conformance": {"core": "invalid", "runtime": "none", "profiles": []}, "errors": [{"code": "HRA002", "message": message, "location": "input"}], "warnings": []}, ensure_ascii=False))
        else:
            print(message, file=sys.stderr)
        return 2
    print(json.dumps(result.as_json(), ensure_ascii=False, indent=2) if args.as_json else render_human(result))
    return 0 if result.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
