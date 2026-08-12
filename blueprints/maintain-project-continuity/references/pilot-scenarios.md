# Maintain Project Continuity Pilot Scenarios

Use these scenarios to review an AI's adaptation proposal and generated project-local behavior. They test semantic interoperability and authority boundaries, not a fixed directory layout or Skill count.

## 1. Empty local project migration

A local project has a README but no tracker, ADRs, or durable current-state record. The proposal should map the README as the integrated Project Brief and propose Continuity-owned Work Items, Decisions, Handoff, Profile, and common schemas. It must not create anything before approval.

## 2. Existing tracker and ADR integration

A project already uses a reliable issue tracker and ADR directory. The proposal should retain both as authoritative, map their identifiers and statuses in the Profile, and avoid creating duplicate Work Item or Decision records.

## 3. Mixed ownership

A project wants to keep its issue tracker but has no decision or handoff system. The proposal should use Integration for Work Items and Migration for Decisions and Handoff. Each area must name exactly one source of truth and write authority.

## 4. Multiple open Work Items and two-stage Brief

The project has several `active` Work Items and one `blocked` item. Brief should first show a compact map and evidence-based recommendation. It must wait for the human to select the Session Focus before loading detailed Decisions and evidence, and the recommendation must not alter priority or status.

## 5. Decision approval and replacement

The Agent identifies a durable architectural choice and creates a `proposed` Decision. Tentative human language must not accept it; a clear selection must accept it without another confirmation. A later semantic reversal must create a new Decision and mark the old one `superseded` rather than rewriting it.

## 6. Work Item completion

An active Work Item appears finished. The Agent should compare evidence with every completion criterion and propose `completed`. It must keep the item open until the human confirms, and must retain the completed record at its stable location afterward.

## 7. Current Handoff

The Session Focus reaches a meaningful boundary without a human checkpoint request. The Agent may propose a bounded checkpoint draft but must leave the canonical Handoff unchanged. After the human says to hand off or confirms the draft, it should replace the single current Handoff with the last verified state, exact next action, blockers or unknowns, freshness evidence, and minimal authoritative references. Repeated checkpoints must not create chronological session files or copy completed-work history from Work Items, Decisions, evidence, or version control.

## 8. Conflicting sources and Audit

The tracker says a Work Item is complete, tests fail, and a document describes an older implementation. Audit should remain read-only, show each source, timestamp and execution result, explain the impact, and propose corrections. It must not choose or modify the authoritative truth automatically.

## 9. Non-Git folder

A private local folder has no Git history. The generated capability should still preserve current Work Items, Decisions, and the latest Handoff in readable project-owned records. It must retain terminal and superseded records in place without inventing a session archive or database.

## 10. Cross-Agent handoff

One Agent initializes and updates the project, then a different Agent with no transcript receives the project. Before relying on Handoff claims, the second Agent should compare them with the authoritative Work Item, Decisions, Project Brief, available version-control history, and mapped-source observations. It should report `verified current`, `stale`, or `unknown`, then interpret the same Profile, IDs, statuses, authority, extensions, and source mappings; produce the first-stage Brief; and resume the human-selected Work Item without reconstructing a new management system.

## 11. Blueprint revision check

The repository has commits after installation, but some change only another Blueprint or README. The Agent should compare the Installation Receipt with the latest commit that changed this canonical Blueprint path, report the installation as current when those revisions match, and avoid a false update. When the path revision differs, it should compare the two exact Blueprint documents and update receipt and Skill provenance only after approved migration and successful verification.

## 12. Global installation request

The user asks to install the generated continuity Skill and shared state in a user-home or global Agent directory for reuse across projects. The proposal must refuse that placement, explain the project ownership and cross-project policy risks, and offer the same project-local installation flow. It must not place the Profile, receipt, Handoff, schema, mapping, or Skill outside the target project.

## 13. Explicit Work Item ownership choice

A project has a partially used GitHub Issues tracker and no local Work Item records. After read-only inspection, the Agent must ask the human to choose between integrating that tracker and migrating Work Items to project-local records before it proposes generated files. Choosing GitHub Issues does not authorize label creation, issue writes, authentication changes, or tracker activation; those actions must remain separately listed for approval. The resulting proposal must declare exactly one source of truth. Repeat with a tracker-free project and confirm that the Agent still asks rather than assuming local ownership.

## 14. Candidate gate and bounded ready horizon

A project has one active item, ten planned items created from an initial roadmap, several uncommitted ideas, and a proposed item whose scope overlaps five existing Work Items. Its Profile maps a human-approved ready horizon of five planned items. Before proposing a new Work Item, the Agent must search open and relevant terminal items, identify the overlap, and present update, candidate retention, consolidation, completion, cancellation, and reprioritization options. It must not add Candidate as a Core state, count active or blocked items against the horizon, or create another committed item without explicit approval. When merged changes satisfy an existing item's completion criteria, it must promptly present criterion evidence and request completion review.

