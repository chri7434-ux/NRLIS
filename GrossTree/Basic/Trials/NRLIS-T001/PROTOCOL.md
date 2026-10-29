# NRLIS-T001 N-of-1 Shadow Protocol

**Protocol version:** 0.3

**Participant:** NRLIS-P001

**Status:** WP1 governance preparation open; closed to enrollment and every
participant-facing activity

**Study type:** Prospective single-participant feasibility workflow

**Planned first AI mode:** Shadow inference only; not currently authorized

**Not represented as:** Clinical efficacy trial

## 1. Purpose

Evaluate whether the frozen NRLIS workflow can generate useful, calibrated
candidate meanings for P001 on future sessions without speaking, transmitting,
or acting on unconfirmed predictions.

T001 estimates shadow-mode candidate performance and safety. It does not
estimate actual AI-assisted message completion, actual AI Time-to-Message, or
clinical benefit.

## 2. Normative specifications

The following are part of this protocol:

- `TASK_REFERENCE_AUTHORSHIP_SOP.md`;
- `../../Training/Evaluation/T001_ANALYSIS_SPEC.md`;
- `../../Training/Evaluation/METRICS.md`;
- `../../Training/Dataset/DATA_CONTRACT.md`;
- `../../Training/Dataset/DATA_MANAGEMENT_WITHDRAWAL_PLAN.md`;
- `ACCESSIBLE_CONSENT_ASSENT_DISSENT_PLAN.md`;
- `../../../__init__/WP1_GOVERNANCE_AND_DETERMINATION_PLAN.md`; and
- `../../../__init__/EVALUATION_SAFETY_GOVERNANCE.md`.

If a normative version changes after a prospective block is inspected, the
block becomes development evidence and a new prospective block is required.

## 3. Authorization ladder and preconditions

No participant-facing research contact, screening, intake, profiling, task, or
data retention begins until:

- all applicable institutions or authorities provide the required scoped
  determinations, or a documented reliance/authorization agreement identifies
  the reviewing IRB and all remaining local responsibilities;
- the accountable investigator, ethics contact, independent consent-access
  reviewer, SLP/clinical collaborator, data steward, technical lead, and
  independent event reviewer are verified as required;
- the family-investigator conflict plan is approved;
- the accessible consent or valid representative-permission process is
  approved;
- the activity, modality, purpose, and data layers are explicitly named in an
  approved protocol version; and
- any retained information has an approved storage, access, retention,
  withdrawal, deletion, and incident pathway.

Participant-facing intake is a research interaction even when no audio, video,
or gaze stream is recorded. Family knowledge gathered before authorization
cannot be silently entered as NRLIS research data.

The mandatory sequence is:

1. separately authorized research contact;
2. an approved, minimal pre-consent access check, if the deciding body permits
   one, with its retention boundary fixed in advance;
3. legally effective participant consent or valid LAR permission, together
   with the participant's own agreement and absence of dissent;
4. enrollment recorded only after step 3;
5. Stage A1 session confirmation, cancel, and non-AI fallback validation; and
6. Stage A2 only after each recorded/device modality and private-storage path
   is separately authorized.

Enrollment is not permission to record. Raw audio, video, gaze, screen capture,
or historical-media ingest requires an additional modality-specific permission
and storage gate. Participant-data training, shadow inference, candidate
reveal, and output each require still later protocol gates.

The current WP1 registry authorizes none of these activities.

## 4. Stage A - Capability and baseline sessions (currently blocked)

If WP1 exits and an approved protocol opens Stage A, it proceeds in two
separately authorized steps:

- **Stage A1 - access and non-AI capability assessment:** use only approved
  minimal structured observations and no raw media by default; re-confirm the
  already approved ongoing participant-agreement route and validate the
  session's stop/cancel, authorship-confirmation, and non-AI fallback controls.
  Stage A1 does not establish consent and cannot occur before enrollment.
- **Stage A2 - recorded or device-measured baseline:** begin only after the
  relevant audio, video, gaze, screen, or device modality and its private
  storage are separately authorized.

Tasks:

- verify preferred language, dialect, text, picture, and audio formats;
- compare direct touch, gaze, switch, gesture, and vocal response where
  applicable;
- establish reliable yes/no, cancel, and "none of these";
- run the registered `T0_ACCESS_CONTROL` known-answer and catch-trial procedure;
- measure current communication success and time-to-message;
- identify fatigue window and positioning requirements; and
- define an initial low-risk message inventory.

