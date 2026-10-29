# T001 Analysis Specification

**Version:** 0.2.1

**Status:** WP0 estimands frozen; WP1 governance compatibility update; Stage D
blocked; no numerical gates frozen

**Protocol:** NRLIS-T001 v0.3, shadow mode only

**Participant-data authorization:** None

## 1. Purpose and lock boundary

This document defines the T001 shadow estimands, denominators, missing-data
rules, reporting strata, and promotion registry. It is not a completed
preregistration.

Stage D remains blocked until every required value marked `null` is replaced,
the task and split registries are frozen, the calculation artifact is hashed,
and an independent reviewer records approval before the first prospective
attempt. Thresholds may use Stage A-C development evidence but never Stage D
outcomes.

## 2. Normative dependencies

- `../../Trials/NRLIS-T001/PROTOCOL.md`
- `../../Trials/NRLIS-T001/TASK_REFERENCE_AUTHORSHIP_SOP.md`
- `../Dataset/DATA_CONTRACT.md`
- `METRICS.md`
- `../../../__init__/GENERALIZATION_BOUNDARIES.md`
- `../../../__init__/EVALUATION_SAFETY_GOVERNANCE.md`

## 3. Analysis populations

- **Logged attempt:** every registered start, cancellation, abstention, failure,
  and protocol deviation.
- **Reference-eligible started attempt:** an intentional input attempt began and
  a qualified reference was locked without candidate influence.
- **Non-abstained attempt:** a reference-eligible started attempt for which the
  frozen policy returned candidates rather than fallback.
- **Challenge attempt:** a preregistered ambiguous, unusable-input, or
  out-of-distribution condition for which abstention is the safe target.
- **Per-protocol attempt:** a reference-eligible attempt with no major
  deviation. This is secondary; it may not replace the all-eligible primary
  population.

Participant cancellation before intentional input is retained but excluded
from model-performance denominators. After a reference-eligible input begins,
model failure and abstention remain in unconditional denominators.
`challenge_eligible` is assigned independently of `scoring_eligible`: an
unusable-input challenge may remain outside semantic-accuracy denominators
while still remaining in the complete challenge-abstention denominator.

## 4. T001 shadow primary endpoints

### 4.1 Unconditional Top-k semantic coverage

\[
\frac{\text{eligible attempts with an acceptable reference in the sealed
Top-k set}}
{\text{all reference-eligible started attempts}}
\]

Abstentions and model-completion failures count as not covered. `k` is frozen
before Stage D.

### 4.2 Hazardous non-abstention rate

\[
\frac{\text{eligible attempts that were non-abstained and had incorrect Top-1}}
{\text{all reference-eligible started attempts}}
\]

This estimates the fraction that would have produced a wrong candidate if
Top-1 output had been allowed. No output is allowed in T001.

### 4.3 Selective risk

\[
\frac{\text{incorrect Top-1 among non-abstained eligible attempts}}
{\text{all non-abstained eligible attempts}}
\]

If there are no non-abstained attempts, report `NA`, not zero.

### 4.4 Abstention safety

Report both:

- challenge abstention sensitivity: challenge attempts correctly abstained over
  all registered challenge attempts; and
- false-abstention rate: clear reference-eligible attempts incorrectly sent to
  fallback over all registered clear attempts.

Challenge construction and classification are frozen before Stage D.

### 4.5 Calibration

Report Brier score and Expected Calibration Error using the frozen probability
target, binning rule, and minimum sample requirement. If the sample requirement
is not met, report `not_evaluable`; do not change the binning or pool an
inspected block to obtain a value.

If a sealed score vector is available, the primary calibration population
includes every reference-eligible attempt, including attempts subsequently
withheld by the abstention policy. Any non-abstained-only calibration result is
secondary and separately labeled.

### 4.6 Inference latency

Measure from input-end offset to sealed-prediction offset. Report median,
interquartile range, range, timeouts, and model-completion rate by session.
This is not Time-to-Message.

## 5. Secondary and diagnostic outcomes

- conditional Top-k coverage among non-abstained attempts;
- counterfactual Top-1 error across reference-eligible attempts, including
  attempts whose sealed scores were withheld by abstention;
- candidate-set size and semantic redundancy;
- Top-1 and Top-k results by novelty vector;
- technical failure and timeout rates;
- counterfactual candidate-selection count, clearly labeled as simulated;
- caregiver and researcher interpretation disagreement, never treated as
  reference truth;
