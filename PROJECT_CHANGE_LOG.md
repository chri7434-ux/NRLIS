# Project Change Log

**Role:** Authoritative append-only modification record  
**Timezone:** America/New_York (`EDT` or `EST` as applicable)

## Logging rules

Each entry records:

- event or observation time;
- relevant modification-time range;
- modified paths;
- a brief description; and
- resulting project-state change.

Entries reconstructed from filesystem metadata are explicitly labeled. Future
entries should be appended in descending or ascending chronological order
consistently; this log uses ascending order.

## Entries

### CHG-0001 - Initial evidence and architecture seed

- Event time: 2026-07-29 15:55-16:12 EDT
- Modification time: 2026-07-29 15:55:20-16:12:02 EDT
- Record type: Reconstructed from filesystem modification times
- Modified content:
  - `GrossTree/Literatures/`
  - `GrossTree/__init__/Overall_view.png`
- Brief: Added the fMRI semantic-decoding paper, personalized disordered-speech
  ASR paper images, and the first workflow overview image.
- Project state: Unstructured evidence seed -> initial evidence-backed concept.

### CHG-0002 - Protocol-first research scaffold

- Event time: 2026-07-29 16:25-16:27 EDT
- Modification time: 2026-07-29 16:25:49-16:26:59 EDT
- Record type: Reconstructed from filesystem modification times
- Modified content:
  - `GrossTree/__init__/`
  - `GrossTree/Basic/Profiles/`
  - `GrossTree/Basic/Trials/`
  - `GrossTree/Basic/Training/`
  - `README.md`
  - `.gitignore`
- Brief: Added the research charter, G0-G5 generalization boundary, algorithm
  workflow, safety/governance, evidence and decision registers, P001
  pre-enrollment profile, T001 shadow protocol, dataset contract, metrics, and
  frozen pre-data configuration.
- Project state: Concept -> protocol-first / pre-data v0.1.

### CHG-0003 - GrossTree consolidation observed

- Event time: Observed 2026-07-29 16:32:07 EDT
- Modification time: Original file modification times preserved
- Record type: Reconstructed structural event; exact move time unavailable
- Modified content:
  - `GrossTree/`
  - root `README.md` references
  - root `.gitignore` references
- Brief: Substantive research content was consolidated under `GrossTree/`.
  The move preserved file modification times but made prior root-relative README
  and private-data ignore paths stale.
- Project state: Flat mixed root -> root governance plus GrossTree business
  content; navigation repair required.

### CHG-0004 - Master index, log, and enforcement layer

- Event time: 2026-07-29 16:32 EDT
- Modification time: 2026-07-29 16:32 EDT
- Record type: Direct project modification
- Modified content:
  - `CONTENT_OF_WORK.md`
  - `PROJECT_CHANGE_LOG.md`
  - `AGENTS.md`
  - `scripts/audit_content_index.py`
  - `README.md`
  - `.gitignore`
- Brief: Created a root-level master content index, append-only change log,
  future-work governance rules, and an automated index audit. Repaired all
  README and sensitive-data ignore paths after GrossTree consolidation.
- Project state: Protocol-first v0.1 with ad hoc navigation -> indexed,
  auditable, growth-ready protocol-first v0.1.

### CHG-0005 - Hidden collaboration infrastructure indexed and repaired

- Event time: 2026-07-29 16:34 EDT
- Modification time: 2026-07-29 16:31:54-16:34 EDT
- Record type: Direct project modification following audit discovery
- Modified content:
  - `.codex/config.toml`
  - `.collab/`
  - `CONTENT_OF_WORK.md`
  - `PROJECT_CHANGE_LOG.md`
- Brief: Registered the existing Codex-Grok collaboration infrastructure as a
  separate hidden-tool workstream. Updated its default, template, safety-test,
  published-evidence, and restricted-data paths to the new `GrossTree/`
  locations.
- Project state: Indexed research tree with unregistered/stale hidden tooling ->
  fully indexed workspace with GrossTree-aware collaboration tooling.

### CHG-0006 - Persistent memory governance rule recorded

- Event time: 2026-07-29 16:35 EDT
- Modification time: 2026-07-29 16:35:36-16:35:55 EDT
- Record type: Direct project and external memory modification
- Modified content:
  - `CONTENT_OF_WORK.md`
  - `PROJECT_CHANGE_LOG.md`
  - external memory note (local, outside the repository; path omitted)
- Brief: Persisted the user's requirement that every future project file
  creation, move, rename, or deletion update the master content index; every
  project modification append the project log; and every change set pass the
  automated content-index audit.
- Project state: Workspace-enforced governance -> workspace- and
  memory-persisted governance for future sessions.

### CHG-0007 - Agent collaboration infrastructure consolidated

- Event time: 2026-07-29 16:42 EDT
- Modification time: 2026-07-29 16:42 EDT
- Record type: Direct project modification
- Modified content:
  - `.collab/` moved to `AgentCollaboration/`
  - `.codex/config.toml`
  - `AgentCollaboration/README.md`
  - `AgentCollaboration/scripts/smoke-test.mjs`
  - `AGENTS.md`
  - `README.md`
  - `CONTENT_OF_WORK.md`
  - `PROJECT_CHANGE_LOG.md`
- Brief: Consolidated all substantive Codex-Grok collaboration files into one
  discoverable root subdirectory and repaired MCP, test, documentation, and
  index references. Retained `.codex/config.toml` only as the fixed-location
  discovery shim required by Codex.
- Project state: Distributed hidden collaboration tooling -> centralized,
  indexed `AgentCollaboration/` workstream with a minimal Codex discovery shim.

### CHG-0008 - Private GitHub repository established

- Event time: 2026-07-29 16:56-16:57 EDT
- Modification time: 2026-07-29 16:56:49-16:58:34 EDT
- Record type: Direct project and external repository modification
- Modified content:
  - private GitHub repository `chri7434-ux/Project_NRLIS`
  - local version-control internals under `.git/` (excluded from content index)
  - `.gitignore`
  - `README.md`
  - `CONTENT_OF_WORK.md`
  - `PROJECT_CHANGE_LOG.md`
- Brief: Created the canonical private GitHub repository, initialized the local
  `main` branch, bound `origin`, and prepared the complete audited workspace for
  its initial synchronized commit. Expanded ignore rules for local
  environments, generated Python/Node content, and secrets files.
- Project state: Indexed local protocol-first workspace -> private,
  version-controlled canonical project baseline.

### CHG-0009 - GitHub plugin private-repository access verified

