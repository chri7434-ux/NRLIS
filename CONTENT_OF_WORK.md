# Content of Work

**Role:** Authoritative project-wide content index  
**Location rule:** Kept at the project root, outside `GrossTree/`  
**Last audited:** 2026-09-05 20:46:45 CST (+0800)
**Current project state:** WP2.3 sealed synthetic model-to-concept routing verified within WP1-Lite; Human-ready checkpoint not met and all participant research activity blocked
**Canonical repository:** `chri7434-ux/Project_NRLIS`
**GitHub plugin access:** Verified 2026-07-29 17:08 EDT
**Repository governance:** PR-only, squash-only, automatic branch cleanup, read-only Actions token, local direct-main guard
**Server-side main protection:** Unavailable on current private-repository plan; documented local/CI fallback active

## 1. Maintenance contract

This file is the source of truth for:

- where every persistent project file belongs;
- what each directory is responsible for;
- what each indexed file contributes; and
- how future growth should be routed.

Every persistent file creation, move, rename, or deletion must update this file
in the same task. Every project modification must also append
`PROJECT_CHANGE_LOG.md`. Run `python3 scripts/audit_content_index.py` before
declaring the task complete.

Excluded from the manifest: `.DS_Store`, `tmp/`, cache files, generated
dependency trees, local virtual environments, version-control internals, and
approved private participant assets.

## 2. Root directory responsibilities

| Path | Responsibility | Placement rule |
|---|---|---|
| `/` | Global navigation and governance | Keep only entry points, total index, total log, workspace rules, ignore rules, and maintenance tooling |
| `.codex/` | Local Codex workspace configuration | Tool registration only; do not place research content or participant data here |
| `.github/` | GitHub repository automation and contribution intake | Keep deterministic workflows, dependency updates, PR templates, and issue forms here |
| `AgentCollaboration/` | Fail-closed Codex-Grok review bridge | Keep all substantive collaboration tooling, schemas, templates, tests, and bounded review records together |
| `GrossTree/` | All substantive NRLIS research and implementation content | Research material belongs below the responsible workstream, not at root |
| `scripts/` | Project-wide integrity and maintenance checks | Tools here must not contain participant data or research conclusions |

## 3. GrossTree directory responsibilities

| Directory | Responsibility | Put here | Do not put here |
|---|---|---|---|
| `GrossTree/__init__/` | Project definition and research-control layer | charter, boundaries, workflow rationale, safety, evidence, decisions, architecture | raw data, model checkpoints, participant identifiers |
| `GrossTree/Basic/` | Core Phase 0-1 workflow | profiles, trials, training contracts, initial implementation | speculative BCI/sEMG extensions |
| `GrossTree/Basic/CareAAC/` | Ordinary-care AAC software separated from research | synthetic vocabulary schemas, fixed phrase UI, deterministic interaction core/scenarios, access adapters, safety tests, and operating instructions | participant records, real interaction logs, analytics, research metrics, personalized phrases, or recording/model code |
| `GrossTree/Basic/Profiles/` | Capability-profile system | participant-neutral schemas and empty profile placeholders | completed profiles, names, direct identifiers, raw recordings |
| `GrossTree/Basic/Profiles/NRLIS-P001/` | First anchor-case profile | P001 intake and versioned profile | unrelated participants or raw media |
| `GrossTree/Basic/Trials/` | Study/session operations | protocol folders, session schemas, operational templates | model weights or literature |
| `GrossTree/Basic/Trials/NRLIS-T001/` | First N-of-1 shadow workflow | T001 protocol and logs/templates | live unapproved participant data |
| `GrossTree/Basic/Training/Config/` | Versioned executable configuration | frozen model/routing/safety configuration and synthetic baseline contracts | narrative research rationale |
| `GrossTree/Basic/Training/Dataset/` | Dataset governance and schemas | contracts, manifests, private-data rules, and release-review requirements | participant assets or unapproved reporting material |
| `GrossTree/Basic/Training/Evaluation/` | Metric and analysis definitions | metric contracts and future frozen analysis specs | outcome claims without protocol links |
| `GrossTree/Basic/Training/Implementation/` | Executable research plumbing | deterministic validators, baselines, and tests | participant assets or unreviewed output |
| `GrossTree/Extension/` | Later-phase research outside the core | sEMG, EEG, fMRI, BCI, experimental modalities | Phase 1 production dependencies |