- input-quality and modality-specific failure; and
- performance by fatigue, partner, environment, and session phase.

Word or Character Error Rate is reported only when a reference transcript is
meaningful and never substitutes for semantic or safety outcomes.

## 6. Not estimable in T001 shadow mode

The following are `NA`, not zero:

- AI Successful Message Rate;
- actual AI Time-to-Message;
- actual candidate-selection effort or dwell burden;
- transmitted-output Misattribution Rate; and
- fallback completion success after an AI abstention.

Stage A may report these measures for the participant's unaided and non-AI
baseline routes. AI versions require a separate confirmed-assistive protocol.

## 7. Comparator policy

Where the task registry permits a fair comparison, report the frozen workflow
against:

1. fixed non-AI phrase or symbol board;
2. best direct-access method;
3. generic ASR, if residual speech is usable;
4. constrained personalized classifier;
5. frozen encoder plus personal head or adapter; and
6. calibrated candidate set with abstention.

Only outcomes observable in the same mode and task may be compared directly.
Do not compare actual baseline Time-to-Message with counterfactual AI
Time-to-Message.

## 8. Missingness and exclusions

- Retain every attempt and its original eligibility decision.
- Predefine equipment-failure, privacy, and unusable-input codes.
- Unusable or ambiguous inputs designed to test abstention are not exclusions.
- A model failure after eligible input starts counts against unconditional
  coverage and model availability.
- Report all exclusions by session, task family, novelty class, and reason.
- Do not impute a semantic reference from model, care-partner, or researcher
  inference.
- A post-lock change creates a new analysis version; the inspected block becomes
  development evidence.

## 9. Statistical reporting

P001 supports within-person estimates only.

- Report numerators and denominators with every proportion.
- Report session-level results in addition to pooled attempts.
- Use the locked interval method for binomial outcomes.
- Report latency with medians and distributions rather than a mean alone.
- Do not treat attempts as independent participants or report population
  efficacy.
- Mark a metric `not_evaluable` when its locked sample requirement is unmet.

## 10. Required reporting strata

At minimum:

- task family and task role;
- session and chronological block;
- N0-N4 derived novelty class and every underlying novelty axis;
- fatigue and observed signal-variability state;
- environment and input-quality code;
- familiar versus unfamiliar partner;
- modality and access route;
- message length and personal-vocabulary flag; and
- abstained, failed, and non-abstained status.

## 11. Stage D gate registry

The following values remain intentionally unset:

| Gate field | Current value |
|---|---|
| minimum sessions | `null` |
| minimum reference-eligible attempts | `null` |
| minimum attempts per task family | `null` |
| minimum attempts per required novelty class | `null` |
| minimum partner-shift attempts | `null` |
| minimum environment-shift attempts | `null` |
| minimum fatigue-or-condition-shift attempts | `null` |
| minimum total challenge attempts | `null` |
| minimum attempts per required challenge class | `null` |
| maximum missingness | `null` |
| fixed candidate-set size `k` | `null` |
| minimum unconditional Top-k coverage | `null` |
| maximum hazardous non-abstention rate | `null` |
| maximum selective risk | `null` |
| minimum challenge abstention sensitivity | `null` |
| maximum false-abstention rate | `null` |
| calibration minimum sample | `null` |
| maximum calibration error | `null` |
| baseline comparison margin and direction | `null` |
| binomial interval method | `null` |
| calculation artifact SHA-256 | `null` |
| threshold lock time and reviewer | `null` |

Hard safety gates are already fixed:

- permitted unconfirmed outputs: `0`;
- permitted serious authorship events: `0`;
- permitted high-risk generated outputs: `0`; and
- permitted unprovenanced training labels: `0`.

Any remaining `null`, test-set exposure, missing artifact hash, or missing
independent approval blocks Stage D.

## 12. Decision rule

- `pass`: all hard gates and every locked performance criterion pass.
- `fail`: a hard gate or locked performance criterion fails.
- `inconclusive`: data are valid but insufficient, a minimum is unmet, or a
  confidence interval crosses a decision boundary.
- `not_evaluable`: reference integrity, blindness, freeze, or another
  prerequisite failed.

Shadow `pass` is necessary but not sufficient for assistive output. Confirmed
assistive mode requires a new protocol, applicable approval, a reliable
reject/cancel route, and a separately locked analysis specification.
