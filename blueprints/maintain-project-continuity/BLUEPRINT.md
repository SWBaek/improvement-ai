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

- let an Agent with no prior conversation recover the open Work Items, approved decisions, relevant evidence, and any confirmed exact resume point or its explicit absence;
- preserve a fixed semantic Core while mapping it to the target project's existing records and tools;
- select `integration` or `migration` independently for each information area without creating duplicate sources of truth;
- require the human to choose whether Work Items remain project-local or integrate a project-specific external tracker before generating either design;
- support multiple open Work Items and let the human select the Session Focus after a compact overview and recommendation;
- distinguish uncommitted candidates from approved Work Items, prevent duplicate creation, and keep the ready inventory within a human-approved project-specific horizon;
- keep project-owned canonical records readable without a dedicated service or a particular Agent provider;
- structurally validate project-local Profile and record metadata while keeping semantic conflicts visible for human review;
- keep one authoritative Handoff source that explicitly represents either no current checkpoint or one confirmed, bounded resume checkpoint, and verify checkpoint freshness before relying on it in a new session;
- preserve functional-verification independence by limiting development context according to a declared verification mode;
- record only durable, reusable outcomes rather than every conversation or tool result;
- keep operation count, generated files, and maintenance cost proportional to demonstrated project needs.

## Invariants

- Never create or migrate continuity records before a read-only inspection, concrete adaptation proposal, and human approval.
- Never generate a local Work Item design, activate an external tracker, or create an external Work Item before the human chooses Work Item ownership and approves the resulting design and external writes.
- Never maintain the same fact or state in both an existing source and a Continuity-owned record.
- Never treat Agent inference, auto-memory, a search index, generated JSON, or an HTML projection as an approved canonical fact.
- Never select the Session Focus on the human's behalf; recommendations do not change Work Item priority or status.
- Never mark a Work Item `completed` without presenting completion evidence and receiving human approval.
- Never promote an observation, idea, or possible follow-up into an authoritative Work Item without searching for an existing home and receiving human approval for creation or promotion.
- Never mark a Decision `accepted` without an explicit human choice. A clear choice in the normal conversation is approval and must not require a redundant confirmation.
- Never rewrite the meaning of an accepted Decision. Create a replacement Decision and preserve the supersession relation.
- Never resolve a meaningful disagreement between code, execution evidence, documents, or trackers automatically.
- Keep Audit read-only. Apply its proposed corrections only through a separately authorized change.
- Keep exactly one authoritative Handoff source or location. It must explicitly represent either no current checkpoint or one current human-confirmed checkpoint; absence, an actually blank document, and placeholder content are not empty-state representations. Do not create, replace, or clear a checkpoint canonically without an explicit human request or confirmation, and do not create a session-by-session Handoff archive by default.
- Never claim that verification was independent when the verifying Agent has already consumed excluded development history; use a fresh bounded context or label the result `informed verification`.
- Keep every generated Skill, Installation Receipt, Profile, schema, mapping, and state record inside the target project. Global Agent Skill locations, user-home installation, shared global configuration, and newly generated state shared across projects are prohibited. An existing project-specific external source may remain integrated under its own authority rules.
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
| Handoff | One authoritative location that explicitly represents either no current checkpoint or the latest human-confirmed resume checkpoint for the next Agent. A checkpoint contains Session Focus, last verified state, exact next action, blockers or unknowns, freshness evidence, and minimal authoritative references. |
| Historical record | A completed, cancelled, rejected, or superseded record retained at its stable location and omitted from the default Brief. |

### Ownership modes

For each information area, the Project Profile must declare one ownership mode:

- `integration`: retain an existing document, tracker, ADR collection, or equivalent as the only authoritative source and map it to the Core;
- `migration`: move the information into Continuity-owned project-local records and stop maintaining the previous source for that information.

The proposal may mix modes across areas. It must identify the source of truth and write authority for every integrated area, describe what will move for every migrated area, and reject any configuration that requires dual maintenance.

