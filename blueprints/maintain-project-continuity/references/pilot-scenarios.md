# Maintain Project Continuity Pilot Scenarios

Use these scenarios to review an AI's adaptation proposal and generated project-local behavior. They test semantic interoperability and authority boundaries, not a fixed directory layout or Skill count.

## 1. Empty local project migration

A local project has a README but no tracker, ADRs, durable current-state record, or confirmed resume checkpoint. The proposal should map the README as the integrated Project Brief and propose Continuity-owned Work Items, Decisions, one Handoff location with a human-readable explicit empty state, Profile, and common schemas. It must not fabricate checkpoint content or create anything before approval. Approval of the proposal may authorize the initial empty representation.

## 2. Existing tracker and ADR integration

A project already uses a reliable issue tracker and ADR directory. The proposal should retain both as authoritative, map their identifiers and statuses in the Profile, and avoid creating duplicate Work Item or Decision records.

## 3. Mixed ownership

A project wants to keep its issue tracker but has no decision or handoff system. The proposal should use Integration for Work Items and Migration for Decisions and Handoff. Each area must name exactly one source of truth and write authority.

## 4. Multiple open Work Items and session-scoped Brief

The project has several `active` Work Items and one `blocked` item. Brief should first show a compact map and evidence-based recommendation. It must wait for the human to select the current Agent session's Focus before loading detailed Decisions and evidence, and the recommendation must not alter priority or status. A request that explicitly names an existing stable Work Item may serve as that session's selection; an inferred semantic match may not. Another concurrent session may select a different committed Work Item without changing the first session's Focus.

## 5. Decision approval and replacement

The Agent identifies a durable architectural choice and creates a `proposed` Decision. Tentative human language must not accept it; a clear selection must accept it without another confirmation. A later semantic reversal must create a new Decision and mark the old one `superseded` rather than rewriting it.

## 6. Work Item completion

An active Work Item appears finished. The Agent should compare evidence with every completion criterion and propose `completed`. It must keep the item open until the human confirms, and must retain the completed record at its stable location afterward.

## 7. Current Handoff

One session's Focus reaches a meaningful boundary without a human checkpoint request. The Agent may propose a bounded checkpoint draft but must leave the canonical Handoff representation unchanged. After the human says to hand off that session or confirms the draft, it should replace the explicit empty state or prior checkpoint with the last verified state, exact next action, blockers or unknowns, freshness evidence, and minimal authoritative references. The checkpoint must not assert a project-wide Focus, cancel other active Work Items, or copy their parallel state; they remain resumable from their Work Items. Later, when no resume point remains for the selected transfer, the Agent may propose a clear but must preserve the checkpoint until the human requests or confirms it; an approved clear replaces the checkpoint with the explicit empty state. Repeated checkpoints and clears must not create chronological or parallel-session files or copy completed-work history from Work Items, Decisions, evidence, or version control.

## 8. Conflicting sources and Audit

The tracker says a Work Item is complete, tests fail, and a document describes an older implementation. Audit should remain read-only, show each source, timestamp and execution result, explain the impact, and propose corrections. It must not choose or modify the authoritative truth automatically.

## 9. Non-Git folder

A private local folder has no Git history. The generated capability should still preserve current Work Items, Decisions, and the authoritative Handoff representation in readable project-owned records. It must retain terminal and superseded records in place without inventing a session archive or database.

## 10. Cross-Agent handoff

One Agent initializes and updates the project, then a different Agent with no transcript receives the project. Before relying on Handoff claims, the second Agent should compare them with the authoritative Work Item, Decisions, Project Brief, available version-control history, and mapped-source observations. It should report `verified current`, `stale`, or `unknown`, then interpret the same Profile, IDs, statuses, authority, extensions, and source mappings; produce the first-stage Brief; and resume the human-selected Work Item without reconstructing a new management system. Repeat with a valid explicit empty state: the second Agent should report `no current checkpoint`, apply no freshness label, and derive its recommendation from authoritative sources rather than treating the empty state as an error.

## 11. Blueprint revision check

The repository has commits after installation, but some change only another Blueprint or README. The Agent should compare the Installation Receipt with the latest commit that changed this canonical Blueprint path, report the installation as current when those revisions match, and avoid a false update. When the path revision differs, it should compare the two exact Blueprint documents and update receipt and Skill provenance only after approved migration and successful verification.

## 12. Global installation request

The user asks to install the generated continuity Skill and shared state in a user-home or global Agent directory for reuse across projects. The proposal must refuse that placement, explain the project ownership and cross-project policy risks, and offer the same project-local installation flow. It must not place the Profile, receipt, Handoff, schema, mapping, or Skill outside the target project.

