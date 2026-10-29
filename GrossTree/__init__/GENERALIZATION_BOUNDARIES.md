# Generalization Boundaries

**Version:** 0.2
**Purpose:** Prevent prototype performance from being overstated and define what
must be demonstrated before scope expands.

## 1. The unit of generalization

The initial unit of generalization is the **workflow contract**:

1. capability assessment;
2. modality routing;
3. candidate inference;
4. uncertainty calibration;
5. user confirmation;
6. safe output;
7. confirmed-only adaptation; and
8. longitudinal monitoring.

The project does not initially assume one universal speech, language, or intent
model.

## 2. Evidence scope and operating mode are independent

The G0-G5 ladder describes evidence scope. Operating mode describes whether a
prediction remains hidden or may be selected and output:

- `shadow`: predictions are sealed for evaluation and are not shown, spoken,
  transmitted, or acted upon; and
- `confirmed_assistive`: a low-risk candidate may be output only after a valid
  participant-authorship action under a separately approved protocol.

Moving to assistive mode does not increase the G-level. Achieving a G-level
does not authorize output. A P001 assistive study remains at most G2.

## 3. Boundary matrix

| Dimension | Phase 1 in scope | Outside the current claim boundary |
|---|---|---|
| Participant | One adult anchor case | Children or population-level claims |
| Etiology | Observed communication impairment; diagnosis recorded only if clinically established | AI diagnosis or etiological inference |
| Language | Participant's documented language/dialect profile | Cross-dialect transfer without external testing |
| Expression | Residual speech and at least one verifiable confirmation channel | Attribution of unconstrained output without verification |
| Modalities | Audio, touch, gaze, head movement, or switch as available | sEMG, EEG, and implanted BCI in the core Phase 1 protocol |
| Message type | Short, user-relevant, low-risk messages | Emergency, medical consent, legal, financial, or irreversible commands |
| Environment | Documented home research setting | Hospital, public, telephone, or noisy settings without testing |
| Learning | Personal adapter trained on confirmed labels | Unsupervised online learning or silent correction |
| Outcome | Feasibility, coverage, latency, burden, and safety | Treatment efficacy, cognitive restoration, or clinical benefit |

## 4. Generalization claim ladder

### G0 - Component verification

The software runs, inputs are recorded as designed, and labels retain
provenance. No participant-performance claim is allowed.

### G1 - Within-session technical validity

The system can reproduce performance on held-out trials from a single
controlled session. This is debugging evidence, not real-world generalization.

### G2 - Within-person prospective generalization

The frozen system is evaluated on later dates and includes:

- new recording sessions;
- preregistered N2 or higher message novelty;
- different conversation partners;
- documented fatigue or speech-variability states; and
- at least one environment shift.

This is the maximum claim initially available from P001.

### G3 - Cross-person, matched-stratum generalization

The frozen workflow is evaluated on independent participants with similar
capability profiles, with personal calibration reported separately.

### G4 - Cross-stratum generalization

The workflow is evaluated across severity, impairment type, dialect, literacy,
motor-access method, and stable versus progressive conditions.

### G5 - Live clinical or product generalization

The system is evaluated in intended-use settings with independent oversight,
human-factors analysis, lifecycle monitoring, and applicable regulatory review.

## 5. Novelty contract

The word "unseen" is not a sufficient split description. Each attempt records:

- recording-instance novelty;
- chronological session relation;
- exact surface-form relation;
- semantic-label relation;
- intent-category relation;
- partner, environment, fatigue-state, and access-route shifts; and
- same versus independent participant.

The task SOP derives N0-N4 classes:

- N0 repeated instance;
- N1 new recording, seen surface and semantic target;
- N2 unseen surface, seen semantic target;
- N3 unseen semantic target, seen intent category; and
- N4 unseen intent category or other out-of-distribution condition.

Novelty is necessary but not sufficient for G2. The model, policy, task
registry, and analysis must be frozen before a chronologically later,
uninspected block.

## 6. Claim-task-metric map

| Allowed claim | Required task/evidence | Required metric family | Maximum supported level |
|---|---|---|---|
| Components, provenance, and output interlocks operate as specified | Synthetic fixtures and deterministic baseline | Schema validation, reproducibility, provenance completeness, zero prohibited output paths | G0 |
| A model recognizes controlled targets within one session | T1 prompted-known with a valid split | Top-k coverage, selective risk, calibration | G1 |
| P001 performance persists on later-session paraphrases | Frozen T2 held-out-paraphrase block | Novelty-stratified coverage, hazard, abstention, calibration | G2 |
| Candidate meanings match eligible P001 naturalistic references | Frozen T3 with pre-reveal independent reference | Coverage, hazardous non-abstention, selective risk, abstention, inference latency | G2 |
| Confirmed output is feasible for P001 | T3/T4 under a new confirmed-assistive protocol | Successful Message Rate, actual Time-to-Message, transmitted misattribution, effort, fallback success | G2 |
| The workflow transfers to matched independent participants | Frozen interfaces plus participant-specific calibration reported separately | Per-person and pooled workflow metrics | G3 |
| Capability routing generalizes across strata or improves on diagnosis-only routing | Independent participants across severity, language, motor-access, and condition strata | Routing success, burden, safety, and failure by stratum | G4 |

No task supports a claim of unexpressed-thought access. T1/T2 prompted targets do
not support spontaneous-authorship claims. T4 post-reveal selection supports
only the bounded statement that the participant selected, rejected, or
authorized a displayed message.

## 7. Evidence that does not establish generalization

The following must not be used alone to support a G2 or higher claim:

- random splitting of repeated utterances from the same recording session;
- training and testing on the same phrase inventory;
- family interpretation without independent confirmation;
- retrospective selection of only successful interactions;
- accuracy after tuning on the evaluation period;
- language-model plausibility without user confirmation;
- synthetic dysarthric audio as a substitute for patient evaluation; or
- Word Error Rate without semantic success, latency, and safety outcomes.

## 8. Participant capability boundary

Open-ended AI-assisted communication requires at least one reproducible
intentional signal that is logically independent of the AI candidate:

- direct touch;
- eye-gaze selection;
- switch activation;
- head movement;
- a reliable yes/no response; or
- another validated intentional control.

If no such channel exists, the system may conduct carefully reviewed
known-answer or stimulus-locked research, but generated language must not be
treated as the participant's communication.

## 9. Language and aphasia boundary

The system must separate:

- speech-motor decoding: what acoustic or articulatory pattern was attempted;
- language support: which words or concepts the participant can formulate;
- context modeling: which messages are plausible in the present situation; and
- authorship: which candidate the participant intentionally accepts.

For suspected or established aphasia, the language model's influence must be
reduced and visual, semantic, gesture, or partner-supported alternatives
increased. A fluent AI sentence is not evidence that the participant formulated
that sentence.

## 10. Family anchor-case boundary

P001 may be a development and longitudinal feasibility participant. Once P001
data or feedback influence the workflow, P001 cannot serve as independent
evidence of cross-person generalization.

Future P001 sessions can remain prospective only if:

- model and thresholds are frozen before the session block;
- task, novelty, reference, and analysis specifications are frozen;
- the block is not inspected during collection;
- all attempts are retained;
- exclusions are pre-specified; and
- any later redesign starts a new evaluation block.

## 11. Expansion gates

Scope may expand only when the project records:

1. the new intended-use population or setting;
2. the new failure modes introduced;
3. the independent evidence required;
4. an updated risk control;
5. a revised consent and data-governance path; and
6. a versioned go/no-go decision.