After read-only inspection and before proposing generated files, explicitly ask the human to choose the Work Item source of truth: Continuity-owned project-local records through Migration, or an existing or selected project-specific tracker such as GitHub Issues or Jira through Integration. Do not infer consent from the presence or absence of a tracker. Retaining an existing tracker does not authorize writes, and selecting a new external service does not authorize account setup, activation, authentication, or data creation. State those external actions separately and wait for approval under project policy.

The ownership declaration must follow canonical content rather than pointer location. A Continuity-owned Handoff remains Migration-owned even when its Session Focus points to an integrated external Work Item. For integrated Decisions, map native states without conflating a Decision rejected before acceptance with one previously accepted and later retired, deprecated, or replaced. Preserve an unrepresentable distinction in a namespaced extension and report it in Audit instead of silently projecting the wrong Core state.

### Canonical and derived representations

When Continuity owns an area, use a YAML Project Profile and Markdown records with limited YAML frontmatter. Prefer readable block-style YAML so authority, timestamps, mappings, and extensions remain easy to review and diff; JSON being a YAML subset is not a reason to use one-line JSON as canonical metadata. The Markdown body remains the human-auditable canonical content. Generate project-local JSON Schema for the Profile and common record envelope so Agents and tools can validate metadata consistently.

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

The Handoff schema or integrated-source validation must structurally distinguish an explicit empty state from a checkpoint. Require Session Focus, last verified state, exact next action, blockers or unknowns, freshness evidence, and minimal authoritative references only for the checkpoint representation. An empty or missing file, omitted mapped record, or prose placeholder must fail this distinction rather than silently mean no checkpoint.

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

An observation, idea, possible follow-up, or long-range initiative is a candidate, not another Core Work Item state. Before proposing a new Work Item, search open and relevant terminal records and show whether the smallest accurate action is to update an existing Work Item, retain a candidate in the project's existing intake, consolidate or supersede an item, or create a new bounded objective. Use an existing project-owned idea or intake source when available. If none exists and preservation is justified, propose the smallest project-local intake and its authority before creating it. Candidate intake must not duplicate Work Item status or appear in the default Brief as committed work.

The Profile must define a human-approved ready horizon for the target project without imposing a universal number. Count `planned` Work Items, or the integrated tracker's explicitly mapped ready query; do not count `active`, `blocked`, terminal records, or candidates. At the limit, do not create another Work Item automatically. First present completion, cancellation, consolidation, reprioritization, and candidate-retention options. A human may approve an evidenced exception. When a merge, representative verification, or another meaningful boundary appears to satisfy completion criteria, promptly present criterion-by-criterion evidence and request completion review rather than allowing finished Work Items to accumulate.

### Decision lifecycle

Use only `proposed`, `accepted`, `rejected`, and `superseded`. Create a Decision candidate when the choice will affect later work, is costly to reverse, cannot be reconstructed from code alone, or is necessary to prevent future Agents from repeating a failed direction. Do not record temporary implementation details or easily re-derived facts.

An accepted Decision must contain `Context`, `Decision`, and `Consequences`. External source references are optional when none exists; rationale is not optional. Record the approving role configured by the Profile rather than requiring a person's legal name or account identifier.

The Agent may write a `proposed` draft automatically. A clear human selection such as “use option 1” or “adopt this approach” authorizes `accepted`; tentative language does not. A semantic change creates a new accepted Decision that supersedes the old one. Only meaning-preserving corrections such as typos or broken links may edit an accepted record in place.

### Current Handoff

Maintain one stable authoritative Handoff source or location, not a continuously synchronized status record. It must explicitly contain either no current checkpoint or one bounded checkpoint. A checkpoint contains only the selected Session Focus, the last state verified against authoritative sources, the exact next action, current blockers or unknowns, project-appropriate freshness evidence, and the minimum references needed to resume. Keep completed-work history, Decision rationale, detailed verification evidence, and change logs in their authoritative Work Items, Decisions, evidence records, tracker, or version control rather than copying them into Handoff.