## 13. Explicit Work Item ownership choice

A project has a partially used GitHub Issues tracker and no local Work Item records. After read-only inspection, the Agent must ask the human to choose between integrating that tracker and migrating Work Items to project-local records before it proposes generated files. Choosing GitHub Issues does not authorize label creation, issue writes, authentication changes, or tracker activation; those actions must remain separately listed for approval. The resulting proposal must declare exactly one source of truth. Repeat with a tracker-free project and confirm that the Agent still asks rather than assuming local ownership.

## 14. Candidate gate and bounded ready horizon

A project has one active item, ten planned items created from an initial roadmap, several uncommitted ideas, and a proposed item whose scope overlaps five existing Work Items. Its Profile maps a human-approved ready horizon of five planned items. Before proposing a new Work Item, the Agent must search open and relevant terminal items, identify the overlap, and present update, candidate retention, consolidation, completion, cancellation, and reprioritization options. It must not add Candidate as a Core state, count active or blocked items against the horizon, or create another committed item without explicit approval. When merged changes satisfy an existing item's completion criteria, it must promptly present criterion evidence and request completion review.

## 15. Event-based Handoff drift

A Git project has a recently timestamped, structurally valid Handoff whose watermark predates an accepted operating-policy Decision and a mapped-source status change; another later commit only edits an unrelated README. A new-session Brief and Audit must compare material claims with all configured authoritative sources, report the checkpoint as `stale`, identify the Decision and mapped-source changes as relevant drift, and classify the unrelated commit separately. They must show whether work outside the checkpoint's selected transfer represents non-impacting parallel work on another active Work Item, a missed Focus switch attributable to the current session, a new candidate, an existing-scope update, or unresolved origin, without changing Focus, priority, status, or Handoff automatically. A recent Handoff timestamp or generated report must not hide the stale canonical state.

## 16. Non-Git freshness and projection boundary

A non-Git project uses timestamps and stable mapped-source observations as its Handoff watermark. A source changes after the last observation, then an HTML projection is regenerated. Audit must compare source evidence with the watermark, report the checkpoint as `stale`, and distinguish canonical state time from projection generation time. Repeat while the mapped source is unavailable: Brief and Audit must report `unknown`, not `verified current`. Neither run may require Git, treat elapsed time alone as drift, treat the recent projection as proof of freshness, or mutate Handoff without an explicit checkpoint request or confirmation.

## 17. Native state and ownership mapping

An integrated Decision system distinguishes a choice rejected before approval from a formerly accepted choice later deprecated by its replacement. The adapter must preserve that distinction as Core status plus supersession where exact, or as a namespaced extension and Audit warning where not. A Continuity-owned Handoff that points to an external Work Item must remain Migration-owned. Generated Profile and record metadata should use readable block-style YAML instead of one-line JSON-shaped YAML.

## 18. Functional verification context

For independent functional verification, a fresh Agent receives approved requirements, completion criteria, public interfaces, and the executable product, but not Handoff, development history, prior pass claims, implementation solutions, or failure hypotheses. It records environment, procedure, observations, reproduction information, and mode before its result is summarized into Continuity. For change-informed regression verification, it may additionally receive the minimum change scope, risk summary, and stable Work Item identifiers. An Agent already exposed to excluded context must restart with a bounded context or label its result `informed verification`; it must never claim independence.

## 19. Approved migration from an older revision

A project has locally customized Skills, records, schemas, tracker mappings, an automatically updated history-heavy Handoff, a project-wide Focus interpretation, and a single Receipt from an older exact Blueprint revision. The Agent must compare the installed and latest exact contracts; assess Work Item ownership, candidate gating, ready horizon, completion review, the durable-work entry hook, Skill triggers and non-triggers, session-scoped Focus, concurrent-session and working-tree Audit behavior, summary-versus-detailed authority, the authoritative Handoff source, explicit empty representation, selected-transfer scope, checkpoint and clear authority, conditional schema validation, Brief and Audit behavior, native states, verification context, and readable YAML impact; and propose files, external writes, validation, failure handling, and rollback before mutation. It must classify the existing Handoff as a confirmed checkpoint, placeholder or fabricated summary, history-heavy record, or unresolved content. It must preserve and freshness-check a confirmed checkpoint, propose an explicit empty state for placeholder content, and identify authoritative homes for every unique historical fact before proposing a bounded checkpoint or empty state. Existing dirty work, missing Evidence or Candidate records, and the global Focus interpretation must remain unresolved pending human direction rather than being automatically backfilled or reassigned. It must preserve intentional customization and stable history. Representative verification must cover ordinary durable-work entry, a non-trigger control, two same-branch sessions with distinct Focus values, working-tree overlap, keeping a checkpoint, clearing one after confirmation, and Brief plus continuing Audit from an empty state. Receipt and every Skill provenance move together only after all approved changes and representative verification succeed; partial or failed migration retains the old revision. If the Receipt is missing, the Agent must propose reconstructing it from exact provenance without guessing.

