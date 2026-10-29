# Contributing to Project NRLIS

## Before changing files

Read:

- `CONTENT_OF_WORK.md`;
- `AGENTS.md`;
- `REPOSITORY_GOVERNANCE.md`; and
- the README for the workstream you will change.

Never add participant-identifying information, raw recordings, credentials,
health records, private session data, or learned voice/model artifacts to Git.

## Local setup

Install the versioned Git hooks once per clone:

```bash
bash scripts/install_git_hooks.sh
```

The hook blocks direct pushes to `main`. Normal work must use a branch and pull
request.

## Change workflow

1. Update local `main`.
2. Create a focused branch.
3. Make the smallest coherent change.
4. Update the master index for every persistent path change.
5. Append the project change log.
6. Run:

```bash
python3 scripts/audit_content_index.py
python3 scripts/audit_repository_safety.py
node AgentCollaboration/scripts/smoke-test.mjs
```

7. Open a pull request using the repository template.
8. Squash-merge only after the deterministic checks pass.

## Research and model-review discipline

- Separate observation, inference, hypothesis, and evidence.
- Stay within the active generalization boundary.
- Do not use Codex/Grok agreement as scientific validation.
- Do not send participant, private, raw, authentication, or identifying data to
  external model review.
- Save only curated, non-sensitive collaboration records with explicit
  provenance.

## Reporting problems

Use a GitHub issue only for non-sensitive material. Follow `SECURITY.md` for
credentials, vulnerabilities, privacy events, or participant-related concerns.
