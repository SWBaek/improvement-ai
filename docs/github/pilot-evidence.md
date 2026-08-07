# Pilot Evidence

Pilot evidence shows how an exact Blueprint revision behaved after generation and real use in a target project. Submit it as a comment on that Blueprint's existing tracking issue. Do not open a separate Pilot issue.

Successful, failed, and inconclusive results are all useful. The project and contributor may remain anonymous; the evidence must still describe the project context well enough to distinguish independent Pilots.

## Privacy rules

Remove or generalize:

- private repository, company, product and person names;
- local absolute paths and internal URLs;
- source code, credentials, tokens and configuration secrets;
- original prompts, transcripts and session logs;
- proprietary architecture, research data and business metrics.

Report reusable behavior and failure patterns rather than copying project artifacts. Confirm that generated Skills, receipts, profiles, schemas and state remained inside the target project. Existing project-specific external trackers may be described generically.

## Comment template

Copy this template into the Blueprint tracking issue and replace the placeholders.

```markdown
## Pilot evidence

- Blueprint: `<name>`
- Path-scoped revision: `<40-character-commit>`
- Result: `successful | failed | inconclusive`
- Target project: `<anonymous project type and lifecycle>`
- Existing management system: `<tracker, ADR, research notes, or none>`
- Agent/client: `<Agent product or harness>`

### Adaptation

- Ownership or mapping: `<Integration/Migration choices or equivalent adaptation>`
- Generated artifacts: `<artifact kinds and project-relative path summary>`
- Operations exercised: `<establish/brief/decision/handoff/audit/etc.>`

### Expected and observed

- Expected outcome: `<what the Blueprint should enable>`
- Observed outcome: `<what actually happened>`
- Verification: `<evidence used to judge the outcome>`

### Contract checks

- [ ] There was one source of truth per information area.
- [ ] Human authority and external-write boundaries were preserved.
- [ ] All generated filesystem artifacts stayed inside the target project.
- [ ] Global Agent Skill locations and new cross-project shared state were not used.
- [ ] Installation Receipt and generated Skill provenance used the same exact revision.

### Cost and learning

- Maintenance cost: `<what had to be kept current>`
- Friction or failure: `<confusion, repeated correction, drift, missing behavior>`
- Reusable learning: `<smallest Blueprint-level lesson>`
- Suggested follow-up: `<none, reference clarification, contract issue, or another Pilot>`

### Privacy confirmation

- [ ] I removed credentials, private code, identifiable project details, local absolute paths and original session logs.
```

## Promotion use

Repeated evidence from one target project improves confidence in that Pilot but does not count as another independent project. A maintainer determines whether two submissions are sufficiently independent and whether invariants, triggers, adaptation freedom and authority boundaries are stable enough to mark the Blueprint Promoted.