## 4. Placement decision guide

When adding a file:

1. Project-wide navigation or governance -> root.
2. GitHub workflows, dependency automation, PR templates, or issue forms ->
   `.github/`.
3. Research boundary, rationale, architecture, evidence, or decision ->
   `GrossTree/__init__/`.
4. Non-recording ordinary-care AAC software -> `GrossTree/Basic/CareAAC/`.
5. Participant capability information -> the participant's folder under
   `GrossTree/Basic/Profiles/`.
6. Session or trial operation -> the protocol folder under
   `GrossTree/Basic/Trials/`.
7. Model parameters or routing flags -> `GrossTree/Basic/Training/Config/`.
8. Data schema, provenance, or split manifest ->
   `GrossTree/Basic/Training/Dataset/`.
9. Metrics or analysis specifications ->
   `GrossTree/Basic/Training/Evaluation/`.
10. Non-core sensing or future methods -> `GrossTree/Extension/`.
11. External primary literature is cited by reference only (DOI or URL); full-text papers are not redistributed in this public repository.

If no location fits, update the directory-responsibility table before creating
a new folder.

## 5. Human-readable file index

### Root governance

| File | Purpose | Status |
|---|---|---|
| `.editorconfig` | Normalizes UTF-8, LF endings, indentation, final newlines, and Markdown whitespace handling | Active |
| `.gitattributes` | Normalizes text line endings and marks literature/figure assets as binary | Active |
| `.gitignore` | Blocks temporary/runtime files, local environments, private participant areas, sensitive media, biosignals, and learned voice/model artifacts | Active |
| `AGENTS.md` | Enforces index, log, placement, and audit rules for future work | Active |
| `CONTRIBUTING.md` | Defines the privacy-preserving branch, audit, review, and contribution workflow | Active |
| `CONTENT_OF_WORK.md` | Master directory responsibility map and complete file index | Authoritative |
| `PROJECT_CHANGE_LOG.md` | Append-only record of time, paths, changes, and project-state transitions | Authoritative |
| `README.md` | Concise project and canonical repository entry point with high-level non-negotiable rules | Active |
| `REPOSITORY_GOVERNANCE.md` | Defines PR-only operation, CI controls, merge policy, hook behavior, and GitHub plan limitation | Active |
| `SECURITY.md` | Defines private reporting and containment boundaries for vulnerabilities, credentials, and participant-related events | Active |
| `requirements.txt` | Pins the safe YAML parser required by the fail-closed WP1 baseline gate | PyYAML 6.0.3 |
| `scripts/audit_change_log.py` | Requires every persistent change set to append, never rewrite, the authoritative project log | Active |
| `scripts/audit_content_index.py` | Detects persistent files missing from the manifest and stale indexed paths | Active |
| `scripts/audit_repository_safety.py` | Rejects unignored private paths, secret-like tokens, sensitive types, symlinks, and oversized files | Active |
| `scripts/install_git_hooks.sh` | Configures the versioned local hooks path for a clone | Active |
| `scripts/git-hooks/pre-push` | Blocks direct pushes or deletion of `main` unless a documented recovery override is active | Active |

### GitHub repository infrastructure

| File | Purpose | Status |
|---|---|---|
| `.github/workflows/repository-governance.yml` | Installs pinned Python/YAML and schema dependencies, then runs append-only log, index, safety, syntax, WP1, deterministic/neural/intake synthetic/intent-routing checks, Care-mode vocabulary/scenario/state-machine tests, and fail-closed collaboration checks on PRs and `main` | Active |
| `.github/dependabot.yml` | Maintains pinned GitHub Actions, root Python, and collaboration npm dependencies weekly | Active |
| `.github/pull_request_template.md` | Requires scope, boundary, privacy, index, log, and validation attestations | Active |
| `.github/ISSUE_TEMPLATE/config.yml` | Disables unstructured issues and routes sensitive matters to private reporting | Active |
| `.github/ISSUE_TEMPLATE/research_task.yml` | Structured evidence- and boundary-aware research task intake | Active |
| `.github/ISSUE_TEMPLATE/bug_report.yml` | Structured synthetic or disclosure-reviewed infrastructure and software bug intake | Active |

### Agent collaboration infrastructure

