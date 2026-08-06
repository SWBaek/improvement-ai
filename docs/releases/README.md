# Skill releases

This directory records human-readable release history outside the Skill execution context. `skills/catalog.json` is the canonical source for current versions and lifecycle status.

## Versioning

Each Skill has an independent Semantic Version and tag:

```text
<skill-name>-v<major>.<minor>.<patch>
```

- During `0.x`, patch releases preserve the published input and durable-record contracts.
- During `0.x`, minor releases may contain a documented breaking change and must include migration and rollback guidance.
- From `1.0.0`, breaking changes require a major release.
- A GitHub Release and capability lifecycle status are independent. An `In Progress` Skill may have a public `0.x` release while it is being piloted.

## Main branch contract

`main` is always installable. Any change under a released `skills/<name>/` directory must include a higher version in `skills/catalog.json` and a matching entry in that Skill's release history. After merge, the release workflow creates one immutable tag and GitHub Release per changed Skill version.

The `skills` installer follows the originally installed Git ref and detects folder changes rather than interpreting Semantic Versions. Default installations follow `main`; tag URLs provide reproducible installs and rollback points.
