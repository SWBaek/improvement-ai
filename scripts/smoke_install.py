#!/usr/bin/env python3
"""Exercise the supported Codex installation path in an isolated project."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_CLI = "skills@1.5.22"
SKILL = "manage-focus-cycle"


def run(command: list[str], cwd: Path) -> str:
    result = subprocess.run(command, cwd=cwd, text=True, encoding="utf-8", capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(
            f"command failed ({result.returncode}): {' '.join(command)}\n{result.stdout}\n{result.stderr}"
        )
    return result.stdout + result.stderr


def main() -> int:
    executable = shutil.which("npx.cmd" if os.name == "nt" else "npx")
    if not executable:
        print("npx is required for the installation smoke test", file=sys.stderr)
        return 1

    try:
        with tempfile.TemporaryDirectory(prefix="improvement-ai-install-") as temp:
            project = Path(temp)
            listing = run([executable, SKILLS_CLI, "add", str(ROOT), "--list"], project)
            if SKILL not in listing:
                raise RuntimeError(f"{SKILL} was not discoverable in installer output")

            run(
                [
                    executable,
                    SKILLS_CLI,
                    "add",
                    str(ROOT),
                    "--skill",
                    SKILL,
                    "--agent",
                    "codex",
                    "--copy",
                    "-y",
                ],
                project,
            )

            candidates = [
                project / ".agents" / "skills" / SKILL,
                project / ".codex" / "skills" / SKILL,
            ]
            installed = next((path for path in candidates if (path / "SKILL.md").is_file()), None)
            if installed is None:
                raise RuntimeError("Codex installation did not contain the Skill entrypoint")
            required = [
                "LICENSE.txt",
                "assets/focus-cycle-workspace.html",
                "references/workspace-input.schema.json",
                "scripts/render_workspace.py",
            ]
            missing = [path for path in required if not (installed / path).is_file()]
            if missing:
                raise RuntimeError(f"installed Skill is incomplete: {', '.join(missing)}")
    except RuntimeError as exc:
        print(f"installation smoke test failed: {exc}", file=sys.stderr)
        return 1

    print(f"installation smoke test passed: {SKILL} via {SKILLS_CLI}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
