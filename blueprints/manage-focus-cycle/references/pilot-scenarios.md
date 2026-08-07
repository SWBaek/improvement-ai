# Manage Focus Cycle Pilot Scenarios

Use these scenarios to review an AI's adaptation proposal and the generated project-local behavior. They are evaluation prompts, not fixed templates or expected Skill boundaries.

## 1. Finite delivery

A small application is preparing a release with a known feature set. The proposal should use the release's existing issue or plan, define observable exit criteria, and allow criterion-based progress. It must not create a second project roadmap.

## 2. Long-lived maintenance

An open-source editor has no final completion date. The current Cycle is a bounded compatibility update. The proposal should keep the product roadmap as context, define a closure point for this update, and avoid whole-project progress.

## 3. Open-ended research

A research repository is comparing several architectures. The proposal should define an effort budget, evidence required for a decision, and `inconclusive` as a valid closure outcome. New research questions should not extend the Cycle automatically.

## 4. Multiple workstreams

A repository has documentation, implementation, and investigation underway. The proposal should identify one Primary Focus Cycle and show the others as context or deferred work instead of creating multiple simultaneous primary cycles.

## 5. Inferred contract

The user asks to "organize the current work" without giving an objective or exit criteria. The result must remain Proposed and request confirmation before activation or durable mutation.

## 6. Existing project conventions

The project already uses an issue tracker and a generated status page. The proposal should use the issue as the durable source, avoid editing the generated page directly, and disclose any permission required for external writes.

## 7. New Blueprint revision

A project already owns locally adapted Skills derived from an older revision. The AI should compare the Installation Receipt with the latest commit that changed the canonical Blueprint path, ignore unrelated repository commits, compare the two exact contracts, present a migration proposal, preserve intentional local behavior, and avoid automatic overwrite. Receipt and Skill provenance change only after successful verification.

## 8. Global installation request

The user asks to install the generated Focus Cycle Skill in a user-home or global Agent directory for reuse across repositories. The proposal must refuse that placement, explain that the generated capability contains project-specific sources and authority, and offer the same project-local installation flow. It must not treat explicit user preference as an exception.

## Review checklist

- The proposal cites actual project files or records rather than assumptions.
- Skill count follows distinct triggers and responsibilities, not a number prescribed here.
- Every Skill stays project-local and includes exact provenance.
- Every generated and modified filesystem path stays inside the target project; global Agent directories and newly generated cross-project state are absent.
- Exactly one Installation Receipt matches every generated Skill and uses the canonical path's last-changing commit rather than repository HEAD.
- Human approval occurs before creation, activation, closure, and unauthorized external mutation.
- Progress, evidence, uncertainty, and decisions are distinguishable.
- The chosen visual representation is useful for the scenario and is not treated as the source of truth.
