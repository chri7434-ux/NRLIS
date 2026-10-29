# Verification Implementation

This directory contains the participant-free execution layer for the first
NRLIS software verification gates. It checks that versioned synthetic records
can be validated, routed through a deterministic non-learning baseline, scored,
and retained with provenance while every output path remains disabled.

It also contains a deterministic two-layer neural baseline over generated
synthetic embedding vectors. That baseline verifies development/calibration/
test separation, neural training, temperature fitting, abstention, evaluation,
and disabled artifact output. The vectors are not speech features; the result
is training-plumbing evidence only, not ASR, participant, or clinical evidence.

The WP2.1 recording-intake validator checks only the participant-free synthetic
metadata fixture. It rejects participant classification, real-recording
context, sensitive/content-bearing field names, permission or authorization
drift, claimed references or split assignment, external approval pointers, and
care-to-research reuse. It accepts no audio path and performs no media access.

It also contains the WP1 governance validator. That validator treats
`wp1_gate_registry.json` as the only authoritative WP1 state, requires
gate-specific ledger-bound external evidence from eligible authority types,
binds decisions to a canonical hash of the normative scope documents, freezes
role-specific competency requirements and stable holder separation, checks
the recorder holder at decision time, enforces current training and review
dates, and rejects duplicated derived WP1 state or enabled participant
execution flags in `baseline_v0.yaml`.

The WP1 gate is intentionally two-layered: JSON Schema validates structure and
required provenance fields, while Python validates cross-record semantics and
exit computation. The `validate_wp1.py check` CLI invokes both layers and
fails closed if Node.js, Ajv, or the semantic check is unavailable. Calling
`validate_registry()` as a Python function runs only the semantic layer and is
not a release gate. Baseline validation uses a duplicate-key-rejecting YAML
safe loader, recursively audits every mapping leaf, and preserves scalar types
so a quoted `"false"` cannot satisfy a Boolean interlock. Mapping keys are
restricted to lowercase `snake_case`, preventing a literal dotted key from
masquerading as a nested executable path.

The allowed conclusion is deliberately narrow:

> G0 component verification passed on synthetic fixtures; no
> participant-performance claim.

Passing these checks does not authorize P001 enrollment, recording, model
training, assistive output, or any clinical or cross-person claim.

## WP2.3 synthetic intent routing

`synthetic_intent_adapter.py` connects the fixed generated-vector MLP to two
exact WP2.2 concept IDs, abstains on unmapped or outside-panel winners, and
keeps full-class probabilities after calibration. It accepts no external input
file and remains disconnected from CareAAC. See
[`SYNTHETIC_INTENT_ROUTING.md`](../Evaluation/SYNTHETIC_INTENT_ROUTING.md) for
provenance, routing order, fixture limitations, and the retained synthetic error.

## Files

- `synthetic_intent_adapter.py` implements the sealed synthetic routing check
  and tmp-only artifact writer.
- `test_synthetic_intent_adapter.py` verifies mapping, uncertainty, malformed
  packets, provenance, fitting isolation, determinism, and disabled output.

- `synthetic_g0.py` implements the standard-library-only validator, baseline,
  metric calculator, deterministic artifact writer, and command-line interface.
- `test_synthetic_g0.py` exercises schema, leakage, split, determinism,
  denominator, output, and path-safety invariants.
- `participant_free_neural.py` implements the standard-library-only synthetic
  multilayer-perceptron training, calibration, abstention, evaluation, and safe
  artifact CLI.
- `test_participant_free_neural.py` exercises strict configuration, synthetic
  classification, split isolation, determinism, frozen metrics, claim limits,
  output controls, and CLI behavior.
- `validate_recording_intake.py` validates the deny-only WP2.1 synthetic intake
  and provenance contract without accessing recordings.
- `test_validate_recording_intake.py` exercises schema closure, sensitive-field
  rejection, synthetic-only classification, permission/authorization closure,
  reference/split denial, and CLI behavior.
- `validate_wp1.py` validates the fail-closed WP1 registry and its
  pointer-only baseline consumer.
- `test_validate_wp1.py` exercises arbitrary-ID rejection, authority/scope
  binding, canonical document and protocol-version anchoring, gate-specific
  evidence and outcomes, revocation and expiry, stable-holder independence
  and turnover, role-specific training, baseline interlocks, consent-scope
  closure, and zero inherited activity authorization.

Inputs are versioned under `Training/Config/` and `Training/Dataset/`. The
frozen metric expectation is under `Training/Evaluation/`. Generated artifacts
inside the repository may be written only under the ignored `tmp/` directory.

## Commands

```bash
python3 -m pip install --requirement requirements.txt
npm ci --prefix AgentCollaboration --ignore-scripts
python3 GrossTree/Basic/Training/Implementation/synthetic_g0.py validate
python3 GrossTree/Basic/Training/Implementation/synthetic_g0.py check
python3 GrossTree/Basic/Training/Implementation/participant_free_neural.py check
python3 GrossTree/Basic/Training/Implementation/synthetic_intent_adapter.py check
python3 GrossTree/Basic/Training/Implementation/validate_recording_intake.py check
python3 GrossTree/Basic/Training/Implementation/validate_wp1.py check
python3 GrossTree/Basic/Training/Implementation/synthetic_g0.py run \
  --output-dir tmp/synthetic-g0
python3 GrossTree/Basic/Training/Implementation/participant_free_neural.py run \
  --output-dir tmp/participant-free-neural-v0
python3 -m unittest discover \
  -s GrossTree/Basic/Training/Implementation \
  -p 'test_*.py' -v
```

The predictor accepts only `observable_signal_code` and
`input_quality_code`. It never receives the prompt, reference semantic label,
care-partner interpretation, or participant data.

Unconditional Top-k coverage treats every abstention as not covered.
Counterfactual Top-1 error, Brier score, and ECE evaluate the sealed score
vector for every scoring-eligible attempt, including attempts whose safety
policy abstained. Hazardous non-abstention and selective risk separately
measure errors that the policy did not withhold.

`challenge_eligible` is a separate denominator from `scoring_eligible`, so a
registered unusable-input challenge remains in abstention-sensitivity testing
without becoming accuracy ground truth. The static fixture also reports
conditional Top-k coverage among non-abstained attempts. Wall-clock inference
latency is explicitly `not_evaluable_in_static_fixture`; its logging and
thresholds belong to timed execution and later frozen shadow blocks.

The frozen challenge target is also independent from the model's abstention
rule. The fixture deliberately contains both a missed challenge and a false
abstention, so challenge sensitivity and false-abstention rate are not
guaranteed by construction.
