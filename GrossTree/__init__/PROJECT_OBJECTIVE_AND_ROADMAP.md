# NRLIS Project Objective and Research Roadmap

**Version:** 0.6

**Status:** WP2.3 synthetic model-to-concept routing verified;
Human-ready checkpoint not met; pre-participant-data

**Participant-data authorization:** None

**Planned evidence ceiling after later gates:** G2 within-person prospective
evidence for P001; current earned evidence remains synthetic G0 only

## 1. Canonical objective

Develop and prospectively evaluate a versioned, safety-gated,
capability-adaptive assistive-communication workflow that:

1. characterizes observable communication capabilities without inferring a
   diagnosis;
2. routes consented signals through the least burdensome reliable available
   channel;
3. generates a bounded, calibrated set of candidate meanings;
4. abstains or falls back when evidence is insufficient;
5. permits speech, transmission, or action only after a participant-authorship
   action through an independently validated channel; and
6. adapts only from provenance-qualified labels under explicit version control.

The initial empirical target is prospective, within-person technical and
feasibility evidence for P001. The initial generalization target is the
workflow contract, not a universal decoder. Workflow portability requires
independent participants at G3 or above.

## 2. Research contribution

The intended contribution is a reproducible method for moving from:

`capability assessment -> route selection -> reference acquisition -> candidate
inference -> calibration/abstention -> participant confirmation -> safe output
-> confirmed-only adaptation -> drift monitoring`

The project tests whether each step is measurable, auditable, and safe enough
to support the next step. A more complex model is justified only when it adds
value beyond unaided communication, low-tech AAC, direct access, and simpler
personalized baselines.

Voice synthesis, if studied later, is a downstream renderer for an already
confirmed message. Historical voice recordings do not establish current intent
and do not substitute for post-impairment paired signals and qualified labels.

## 2.1 Two purposes and three operating lanes

NRLIS has two purposes that must advance without being confused:

1. improve P001's practical communication options as soon as reasonably
   possible; and
2. develop a reproducible workflow that can later support research claims.

The project therefore uses three lanes:

- **Lane A - participant-free engineering:** code, synthetic or appropriately
  licensed public data, model interfaces, simulated access methods, evaluation,
  calibration, abstention, and output interlocks. This lane is active now.
- **Lane B - ordinary family care and co-design:** non-recording, non-research
  AAC support used for P001's immediate benefit. It is not a source of NRLIS
  research or training data, and refusal to join research never removes this
  support.
- **Lane C - prospective N-of-1 research:** systematic collection or analysis
  of P001 information for model training, evaluation, publication, or
  generalizable knowledge. This lane remains closed until the Human-ready
  checkpoint and activity-specific gates are satisfied.

`WP1-Lite` names the current operating profile across Lane A and participant-
neutral preparation. It is not an ethics determination, registry status,
participant enrollment, or a shortened route into Lane C.

## 3. Explicit non-objectives

The current program does not seek to establish:

- brain reading, consciousness detection, or access to unexpressed thought;
- diagnosis, prognosis, treatment, or restoration of language or cognition;
- autonomous interpretation of a person's wishes;
- decision-making capacity;
- safe emergency, medical, legal, financial, or consent communication;
- a universal model requiring no personal calibration; or
- clinical effectiveness or population generalization from P001.

## 4. Two independent progression axes

Evidence scope and operating mode are separate:

- the **G0-G5 ladder** describes how far evidence generalizes; and
- **shadow versus confirmed-assistive mode** describes whether a prediction can
  be shown, spoken, transmitted, or acted upon.

A P001 confirmed-assistive study can remain G2. A high G-level claim does not
authorize output. Moving from shadow to assistive mode requires a new protocol
version and approval even if the underlying model is unchanged.

## 5. Rational work-package roadmap