- Event time: 2026-07-29 17:08 EDT
- Modification time: Observed 2026-07-29 17:08:44 EDT
- Record type: Direct external connector verification and project status update
- Modified content:
  - GitHub plugin authorization for private repository
    `chri7434-ux/Project_NRLIS`
  - `CONTENT_OF_WORK.md`
  - `PROJECT_CHANGE_LOG.md`
- Brief: Reauthorized the GitHub plugin and verified that its connector can
  directly read the canonical private repository, identify `main` as the
  default branch, and report admin, maintain, pull, push, and triage access.
- Project state: Private GitHub repository with CLI-only verified access ->
  private canonical repository with verified CLI and GitHub plugin access.

### CHG-0010 - Repository infrastructure baseline and Grok review

- Event time: 2026-07-29 17:14-17:18 EDT
- Modification time: 2026-07-29 17:14:09-17:25:30 EDT
- Record type: Direct repository, GitHub, and bounded model-review modification
- Modified content:
  - merged GitHub PR #1 at commit `26f6539`
  - `.github/`
  - `.editorconfig`
  - `.gitattributes`
  - `REPOSITORY_GOVERNANCE.md`
  - `CONTRIBUTING.md`
  - `SECURITY.md`
  - `scripts/audit_repository_safety.py`
  - `scripts/install_git_hooks.sh`
  - `scripts/git-hooks/pre-push`
  - `AgentCollaboration/.gitignore`
  - `AgentCollaboration/README.md`
  - `AgentCollaboration/grok-mcp/server.mjs`
  - `.codex/config.toml`
  - `AgentCollaboration/runs/NRLIS-INFRA-BASELINE-001-R1/provenance.json`
  - `AgentCollaboration/runs/NRLIS-INFRA-BASELINE-001-R1/review.json`
  - `AgentCollaboration/runs/NRLIS-SMOKE-001/provenance.json`
  - `AGENTS.md`
  - `README.md`
  - `CONTENT_OF_WORK.md`
  - `PROJECT_CHANGE_LOG.md`
- Brief: Merged the verified GitHub-plugin record, then created a deterministic
  repository-governance workflow, safety audit, versioned direct-main push
  guard, contribution and security policies, structured issue/PR intake, and
  pinned Actions dependency maintenance. Exercised the fail-closed Grok bridge:
  an unsupported `.gitignore` request was rejected before transfer, and a
  six-file read-only retry produced the curated infrastructure review
  `NRLIS-INFRA-BASELINE-001-R1`. Upgraded the bridge to v0.2.0 so future calls
  explicitly request `grok-4.5` with `high` reasoning effort and return that
  requested provenance. Recorded that the completed v0.1.0 review used the
  provider default and therefore does not prove an exact Heavy serving tier.
  A separate v0.2.0 live smoke test then succeeded with explicit
  `grok-4.5`/`high` request metadata, restricted-path rejection, no web,
  no subagents, and no live-repository write access.
- Project state: Private Git-backed and connector-verified pre-data workspace ->
  PR-centered, CI-audited infrastructure baseline under validation.

### CHG-0011 - Remote repository settings hardened

- Event time: 2026-07-29 17:27-17:29 EDT
- Modification time: 2026-07-29 17:27:35-17:29:28 EDT
- Record type: Direct GitHub settings modification and repository status update
- Modified content:
  - GitHub merge settings, Actions permissions, vulnerability alerts,
    automated security fixes, topics, and labels
  - `.github/ISSUE_TEMPLATE/research_task.yml`
  - `.github/ISSUE_TEMPLATE/bug_report.yml`
  - `.github/dependabot.yml`
  - `REPOSITORY_GOVERNANCE.md`
  - `CONTENT_OF_WORK.md`
  - `PROJECT_CHANGE_LOG.md`
- Brief: After PR #2 passed the new `Repository governance` workflow and was
  squash-merged at `1691836`, restricted the repository to squash-only merges
  with automatic source-branch deletion. Confirmed read-only default Actions
  permissions with PR approval disabled, enabled vulnerability alerts and
  automated security fixes, and added bounded topics and workflow labels.
  GitHub rulesets remained unavailable with HTTP 403 on the current plan; the
  repository stayed private and retained the documented PR/CI/local-hook
  fallback instead of weakening privacy.
- Project state: CI-audited infrastructure baseline under validation ->
  operational private repository baseline with hardened remote settings and a
  documented server-side protection limitation.

### CHG-0012 - Phase 0B contract freeze and synthetic G0 verification

- Event time: 2026-07-29 18:09-18:45 EDT
- Modification time: 2026-07-29 18:09-18:45 EDT; bounded Grok reviews
  observed during the same event window
- Record type: Direct project modification, deterministic component
  verification, and bounded independent model review
- Modified content:
  - `.codex/config.toml`
  - `.github/dependabot.yml`
  - `.github/workflows/repository-governance.yml`
  - `.gitignore`
  - `AgentCollaboration/README.md`
  - `AgentCollaboration/package.json`
  - `AgentCollaboration/package-lock.json`
  - `AgentCollaboration/grok-mcp/server.mjs`
  - `AgentCollaboration/schemas/task.schema.json`
  - `AgentCollaboration/schemas/provenance.schema.json`
  - `AgentCollaboration/scripts/smoke-test.mjs`
  - `AgentCollaboration/scripts/validate-artifacts.mjs`
  - `AgentCollaboration/tests/bridge.test.mjs`
  - `AgentCollaboration/tests/fake-grok.mjs`
  - `AgentCollaboration/templates/task.example.json`
  - `AgentCollaboration/runs/NRLIS-INFRA-BASELINE-001-R1/provenance.json`
  - `AgentCollaboration/runs/NRLIS-SMOKE-001/provenance.json`
  - `GrossTree/README.md`
  - `GrossTree/__init__/PROJECT_OBJECTIVE_AND_ROADMAP.md`
  - `GrossTree/__init__/PROJECT_CHARTER.md`
  - `GrossTree/__init__/GENERALIZATION_BOUNDARIES.md`
  - `GrossTree/__init__/EVALUATION_SAFETY_GOVERNANCE.md`
  - `GrossTree/__init__/DECISION_LOG.md`
  - `GrossTree/Basic/Trials/NRLIS-T001/PROTOCOL.md`
  - `GrossTree/Basic/Trials/NRLIS-T001/TASK_REFERENCE_AUTHORSHIP_SOP.md`
  - `GrossTree/Basic/Trials/NRLIS-T001/session_log_template.csv`
  - `GrossTree/Basic/Training/Config./baseline_v0.yaml` moved to
    `GrossTree/Basic/Training/Config/baseline_v0.yaml`
  - `GrossTree/Basic/Training/Config/synthetic_g0_baseline.json`
  - `GrossTree/Basic/Training/Config/synthetic_g0_config.schema.json`
  - `GrossTree/Basic/Training/Dataset/DATA_CONTRACT.md`
  - `GrossTree/Basic/Training/Dataset/synthetic_g0.schema.json`
  - `GrossTree/Basic/Training/Dataset/synthetic_g0_fixture.json`
  - `GrossTree/Basic/Training/Evaluation/METRICS.md`
  - `GrossTree/Basic/Training/Evaluation/T001_ANALYSIS_SPEC.md`
  - `GrossTree/Basic/Training/Evaluation/synthetic_g0_expected_metrics.json`
  - `GrossTree/Basic/Training/Implementation/README.md`
  - `GrossTree/Basic/Training/Implementation/synthetic_g0.py`
  - `GrossTree/Basic/Training/Implementation/test_synthetic_g0.py`
  - `scripts/audit_change_log.py`
  - `scripts/audit_content_index.py`
  - `scripts/audit_repository_safety.py`
  - `README.md`
  - `REPOSITORY_GOVERNANCE.md`
  - `CONTENT_OF_WORK.md`
  - `PROJECT_CHANGE_LOG.md`
