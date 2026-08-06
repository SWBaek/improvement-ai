#!/usr/bin/env python3
"""Render or check the human-readable Skill index from skills/catalog.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "skills" / "catalog.json"
INDEX = ROOT / "skills" / "README.md"
START = "<!-- skill-index:start -->"
END = "<!-- skill-index:end -->"
REPOSITORY = "https://github.com/SWBaek/improvement-ai"


def render_block() -> str:
    payload = json.loads(CATALOG.read_text(encoding="utf-8"))
    rows = [
        "| Skill | Version | Status | Release | Tracking |",
        "|---|---|---|---|---|",
    ]
    for skill in sorted(payload["skills"], key=lambda item: item["name"]):
        name = skill["name"]
        version = skill["version"]
        tag = f"{name}-v{version}"
        rows.append(
            f"| [{name}]({name}/SKILL.md) | `{version}` | {skill['status']} | "
            f"[{tag}]({REPOSITORY}/releases/tag/{tag}) | "
            f"[#{skill['trackingIssue']}]({REPOSITORY}/issues/{skill['trackingIssue']}) |"
        )
    return "\n".join(rows)


def expected_index() -> str:
    current = INDEX.read_text(encoding="utf-8")
    if current.count(START) != 1 or current.count(END) != 1:
        raise ValueError("skills/README.md must contain exactly one Skill index marker pair")
    before, remainder = current.split(START, 1)
    _, after = remainder.split(END, 1)
    return f"{before}{START}\n{render_block()}\n{END}{after}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()

    try:
        expected = expected_index()
        current = INDEX.read_text(encoding="utf-8")
    except (OSError, ValueError, json.JSONDecodeError, KeyError) as exc:
        print(f"Skill index error: {exc}", file=sys.stderr)
        return 1

    if args.check:
        if current != expected:
            print("skills/README.md is out of sync; run scripts/render_skill_index.py --write", file=sys.stderr)
            return 1
        print("Skill index is up to date")
        return 0

    INDEX.write_text(expected, encoding="utf-8", newline="\n")
    print(f"Updated {INDEX.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