| Work package | Purpose | Entry condition | Required exit evidence | Current state |
|---|---|---|---|---|
| WP0 - Scientific contract | Freeze objective, tasks, reference/authorship rules, metrics, and gates | Repository governance available | Versioned normative contracts with no unresolved mode or label ambiguity | Complete for v0.3; Stage D numerical gates intentionally deferred |
| WP1 - Human-ready checkpoint | Resolve the applicable oversight route and prepare only the roles, accessible-consent, private-data, and activity-specific controls needed before Lane C | WP0 boundaries sufficiently stable; Lane A may continue in parallel | All machine-registry gates terminally supported, required roles verified, approved accessible-consent and data-lifecycle paths, and independent exit-review pass; no inherited activity authorization | Full checkpoint open but not met; formal staffing and external action deferred until a determination request or participant-facing transition |
| WP2 - Participant-free G0 engineering | Implement schemas, validators, deterministic and neural-training baselines, provenance, calibration, abstention, and fail-closed output controls without participant data | WP0 machine-readable fields defined | Reproducible synthetic end-to-end runs; zero prohibited output paths; schema, split, calibration, provenance, vocabulary, interaction-state, and claim-boundary checks pass | Active; deterministic and neural G0 plumbing, WP2.1 intake/Care interface, and WP2.2 vocabulary/interaction architecture verified; WP2.3 sealed model-to-concept routing verified; no speech, participant, or clinical-performance claim |
| WP3 - P001 capability and non-AI baseline | Establish reliable access, confirmation, cancel, fallback, and current communication performance | WP1 complete; protocol authorizes the activity | Versioned profile, confirmation reliability rule, fatigue/stop limits, and best non-AI baseline | Blocked |
| WP4 - Prompted calibration dataset | Collect qualified, provenance-tracked development labels | WP3 gates pass; approved recording/storage active | Frozen data manifest with chronological development/calibration partitions and overlap audit | Blocked |
| WP5 - Model development | Compare deterministic, generic, constrained personalized, and frozen-encoder approaches | WP4 development data available | Selected model/configuration, calibration and abstention policy, documented baseline comparison | Blocked |
| WP6 - Frozen prospective shadow block | Test later-session, held-out, and eligible naturalistic attempts without output | All Stage D thresholds and artifacts locked before first attempt | Locked analysis result and independent pass/fail/inconclusive review; P001 claim ceiling G2 | Blocked |
| WP7 - Confirmed-assistive feasibility | Evaluate actual message completion, burden, and authorship under confirmation | WP6 promotion gate passes; new protocol and approval | Low-risk confirmed-output evidence with zero serious authorship events | Blocked |
| WP8 - Independent participant replication | Test workflow portability across capability strata | Independent protocol, roles, and governance | G3 matched-stratum evidence, then separately justified G4 expansion | Blocked |

Lane A and WP2 are active under the WP1-Lite operating profile. Full WP1 is a
Human-ready checkpoint, not a prerequisite for participant-free engineering.
Its current machine registry keeps all 21
participant-activity permissions false and all permission scopes
`not_authorized`. WP3 and all later work remain blocked until their stated
gates pass. This roadmap does not authorize contact for research, enrollment,
intake, recording, participant profiling, historical-media ingest,
participant-specific inference, model training, candidate reveal, or output.

### 5.1 WP2.1 delivered boundary

WP2.1 adds two participant-neutral components:

- a deny-only recording-intake and provenance schema, synthetic fixture,
  semantic validator, and negative tests; and
- a local Care-mode AAC synthetic MVP with bounded generic candidates,
  `none/repeat/cancel/fallback` controls, explicit user confirmation, keyboard
  and auto-scan access, a future gaze/switch event adapter, and no capture,
  persistence, transmission, synthesized speech, or research logging.

The intake framework contains no authorized permission state and does not
accept real participant records. The Care-mode interface is Lane B support,
implemented with Lane A synthetic content. Its transient selections and use
must not be converted into research or training data. Neither component opens
WP3, changes the WP1 registry, or raises the earned claim above G0.

