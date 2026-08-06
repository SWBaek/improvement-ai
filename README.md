# improvement-ai

> A versioned portfolio of reusable AI collaboration capabilities, proven in real projects and distributed as Agent Skills.

[한국어](README.ko.md)

`improvement-ai` is not one application or service. It is the canonical source for small, composable workflows discovered while working with AI: start with a Skill, validate it in real projects, and add deterministic scripts, packages, frameworks, or separate services only when evidence justifies them.

## Principles

- **Skill first:** begin with the smallest reusable Agent Skill.
- **Real use before abstraction:** promote capabilities based on observed project use, not speculative generality.
- **One source:** maintain common capability sources here and keep client-specific adapters thin.
- **Human-readable outcomes:** use concise text, tables, diagrams, or HTML according to the decision being reviewed.
- **Safe, verifiable distribution:** declare triggers, non-triggers, expected outcomes, versions, dependencies, and checks.

## Capability lifecycle

| Status | Meaning |
|---|---|
| Candidate | A real problem exists, but the reusable workflow is not yet clear. |
| In Progress | A Skill is being piloted and refined in real work. |
| Promoted | Repeated use has confirmed its value, triggers, and safeguards. |
| Deprecated | The capability has a documented replacement or retirement reason. |

Release maturity and capability maturity are independent. A public `0.x` release can remain `In Progress` until pilot evidence supports promotion.

## Available Skills

| Skill | Version | Status | Supported client | Purpose |
|---|---:|---|---|---|
| [`manage-focus-cycle`](skills/manage-focus-cycle/SKILL.md) | 0.1.0 | In Progress | Codex | Manage one bounded Focus Cycle inside finite, long-lived, maintenance, or research projects. |

`manage-focus-cycle` defines a Completion Contract, keeps one Primary Focus Cycle, renders a safe temporary HTML Workspace, and closes work without inventing a final endpoint or whole-project completion percentage. See [release history](docs/releases/manage-focus-cycle.md) and [tracking issue #10](https://github.com/SWBaek/improvement-ai/issues/10).

## Install and use

Node.js 22.20 or later is required by the tested `skills` installer. The Workspace renderer requires Python 3.13. Codex is the verified client; other Agent Skills clients are currently unverified.

List and install the Skill for one project:

```powershell
npx skills@latest add SWBaek/improvement-ai --list
npx skills@latest add SWBaek/improvement-ai --skill manage-focus-cycle --agent codex -y
```

Invoke it explicitly in a new Codex session:

```text
$manage-focus-cycle Establish the current bounded objective and completion contract, then open the visual Workspace.
```

Update an existing project or global installation:

```powershell
npx skills@latest update manage-focus-cycle --project -y
npx skills@latest update manage-focus-cycle --global -y
```

The installer tracks content changes on the Git ref originally installed. Default installs follow `main`; version tags provide reproducible installs and rollback points. Watch this repository's GitHub Releases to receive release notifications.

## Repository layout

```text
skills/        Agent Skills and their bundled runtime resources
tools/         Independent automation that supports capabilities
packages/      Installable CLI and package sources
frameworks/    Versioned contracts proven to be shared by capabilities
configs/       Common configuration and client adapters
external/      External source, version, and license records
scripts/       Repository validation and release automation
tests/         Contract and behavior verification
docs/          Architecture, decisions, issue policy, and release history
```

Project-specific implementations, credentials, session logs, caches, and regenerable runtime output do not belong here.

## Validate and contribute

```powershell
python scripts/validate_repository.py
python -m unittest discover -s tests -p "test_*.py" -v
```

Issues and pull requests are welcome without a support SLA. Read [CONTRIBUTING.md](CONTRIBUTING.md), report vulnerabilities through the private path described in [SECURITY.md](SECURITY.md), and review the [MIT license](LICENSE).

## Maintainer documentation

- [Agent operating rules](AGENTS.md)
- [Repository architecture](docs/architecture.md)
- [Skill release policy](docs/releases/README.md)
- [Architecture decisions](docs/decisions/)
- [GitHub Issue standard](docs/github/issues.md)
- [GitHub repository settings](docs/github/repository-settings.md)