- Brief: Froze the WP0 v0.2 objective, claim ladder, T0-T4 task taxonomy,
  pre-reveal reference and authorship order, multi-axis novelty contract,
  mode-specific metrics, data contract, and T001 analysis structure. Kept all
  27 Stage D performance/analysis gates `null` and blocking, all hard safety
  limits at zero, and enrollment, recording, participant-data training,
  Stage D, and output disabled.
- Brief: Implemented the standard-library-only synthetic G0 execution path with
  strict synthetic schemas, deterministic fixed-bank inference, immutable
  hashes, 10 retained attempts, separate semantic-scoring and abstention
  challenge populations, unconditional and conditional Top-k, calibration,
  abstention safety, safe output-path handling, and 16 acceptance tests. The
  fixture deliberately includes a missed challenge and a false abstention so
  safety metrics are not guaranteed by construction. Static-fixture inference
  latency is explicitly not evaluable. The only earned statement is
  `G0_component_verified_synthetic_only`; no participant-performance claim.
- Brief: Upgraded the Codex-Grok bridge to v0.3 with canonical runtime schemas,
  complete provenance hashes, strict evidence-path validation, portable
  project-root resolution, a minimal reviewer environment allowlist, suppressed
  stderr content, pinned dependencies, six deterministic bridge tests, and
  schema-aware CI. Expanded repository safety scanning and added an append-only
  change-log audit.
- Brief: Two bounded Grok methodology reviews
  (`NRLIS-PHASE0B-G0-AUDIT-001` and `NRLIS-PHASE0B-G0-AUDIT-002`) identified
  metric-registry, challenge-denominator, conditional-coverage, static-latency,
  and cross-governance inconsistencies; each finding was corrected before this
  transition. The reviews were not stored as curated run artifacts because the
  already-loaded connector reported legacy v0.1.0 metadata rather than the
  complete v0.3 provenance required for new records.
- Brief: A direct post-hardening v0.3 live smoke
  (`run_id=5cf328e5-7cbf-4359-9247-cf660ed33071`) then succeeded with explicit
  `grok-4.5` / `high`, a three-file allowlisted snapshot, complete-v1 hashes,
  zero repository write access, web disabled, and subagents disabled. Its
  envelope was verified but not curated into `runs/`; the app-level MCP tool
  metadata in this already-open task remains cached on the legacy schema until
  the connector is reloaded.
- Validation: 16/16 synthetic tests; frozen synthetic check with eight
  scoring-eligible attempts and zero output bypasses; 6/6 bridge tests;
  canonical JSON Schema validation; v0.3 static and bounded live MCP smoke;
  Python/JavaScript/shell syntax; unique 70-field session registry;
  content-index, change-log, and repository-safety audits; and
  `git diff --check`.
- Project state: Operational private repository baseline with a pre-data v0.1
  research draft -> Phase 0B with WP0 v0.2 frozen, synthetic-only G0 component
  verification passed, hardened collaboration v0.3 and CI, and all participant
  activity still blocked pending WP1 and later gates.

### CHG-0013 - Draft PR opened and initial CI verified

- Event time: 2026-07-29 18:46-18:48 EDT
- Modification time: 2026-07-29 18:48 EDT
- Record type: External repository state verification and direct project-log
  append
- Changed paths and external state:
  - branch `codex/infra-and-synthetic-g0`
  - commit `ad2ff1b0fd52a449bad20783f89c40b703c4a7ae`
  - Draft PR `#4`: `https://github.com/chri7434-ux/Project_NRLIS/pull/4`
  - GitHub Actions run `30497290026`, job `90728947226`
  - `PROJECT_CHANGE_LOG.md`
- Brief: Pushed the audited Phase 0B and synthetic G0 change set, opened Draft
  PR #4 against `main`, and verified that the initial `Repository governance`
  workflow passed in 19 seconds. The PR remains draft and unmerged.
- Project state: Locally committed and audited feature branch -> private remote
  Draft PR with initial required CI passing, pending human review and a later
  explicit merge decision.

### CHG-0014 - WP1 governance preparation opened with fail-closed gates

- Event time: 2026-07-29 18:49-20:20 EDT
- Modification time: 2026-07-29 18:49-20:20 EDT; bounded official-source,
  independent repository-gap, and Grok reviews observed during the same event
  window
- Record type: Direct project modification, governance-work-package opening,
  combined machine-gate implementation, and bounded independent review
