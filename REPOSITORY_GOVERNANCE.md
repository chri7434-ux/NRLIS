# Repository Governance

## Purpose

This document defines the version-control and GitHub operating baseline for
Project NRLIS. It governs repository changes only; it does not authorize
participant enrollment, recording, clinical use, or scientific claims.

## Normal change path

1. Start from the latest `main`.
2. Create a narrowly named `codex/<description>` or human feature branch.
3. Update `CONTENT_OF_WORK.md` for persistent path changes.
4. Append `PROJECT_CHANGE_LOG.md` for every persistent project change.
5. Run both repository audits and the relevant syntax or smoke tests.
6. Open a pull request and let `Repository governance` complete.
7. Use squash merge and delete the merged source branch.

Direct pushes to `main` are not part of the normal workflow. The versioned
pre-push hook blocks them in configured local clones. The only local bypass is
`NRLIS_ALLOW_MAIN_PUSH=1`, reserved for a documented recovery action whose
reason and resulting state are appended to `PROJECT_CHANGE_LOG.md`.

## Enforced controls

- `.github/workflows/repository-governance.yml` runs deterministic checks on
  every pull request and push to `main`.
- `scripts/audit_change_log.py` requires each persistent change set to append
  the project log and rejects rewriting existing log history.
- `scripts/audit_content_index.py` checks the authoritative file manifest.
- `scripts/audit_repository_safety.py` rejects tracked or unignored private
  paths, secret-like tokens, sensitive media/model formats, symlinks, and
  oversized files.
- `AgentCollaboration/scripts/smoke-test.mjs` verifies the fail-closed Grok
  bridge without making a live model request.
- Canonical collaboration JSON is validated against versioned schemas, and the
  bridge's negative tests verify path, provenance, and evidence fail-closed
  behavior.
- The synthetic G0 check exercises deterministic inference and evaluation
  plumbing without participant data or participant-performance claims.
- The pull-request template requires privacy, index, log, and validation
  attestations.
- GitHub Actions dependencies are pinned to full commit SHAs and maintained by
  Dependabot.

## Remote repository settings

The operational baseline uses:

- private visibility and `main` as the default branch;
- squash merge as the only enabled merge strategy;
- automatic deletion of merged source branches;
- read-only default GitHub Actions token permissions with pull-request approval
  disabled;
- Issues and Projects enabled, with the Wiki disabled;
- dependency vulnerability alerts and automated security fixes enabled;
- bounded repository topics that describe assistive communication, dysarthria,
  human-in-the-loop multimodal AI, applied mathematics, bioengineering, and
  research infrastructure; and
- standard `infrastructure`, `research`, `safety`, `privacy`, `evidence`, and
  `blocked` labels.

## GitHub plan limitation

At the infrastructure-baseline audit on 2026-07-29, GitHub returned HTTP 403
for private-repository rulesets and stated that GitHub Pro or a public
repository was required. Project NRLIS must remain private, so no visibility
change is permitted as a workaround.

Until the account or organization plan supports server-side branch protection,
the project uses:

- pull-request-only operating policy;
- a versioned local pre-push hook;
- squash-only merge settings;
- automatic deletion of merged branches;
- deterministic CI on every pull request; and
- append-only logging of exceptional direct-main actions.

Recheck server-side rulesets after any plan or ownership change. When available,
require the `Repository governance` check, disallow force pushes and deletion,
and require pull requests for `main`.

## Grok collaboration boundary

Live Grok review is opt-in per bounded task and is never a CI requirement.
Only allowlisted, non-restricted files may enter a temporary read-only
snapshot. A Grok conclusion is review evidence, not scientific validation.
Curated review records may be stored under
`AgentCollaboration/runs/<task-id>/review.json` after privacy and provenance
verification.
