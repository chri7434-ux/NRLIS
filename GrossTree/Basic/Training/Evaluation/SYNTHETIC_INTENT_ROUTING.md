# WP2.3 Synthetic Model-to-Intent Adapter and Calibrated Candidate Routing

**Version:** 0.1.0

**Data classification:** Synthetic, participant-free engineering (Lane A)

**Implementation:** `../Implementation/synthetic_intent_adapter.py`

## Purpose and scope

This component joins the existing generated-vector MLP to the WP2.2 semantic
vocabulary contract. It produces sealed engineering decisions containing known
concept IDs and their full-class probabilities, or an empty abstention result.
It has no connection to the CareAAC page, event adapter, or confirmation core.
There is no speech, message transmission, participant prediction, or candidate
reveal. The command line accepts no media, model, score file, participant
record, or care-interaction input.

The four synthetic source classes do not cover the forty-concept vocabulary.
Only the following two exact conceptual mappings are supported:

| Source class | Concept ID | Treatment |
|---|---|---|
| `SYN-SEM-WATER` | `need-water` | Eligible only in `basic-needs/basic-essential` |
| `SYN-SEM-REPOSITION` | `comfort-position` | Eligible only in `comfort/comfort-body` |
| `SYN-SEM-PAIN` | None | Abstain; pain is not identical to the broader phrase "I feel unwell" |
| `SYN-SEM-OTHER` | None | Abstain; an unspecified meaning cannot become a phrase |

These are engineering fixture correspondences, not empirically validated
semantic labels. The two mapped classes each occur in a different panel.
Although the contract caps candidate sets at two, the current fixture can
produce at most one candidate per panel. It does not demonstrate multi-option
ranking or forty-concept recognition. Extending class coverage needs a new
versioned synthetic model contract and independent regression expectations.

## Calibration and provenance

The source configuration and exported vocabulary are pinned by canonical JSON
SHA-256 digests using `synthetic_g0.canonical_json_bytes`. The configuration
schema also freezes label order, exact mapping, thresholds, and deny-only flags.
Changing a phrase while retaining a vocabulary version still fails the digest
check. These fingerprints bind repository fixtures, never participant assets.

The adapter generates the existing deterministic 96 development, 32 calibration,
and 48 held-out test vectors. Only development examples enter MLP fitting.
Temperature is selected by minimum negative log likelihood over the frozen
grid on calibration examples; ties select the smaller temperature. Test
examples are absent from both calls. The probability threshold (0.65) and margin
threshold (0.25) are inherited unchanged from the source configuration and are
not fitted to the routed test results. With this probability threshold, a
normalized top-class probability already implies a margin of at least 0.30;
the separate 0.25 margin interlock is currently redundant.

The generated artifact binds source/vocabulary/adapter configuration digests,
both implementation digests, trained parameters, development and calibration
example digests, selected temperature, and threshold origin. A score packet
must match this calibration provenance and the complete ordered class vector.
Packets are an internal synthetic test surface; a caller-supplied classification
string or digest is not proof of consent, data origin, or permission to ingest
real data. The executable generates its own examples and provides no file-ingest
interface. Temperature scaling itself does not establish reliable calibration
for speech or people.

## Routing order

1. Reject malformed, extra-field, non-synthetic, stale-provenance, non-finite,
   negative, length-mismatched, or non-normalized packets with `AdapterError`.
   Boolean values cannot pass as numeric scores or configuration flags.
2. Require a known panel belonging to the requested context.
3. Find the global top class using the complete probability vector and fixed
   label order for ties. An unmapped winner produces `unmapped_top_class`.
4. If the winner is outside the requested panel, produce `top_outside_panel`.
   Do not replace it with the best remaining class.
5. Enforce the frozen probability and margin thresholds. Insufficient evidence
   produces `below_probability` or `below_margin`.
6. For an eligible winner, retain mapped concepts in the requested panel above
   the 0.10 candidate floor, order by full-class probability, and cap at two.
   Filtering never renormalizes probabilities. Unknown-class and outside-panel
   probability mass remains relevant to uncertainty.

Every abstention has an empty candidate list. Every decision retains
`none_of_these`, `repeat`, `cancel`, and `non_predictive_fallback`, marks
confirmation as required, and denies candidate reveal and Care UI connection.
`output_action` is always `no_action_shadow_only`; a high score grants no
confirmation or output authority. Invalid input produces no candidate decision.

## Evaluation and honest limits

Every one of the 48 held-out examples is crossed with all ten fixed panels.
This ensures that neither the reference label nor a favorable panel selection
guides routing. References are attached only after each decision. The resulting
480 routes are dependent repeated evaluations, not 480 independent examples,
real sessions, or a population over which to claim clinical confidence bounds.

The frozen regression contains 17 eligible routes, 270 unmapped-top abstentions,
189 outside-panel abstentions, and four low-probability abstentions. Sixteen of
the 17 candidate routes include the mapped reference; one is wrong. That error
is deliberately retained. The 0.0354 candidate coverage and 1/17 selective error
are fixture regression measurements, not patient accuracy or expected care
performance. Most panels contain no class supported by this four-class model.
No threshold was changed after inspecting these results. Frozen expectations
detect implementation drift; they are not an independent validation dataset.

Unit tests cover exact mapping, unknown/mismatched classes, panel restrictions,
probability preservation, abstention, typed schema rejection, stale source and
vocabulary, test-data exclusion from fitting, deterministic provenance/results,
retained errors, controls/output flags, and tmp-only exclusive artifact writes.
Existing CareAAC tests continue to verify the unchanged non-model UI boundary.

## Run and inspect

From the project root, with the repository dependencies installed:

```bash
python3 GrossTree/Basic/Training/Implementation/synthetic_intent_adapter.py check
python3 GrossTree/Basic/Training/Implementation/synthetic_intent_adapter.py run \
  --output-dir tmp/synthetic-intent-adapter-v0
python3 -m unittest discover \
  -s GrossTree/Basic/Training/Implementation \
  -p 'test_synthetic_intent_adapter.py' -v
```

`check` verifies without creating an artifact. `run` writes `predictions.json`
and `metrics.json` only beneath ignored `tmp/`, refuses overwrite, and rejects
artifact file symlinks. No real recordings, model checkpoints, or participant
records are written. WP1, WP3 and later gates retain their existing state; the
earned evidence ceiling remains G0 synthetic component verification.
