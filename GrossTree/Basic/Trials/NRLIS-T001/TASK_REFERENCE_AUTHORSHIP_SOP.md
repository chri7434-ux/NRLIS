# T001 Task, Reference, and Authorship SOP

**Version:** 0.2

**Status:** WP0 scientific contract frozen; WP1 preparation open; no
participant activity authorized

**Protocol:** NRLIS-T001 v0.3

**Participant-data authorization:** None

## 1. Purpose

This SOP defines how an attempt is classified, how its reference meaning is
obtained without model influence, and which claims its evidence may support.
It replaces the ambiguous use of "true intent" with auditable reference and
authorship fields.

This document does not authorize participant interaction or data collection.

## 2. Terms that must remain separate

- **Reference meaning:** the semantic target against which a candidate set may
  be scored.
- **Prompt acceptance:** confirmation that the participant understood and
  agreed to attempt an externally assigned target.
- **Pre-reveal independent reference:** a reference obtained through a
  non-predictive route while AI candidates remain hidden.
- **Post-reveal selection:** selection or rejection after seeing candidates.
- **Output authorization:** a valid confirmation allowing a selected,
  low-risk message to be rendered under a future assistive protocol.
- **Authorship:** the bounded claim supported by the participant's initiation,
  selection, confirmation, rejection, or correction action.

Prompt acceptance is not spontaneous authorship. Post-reveal selection may
authorize the selected output but is not an unbiased reference for the model's
pre-existing accuracy.

## 3. Task taxonomy

| Task family | Definition | Permitted evidence use | Prohibited interpretation |
|---|---|---|---|
| `T0_ACCESS_CONTROL` | Randomized known-answer, deliberately incorrect-option, reject, and cancel trials used to validate an independent response route | Access reliability and session eligibility | Model accuracy or open-ended communication |
| `T1_PROMPTED_KNOWN` | A registered target that the participant understands and accepts before producing the input signal | Development, calibration, and controlled G1 evaluation when split rules permit | Spontaneous or self-initiated authorship |
| `T2_HELDOUT_PARAPHRASE` | A sequestered target whose exact surface form is absent from development data; its semantic label may be previously seen | Surface-form robustness; G2 only in a frozen later-session block | Unseen semantic intent unless separately coded |
| `T3_NATURALISTIC` | A participant-initiated attempt whose reference is independently documented while AI candidates remain sealed | P001 naturalistic G2 evaluation when the reference is eligible | Accuracy or authorship when only a family or model guess exists |
| `T4_POST_REVEAL_SELECTION` | A future assistive-mode attempt in which the participant sees and selects, rejects, or corrects a candidate | Output authorization and interface feasibility under a new protocol | Unbiased shadow accuracy or automatic training eligibility |

T4 is not conducted in T001 shadow mode. A T3 attempt without an eligible
pre-reveal independent reference is retained as `exploratory_only` and is not
included in accuracy, authorship, or training denominators.

## 4. Required task-registry fields

Before an attempt begins, register:

- task-registry version;
- task family and task role;
- prompt ID, if applicable;
- semantic-label ID and acceptable-paraphrase-set ID, if assigned;
- initiation source: `system_prompt` or `participant_initiated`;
- intended split: development, calibration, prospective test, or exploratory;
- risk category;
- allowed input and confirmation routes; and
- planned novelty vector.

The held-out registry must be sequestered from model development. Viewing or
using an item to change a model, prompt, threshold, phrase bank, or analysis
converts it to development data.

## 5. Attempt sequence

### 5.1 Session access check

1. Run the registered T0 known-answer and catch-trial procedure.
2. Record accuracy, false activation, no-response, latency, and evidence of
   yes/no or positional bias.
3. Stop or use the non-AI fallback if the locked session reliability rule is
   not met.

The reliability rule and its numerical thresholds must be approved before
participant recording. No values are inferred by this document.

### 5.2 Task assignment and input

1. Lock the task family and registry entry before input.
2. For T1 or T2, confirm prompt comprehension and acceptance before production.
3. For T3, record the participant's intentional start using the validated
   channel; do not suggest a semantic answer.
4. Capture only the modalities and context fields authorized by protocol and
   consent.

### 5.3 Reference acquisition and prediction sealing

- For T1 and T2, the accepted registry target is the reference.
- For T3, obtain the reference through an independent, non-predictive route
  after initiation and before any candidate reveal.
- A prediction may be computed in parallel, but its complete candidate set,
  scores, abstention decision, model hash, and configuration hash must be
  sealed and unavailable to anyone assisting reference acquisition.
- Record whether the reference was acquired `pre_input`,
  `post_input_pre_reveal`, `post_reveal`, or was `absent`.
- Lock the reference source, ambiguity status, reviewer, and time offset before
  scoring.

