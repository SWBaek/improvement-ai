from __future__ import annotations

import json
import importlib.util
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "manage-focus-cycle"
TEMPLATE = SKILL_ROOT / "assets" / "focus-cycle-workspace.html"
SCENARIOS = ROOT / "tests" / "fixtures" / "manage-focus-cycle" / "scenarios.json"
WORKSPACE_INPUT = ROOT / "tests" / "fixtures" / "manage-focus-cycle" / "workspace-input.json"
RENDERER_PATH = SKILL_ROOT / "scripts" / "render_workspace.py"
RENDERER_SPEC = importlib.util.spec_from_file_location("render_workspace", RENDERER_PATH)
assert RENDERER_SPEC and RENDERER_SPEC.loader
RENDERER = importlib.util.module_from_spec(RENDERER_SPEC)
RENDERER_SPEC.loader.exec_module(RENDERER)


class WorkspaceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.tags: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag)
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.add(attributes["id"] or "")


class ManageFocusCycleSkillTests(unittest.TestCase):
    def test_skill_contract_and_implicit_invocation_metadata(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        metadata = (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")

        self.assertIn("name: manage-focus-cycle", skill)
        self.assertIn("Do not use for an already-scoped implementation task", skill)
        self.assertIn("exactly one Primary Focus Cycle", skill)
        self.assertIn("docs/focus/focus-cycle.md", skill)
        self.assertIn("scripts/render_workspace.py", skill)
        self.assertIn("workspace-input.schema.json", skill)
        self.assertIn("allow_implicit_invocation: true", metadata)
        self.assertIn("$manage-focus-cycle", metadata)

    def test_workspace_has_required_landmarks_and_no_input_controls(self) -> None:
        source = TEMPLATE.read_text(encoding="utf-8")
        parser = WorkspaceParser()
        parser.feed(source)

        required = {
            "project-context",
            "active-focus-cycle",
            "completion-contract",
            "current-discussion",
            "sources-freshness",
        }
        self.assertTrue(required.issubset(parser.ids))
        self.assertFalse({"form", "input", "button", "textarea", "select"} & set(parser.tags))
        self.assertIn("mermaid@11.16.1", source)
        self.assertIn("Mermaid unavailable; diagram source remains visible.", source)
        self.assertIn("{{NO_PROJECT_COMPLETION_LABEL}}", source)

    def test_renderer_validates_and_renders_safe_localized_html(self) -> None:
        payload = json.loads(WORKSPACE_INPUT.read_text(encoding="utf-8"))
        payload["project"]["purpose"] = '<script>alert("unsafe")</script>'
        payload["discussion"]["blocks"][0]["text"] = '<img src=x onerror="unsafe">'

        validated = RENDERER.validate_payload(payload)
        rendered = RENDERER.render_html(validated)

        self.assertIn("프로젝트 맥락", rendered)
        self.assertIn("&lt;script&gt;alert(&quot;unsafe&quot;)&lt;/script&gt;", rendered)
        self.assertIn("&lt;img src=x onerror=&quot;unsafe&quot;&gt;", rendered)
        self.assertNotIn('<script>alert("unsafe")</script>', rendered)
        self.assertNotRegex(rendered, r"\{\{[A-Z_]+\}\}")

        with tempfile.TemporaryDirectory() as temp:
            output = RENDERER.write_atomic(Path(temp) / "index.html", rendered)
            self.assertTrue(output.is_file())
            self.assertEqual([], list(output.parent.glob(".focus-cycle-*.tmp")))

    def test_renderer_rejects_unsafe_links_unknown_fields_and_invalid_tables(self) -> None:
        payload = json.loads(WORKSPACE_INPUT.read_text(encoding="utf-8"))
        payload["sources"][0]["location"] = "javascript:alert(1)"
        with self.assertRaisesRegex(RENDERER.InputError, "unsafe source link scheme"):
            RENDERER.validate_payload(payload)

        payload = json.loads(WORKSPACE_INPUT.read_text(encoding="utf-8"))
        payload["unexpected"] = True
        with self.assertRaisesRegex(RENDERER.InputError, "unknown field"):
            RENDERER.validate_payload(payload)

        payload = json.loads(WORKSPACE_INPUT.read_text(encoding="utf-8"))
        payload["discussion"]["blocks"][2]["rows"][0] = ["one cell"]
        with self.assertRaisesRegex(RENDERER.InputError, "must have 2 cells"):
            RENDERER.validate_payload(payload)

    def test_non_ascii_project_name_uses_stable_safe_slug(self) -> None:
        first = RENDERER.slugify("장기 연구 프로젝트")
        second = RENDERER.slugify("장기 연구 프로젝트")
        self.assertEqual(first, second)
        self.assertRegex(first, r"^project-[0-9a-f]{8}$")

    def test_renderer_supports_every_lifecycle_mode_and_english_labels(self) -> None:
        statuses = ("Proposed", "Active", "Blocked", "Ready to Close", "Closed")
        modes = ("delivery", "maintenance", "research", "decision")
        for status in statuses:
            for mode in modes:
                with self.subTest(status=status, mode=mode):
                    payload = json.loads(WORKSPACE_INPUT.read_text(encoding="utf-8"))
                    payload["language"] = "en-US"
                    payload["cycle"]["status"] = status
                    payload["cycle"]["mode"] = mode
                    rendered = RENDERER.render_html(RENDERER.validate_payload(payload))
                    self.assertIn("Project Context", rendered)
                    self.assertIn(f">{status}<", rendered)

    def test_scenarios_cover_required_archetypes_and_guardrails(self) -> None:
        payload = json.loads(SCENARIOS.read_text(encoding="utf-8"))
        scenarios = {item["id"]: item for item in payload["scenarios"]}

        self.assertEqual(
            {
                "finite-delivery",
                "long-lived-maintenance",
                "open-ended-research",
                "multiple-workstreams",
                "inferred-contract",
                "fallback-record",
            },
            set(scenarios),
        )
        self.assertEqual("Proposed", scenarios["inferred-contract"]["expected"]["status"])
        self.assertTrue(
            scenarios["inferred-contract"]["expected"]["requiresHumanConfirmation"]
        )
        self.assertEqual(
            "inconclusive",
            scenarios["open-ended-research"]["expected"]["validClosureOutcome"],
        )
        self.assertEqual(
            "docs/focus/focus-cycle.md",
            scenarios["fallback-record"]["expected"]["durableRecord"],
        )

        for scenario in scenarios.values():
            self.assertEqual(1, scenario["expected"]["primaryCycleCount"])
            self.assertFalse(scenario["expected"]["wholeProjectPercentageAllowed"])


if __name__ == "__main__":
    unittest.main()
