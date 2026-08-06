# Contributing

Issues and pull requests are welcome. This is a maintainer-led personal capability portfolio; acceptance and response timing remain at the maintainer's discretion and no support SLA is provided.

## Before opening a change

1. Search existing issues and choose the matching Issue Form.
2. Describe the affected workflow, trigger or non-trigger, expected result, and verification evidence.
3. Do not include credentials, private project data, session logs, caches, or generated runtime artifacts.

## Pull requests

1. Create a focused branch and preserve the flat `skills/<skill-name>` layout.
2. Update only documentation and tests that directly protect the changed behavior.
3. Increase `skills/catalog.json` only when intentionally publishing a GitHub Release snapshot.
4. When changing `manage-focus-cycle` behavior, optionally run:

   ```powershell
   python -m unittest tests.test_manage_focus_cycle -v
   ```

5. Explain the user-visible outcome and any meaningful compatibility or security impact.

GitHub service operations follow `AGENTS.md`: use authenticated `gh`, never place tokens in commands or files.
