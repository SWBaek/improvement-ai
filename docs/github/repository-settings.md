# GitHub repository settings

The public repository `SWBaek/improvement-ai` protects history without imposing automated validation on fast Skill iteration.

## Required remote state

- Delete a merged pull request branch automatically.
- Enable Issues and private vulnerability reporting.
- Apply the active `Protect main history` branch ruleset to the default branch.
- Prevent branch deletion and non-fast-forward pushes.
- Require a pull request with resolved review threads.
- Do not require status checks or platform validation.
- Require no approval count for the single-maintainer workflow; code-owner assignment remains informational.

## Verification

Use only authenticated `gh` for GitHub state:

```powershell
gh auth status
gh repo view SWBaek/improvement-ai --json description,deleteBranchOnMerge,hasIssuesEnabled,repositoryTopics
gh api repos/SWBaek/improvement-ai/private-vulnerability-reporting
gh api repos/SWBaek/improvement-ai/rulesets
```

Add required checks only after repeated failures show that the check protects a real user outcome at acceptable development cost.