| File | Purpose | Status |
|---|---|---|
| `.codex/config.toml` | Fixed-location Codex discovery shim with explicit Grok model, reasoning, timeout, and snapshot limits | Active minimal configuration |
| `AgentCollaboration/README.md` | Explains collaboration boundaries, restricted paths, validation, and operating rules | Active |
| `AgentCollaboration/.gitignore` | Excludes generated collaboration-run contents while retaining the runs directory | Active |
| `AgentCollaboration/package.json` | Pins the collaboration validator/runtime dependencies and test commands | v0.3.0 active |
| `AgentCollaboration/package-lock.json` | Reproducibly locks the collaboration dependency graph | Active |
| `AgentCollaboration/grok-mcp/server.mjs` | Implements the bounded, fail-closed read-only review server with canonical task/review schemas and complete provenance | v0.3.0 active |
| `AgentCollaboration/runs/.gitkeep` | Preserves the review-run output directory without adding run data | Infrastructure placeholder |
| `AgentCollaboration/schemas/grok-review.schema.json` | Structured schema for Grok review outputs | Active |
| `AgentCollaboration/schemas/provenance.schema.json` | Validates complete v0.3 review provenance and explicitly bounded historical records | Active |
| `AgentCollaboration/schemas/task.schema.json` | Structured schema for bounded collaboration tasks | Active |
| `AgentCollaboration/scripts/smoke-test.mjs` | Tests MCP handshake, tool list, restricted participant-path rejection, and optional live review | Active |
| `AgentCollaboration/scripts/validate-artifacts.mjs` | Validates canonical collaboration, synthetic, and WP1 governance schemas, supports the fail-closed WP1-only CLI layer, and checks bounded historical review records | Active |
| `AgentCollaboration/tests/bridge.test.mjs` | Exercises portable startup, complete provenance, task validation, fail-closed review evidence, and combined WP1 schema/semantic CLI enforcement | 7 tests active |
| `AgentCollaboration/tests/fake-grok.mjs` | Deterministic local reviewer fixture used without live model access | Test fixture |
| `AgentCollaboration/templates/task.example.json` | Example bounded review task using current GrossTree paths | Active |
| `AgentCollaboration/runs/NRLIS-INFRA-BASELINE-001-R1/review.json` | Curated, non-sensitive Grok review of repository infrastructure gaps before explicit model pinning | Verified review record |
| `AgentCollaboration/runs/NRLIS-INFRA-BASELINE-001-R1/provenance.json` | Records the bounded historical review snapshot and explicitly marks its provenance as legacy-partial | Verified historical provenance |
| `AgentCollaboration/runs/NRLIS-SMOKE-001/provenance.json` | Records the historical v0.2.0 live smoke test and explicitly marks its provenance as legacy-partial | Verified historical infrastructure test |

### Research-control layer

| File | Purpose | Status |
|---|---|---|
| `GrossTree/README.md` | Routes the research subtree, Care-mode software, active participant-free work, and blocked participant-data work | Active |
| `GrossTree/__init__/PROJECT_OBJECTIVE_AND_ROADMAP.md` | Freezes the canonical objective, two-purpose/three-lane operating model, WP1-Lite boundary, WP2.1-WP2.3 delivery, and WP0-WP8 gates | v0.6 WP2.3 verified; Human-ready checkpoint blocked |
| `GrossTree/__init__/PROJECT_CHARTER.md` | Intended use, immediate-care/research separation, non-use, questions, phase-correct roles, claim limits, and WP1 routing | v0.3 WP1-Lite active; pre-participant |
| `GrossTree/__init__/WP1_GOVERNANCE_AND_DETERMINATION_PLAN.md` | Distinguishes participant-free WP1-Lite work from the full Human-ready checkpoint and defines applicability, external determinations, role separation, and exit gates | v0.4 WP1-Lite active; Human-ready external action pending |
| `GrossTree/__init__/GENERALIZATION_BOUNDARIES.md` | G0-G5 claim ladder, orthogonal operating modes, novelty contract, and claim mapping | v0.2 active |
| `GrossTree/__init__/WORKFLOW_AND_ALGORITHMS.md` | Capability routing, deep-learning methods, calibration, fusion, experiment order, synthetic neural milestone, recording-intake gate, and WP2.2 semantic-vocabulary/interaction contract | v0.4 active |
| `GrossTree/__init__/EVALUATION_SAFETY_GOVERNANCE.md` | Mode-specific metrics, dataset splitting, authorship, safety, consent, and reporting controls | v0.2 active |
| `GrossTree/__init__/EVIDENCE_REGISTER.md` | Evidence-to-design traceability including nuanced exemption, LAR, multi-institution, privacy, device, AI-governance, and accessibility anchors | v0.3 active |
| `GrossTree/__init__/DECISION_LOG.md` | Append-only material research-design decisions, including WP1-Lite right-sizing, family-care/research separation, bounded neural training, deny-only intake, stable concepts, and unified confirmation controls | Active through D039 |
| `GrossTree/__init__/Overall_view.png` | Visual overview of the capability-adaptive workflow | Current architecture image |