- Changed paths:
  - `.github/ISSUE_TEMPLATE/bug_report.yml`
  - `.github/dependabot.yml`
  - `.github/workflows/repository-governance.yml`
  - `AGENTS.md`
  - `AgentCollaboration/scripts/validate-artifacts.mjs`
  - `AgentCollaboration/tests/bridge.test.mjs`
  - `CONTENT_OF_WORK.md`
  - `GrossTree/Basic/Profiles/NRLIS-P001/INTAKE_CHECKLIST.md`
  - `GrossTree/Basic/Profiles/NRLIS-P001/PROFILE.md`
  - `GrossTree/Basic/Profiles/PROFILE_SCHEMA.md`
  - `GrossTree/Basic/Training/Config/baseline_v0.yaml`
  - `GrossTree/Basic/Training/Config/wp1_gate_registry.json`
  - `GrossTree/Basic/Training/Config/wp1_gate_registry.schema.json`
  - `GrossTree/Basic/Training/Dataset/DATA_CONTRACT.md`
  - `GrossTree/Basic/Training/Dataset/DATA_MANAGEMENT_WITHDRAWAL_PLAN.md`
  - `GrossTree/Basic/Training/Evaluation/T001_ANALYSIS_SPEC.md`
  - `GrossTree/Basic/Training/Implementation/README.md`
  - `GrossTree/Basic/Training/Implementation/test_validate_wp1.py`
  - `GrossTree/Basic/Training/Implementation/validate_wp1.py`
  - `GrossTree/Basic/Trials/NRLIS-T001/ACCESSIBLE_CONSENT_ASSENT_DISSENT_PLAN.md`
  - `GrossTree/Basic/Trials/NRLIS-T001/PROTOCOL.md`
  - `GrossTree/Basic/Trials/NRLIS-T001/TASK_REFERENCE_AUTHORSHIP_SOP.md`
  - `GrossTree/README.md`
  - `GrossTree/__init__/DECISION_LOG.md`
  - `GrossTree/__init__/EVIDENCE_REGISTER.md`
  - `GrossTree/__init__/PROJECT_CHARTER.md`
  - `GrossTree/__init__/PROJECT_OBJECTIVE_AND_ROADMAP.md`
  - `GrossTree/__init__/WP1_GOVERNANCE_AND_DETERMINATION_PLAN.md`
  - `PROJECT_CHANGE_LOG.md`
  - `README.md`
  - `requirements.txt`
- Brief: Formally opened WP1 as participant-neutral governance preparation,
  not as institutional approval or participant activity. Added the
  multi-institution determination plan, accessible consent/agreement/dissent
  plan, data-management and withdrawal plan, protocol ordering controls, and
  de-identified profile/intake placeholders. The authoritative registry
  remains `open_blocked_external_determinations`: all 25 gates are unresolved
  or in progress, all seven roles are unassigned, all 21 activity
  authorizations are false, all 21 consent scopes are `not_authorized`,
  external authority/evidence/training ledgers are empty, the scope hash is
  `null`, the pre-participant hold is active, and WP1 exit is false.
- Brief: Implemented an inseparable JSON-Schema and semantic WP1 CLI. It
  freezes per-gate evidence, authority, outcome, and recorder policies;
  role-specific competencies, independence, separation, holder coverage, and
  finite validity; current recorder-holder authorship; and a v1.1 scope
  manifest hashing the complete eight-document T001 normative set, protocol,
  and project charter. WP1 completion still cannot grant or inherit any
  participant activity.
- Brief: Replaced the prior two-level baseline scan with pinned PyYAML 6.0.3
  safe parsing, duplicate/merge/alias failure, recursive root/nested/list leaf
  inspection, strict scalar types, lowercase-snake-case keys, frozen deny-only
  flags, and rejection of all duplicate activity-state or unknown
  `*_enabled` fields. CI installs the Python and Ajv dependencies before the
  combined gate, and Dependabot now covers root Python dependencies.
- Brief: Independent official-source review preserved the Common Rule/FDA LAR
  distinction, all-applicable-institution and reliance responsibilities,
  conditional HIPAA/device language, and the rule that machine consistency
  cannot authenticate external issuance. Iterative repository-gap and bounded
  Grok reviews exposed and drove correction of gate-type, competency,
  canonical-scope, reviewer-turnover, combined-schema, baseline-depth/type,
  and path-encoding weaknesses. Final repository-gap and Grok R4 reviews
  reported no remaining critical or major issue. Grok snapshots were
  temporary, participant-neutral, web-disabled, and read-only; they were not
  curated into `runs/`.
- Validation: 68/68 Python tests (16 synthetic G0 and 52 WP1); synthetic
  validation/check with 10 retained attempts, eight scoring-eligible attempts,
  and zero output bypasses; combined 25-gate/7-role/21-activity WP1 check;
  7/7 bridge tests; canonical JSON Schema/artifact validation; fail-closed
  restricted-path smoke; Python/JavaScript/shell syntax; content-index,
  change-log, and repository-safety audits; and `git diff --check`.
- Project state: Draft PR with WP0 v0.2 and synthetic G0 -> WP1 governance
  preparation formally open but blocked on external determinations, qualified
  role appointments, accessible-consent approval, and approved data lifecycle;
  earned evidence remains G0 synthetic-only and no participant activity is
  authorized.

### CHG-0015 - WP1-Lite boundary and participant-free neural milestone

- Event time: 2026-09-04 22:24 CST (+0800)
- Modification time: 2026-09-04 22:06-22:24 CST (+0800), covering the
  documentation, implementation, validation, index, and local containment
  actions observed during this event window
- Record type: Direct project modification, participant-free work-package
  activation, synthetic neural implementation, and privacy containment
- Changed paths:
  - `.github/workflows/repository-governance.yml`
  - `CONTENT_OF_WORK.md`
  - `GrossTree/Basic/Training/Config/baseline_v0.yaml`
  - `GrossTree/Basic/Training/Config/participant_free_neural_v0.json`
  - `GrossTree/Basic/Training/Config/participant_free_neural_v0.schema.json`
  - `GrossTree/Basic/Training/Evaluation/participant_free_neural_v0_expected_metrics.json`
  - `GrossTree/Basic/Training/Implementation/README.md`
  - `GrossTree/Basic/Training/Implementation/participant_free_neural.py`
  - `GrossTree/Basic/Training/Implementation/test_participant_free_neural.py`
  - `GrossTree/README.md`
  - `GrossTree/__init__/DECISION_LOG.md`
  - `GrossTree/__init__/PROJECT_CHARTER.md`
  - `GrossTree/__init__/PROJECT_OBJECTIVE_AND_ROADMAP.md`
  - `GrossTree/__init__/WORKFLOW_AND_ALGORITHMS.md`
  - `GrossTree/__init__/WP1_GOVERNANCE_AND_DETERMINATION_PLAN.md`
  - `PROJECT_CHANGE_LOG.md`
  - `README.md`
  - unindexed local media directory, relocated intact to a non-Git quarantine
    outside the repository; no private asset filename is recorded here
- Brief: Reframed the current stage as WP1-Lite: participant-free engineering
  may proceed without implying enrollment, institutional determination, consent,
  approved storage, or any participant authorization. The Human-ready checkpoint
  remains the mandatory boundary before prospective family-member research.
