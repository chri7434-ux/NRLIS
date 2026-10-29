# NRLIS Research Workspace

**Current research state:** WP2.3 sealed synthetic model-to-concept routing
verified within WP1-Lite; WP0 v0.3 frozen; deterministic and
synthetic-neural G0 checks passed; Human-ready checkpoint not met;
pre-participant-data

**Research contact, pre-consent access checks, intake, enrollment, and
recording:** Closed

**Participant-data model training:** Disabled; participant-free synthetic
neural training: active

**T001 operating mode:** Shadow only; output disabled

`GrossTree/` contains the substantive research definition, participant-neutral
schemas, protocol contracts, model/evaluation configuration, extensions, and
source evidence for Project NRLIS.

## Start here

1. `__init__/PROJECT_OBJECTIVE_AND_ROADMAP.md` - canonical objective, current
   boundaries, and gated research progression.
2. `__init__/PROJECT_CHARTER.md` - intended use, non-use, research questions,
   roles, and phases.
3. `__init__/WP1_GOVERNANCE_AND_DETERMINATION_PLAN.md` - current WP1
   applicability matrix, required roles, external request, and exit gates.
4. `__init__/GENERALIZATION_BOUNDARIES.md` - G0-G5 ladder, novelty contract, and
   claim-task-metric mapping.
5. `__init__/EVALUATION_SAFETY_GOVERNANCE.md` - project-wide evaluation,
   authorship, consent, safety, and reporting rules.
6. `Basic/Trials/NRLIS-T001/PROTOCOL.md` - first P001 shadow protocol, currently
   draft and closed.
7. `Basic/Trials/NRLIS-T001/ACCESSIBLE_CONSENT_ASSENT_DISSENT_PLAN.md` -
   participant-neutral consent-access and dissent design.
8. `Basic/Trials/NRLIS-T001/TASK_REFERENCE_AUTHORSHIP_SOP.md` - task taxonomy,
   reference acquisition, candidate blindness, and bounded authorship rules.
9. `Basic/Training/Evaluation/T001_ANALYSIS_SPEC.md` - shadow estimands,
   missingness rules, and blocked numerical gate registry.
10. `Basic/Training/Dataset/DATA_CONTRACT.md` - identifiers, storage,
   provenance, eligibility, and split contract.
11. `Basic/Training/Dataset/DATA_MANAGEMENT_WITHDRAWAL_PLAN.md` - private
    storage, access, retention, withdrawal, deletion, and incident design.
12. `Basic/Training/Config/wp1_gate_registry.json` - fail-closed WP1 roles,
    gates, holds, permission scopes, and activity authorizations.
13. `Basic/Training/Implementation/participant_free_neural.py` - deterministic
    participant-free neural training, calibration, abstention, and evaluation
    check; it is not an ASR benchmark.
14. `Basic/Training/Dataset/RECORDING_INTAKE_AND_PROVENANCE.md` - deny-only
    recording classification, provenance, permission, and split framework;
    real-recording ingest remains disabled.
15. `Basic/CareAAC/README.md` - local non-research synthetic communication board
    with explicit confirmation, cancel, fallback, and switch/gaze adapter
    contract; it records nothing.
16. `Basic/CareAAC/VOCABULARY_ARCHITECTURE.md` - stable concept/surface/panel
    separation, deterministic interaction invariants, synthetic scenarios, and
    the later private-overlay boundary.

17. `Basic/Training/Evaluation/SYNTHETIC_INTENT_ROUTING.md` - WP2.3 sealed
    synthetic model-to-concept mapping, calibration, panel routing, and regression.

## Directory routing

- `__init__/`: objective, architecture, boundaries, evidence, safety, and
  research decisions.
- `Basic/CareAAC/`: non-recording, non-persistent Lane B AAC software built and
  tested with generic synthetic content; never store care interaction records
  here.
- `Basic/Profiles/`: participant-neutral capability schema and empty profile
  placeholders; completed participant profiles belong in approved private
  storage.
- `Basic/Trials/`: versioned session and protocol operations.
- `Basic/Training/Config/`: machine-readable routing, model, safety, and gate
  configuration.
- `Basic/Training/Dataset/`: schemas, synthetic fixtures, provenance, and split
  contracts.
- `Basic/Training/Evaluation/`: metrics and frozen analysis specifications.
- `Extension/`: later-phase modalities such as sEMG, EEG, fMRI, and BCI; none
  is part of the Phase 1 core.
- External source evidence is cited by DOI in `__init__/EVIDENCE_REGISTER.md`;
  full-text papers are not redistributed here.

## Non-negotiable interpretation rules

- The workflow contract, not a universal intent decoder, is the initial unit of
  generalization.
- A candidate meaning is a model hypothesis, not the participant's intent.
- Prompt acceptance, pre-reveal reference, post-reveal selection, and output
  authorization are different records.
- Shadow mode does not estimate actual message completion or actual
  Time-to-Message.
- Output requires a separately approved confirmed-assistive protocol and an
  independently validated participant-authorship action.
- Voice synthesis may render an already confirmed message; it cannot provide
  evidence of intent.
- P001 can support at most G2. G3 and above require independent participants.
- No research document, schema, configuration, or synthetic fixture authorizes
  enrollment, recording, clinical use, or participant-data training.
- WP1 completion, if later achieved, authorizes no participant activity by
  inheritance; an exact approved activity and protocol version are still
  required.

Repository-wide navigation, change logging, privacy rules, and audits are
governed by the root `CONTENT_OF_WORK.md`, `AGENTS.md`,
`REPOSITORY_GOVERNANCE.md`, and `SECURITY.md`.
