# Focus Cycle Workspace Rendering

Render a current human-readable view, not an immutable review artifact or project-management application.

## Output contract

- Windows: `%TEMP%\focus-cycle-workspace\<project-name>\index.html`
- macOS/Linux: `${TMPDIR:-/tmp}/focus-cycle-workspace/<project-name>/index.html`
- Sanitize the project directory name to lowercase letters, digits, and hyphens.
- Overwrite the same file on every Skill run; the durable project record owns history.
- Match the language of the current user conversation.
- Open the file with the platform browser when possible and always report the absolute path.

## Required regions

1. `project-context`: long-lived purpose, relevant workstreams, and current source freshness. Never show whole-project completion.
2. `active-focus-cycle`: Primary objective, why now, mode, status, blockers, and cycle-specific progress.
3. `completion-contract`: scope, exit criteria, budget or review point, expected outcome, and reopen condition.
4. `current-discussion`: the adaptive visual surface for the question currently advancing the Cycle.
5. `sources-freshness`: observed, inferred, unknown, human-confirmed, source links, revisions, and update time.

Show the requested human decision near the Focus Cycle header. Do not add forms, buttons, approval controls, editable fields, or comment widgets.

## Adaptive representation

Choose the smallest visual that makes the current relationship clear.

- Use criterion cards or a milestone strip for delivery.
- Use release scope, issue grouping, health indicators, and regression risk for maintenance.
- Use question/evidence maps, hypothesis states, uncertainty, and decision readiness for research.
- Use comparison tables, constraint maps, architecture diagrams, or decision trees for decisions.
- Use plain concise text when a visual adds no information.

Tie every visual to the Primary Focus Cycle. Do not render a generic project dashboard.

## HTML policy

- Start from `assets/focus-cycle-workspace.html` and keep one portable HTML file.
- Keep core layout and styles inline.
- Mermaid diagrams may use `https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs`.
- If the CDN fails, leave Mermaid source and all surrounding labels readable.
- Use semantic headings, landmarks, tables with captions, high-contrast text, and responsive layouts.
- Do not require JavaScript for Project Context, Completion Contract, evidence, sources, or requested decisions.
- Remove unused placeholder sections instead of filling them with invented content.

## Integrity rules

- Label facts as observed, conclusions as inferred, gaps as unknown, and decisions as human-confirmed.
- Include the durable record path and source revision or observation timestamp.
- Never fabricate a percentage, deadline, confidence score, or completed criterion.
- If sources conflict, display the conflict and request resolution.
- If the Cycle is Proposed, visually distinguish draft criteria from confirmed criteria.
- If the Cycle is Closed, show outcome, residual unknowns, and reopen condition instead of ongoing progress.