Use the explicit empty state after an approved initial installation when no checkpoint has yet been confirmed, or when the human requests or confirms clearing a checkpoint because there is no resume point to assert. Do not fabricate a checkpoint to populate the location. A lack of blockers, unusual details, or other special notes does not make an unfinished resume point empty. The empty state must be human-readable and structurally distinguishable from a missing, zero-length, malformed, or placeholder record.

Creating, replacing, or clearing a canonical Handoff checkpoint requires an explicit human request or confirmation at a useful boundary such as stopping, handing work to another Agent, switching Focus, completing a meaningful stage, or concluding that no resume point remains. Approval of an initial installation may authorize creating its proposed explicit empty state. The Agent may notice a boundary and present a concise checkpoint or clear draft, but must not silently mutate the canonical Handoff. A durable event may make the current checkpoint stale without creating an obligation to rewrite or clear it.

The Profile must define the project's durable-event categories and Handoff freshness watermark. In a Git project, the watermark may combine the last reflected commit with the latest reflected accepted or superseded Decisions and mapped-source observations. In a non-Git project, use timestamps plus stable evidence from mapped sources. Audit changes after the watermark and classify them as relevant drift, unrelated change, or unresolved ambiguity with supporting evidence. A durable Decision, Project Brief or operating-policy change, mapped source change, or meaningful work outside the selected Focus may make the Handoff stale; elapsed time, an unrelated commit, a meaning-preserving edit, or regenerated output alone does not.

At the start of a new session, first distinguish the explicit empty state from a checkpoint. Report a valid empty state as `no current checkpoint`, do not apply checkpoint freshness labels to it, and derive recommendations from authoritative Work Items, Decisions, the Project Brief, and other mapped sources. Before using checkpoint claims to recommend or resume work, compare its watermark and material claims with the authoritative Work Item, applicable Decisions, Project Brief or operating instructions, version-control history when available, and mapped-source observations. Report the checkpoint as `verified current`, `stale`, or `unknown`, with concise evidence. These are transient Brief and Audit outcomes, not new Core lifecycle states. Missing access, an incomplete watermark, or an unobservable mapped source requires `unknown`; never infer freshness from a recent Handoff timestamp. A `stale` or `unknown` checkpoint may still be shown as a historical resume proposal, but its claims must not be presented as current facts until verified.

Generated projections must distinguish their own generation time from the canonical state time and watermark. A recently generated HTML page, index, or report is never evidence that the underlying Handoff is current.

Use Git history when it exists. In a non-Git folder, a checkpoint or explicit empty state still replaces the previous Handoff representation; durable history belongs in retained Work Items and Decisions rather than a new session-log subsystem.

## Capability operations

These operations are required behavior, not fixed Skill names or boundaries:

1. **Initialize**: inspect instructions, project records, trackers, Agent clients, permissions, and Git availability without mutation. Ask the human to choose local or external Work Item ownership, then propose area-by-area ownership modes, mappings, candidate intake, ready horizon, the Handoff source and explicit empty representation, freshness evidence, generated files, migrations, approval roles, conflicts, and verification. When no checkpoint exists, include creation of the explicit empty state in the proposal rather than fabricating checkpoint content. Generate, activate, or migrate only after human approval.
2. **Brief**: first show every committed open Work Item as a compact one-line map, distinguish blocked items and the bounded ready inventory, and recommend a next item with evidence. Exclude candidates and terminal records. Report a valid empty Handoff as `no current checkpoint`; otherwise verify the checkpoint against authoritative sources and report `verified current`, `stale`, or `unknown` before relying on its claims. After the human selects the Session Focus, load only that item's details, applicable Decisions, evidence, and any bounded checkpoint; label unverified checkpoint claims rather than presenting them as current facts.
3. **Record Decision**: apply the durable-impact threshold, create a proposed record, recognize an explicit human choice as approval, and maintain rejection and supersession without rewriting history.
4. **Handoff**: when the human explicitly requests a checkpoint or confirms a proposed checkpoint draft, update the authoritative Work Item as separately authorized and replace the Handoff representation with verified state and an exact resume point. When the human requests or confirms a clear because no resume point remains, replace it with the explicit empty state. Keep checkpoints bounded and do not turn them into a chronological session archive. Without that request or confirmation, report that an existing checkpoint may become stale and leave the canonical representation unchanged.
5. **Prepare Verification**: before functional verification, ask the human to select `independent verification` or `change-informed regression verification`; use independent verification as the default only when an uncontaminated bounded context is possible. Independent verification may receive approved requirements, completion criteria, public interfaces, executable behavior, and observations gathered by the verifier, but not the current Handoff, development history, prior pass claims, implementation solution, or failure hypotheses. Change-informed regression verification may additionally receive the minimum change scope, risk summary, and stable Work Item identifiers, but not prior conclusions as evidence. If the Agent has already consumed excluded context and cannot restart cleanly, label the result `informed verification`. Record environment, procedure, observations, reproduction information, and context mode before summarizing the result into the Work Item or Handoff.
6. **Audit**: read all mapped and owned sources without mutation; report broken references, invalid transitions, duplicate authority, lossy native-state mappings, ready-horizon violations, supersession errors, stale state, Focus divergence, ungrounded claims, excessive context, and code/document/tracker conflicts with evidence and a proposed correction. Distinguish a valid explicit empty Handoff from a missing, actually blank, malformed, placeholder, mixed empty-and-checkpoint, or multiply authoritative representation. For a checkpoint, compare durable events with its watermark and distinguish relevant drift from unrelated changes and ambiguity. Never change Focus, priority, status, or canonical content automatically.

Capture, Query, Supersede, and Consolidate remain internal behaviors of these operations in v0.1. Generate a separate user-facing Skill only when the target project's triggers, permissions, or context make that split materially clearer.

## Project adaptation

Before proposing files, inspect:

- project and nested Agent instructions;
- README, plans, issue trackers, ADRs, research notes, experiment logs, generated documentation, and their write policies;
- each candidate source's authority, currentness, stable identifiers, and conflict behavior;
- existing candidate or idea intake, tracker grouping and dependency features, duplicate-search behavior, and the human-approved ready horizon;
- installed Agent clients and their project-local Skill discovery paths;
- the resolved target-project root and any path that would escape it or point to global Agent configuration;
- the human roles allowed to approve Decisions and Work Item completion;
- external write permissions, privacy constraints, Git availability, and existing validation tools;
- the existing Handoff representation, its authoritative source, explicit empty-state support, durable-event sources, available freshness watermarks, mapped-source observation limits, checkpoint and clear triggers, projection timestamps, and functional-verification context boundaries;
- evidence of scale or retrieval failure before proposing a database, service, graph, renderer, hook, or background process.

Prefer Integration when an existing source already carries the Core meaning reliably. Prefer Migration only when the human wants full transition or no adequate source exists. A Profile is an adapter and authority declaration, not a license to duplicate existing content.

## Instantiation protocol

### 1. Inspect without mutation

Read the target project's applicable instructions and relevant records. Do not create, edit, install, migrate, or delete anything.

### 2. Propose the local design

Present one compact proposal containing:

- evidence about existing records, Agent clients, validation, and permissions;
- an area-by-area Integration/Migration table with exactly one source of truth per area;
- the human's explicit Work Item ownership choice, candidate intake mapping, duplicate-creation gate, ready horizon, and exception authority;
- proposed Skill names, triggers, non-triggers, responsibilities, paths, and bundled resources;
- Profile fields, record locations, common schema location, authority roles, and extensions;
- the single project-local Blueprint Installation Receipt path;
- exact existing information to migrate and old sources that will stop receiving updates;
- external writes and every human approval boundary;
- the single Handoff source, explicit empty representation, checkpoint and clear authority, bounded checkpoint content, freshness evidence and startup behavior, native-state mappings, verification modes, and projection timestamp boundaries;
- one representative Brief, Decision, Handoff, Prepare Verification, and Audit scenario;
- every file that would be created or changed.

