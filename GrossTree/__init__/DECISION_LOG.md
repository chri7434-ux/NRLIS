# Decision Log

Material design decisions are append-only. A later decision may supersede an
earlier one but must not erase it.

## D001 - Workflow is the initial unit of generalization

- Date: 2026-07-29
- Status: active
- Decision: Generalize the capability-assessment, routing, confirmation,
  adaptation, and monitoring workflow; do not assume a universal intent model.
- Evidence: E001, E003, E005
- Consequence: Personal calibration is expected and reported.

## D002 - P001 is an anchor development case

- Date: 2026-07-29
- Status: active
- Decision: Use P001 for co-design, feasibility, failure analysis, and
  longitudinal evaluation.
- Evidence: project rationale
- Consequence: P001 cannot establish cross-person generalization. Prospective
  P001 evidence requires a frozen future session block.

## D003 - Maximum initial claim is G2

- Date: 2026-07-29
- Status: active
- Decision: Phase 1 may claim only within-person prospective generalization.
- Evidence: E001, E005
- Consequence: G3 and above require independent participants.

## D004 - Shadow mode precedes assistive output

- Date: 2026-07-29
- Status: active
- Decision: Predictions are evaluated without being spoken or transmitted
  before any confirmed assistive mode.
- Evidence: E004, E005
- Consequence: Counterfactual authorship errors can be measured without making
  them real communication events.

## D005 - Short, constrained messages precede open vocabulary

- Date: 2026-07-29
- Status: active
- Decision: Begin with low-risk, participant-relevant short messages.
- Evidence: E001
- Consequence: Open-vocabulary work requires a new gate and protocol version.

## D006 - Late fusion precedes joint multimodal end-to-end training

- Date: 2026-07-29
- Status: active
- Decision: Develop and validate each modality separately, then combine
  inspectable scores.
- Evidence: engineering rationale; hypothesis
- Consequence: Missing modalities and modality-specific failure remain visible.

## D007 - Brain and biosignal interfaces remain Extension-track

- Date: 2026-07-29
- Status: active
- Decision: sEMG, EEG, fMRI, and implanted BCI are excluded from the Phase 1
  core.
- Evidence: E002
- Consequence: Phase 1 uses consumer-accessible, non-invasive communication
  routes only.

## D008 - Confirmed-only personal learning

- Date: 2026-07-29
- Status: active
- Decision: Only participant-confirmed or accepted known-prompt labels may
  train the personal adapter.
- Evidence: E003, E005
- Consequence: Caregiver interpretation remains a separate analysis field.

## D009 - Evidence scope and operating mode are orthogonal

- Date: 2026-07-29
- Status: active
- Decision: Use the G0-G5 ladder for evidence scope and use shadow versus
  confirmed-assistive mode for output permission; neither axis determines the
  other.
- Evidence: evaluation-design and authorship-safety rationale
- Consequence: A P001 assistive study remains at most G2, and a G-level never
  authorizes output without a separate applicable protocol.

## D010 - Reference, selection, and output authorization remain distinct

- Date: 2026-07-29
- Status: active
- Decision: Treat a pre-reveal independent reference, a post-reveal candidate
  selection, and authorization to render a message as different records.
- Evidence: measurement-validity and confirmation-bias rationale
- Consequence: Post-reveal selection is not an unbiased scoring reference and
  is training-ineligible by default.

## D011 - Prompted targets do not establish spontaneous authorship

- Date: 2026-07-29
- Status: active
- Decision: Use an understood and accepted known prompt for controlled
  development or evaluation without describing it as participant-initiated
  communication.
- Evidence: task-design and authorship rationale
- Consequence: Prompted-task reports state that the participant accepted and
  attempted an assigned target.

## D012 - Message novelty is multi-axis

- Date: 2026-07-29
- Status: active
- Decision: Replace a bare seen/unseen label with recording, session, surface,
  semantic, intent-category, context-shift, and participant novelty fields.
- Evidence: generalization and leakage-control rationale
- Consequence: Every G2 claim identifies the exact novelty class and requires a
  frozen, chronologically later, uninspected block.

## D013 - Numerical promotion gates remain blocked while null

