# manage-focus-cycle release history

## 0.1.0

### Added

- A bounded Primary Focus Cycle workflow for delivery, maintenance, research, and decision work.
- A Completion Contract with explicit closure, stopping, and reopen conditions.
- A deterministic, schema-versioned renderer for the temporary Focus Cycle Workspace.
- Adaptive paragraph, list, table, and Mermaid discussion blocks.

### Security and reliability

- Escape all project-provided text before inserting it into HTML.
- Reject unknown schema fields, unsafe link schemes, invalid discussion blocks, and unsupported schema versions.
- Write Workspace files atomically and retain readable Mermaid source when the pinned CDN dependency is unavailable.

### Compatibility

- Codex is the supported client for this release.
- Other Agent Skills clients may load the common `SKILL.md` but are not verified.
- The renderer requires Python 3.13 and uses only the standard library.
- Workspace input schema version is `1`.

### Migration

This is the first public version. Pre-release placeholder-based Workspace generation has no compatibility guarantee and should be replaced by the bundled renderer.

### Rollback

Install the `manage-focus-cycle-v0.1.0` tag directly when a later version must be replaced with this release.
