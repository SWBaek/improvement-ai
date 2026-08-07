# improvement-ai

> Canonical Capability Blueprints that AI agents adapt into project-owned Skills and workflows.

[한국어](README.ko.md)

`improvement-ai` is not an application, Skill catalog, package registry, or source of installable runtime implementations. It records reusable capability designs as compact Blueprints. A human gives a Blueprint to an AI working inside a target project; the AI inspects that project's conventions, proposes a local design, and creates project-owned Skills only after approval.

## Principles

- **Blueprint, not product:** preserve the problem, invariants, operations, adaptation points, and acceptance criteria rather than one universal implementation.
- **Inspect before designing:** ground every proposal in the target project's instructions, records, tools, and Agent clients.
- **Propose before writing:** show the Skill decomposition, paths, permissions, and verification method before changing files.
- **Project ownership:** generated Skills and supporting assets belong to the consuming project and do not automatically track upstream changes.
- **Revision provenance:** record the exact Blueprint path and 40-character Git commit in every generated Skill.
- **Human authority:** keep approval boundaries explicit for generation, external writes, activation, and irreversible decisions.
- **Evidence-led promotion:** promote a Blueprint only after successful use in two different projects.

## Available Blueprints

| Blueprint | Status | Purpose | Use |
|---|---|---|---|
| `manage-focus-cycle` | In Progress | Generate project-local capabilities for managing one bounded Focus Cycle without inventing a final endpoint for the containing project. | [Install](blueprints/manage-focus-cycle/README.md) · [Contract](blueprints/manage-focus-cycle/BLUEPRINT.md) |
| `maintain-project-continuity` | In Progress | Generate project-local continuity capabilities that preserve work, decisions, evidence, and handoff across sessions, Agents, and models. | [Install](blueprints/maintain-project-continuity/README.md) · [Contract](blueprints/maintain-project-continuity/BLUEPRINT.md) |

See the [Blueprint index](blueprints/README.md) and each Blueprint's tracking issue.

## Use

Open the **Install** guide for the capability you want, copy its ready-to-use prompt, and give it to the AI already working in the target project. The guide starts a read-only inspection and proposal; project files are created only after you approve that proposal.

Use a `main` URL for the latest design. Replace `main` with an exact commit for reproducible instantiation. The AI must resolve and record the exact revision even when starting from `main`.

Generated Skills follow the target Agent's project-local discovery path. For example, Codex commonly uses `.agents/skills/<name>/` and Claude Code uses `.claude/skills/<name>/`. This repository does not install, update, or synchronize those files.

## Lifecycle

| Status | Meaning |
|---|---|
| Candidate | A repeated problem exists as an issue, but no Blueprint has been written. |
| In Progress | A Blueprint exists and generated results are being piloted in real projects. |
| Promoted | Two different projects have generated and used the capability successfully. |
| Deprecated | A replacement or retirement reason and consumer guidance are recorded. |

## Repository layout

```text
blueprints/    Canonical generative capability designs and evaluation scenarios
docs/          Architecture, decisions, and GitHub operating policy
scripts/       Repository-governance helpers only
.github/       Blueprint issue forms, labels, ownership, and pull-request guidance
```

Project-specific generated Skills, runtime implementations, credentials, session logs, and private Pilot artifacts do not belong here.

## Historical snapshot

The [`manage-focus-cycle-v0.1.0` GitHub Release](https://github.com/SWBaek/improvement-ai/releases/tag/manage-focus-cycle-v0.1.0) is an immutable historical snapshot of the retired installable-Skill approach. It is not the current distribution path and receives no updates from `main`.

Issues and pull requests are accepted without a support SLA. See [Contributing](CONTRIBUTING.md), [Security](SECURITY.md), [Architecture](docs/architecture.md), and the [MIT License](LICENSE).