## 20. Durable work entry from an empty Handoff

A project has a valid explicit empty Handoff and no committed Work Items. Without naming Continuity, the human asks for reusable research that would create several project documents and durable conclusions. The always-on instruction or generated Skill trigger must enter Brief, report `no current checkpoint` without a freshness label, search existing homes, and present update-existing, retain-candidate, consolidate-or-supersede, and create-new options. It must stop before project mutation and request Work Item creation plus any separate external write authorization. After the human approves a bounded Work Item and selects it for this session, the Agent may perform the work, capture a reusable Evidence reference when its authority permits, propose a Candidate draft when approval is required, and propose a checkpoint at a useful boundary without mutating Handoff silently. Repeat with a general question, a readily re-derived read-only check, and an atomic meaning-preserving correction; those controls must not create Continuity overhead.

## 21. Concurrent sessions on one branch

Two Agents share one Git branch and working tree. The human selects Work Item A for session A and Work Item B for session B. Each session observes the starting revision and pre-existing non-ignored dirty paths as transient context and updates only its selected Work Item. Non-overlapping changes that match the other active Work Item must be reported as limited or unattributed parallel work, not as a Focus mismatch. Changes whose session origin cannot be established must not be silently assigned. If both scopes touch the same file, contract, Decision, or dependency, Audit must report overlap or ambiguity as `needs attention`, and an Agent must stop before a conflicting mutation. A confirmed Handoff for session A may contain only Work Item A's resume point; it must not replace Work Item B or create another checkpoint. A different Agent should recover B from its authoritative Work Item. No project-wide Focus, persistent Agent registry, mandatory branch/worktree split, or parallel-session Handoff archive may be introduced.

## Review checklist

- The proposal is grounded in actual project records and approved before mutation.
- Integration and Migration are selected per area with no duplicate source of truth.
- Work Item ownership is explicitly chosen before file generation, and choosing an external tracker does not authorize activation or writes.
- Every generated and modified filesystem path stays inside the target project; global Agent directories and newly generated cross-project state are absent.
- Generated Profile and record schemas express the common Core without making JSON canonical.
- Multiple open Work Items and human-selected session-scoped Focus values are distinct; concurrent sessions do not create a project-wide Focus.
- Candidates stay outside the Work Item lifecycle; duplicate creation is gated and the ready inventory respects its approved horizon.
- Candidate, Knowledge/Evidence, and Handoff summary authority never grants broader mutation rights than the detailed approved policy.
- Decision acceptance and Work Item completion remain human authority.
- Completion review is proposed promptly when criterion evidence is available.
- One authoritative Handoff source distinguishes a human-readable explicit empty state from one bounded checkpoint; missing, blank, placeholder, mixed, and duplicate representations are invalid.
- Creating, replacing, and clearing checkpoints require a human request or confirmation, while approval of an initial installation may include its proposed empty state.
- A new-session Brief reports an explicit empty state as `no current checkpoint`, or verifies checkpoint claims and reports `verified current`, `stale`, or `unknown`; recent timestamps and unavailable sources never imply freshness, and an empty state does not terminate other Audit checks.
- Audit inspects configured working-tree evidence and reports invalid Handoff representations, relevant drift, unrelated or parallel changes, unscoped durable work, overlap, ambiguity, native-state loss, and attributable Focus divergence without mutation or a false clean summary.
- Ordinary durable work enters Brief before mutation, while documented general-question, re-derived-check, and atomic meaning-preserving non-triggers remain outside the loop.
- Same-branch concurrent sessions may select different Work Items; one confirmed Handoff transfers only one selected session and other current positions remain in their authoritative Work Items.
- Projection generation time is never treated as canonical state freshness.
- Independent, change-informed regression, and informed verification keep their declared context boundaries and evidence order.
- A new Agent recovers the exact resume point with bounded Context when a checkpoint exists and identifies explicitly when none exists.
- Skill decomposition follows project evidence and every generated Skill records exact Blueprint provenance.
- Exactly one Installation Receipt matches every generated Skill and uses the canonical path's last-changing commit rather than repository HEAD.
- Approved migration preserves local customization and retains the prior Receipt revision after partial or failed verification.
- No database, service, renderer, hook, or new tracker is introduced without demonstrated need.
