# Focus Cycle Model

Use this model to separate a long-lived Project from the bounded work that can actually be completed.

## Core hierarchy

```text
Project
└─ Primary Focus Cycle
   └─ Current Discussion
```

- **Project**: durable context, purpose, constraints, and workstreams. It may have no final endpoint.
- **Primary Focus Cycle**: the one short-term objective currently receiving coordinated attention.
- **Current Discussion**: the question, comparison, evidence review, or decision that advances the Cycle now.

Other workstreams may be important, but list them as context, deferred, or blocking dependencies rather than co-equal active Cycles.

## Lifecycle

| Status | Meaning | Allowed transition |
|---|---|---|
| Proposed | Objective or Completion Contract needs human confirmation | Active, discarded |
| Active | Contract is confirmed and work is progressing | Blocked, Ready to Close, Closed |
| Blocked | A named dependency prevents meaningful progress | Active, Ready to Close, Closed |
| Ready to Close | Evidence supports a closure decision | Active, Closed |
| Closed | Human confirmed an outcome and residual unknowns | Reopen only when the recorded condition occurs |

Use a closure outcome separate from status: `achieved`, `decision-made`, `inconclusive`, `stopped`, or `superseded`. Explain the outcome in project language rather than forcing these English tokens into project-native records.

## Completion Contract

A usable contract answers:

- What bounded objective is being pursued?
- Why is it the Primary Focus now?
- What is explicitly in and out of scope?
- Which observable criteria permit closure?
- What review date, evidence threshold, or effort budget limits the Cycle?
- What decision, artifact, or learning outcome should closure produce?
- Which future condition justifies reopening?

For research, do not use complete understanding as a criterion. Prefer hypothesis resolution, evidence sufficiency, bounded risk, decision readiness, a documented inconclusive result, or an explicit cost-versus-value stopping rule.

If the user supplied an objective but the exit criteria are inferred, keep the Cycle Proposed. Changes to an Active contract require explicit human acknowledgment and a recorded reason.

## Progress by work mode

- **Delivery**: completion criteria, milestones, verified outputs, and blockers.
- **Maintenance**: current release or maintenance objective, issue set, service health, and regression risk.
- **Research**: resolved questions, evidence quality, tested hypotheses, remaining decision-critical unknowns, and decision readiness.
- **Decision**: alternatives eliminated, constraints satisfied, unresolved tradeoffs, and decision authority.

Only show a percentage when the denominator is stable and meaningful. Otherwise use criterion states, evidence coverage, readiness, or milestone position.

## Durable source precedence

1. Follow `AGENTS.md` and project-specific operating policy.
2. Use the explicitly designated issue, decision log, plan, mission document, SDOC, or equivalent source.
3. Never edit a generated summary when its source or update command is identified.
4. If no suitable record exists, use `docs/focus/focus-cycle.md`.

External sources may be referenced read-only. Update them only through authorized tools and project policy.

## Fallback document

Keep the fallback concise and machine-maintainable. Adapt labels to the project language.

```markdown
# Focus Cycle

- Status: Proposed | Active | Blocked | Ready to Close | Closed
- Mode: delivery | maintenance | research | decision
- Updated: ISO-8601 timestamp

## Project Context

Long-lived purpose and relevant workstreams. Do not add whole-project completion.

## Primary Objective

Bounded objective and why it is primary now.

## Scope

- In:
- Out:

## Completion Contract

- [ ] Observable exit criterion
- Review point or effort budget:
- Expected decision, artifact, or learning outcome:
- Reopen condition:

## Evidence and Progress

Observed evidence mapped to the criteria; separate inference and unknowns.

## Current Discussion

Current question, options, blockers, and requested human decision.

## Closure

Outcome, residual unknowns, next Cycle candidate, and confirmation.

## Sources

Project-relative paths, issue URLs, revisions, and observation time.
```
