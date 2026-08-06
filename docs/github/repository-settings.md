# GitHub repository settings

The public repository `SWBaek/improvement-ai` protects history without adding automated validation or Release machinery to Blueprint iteration.

## Required remote state

- Delete merged pull request branches automatically.
- Enable Issues and private vulnerability reporting.
- Apply the active `Protect main history` ruleset to the default branch.
- Prevent branch deletion and non-fast-forward pushes.
- Require a pull request with resolved review threads.
- Do not require status checks, platform validation, Release workflows, or an approval count for the single-maintainer workflow.
- Use Blueprint, documentation, AI workflow, and Agent Skills topics without naming a single supported Agent as the repository identity.

## Verification

Use only authenticated `gh` for GitHub state:

```powershell
gh auth status
gh repo view SWBaek/improvement-ai --json description,deleteBranchOnMerge,hasIssuesEnabled,repositoryTopics
gh api repos/SWBaek/improvement-ai/private-vulnerability-reporting
gh api repos/SWBaek/improvement-ai/rulesets
gh workflow list --repo SWBaek/improvement-ai
```

Add automation only after repeated failures show that it protects a real Blueprint or consumer outcome at acceptable maintenance cost.