### Care-mode AAC

| File | Purpose | Status |
|---|---|---|
| `GrossTree/Basic/CareAAC/README.md` | Defines the non-research, non-recording Care-mode boundary, architecture files, local run instructions, interface design, access adapter, and safety behavior | UI v0.3.0; vocabulary v0.2.0 active |
| `GrossTree/Basic/CareAAC/VOCABULARY_ARCHITECTURE.md` | Defines stable concept/surface/navigation separation, interaction invariants, synthetic scenario purpose, and later private-overlay boundary | v0.1 WP2.2 normative design |
| `GrossTree/Basic/CareAAC/index.html` | Accessible Chinese app shell with responsive context sidebar, phrase cards, native confirmation dialog, current-message region, and operation settings | UI v0.3.0 synthetic care interface |
| `GrossTree/Basic/CareAAC/styles.css` | Apple-inspired neutral visual system, responsive cards, dialog transitions, scan focus, and motion/transparency/contrast preferences | UI v0.3.0 active |
| `GrossTree/Basic/CareAAC/synthetic_vocabulary_v0.js` | Frozen original generic four-context phrase bank | v0.1.0 superseded reference; not loaded |
| `GrossTree/Basic/CareAAC/synthetic_vocabulary_v1.schema.json` | Strict schema for modes, safety policy, taxonomy, fixed panels, stable concepts, and surface forms | v1.0 active |
| `GrossTree/Basic/CareAAC/synthetic_vocabulary_v1.js` | Frozen five-context, ten-panel, forty-concept generic Chinese vocabulary with canonical/compact renderings | v0.2.0 synthetic-only active |
| `GrossTree/Basic/CareAAC/interaction_core.js` | DOM-independent deterministic proposal, navigation, confirmation, rejection, cancel, repeat, none, fallback, and surface-mode state machine | v1.0.0 no-history core |
| `GrossTree/Basic/CareAAC/synthetic_interactions_v1.schema.json` | Strict schema for declarative participant-free state-transition scenarios | v1.0 active |
| `GrossTree/Basic/CareAAC/synthetic_interactions_v1.json` | Seven deterministic synthetic scenarios covering confirmation, correction, navigation, compact mode, fallback, repeat, cancel, and hidden-concept rejection | v1.0 synthetic-only |
| `GrossTree/Basic/CareAAC/app.js` | DOM adapter for fixed phrase cards, native confirmation dialog, focus containment, keyboard/scan access, bounded future gaze/switch controls, and explicit safety paths | UI v0.3.0; no persistence or transmission |
| `GrossTree/Basic/CareAAC/validate_care_architecture.py` | Composes strict schemas with semantic closure for vocabulary, panels, safety policy, and synthetic scenario arguments | v0.1.0 fail-closed validator |
| `GrossTree/Basic/CareAAC/test_validate_care_architecture.py` | Negative tests for schema drift, panel integrity, identity/content/score fields, model or personalization enablement, and scenario contamination | 13 tests active |
| `GrossTree/Basic/CareAAC/test_interaction_core.mjs` | Executes all declarative scenarios and verifies sole confirmation output, hidden-concept rejection, navigation, compact rendering, clearing, and no-history state | 7 tests active |
| `GrossTree/Basic/CareAAC/test_care_aac.py` | Static tests for v0.2 assets, synthetic classification, concept/panel references, CSP, no capture/persistence/exfiltration APIs, safety controls, and adapter contract | 10 tests active |

### Profiles and trials

