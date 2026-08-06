# GitHub repository settings

The public repository `SWBaek/improvement-ai` uses settings that keep `main` releasable and make security reports private.

## Required remote state

- Delete a merged pull request branch automatically.
- Enable Issues and private vulnerability reporting.
- Apply the active `Protect releasable main` branch ruleset to the default branch.
- Prevent branch deletion and non-fast-forward pushes.
- Require a pull request with resolved review threads.
- Require `Validate (ubuntu-latest)` and `Validate (windows-latest)` against the latest target branch state.
- Require no approval count for the single-maintainer workflow; code-owner assignment remains informational.

## Verification

Use only authenticated `gh` for GitHub state:

```powershell
gh auth status
gh repo view SWBaek/improvement-ai --json description,deleteBranchOnMerge,hasIssuesEnabled,repositoryTopics
gh api repos/SWBaek/improvement-ai/private-vulnerability-reporting
gh api repos/SWBaek/improvement-ai/rulesets
```

If workflow job names change, update the ruleset required checks only after the replacement checks have run successfully on a pull request.