In the frozen prospective block, participants, communication partners, and
development investigators remain blind to candidates throughout collection.
Unlocking for analysis follows the locked analysis specification.

### 5.4 Eligibility assignment

Assign three independent Boolean fields:

- `scoring_eligible`: a qualified reference was locked without candidate
  influence and the attempt meets the prespecified analysis definition;
- `authorship_claim_eligible`: the recorded action supports the exact bounded
  authorship statement being made; and
- `training_eligible`: consent, protocol, split, source, and timing allow the
  record to enter a later development version.

Eligibility is never inferred from label-source rank alone.
Assign `challenge_eligible` separately for preregistered abstention challenges.
It may be true when semantic `scoring_eligible` is false, including a registered
unusable-input challenge.

## 6. Reference-source and eligibility rules

| Reference source/status | Shadow scoring | Initial personal adaptation | Authorship statement |
|---|---:|---:|---|
| `known_prompt_participant_accepted` | Yes, subject to split | Yes, in development/calibration only | Participant accepted and attempted the assigned target |
| `participant_independent_pre_reveal` | Yes | Yes, in development/calibration only | Participant independently indicated the reference |
| `participant_selected_post_reveal` | No | No by default; a future protocol must opt in and remove it from test evidence | Participant selected or authorized the displayed message |
| `clinician_documented` | No for T001 model accuracy | No | Clinical observation only |
| `care_partner_interpreted` | No | No | Care-partner interpretation only |
| `researcher_inferred` | No | No | Researcher inference only |
| `model_generated` | No | No | Model hypothesis only |
| ambiguous, absent, or influenced reference | No | No | No participant-intent claim |

Care-partner and researcher observations remain useful error-analysis fields
but must never silently supersede the participant-qualified reference.

## 7. Authorship states and events

Use one of:

- `assigned_target_accepted`;
- `participant_independent_reference`;
- `participant_selected_output`;
- `participant_rejected_all`;
- `participant_cancelled`;
- `reference_ambiguous`; or
- `no_authorship_claim`.

A **serious authorship event** is any actual:

- speech, transmission, or action without the confirmation required by the
  applicable protocol;
- representation of model, care-partner, or researcher inference as the
  participant's message;
- AI generation or autonomous interpretation of an excluded high-risk message;
  or
- relabeling of a post-reveal selection as a pre-reveal reference.

An incorrect, non-abstained shadow Top-1 prediction is a
`counterfactual_authorship_hazard`, not an actual authorship event, unless an
output or representation breach also occurred.

## 8. Novelty vector

Do not use a single `seen/unseen` field. Record each axis:

- `recording_instance`: `duplicate` or `new`;
- `session_relation`: `development` or `later_prospective`;
- `surface_relation`: `exact_seen` or `unseen_paraphrase`;
- `semantic_relation`: `seen` or `unseen`;
- `intent_category_relation`: `seen` or `unseen_ood`;
- partner, environment, fatigue-state, and access-route shift flags; and
- `participant_relation`: `same`, `new_matched_stratum`, or
  `new_cross_stratum`.

Derived reporting classes are:

- N0: repeated instance, debugging only;
- N1: new recording of a seen surface and semantic target;
- N2: unseen surface form for a seen semantic target;
- N3: unseen semantic target within a seen intent category; and
- N4: unseen intent category or other out-of-distribution condition.

Novelty alone does not establish G2. The system and analysis must also be
frozen, the session must be chronologically later, and the prospective block
must remain uninspected during collection.

## 9. Minimum attempt-log fields

Every attempt references or stores:

- protocol, profile, task, analysis, model, configuration, and registry
  versions;
- session, block, attempt, input-record-set, reference, prediction, and
  candidate-set IDs;
- reference source, acquisition phase, lock offset, ambiguity, and reviewer;
- the three eligibility fields;
- separate challenge-abstention eligibility;
- confirmation-route version and session access-check ID;
- complete novelty vector;
- input quality, environment, partner, fatigue, and permitted modalities;
- prediction-seal offset, abstention, output action, and protocol deviations;
  and
- cancellation, serious-authorship-event, counterfactual-hazard, correction,
  and supersession fields.

Candidate contents, raw scores, and calibrated probabilities belong in the
normalized prediction record. The session CSV stores only its opaque ID and
summary fields.

## 10. Stop and ineligibility rules

Stop immediately under the protocol's dissent, distress, acute-change,
privacy, fatigue, prompting, or confirmation-channel rules. A stopped attempt
is retained and is not participant failure.

Mark an attempt non-scoring rather than reconstructing a label when:

- the reference is absent, ambiguous, candidate-influenced, or inferred by
  another person;
- the registered task or reveal order was violated;
- the candidate set was visible during reference acquisition;
- the attempt influenced model or threshold development; or
- the predefined technical-exclusion rule applies.

All exclusions and their timing remain visible in the analysis record.
