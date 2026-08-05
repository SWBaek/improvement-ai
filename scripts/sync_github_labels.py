#!/usr/bin/env python3
"""Create or update the repository label catalog through authenticated gh only."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / ".github" / "issue-labels.json"


def run_gh(arguments: list[str], *, capture: bool = False) -> str:
    result = subprocess.run(
        ["gh", *arguments],
        check=False,
        text=True,
        capture_output=capture,
    )
    if result.returncode != 0:
        if capture and result.stderr:
            print(result.stderr.strip(), file=sys.stderr)
        raise SystemExit(result.returncode)
    return result.stdout.strip() if capture else ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", help="GitHub repository in OWNER/NAME form")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print the authenticated gh commands without changing labels",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if shutil.which("gh") is None:
        print("error: GitHub CLI (gh) is required", file=sys.stderr)
        return 1

    run_gh(["auth", "status", "--hostname", "github.com"])
    repository = args.repo or run_gh(
        ["repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"],
        capture=True,
    )

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    labels = catalog["labels"]
    for label in labels:
        command = [
            "label",
            "create",
            label["name"],
            "--repo",
            repository,
            "--color",
            label["color"],
            "--description",
            label["description"],
            "--force",
        ]
        if args.dry_run:
            print("gh " + subprocess.list2cmdline(command))
        else:
            run_gh(command)
            print(f"synced: {label['name']}")

    print(f"{'would sync' if args.dry_run else 'synced'} {len(labels)} labels for {repository}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
