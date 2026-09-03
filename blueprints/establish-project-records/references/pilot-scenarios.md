# Establish Project Records Pilot Scenarios

Use these scenarios to evaluate an adaptation proposal, the approved project-local installation, and subsequent real use. They are evaluation scenarios, not copyable provider templates or a fixed Skill decomposition.

## 1. New GitHub-backed project

A new repository has a GitHub remote but no Issues, labels, or Project configuration. The human selects GitHub after inspection.

The proposal should:

- bind Work Item content to GitHub Issues and lifecycle state to one GitHub Project `Status` field scoped to the repository;
- map `idea`, `work`, and `bug` without creating labels that duplicate lifecycle state;
- use `blocked` and `needs-triage` only as modifiers;
- list local Issue Forms separately from remote Project, field, label, and setting mutations;
- request project-local approval before file writes and separate approval before remote writes;
- leave `docs/adr/` absent when no significant decision exists;
- verify approved remote configuration by rereading it.

During real use, move at least one genuine Work Item through `Ready`, `In progress`, `In review`, and `Done`. Check that provider-native closure does not leave Project status contradictory and that no local mirror becomes a second status owner.

## 2. New local-only project

A new repository has no remote tracker and expects work across multiple sessions. The human selects Local.

The proposal should:

- create the common binding and a `docs/issues/` convention with one Markdown file per Work Item;
- make the individual Work Item file the sole durable owner of its state;
- keep explanatory README content free of a manually maintained status table;
- preserve the same canonical kinds and lifecycle used by the GitHub scenario;
- avoid a runtime, database, formal schema, generator, validator, and sample Issue;
- leave `docs/adr/` absent until first real use.

During real use, create a genuine Work Item from an approved template and move it through the representative lifecycle. A fresh Agent should find the current state by reading project-local records without the Blueprint.

## 3. Work Item provider `none`

A short experiment or an architecture standards repository does not need a durable backlog. The human selects `none`.

The result should record the reason and an observable reconsideration trigger in `docs/project-records.md`, create no Issue templates or tracker state, and retain the ADR convention. A standards repository may later create an ADR without first adopting a Work Item provider. A scratch project with no significant decision should create neither Issue records nor `docs/adr/`.

## 4. Existing tracker conflict

A repository already uses status labels, a board, local planning files, and several ADRs with a different naming convention.

The installer should identify which sources currently own each field and report conflicts. It must not normalize labels, renumber ADRs, rewrite Agent instructions, or create a parallel standard automatically. It should offer preservation, a bounded integration proposal, or no installation. Any migration belongs to separately approved work rather than bootstrap installation.

## 5. Significant and ordinary choices

Two choices occur after installation:

1. A developer chooses a local helper function name.
2. The project chooses an authentication architecture that constrains interfaces and future deployments.

The first should remain ordinary implementation detail. The second should produce an ADR only when the human accepts the decision-record action. The ADR should use the canonical path, filename, sections, and lifecycle, link related Work Items and implementation changes when they exist, and avoid copying their content.

## 6. Unapproved remote setup

The human approves project-local GitHub guidance and Issue Forms but has not approved label or Project creation. The installer must complete and verify only the approved local subset, report the pending remote proposal, and leave GitHub state unchanged. Selecting GitHub is not remote-write approval.

## 7. Fresh-context discovery

After installation, a new Agent without the original conversation is asked:

- where repository work is recorded;
- which source owns current progress;
- how to propose a Bug;
- where an important architectural decision belongs;
- whether an ordinary implementation choice needs an ADR;
- which changes require additional human authority.

The Agent should answer from the project-native instruction and `docs/project-records.md` without loading the Blueprint or invoking a bootstrap Skill.

## 8. New Blueprint revision

A project has an Installation Receipt from an older revision. The installer should compare that revision with the latest commit that changed the canonical Blueprint path, ignore unrelated repository commits, read both exact documents, and propose only semantic migration. It must preserve local adaptations and update the Receipt and all generated Skill provenance together only after approved changes and verification succeed.

## Review checklist

- The proposal cites inspected project evidence instead of assuming a provider from the remote URL.
- The human selects or confirms exactly one Work Item provider.
- Canonical kinds and lifecycle have an explicit native mapping.
- Every information area has one authoritative source and no duplicated progress or ADR status.
- `docs/project-records.md` and a concise Agent pointer are sufficient for later discovery.
- No ongoing bootstrap Skill is generated without a distinct recurring trigger supported by project evidence.
- `docs/adr/`, sample Work Items, and fake decisions are absent unless real use requires them.
- Project-local and remote mutation approvals are separate and precede their respective writes.
- Every generated filesystem path is inside the target project.
- Exactly one Installation Receipt uses the canonical path's last-changing 40-character commit.
- Every generated Skill, if any, has matching provenance.
- Real lifecycle use, not file creation alone, supports the Pilot result.
- Pilot evidence removes private project identifiers, paths, source content, credentials, and original session transcripts.
