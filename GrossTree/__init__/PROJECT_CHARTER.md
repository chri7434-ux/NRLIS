# NRLIS Research Charter

**Version:** 0.3

**Status:** WP1-Lite participant-free engineering active; Human-ready
checkpoint not met; pre-participant-data

**First anchor case:** NRLIS-P001, not yet enrolled

**First feasibility protocol:** NRLIS-T001, shadow mode only

## 1. Research objective

Develop and prospectively evaluate a versioned, safety-gated,
capability-adaptive assistive-communication workflow that selects the least
burdensome reliable available channel, generates bounded and calibrated
candidate meanings, abstains or falls back when evidence is insufficient,
permits output only after an independently validated participant-authorship
action, and adapts only from provenance-qualified labels.

The primary research contribution is a repeatable development and evaluation
paradigm. The initial unit of generalization is the workflow contract, not a
single model that works without personal calibration. The canonical objective
and gated progression are maintained in `PROJECT_OBJECTIVE_AND_ROADMAP.md`.

## 2. Intended use statement

NRLIS is an investigational assistive-communication workflow. It is designed to
support people whose natural speech does not reliably meet their communication
needs. It may supplement residual speech and established Augmentative and
Alternative Communication (AAC), but it does not replace clinical assessment or
existing reliable communication methods.

The first implementation will be limited to:

- adult acquired communication impairment;
- non-invasive, consumer-accessible input modalities;
- a participant with at least one independently verifiable response channel;
- short, user-relevant messages before open-ended conversation;
- offline or shadow-mode inference before confirmed output; and
- personalized modeling with explicit, provenance-tracked labels.

### 2.1 Immediate-help and research separation

The project does not require P001 to wait for a research model before using
ordinary communication support. Participant-free engineering and ordinary
family-care AAC may proceed in parallel:

- participant-free engineering uses only synthetic or appropriately licensed
  public data and cannot make a participant-performance claim;
- ordinary care may use non-recording communication boards, pictures, writing,
  gestures, direct selection, generic text-to-speech, and other agreed AAC
  supports for P001's benefit; and
- care observations and historical family knowledge are not silently copied
  into a research profile, dataset, model, metric, or publication.

Systematic collection or analysis for training, evaluation, publication, or
generalizable knowledge is a separate prospective research lane. Declining
that lane must not reduce P001's access to ordinary communication support.

## 3. Explicit non-use statement

Until later evidence and review support expansion, NRLIS must not be represented
as:

- a brain-reading or consciousness-detection system;
- a diagnostic, prognostic, or treatment system;
- an autonomous interpreter of a person's wishes;
- evidence of decision-making capacity;
- a substitute for informed consent;
- the sole communication route for emergencies or high-stakes decisions;
- a pediatric, dementia, altered-consciousness, or psychiatric assessment tool;
  or
- a clinically validated medical device.

## 4. Primary research questions and evidence targets

| Research question | Earliest applicable evidence | Current status |
|---|---|---|
| Can capability-based routing identify a usable route more reliably than diagnosis-only routing? | Independent participants across capability strata; G3-G4 | Deferred; P001 cannot answer this |
| Does personal adaptation improve candidate coverage on future sessions, contexts, and precisely defined novelty classes? | Frozen P001 later-session shadow evaluation; at most G2 | T001 target |
| Can calibrated abstention prevent weak evidence from becoming an incorrect non-abstained candidate? | Controlled G1 and prospective G2 shadow evaluation | T001 target |
| Does explicit confirmation preserve authorship while reducing actual Time-to-Message or selection burden? | New confirmed-assistive protocol; at most G2 for P001 | Not estimable in T001 shadow mode |
| Can the workflow detect fatigue, session variation, or progression-related drift before performance becomes unsafe? | Longitudinal, frozen P001 blocks; at most G2 | Later Phase 1 target |

## 5. Initial contribution claims allowed

If its applicable gates and prospective design are completed, the first family
case may support claims about:

- feasibility for one anchor participant;
- shadow-workflow operation and failure modes;
- within-person longitudinal adaptation;
- profile and session workflow completeness;
- prospective shadow-mode performance; and
- engineering readiness for evaluation with independent participants.

It may not support claims about:

- population accuracy;
- clinical effectiveness;
- cross-dialect or cross-diagnosis performance;
- restoration of language or cognition; or
- reliable communication for people without a verifiable response channel.

Prompted-target performance is not evidence of spontaneous authorship.
Post-reveal candidate selection may authorize that selected output under a
future protocol, but is not an unbiased reference for prior model accuracy.

## 6. Roles at the correct stage