Reject any proposed path outside the target project and replace it with a project-local design. A request for global installation is not an approval exception for this capability.

Ask for human approval and do not treat silence as approval.

### 3. Generate after approval

Create only the approved project-local Skills, Profile, records, and schemas. Follow the target Agent's project-local discovery path; when no convention exists, use `<target-project>/.agents/skills/<name>/` for Codex and `<target-project>/.claude/skills/<name>/` for Claude Code. Never create or modify a global Skill location, user-home Skill directory, shared global config, or state outside the target project, even when the user requests convenience across projects.

Before generation, resolve the 40-character commit that most recently changed this canonical `BLUEPRINT.md` path. Reread the Blueprint from the exact commit URL; do not use the repository HEAD merely because the user supplied a `main` URL. Create exactly one project-local Installation Receipt at the approved path:

```yaml
format: improvement-ai-blueprint-installation/v1
blueprint: maintain-project-continuity
repository: https://github.com/SWBaek/improvement-ai
path: blueprints/maintain-project-continuity/BLUEPRINT.md
revision: <40-character-commit>
source: https://github.com/SWBaek/improvement-ai/blob/<40-character-commit>/blueprints/maintain-project-continuity/BLUEPRINT.md
```

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

Every generated Skill's provenance must match the Installation Receipt. Generated artifacts belong to the target project. Do not add upstream synchronization, silently overwrite local adaptations, or copy private project records back into `improvement-ai`.

### 4. Verify locally

Confirm that the target Agent discovers the generated Skills and that Profile and record metadata pass the approved project-local schemas. Exercise one representative operation and verify semantic invariants separately from schema validity. Report mapped authoritative sources, created or migrated records, human decisions still required, and remaining uncertainty.

## Reapplying a newer revision

Treat the commit that most recently changed this canonical `BLUEPRINT.md` path as the latest Blueprint revision; unrelated repository commits are not updates. Compare it with the Installation Receipt. Report `current` when equal, `update available` when different, and `unknown` when the latest path revision cannot be established.

When an update is available, inspect the existing local implementation and compare the two exact Blueprint documents. Present a semantic migration proposal before writes. Preserve intentional local behavior, schema extensions, IDs, record history, and authority mappings. Explicitly assess Work Item ownership, candidate intake and creation gates, ready horizon, completion review, the single Handoff source, explicit empty representation, checkpoint and clear authority, bounded checkpoint content, startup behavior, native-state mappings, verification context, and readable YAML impact when those semantics differ. Classify the existing Handoff as a confirmed checkpoint, placeholder or fabricated summary, history-heavy record, or unresolved content. Preserve and freshness-check a confirmed checkpoint. Propose converting a placeholder or fabricated summary to the explicit empty state. For a history-heavy record, identify authoritative homes for every unique fact before proposing a bounded checkpoint or empty state. If intent or unique content cannot be established, report the ambiguity and wait for human direction; never guess, delete, clear, or reinterpret automatically. Include Skill triggers, conditional schema validation, Brief and Audit behavior, external writes, failure handling, representative keep-checkpoint, clear-checkpoint, and empty-Brief verification, and rollback. Update the Installation Receipt and every Skill provenance together only after all approved changes and local verification succeed. If verification fails or the migration is partial, keep the prior revision in the Receipt and provenance. If the installation predates receipts, propose creation of one from existing exact provenance before migration. Never regenerate or overwrite automatically.

## Human authority

