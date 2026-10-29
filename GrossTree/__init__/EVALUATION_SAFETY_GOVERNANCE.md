# Evaluation, Safety, and Governance

**Version:** 0.2
**Applies to:** All profiles, sessions, algorithms, and output modalities.

## 1. Evaluation principles

- Evaluate communication, not transcript appearance alone.
- Separate technical validation, within-person generalization, and
  cross-person generalization.
- Freeze algorithms and thresholds before prospective evaluation.
- Retain all attempts, including abstentions, cancellations, and failures.
- Report participant burden and authorship errors alongside accuracy.
- Treat evidence scope and operating mode as independent: a G-level does not
  authorize output, and assistive mode does not increase a G-level.
- Keep pre-reveal reference, post-reveal selection, and output authorization
  distinct.

## 2. Dataset splitting

### Not accepted for generalization claims

- random utterance splitting within a recording session;
- repeated versions of the same prompt across train and test;
- speaker overlap for a cross-person claim; or
- post-test threshold tuning reported as prospective performance.

### Required for P001 G2 evaluation

- chronological development, calibration, and prospective test blocks;
- held-out recording dates;
- preregistered multi-axis message novelty, including the required N2 or higher
  class;
- documented conversation-partner shift;
- documented condition shift such as fatigue or background noise; and
- pre-specified handling of missing or unusable sessions.

## 3. Mode-specific primary outcomes

### Shadow mode

1. **Unconditional Top-k Semantic Coverage:** qualified reference present in
   the sealed candidate set, with abstentions and model failures retained.
2. **Hazardous Non-Abstention Rate:** wrong, non-abstained Top-1 over all
   reference-eligible started attempts.
3. **Selective Risk:** wrong Top-1 among non-abstained attempts.
4. **Abstention Safety:** challenge sensitivity and false-abstention rate.
5. **Calibration:** Brier score and Expected Calibration Error under a frozen
   calculation rule.
6. **Inference Latency and Availability:** input end to sealed prediction,
   including failures and timeouts.

AI Successful Message Rate, actual AI Time-to-Message, transmitted-output
misattribution, actual selection effort, and fallback completion are `NA` in
shadow mode, not zero.

### Confirmed-assistive mode

A separately approved protocol may measure:

1. Successful Message Rate;
2. actual Time-to-Message;
3. transmitted-output Misattribution Rate;
4. correction, cancellation, selection, dwell, and fallback burden; and
5. participant and communication-partner workload.

## 4. Secondary and diagnostic outcomes

- conditional Top-k semantic coverage among non-abstained attempts;
- counterfactual Top-1 error across reference-eligible attempts, including
  attempts withheld by abstention;
- selectively recalculated calibration among non-abstained attempts, clearly
  distinguished from the primary all-eligible sealed-score calibration;
- Word or Character Error Rate, when a reference transcript is meaningful;
- counterfactual candidate-selection count in shadow mode, labeled simulated;
- actual keystroke or dwell savings only in confirmed-assistive mode;
- actual correction and cancellation rate only in confirmed-assistive mode;
- candidate-set size and conformal coverage;
- participant fatigue rating;
- communication-partner workload; and
- system availability and setup time.

## 5. Absolute Phase 1 safety constraints

- Unconfirmed automatic speech or message transmission: **zero permitted**.
- AI-generated emergency, consent, legal, or financial statements: **disabled**.
- Removal of "none", "repeat", "cancel", or fallback: **not permitted**.
- Unsupervised personal-model update: **disabled**.
- Training on labels without provenance: **not permitted**.
- Use as the participant's only emergency communication channel: **not
  permitted**.

## 6. Provisional promotion gates

### G0 to G1

- data schema validates;
- timestamps and label provenance are complete;
- deterministic baseline can be reproduced; and
- no output bypasses confirmation.

### G1 to G2 shadow mode

- capability profile completed;
- an independent intentional response channel documented;
- baseline communication performance recorded;
- algorithm, candidate policy, and analysis frozen; and
- prospective test block registered before inspection.

### Shadow mode to confirmed assistive mode

- no serious authorship or prohibited-output event;
- candidate coverage improves on or meaningfully complements the best
  non-AI baseline;
- confidence is sufficiently calibrated to support abstention;
- participant can reliably reject candidates and cancel;
- fatigue and stopping rules have been tested; and
- an independent reviewer approves the transition.

Numerical thresholds will be declared after baseline feasibility measurement
but before the prospective test block. They must not be selected after seeing
test performance.

Every required gate field remains `null` until legitimately determined and
locked. Any `null`, missing calculation-artifact hash, test exposure, or absent
independent approval blocks the prospective shadow segment. Gate outcomes are
`pass`, `fail`, `inconclusive`, or `not_evaluable`; an override requires a new
version and evaluation block.

A serious authorship event is an actual unconfirmed output, an observer/model
inference represented as the participant's message, prohibited high-risk
generation, or a post-reveal selection relabeled as a pre-reveal reference. A
wrong non-abstained Top-1 in shadow mode is a counterfactual hazard, not an
actual authorship event unless an output or representation breach also occurs.

## 7. High-risk communication policy

High-risk domains include:

- emergency symptoms;
- treatment decisions;
- informed consent;
- legal or financial decisions;
- allegations or statements about another person; and
- irreversible commands.

During Phase 1, the system may display a fixed, pre-authorized phrase or assist
with navigation to a human, but it may not generate or autonomously interpret a
high-risk message.

## 8. Stop and pause rules

Pause the session if:

- the participant signals stop, distress, pain, or fatigue;
- confirmation reliability falls below the profile's documented baseline;
- repeated candidates appear to influence rather than reflect intent;
- the communication partner cannot distinguish observation from inference;
- equipment positioning or gaze calibration is unstable;
- new or abruptly worsening neurological symptoms are observed; or
- privacy or recording status is unclear.

Stopping a session does not count as participant failure.

## 9. Consent and family conflict-of-interest controls

Communication impairment is not equivalent to lack of decision-making
capacity. Consent materials must use the participant's accessible communication
route. Where capacity is uncertain or absent:

- obtain institutional ethics/IRB guidance before enrollment;
- document the legal basis for representative permission;
- seek and respect assent and dissent whenever possible;
- repeat consent checks if the condition changes; and
- use an independent person rather than the family investigator alone.

The family relationship and investigator role must be disclosed in any
protocol, report, or publication.

## 10. Data governance

- Use project IDs, not names, in research files.
- Keep the re-identification key outside this workspace.
- Treat voice, video, gaze, and communication history as sensitive biometric
  and health-adjacent data.
- Store raw participant data in approved encrypted storage, not in the source
  repository.
- Record consent scope separately for recognition research, voice cloning,
  demonstrations, publication, and future model training.
- Provide deletion and model-retraining procedures before collecting data.
- Treat schemas and synthetic fixtures as infrastructure evidence only; they do
  not satisfy participant-data governance requirements.

## 11. Reporting

Early live evaluation should report:

- intended use and workflow placement;
- participant selection and capability profile;
- algorithm version and human-AI interaction;
- errors, abstentions, exclusions, and adaptations;
- session-level rather than only pooled performance;
- family investigator conflict;
- harms, burdens, and failure modes; and
- every deviation from the frozen protocol.