During participant-free engineering, the project/scope owner, technical owner,
and synthetic-data/release custodian are responsibility hats and may be held by
one builder. This does not assign or verify a formal WP1 role.

Before participant data collection intended for research or publication, the
project must activate and verify the applicable full responsibilities:

- participant or legally valid representative, as applicable;
- an independent person responsible for consent accessibility and dissent;
- a Speech-Language Pathologist (SLP) or equivalent clinical collaborator;
- a technical lead;
- a data steward;
- an ethics/IRB contact or documented determination; and
- a person other than the family investigator who can review adverse or
  ambiguous communication events.

The family investigator must not be the sole judge of the participant's intent,
consent capacity, or success.

WP1 role assignments are tracked by stable opaque holder IDs, current training
records, and ledger-bound evidence in
`WP1_GOVERNANCE_AND_DETERMINATION_PLAN.md` and the machine-readable gate
registry. Opening WP1 does not count as assigning or verifying any role.

## 7. Phase model

### Phase 0 - Protocol, infrastructure, and participant-free modeling

- Freeze intended use and non-use.
- Define capability profile, task and authorship SOP, data contract, analysis
  specification, risk controls, and baselines.
- Verify deterministic and neural-training plumbing with synthetic data before
  participant data. These checks do not establish speech-recognition or
  participant performance.
- Obtain an ethics/IRB determination before prospective research data
  collection.

### Phase 1A - P001 capability and communication baseline

- Document observed abilities separately from clinical diagnoses.
- Establish at least one reproducible yes/no, cancel, or direct-selection
  channel.
- Measure current unaided and low-tech AAC communication performance.

### Phase 1B - P001 shadow-mode N-of-1

- Generate predictions without speaking or acting on them.
- Evaluate by future date, context, fatigue state, and the registered
  multi-axis novelty taxonomy.
- Freeze the algorithm before the prospective test segment.

### Phase 1C - P001 confirmed assistive mode

- Enter only after predefined safety and performance gates are met.
- Require confirmation before output.
- Keep a low-tech fallback continuously available.

### Phase 2 - Independent participant feasibility

- Recruit across capability strata, not diagnosis alone.
- Use frozen workflow interfaces and pre-specified evaluation.
- Test leave-one-person-out and fully held-out participants.

### Phase 3 - Early live clinical evaluation

- Add clinical workflow and human-factors evaluation.
- Use appropriate reporting guidance such as DECIDE-AI when applicable.
- Establish lifecycle monitoring consistent with Good Machine Learning
  Practice if the project becomes a medical-device program.

## 8. Normative research contracts

- `PROJECT_OBJECTIVE_AND_ROADMAP.md`: canonical objective and gated work
  packages.
- `WP1_GOVERNANCE_AND_DETERMINATION_PLAN.md`: applicable-determination,
  independent-role, and WP1 exit requirements.
- `GENERALIZATION_BOUNDARIES.md`: G0-G5 ladder and claim-task-metric mapping.
- `../Basic/Trials/NRLIS-T001/ACCESSIBLE_CONSENT_ASSENT_DISSENT_PLAN.md`:
  accessible consent, participant agreement/dissent, and separate permission
  scopes.
- `../Basic/Trials/NRLIS-T001/TASK_REFERENCE_AUTHORSHIP_SOP.md`: task,
  reference, reveal, and authorship rules.
- `../Basic/Training/Evaluation/T001_ANALYSIS_SPEC.md`: shadow estimands and
  promotion registry.
- `../Basic/Training/Dataset/DATA_CONTRACT.md`: provenance and split rules.
- `../Basic/Training/Dataset/DATA_MANAGEMENT_WITHDRAWAL_PLAN.md`: storage,
  access, retention, withdrawal, deletion, and incident controls.

No contract authorizes enrollment, recording, participant-data training, or
assistive output while its applicable gates remain incomplete.

## 9. Change control

Every material change must record:

- version and date;
- reason for change;
- data visible when the decision was made;
- affected profiles or sessions;
- whether prior test data have become development data; and
- which claims remain valid.

Once a test set or prospective period influences design, it is no longer an
independent test.

## 10. Local evidence anchors

- Green et al. (2021), doi:10.21437/Interspeech.2021-1384: supports
  personalized ASR for prompted short phrases, while documenting limitations in
  longer, spontaneous, noisy, and severely impaired speech.
- Tang et al. (2023), doi:10.1038/s41593-023-01304-9: supports the scientific possibility of
  person-specific non-invasive semantic decoding under fMRI, while documenting
  the need for subject cooperation and extensive individual training.
