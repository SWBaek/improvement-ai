#!/usr/bin/env python3
"""Validate structured Focus Cycle data and render a safe standalone Workspace."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import sys
import tempfile
import unicodedata
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = SKILL_ROOT / "references" / "workspace-input.schema.json"
TEMPLATE_PATH = SKILL_ROOT / "assets" / "focus-cycle-workspace.html"
PLACEHOLDER = re.compile(r"\{\{[A-Z_]+\}\}")
SLUG_PART = re.compile(r"[^a-z0-9]+")
LABELS = {
    "en": {
        "workspace": "Focus Cycle Workspace",
        "updated": "Updated",
        "durable_record": "Durable record",
        "human_decision": "Human decision",
        "mode": "Mode",
        "progress_view": "Progress view",
        "decision_readiness": "Decision readiness",
        "primary_blocker": "Primary blocker",
        "long_lived_context": "Long-lived context",
        "project_context": "Project Context",
        "no_project_completion": "No whole-project completion is calculated.",
        "purpose": "Purpose",
        "workstreams": "Relevant workstreams",
        "sources": "Sources & Freshness",
        "primary_work": "Primary work",
        "active_cycle": "Active Focus Cycle",
        "objective": "Objective",
        "why_now": "Why now",
        "in_scope": "In scope",
        "out_scope": "Out of scope",
        "cycle_progress": "Cycle-specific progress",
        "exit_conditions": "Exit conditions",
        "completion_contract": "Completion Contract",
        "review_budget": "Review point / budget",
        "expected_outcome": "Expected outcome",
        "reopen_condition": "Reopen condition",
        "current_interaction": "Current interaction",
        "current_discussion": "Current Discussion",
        "question": "Question",
        "revision": "Revision",
        "observed": "observed",
        "empty_visual": "No additional visual is required for this discussion.",
        "footer": "This Workspace is a temporary human-readable projection. Confirm decisions in chat and keep durable history in the named project record.",
    },
    "ko": {
        "workspace": "Focus Cycle Workspace",
        "updated": "갱신",
        "durable_record": "영구 기록",
        "human_decision": "사람의 결정",
        "mode": "작업 유형",
        "progress_view": "진행 표현",
        "decision_readiness": "결정 준비도",
        "primary_blocker": "주요 장애물",
        "long_lived_context": "장기 맥락",
        "project_context": "프로젝트 맥락",
        "no_project_completion": "프로젝트 전체 완료율은 계산하지 않습니다.",
        "purpose": "목적",
        "workstreams": "관련 작업 흐름",
        "sources": "출처 및 최신성",
        "primary_work": "현재 주 작업",
        "active_cycle": "Primary Focus Cycle",
        "objective": "목표",
        "why_now": "지금 중요한 이유",
        "in_scope": "범위 안",
        "out_scope": "범위 밖",
        "cycle_progress": "Cycle 진행 상태",
        "exit_conditions": "종료 조건",
        "completion_contract": "Completion Contract",
        "review_budget": "검토 시점 / 예산",
        "expected_outcome": "기대 결과",
        "reopen_condition": "재개 조건",
        "current_interaction": "현재 상호작용",
        "current_discussion": "현재 논의",
        "question": "질문",
        "revision": "리비전",
        "observed": "확인",
        "empty_visual": "이 논의에는 추가 시각화가 필요하지 않습니다.",
        "footer": "이 Workspace는 임시 표현층입니다. 결정은 채팅에서 확인하고 이력은 지정된 프로젝트 기록에 보존합니다.",
    },
}


class InputError(ValueError):
    """Raised when Workspace input does not satisfy the public contract."""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Workspace JSON input")
    parser.add_argument("--output", type=Path, help="Override the stable temp HTML path")
    parser.add_argument("--open", action="store_true", dest="open_browser", help="Open the rendered HTML")
    parser.add_argument("--validate-only", action="store_true", help="Validate without writing HTML")
    args = parser.parse_args(argv)
    if args.validate_only and (args.output or args.open_browser):
        parser.error("--validate-only cannot be combined with --output or --open")
    return args


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise InputError(f"input file does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise InputError(f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc
    except OSError as exc:
        raise InputError(f"cannot read input file: {exc}") from exc


def matches_type(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    return False


def validate_schema(value: Any, schema: dict[str, Any], path: str = "$") -> None:
    expected = schema.get("type")
    if expected and not matches_type(value, expected):
        raise InputError(f"{path} must be {expected}")

    if "enum" in schema and value not in schema["enum"]:
        allowed = ", ".join(repr(item) for item in schema["enum"])
        raise InputError(f"{path} must be one of: {allowed}")

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            raise InputError(f"{path} must not be empty")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            raise InputError(f"{path} exceeds maximum length {schema['maxLength']}")

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise InputError(f"{path} must contain at least {schema['minItems']} item(s)")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                validate_schema(item, item_schema, f"{path}[{index}]")

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        missing = [key for key in schema.get("required", []) if key not in value]
        if missing:
            raise InputError(f"{path} is missing required field(s): {', '.join(missing)}")
        if schema.get("additionalProperties") is False:
            unknown = sorted(set(value) - set(properties))
            if unknown:
                raise InputError(f"{path} has unknown field(s): {', '.join(unknown)}")
        for key, child in value.items():
            if key in properties:
                validate_schema(child, properties[key], f"{path}.{key}")


def validate_business_rules(payload: dict[str, Any]) -> None:
    timestamp = payload["updatedAt"]
    try:
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise InputError("$.updatedAt must be an ISO-8601 timestamp") from exc

    for index, source in enumerate(payload["sources"]):
        try:
            datetime.fromisoformat(source["observedAt"].replace("Z", "+00:00"))
        except ValueError as exc:
            raise InputError(f"$.sources[{index}].observedAt must be an ISO-8601 timestamp") from exc
        parsed = urlsplit(source["location"])
        if parsed.scheme.lower() not in {"", "http", "https"}:
            raise InputError(f"unsafe source link scheme: {parsed.scheme}")
        if parsed.scheme.lower() in {"http", "https"} and not parsed.netloc:
            raise InputError(f"$.sources[{index}].location must have a host")

    for index, block in enumerate(payload["discussion"]["blocks"]):
        block_type = block["type"]
        required_by_type = {
            "paragraph": {"text"},
            "list": {"items"},
            "table": {"caption", "columns", "rows"},
            "mermaid": {"source", "fallback"},
        }
        allowed_by_type = {
            "paragraph": {"type", "title", "text"},
            "list": {"type", "title", "items"},
            "table": {"type", "title", "caption", "columns", "rows"},
            "mermaid": {"type", "title", "source", "fallback"},
        }
        missing = required_by_type[block_type] - set(block)
        extra = set(block) - allowed_by_type[block_type]
        if missing:
            raise InputError(f"$.discussion.blocks[{index}] is missing: {', '.join(sorted(missing))}")
        if extra:
            raise InputError(f"$.discussion.blocks[{index}] has fields invalid for {block_type}: {', '.join(sorted(extra))}")
        if block_type == "table":
            width = len(block["columns"])
            for row_index, row in enumerate(block["rows"]):
                if len(row) != width:
                    raise InputError(
                        f"$.discussion.blocks[{index}].rows[{row_index}] must have {width} cells"
                    )


def validate_payload(payload: Any) -> dict[str, Any]:
    schema = load_json(SCHEMA_PATH)
    validate_schema(payload, schema)
    assert isinstance(payload, dict)
    validate_business_rules(payload)
    return payload


def escape(value: Any) -> str:
    return html.escape(str(value), quote=True)


def slugify(project_name: str) -> str:
    normalized = unicodedata.normalize("NFKD", project_name).encode("ascii", "ignore").decode("ascii")
    slug = SLUG_PART.sub("-", normalized.lower()).strip("-")
    if slug:
        return slug
    digest = hashlib.sha256(project_name.encode("utf-8")).hexdigest()[:8]
    return f"project-{digest}"


def default_output_path(project_name: str) -> Path:
    return Path(tempfile.gettempdir()) / "focus-cycle-workspace" / slugify(project_name) / "index.html"


def render_heading(title: str | None, level: int = 3) -> str:
    return f"<h{level}>{escape(title)}</h{level}>" if title else ""


def render_list(items: list[str], css_class: str = "") -> str:
    class_attr = f' class="{escape(css_class)}"' if css_class else ""
    body = "".join(f"<li>{escape(item)}</li>" for item in items)
    return f"<ul{class_attr}>{body}</ul>"


def render_discussion_blocks(blocks: list[dict[str, Any]], labels: dict[str, str]) -> str:
    output: list[str] = []
    for block in blocks:
        title = render_heading(block.get("title"))
        block_type = block["type"]
        if block_type == "paragraph":
            content = f"<p>{escape(block['text'])}</p>"
        elif block_type == "list":
            content = render_list(block["items"])
        elif block_type == "table":
            columns = "".join(f"<th scope=\"col\">{escape(item)}</th>" for item in block["columns"])
            rows = "".join(
                "<tr>" + "".join(f"<td>{escape(cell)}</td>" for cell in row) + "</tr>"
                for row in block["rows"]
            )
            content = (
                '<div class="table-wrap"><table>'
                f"<caption>{escape(block['caption'])}</caption>"
                f"<thead><tr>{columns}</tr></thead><tbody>{rows}</tbody></table></div>"
            )
        else:
            content = (
                f'<pre class="mermaid">{escape(block["source"])}</pre>'
                f'<p class="diagram-fallback">{escape(block["fallback"])}</p>'
            )
        output.append(f'<div class="discussion-block">{title}{content}</div>')
    return "".join(output) or f'<p class="muted">{escape(labels["empty_visual"])}</p>'


def render_workstreams(workstreams: list[dict[str, str]]) -> str:
    return "".join(
        '<li class="workstream">'
        f'<span class="state state-{escape(item["state"])}">{escape(item["state"])}</span>'
        f'<div><strong>{escape(item["name"])}</strong><p>{escape(item["detail"])}</p></div>'
        "</li>"
        for item in workstreams
    ) or '<li class="muted">No additional workstreams are in view.</li>'


def render_progress(progress: dict[str, Any]) -> str:
    items = "".join(
        '<article class="progress-item">'
        f'<span class="state state-{escape(item["state"])}">{escape(item["state"])}</span>'
        f'<h3>{escape(item["label"])}</h3><p>{escape(item["detail"])}</p>'
        "</article>"
        for item in progress["items"]
    )
    return f'<p class="summary">{escape(progress["summary"])}</p><div class="card-grid">{items}</div>'


def render_criteria(criteria: list[dict[str, str]]) -> str:
    return "".join(
        '<article class="criterion">'
        f'<span class="state state-{escape(item["state"])}">{escape(item["state"])}</span>'
        f'<p>{escape(item["text"])}</p>'
        "</article>"
        for item in criteria
    )


def safe_link(location: str) -> str:
    parsed = urlsplit(location)
    if parsed.scheme.lower() in {"http", "https"} and parsed.netloc:
        safe = escape(location)
        return f'<a href="{safe}" target="_blank" rel="noopener noreferrer">{safe}</a>'
    if parsed.scheme:
        raise InputError(f"unsafe source link scheme: {parsed.scheme}")
    return f"<code>{escape(location)}</code>"


def render_sources(sources: list[dict[str, str]], labels: dict[str, str]) -> str:
    return "".join(
        '<li class="source-item">'
        f'<span class="state state-{escape(item["classification"])}">{escape(item["classification"])}</span>'
        f'<div><strong>{escape(item["label"])}</strong><p>{safe_link(item["location"])}</p>'
        f'<small>{escape(labels["revision"])} {escape(item["revision"])} · {escape(labels["observed"])} {escape(item["observedAt"])}</small></div>'
        "</li>"
        for item in sources
    )


def render_scope(scope: dict[str, list[str]], labels: dict[str, str]) -> str:
    return (
        '<div class="scope-grid">'
        f'<div><h3>{escape(labels["in_scope"])}</h3>{render_list(scope["in"])}</div>'
        f'<div><h3>{escape(labels["out_scope"])}</h3>{render_list(scope["out"])}</div>'
        "</div>"
    )


def render_html(payload: dict[str, Any]) -> str:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    project = payload["project"]
    cycle = payload["cycle"]
    contract = payload["contract"]
    discussion = payload["discussion"]
    labels = LABELS["ko"] if payload["language"].lower().startswith("ko") else LABELS["en"]
    replacements = {
        "{{LANG}}": escape(payload["language"]),
        "{{PAGE_TITLE}}": escape(f"{project['name']} — {cycle['title']}"),
        "{{PROJECT_NAME}}": escape(project["name"]),
        "{{FOCUS_CYCLE_TITLE}}": escape(cycle["title"]),
        "{{UPDATED_AT}}": escape(payload["updatedAt"]),
        "{{DURABLE_RECORD}}": escape(payload["durableRecord"]),
        "{{CYCLE_STATUS}}": escape(cycle["status"]),
        "{{STATUS_CLASS}}": escape(SLUG_PART.sub("-", cycle["status"].lower()).strip("-")),
        "{{REQUESTED_DECISION}}": escape(discussion["requestedDecision"]),
        "{{WORK_MODE}}": escape(cycle["mode"]),
        "{{PROGRESS_KIND}}": escape(cycle["progress"]["kind"]),
        "{{READINESS}}": escape(cycle["readiness"]),
        "{{PRIMARY_BLOCKER}}": escape(cycle["primaryBlocker"]),
        "{{PROJECT_PURPOSE}}": escape(project["purpose"]),
        "{{WORKSTREAM_ITEMS}}": render_workstreams(project["workstreams"]),
        "{{SOURCE_ITEMS}}": render_sources(payload["sources"], labels),
        "{{OBJECTIVE}}": escape(cycle["objective"]),
        "{{WHY_NOW}}": escape(cycle["whyNow"]),
        "{{SCOPE_CONTENT}}": render_scope(cycle["scope"], labels),
        "{{PROGRESS_CONTENT}}": render_progress(cycle["progress"]),
        "{{CRITERION_CARDS}}": render_criteria(contract["criteria"]),
        "{{REVIEW_BUDGET}}": escape(contract["reviewBudget"]),
        "{{EXPECTED_OUTCOME}}": escape(contract["expectedOutcome"]),
        "{{REOPEN_CONDITION}}": escape(contract["reopenCondition"]),
        "{{CURRENT_QUESTION}}": escape(discussion["question"]),
        "{{DISCUSSION_BLOCKS}}": render_discussion_blocks(discussion["blocks"], labels),
        "{{WORKSPACE_LABEL}}": escape(labels["workspace"]),
        "{{UPDATED_LABEL}}": escape(labels["updated"]),
        "{{DURABLE_RECORD_LABEL}}": escape(labels["durable_record"]),
        "{{HUMAN_DECISION_LABEL}}": escape(labels["human_decision"]),
        "{{MODE_LABEL}}": escape(labels["mode"]),
        "{{PROGRESS_VIEW_LABEL}}": escape(labels["progress_view"]),
        "{{DECISION_READINESS_LABEL}}": escape(labels["decision_readiness"]),
        "{{PRIMARY_BLOCKER_LABEL}}": escape(labels["primary_blocker"]),
        "{{LONG_LIVED_CONTEXT_LABEL}}": escape(labels["long_lived_context"]),
        "{{PROJECT_CONTEXT_LABEL}}": escape(labels["project_context"]),
        "{{NO_PROJECT_COMPLETION_LABEL}}": escape(labels["no_project_completion"]),
        "{{PURPOSE_LABEL}}": escape(labels["purpose"]),
        "{{WORKSTREAMS_LABEL}}": escape(labels["workstreams"]),
        "{{SOURCES_LABEL}}": escape(labels["sources"]),
        "{{PRIMARY_WORK_LABEL}}": escape(labels["primary_work"]),
        "{{ACTIVE_CYCLE_LABEL}}": escape(labels["active_cycle"]),
        "{{OBJECTIVE_LABEL}}": escape(labels["objective"]),
        "{{WHY_NOW_LABEL}}": escape(labels["why_now"]),
        "{{CYCLE_PROGRESS_LABEL}}": escape(labels["cycle_progress"]),
        "{{EXIT_CONDITIONS_LABEL}}": escape(labels["exit_conditions"]),
        "{{COMPLETION_CONTRACT_LABEL}}": escape(labels["completion_contract"]),
        "{{REVIEW_BUDGET_LABEL}}": escape(labels["review_budget"]),
        "{{EXPECTED_OUTCOME_LABEL}}": escape(labels["expected_outcome"]),
        "{{REOPEN_CONDITION_LABEL}}": escape(labels["reopen_condition"]),
        "{{CURRENT_INTERACTION_LABEL}}": escape(labels["current_interaction"]),
        "{{CURRENT_DISCUSSION_LABEL}}": escape(labels["current_discussion"]),
        "{{QUESTION_LABEL}}": escape(labels["question"]),
        "{{FOOTER_NOTE}}": escape(labels["footer"]),
    }
    for token, value in replacements.items():
        template = template.replace(token, value)
    remaining = sorted(set(PLACEHOLDER.findall(template)))
    if remaining:
        raise RuntimeError(f"template contains unreplaced placeholders: {', '.join(remaining)}")
    return template


def write_atomic(path: Path, content: str) -> Path:
    path = path.expanduser().resolve()
    if path.suffix.lower() != ".html":
        raise InputError("output path must end with .html")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", dir=path.parent, prefix=".focus-cycle-", suffix=".tmp", delete=False
        ) as stream:
            temporary = Path(stream.name)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary and temporary.exists():
            temporary.unlink()
    return path


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        payload = validate_payload(load_json(args.input))
        if args.validate_only:
            print("valid")
            return 0
        output = args.output or default_output_path(payload["project"]["name"])
        output = write_atomic(output, render_html(payload))
        if args.open_browser and not webbrowser.open(output.as_uri()):
            print(f"warning: browser could not be opened for {output}", file=sys.stderr)
        print(output)
        return 0
    except InputError as exc:
        print(f"input error: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"runtime error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