- Date: 2026-07-29
- Status: active
- Decision: Do not invent pre-data performance thresholds; derive them only
  from permitted development evidence and lock them before Stage D.
- Evidence: prospective-evaluation and anti-overfitting rationale
- Consequence: Any required `null`, missing artifact hash, or missing
  independent approval prevents the prospective shadow block from opening.

## D014 - WP0 v0.2 scientific contract is frozen

- Date: 2026-07-29
- Status: active
- Decision: Freeze the Phase 0B objective, task/reference/authorship ordering,
  metric definitions, data contract, and promotion framework as WP0 v0.2.
  Stage D numerical thresholds remain intentionally deferred and blocking.
- Evidence: integrated contract audit and independent bounded methodology review
- Consequence: Later changes are versioned; WP1 may proceed externally and
  synthetic-only WP2 may proceed, but participant enrollment, recording,
  training, Stage D, and output remain disabled.

## D015 - Synthetic G0 component verification passed

- Date: 2026-07-29
- Status: active
- Decision: Record G0 component verification as passed on the versioned
  synthetic-only fixture after schema validation, deterministic execution,
  frozen-metric comparison, negative tests, and zero prohibited output bypass.
- Evidence: synthetic fixture/config/expected-metric hashes, 15 acceptance
  tests, collaboration schema tests, and repository CI checks
- Consequence: The earned level is
  `G0_component_verified_synthetic_only`. It supports no participant,
  clinical, authorship, assistive-output, or cross-person claim. Static-fixture
  inference latency remains not evaluable.

## D016 - Abstention challenge and semantic scoring populations are separate

- Date: 2026-07-29
- Status: active
- Decision: Use `challenge_eligible` independently from `scoring_eligible`, and
  report conditional Top-k coverage separately from overall non-abstained
  coverage.
- Evidence: independent methodology review identified denominator ambiguity
- Consequence: Registered unusable-input challenges remain in challenge
  abstention sensitivity without entering semantic-accuracy ground truth.

## D017 - WP1 opens as governance preparation only

- Date: 2026-07-29
- Status: active
- Decision: Open WP1 for participant-neutral governance drafting, role
  recruitment, and external determination requests while keeping every
  participant-facing activity and permission scope closed.
- Evidence: E006-E012; WP1 repository gap and safety red-team audits
- Consequence: WP1 is `open_blocked_external_determinations`, not complete or
  approved. Contact for research, enrollment, intake, profiling, recording,
  historical-media ingest, participant-specific inference, training,
  candidate reveal, rendering, transmission, demonstration, publication, and
  secondary use remain disabled.

## D018 - Activity authorization is scoped and never inherited

- Date: 2026-07-29
- Status: active
- Decision: Separate project/institution, enrollment, session/activity,
  modality/data-layer, and record/output authority. WP1 completion does not
  itself grant any participant activity.
- Evidence: E007-E012; authorship and family-conflict safety rationale
- Consequence: Every activity requires exact purpose, modality, data layer,
  protocol version, evidence record, authority, date, and absence of an active
  hold. Missing, unresolved, expired, revoked, or mismatched evidence returns
  `not_authorized`.

## D019 - Pseudonymous N-of-1 profiles remain private by default

- Date: 2026-07-29
- Status: active
- Decision: Treat the completed P001 profile and participant-level records as
  sensitive and potentially re-identifiable even when direct identifiers are
  removed.
- Evidence: E009; single-participant disclosure-risk rationale
- Consequence: Git retains only the empty P001 placeholder,
  participant-neutral schemas, synthetic fixtures, and disclosure-reviewed
  aggregates. Actual profiles, media, logs, and personal models require an
  approved private store.

## D020 - WP1 evidence is ledger-bound, current, and scope-specific

- Date: 2026-07-29
- Status: active
- Decision: A terminal WP1 gate requires a current ledger record bound to an
  identified issuing authority, artifact and external-record hashes, the
  frozen protocol/scope, covered gate IDs, an internal recorder, review date,
  expiry, and revocation state. An `EXT-*` string alone is not evidence.
