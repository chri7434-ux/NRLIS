# Project NRLIS Workspace Rules

These rules apply to the entire repository workspace.

## Required navigation

Before creating, moving, deleting, or materially repurposing a persistent file:

1. Read `CONTENT_OF_WORK.md`.
2. Confirm the responsible directory and naming convention.
3. Read `REPOSITORY_GOVERNANCE.md` for Git or GitHub changes.
4. Make the file change and index/log updates as one atomic task.

## Mandatory Content of Work update

For every persistent file that is created, moved, renamed, or deleted:

- update the human-readable directory or file description in
  `CONTENT_OF_WORK.md`;
- update the complete indexed-file manifest in `CONTENT_OF_WORK.md`; and
- keep paths relative to the project root.

For a content-only edit, update the index description if the file's purpose or
project status changes.

## Mandatory project log update

Every persistent project change must append an entry to
`PROJECT_CHANGE_LOG.md` containing:

- event time with timezone;
- relevant file modification time or observed time;
- changed paths;
- a brief change description; and
- the resulting project-state transition.

The log is append-only. Never erase or silently rewrite older entries. If an
older entry is inaccurate, append a correction.

## Required audit

After file changes, run:

```bash
python3 scripts/audit_content_index.py
python3 scripts/audit_repository_safety.py
```

The task is incomplete until both audits pass. The content-index audit must
report that the indexed manifest and persistent workspace files match. The
repository-safety audit must report that tracked or unignored files contain no
blocked path, sensitive file type, secret-like token, symlink, or oversized
artifact.

## Repository change workflow

- Normal work uses a focused branch and pull request; do not push directly to
  `main`.
- Install the versioned hook with `bash scripts/install_git_hooks.sh`.
- Squash-merge only after the `Repository governance` workflow passes.
- Delete merged source branches.
- Live Grok review is never a CI requirement. CI may run only the static,
  non-live collaboration smoke test.
- A curated Grok result may be committed only as
  `AgentCollaboration/runs/<task-id>/review.json` after privacy and provenance
  verification.

## Exclusions

Do not add the following to the content manifest:

- `.DS_Store`;
- files under `tmp/`;
- Python cache files;
- version-control internals; or
- participant data inside an approved `private/` directory.

Private participant data must never be described with identifying filenames.
Its governing schema and storage responsibility belong in the index, not the
private assets themselves.

## Placement rules

- Root: only project-wide navigation, governance, logs, and maintenance tools.
- `.github/`: GitHub workflows, dependency updates, pull-request templates, and
  issue forms only.
- `AgentCollaboration/`: all substantive Codex-Grok collaboration bridge code,
  schemas, templates, tests, and bounded review records.
- `.codex/config.toml`: the only permitted collaboration file outside
  `AgentCollaboration/`; retained solely because Codex requires this fixed
  discovery location.
- `GrossTree/__init__/`: research definition, boundaries, architecture,
  evidence, safety, and decisions.
- `GrossTree/Basic/Profiles/`: participant-neutral schemas and empty profile
  placeholders; completed participant profiles belong in approved private
  storage.
- `GrossTree/Basic/Trials/`: trial/session protocols and operational templates.
- `GrossTree/Basic/Training/`: model configuration, dataset contracts, and
  evaluation definitions.
- `GrossTree/Extension/`: non-core or later-phase modalities and experiments.
- External literature: cite by DOI in `GrossTree/__init__/EVIDENCE_REGISTER.md`;
  do not commit third-party full-text papers.