- Brief: Formalized two purposes and three lanes. Participant-free engineering
  and ordinary family-care AAC may be developed separately, but care interactions
  do not silently become research data and cannot be retrospectively reused
  without the later approved pathway.
- Brief: Added a deterministic two-layer MLP over generated synthetic embeddings,
  disjoint development/calibration/test splits, calibration-only temperature
  selection, abstention, held-out metrics, and a tmp-only no-action artifact
  path. This verifies neural training and evaluation plumbing only; the synthetic
  vectors are not speech, and the result supports no participant, clinical,
  dialect-ASR, intent-decoding, or communication-benefit claim.
- Brief: Detected twelve ignored audio files in an unmanaged root directory
  during the content audit. Without inspecting their contents, they were moved
  intact to a local non-Git quarantine outside the repository. They were not
  indexed, committed, uploaded, analyzed, transformed, or used for training;
  quarantine is containment only and is not an approved research data store.
- Validation: 78/78 Python tests; deterministic synthetic G0 check; participant-
  free neural check with 48 held-out synthetic test examples, accuracy 0.875,
  zero participant claims, and zero output bypasses; combined 25-gate/7-role/
  21-activity WP1 check; 7/7 collaboration bridge tests; static restricted-path
  smoke; canonical artifact validation; Python and shell syntax; content-index
  and repository-safety audits; and `git diff --check`.
- Project state: WP1 governance preparation with an overly broad practical stop
  -> WP1-Lite participant-free engineering active with both deterministic and
  neural synthetic G0 plumbing verified. Human-ready remains unmet, all 21
  participant activity authorizations remain closed, and no family-member data
  may enter research, training, inference, or evaluation.

### CHG-0016 - WP2.1 recording intake and Care-mode AAC synthetic MVP v0.1

- Event time: 2026-09-04 23:19 CST (+0800)
- Modification time: 2026-09-04 22:25-23:19 CST (+0800), covering the
  framework, implementation, validation, interface, index, and browser-QA
  actions observed during this event window
- Record type: Direct project modification, participant-free intake-framework
  implementation, and synthetic care-interface milestone
- Changed paths:
  - `.github/workflows/repository-governance.yml`
  - `CONTENT_OF_WORK.md`
  - `GrossTree/Basic/CareAAC/README.md`
  - `GrossTree/Basic/CareAAC/app.js`
  - `GrossTree/Basic/CareAAC/index.html`
  - `GrossTree/Basic/CareAAC/styles.css`
  - `GrossTree/Basic/CareAAC/synthetic_vocabulary_v0.js`
  - `GrossTree/Basic/CareAAC/test_care_aac.py`
  - `GrossTree/Basic/Training/Config/baseline_v0.yaml`
  - `GrossTree/Basic/Training/Dataset/DATA_CONTRACT.md`
  - `GrossTree/Basic/Training/Dataset/RECORDING_INTAKE_AND_PROVENANCE.md`
  - `GrossTree/Basic/Training/Dataset/recording_intake_v0.schema.json`
  - `GrossTree/Basic/Training/Dataset/recording_intake_v0.synthetic.json`
  - `GrossTree/Basic/Training/Implementation/README.md`
  - `GrossTree/Basic/Training/Implementation/test_validate_recording_intake.py`
  - `GrossTree/Basic/Training/Implementation/validate_recording_intake.py`
  - `GrossTree/README.md`
  - `GrossTree/__init__/DECISION_LOG.md`
  - `GrossTree/__init__/PROJECT_OBJECTIVE_AND_ROADMAP.md`
  - `GrossTree/__init__/WORKFLOW_AND_ALGORITHMS.md`
  - `PROJECT_CHANGE_LOG.md`
  - `README.md`
- Brief: Added a deny-only recording-intake and provenance contract that records
  no audio, transcript, identifying name, content-bearing path, or participant
  approval. Its only executable fixture is zero-speaker and synthetic; the
  validator fails closed on real-recording classification, sensitive fields,
  reference qualification, split assignment, reuse, or authorization drift.
- Brief: Defined the later governed sequence for containment, source/control
  review, context classification, speaker and third-party review, separate
  collection/use scopes, reference qualification, and chronological splitting.
  These are specifications for future authorized work, not claims that any gate
  has been satisfied or that quarantined family recordings may be opened.
- Brief: Added Care-mode AAC synthetic MVP v0.1 as a static Chinese interface
  using generic phrases only. It supports context selection, four candidate
  choices, separate confirmation, cancel/repeat/no-match fallback, keyboard,
  pointer, automatic scanning, and bounded future switch/gaze event hooks. It
  has no microphone, recording, upload, file input, speech synthesis, analytics,
  cookies, storage, external network request, or research-data export.
- Validation: 90/90 Python implementation tests plus 9/9 CareAAC static tests;
  deterministic synthetic G0, participant-free neural G0, WP1 combined gate,
  recording-intake deny-only check, 7/7 collaboration bridge tests, static
  restricted-path smoke, canonical artifact validation, Python/JavaScript/shell
  syntax, `git diff --check`, and content-index/repository-safety audits. Browser
  QA covered desktop and 390-by-844 mobile layouts, pointer, keyboard, cancel,
  rejected confirmation, confirmed output, and auto-scan selection; observed
  browser state had no cookies or web storage, no console warning/error, and
  only four local static-resource requests. Temporary QA images and session
  artifacts were kept outside the repository.
- Project state: Participant-free synthetic neural G0 verified -> WP2.1
  Recording Intake + Provenance Framework and Care-mode AAC synthetic MVP v0.1
  verified. Human-ready remains unmet, all participant authorizations remain
  closed, and no family-member recording has been accessed, copied into the
  repository, analyzed, transcribed, transformed, or used for model work.

### CHG-0017 - WP2.2 synthetic interaction and vocabulary architecture

- Event time: 2026-09-05 00:41 CST (+0800)
- Modification time: 2026-09-04 23:30 through 2026-09-05 00:41 CST (+0800),
  covering architecture, schema, implementation, testing, interface, browser-
  QA, navigation, and governance updates observed during this event window
- Record type: Direct project modification, participant-free architecture
  milestone, and Care-mode interface revision