- Evidence: independent WP1 red-team review; E007-E010
- Consequence: Expired, revoked, missing, wrong-domain, wrong-scope, or
  unverified-authority evidence cannot close a gate. Structural validation
  does not authenticate issuance; the ethics contact and independent exit
  reviewer must reconcile the metadata against the external system.

## D021 - Role separation uses stable holder identity and finite validity

- Date: 2026-07-29
- Status: active
- Decision: Bind each verified role and training record to a stable opaque
  holder ID, enforce required role separation on that ID, and require finite
  future role, training, and review validity.
- Evidence: independent WP1 red-team review; conflict-of-interest and
  lifecycle-control rationale
- Consequence: Different appointment IDs cannot disguise one person's
  prohibited dual role. Missing or stale appointment, training, independence,
  or combination evidence blocks WP1 exit.

## D022 - Consent precedes enrollment and Stage A

- Date: 2026-07-29
- Status: active
- Decision: Freeze the sequence as authorized contact, approved minimal
  pre-consent access check if permitted, legally effective consent or valid LAR
  permission plus participant agreement, enrollment, Stage A1 session-control
  validation, and only then separately authorized Stage A2 modalities.
- Evidence: E007, E008, E012; independent WP1 protocol review
- Consequence: Stage A1 cannot establish consent or occur before enrollment,
  and enrollment never authorizes recording.

## D023 - Release eligibility is not inferred from aggregation or coding

- Date: 2026-07-29
- Status: active
- Decision: Use `disclosure-reviewed and release-approved` as the repository
  and reporting eligibility label. Use `HIPAA-de-identified` only when HIPAA
  applies and a documented 45 CFR 164.514 pathway supports the label.
- Evidence: E009; independent official-source review
- Consequence: Aggregation, coding, pseudonymization, or name removal alone
  does not make material eligible for Git, demonstration, or publication.

## D024 - Determination scope is anchored to normative repository content

- Date: 2026-07-29
- Status: active
- Decision: Compute the WP1 determination-scope hash from a canonical manifest
  containing the protocol identity and version, registry-schema version,
  frozen activity keys, and SHA-256 hashes of the six governing scope
  documents.
- Evidence: independent WP1 repository-gap review
- Consequence: A self-consistent arbitrary hash or invented protocol version
  cannot preserve a terminal gate. Editing a governing document requires a
  refreshed scope hash and any externally required re-review.

## D025 - Gate closure is type-, authority-, and outcome-specific

- Date: 2026-07-29
- Status: active
- Decision: Freeze eligible record types, authority types, recording roles,
  and decision outcomes for each of the 25 WP1 gates. A gate status of
  `not_applicable` is never terminal; only `WP1-G01` through `WP1-G05` may use
  a scoped external-evidence outcome of `not_applicable`.
- Evidence: independent WP1 repository-gap review
- Consequence: Generic approvals, training-provider records, or an
  applicability label cannot close a mandatory consent, role, data, incident,
  activity-scope, or independent-review control.

## D026 - Role competency and decision authorship bind to stable holders

- Date: 2026-07-29
- Status: active
- Decision: Freeze a competency set for each required role, require
  appointment, training, independence, and combination evidence to cover the
  exact role or role set, and record the stable holder who entered each gate
  decision.
- Evidence: independent WP1 repository-gap review; family-conflict and
  reviewer-turnover rationale
- Consequence: Unrelated training cannot verify a role, and a replacement
  reviewer cannot inherit a previous holder's `WP1-G25` exit decision.

## D027 - WP1 release validation composes schema and semantic layers

- Date: 2026-07-29
- Status: active
- Decision: Treat JSON Schema validation and the Python semantic audit as an
  inseparable WP1 machine gate. Freeze `independence_required` per role in the
  semantic layer alongside separation and competency policies.
- Evidence: independent official-source wording check; independent Grok
  governance consistency audit
- Consequence: The WP1 CLI fails closed if schema validation is unavailable or
  required provenance fields are absent. A mutable independence flag cannot
  remove required evidence, and neither machine layer is represented as proof
  of authentic external issuance.

## D028 - Scope manifest covers the complete T001 normative set

- Date: 2026-07-29
- Status: active; scope-coverage correction to D024
- Decision: Use scope-manifest v1.1 and hash all eight documents declared by
  T001 as normative, the T001 protocol itself, and the project charter.
