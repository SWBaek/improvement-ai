# Contributing

Issues and pull requests are welcome. This is a maintainer-led Capability Blueprint repository with no support SLA.

## Before proposing a Blueprint

1. Search existing issues and explain the repeated human-AI workflow problem.
2. Describe the required outcomes and invariants without fixing a universal implementation.
3. Identify the project contexts in which the capability should and should not be generated.
4. Define how an AI will inspect a target project, propose local Skills, obtain approval, and verify the result.
5. Exclude credentials, private project data, session logs, and generated project artifacts.

## Pull requests

1. Keep the human install entry point at `blueprints/<name>/README.md` and the canonical AI contract at `blueprints/<name>/BLUEPRINT.md`.
2. Add references only when the Blueprint cannot remain concise without them; do not add executable implementations, schemas, generators, or installable Skills.
3. Update the Blueprint index, tracking issue, architecture, or ADR only when their contract changes.
4. Check changed links, run the label-sync dry run when labels change, and run `git diff --check`.
5. Explain the human-visible capability outcome and the adaptation freedom left to target projects.
6. Treat the last commit that changes the canonical `BLUEPRINT.md` path as that Blueprint's revision; do not add SemVer, tags, Releases, changelogs, or version catalogs.
7. Require every generated artifact to stay inside the target project; do not add or recommend global Agent Skill installation or shared project state.

GitHub service operations follow `AGENTS.md`: use authenticated `gh` and never place tokens in commands or files.