- Changed paths:
  - `.github/workflows/repository-governance.yml`
  - `CONTENT_OF_WORK.md`
  - `GrossTree/Basic/CareAAC/README.md`
  - `GrossTree/Basic/CareAAC/VOCABULARY_ARCHITECTURE.md`
  - `GrossTree/Basic/CareAAC/app.js`
  - `GrossTree/Basic/CareAAC/index.html`
  - `GrossTree/Basic/CareAAC/interaction_core.js`
  - `GrossTree/Basic/CareAAC/styles.css`
  - `GrossTree/Basic/CareAAC/synthetic_interactions_v1.json`
  - `GrossTree/Basic/CareAAC/synthetic_interactions_v1.schema.json`
  - `GrossTree/Basic/CareAAC/synthetic_vocabulary_v1.js`
  - `GrossTree/Basic/CareAAC/synthetic_vocabulary_v1.schema.json`
  - `GrossTree/Basic/CareAAC/test_care_aac.py`
  - `GrossTree/Basic/CareAAC/test_interaction_core.mjs`
  - `GrossTree/Basic/CareAAC/test_validate_care_architecture.py`
  - `GrossTree/Basic/CareAAC/validate_care_architecture.py`
  - `GrossTree/Basic/Training/Config/baseline_v0.yaml`
  - `GrossTree/README.md`
  - `GrossTree/__init__/DECISION_LOG.md`
  - `GrossTree/__init__/PROJECT_OBJECTIVE_AND_ROADMAP.md`
  - `GrossTree/__init__/WORKFLOW_AND_ALGORITHMS.md`
  - `PROJECT_CHANGE_LOG.md`
  - `README.md`
- Brief: Defined a versioned model-to-interface contract in which future models
  may propose only a stable concept ID or abstain. Semantic identity is now
  separated from canonical/compact Chinese surface forms and from context/panel
  navigation. The active fixture contains five contexts, ten fixed four-item
  panels, forty unique low-risk synthetic concepts, six mandatory navigation/
  safety actions, and no dialect, personal, model-generated, or clinical data.
- Brief: Added strict vocabulary and interaction schemas plus a fail-closed
  semantic validator. It rejects unknown fields, concept/panel collisions,
  content or identity fields, score/timing/log fields, model or personalization
  enablement, dialect claims, free text, auto-confirmation, care-to-research
  reuse, participant records, and malformed synthetic action arguments.
- Brief: Extracted one DOM-independent deterministic interaction core shared by
  browser and Node tests. Only its confirmation transition can create visual
  output. Hidden concepts cannot become pending; rejection, panel navigation,
  repeat, none, cancel, and fallback cannot bypass confirmation. Seven
  declarative synthetic scenarios cover the principal state transitions while
  storing no interaction history.
- Brief: Advanced the Care-mode UI to v0.2 with two panels per context, fixed
  four-item candidate sets, complete/compact surface selection, accessible
  panel navigation, and a unified `controlId` adapter for context, concept,
  confirmation, navigation, and fallback controls. The prior `choiceId` form is
  accepted only as a bounded compatibility alias. The v0.1 vocabulary remains
  as a superseded reference and is not loaded by the page.
- Validation: 90/90 Training Implementation Python tests; 23/23 CareAAC Python
  tests; 7/7 CareAAC Node state-machine tests; deterministic synthetic G0,
  participant-free neural G0, recording-intake, WP1 combined, and Care
  architecture checks; 7/7 collaboration bridge tests; restricted-path smoke;
  canonical artifact validation; Python/JavaScript/shell syntax; `git diff
  --check`; and change-log, content-index, and repository-safety audits. Headed
  Playwright QA covered desktop and 390-by-844 mobile layouts, panel navigation,
  compact rendering, pending-without-output, rejection and keyboard correction,
  explicit confirmation, Escape cancellation, and auto-scan context selection.
  The browser exposed no cookies or web storage, no console warning/error, and
  exactly five localhost static-resource requests; QA artifacts were moved
  outside the repository.
- Project state: WP2.1 intake and Care-mode v0.1 verified -> WP2.2 semantic
  vocabulary and deterministic synthetic interaction architecture verified.
  Earned evidence remains G0 synthetic-only; Human-ready and every participant
  activity remain closed. No family-member recording or real care interaction
  was accessed, entered, persisted, analyzed, transcribed, transformed, or used
  for training, evaluation, or vocabulary personalization.

### CHG-0018 - WP2.2 scan-focus and empty-context refinement

- Event time: 2026-09-05 00:43 CST (+0800)
- Modification time: 2026-09-05 00:42-00:43 CST (+0800)
- Record type: Corrective follow-up to CHG-0017 within the same WP2.2 delivery
- Changed paths:
  - `CONTENT_OF_WORK.md`
  - `GrossTree/Basic/CareAAC/app.js`
  - `PROJECT_CHANGE_LOG.md`
- Brief: After CHG-0017 was timestamped, refined automatic scanning so an open
  confirmation panel exposes only confirm/reject to the scan cycle; otherwise
  the cycle is limited to the controls relevant to whether a context is active.
  Repeating candidates before context selection now returns an explicit prompt
  rather than a misleading repetition message.
- Validation: 23/23 CareAAC Python tests, 7/7 CareAAC Node tests, Care
  architecture check, JavaScript syntax, and repository audits passed after the
  refinement.
- Project state: No stage or authorization change; WP2.2 remains verified,
  participant-free, synthetic-only, non-recording, non-persistent, and
  non-research in Care mode.

### CHG-0019 - WP2.3 synthetic intent adapter implementation started

- Event time: 2026-09-05 20:41:28 CST (+0800)
- Modification time: Observed 2026-09-05 20:41:28 CST (+0800)
- Record type: Direct participant-free implementation on `codex/wp2-3-synthetic-intent-routing`
- Changed paths:
  - `GrossTree/Basic/Training/Config/synthetic_intent_adapter_v0.json`
  - `GrossTree/Basic/Training/Config/synthetic_intent_adapter_v0.schema.json`
  - `GrossTree/Basic/Training/Implementation/synthetic_intent_adapter.py`
  - `CONTENT_OF_WORK.md`
  - `PROJECT_CHANGE_LOG.md`
- Brief: Added a frozen exact mapping from synthetic WATER/REPOSITION classes to existing concept IDs; PAIN and OTHER have no equivalent concept and must abstain. Full-class probabilities are never renormalized after filtering. Training/calibration use only generated development/calibration splits. The Care interface is not connected. Installed the required versioned local Git hook. Remote WP2.2 tree was checked identical to local despite different commit IDs from prior API publication; PRs #4-#6 remain open. The new branch intentionally continues the existing dependency stack.
- Validation: Pending implementation acceptance and repository audits.
- Project state: WP2.2 verified -> WP2.3 implementation in progress; earned evidence remains synthetic G0, with participant authorization and all participant output paths unchanged.