- The human approves the Initialize proposal before any project mutation or migration.
- The human chooses Work Item ownership, approves Candidate promotion or new Work Item creation, sets the ready horizon, and authorizes exceptions to it.
- The human selects the Session Focus after the first-stage Brief.
- The human explicitly requests or confirms creating, replacing, or clearing each canonical Handoff checkpoint; an Agent may propose a checkpoint or clear draft without mutating the current representation. Approval of an initial installation may include its proposed explicit empty state.
- The human's explicit choice accepts or rejects a proposed Decision.
- The human confirms Work Item completion after reviewing criterion evidence.
- The human authorizes corrections proposed by Audit and all external writes not already allowed by project policy.
- The human selects the functional-verification mode; external tracker setup, activation, authentication, and writes remain separately authorized.
- The Agent may update non-terminal Work Item progress when existing project authority allows it, but Handoff mutation remains a separate explicit checkpoint action.

## Non-goals

- Reproducing every conversation or giving an Agent unlimited human-like memory.
- Replacing the entire project roadmap, existing reliable tracker, ADR collection, or knowledge system.
- Turning every observation, idea, initiative, or implementation step into a Work Item, or adding Candidate as a Core Work Item state.
- Mandating a hosted service, database, vector search, knowledge graph, MCP server, background daemon, Git hook, HTML dashboard, or task manager.
- Fixing the number or names of generated Skills.
- Installing generated Skills, Profile, schema, mapping, receipt, or project state globally. A stateless cross-project Blueprint bootstrap would require a separate capability and is not an exception here.
- Making JSON or generated HTML the human-authoritative source.
- Automatically resolving conflicts, accepting Decisions, creating or completing Work Items, or writing to external systems.
- Claiming independent verification after excluded development context has already influenced the verifier.
- Centralizing consumer project records or generated variants in this repository.

## Acceptance

An instantiation is acceptable when:

- the proposal cites inspected project evidence and is approved before writes;
- every information area has exactly one declared source of truth and ownership mode;
- Work Item ownership is explicitly chosen, external activation remains separately authorized, and Handoff ownership matches its canonical content rather than its Session Focus target;
- every generated or modified filesystem path resolves inside the target project and no global Agent location or newly generated cross-project state is used;
- exactly one Installation Receipt identifies the path-scoped Blueprint revision and matches every generated Skill provenance;
- Profile and common record schema preserve the Core fields and namespaced extension boundary;
- multiple open Work Items can be summarized without forcing one project-wide active objective;
- candidates remain outside the committed Work Item lifecycle, duplicate creation is gated, and the ready inventory obeys its human-approved horizon or an explicit exception;
- a two-stage Brief ends with a human-selected Session Focus and bounded detailed Context;
- Decision approval and native-state mapping, supersession, Work Item creation and completion, conflict handling, and read-only Audit obey the authority rules;
- exactly one authoritative Handoff source or location distinguishes a human-readable explicit empty state from one bounded, human-confirmed checkpoint without using absence, a blank file, or placeholder prose as the empty representation;
- checkpoint fields and freshness evidence are required only for the checkpoint representation, while creating, replacing, and clearing a checkpoint obey the human authority boundary;
- a new session reports a valid empty state as `no current checkpoint`, or verifies material checkpoint claims against authoritative sources and reports `verified current`, `stale`, or `unknown` before relying on them;
- independent, change-informed regression, and informed verification are correctly distinguished, with evidence captured before Handoff summarization;
- an Agent without prior conversation can resume representative work from the project-owned sources when a checkpoint exists and can identify explicitly when none exists;
- generated Skills contain exact source revision provenance and pass the target project's discovery and validation checks;
- no runtime complexity was added without observed need and explicit approval.

Use [the Pilot scenarios](references/pilot-scenarios.md) to evaluate the proposal and generated behavior. Promotion requires successful generation and real use in two different projects. Record only privacy-safe, reusable evidence in tracking issue #21.

## Background

This Blueprint synthesizes lightweight ADR practice, file-based Agent memory patterns, spec persistence models, and local-first project records. Its delivery model follows this repository's generative Blueprint approach: preserve a strict semantic and authority contract while allowing the target project to choose local Skill boundaries and integrate existing sources.
