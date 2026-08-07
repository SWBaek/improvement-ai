# Maintain Project Continuity Capability Blueprint

- Status: In Progress
- Tracking: [issue #21](https://github.com/SWBaek/improvement-ai/issues/21)
- Canonical path: `blueprints/maintain-project-continuity/BLUEPRINT.md`

Use this Blueprint to design project-owned Agent Skills and supporting records that preserve a project's current work, approved decisions, reusable evidence, and exact resume point across sessions, Agents, and models. Do not copy a fixed implementation from this repository. Inspect the target project, propose how its existing sources map to the Continuity Core, and create project-local artifacts only after human approval.

## Problem

AI session context is finite and may lose details during compaction. A new Agent or model does not automatically inherit the current work state, prior decision rationale, failed approaches, or next action. This is especially costly in local or private projects that do not use a hosted issue service.

Agent-specific memory is useful but cannot be the project's authoritative continuity source: it may be product- or machine-bound, its selection process may be opaque, and it may mix Agent inference with human-approved facts. The project needs a small, auditable, provider-independent continuity contract rather than a transcript archive or unlimited AI memory.

## Required outcomes

The generated local capability must:

- let an Agent with no prior conversation recover the open Work Items, approved decisions, relevant evidence, and exact resume point;
- preserve a fixed semantic Core while mapping it to the target project's existing records and tools;
- select `integration` or `migration` independently for each information area without creating duplicate sources of truth;
- support multiple open Work Items and let the human select the Session Focus after a compact overview and recommendation;
- keep project-owned canonical records readable without a dedicated service or a particular Agent provider;
- structurally validate project-local Profile and record metadata while keeping semantic conflicts visible for human review;
- record only durable, reusable outcomes rather than every conversation or tool result;
- keep operation count, generated files, and maintenance cost proportional to demonstrated project needs.

## Invariants

- Never create or migrate continuity records before a read-only inspection, concrete adaptation proposal, and human approval.
- Never maintain the same fact or state in both an existing source and a Continuity-owned record.
- Never treat Agent inference, auto-memory, a search index, generated JSON, or an HTML projection as an approved canonical fact.
- Never select the Session Focus on the human's behalf; recommendations do not change Work Item priority or status.
- Never mark a Work Item `completed` without presenting completion evidence and receiving human approval.
- Never mark a Decision `accepted` without an explicit human choice. A clear choice in the normal conversation is approval and must not require a redundant confirmation.
- Never rewrite the meaning of an accepted Decision. Create a replacement Decision and preserve the supersession relation.
- Never resolve a meaningful disagreement between code, execution evidence, documents, or trackers automatically.
- Keep Audit read-only. Apply its proposed corrections only through a separately authorized change.
- Keep exactly one current Handoff unless the target project already has an authoritative equivalent. Do not create a session-by-session Handoff archive by default.
- Preserve completed, cancelled, rejected, and superseded records in place; exclude them from the default Brief rather than deleting or moving them.
- Do not collect credentials, private transcript history, or sensitive data without an explicit project policy.

## Continuity Core

Every generated implementation must preserve these meanings even when an existing project uses different names or physical files.

| Information area | Required meaning |
|---|---|
| Project Brief | Stable project purpose, scope, constraints, and operating instructions. |
| Work Item | One bounded objective with completion criteria, current position, next actions, blockers, and verification evidence. |
| Session Focus | The human-selected Work Item for the current session; it is not a second durable task record. |
| Decision | One durable choice with context, outcome, consequences, approval authority, and replacement history. |
| Knowledge/Evidence reference | A reference to reusable research, experiments, failures, or observations without copying their authoritative source. |
| Handoff | The current point-in-time briefing for the next Agent: Session Focus, completed work, verification, resume point, unknowns, and references. |
| Historical record | A completed, cancelled, rejected, or superseded record retained at its stable location and omitted from the default Brief. |

### Ownership modes

For each information area, the Project Profile must declare one ownership mode:

- `integration`: retain an existing document, tracker, ADR collection, or equivalent as the only authoritative source and map it to the Core;
- `migration`: move the information into Continuity-owned project-local records and stop maintaining the previous source for that information.

The proposal may mix modes across areas. It must identify the source of truth and write authority for every integrated area, describe what will move for every migrated area, and reject any configuration that requires dual maintenance.

### Canonical and derived representations

When Continuity owns an area, use a YAML Project Profile and Markdown records with limited YAML frontmatter. The Markdown body remains the human-auditable canonical content. Generate project-local JSON Schema for the Profile and common record envelope so Agents and tools can validate metadata consistently.

JSON interchange, HTML, full-text indexes, embeddings, and graphs are derived projections. Do not require or generate them unless the project has a demonstrated consumer or failure that justifies their maintenance. This Blueprint does not contain a formal schema, template, generator, or validator to copy.

### Common metadata contract

The generated project-local schema must keep Core fields at the top level and permit project- or domain-specific metadata only under a namespaced `extensions` object. At minimum, records must represent:

- schema version;
- stable record ID and Core type;
- allowed status for that type;
- creation and last-update timestamps;
- authority, including the Profile-defined approving role when approval applies;
- `supersedes` references;
- optional source and evidence references;
- namespaced extensions.

Schema validation covers shape and allowed values. Audit must separately check referenced-record existence, supersession cycles, actual approval evidence, ownership conflicts, and stale state. Do not create type-specific schemas until Pilot evidence shows that the common envelope is insufficient.

Continuity-owned Work Items use monotonically increasing, non-reused identifiers such as `WI-0001`; Decisions use `DR-0001`. Integrated records keep their existing stable identifiers.

### Work Item lifecycle

Allow multiple Work Items to be open at once. Use only these states in the v0.1 Core:

```text
planned → active → completed
             ↕
          blocked

any open state → cancelled
```

Do not add `paused`; move an intentionally deferred item to `planned` and record the reason. An Agent may update progress, blockers, next actions, and verification evidence at a meaningful work boundary. It may only propose `completed`, show evidence against every completion criterion, and wait for human confirmation.

### Decision lifecycle

Use only `proposed`, `accepted`, `rejected`, and `superseded`. Create a Decision candidate when the choice will affect later work, is costly to reverse, cannot be reconstructed from code alone, or is necessary to prevent future Agents from repeating a failed direction. Do not record temporary implementation details or easily re-derived facts.

An accepted Decision must contain `Context`, `Decision`, and `Consequences`. External source references are optional when none exists; rationale is not optional. Record the approving role configured by the Profile rather than requiring a person's legal name or account identifier.

The Agent may write a `proposed` draft automatically. A clear human selection such as “use option 1” or “adopt this approach” authorizes `accepted`; tentative language does not. A semantic change creates a new accepted Decision that supersedes the old one. Only meaning-preserving corrections such as typos or broken links may edit an accepted record in place.

### Current Handoff

Maintain one current Handoff containing the selected Session Focus, last completed work, verification results, exact resume point, unresolved risks, and relevant record or source references. Update it, together with the affected Work Item, when work starts or changes status, a meaningful stage finishes, a blocker appears or clears, verification changes the next action, or the session switches or stops. Do not update it for ordinary conversation without a durable state change.

Use Git history when it exists. In a non-Git folder, the latest Handoff still replaces the previous Handoff; durable history belongs in retained Work Items and Decisions rather than a new session-log subsystem.

## Capability operations

These operations are required behavior, not fixed Skill names or boundaries:

1. **Initialize**: inspect instructions, project records, trackers, Agent clients, permissions, and Git availability without mutation. Propose area-by-area ownership modes, mappings, generated files, migrations, approval roles, conflicts, and verification. Generate or migrate only after human approval.
2. **Brief**: first show every open Work Item as a compact one-line map, distinguish blocked items, and recommend a next item with evidence. After the human selects the Session Focus, load only that item's details, applicable Decisions, evidence, and current Handoff.
3. **Record Decision**: apply the durable-impact threshold, create a proposed record, recognize an explicit human choice as approval, and maintain rejection and supersession without rewriting history.
4. **Handoff**: at a meaningful work boundary, update the authoritative Work Item and the single current Handoff with verified state and an exact resume point. Do not turn Handoff into a chronological session archive.
5. **Audit**: read all mapped and owned sources without mutation; report broken references, invalid transitions, duplicate authority, supersession errors, stale state, ungrounded claims, excessive context, and code/document/tracker conflicts with evidence and a proposed correction.

Capture, Query, Supersede, and Consolidate remain internal behaviors of these operations in v0.1. Generate a separate user-facing Skill only when the target project's triggers, permissions, or context make that split materially clearer.

## Project adaptation

Before proposing files, inspect:

- project and nested Agent instructions;
- README, plans, issue trackers, ADRs, research notes, experiment logs, generated documentation, and their write policies;
- each candidate source's authority, currentness, stable identifiers, and conflict behavior;
- installed Agent clients and their project-local Skill discovery paths;
- the human roles allowed to approve Decisions and Work Item completion;
- external write permissions, privacy constraints, Git availability, and existing validation tools;
- evidence of scale or retrieval failure before proposing a database, service, graph, renderer, hook, or background process.

Prefer Integration when an existing source already carries the Core meaning reliably. Prefer Migration only when the human wants full transition or no adequate source exists. A Profile is an adapter and authority declaration, not a license to duplicate existing content.

## Instantiation protocol

### 1. Inspect without mutation

Read the target project's applicable instructions and relevant records. Do not create, edit, install, migrate, or delete anything.

### 2. Propose the local design

Present one compact proposal containing:

- evidence about existing records, Agent clients, validation, and permissions;
- an area-by-area Integration/Migration table with exactly one source of truth per area;
- proposed Skill names, triggers, non-triggers, responsibilities, paths, and bundled resources;
- Profile fields, record locations, common schema location, authority roles, and extensions;
- exact existing information to migrate and old sources that will stop receiving updates;
- external writes and every human approval boundary;
- one representative Brief, Decision, Handoff, and Audit verification scenario;
- every file that would be created or changed.

Ask for human approval and do not treat silence as approval.

### 3. Generate after approval

Create only the approved project-local Skills, Profile, records, and schemas. Follow the target Agent's discovery path; when no convention exists, use `.agents/skills/<name>/` for Codex and `.claude/skills/<name>/` for Claude Code. Do not use a global Skill location.

For every generated `SKILL.md`:

- use lowercase kebab-case for the directory and `name`;
- place only `name` and a concrete trigger-oriented `description` in YAML frontmatter;
- make non-triggers explicit and keep detailed variants in progressively loaded references;
- preserve the Core semantics and human authority regardless of Skill decomposition;
- append this provenance comment after resolving the Blueprint to an exact 40-character commit:

```markdown
<!-- improvement-ai-blueprint
source: https://github.com/SWBaek/improvement-ai/blob/<40-character-commit>/blueprints/maintain-project-continuity/BLUEPRINT.md
revision: <40-character-commit>
-->
```

Generated artifacts belong to the target project. Do not add upstream synchronization, silently overwrite local adaptations, or copy private project records back into `improvement-ai`.

### 4. Verify locally

Confirm that the target Agent discovers the generated Skills and that Profile and record metadata pass the approved project-local schemas. Exercise one representative operation and verify semantic invariants separately from schema validity. Report mapped authoritative sources, created or migrated records, human decisions still required, and remaining uncertainty.

## Reapplying a newer revision

When adopting a newer Blueprint revision, inspect the existing local implementation and recorded revision. Present a semantic comparison and migration proposal before writes. Preserve intentional local behavior, schema extensions, IDs, record history, and authority mappings. Never regenerate or overwrite automatically.

## Human authority

- The human approves the Initialize proposal before any project mutation or migration.
- The human selects the Session Focus after the first-stage Brief.
- The human's explicit choice accepts or rejects a proposed Decision.
- The human confirms Work Item completion after reviewing criterion evidence.
- The human authorizes corrections proposed by Audit and all external writes not already allowed by project policy.
- The Agent may update non-terminal Work Item state and the current Handoff without an extra prompt at a meaningful work boundary.

## Non-goals

- Reproducing every conversation or giving an Agent unlimited human-like memory.
- Replacing the entire project roadmap, existing reliable tracker, ADR collection, or knowledge system.
- Mandating a hosted service, database, vector search, knowledge graph, MCP server, background daemon, Git hook, HTML dashboard, or task manager.
- Fixing the number or names of generated Skills.
- Making JSON or generated HTML the human-authoritative source.
- Automatically resolving conflicts, accepting Decisions, completing Work Items, or writing to external systems.
- Centralizing consumer project records or generated variants in this repository.

## Acceptance

An instantiation is acceptable when:

- the proposal cites inspected project evidence and is approved before writes;
- every information area has exactly one declared source of truth and ownership mode;
- Profile and common record schema preserve the Core fields and namespaced extension boundary;
- multiple open Work Items can be summarized without forcing one project-wide active objective;
- a two-stage Brief ends with a human-selected Session Focus and bounded detailed Context;
- Decision approval, supersession, Work Item completion, conflict handling, and read-only Audit obey the authority rules;
- only one current Handoff exists and it identifies an exact resume point;
- an Agent without prior conversation can resume representative work from the project-owned sources;
- generated Skills contain exact source revision provenance and pass the target project's discovery and validation checks;
- no runtime complexity was added without observed need and explicit approval.

Use [the Pilot scenarios](references/pilot-scenarios.md) to evaluate the proposal and generated behavior. Promotion requires successful generation and real use in two different projects. Record only privacy-safe, reusable evidence in tracking issue #21.

## Background

This Blueprint synthesizes lightweight ADR practice, file-based Agent memory patterns, spec persistence models, and local-first project records. Its delivery model follows this repository's generative Blueprint approach: preserve a strict semantic and authority contract while allowing the target project to choose local Skill boundaries and integrate existing sources.