| File | Purpose | Status |
|---|---|---|
| `GrossTree/Basic/Profiles/PROFILE_SCHEMA.md` | General capability-profile schema with provenance, separate permission scopes, and private-storage classification | v0.2 participant-neutral |
| `GrossTree/Basic/Profiles/NRLIS-P001/PROFILE.md` | Empty first anchor-case placeholder with no participant evidence | v0.0 pre-enrollment |
| `GrossTree/Basic/Profiles/NRLIS-P001/INTAKE_CHECKLIST.md` | Participant-specific intake questions gated on WP1 and private storage | Draft; use not authorized |
| `GrossTree/Basic/Trials/NRLIS-T001/PROTOCOL.md` | First prospective N-of-1 shadow protocol with separate participant-contact, Stage A1, and raw-media gates | v0.3 WP1-integrated; closed |
| `GrossTree/Basic/Trials/NRLIS-T001/ACCESSIBLE_CONSENT_ASSENT_DISSENT_PLAN.md` | Defines participant-neutral accessible consent, governing LAR definitions, participant agreement/dissent, permission scopes, re-consent, and withdrawal | v0.2 submission draft; not approved |
| `GrossTree/Basic/Trials/NRLIS-T001/TASK_REFERENCE_AUTHORSHIP_SOP.md` | Defines T0-T4 tasks, reveal order, reference provenance, authorship, eligibility, and novelty | v0.2 scientific contract; protocol v0.3; closed |
| `GrossTree/Basic/Trials/NRLIS-T001/session_log_template.csv` | Seventy-field flat attempt registry linked to normalized reference and prediction records | Template; no participant rows |

### Training, data, and evaluation

