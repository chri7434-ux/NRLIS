# Evaluation Metric Definitions

**Version:** 0.2

**Status:** Pre-data metric contract

**Applies to:** NRLIS technical, shadow, and future confirmed-assistive studies

## 1. Mode applicability

| Metric | Synthetic/G0 | Shadow | Confirmed assistive |
|---|---:|---:|---:|
| Schema/provenance completeness | Yes | Yes | Yes |
| Deterministic reproducibility | Yes | As applicable | As applicable |
| Unconditional Top-k semantic coverage | Synthetic fixture only | Primary | Secondary |
| Conditional Top-k semantic coverage | Synthetic diagnostic | Secondary | Secondary |
| Counterfactual Top-1 error | Synthetic diagnostic | Secondary | Not an actual-output metric |
| Hazardous non-abstention rate | Synthetic fixture only | Primary | Safety |
| Selective risk | Synthetic fixture only | Primary | Safety |
| Abstention safety and calibration | Synthetic fixture only | Primary | Safety |
| Inference latency | Timed fixture only; static fixture `NA` | Primary | Component |
| Successful Message Rate | No | `NA` | Primary |
| Actual Time-to-Message | No | `NA` | Primary |
| Transmitted-output Misattribution Rate | No | `NA` | Hard safety outcome |
| Actual selection effort and fallback success | No | `NA` | Primary/secondary |

`NA` means the outcome is not estimable in that mode. It must not be reported
as zero.

## 2. Attempt populations

- **Logged attempts:** all starts, cancellations, failures, abstentions, and
  deviations.
- **Reference-eligible started attempts:** an intentional input began and a
  qualified reference was locked without candidate influence.
- **Non-abstained attempts:** reference-eligible attempts receiving candidates
  rather than fallback.
- **Challenge attempts:** preregistered ambiguous, unusable-input, or
  out-of-distribution conditions for which abstention is the safe target.

The protocol-specific analysis specification controls exact inclusion and
exclusion rules.

## 3. Unconditional Top-k Semantic Coverage

\[
\frac{\text{reference-eligible attempts with an acceptable reference in
Top-k}}
{\text{all reference-eligible started attempts}}
\]

Use the frozen acceptable-paraphrase set. Abstentions and model failures count
as not covered. A plausible but unqualified sentence is not correct.

Also report conditional Top-k coverage among non-abstained attempts as a
secondary measure.

## 4. Hazardous non-abstention and selective risk

Hazardous non-abstention rate:

\[
\frac{\text{wrong Top-1 and non-abstained eligible attempts}}
{\text{all reference-eligible started attempts}}
\]

Selective risk:

\[
\frac{\text{wrong Top-1 among non-abstained eligible attempts}}
{\text{all non-abstained eligible attempts}}
\]

If the selective-risk denominator is zero, report `NA`. In shadow mode these
are counterfactual safety measures; no output occurred.

## 5. Abstention safety

Report:

- challenge abstention sensitivity;
- false-abstention rate on registered clear attempts;
- overall candidate coverage;
- model failure and timeout rate; and
- errors and candidate-set size across the coverage-risk curve.

An unusable or ambiguous input included to test abstention is not removed as a
technical exclusion.

## 6. Calibration

For fixed candidate tasks, report:

- Brier score;
- Expected Calibration Error using frozen bins;
- reliability table or plot when privacy review permits; and
- the target event and sample size.

When a sealed score vector exists, calibration is evaluated over all
reference-eligible attempts, including attempts subsequently withheld by the
abstention policy. Selective calibration among non-abstained attempts may be
reported separately and must use a distinct label.

Consider conformal candidate sets only when a separately frozen calibration
sample is large enough. If the preregistered minimum is not met, report
`not_evaluable`; do not change bins or combine inspected test data.

## 7. Inference latency and availability

Inference latency runs from input end to sealed prediction. Report median,
interquartile range, range, timeouts, and model-completion rate by session.
Inference latency is not Time-to-Message.

## 8. Confirmed-assistive metrics

These metrics require a separate protocol that permits participant-confirmed,
low-risk output.

### Successful Message Rate

\[
\frac{\text{eligible attempts ending in participant-confirmed intended output}}
{\text{eligible communication attempts}}
\]

Report with and without abstentions and with exact numerator/denominator.

### Transmitted-output Misattribution Rate

\[
\frac{\text{spoken or transmitted outputs not supported by valid participant
authorization}}
{\text{all spoken or transmitted outputs}}
\]

The absolute number of serious authorship events is reported separately and
has a hard permitted value of zero.

### Actual Time-to-Message

Measure from the participant's intentional start signal to confirmed
completion. Report median, distribution, cancellations, timeouts, and fallback
route. Do not substitute inference latency.

### Effort, fatigue, and fallback

Record:

- number of selections;
- dwell or switch activations;
- correction and cancellation count;
- setup and calibration time;
- accessible participant-rated fatigue;
- communication-partner workload;
- fallback use and fallback completion; and
- performance by session phase.

## 9. Reporting strata

At minimum stratify by:

- task family and session;
- every novelty-vector axis and N0-N4 derived class;
- fatigue and observed signal-variability state;
- environment/noise and input-quality code;
- familiar versus unfamiliar partner;
- modality and access route;
- message length and personal vocabulary; and
- abstention, model failure, and protocol-deviation status.

Report session-level results in addition to pooled attempts. P001 metrics are
within-person estimates and must not be presented as population accuracy or
clinical effectiveness.