- Evidence: independent WP1 repository-gap audit
- Consequence: Authorship, analysis, metric, safety, consent, data, protocol,
  or governance changes invalidate the current scope hash. D024's earlier
  six-document count is superseded.

## D029 - Baseline cannot become a second activity registry

- Date: 2026-07-29
- Status: active
- Decision: Reject every baseline field whose leaf name is one of the 21
  authoritative activity keys, reject unknown `*_enabled` fields, and freeze
  every recognized executable or safety flag to its deny-only value.
- Evidence: independent WP1 repository-gap audit
- Consequence: Adding an activity-like field to `baseline_v0.yaml`, even with
  a false value, fails validation instead of creating a parallel authorization
  vocabulary that could later drift open.

## D030 - Baseline parsing is recursive and type-strict

- Date: 2026-07-29
- Status: active; parser-strengthening correction to D029
- Decision: Parse `baseline_v0.yaml` with a pinned YAML safe loader that
  rejects duplicate and merge keys, recursively inspects root, nested mapping,
  and list leaves, and preserves scalar types for exact interlock comparison.
- Evidence: independent WP1 repository-gap audit
- Consequence: Root or deeply nested activity and `*_enabled` fields cannot
  evade inspection, and the string `"false"` cannot satisfy a Boolean `false`
  gate. Missing parser dependencies fail the combined CLI closed.

## D031 - Baseline path encoding is unambiguous

- Date: 2026-07-29
- Status: active; path-encoding strengthening to D030
- Decision: Restrict every baseline mapping key to lowercase `snake_case`;
  reserve dots and list-index notation exclusively for the validator's
  internal rendered paths.
- Evidence: independent WP1 repository-gap audit
- Consequence: A literal root key such as `"protocol.output_enabled"` cannot
  masquerade as the real nested `protocol: {output_enabled: ...}` interlock.

## D032 - WP1-Lite is a participant-free operating profile

- Date: 2026-09-04
- Status: active; right-sizes the timing of D021-D031 without weakening them
- Decision: Treat WP1-Lite as the current participant-free engineering and
  participant-neutral preparation profile. Full WP1 remains the Human-ready
  checkpoint for prospective participant research; WP1-Lite is not a registry
  state, determination, exemption, enrollment, or activity authorization.
- Evidence: repository stage audit; Cornell Precollege status clarification;
  current baseline and WP1 registry
- Consequence: Synthetic or appropriately licensed public-data software and
  model work may proceed now. The seven formal roles and external evidence are
  activated at a determination request or participant-facing transition, while
  every participant activity remains fail-closed.

## D033 - Immediate family-care AAC and research data are separate lanes

- Date: 2026-09-04
- Status: active
- Decision: Allow ordinary non-research AAC support to serve P001's immediate
  communication needs without waiting for the research program. Care
  observations, family knowledge, and non-research co-design records are not
  retrospectively converted into NRLIS profiles, training data, test evidence,
  metrics, demonstrations, or publications.
- Evidence: project intended use; prospective data-integrity requirements;
  participant-autonomy and family-conflict analysis
- Consequence: Declining research cannot remove ordinary communication support.
  Any desired research use begins prospectively after the Human-ready and
  activity-specific gates rather than by relabeling earlier care activity.

## D034 - First neural milestone verifies plumbing, not speech performance

- Date: 2026-09-04
- Status: active
- Decision: Establish the first participant-free neural executable as a
  deterministic two-layer MLP over generated synthetic embedding vectors, with
  isolated development, calibration, and held-out test splits, temperature
  scaling, probability-and-margin abstention, frozen metrics, and no output.
- Evidence: participant-free neural configuration, implementation, expected
  metrics, and acceptance tests
- Consequence: Passing the check supports only the claim that neural training,
  calibration, abstention, evaluation, and disabled-output plumbing work. The
  synthetic vectors are not speech, and no ASR, participant, clinical, or
  cross-person claim is earned.

## D035 - Recording intake v0.1 is a deny-only receiving contract