### CHG-0020 - WP2.3 regression, documentation and CI integration

- Event time: 2026-09-05 20:44:43 CST (+0800)
- Modification time: Observed 2026-09-05 20:44:43 CST (+0800)
- Record type: Direct participant-free implementation and verification preparation
- Changed paths:
  - `GrossTree/Basic/Training/Implementation/test_synthetic_intent_adapter.py`
  - `GrossTree/Basic/Training/Evaluation/SYNTHETIC_INTENT_ROUTING.md`
  - `GrossTree/Basic/Training/Evaluation/synthetic_intent_adapter_v0_expected.json`
  - `GrossTree/Basic/Training/Implementation/synthetic_intent_adapter.py`
  - `.github/workflows/repository-governance.yml`
  - `GrossTree/Basic/Training/Implementation/README.md`
  - `GrossTree/Basic/Training/Config/baseline_v0.yaml`
  - `GrossTree/__init__/PROJECT_OBJECTIVE_AND_ROADMAP.md`
  - `GrossTree/__init__/DECISION_LOG.md`
  - `README.md`
  - `GrossTree/README.md`
  - `CONTENT_OF_WORK.md`
  - `PROJECT_CHANGE_LOG.md`
- Brief: Added 17 acceptance tests, frozen synthetic routing expectations, a reproducible execution/limitations specification, implementation fingerprints, and exclusive tmp-only artifact creation. Updated CI, navigation, roadmap v0.6, baseline v1.1.0 and decision D039. The 480 crossed routes include 17 candidate routes, of which one is incorrect; thresholds were not altered after evaluation. Python validation dependencies were installed only in ignored tmp/wp23-venv; pinned npm validation dependencies were restored.
- Validation: Initial generated routing run completed; full acceptance and repository checks pending.
- Project state: WP2.3 implementation -> integrated WP2.3 verification candidate; participant permissions, research enrollment and Care UI model routing remain closed.

### CHG-0021 - WP2.3 local acceptance verified

- Event time: 2026-09-05 20:46:45 CST (+0800)
- Modification time: Observed 2026-09-05 20:46:45 CST (+0800)
- Record type: Verification completion and navigation status update
- Changed paths:
  - `CONTENT_OF_WORK.md`
  - `GrossTree/__init__/PROJECT_OBJECTIVE_AND_ROADMAP.md`
  - `GrossTree/__init__/DECISION_LOG.md`
  - `README.md`
  - `GrossTree/README.md`
  - `PROJECT_CHANGE_LOG.md`
- Brief: Updated project navigation and roadmap to WP2.3 verified. Reconstructed the exact unsigned remote WP2.2 Git object from API metadata and its already-matching tree, checked its SHA, and aligned only the new WP2.3 branch to that equivalent parent. Git HTTPS had failed; GitHub API reads remained available. Older local work branches and all uncommitted implementation changes were preserved.
- Validation: 107/107 Training Implementation Python tests (including 17 adapter tests); 23/23 CareAAC Python tests; 7/7 CareAAC Node tests; 7/7 collaboration bridge tests; deterministic G0, neural G0, adapter, intake, combined WP1 and vocabulary CLI checks; full Ajv validation of the new schema/config; canonical artifact validation; Python/JavaScript/shell syntax; git diff --check; append-only log, content-index and repository-safety audits (111 persistent files). An initial bridge invocation used system Python without PyYAML and failed; rerunning with the isolated dependency environment on PATH passed. No browser UI assets changed, so existing UI tests were retained without claiming a new browser session.
- Project state: Integrated WP2.3 verification candidate -> locally verified synthetic model-to-concept routing. GitHub publication/CI remains a separate next step; earned evidence remains G0 and all 21 participant activity authorizations remain closed.

### CHG-0022 - WP2.3 Draft PR published with exact Git identity

- Event time: 2026-09-05 20:48:55 CST (+0800)
- Modification time: Observed 2026-09-05 20:48:55 CST (+0800)
- Record type: Private GitHub publication verification and append-only local record
- Changed paths:
  - `PROJECT_CHANGE_LOG.md`
  - remote branch `codex/wp2-3-synthetic-intent-routing`
  - private repository Draft PR #7
- Brief: Published implementation commit `8871cbdf24593569ad0c702577675d996b298ccb`
  through Git Data API after Git HTTPS failures. Verified the remote tree and
  commit exactly match local Git; created Draft PR #7 against the WP2.2 branch
  and configured local tracking. The base is the verified remote WP2.2 commit
  `3d11fb79e3987391d3e6ac9e5eea6a5c1f44687e`. No main push or merge occurred.
- Validation: Local 144-test acceptance suite and required audits passed before
  publication. A tmp-only CLI run also generated inspectable synthetic artifacts.
  GitHub CI is evaluated independently for the final PR head; this record does
  not preclaim its result. The final log-only follow-up must pass both audits
  and the append-only check before publication.
- Project state: Locally verified WP2.3 -> published Draft PR #7, stacked after
  #4 -> #5 -> #6, with final remote CI verification pending. Participant, Care
  UI, and evidence boundaries are unchanged.

### CHG-0023 - CareAAC interface refresh layout and visual system

- Event time: 2026-09-05 21:02:58 CST (+0800)
- Modification time: Observed 2026-09-05 21:02:58 CST (+0800)
- Changed paths:
  - `GrossTree/Basic/CareAAC/index.html`
  - `GrossTree/Basic/CareAAC/styles.css`
  - `CONTENT_OF_WORK.md`
  - `PROJECT_CHANGE_LOG.md`
- Brief: Started the user-requested interface refresh before the next research
  node, on `codex/care-aac-interface-refresh` based on the verified PR #7 head.
  Replaced the long stacked layout with a desktop context sidebar, mobile context
  strip, two-column phrase cards, a native confirmation dialog, persistent
  current-message area and compact operation settings. Added a neutral visual
  system with system typography, restrained blue accents, inline icon slots,
  light material treatment and reduced-motion/transparency/contrast support.
  Installed the required local hook. Browser logic integration and visual QA
  are still in progress.
- Project state: WP2.3 verified with Care UI v0.2 -> Care UI v0.3 design in
  progress; research milestones, vocabulary, data and output boundaries unchanged.

### CHG-0024 - CareAAC modal, focus and scan interaction integration

- Event time: 2026-09-05 21:05:09 CST (+0800)
- Modification time: Observed 2026-09-05 21:05:09 CST (+0800)
- Changed paths:
  - `GrossTree/Basic/CareAAC/app.js`
  - `GrossTree/Basic/CareAAC/styles.css`
  - `PROJECT_CHANGE_LOG.md`