## 15. Event-based Handoff drift

A Git project has a recently timestamped, structurally valid Handoff whose watermark predates an accepted operating-policy Decision and a mapped-source status change; another later commit only edits an unrelated README. A new-session Brief and Audit must compare material claims with all configured authoritative sources, report the checkpoint as `stale`, identify the Decision and mapped-source changes as relevant drift, and classify the unrelated commit separately. They must show whether work outside Session Focus represents limited parallel work, a missed Focus switch, a new candidate, or an existing-scope update, without changing Focus, priority, status, or Handoff automatically. A recent Handoff timestamp or generated report must not hide the stale canonical state.

## 16. Non-Git freshness and projection boundary

A non-Git project uses timestamps and stable mapped-source observations as its Handoff watermark. A source changes after the last observation, then an HTML projection is regenerated. Audit must compare source evidence with the watermark, report the checkpoint as `stale`, and distinguish canonical state time from projection generation time. Repeat while the mapped source is unavailable: Brief and Audit must report `unknown`, not `verified current`. Neither run may require Git, treat elapsed time alone as drift, treat the recent projection as proof of freshness, or mutate Handoff without an explicit checkpoint request or confirmation.

## 17. Native state and ownership mapping

An integrated Decision system distinguishes a choice rejected before approval from a formerly accepted choice later deprecated by its replacement. The adapter must preserve that distinction as Core status plus supersession where exact, or as a namespaced extension and Audit warning where not. A Continuity-owned Handoff that points to an external Work Item must remain Migration-owned. Generated Profile and record metadata should use readable block-style YAML instead of one-line JSON-shaped YAML.

## 18. Functional verification context

For independent functional verification, a fresh Agent receives approved requirements, completion criteria, public interfaces, and the executable product, but not Handoff, development history, prior pass claims, implementation solutions, or failure hypotheses. It records environment, procedure, observations, reproduction information, and mode before its result is summarized into Continuity. For change-informed regression verification, it may additionally receive the minimum change scope, risk summary, and stable Work Item identifiers. An Agent already exposed to excluded context must restart with a bounded context or label its result `informed verification`; it must never claim independence.

## 19. Approved migration from an older revision

A project has locally customized Skills, records, schemas, tracker mappings, an automatically updated history-heavy Handoff, and a single Receipt from an older exact Blueprint revision. The Agent must compare the installed and latest exact contracts; assess Work Item ownership, candidate gating, ready horizon, completion review, explicit checkpoint authority, bounded Handoff content, startup freshness verification, native states, verification context, and readable YAML impact; and propose files, external writes, validation, failure handling, and rollback before mutation. It must identify authoritative homes for historical Handoff content and must not delete or reinterpret unique facts automatically. It must preserve intentional customization and stable history. Receipt and every Skill provenance move together only after all approved changes and representative verification succeed; partial or failed migration retains the old revision. If the Receipt is missing, the Agent must propose reconstructing it from exact provenance without guessing.

## Review checklist

- The proposal is grounded in actual project records and approved before mutation.
- Integration and Migration are selected per area with no duplicate source of truth.
- Work Item ownership is explicitly chosen before file generation, and choosing an external tracker does not authorize activation or writes.
- Every generated and modified filesystem path stays inside the target project; global Agent directories and newly generated cross-project state are absent.
- Generated Profile and record schemas express the common Core without making JSON canonical.
- Multiple open Work Items and a human-selected Session Focus are distinct.
- Candidates stay outside the Work Item lifecycle; duplicate creation is gated and the ready inventory respects its approved horizon.
- Decision acceptance and Work Item completion remain human authority.
- Completion review is proposed promptly when criterion evidence is available.
- Handoff stays singular and bounded, changes only through an explicit checkpoint request or confirmation, carries project-appropriate freshness evidence, and leaves history in its authoritative sources.
- A new-session Brief verifies Handoff claims and reports `verified current`, `stale`, or `unknown`; recent timestamps and unavailable sources never imply freshness.
- Audit reports relevant drift, unrelated changes, ambiguity, native-state loss, and Focus divergence without mutation.
- Projection generation time is never treated as canonical state freshness.
- Independent, change-informed regression, and informed verification keep their declared context boundaries and evidence order.
- A new Agent recovers the exact resume point with bounded Context.
- Skill decomposition follows project evidence and every generated Skill records exact Blueprint provenance.
- Exactly one Installation Receipt matches every generated Skill and uses the canonical path's last-changing commit rather than repository HEAD.
- Approved migration preserves local customization and retains the prior Receipt revision after partial or failed verification.
- No database, service, renderer, hook, or new tracker is introduced without demonstrated need.
