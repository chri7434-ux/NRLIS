# NRLIS Data Contract

**Version:** 0.5

**Status:** WP1 lifecycle plan linked; no participant data authorized

## 1. Storage boundary

This repository contains schemas, code, configuration, synthetic fixtures, and
disclosure-reviewed, release-approved reporting material. It must not contain:

- raw participant audio or video;
- raw gaze or biosignal streams;
- identifiable health records;
- exact dates linked to identity;
- contact information;
- consent signatures;
- the re-identification key; or
- an unrestricted personal voice or recognition model.

Raw participant data must reside in an approved encrypted location referenced
by opaque record IDs. Synthetic fixtures must be explicitly marked synthetic
and must not imitate a real participant's identifying voice or history.

A completed N-of-1 capability profile, participant-level session log, or rare
dialect/message record is not assumed anonymous because it uses a project ID.
The actual P001 profile and participant-level records belong in approved
private storage by default. Git retains only the empty P001 placeholder,
participant-neutral schemas, synthetic fixtures, and disclosure-reviewed,
release-approved reporting material.

`Aggregate`, `coded`, `pseudonymous`, or removal of direct names does not by
itself make material eligible for Git or public release. Use the label
`HIPAA-de-identified` only when HIPAA applies and a documented 45 CFR 164.514
Expert Determination or Safe Harbor pathway supports it. Voiceprints,
full-face/comparable images, and other unique characteristics require explicit
review under the applicable rule. The project-wide repository eligibility
label remains `disclosure-reviewed and release-approved`.

`DATA_MANAGEMENT_WITHDRAWAL_PLAN.md` operationalizes storage, access,
retention, withdrawal, deletion, model disposition, backup, and incident
requirements. Its existence is not evidence that a store or process has been
approved.

## 2. Identifier hierarchy

- Participant: `NRLIS-P###`
- Trial/protocol: `NRLIS-T###`
- Session: `S####`
- Block: `B####`
- Attempt: `A####`
- Recording/input asset: `R########`
- Input record set: `ISET-########`
- Reference: `REF-########`
- Semantic label: `SEM-####`
- Task registry item: `TASK-########`
- Model: semantic version plus immutable artifact hash
- Prediction: `PRED-########`
- Candidate set: `CSET-########`

Do not encode names, initials, birth dates, diagnosis, location, message
contents, or other identifying facts in IDs.

## 3. Data layers

### Raw layer

Immutable source signal in approved private storage. Never overwritten.

### Derived-signal layer

Segment boundaries, quality measures, acoustic or visual features, and
embeddings. Each record references the raw asset, transformation version, and
consent scope.

### Reference and label layer

Every reference record includes:

- semantic-label ID and acceptable-paraphrase-set ID;
- task family, task role, and initiation source;
- reference source;
- reference-acquisition phase relative to input and candidate reveal;
- reference lock offset and reviewer;
- confirmation-route ID and version;
- ambiguity and candidate-influence flags;
- scoring, authorship-claim, and training eligibility;
- consent and split eligibility;
- correction and supersession history; and
- protocol, task-SOP, and registry versions.

Reference meaning, prompt acceptance, post-reveal selection, and output
authorization remain separate fields.

### Prediction layer

Every prediction record includes:

- model semantic version and immutable artifact hash;
- configuration and preprocessing hashes;
- input-record-set and context-record IDs;
- complete ordered candidate list and semantic-label IDs;
- raw scores and calibrated probabilities;
- candidate-set policy and fixed `k`;
- abstention decision and reason;
- prediction-seal offset;
- output action;
- later correction or supersession; and
- protocol, task, analysis, and split versions.

### Modeling layer

Uses only records permitted by consent, protocol, source, timing, and split.
An immutable manifest records exact training, validation, calibration, and test
IDs. Source rank alone does not determine eligibility.

### Reporting layer

Contains only disclosure-reviewed, release-approved aggregates or examples
whose governing privacy, consent, protocol, and publication checks are
recorded. Aggregation alone is not release approval.

## 4. Reference-source hierarchy

Reference sources are not interchangeable:

1. `participant_independent_pre_reveal`
2. `known_prompt_participant_accepted`
3. `participant_selected_post_reveal`
4. `clinician_documented`
5. `care_partner_interpreted`
6. `researcher_inferred`
7. `model_generated`

For T001:

- levels 1 and 2 may be scoring-eligible and may enter supervised personal
  adaptation only in declared development/calibration partitions;
- level 3 may authorize a selected output only under a future
  confirmed-assistive protocol, is not an unbiased accuracy reference, and is
  training-ineligible by default;
- levels 4-7 may support error analysis but are neither scoring nor training
  truth; and
- ambiguous, candidate-influenced, or missing references are ineligible.

No label may move from evaluation to training without a new version that marks
the inspected block as development data.

## 5. Semantic representation

Store separately:

- verbatim dialect transcription, if possible;
- phonetic or pronunciation annotation, if used;
- standard written semantic label;
- English technical gloss, if needed;
- intent category;
- risk category;
- personal-vocabulary flag; and
- versioned acceptable-paraphrase set.

This prevents recognition accuracy from depending on one disputed dialect
orthography and prevents a plausible paraphrase from being accepted after
seeing the prediction.

## 6. Task and novelty contract

Every attempt records:

- task family: T0-T4;
- task role: access validation, development, calibration, prospective test, or
  exploratory;
- prompt and task-registry IDs;
- recording-instance, session, surface, semantic, intent-category, and
  participant novelty;
- partner, environment, fatigue-state, and access-route shift flags; and
- derived N0-N4 novelty class.

Do not store one undifferentiated `seen/unseen` field.

## 7. Split contract

Every experiment manifest specifies:

- participant IDs;
- session and chronological block IDs;
- task-registry and semantic-label IDs;
- development, validation, calibration, and test role;
- novelty vector and required strata;
- recording environment and partner code;
- split rationale and overlap audit;
- frozen preprocessing, model, task, analysis, and configuration versions;
- contamination checks and test-access history; and
- whether the split supports G1, G2, G3, or higher.

P001 G2 evaluation uses chronologically later session blocks, a frozen
multi-axis novelty audit, and no inspection during collection. Random splitting
of repeated utterances does not support generalization.

## 8. Attempt and session provenance

The session/attempt record stores or references:

- project, protocol, profile, task, analysis, model, configuration, and split
  versions;
- session, block, attempt, input-record-set, reference, prediction, and
  candidate-set IDs;
- input modality and quality, context, partner, environment, fatigue, and
  access route;
- reference timing, source, eligibility, ambiguity, and reviewer;
- separate semantic-scoring and registered abstention-challenge eligibility;
- relative attempt, input-end, reference-lock, and prediction-seal offsets;
- cancellation, abstention, output action, exclusion, and protocol deviation;
- serious-authorship-event and counterfactual-hazard fields; and
- correction and supersession links.

Exact candidate contents and scores belong in the prediction layer, not as an
unversioned free-text CSV field.

## 9. Missingness and immutability

- Retain every registered attempt, including cancellation, abstention, model
  failure, and unusable input.
- Use predefined missingness and exclusion codes.
- Do not reconstruct a missing reference from model or observer plausibility.
- Raw and locked reference/prediction records are append-only; corrections
  create superseding records.
- Any test-data inspection that changes a model, threshold, prompt, phrase
  bank, or analysis converts the affected block to development data.

## 10. Retention and deletion

Before participant data collection, define:

- retention duration by data layer;
- who may access each layer;
- backup and recovery method;
- participant withdrawal process;
- deletion feasibility for derived features and models;
- whether and when model retraining is required after withdrawal; and
- disposition of prediction, reference, audit, and publication records.

None of these requirements is satisfied merely by creating a schema or
synthetic fixture. WP1 records them in
`DATA_MANAGEMENT_WITHDRAWAL_PLAN.md`; every operational value and external
approval remains blocking until evidenced in the WP1 gate registry.

## 11. WP2.1 recording-intake gate

`RECORDING_INTAKE_AND_PROVENANCE.md` and
`recording_intake_v0.schema.json` define the participant-neutral receiving
contract. Version 0.1 is deny-only: it provides no authorized permission value,
keeps scoring/training eligibility false, and permits only synthetic
validation, non-Git quarantine, or metadata inventory dispositions.

The checked-in `recording_intake_v0.synthetic.json` record is the only valid
executable input. It represents zero real speakers and contains no participant
data. The validator does not accept an audio path or a participant-classified
manifest. This gate therefore proves structural closure, not provenance,
consent, approved storage, research eligibility, or fitness of any existing
recording.
