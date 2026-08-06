from __future__ import annotations

import json
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "manage-focus-cycle"
TEMPLATE = SKILL_ROOT / "assets" / "focus-cycle-workspace.html"
SCENARIOS = ROOT / "tests" / "fixtures" / "manage-focus-cycle" / "scenarios.json"


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
        self.assertIn("mermaid@11", source)
        self.assertIn("Mermaid unavailable; diagram source remains visible.", source)
        self.assertIn("No whole-project completion is calculated.", source)

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
