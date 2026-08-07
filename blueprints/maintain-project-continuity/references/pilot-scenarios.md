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

The Session Focus reaches a meaningful boundary. The Agent should update the authoritative Work Item and the single current Handoff with completed work, verification, exact resume point, unknowns, and references. Repeated Handoff operations must update the current record rather than create chronological session files.

## 8. Conflicting sources and Audit

The tracker says a Work Item is complete, tests fail, and a document describes an older implementation. Audit should remain read-only, show each source, timestamp and execution result, explain the impact, and propose corrections. It must not choose or modify the authoritative truth automatically.

## 9. Non-Git folder

A private local folder has no Git history. The generated capability should still preserve current Work Items, Decisions, and the latest Handoff in readable project-owned records. It must retain terminal and superseded records in place without inventing a session archive or database.

## 10. Cross-Agent handoff

One Agent initializes and updates the project, then a different Agent with no transcript receives the project. The second Agent should interpret the same Profile, IDs, statuses, authority, extensions, and source mappings; produce the first-stage Brief; and resume the human-selected Work Item without reconstructing a new management system.

## 11. Blueprint revision check

The repository has commits after installation, but some change only another Blueprint or README. The Agent should compare the Installation Receipt with the latest commit that changed this canonical Blueprint path, report the installation as current when those revisions match, and avoid a false update. When the path revision differs, it should compare the two exact Blueprint documents and update receipt and Skill provenance only after approved migration and successful verification.

## Review checklist

- The proposal is grounded in actual project records and approved before mutation.
- Integration and Migration are selected per area with no duplicate source of truth.
- Generated Profile and record schemas express the common Core without making JSON canonical.
- Multiple open Work Items and a human-selected Session Focus are distinct.
- Decision acceptance and Work Item completion remain human authority.
- Handoff stays singular and current; historical meaning stays in Work Items and Decisions.
- Audit reports conflicts without mutation.
- A new Agent recovers the exact resume point with bounded Context.
- Skill decomposition follows project evidence and every generated Skill records exact Blueprint provenance.
- Exactly one Installation Receipt matches every generated Skill and uses the canonical path's last-changing commit rather than repository HEAD.
- No database, service, renderer, hook, or new tracker is introduced without demonstrated need.
