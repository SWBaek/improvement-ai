# Contributing

Issues and pull requests are welcome. `improvement-ai` is a maintainer-led Capability Blueprint repository with no support or review SLA. Start by choosing the contribution route below; not every useful observation needs to become a Blueprint.

## Choose your contribution

| Contribution | Start here | Issue required |
|---|---|---|
| Typo, broken link, or meaning-preserving clarification | Direct pull request | No |
| Research or benchmark evidence | `docs/research/` pull request | No |
| Early, non-normative capability idea | `docs/idea/` pull request | Optional |
| New Capability Blueprint | Blueprint proposal issue | Yes |
| Existing Blueprint contract change | Its tracking issue or a feature issue | Yes |
| Pilot evidence | Comment on the Blueprint tracking issue | No new issue |
| Repository identity, lifecycle, or policy change | Feature issue and, when required, a new ADR | Yes |
| Security vulnerability | GitHub private vulnerability report | Never use a public issue |

A direct documentation pull request that turns out to change an invariant, operation, authority boundary, lifecycle, or public contract must stop and move to an issue-first route.

## Capability lifecycle

```text
Idea note
  → Candidate issue
  → In Progress Blueprint and tracking issue
  → Promoted after two independent real-project Pilots
  → Deprecated when replaced or retired
```

- **Idea** explores a problem or hypothesis without promising implementation.
- **Candidate** records a repeated problem, target contexts, invariants, authority, and Pilot conditions in an issue.
- **In Progress** has a canonical Blueprint and is being generated and used in real projects.
- **Promoted** requires maintainer-confirmed evidence from two different target projects.
- **Deprecated** retains the canonical path with a replacement or retirement explanation.

Repeated runs in one project strengthen one Pilot; they do not count as a second independent project.

## Contribution requirements

### Idea

An Idea note must distinguish the problem, observations, current hypothesis, non-goals, risks, validation questions, and sources. It is not a decision, Candidate issue, or implementation promise. Follow the guidance in [`docs/idea/README.md`](docs/idea/README.md).

Every Idea note and its index row must use exactly one of these states and record `Last reviewed` plus a concrete `Next trigger`:

- `Exploring`: active investigation;
- `Parked`: intentionally paused until the stated resume condition;
- `Promoted`: continued in a linked issue or Blueprint;
- `Dropped`: deliberately closed with a recorded reason.

Do not copy Blueprint or Pilot execution status back into a promoted Idea. Preserve the original exploration context and link to the canonical Blueprint and tracking issue instead.

### Research and benchmarks

Research must state the research date, purpose, comparison criteria, primary sources, limitations, and implications for the current strategy. Keep observed evidence separate from inference. Research does not change a Blueprint contract by itself.

### New Blueprint

Search existing open and closed issues, then use the [Capability Blueprint proposal form](https://github.com/SWBaek/improvement-ai/issues/new?template=blueprint_proposal.yml). Do not create a speculative Blueprint directory before the proposal is accepted as a Candidate.

An In Progress Blueprint contribution includes:

- a human install entry point at `blueprints/<name>/README.md`;
- the canonical English contract at `blueprints/<name>/BLUEPRINT.md`;
- English Pilot scenarios under directly linked `references/`;
- the Blueprint index and tracking issue links;
- project-local generation, Installation Receipt, path-scoped revision, human authority, and no-global-install invariants.

Do not add an installable Skill, runtime, CLI, package, formal schema, generator, central adapter, project-specific output, or Release machinery.

### Existing Blueprint change

Link the tracking or feature issue and describe:

- required outcome or invariant changes;
- project adaptation freedom that changes;
- human authority or external-write changes;
- impact on existing project-local installations and migration needs;
- the new path-scoped Blueprint revision created by changing `BLUEPRINT.md`.

Meaning-preserving corrections may use a direct pull request. If a correction changes generated behavior or requires consumer migration, it is a contract change.

### Repository policy

Repository identity, lifecycle, installation, versioning, or public governance changes require an issue. Add a new ADR when the change establishes a long-lived decision; do not edit an accepted ADR to change its historical meaning. Link superseded decisions from the new ADR.

### AI-assisted contributions

AI-assisted contributions are allowed. The submitter remains responsible for understanding and reviewing the content, checking claims and sources, respecting licenses, removing sensitive information, and reporting the checks actually run. “AI generated it” is not evidence of correctness.

## Pilot evidence

Submit Pilot evidence as a comment on the Blueprint's existing tracking issue using the [Pilot evidence template](docs/github/pilot-evidence.md). Successful, failed, and inconclusive use are all valuable.

- The project and contributor may remain anonymous.
- Remove private repository names, paths, code, credentials, original session logs, and identifiable business data.
- Report the exact path-scoped Blueprint revision and enough adaptation evidence for the maintainer to judge interoperability.
- The maintainer decides whether two submissions represent independent projects and whether the contract, triggers, and authority boundaries are stable enough for Promotion.

## Language policy

- Canonical `BLUEPRINT.md` files and Pilot scenarios are written in English.
- Capability install READMEs and repository governance documents keep their established primary language.
- Update `README.md` and `README.ko.md` together when user-visible meaning changes.
- Preserve contract terms, state names, operation names, and field names when translation could change their meaning.

## Sources, licenses, and privacy

- Link external ideas and explain why they are relevant.
- Check the license before copying text, templates, code, or assets; attribution alone does not grant permission.
- Prefer paraphrase and original analysis over copying.
- Never commit credentials, private project artifacts, raw session logs, personal paths, or identifiable Pilot material.
- Use the private vulnerability reporting path described in [SECURITY.md](SECURITY.md) for exploitable behavior.

## Pull requests

Keep each pull request focused on one contribution route. Complete the pull request template, link required issues, and explain both the human-visible outcome and the adaptation freedom left to target projects.

Minimum checks:

1. Review every changed local link.
2. Run `git diff --check`.
3. Run the label-sync dry run only when label definitions change.
4. Confirm no runtime, installable Skill, formal schema, generated project output, secret, or private Pilot evidence was added.
5. Confirm generated capability guidance remains project-local, uses one Installation Receipt, and prohibits global installation.

Agents operating in this repository follow `AGENTS.md`: use authenticated `gh` for GitHub service operations and never place tokens in commands, files, logs, or commits.

## Review and acceptance

Maintainers may merge overlapping ideas, narrow scope, keep a proposal in Idea stage, request additional Pilot evidence, or reject runtime and abstraction proposals that lack repeated failure evidence. Negative evidence is not a failed contribution.

Only a maintainer confirms Promoted status after reviewing evidence from two independent real projects. A merged Blueprint is In Progress, not proven complete.