| File | Purpose | Status |
|---|---|---|
| `GrossTree/Basic/Training/Implementation/test_synthetic_intent_adapter.py` | Acceptance tests for exact meanings, calibration isolation, malformed packets, provenance, deterministic routing, and output/artifact boundaries | WP2.3 verified; synthetic-only |
| `GrossTree/Basic/Training/Evaluation/SYNTHETIC_INTENT_ROUTING.md` | WP2.3 mapping, calibration provenance, full-probability panel routing, regression denominators, error retention, and execution contract | WP2.3 verified; synthetic-only |
| `GrossTree/Basic/Training/Evaluation/synthetic_intent_adapter_v0_expected.json` | Frozen regression over 48 synthetic test vectors crossed with 10 panels; includes the observed candidate error | WP2.3 verified; synthetic-only |
| `GrossTree/Basic/Training/Config/synthetic_intent_adapter_v0.json` | Frozen model/vocabulary fingerprints, exact semantic mapping, probability/panel policy, and disabled output flags | WP2.3 verified; synthetic-only |
| `GrossTree/Basic/Training/Config/synthetic_intent_adapter_v0.schema.json` | Closed and type-strict configuration, synthetic score-packet, and sealed candidate-decision schemas | WP2.3 verified; synthetic-only |
| `GrossTree/Basic/Training/Implementation/synthetic_intent_adapter.py` | Generated-neural score calibration, bounded concept routing, abstention, and tmp-only synthetic verification CLI | WP2.3 verified; synthetic-only |
| `GrossTree/Basic/Training/Config/baseline_v0.yaml` | Machine-readable participant-free engineering status, neural/intake/Care-mode vocabulary/interaction routing, pointer-only WP1 authority, deny-only participant interlocks, contracts, and blocked Stage D state | v1.1.0; WP2.3 routing registered; participant paths disabled |
| `GrossTree/Basic/Training/Config/participant_free_neural_v0.json` | Frozen synthetic embedding generator, two-layer MLP, calibration, abstention, claim, and deny-only safety configuration | v0.1.0 participant-free neural G0 |
| `GrossTree/Basic/Training/Config/participant_free_neural_v0.schema.json` | Strict JSON Schema for the participant-free neural configuration | v0.1 active |
| `GrossTree/Basic/Training/Config/wp1_gate_registry.json` | Authoritative 25-gate, 7-role, 21-activity WP1 state with v1.1 complete-normative scope metadata, frozen competencies, empty external ledgers, and active hold | v0.3.0; open and fail-closed |
| `GrossTree/Basic/Training/Config/wp1_gate_registry.schema.json` | Strict JSON Schema for authorities, gate/role evidence, competency training, stable recorder holders, canonical scope, and authorization closure | v1.2 active |
| `GrossTree/Basic/Training/Config/synthetic_g0_baseline.json` | Deterministic fixed-bank rule baseline with output permanently disabled | v1.0 synthetic-only |
| `GrossTree/Basic/Training/Config/synthetic_g0_config.schema.json` | JSON Schema for the synthetic baseline configuration | v1.0 active |
| `GrossTree/Basic/Training/Dataset/DATA_CONTRACT.md` | Storage, identifiers, reference provenance, eligibility, split, deletion, N-of-1 privacy, release review, and the deny-only recording-intake gate | v0.5 active; no participant data |
| `GrossTree/Basic/Training/Dataset/DATA_MANAGEMENT_WITHDRAWAL_PLAN.md` | Defines private-store classes, access, retention, withdrawal, model disposition, historical media, incidents, and release-approved reporting | v0.2 approval pending |
| `GrossTree/Basic/Training/Dataset/RECORDING_INTAKE_AND_PROVENANCE.md` | Defines the deny-only intake sequence, recording-class routing, permission separation, provenance, chronology, and repository boundary | v0.1 participant-neutral; real ingest disabled |
| `GrossTree/Basic/Training/Dataset/recording_intake_v0.schema.json` | Strict recording-intake metadata schema with no authorized permission value and all action gates false | v0.1 deny-only |
| `GrossTree/Basic/Training/Dataset/recording_intake_v0.synthetic.json` | Zero-speaker synthetic metadata fixture for recording-intake contract verification | v0.1 synthetic-only |
| `GrossTree/Basic/Training/Dataset/synthetic_g0.schema.json` | Strict JSON Schema for participant-free synthetic G0 fixtures | v1.0 active |
| `GrossTree/Basic/Training/Dataset/synthetic_g0_fixture.json` | Ten-attempt deterministic synthetic fixture with separate scoring and challenge populations | v1.0 synthetic-only |
| `GrossTree/Basic/Training/Evaluation/METRICS.md` | Mode-specific definitions for coverage, hazard, calibration, latency, message success, and burden | v0.2 active |
| `GrossTree/Basic/Training/Evaluation/participant_free_neural_v0_expected_metrics.json` | Frozen held-out metrics and zero-participant/zero-output safety expectations for the synthetic neural baseline | v0.1 synthetic-only |
| `GrossTree/Basic/Training/Evaluation/T001_ANALYSIS_SPEC.md` | Freezes T001 populations, estimands, missingness, strata, and the blocked Stage D registry | v0.2.1; v0.3 protocol compatible; Stage D blocked |
| `GrossTree/Basic/Training/Evaluation/synthetic_g0_expected_metrics.json` | Frozen hash and metric expectation for deterministic synthetic verification | v1.0 synthetic-only |
| `GrossTree/Basic/Training/Implementation/README.md` | Routes deterministic, neural, intent-routing, recording-intake, and WP1 checks with claim boundaries, dependencies, and reproducible commands | Active |
| `GrossTree/Basic/Training/Implementation/participant_free_neural.py` | Standard-library deterministic two-layer MLP training, calibration, abstention, evaluation, and tmp-only artifact CLI over generated synthetic embeddings | v0.1.0 participant-free only |
| `GrossTree/Basic/Training/Implementation/synthetic_g0.py` | Standard-library validator, non-learning predictor, evaluator, and safe artifact CLI | v1.0.0; synthetic-only |
| `GrossTree/Basic/Training/Implementation/test_participant_free_neural.py` | Acceptance tests for strict synthetic-only configuration, split isolation, determinism, frozen metrics, claim limits, and disabled output | 10 tests active |
| `GrossTree/Basic/Training/Implementation/test_validate_recording_intake.py` | Negative tests for schema closure, sensitive fields, real context, permission/authorization drift, references, splits, and care-data reuse | 12 tests active |
| `GrossTree/Basic/Training/Implementation/test_synthetic_g0.py` | Acceptance tests for schema, leakage, splits, denominators, determinism, and output safety | 16 tests active |
| `GrossTree/Basic/Training/Implementation/validate_wp1.py` | Composes JSON Schema, recursive type-strict unambiguous YAML paths, and semantic enforcement of complete scope, single-source activity state, gate-specific authority/outcomes, frozen role policies, holder-at-decision, finite validity, holds, and zero inherited activity | Active fail-closed combined validator |
| `GrossTree/Basic/Training/Implementation/validate_recording_intake.py` | Validates only the WP2.1 synthetic metadata fixture and rejects real-recording, approval, reference, split, content, and authorization claims | v0.1 deny-only executable |
| `GrossTree/Basic/Training/Implementation/test_validate_wp1.py` | Negative and structural tests for arbitrary evidence, gate-specific authority/outcomes, full scope/protocol, expiry/revocation, frozen roles, holder turnover, root/deep/dotted YAML drift, typed interlocks, and zero inherited activity | 52 tests active |