- Brief: Added source-controlled inline line icons and phrase-card rendering;
  preserved context button DOM identity for focus continuity; integrated the
  native modal with question-first focus, explicit confirm/reject, all four
  fallback/safety controls, bounded modal access events and native focus trapping.
  Auto-scan can continue into confirmation and can start inside the dialog;
  repeated held keys cannot advance confirmation, and select/summary controls
  do not trigger phrase shortcuts. Added reduced-motion-aware message reveal.
  UI revision is separate from the unchanged vocabulary version.
- Validation: Browser acceptance and repository audits pending.
- Project state: Care UI v0.3 design -> integrated interface for visual and
  interaction QA; vocabulary, deterministic core and research permissions unchanged.

### CHG-0025 - CareAAC keyboard containment and narrow-screen refinement

- Event time: 2026-09-05 21:08:48 CST (+0800)
- Modification time: Observed 2026-09-05 21:08:48 CST (+0800)
- Changed paths:
  - `GrossTree/Basic/CareAAC/app.js`
  - `GrossTree/Basic/CareAAC/styles.css`
  - `PROJECT_CHANGE_LOG.md`
- Brief: Browser QA found that native dialog tabbing could reach browser chrome
  after the final control. Added explicit forward/backward wrapping within the
  modal's visible buttons. Added four-character mobile context labels with full
  accessible labels and reduced desktop card height while keeping large phrase
  text and targets. No vocabulary or semantic meaning was changed.
- Validation: Initial desktop/mobile visual inspection passed; expanded browser
  acceptance is rerun after this correction.
- Project state: Interface QA candidate -> refined UI candidate; no research,
  permission, data, or core-state transition.

### CHG-0026 - CareAAC interface documentation and browser acceptance

- Event time: 2026-09-05 21:12:05 CST (+0800)
- Modification time: Observed 2026-09-05 21:12:05 CST (+0800)
- Changed paths:
  - `GrossTree/Basic/CareAAC/README.md`
  - `CONTENT_OF_WORK.md`
  - `PROJECT_CHANGE_LOG.md`
- Brief: Documented the UI v0.3.0 revision separately from the unchanged v0.2.0
  vocabulary/configuration version, native dialog access behavior, reduced-motion
  treatment, local-only launch command, design references, and tested browser
  scope. Updated index purposes/statuses without adding persistent files.
- Validation: 54 Chromium browser acceptance assertions passed, covering explicit
  confirmation, cancel/reject/fallback paths, keyboard and scan access, five
  viewport sizes from 320 to 1440 CSS pixels, 44px button targets, reduced motion,
  local-only resources, no persisted interaction data and no browser errors.
  Desktop/mobile board, confirmation and confirmed-message screenshots were
  visually inspected; QA scripts and images remain outside the repository.
  Final repository regression tests and audits follow this documentation change.
- Project state: Care UI v0.3.0 QA candidate -> browser-verified interface with
  synchronized operating documentation; WP2.3 remains the current research node.

### CHG-0027 - CareAAC interface final local verification

- Event time: 2026-09-05 21:12:56 CST (+0800)
- Modification time: Observed 2026-09-05 21:12:56 CST (+0800)
- Changed paths:
  - `PROJECT_CHANGE_LOG.md`
- Brief: Completed the interface refresh acceptance review. The 40 concepts in
  both display modes passed 80 card and 80 modal/reverse-focus checks at 320px;
  a real 2-second scan cycle required a separate Space activation to confirm.
  The local preview is served only at 127.0.0.1:8765.
- Validation: 144 existing automated tests passed (107 Training Python, 23
  CareAAC Python, 7 CareAAC Node, 7 collaboration Node), alongside 54 Chromium
  browser assertions, the extended phrase/scan checks, deterministic G0, neural
  G0, adapter, intake, WP1 and vocabulary checks, canonical schema validation,
  JavaScript syntax and static non-live bridge smoke. Append-only log, content
  index (111 files), repository safety (111 files), and diff whitespace audits
  passed; mandatory audits are repeated after this append before commit.
- Project state: Browser-verified UI v0.3.0 -> locally verified interface ready
  for a focused Draft PR stacked on #7. No new research node has started.

### CHG-0028 - CareAAC interface Draft PR publication

- Event time: 2026-09-05 21:13:55 CST (+0800)
- Modification time: Observed 2026-09-05 21:13:55 CST (+0800)
- Changed paths:
  - `PROJECT_CHANGE_LOG.md`
  - remote branch `codex/care-aac-interface-refresh`
  - private repository Draft PR #8
- Brief: Published commit `1a693e707e123b536165efe7d077c5114e474bcd`
  with Git Data API after the session's Git HTTPS failures. Verified exact local
  and remote tree/commit identity, then created Draft PR #8 against the verified
  WP2.3 branch (PR #7). Retained the existing review stack without merging.
- Validation: Local unit, browser, schema, smoke and required repository audits
  passed before publication. This log-only follow-up must pass mandatory audits
  before publication; final-head GitHub CI is verified separately and is not
  preclaimed by this entry.
- Project state: Locally verified UI v0.3.0 -> published Draft PR #8, pending
  final-head CI verification; WP2.3 remains the current research milestone.

### CHG-0029 - Public snapshot preparation

- Event time: 2026-10-30 CST (+0800)
- Modification time: 2026-10-30 CST (+0800)
- Changed paths:
  - `GrossTree/Literatures/` (removed)
  - `README.md`
  - `AGENTS.md`
  - `CONTENT_OF_WORK.md`
  - `PROJECT_CHANGE_LOG.md`
  - `.github/ISSUE_TEMPLATE/config.yml`
  - `GrossTree/README.md`
  - `GrossTree/__init__/EVIDENCE_REGISTER.md`
  - `GrossTree/__init__/PROJECT_CHARTER.md`
- Brief: Prepared a single-commit public snapshot of the verified
  `codex/care-aac-interface-refresh` head (`fc3878e`). Removed third-party
  full-text papers and paper-page images (cited by DOI instead); removed local machine paths;
  rewrote the README for public readers. No code, configuration, fixture or
  test was changed.
- Validation: Training and CareAAC Python test suites, CareAAC Node tests, and
  all `check` commands re-run on the snapshot before publication.
- Project state: Private development history -> public, participant-free
  snapshot of interface v0.3.0 and WP2.3. All evidence remains synthetic (G0).

