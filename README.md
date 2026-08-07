# improvement-ai

> Do not install our solution. Give its contract to the AI already inside your project.

[한국어](README.ko.md)

`improvement-ai` distributes **Capability Blueprints**, not universal Skills. A Blueprint fixes the problem, semantic contract, required operations, authority boundaries, and acceptance evidence while leaving implementation to the AI that can inspect the real project. That AI reuses the project's existing records, proposes only the missing local capability, and creates it after human approval.

## What makes this different

Most Skill and workflow repositories ship one implementation and ask every project to adopt or configure it. This repository ships the smallest contract from which an AI can generate a different, project-owned implementation without losing the capability's essential meaning.

```text
Conventional distribution
upstream Skill / CLI / framework
  → copy the same implementation into projects
  → configure adapters
  → keep following upstream

improvement-ai
exact-revision Blueprint
  → the target project's AI inspects local reality
  → it proposes Integration, Migration, Skill boundaries, paths, and permissions
  → the human approves
  → the project owns the generated capability
```

This creates a deliberate boundary:

- **The contract is shared; the implementation is not.** Two projects may generate different Skills and files while preserving the same invariants and operations.
- **Existing systems win.** Mature issues, ADRs, research notes, and project instructions are integrated instead of duplicated; migration occurs only when the human chooses it.
- **The project remains sovereign.** Generated Skills, state, schemas, mappings, and receipts stay inside the target project. There is no global installation or upstream synchronization.
- **AI adaptation remains reviewable.** Inspection is read-only, the complete installation proposal comes before mutation, and important decisions remain human authority.
- **Every installation is reproducible.** One Installation Receipt and each generated Skill identify the exact commit that last changed the canonical Blueprint.
- **A design earns stability through use.** A Blueprint is promoted only after different projects generate and operate it successfully.

The approach was motivated by Andrej Karpathy's `llm-wiki.md`: a compact idea file can be more reusable than a fixed implementation when it gives an AI strong invariants and operations. `improvement-ai` generalizes that pattern into a governed portfolio of project-scoped capabilities. See the [ecosystem benchmark and strategy review](docs/research/bencmark/karpathy-llm-wiki-ecosystem.md).

## Operating principles

- **Blueprint, not product:** preserve the problem, invariants, operations, adaptation points, and acceptance criteria rather than one universal implementation.
- **Inspect before designing:** ground every proposal in the target project's instructions, records, tools, and Agent clients.
- **Propose before writing:** show the Skill decomposition, paths, permissions, and verification method before changing files.
- **Project ownership:** generated Skills and supporting assets belong to the consuming project and do not automatically track upstream changes.
- **No global installation:** every generated Skill, receipt, profile, schema, mapping, and state record stays inside the target project.
- **Revision provenance:** treat the last commit that changed the canonical Blueprint path as its version, and record it in one project-local Installation Receipt and every generated Skill.
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

Use a `main` URL to discover the latest design. Before generation, the AI resolves the last commit that changed that Blueprint's canonical `BLUEPRINT.md`, rereads the exact URL, and records that 40-character revision in the target project. Unrelated repository commits do not make an installation outdated.

Generated Skills follow the target Agent's project-local discovery path. For example, Codex commonly uses `.agents/skills/<name>/` and Claude Code uses `.claude/skills/<name>/`. Global Agent Skill directories and shared paths outside the project are prohibited. This repository does not install, update, or synchronize generated files.

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

## Contributing

Start with the [contribution route table](CONTRIBUTING.md): small documentation, Research, and non-normative Ideas may go directly to a pull request, while new Blueprints and contract or repository-policy changes are issue-first. Submit privacy-safe real-use results to the existing tracking issue with the [Pilot evidence template](docs/github/pilot-evidence.md). Maintainers confirm Promotion only after evidence from two independent projects.

## Historical snapshot

The [`manage-focus-cycle-v0.1.0` GitHub Release](https://github.com/SWBaek/improvement-ai/releases/tag/manage-focus-cycle-v0.1.0) is an immutable historical snapshot of the retired installable-Skill approach. It is not the current distribution path and receives no updates from `main`.

Issues and pull requests are accepted without a support SLA. See [Contributing](CONTRIBUTING.md), [Security](SECURITY.md), [Architecture](docs/architecture.md), and the [MIT License](LICENSE).
