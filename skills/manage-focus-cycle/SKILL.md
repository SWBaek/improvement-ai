---
name: manage-focus-cycle
description: Establish, refresh, visualize, and close one bounded Focus Cycle inside a finite, long-lived, maintenance, or research project. Use when Codex needs to define the current short-term objective and completion or stop criteria, show current focus, evidence, progress, or decision readiness, or decide whether open-ended work should continue, close, or be replaced without inventing a final project endpoint. Do not use for an already-scoped implementation task, a generic whole-project roadmap, ordinary issue triage, or a one-off diagram or document.
---

# Manage Focus Cycle

Manage one bounded Primary Focus Cycle within a project that may continue indefinitely. Treat the Focus Cycle Workspace as a human-readable projection, not as the project source of truth or an input form.

## Invariants

- Never require a final endpoint for the containing project.
- Keep exactly one Primary Focus Cycle active; show other workstreams as context or deferred work.
- Define a Completion Contract before marking a Cycle Active.
- Do not invent numeric progress without a defensible denominator.
- Separate observed evidence, inference, unknowns, and human decisions.
- Never change completion criteria silently to keep work open.
- Use chat for confirmation and decisions; do not add response controls to HTML.

## Workflow

### 1. Inspect context

Read project instructions before other files. Identify project purpose, current work records, decision sources, issue tracker policy, generated-file rules, and relevant recent changes. Read [the Focus Cycle model](references/focus-cycle-model.md) before interpreting or changing a Cycle.

Classify the current work as delivery, maintenance, research, or decision work. This classification selects the progress representation; it does not change the core contract.

### 2. Resolve the durable record

Prefer the project-designated issue, decision log, planning document, SDOC, or equivalent authoritative source. Follow its required tooling and do not edit generated summaries directly.

If no suitable project-native record exists, create or update `docs/focus/focus-cycle.md` using the fallback format in the model reference. Create parent directories as needed.

Do not mutate an external issue tracker without the authorization and workflow required by the project. If external mutation is unavailable, record a local Focus Cycle that references the external source instead of pretending it was updated.

### 3. Choose the operation

- **Establish**: define a new objective and Completion Contract.
- **Refresh or review**: update evidence, progress, unknowns, current discussion, blockers, and readiness.
- **Close**: evaluate the contract and propose a closure outcome.
- **Replace**: close the current Cycle as superseded, then establish the next one.

If the user explicitly supplied both the objective and completion criteria, activate the Cycle. If either core element is inferred, record or render it as Proposed and request confirmation before activation.

### 4. Maintain the contract

Keep objective, why now, scope, exit criteria, review point or effort budget, expected decision or deliverable, and reopen condition visible. Treat new research questions as candidates for a later Cycle unless they block the current contract.

On refresh, compare evidence with each exit criterion. Mark the Cycle Blocked when a named dependency prevents progress and Ready to Close when the criteria support a closure decision.

On close, distinguish achieved, decision made, inconclusive, stopped, and superseded outcomes. Remaining uncertainty does not prevent closure unless the Completion Contract says it does. Always obtain human confirmation before recording Closed.

### 5. Render the Workspace

Read [the Workspace rendering guide](references/workspace-rendering.md), copy [the HTML shell](assets/focus-cycle-workspace.html), replace its placeholders, remove unused example structures, and write the current view to the stable OS temp path.

Render Project Context, Primary Focus Cycle, Completion Contract, Current Discussion, and Sources & Freshness on every invocation, including Proposed and closure-review states. Open the HTML in the available browser when possible.

### 6. Report in chat

State the Primary Focus Cycle, status, strongest evidence or blocker, requested human decision, durable record changed, and absolute Workspace path. Keep the chat summary short because the visual detail belongs in the Workspace.

## Safety

- Preserve unrelated user changes and project-native source conventions.
- Do not turn a long-term vision into a measurable final-project denominator.
- Do not report inferred state as observed fact.
- Do not broaden scope or extend research merely because another question exists.
- Do not publish or host the Workspace unless the user separately authorizes it.
- Do not commit, push, create issues, or modify external systems unless the user or project policy authorizes those actions.

## Completion

A run is complete when the durable record is unchanged or intentionally updated, the Workspace reflects the same Cycle and source freshness, required confirmation is explicit, and the user receives the current path and next decision.
