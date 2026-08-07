# Manage Focus Cycle Capability Blueprint

- Status: In Progress
- Tracking: [issue #15](https://github.com/SWBaek/improvement-ai/issues/15)
- Canonical path: `blueprints/manage-focus-cycle/BLUEPRINT.md`

Use this Blueprint to design project-owned Agent Skills that establish, review, and close one bounded Focus Cycle inside a finite, maintenance, research, or otherwise long-lived project. Do not copy a fixed implementation from this repository; inspect the target project and adapt the capability to its own records, tools, Agent clients, and human review needs.

## Problem

Long-lived and research projects often have no honest final endpoint. Treating the entire project as one measurable task creates false completion percentages, endless research, and unclear stopping decisions. The human instead needs to see the current bounded objective, its exit conditions, the strongest evidence or blocker, and the decision required now.

## Required outcomes

The generated local capability must:

- manage exactly one Primary Focus Cycle while showing other work only as context or deferred work;
- define a Completion Contract before marking a Cycle active;
- support delivery, maintenance, research, and decision work without inventing a final-project endpoint;
- compare current evidence with explicit exit criteria and make closure readiness visible;
- use the target project's existing durable records before proposing a new record;
- keep human decisions in the established conversation or review channel;
- use a visual projection only when it materially improves human understanding;
- close work as achieved, decision made, inconclusive, stopped, or superseded instead of keeping it open only because uncertainty remains.

## Invariants

- Never invent a whole-project percentage without a defensible denominator.
- Never activate an objective or Completion Contract inferred by the AI. Keep it Proposed until the human confirms it.
- Never change exit criteria silently to keep work open or make it appear complete.
- Separate observed evidence, inference, unknowns, and human decisions.
- Require human confirmation before recording a Cycle as Closed.
- Treat new questions as candidates for a later Cycle unless they block the current contract.
- Preserve project instructions, generated-file rules, permissions, and unrelated changes.
- Keep every generated Skill and supporting artifact inside the target project. Global Agent Skill locations, user-home installation, shared global configuration, and newly generated state shared across projects are prohibited. An existing project-specific external source may remain integrated under its own authority rules.
- Do not publish, commit, push, create issues, or modify external systems unless the user and project policy authorize it.

## Capability operations

These operations are required behavior, not fixed Skill boundaries:

1. **Establish**: define the objective, why now, scope, exit criteria, review point or effort budget, expected decision or deliverable, and reopen condition.
2. **Review**: update evidence, criterion status, progress representation, blockers, unknowns, current discussion, and decision readiness.
3. **Close**: compare evidence with the Completion Contract and propose an explicit closure outcome for human confirmation.
4. **Replace**: close the current Cycle as superseded and establish a new Proposed Cycle without carrying criteria forward silently.

Generate one Skill when these operations share one clear trigger and context. Generate multiple Skills only when their triggers, permissions, or required context are materially different. Supporting scripts are appropriate only for fragile or repeatedly reproduced deterministic work.

## Project adaptation

Before proposing files, inspect the target project's agent instructions and relevant records. Determine:

- project purpose and whether the current work is delivery, maintenance, research, or decision work;
- the authoritative issue, plan, decision log, SDOC, research note, or equivalent durable source;
- installed Agent clients and their project-local Skill locations;
- the resolved target-project root and any path that would escape it or point to global Agent configuration;
- existing visualization, documentation, validation, and generated-file conventions;
- operations that require external writes, elevated permissions, or explicit approval;
- whether a visual workspace adds enough value to justify its maintenance.

Prefer the project-native durable source. If none exists, include a proposed local record path in the adaptation proposal rather than creating one silently.

A visual projection may be HTML, a diagram, a table, a timeline, a chart, or concise text. Match the representation to the current discussion. It is not the source of truth or an input form, and it must not replace chat or the project's normal decision channel. Numeric progress is allowed only when the Completion Contract supplies a defensible denominator.

## Instantiation protocol

### 1. Inspect without mutation

Read the target repository instructions and relevant sources. Do not create, edit, install, or delete anything during this step.

### 2. Propose the local design

Present one compact proposal containing:

- evidence about the target project's existing conventions;
- each proposed Skill name, trigger, non-trigger, responsibility, project-local path, and bundled resources;
- the durable source of Focus Cycle state and any fallback record;
- the proposed progress and discussion representation;
- external permissions and human confirmation points;
- the single project-local Blueprint Installation Receipt path;
- one realistic invocation and the verification method;
- files that would be created or changed.

Reject any proposed path outside the target project and replace it with a project-local design. A request for global installation is not an approval exception for this capability.

Ask for human approval. Do not treat silence as approval.

### 3. Generate after approval

Create only the approved project-local Skills and necessary resources. Follow the target Agent's project-local discovery path; when no project convention exists, use `<target-project>/.agents/skills/<name>/` for Codex and `<target-project>/.claude/skills/<name>/` for Claude Code. Never create or modify a global Skill location, user-home Skill directory, shared global config, or state outside the target project, even when the user requests convenience across projects.

Before generation, resolve the 40-character commit that most recently changed this canonical `BLUEPRINT.md` path. Reread the Blueprint from the exact commit URL; do not use the repository HEAD merely because the user supplied a `main` URL. Create exactly one project-local Installation Receipt at the approved path:

```yaml
format: improvement-ai-blueprint-installation/v1
blueprint: manage-focus-cycle
repository: https://github.com/SWBaek/improvement-ai
path: blueprints/manage-focus-cycle/BLUEPRINT.md
revision: <40-character-commit>
source: https://github.com/SWBaek/improvement-ai/blob/<40-character-commit>/blueprints/manage-focus-cycle/BLUEPRINT.md
```

For every generated `SKILL.md`:

- use lowercase kebab-case for the directory and `name`;
- place only `name` and a concrete trigger-oriented `description` in YAML frontmatter;
- keep common workflow instructions concise and load detailed variants progressively;
- use imperative instructions and make non-triggers explicit in the description;
- choose instruction freedom according to risk: heuristics for contextual choices, scripts for fragile deterministic behavior;
- append this provenance comment after resolving the Blueprint to an exact 40-character commit:

```markdown
<!-- improvement-ai-blueprint
source: https://github.com/SWBaek/improvement-ai/blob/<40-character-commit>/blueprints/manage-focus-cycle/BLUEPRINT.md
revision: <40-character-commit>
-->
```

Every generated Skill's provenance must match the Installation Receipt. The generated files belong to the target project. Do not add an upstream update hook, overwrite local adaptations from a newer Blueprint, or copy project-specific output back into `improvement-ai`.

### 4. Verify locally

Confirm that the target Agent can discover each Skill and run one representative Focus Cycle operation. Verify the generated result against every invariant above and the target project's own checks. Report the durable record changed, any visual output path, remaining uncertainty, and the next human decision.

## Reapplying a newer revision

Treat the commit that most recently changed this canonical `BLUEPRINT.md` path as the latest Blueprint revision; unrelated repository commits are not updates. Compare it with the Installation Receipt. Report `current` when equal, `update available` when different, and `unknown` when the latest path revision cannot be established.

When an update is available, inspect the existing local implementation and compare the two exact Blueprint documents. Present a semantic migration proposal first, preserve useful local behavior, and never regenerate or overwrite automatically. Update the Installation Receipt and every Skill provenance together only after approved changes and local verification succeed. If the installation predates receipts, propose creation of one from existing exact provenance before migration.

## Non-goals

- Managing the entire project roadmap or claiming that a long-lived project is complete.
- Mandating HTML, JSON, a particular renderer, or a fixed number of Skills.
- Acting as a hosted workspace, issue tracker, scheduler, or autonomous project manager.
- Installing generated Skills or supporting state globally. A stateless cross-project Blueprint bootstrap would require a separate capability and is not an exception here.
- Synchronizing generated Skills with this repository.
- Centralizing project-specific generated variants in this repository.

## Acceptance

An instantiation is acceptable when:

- the proposal is grounded in inspected project evidence and approved before writes;
- generated Skills have distinct, accurate triggers and project-local paths;
- every generated or modified filesystem path resolves inside the target project and no global Agent location or newly generated cross-project state is used;
- exactly one Installation Receipt identifies the path-scoped Blueprint revision and matches every generated Skill provenance;
- one Primary Focus Cycle and its Completion Contract are visible in the durable source;
- inferred elements remain Proposed and closure requires human confirmation;
- progress and visual claims are supported by evidence;
- provenance contains the exact source path and path-scoped Git revision;
- a representative invocation succeeds without violating project policy.

Use [the Pilot scenarios](references/pilot-scenarios.md) to evaluate the proposal and generated behavior. Promotion requires successful use in two different projects; similarity or difference in their Skill decomposition must be explained by project evidence rather than forced by this Blueprint.

## Background

The delivery form is inspired by Andrej Karpathy's [LLM Wiki idea file](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): preserve a small set of architectural invariants and operations so an AI can instantiate a domain-appropriate implementation. This Blueprint applies that generative approach to bounded project focus management; it does not copy or implement the LLM Wiki workflow.