No AI-performance claim is made from Stage A.
No Stage A record belongs in Git; the repository retains only the empty profile
placeholder, schemas, and disclosure-reviewed, release-approved reporting
material.

## 5. Stage B - Prompted calibration data

Use registered `T1_PROMPTED_KNOWN` short, participant-relevant messages whose
target is understood and accepted before input. These are prompted targets, not
evidence of spontaneous authorship.

For each attempt record:

- prompt ID and semantic label;
- whether the participant understood and accepted the prompt;
- audio or other input quality;
- observed production;
- participant confirmation route;
- caregiver interpretation, stored separately;
- researcher observation, stored separately;
- fatigue and environmental state; and
- unusable-attempt reason.

Do not force completion when a prompt cannot be understood or produced.
Only labels meeting the task SOP's source, timing, consent, and split rules may
enter supervised personal adaptation.

## 6. Stage C - Model development

Compare:

1. fixed non-AI phrase board;
2. generic speech model, if speech is usable;
3. constrained personalized classifier;
4. frozen encoder plus personal adapter;
5. dialect/personal-vocabulary reranking; and
6. calibrated candidate set with abstention.

Development sessions cannot be reused as prospective test evidence.

## 7. Stage D - Frozen prospective shadow block

Before the block:

- freeze model, weights, candidate size, thresholds, and fallback policy;
- freeze the task/reference SOP and analysis specification versions;
- register sequestered T2 held-out-paraphrase items and the planned novelty
  vector for every block;
- predeclare whether eligible T3 naturalistic attempts are included;
- define session count, per-task, per-novelty, partner-shift,
  environment-shift, fatigue-or-condition-shift, and challenge-class minimums,
  plus exclusion rules;
- fill every required numerical gate and calculation field currently `null`;
- appoint an independent reviewer; and
- lock and hash the analysis script or calculation specification.

Any remaining `null`, missing artifact hash, test-item exposure, or missing
independent approval blocks Stage D.

During the block:

- AI predictions remain hidden from the participant, communication partner,
  reference-acquisition helper, and development investigators;
- prompted targets use an accepted, sequestered registry reference;
- naturalistic attempts are scoring-eligible only when an independent
  pre-reveal reference is locked while candidates remain sealed;
- no prediction is spoken or sent;
- all attempts and abstentions are retained;
- protocol deviations are timestamped; and
- investigators do not tune the model.

An incorrect, non-abstained Top-1 is recorded as a counterfactual authorship
hazard. It is not represented as an actual participant message.

## 8. Stage E - Review and go/no-go

Review:

- unconditional Top-k semantic coverage;
- hazardous non-abstention rate and selective risk;
- calibration, challenge abstention sensitivity, and false abstention;
- inference latency and model-completion rate;
- failure by fatigue, noise, novelty vector, modality, and partner;
- caregiver versus participant-label disagreement; and
- serious authorship events, protocol breaches, and counterfactual hazards.

AI Successful Message Rate, actual AI Time-to-Message, actual selection burden,
transmitted-output misattribution, and fallback completion are `NA` in shadow
mode, not zero.

The decision is `pass`, `fail`, `inconclusive`, or `not_evaluable` under the
locked analysis specification. A shadow pass is necessary but not sufficient
for assistive output. Confirmed assistive mode requires a new protocol version,
applicable approval, and a new locked analysis specification.

## 9. Safety exclusions

The protocol does not test AI-generated:

- emergency statements;
- treatment choices;
- consent;
- legal or financial instructions;
- accusations; or
- irreversible commands.

## 10. Stop rules

Stop immediately for:

- participant dissent or cancel signal;
- distress, pain, or excessive fatigue;
- sudden new or worsening neurological symptoms;
- loss of the independent confirmation channel;
- recording or privacy uncertainty;
- repeated prompting that appears to shape the answer; or
- investigator disagreement about whether intent was actually confirmed.

Stopping or cancelling is retained and is not participant failure. Reference
ambiguity must not be resolved by model, caregiver, or researcher plausibility.

## 11. Analysis boundary

P001 can establish at most G2 within-person prospective generalization. P001
cannot establish cross-person, cross-dialect, or clinical effectiveness.

Evidence scope and operating mode are independent: even a future P001
confirmed-assistive study remains at most G2. This protocol remains shadow only
and authorizes no participant-facing activity, enrollment, intake, recording,
inference, candidate reveal, training, or output in its current status.
