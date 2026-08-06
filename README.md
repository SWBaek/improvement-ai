# improvement-ai

> A fast-moving portfolio of reusable AI collaboration capabilities, refined through real project use and shared as Agent Skills.

[한국어](README.ko.md)

`improvement-ai` is not one application or service. It is the canonical source for small, composable workflows discovered while working with AI: start with a Skill, validate it in real projects, and add deterministic scripts, packages, frameworks, or separate services only when evidence justifies them.

## Principles

- **Skill first:** begin with the smallest reusable Agent Skill.
- **Real use before abstraction:** promote capabilities based on observed project use, not speculative generality.
- **One source:** maintain common capability sources here and keep client-specific adapters thin.
- **Human-readable outcomes:** use concise text, tables, diagrams, or HTML according to the decision being reviewed.
- **Proportionate verification:** keep only tests that protect real Skill behavior and add broader checks after failures justify them.

## Capability lifecycle

| Status | Meaning |
|---|---|
| Candidate | A real problem exists, but the reusable workflow is not yet clear. |
| In Progress | A Skill is being piloted and refined in real work. |
| Promoted | Repeated use has confirmed its value, triggers, and safeguards. |
| Deprecated | The capability has a documented replacement or retirement reason. |

Capability maturity comes from Pilot evidence. GitHub Releases are optional snapshots, not a required step for every change.

## Available Skills

| Skill | Status | Primary client | Purpose |
|---|---|---|---|
| [`manage-focus-cycle`](skills/manage-focus-cycle/SKILL.md) | In Progress | Codex | Manage one bounded Focus Cycle inside finite, long-lived, maintenance, or research projects. |

`manage-focus-cycle` defines a Completion Contract, keeps one Primary Focus Cycle, renders a safe temporary HTML Workspace, and closes work without inventing a final endpoint or whole-project completion percentage. See [GitHub Releases](https://github.com/SWBaek/improvement-ai/releases) and [tracking issue #10](https://github.com/SWBaek/improvement-ai/issues/10).

## Install and use

Use the current `skills` installer for discovery and installation. The Workspace renderer uses Python 3.13. Codex is the primary client; other Agent Skills clients are best effort until real use demonstrates a need for broader support.

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

The installer tracks content changes on the Git ref originally installed. Default installs follow the latest development state on `main`; version tags are deliberate, reproducible snapshots. Watch this repository's GitHub Releases to receive snapshot notifications.

## Repository layout

```text
skills/        Agent Skills and their bundled runtime resources
tools/         Independent automation that supports capabilities
packages/      Installable CLI and package sources
frameworks/    Versioned contracts proven to be shared by capabilities
configs/       Common configuration and client adapters
external/      External source, version, and license records
scripts/       Small maintenance helpers justified by repeated use
tests/         Skill behavior tests that protect real user outcomes
docs/          Architecture, decisions, and issue policy
```

Project-specific implementations, credentials, session logs, caches, and regenerable runtime output do not belong here.

## Optional local check

```powershell
python -m unittest tests.test_manage_focus_cycle -v
```

Issues and pull requests are welcome without a support SLA. Read [CONTRIBUTING.md](CONTRIBUTING.md), report vulnerabilities through the private path described in [SECURITY.md](SECURITY.md), and review the [MIT license](LICENSE).

## Maintainer documentation

- [Agent operating rules](AGENTS.md)
- [Repository architecture](docs/architecture.md)
- [Architecture decisions](docs/decisions/)
- [GitHub Issue standard](docs/github/issues.md)
- [GitHub repository settings](docs/github/repository-settings.md)