- Date: 2026-09-04
- Status: active
- Decision: Define recording context, speaker multiplicity, source provenance,
  separate permission scopes, reference status, chronological split state,
  action authorization, and disposition in a strict participant-neutral schema.
  The v0.1 executable validates only a zero-speaker synthetic fixture and
  contains no authorized permission state or real-recording input path.
- Evidence: WP2.1 schema, synthetic fixture, semantic validator, and negative
  acceptance tests; existing data and withdrawal contracts
- Consequence: Possession, quarantine, an opaque ID, family relationship, or a
  completed schema does not make a recording eligible. Audio, original names
  or paths, content, transcripts, exact time/location, identifying facts, and
  participant-level hashes remain outside Git and the v0.1 executable.

## D036 - Care-mode AAC remains non-recording and non-research

- Date: 2026-09-04
- Status: active
- Decision: Implement the first Care-mode AAC interface as a local static app
  using only generic synthetic phrases. Require separate candidate selection
  and user confirmation; keep none, repeat, cancel, and non-AI fallback
  controls available; support touch, keyboard, auto-scan, and a bounded future
  gaze/switch event adapter without implementing gaze tracking.
- Evidence: Care-mode v0.1 source, static privacy/safety tests, desktop and
  narrow-screen browser inspection, keyboard and scan interaction checks, and
  empty browser storage/network diagnostics
- Consequence: The app may support ordinary family communication but cannot be
  used as an emergency or important-decision channel. It captures, stores,
  transmits, synthesizes, and scores nothing; care interactions cannot become
  research or training data, and the app does not open any WP1 authorization.

## D037 - Stable semantic concepts precede dialect or personal vocabulary

- Date: 2026-09-05
- Status: active
- Decision: Make a versioned `concept_id` the only future model-facing target
  for Care-mode candidate proposals. Keep semantic identity separate from
  canonical/compact surface forms and from context/panel navigation. Retain the
  current fixture as fixed generic Chinese with no dialect or personal overlay.
- Evidence: WP2.2 vocabulary architecture, strict schema, 40-concept synthetic
  fixture, semantic validator, and negative acceptance tests
- Consequence: A wording change cannot silently redefine an intent, and a
  future signal model cannot inject free text. Dialect forms, names, household
  terms, frequency adaptation, and voice style require a separately versioned,
  private, permission-scoped overlay after the applicable gates.

## D038 - Confirmation authority belongs to one deterministic interaction core

- Date: 2026-09-05
- Status: active
- Decision: Route pointer, keyboard, auto-scan, and future bounded access
  adapters through the same DOM-independent state machine. Only its explicit
  confirmation transition may create a visual user message; hidden concepts,
  navigation, rejection, repeat, none, cancel, and fallback cannot bypass it.
- Evidence: WP2.2 interaction core, seven declarative synthetic scenarios, Node
  transition tests, static privacy tests, and desktop/mobile browser QA
- Consequence: Later ASR, gaze, switch, or ranking modules must propose an
  allowed concept or abstain and cannot obtain a separate output path. The core
  retains no event history, timing, confidence, participant record, or care-to-
  research data route.

## D039 - Synthetic model mapping cannot approximate unsupported meaning

- Date: 2026-09-05
- Status: active implementation; acceptance verification pending
- Decision: Keep WATER/REPOSITION as the only two exact mappings from the
  existing four-class synthetic neural fixture. PAIN and OTHER remain unmapped;
  filtering out unsupported or outside-panel classes cannot promote a weaker
  alternative or renormalize its probability. Fit temperature only on calibration
  data and retain the existing frozen confidence/margin thresholds.
- Evidence: WP2.3 configuration/schema, independent training/calibration inputs,
  sealed routing implementation, and regression preserving one candidate error.
- Consequence: This is a synthetic engineering bridge, disconnected from CareAAC.
  No forty-concept, speech, patient, or output claim is earned. A new class
  vocabulary needs its own versioned model/data contract and evaluation.

### D039 verification update

- Observed: 2026-09-05 20:46:45 CST (+0800)
- Status: Accepted after 17/17 adapter tests, unchanged CareAAC boundary checks,
  synthetic/WP1 verification, and repository audits. The initial verification-
  pending status above is superseded; the semantic and operating limits remain.