### Literature

| File | Purpose | Status |
|---|---|---|

## 6. Complete indexed-file manifest

The audit tool reads only the paths between the following markers.

<!-- INDEXED_FILES_START -->
- `.codex/config.toml`
- `.editorconfig`
- `.gitattributes`
- `.github/ISSUE_TEMPLATE/bug_report.yml`
- `.github/ISSUE_TEMPLATE/config.yml`
- `.github/ISSUE_TEMPLATE/research_task.yml`
- `.github/dependabot.yml`
- `.github/pull_request_template.md`
- `.github/workflows/repository-governance.yml`
- `.gitignore`
- `AGENTS.md`
- `AgentCollaboration/.gitignore`
- `AgentCollaboration/README.md`
- `AgentCollaboration/grok-mcp/server.mjs`
- `AgentCollaboration/package-lock.json`
- `AgentCollaboration/package.json`
- `AgentCollaboration/runs/.gitkeep`
- `AgentCollaboration/runs/NRLIS-INFRA-BASELINE-001-R1/provenance.json`
- `AgentCollaboration/runs/NRLIS-INFRA-BASELINE-001-R1/review.json`
- `AgentCollaboration/runs/NRLIS-SMOKE-001/provenance.json`
- `AgentCollaboration/schemas/grok-review.schema.json`
- `AgentCollaboration/schemas/provenance.schema.json`
- `AgentCollaboration/schemas/task.schema.json`
- `AgentCollaboration/scripts/smoke-test.mjs`
- `AgentCollaboration/scripts/validate-artifacts.mjs`
- `AgentCollaboration/templates/task.example.json`
- `AgentCollaboration/tests/bridge.test.mjs`
- `AgentCollaboration/tests/fake-grok.mjs`
- `CONTENT_OF_WORK.md`
- `CONTRIBUTING.md`
- `GrossTree/Basic/CareAAC/README.md`
- `GrossTree/Basic/CareAAC/VOCABULARY_ARCHITECTURE.md`
- `GrossTree/Basic/CareAAC/app.js`
- `GrossTree/Basic/CareAAC/index.html`
- `GrossTree/Basic/CareAAC/interaction_core.js`
- `GrossTree/Basic/CareAAC/styles.css`
- `GrossTree/Basic/CareAAC/synthetic_interactions_v1.json`
- `GrossTree/Basic/CareAAC/synthetic_interactions_v1.schema.json`
- `GrossTree/Basic/CareAAC/synthetic_vocabulary_v0.js`
- `GrossTree/Basic/CareAAC/synthetic_vocabulary_v1.js`
- `GrossTree/Basic/CareAAC/synthetic_vocabulary_v1.schema.json`
- `GrossTree/Basic/CareAAC/test_care_aac.py`
- `GrossTree/Basic/CareAAC/test_interaction_core.mjs`
- `GrossTree/Basic/CareAAC/test_validate_care_architecture.py`
- `GrossTree/Basic/CareAAC/validate_care_architecture.py`
- `GrossTree/Basic/Profiles/NRLIS-P001/INTAKE_CHECKLIST.md`
- `GrossTree/Basic/Profiles/NRLIS-P001/PROFILE.md`
- `GrossTree/Basic/Profiles/PROFILE_SCHEMA.md`
- `GrossTree/Basic/Training/Config/baseline_v0.yaml`
- `GrossTree/Basic/Training/Config/participant_free_neural_v0.json`
- `GrossTree/Basic/Training/Config/participant_free_neural_v0.schema.json`
- `GrossTree/Basic/Training/Config/synthetic_g0_baseline.json`
- `GrossTree/Basic/Training/Config/synthetic_g0_config.schema.json`
- `GrossTree/Basic/Training/Config/synthetic_intent_adapter_v0.json`
- `GrossTree/Basic/Training/Config/synthetic_intent_adapter_v0.schema.json`
- `GrossTree/Basic/Training/Config/wp1_gate_registry.json`
- `GrossTree/Basic/Training/Config/wp1_gate_registry.schema.json`
- `GrossTree/Basic/Training/Dataset/DATA_CONTRACT.md`
- `GrossTree/Basic/Training/Dataset/DATA_MANAGEMENT_WITHDRAWAL_PLAN.md`
- `GrossTree/Basic/Training/Dataset/RECORDING_INTAKE_AND_PROVENANCE.md`
- `GrossTree/Basic/Training/Dataset/recording_intake_v0.schema.json`
- `GrossTree/Basic/Training/Dataset/recording_intake_v0.synthetic.json`
- `GrossTree/Basic/Training/Dataset/synthetic_g0.schema.json`
- `GrossTree/Basic/Training/Dataset/synthetic_g0_fixture.json`
- `GrossTree/Basic/Training/Evaluation/METRICS.md`
- `GrossTree/Basic/Training/Evaluation/SYNTHETIC_INTENT_ROUTING.md`
- `GrossTree/Basic/Training/Evaluation/T001_ANALYSIS_SPEC.md`
- `GrossTree/Basic/Training/Evaluation/participant_free_neural_v0_expected_metrics.json`
- `GrossTree/Basic/Training/Evaluation/synthetic_g0_expected_metrics.json`
- `GrossTree/Basic/Training/Evaluation/synthetic_intent_adapter_v0_expected.json`
- `GrossTree/Basic/Training/Implementation/README.md`
- `GrossTree/Basic/Training/Implementation/participant_free_neural.py`
- `GrossTree/Basic/Training/Implementation/synthetic_g0.py`
- `GrossTree/Basic/Training/Implementation/synthetic_intent_adapter.py`
- `GrossTree/Basic/Training/Implementation/test_participant_free_neural.py`
- `GrossTree/Basic/Training/Implementation/test_synthetic_g0.py`
- `GrossTree/Basic/Training/Implementation/test_synthetic_intent_adapter.py`
- `GrossTree/Basic/Training/Implementation/test_validate_recording_intake.py`
- `GrossTree/Basic/Training/Implementation/test_validate_wp1.py`
- `GrossTree/Basic/Training/Implementation/validate_recording_intake.py`
- `GrossTree/Basic/Training/Implementation/validate_wp1.py`
- `GrossTree/Basic/Trials/NRLIS-T001/ACCESSIBLE_CONSENT_ASSENT_DISSENT_PLAN.md`
- `GrossTree/Basic/Trials/NRLIS-T001/PROTOCOL.md`
- `GrossTree/Basic/Trials/NRLIS-T001/TASK_REFERENCE_AUTHORSHIP_SOP.md`
- `GrossTree/Basic/Trials/NRLIS-T001/session_log_template.csv`
- `GrossTree/README.md`
- `GrossTree/__init__/DECISION_LOG.md`
- `GrossTree/__init__/EVALUATION_SAFETY_GOVERNANCE.md`
- `GrossTree/__init__/EVIDENCE_REGISTER.md`
- `GrossTree/__init__/GENERALIZATION_BOUNDARIES.md`
- `GrossTree/__init__/Overall_view.png`
- `GrossTree/__init__/PROJECT_CHARTER.md`
- `GrossTree/__init__/PROJECT_OBJECTIVE_AND_ROADMAP.md`
- `GrossTree/__init__/WORKFLOW_AND_ALGORITHMS.md`
- `GrossTree/__init__/WP1_GOVERNANCE_AND_DETERMINATION_PLAN.md`
- `PROJECT_CHANGE_LOG.md`
- `README.md`
- `REPOSITORY_GOVERNANCE.md`
- `SECURITY.md`
- `requirements.txt`
- `scripts/audit_change_log.py`
- `scripts/audit_content_index.py`
- `scripts/audit_repository_safety.py`
- `scripts/git-hooks/pre-push`
- `scripts/install_git_hooks.sh`
<!-- INDEXED_FILES_END -->
