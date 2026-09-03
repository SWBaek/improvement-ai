# Establish Project Records Capability Blueprint

- Status: In Progress
- Tracking: [issue #72](https://github.com/SWBaek/improvement-ai/issues/72)
- Canonical path: `blueprints/establish-project-records/BLUEPRINT.md`

Use this Blueprint to establish a small, project-owned record system at the start of a repository. The installation itself is the one-time bootstrap: it binds repository work to one Work Item provider, declares a provider-independent Architecture Decision Record convention, and leaves durable local guidance that later humans and Agents can follow without this Blueprint or a continuing bootstrap runtime.

Do not copy a fixed implementation from this repository. Inspect the target project, preserve its instructions and ownership, propose the exact local and remote changes, and generate only the approved project-local result. The target implementation does not require an ongoing Skill when durable guidance and provider-native surfaces are sufficient.

## Problem

When one person moves among projects, each repository may put planned work, progress state, and architectural rationale in different places. An Agent can write to the wrong tracker, duplicate status across an Issue, labels, a board, and local Markdown, or leave a durable decision inside a transient conversation. Relearning these conventions creates context-switching cost even when the underlying workflow is similar.

The solution is not to put every personal reminder, completed change, and decision into one system. A project needs a small binding that distinguishes future repository work, durable decisions, personal next actions, and completed history while giving each information area one authoritative source.

## Required outcomes

The generated local capability must:

- provide one stable project-local entry point at `docs/project-records.md` for the repository's Work Item and ADR conventions;
- bind repository work to exactly one declared provider: GitHub, GitLab, Jira, Local, or `none`;
- use the same canonical Work Item kinds and lifecycle semantics across providers;
- identify the exact native surface that owns each Work Item field and state;
- keep completed implementation history in Git and merged change history rather than a parallel completion ledger;
- declare `docs/adr/` as the provider-independent location for durable architectural decisions;
- create no ADR directory or placeholder ADR until a significant decision actually needs a record;
- connect related Work Items, ADRs, and implementation changes by links without duplicating their content or state;
- leave enough project-local guidance for a new Agent to find and follow the system without loading this Blueprint or invoking a bootstrap Skill again;
- preserve human authority over provider selection, project-local writes, remote mutations, migration, and destructive changes.

## Canonical record semantics

### Work Items

Every supported provider must express these kinds:

- `idea`: a proposal that has not yet been approved for implementation;
- `work`: one approved, verifiable outcome;
- `bug`: reproducible behavior that differs from expected behavior.

Every Work Item must make its context or problem, desired outcome, scope, non-goals, verifiable completion conditions, dependencies or risks, and related evidence discoverable. A Bug also includes the environment, reproduction steps, expected behavior, and observed behavior when those facts are available.

The canonical lifecycle is:

```text
Inbox -> Backlog -> Ready -> In progress -> In review -> Done
```

`blocked` and `needs-triage` are modifiers, not additional progress states. A rejected, duplicate, obsolete, or intentionally abandoned item may close without reaching `Done`, but its disposition must remain visible. A milestone represents a real release or delivery scope, not progress state.

The provider binding may map these meanings to native fields, types, states, labels, or workflow transitions. It must document the mapping in `docs/project-records.md`. Project-specific classification may extend the binding only when it does not redefine or duplicate the canonical kinds and lifecycle.

### Architecture Decision Records

ADR storage does not vary with the Work Item provider:

```text
location: docs/adr/
filename: NNNN-kebab-case-title.md
status: Proposed | Accepted | Rejected | Superseded
sections: Context | Decision | Consequences
```

Create an ADR only for a decision that materially constrains later work, chooses among meaningful alternatives, is costly to reverse, or is likely to make a future maintainer ask why the choice was made. Keep task order, transient investigation, and ordinary implementation detail in the Work Item or normal project documentation.

An Accepted or Rejected ADR is historical evidence. Do not rewrite its meaning when the decision changes. Create a new ADR, mark the old record `Superseded`, and link both directions. Do not mirror ADR status in Work Item labels, a manually maintained status index, or another tracker.

### Record ownership

The binding must preserve these boundaries:

```text
repository work       -> selected Work Item provider
personal next action  -> personal work system, when one is used
completed change      -> Git and merged change history
durable decision      -> docs/adr/ in the project repository
```

A personal reminder may link to repository work but must not become a second backlog or state owner. A Work Item provider of `none` is valid for a short experiment or a decision-oriented repository; `docs/project-records.md` must state why it is sufficient and what observable condition should trigger reconsideration.

## Invariants

- Keep one authoritative source for each information area. Do not mirror progress state between a provider field, status label, local file, or manually maintained index.
- Keep all generated files inside the resolved target-project root. Do not install generated Skills, records, templates, configuration, or state in a user-home or global Agent location.
- Treat existing project instructions, tracker configuration, Issue forms, ADRs, Decision Logs, and generated-file rules as owned inputs. Do not overwrite, rename, renumber, migrate, or normalize them without a specific approved proposal.
- Inspect before proposing and obtain human approval before any project-local mutation.
- Selecting GitHub, GitLab, or Jira does not authorize authentication, activation, Project or board creation, label or field changes, workflow changes, or any other remote write. Propose remote mutations separately and execute only those explicitly approved.
- Do not create sample Work Items, placeholder ADRs, fake decisions, or empty operational directories merely to demonstrate installation.
- Do not require an ongoing bootstrap Skill, background service, database, generated status page, synchronization job, or upstream connection after installation.
- Preserve unrelated working-tree changes and target-project policy.
- Do not publish, commit, push, open or close Work Items, accept or supersede ADRs, or change external systems unless the user and target-project policy authorize the specific action.

## Capability operations

These are installation behaviors, not fixed Skill boundaries:

1. **Inspect**: discover project instructions, repository lifecycle, existing trackers, Work Item and decision records, Agent entry points, remotes, permissions, and conflicting conventions without mutation.
2. **Propose**: recommend one Work Item provider and exact native mapping, show alternatives when evidence is ambiguous, declare the ADR convention, list every local and remote change, and identify approval boundaries.
3. **Establish**: after approval, create or update the project-local binding, provider-native local templates, Agent pointer, and Installation Receipt; perform only separately approved remote mutations.
4. **Verify**: reread local and approved remote state, check source ownership and discoverability, and report drift, unresolved conflicts, and anything not applied.

The installation may generate no Skill when `docs/project-records.md`, the project's always-on Agent instruction, and native provider surfaces make the behavior discoverable. Generate a project-local Skill only when inspected project evidence shows a distinct recurring trigger or operation that durable guidance cannot serve. Never generate a Skill merely to wrap this one-time bootstrap.

## Project adaptation

Before proposing files, inspect:

- the target repository root, instructions, documentation layout, and Agent discovery conventions;
- its lifecycle and whether durable repository work is expected;
- existing remotes, hosted tracker configuration, Issue forms, labels, boards, Projects, workflows, local Issue files, plans, ADRs, and Decision Logs;
- which native field currently owns content, kind, progress, closure, priority, area, dependencies, and release scope;
- public intake, privacy, organization policy, generated-file rules, and required checks;
- permissions and tools required for remote reads and writes;
- all dirty or unrelated files that the installation must preserve.

Prefer a greenfield installation. If an existing record system would require migration or semantic replacement, stop after documenting the conflict and offer preservation, integration, or no-install options. Do not turn bootstrap installation into a migration project.

### GitHub profile

When GitHub is selected, prefer GitHub Issues for Work Item content and one GitHub Project scoped to the repository for canonical lifecycle `Status`. Use labels for kind or project-specific classification and for the `blocked` and `needs-triage` modifiers; do not create status labels that duplicate Project `Status`. Provider-native closure must not silently contradict the canonical lifecycle disposition.

The local proposal should normally consider:

```text
AGENTS.md
docs/project-records.md
.github/ISSUE_TEMPLATE/01-idea.yml
.github/ISSUE_TEMPLATE/02-work.yml
.github/ISSUE_TEMPLATE/03-bug.yml
.github/ISSUE_TEMPLATE/config.yml
.agents/blueprints/establish-project-records.yaml
```

Project creation, custom fields, workflow configuration, labels, Issue Form defaults, and repository settings are remote mutations. Read existing configuration first, present exact additions or changes, and request separate approval before applying them. Reread the remote state after each approved group of changes.

### Local profile

When Local is selected, prefer one Markdown file per Work Item under `docs/issues/`. The individual Work Item file owns its state. A README may explain discovery and creation but must not maintain a second status table. Listing is a directory scan or an on-demand projection, not another durable ledger.

The local proposal should normally consider:

```text
AGENTS.md
docs/project-records.md
docs/issues/README.md
docs/issues/_templates/idea.md
docs/issues/_templates/work.md
docs/issues/_templates/bug.md
.agents/blueprints/establish-project-records.yaml
```

Do not create an example Issue or introduce a runtime, database, formal schema, generator, or validator without observed need.

### GitLab, Jira, and `none`

For GitLab or Jira, inspect the available native types, workflow, fields, board, permissions, and project conventions. Propose an explicit semantic mapping and authority boundary, but do not invent provider automation or claim a tested fixed profile without evidence.

For `none`, create the common binding and Agent pointer but no Issue templates or tracker state. Record the reason and a reconsideration trigger. The ADR convention still applies and its directory remains absent until first use.

## Instantiation protocol

### 1. Inspect without mutation

Read the target-project instructions and relevant local records. Read remote tracker metadata only when access is already available and read-only inspection is authorized. Resolve the project root and reject any generated path that would escape it. Do not create, edit, install, delete, authenticate, activate, or configure anything during inspection.

### 2. Propose the binding

Present one compact proposal containing:

- inspected evidence and any unresolved conflict;
- the recommended Work Item provider and why, plus viable alternatives when the choice is ambiguous;
- the exact canonical-to-native kind and lifecycle mapping;
- the owner of content, state, modifiers, closure, dependencies, and release scope;
- the ADR location, threshold, naming, sections, lifecycle, and superseding behavior;
- the `docs/project-records.md` contents and Agent instruction pointer;
- every file to create or modify and every remote object or setting to create or modify;
- whether any continuing project-local Skill is justified, including its trigger, non-trigger, responsibility, and path;
- the single project-local Installation Receipt path;
- local and remote verification steps, rollback boundaries, and unresolved risks.

Ask the human to select or confirm the provider and approve the project-local proposal. Keep remote mutations in a separate approval group. Do not treat silence or provider selection as write approval.

### 3. Establish after approval

Before generation, resolve the 40-character commit that most recently changed this canonical `BLUEPRINT.md` path. Reread the Blueprint from the exact commit URL; do not use repository HEAD merely because the install entry point used a `main` URL.

Create exactly one project-local Installation Receipt at the approved path, normally `.agents/blueprints/establish-project-records.yaml`:

```yaml
format: improvement-ai-blueprint-installation/v1
blueprint: establish-project-records
repository: https://github.com/SWBaek/improvement-ai
path: blueprints/establish-project-records/BLUEPRINT.md
revision: <40-character-commit>
source: https://github.com/SWBaek/improvement-ai/blob/<40-character-commit>/blueprints/establish-project-records/BLUEPRINT.md
```

Create only approved project-local guidance and provider resources. Merge a concise pointer into the project-native Agent instruction without replacing unrelated instructions. Do not create `docs/adr/` until a real significant decision is being recorded.

If inspected evidence justifies a generated `SKILL.md`:

- use lowercase kebab-case for its directory and `name`;
- put only `name` and a concrete trigger-oriented `description` in YAML frontmatter;
- make ordinary work, generic project questions, and bootstrap-only setup explicit non-triggers;
- append this provenance comment using the same exact revision as the Installation Receipt:

```markdown
<!-- improvement-ai-blueprint
source: https://github.com/SWBaek/improvement-ai/blob/<40-character-commit>/blueprints/establish-project-records/BLUEPRINT.md
revision: <40-character-commit>
-->
```

Every generated Skill provenance must match the one Receipt. Generated files belong to the target project. Do not add automatic upstream synchronization or copy target-project output into `improvement-ai`.

After local generation succeeds, present the remote mutation group again if one was proposed. Execute only the approved subset and stop on authentication, permission, ownership, or semantic conflicts rather than broadening the change.

### 4. Verify

Reread every generated or modified local file and confirm:

- `docs/project-records.md` identifies the provider and every state owner without contradiction;
- the Agent instruction reaches the binding without copying the full policy;
- provider templates express the canonical kinds and required information;
- no local index, label, field, or document duplicates canonical progress or ADR state;
- no empty ADR directory, sample Work Item, placeholder, global file, runtime, or unapproved external state was created;
- exactly one Installation Receipt contains the canonical path's last-changing commit;
- every generated Skill, if any, has matching provenance and a justified recurring trigger.

For an approved remote setup, reread labels, fields, Project or board membership, workflow, and Issue Form defaults. Report any mismatch or partial application explicitly. Do not create fake Work Items to make verification pass.

## Reapplying a newer revision

Treat the commit that most recently changed this canonical `BLUEPRINT.md` path as the latest revision; unrelated repository commits are not updates. Compare it with the Installation Receipt and report `current`, `update available`, or `unknown`.

When an update is available, inspect the project-owned implementation and compare the two exact Blueprint documents. Present a semantic migration proposal, preserve intentional local behavior, and do not regenerate automatically. Update the Receipt and every generated Skill provenance together only after approved changes and verification succeed. If a migration is unnecessary, retain the installed revision.

## Non-goals

- Operating daily Work Item creation, triage, assignment, review, or closure.
- Automatically deciding that an implementation choice requires an ADR or accepting an ADR for the human.
- Managing personal reminders, meetings, research notes, handoffs, focus cycles, or complete project continuity.
- Migrating, renumbering, or normalizing an established tracker, Issue set, ADR log, or Decision Log.
- Synchronizing Work Items or ADRs across providers, repositories, wikis, databases, or global state.
- Requiring a global Skill, continuing project-local bootstrap Skill, service, CLI, package, schema, generator, validator, status page, or update daemon.
- Mandating GitLab or Jira automation before a real Pilot establishes it.
- Creating empty directories, sample records, or fake lifecycle activity as proof of installation.
- Copying provider templates or generated target-project output into this Blueprint repository.

## Acceptance

An instantiation is acceptable when:

- the proposal cites inspected target-project evidence and all writes follow the required approval boundaries;
- `docs/project-records.md` and a concise Agent pointer make Work Item and ADR ownership discoverable without this Blueprint;
- exactly one Work Item provider is declared and its native mapping preserves the canonical kinds and lifecycle;
- one authoritative owner exists for each progress and decision-state field;
- ADR policy uses the standard path, filename, sections, lifecycle, and superseding behavior without creating a placeholder;
- all generated paths resolve inside the target project and no global or new cross-project state exists;
- exactly one Installation Receipt records the canonical path's exact last-changing revision and matches all generated Skill provenance, if any;
- every remote mutation was separately approved and verified by rereading the resulting state;
- no existing record system, unrelated change, or project policy was silently replaced;
- later work can follow the installed binding without invoking a bootstrap Skill or consulting the Blueprint.

Use [the Pilot scenarios](references/pilot-scenarios.md) to evaluate proposals, generated artifacts, and real lifecycle use. Promotion requires maintainer-confirmed generation and real use in two different projects.

## Background

The initial evidence and open questions are preserved in the [Project Records Bootstrap Idea](../../docs/idea/project-records-bootstrap.md). The ADR convention follows Michael Nygard's [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) and the accepted-record lifecycle described by [AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html). The separation between a fixed semantic contract and project-native implementation is intentionally narrower than the paused [Maintain Project Continuity Blueprint](../maintain-project-continuity/BLUEPRINT.md).
