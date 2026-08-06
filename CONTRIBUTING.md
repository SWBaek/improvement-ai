# Contributing

Issues and pull requests are welcome. This is a maintainer-led personal capability portfolio; acceptance and response timing remain at the maintainer's discretion and no support SLA is provided.

## Before opening a change

1. Search existing issues and choose the matching Issue Form.
2. Describe the affected workflow, trigger or non-trigger, expected result, and verification evidence.
3. Do not include credentials, private project data, session logs, caches, or generated runtime artifacts.

## Pull requests

1. Create a focused branch and preserve the flat `skills/<skill-name>` layout.
2. Keep user-facing release history outside the Skill folder.
3. When a released Skill changes, increase its independent version in `skills/catalog.json` and update its release history.
4. Run:

   ```powershell
   python scripts/validate_repository.py
   python -m unittest discover -s tests -p "test_*.py" -v
   ```

5. Explain compatibility, migration, security, and verification impact in the pull request.

GitHub service operations follow `AGENTS.md`: use authenticated `gh`, never place tokens in commands or files.
