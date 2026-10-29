# NRLIS Codex-Grok Collaboration

This directory implements a fail-closed collaboration boundary:

```text
human researcher
      |
      v
Codex coordinator
      |
      | MCP tool call with task ID + explicit paths
      v
local grok-collab MCP server
      |
      | copies only approved files
      v
temporary read-only snapshot
      |
      | Grok Build headless, no web, no subagents, no shell/write tools
      v
structured review returned to Codex
```

Grok does not operate directly on the live repository. The bridge rejects
restricted paths, symlinks, unsupported file types, large snapshots, and paths
outside the project. Temporary snapshots are deleted after each call.

## MCP tools

- `grok_project_review`: independent review of a bounded repository question.
- `grok_compare_hypotheses`: compare explicit hypotheses against selected
  repository evidence.
- `grok_methodology_audit`: audit a proposed method or claim against the NRLIS
  protocol and safety boundaries.

All tools are read-only with respect to the live repository. Codex is
responsible for saving a material result under
`AgentCollaboration/runs/<task-id>/`, verifying it, and deciding whether to
implement anything.

Every call uses the canonical task contract in
`schemas/task.schema.json`. The selected MCP tool must match
`requested_tool`, every snapshot path must be explicit, and task-specific
prohibitions can only add to the bridge's mandatory restrictions.
The reviewer subprocess receives only an explicit minimal environment
allowlist; unrelated parent-process variables are not forwarded. Reviewer
stderr content is suppressed rather than returned or written to logs.

Only a curated, non-sensitive `review.json` and its verified
`provenance.json` are eligible for version control. Raw snapshots, temporary
prompts, intermediate output, and any unverified run artifact remain ignored.
Before tracking a review record, Codex must confirm that it contains no
participant, private, raw, authentication, or identifying data and that every
cited path was part of the bounded snapshot.

The Codex discovery configuration explicitly selects `grok-4.5` with `high`
reasoning effort for future bridge calls. Each v0.3 tool response is an
envelope containing a schema-valid `review` and `provenance`. Provenance records
the requested model and reasoning effort, repository commit and worktree state,
canonical task/config/schema hashes, and a SHA-256 manifest of every snapshot
file. These fields record the bridge request and local source state; they are
not independent proof of the provider's internal serving tier.

The two retained v0.1/v0.2 records are explicitly marked `legacy_partial`.
Only those historical paths may omit v0.3 hashes.

## Restricted by default

- participant-specific profile directories;
- raw or private data directories;
- non-template session logs and tabular datasets;
- audio, video, biosignal, model-weight, archive, and database files;
- credentials, auth files, `.env` files, keys, and symlinks.

Published literature PDFs and figures may be included only when their exact
paths are explicitly supplied.

## Validation

Install the pinned local validation dependency:

```bash
npm ci --prefix AgentCollaboration
```

Run canonical JSON Schema and cross-artifact validation:

```bash
npm --prefix AgentCollaboration run validate:artifacts
```

Run deterministic bridge tests with a local fake reviewer:

```bash
npm --prefix AgentCollaboration test
```

Static MCP handshake and tool-list test:

```bash
node AgentCollaboration/scripts/smoke-test.mjs
```

Live read-only Grok test:

```bash
node AgentCollaboration/scripts/smoke-test.mjs --live
```

The live test sends only `README.md` and
`GrossTree/__init__/PROJECT_CHARTER.md` through a temporary snapshot.
CI never runs the live form.

After changing `.codex/config.toml`, the server, or a canonical input schema,
reload the Codex connector before using the app-exposed tools. Confirm that
`serverInfo.version` is `0.3.0` and that tool inputs require
`requested_tool`, `prohibited_actions`, and `acceptance_checks`. A direct smoke
test validates the checked-out server but does not refresh an already-running
app connector.

## Operating rule

Use one Grok review per task during the initial rollout. A model agreement is
not scientific validation; every finding still requires repository evidence,
primary-source checking, or a deterministic test.

## Codex discovery shim

Codex requires its project configuration at `.codex/config.toml`. That single
fixed-location file is intentionally retained as a minimal discovery shim; all
substantive collaboration code, schemas, templates, tests, and run records live
in this directory.