### 5.2 WP2.2 delivered boundary

WP2.2 replaces phrase text as the system interface with a versioned semantic
contract. Forty generic synthetic concepts are separated from their canonical
and compact Chinese surface forms, organized into five contexts and ten fixed
four-item panels, and restricted to ordinary low-risk care expression. Stable
concept IDs are the only future model-facing target. Panel IDs are navigation,
not labels, and changing surface form does not change meaning.

A DOM-independent deterministic state machine now mediates context selection,
panel navigation, proposal, rejection, confirmation, repeat, cancel, none, and
fallback. Only confirmation can create a visual user message. Seven declarative
synthetic interaction scenarios execute against the same core used by the
browser; strict schema and semantic checks reject model inference,
personalization, dialect claims, free text, auto-confirmation, hidden concepts,
interaction records, and care-to-research reuse.

This architecture is a reusable engineering pattern, not a validated vocabulary
for P001 or any patient group. It contains no dialect or personal overlay, model
scores, recordings, interaction timing, clinical content, or participant data.
It does not open WP3 or any WP1 activity authorization and does not raise the
earned claim above G0.

### 5.3 WP2.3 delivered boundary

WP2.3 routes the existing synthetic four-class MLP through an exact versioned
model-to-concept mapping with calibration-only temperature fitting, full-class
probabilities, panel restrictions, and abstention. WATER and REPOSITION map to
existing concepts; PAIN and OTHER remain unmapped. The adapter does not connect
to CareAAC or expose participant-data inputs. Crossed-panel synthetic regression
retains its errors and proves no speech or participant performance. See
`../Basic/Training/Evaluation/SYNTHETIC_INTENT_ROUTING.md` for the contract,
reproducible commands, provenance and limitations.

## 6. Program-level decision rule

Each promotion decision is one of:

- `pass`: every hard safety condition and locked evidence criterion is met;
- `fail`: at least one hard safety condition or locked criterion fails;
- `inconclusive`: evidence is insufficient or its confidence interval crosses a
  locked decision boundary; or
- `not_evaluable`: a prerequisite or data-integrity condition was not met.

An override is not a valid promotion. A redesign starts a new version and a new
evaluation block; previously inspected test data become development data.

## 7. Normative links

- `PROJECT_CHARTER.md`: intended use, non-use, roles, and research questions.
- `GENERALIZATION_BOUNDARIES.md`: claim ladder and claim-task-metric mapping.
- `EVALUATION_SAFETY_GOVERNANCE.md`: cross-project safety and governance.
- `WP1_GOVERNANCE_AND_DETERMINATION_PLAN.md`: WP1 applicability, role,
  external-request, and exit-gate plan.
- `../Basic/Trials/NRLIS-T001/TASK_REFERENCE_AUTHORSHIP_SOP.md`: operational
  task, reference, and authorship rules.
- `../Basic/Trials/NRLIS-T001/ACCESSIBLE_CONSENT_ASSENT_DISSENT_PLAN.md`:
  participant-neutral consent-access and dissent design.
- `../Basic/Training/Evaluation/T001_ANALYSIS_SPEC.md`: T001 estimands and
  frozen promotion registry.
- `../Basic/Training/Dataset/DATA_CONTRACT.md`: storage, provenance, and split
  contract.
- `../Basic/Training/Dataset/DATA_MANAGEMENT_WITHDRAWAL_PLAN.md`: operational
  data lifecycle, withdrawal, and incident requirements.
- `../Basic/Training/Dataset/RECORDING_INTAKE_AND_PROVENANCE.md`: deny-only
  recording classification and provenance framework.
- `../Basic/CareAAC/README.md`: non-recording, non-persistent Care-mode
  synthetic interface and access contract.
- `../Basic/CareAAC/VOCABULARY_ARCHITECTURE.md`: WP2.2 semantic, surface,
  navigation, interaction, and future-overlay contract.
