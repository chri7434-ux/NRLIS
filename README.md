# Project NRLIS

**A confirm-first AI communication aid for people with aphasia and other
communication impairments.**

NRLIS is an independent research project by Ziting Yang (Shanghai Pinghe
School). It started from one design question: when someone cannot easily say
what they mean, how do you build an AI aid that helps without speaking for
them? The answer this repository implements is that the system may *suggest*
meanings, but nothing is ever said until the user explicitly confirms it, and
"none of these", "repeat", "cancel" and a non-AI fallback are always one step
away.

> **Status: all evidence is synthetic.** No participant, patient, recording,
> speech or clinical data has been collected or used. Every result in this
> repository comes from generated fixtures and verifies software behaviour
> only; it supports no claim about real-world or clinical performance.
> Validation with real participants is future work and is gated behind ethics
> review and accessible consent.

## What is here

| Component | What it does | Where |
|---|---|---|
| Care-mode AAC interface (v0.3) | Static web prototype: pick a context, choose from a fixed four-concept panel, then explicitly confirm or cancel before any message is shown. Touch, keyboard and switch-scan access; no data capture. | [`GrossTree/Basic/CareAAC/`](GrossTree/Basic/CareAAC/README.md) |
| Neural baseline with calibrated abstention | A two-layer neural network written from scratch in the Python standard library (no ML framework), with temperature-scaling calibration and an abstention rule so the model stays silent when it is not confident. Trained and tested on generated vectors only. | [`participant_free_neural.py`](GrossTree/Basic/Training/Implementation/participant_free_neural.py) |
| Sealed synthetic intent routing | Maps model outputs to stable concept IDs and abstains on unmapped or out-of-panel winners; deliberately disconnected from the interface. | [`synthetic_intent_adapter.py`](GrossTree/Basic/Training/Implementation/synthetic_intent_adapter.py) |
| Safety and data-governance validators | Fail-closed checks that block participant data, real recordings and any output path until the documented gates are met. | [`GrossTree/Basic/Training/Implementation/`](GrossTree/Basic/Training/Implementation/README.md) |
| Research protocol | N-of-1 shadow-mode protocol, accessible-consent plan, metrics (Brier score, ECE, selective risk) and generalization boundaries. | [`GrossTree/`](GrossTree/README.md) |

The automated suite has 144 tests (Python and Node.js); CI runs them on every
push.

## Try it

```bash
pip install -r requirements.txt

# Neural baseline: train, calibrate, abstain and evaluate on synthetic vectors
python3 GrossTree/Basic/Training/Implementation/participant_free_neural.py check

# Run the test suites
python3 -m unittest discover -s GrossTree/Basic/Training/Implementation -p 'test_*.py'
python3 -m unittest discover -s GrossTree/Basic/CareAAC -p 'test_*.py'
node --test GrossTree/Basic/CareAAC/test_interaction_core.mjs

# Open the interface prototype
cd GrossTree/Basic/CareAAC && python3 -m http.server 8765
# then visit http://127.0.0.1:8765/
```

## Related paper

A separate paper by the same author, *Application and Evaluation of GPT-6.1
for Language Reconstruction in Natural Conversations of People With Aphasia*,
has been accepted to CMLAI 2027 (manuscript CMLAI-6323). It proposes an
evaluation framework for GPT-based reconstruction of aphasic speech and
demonstrates it on simulated conversation data. Its evaluation code is not
part of this repository.

## Note on this snapshot

This public repository is a single-commit snapshot of the private development
repository at interface v0.3.0 / WP2.3. Third-party full-text papers have been
removed and are cited by DOI in the
[evidence register](GrossTree/__init__/EVIDENCE_REGISTER.md), and local
machine paths have been removed. No code or test was changed.
Development used AI coding assistants under written workspace rules; see
[`AGENTS.md`](AGENTS.md) and [`AgentCollaboration/`](AgentCollaboration/README.md).

## Detailed project status

The project is currently at **WP2.3 within WP1-Lite participant-free
engineering**, with a separate Human-ready checkpoint before any research use
of participant information. WP0 v0.3 is frozen; deterministic G0, synthetic
neural-training plumbing, the deny-only recording-intake framework, and the
Care-mode AAC semantic vocabulary and deterministic interaction architecture,
and sealed synthetic model-to-concept routing are verified. The neural fixture is not speech and supports no participant-
performance claim. Research contact, pre-consent access checking, intake,
enrollment, recording, participant-data training, participant-specific
inference, research candidate reveal, and research output all remain disabled.

Ordinary family-care AAC may proceed separately for immediate benefit, without
turning care observations into research or training data. The full Human-ready
checkpoint remains blocked on the applicable external determination, activated
roles, accessible-consent approval, and an approved private-data lifecycle.
The current Care-mode MVP uses 40 generic synthetic concepts in fixed four-item
panels, retains no history, and does not access a microphone, model, profile,
cloud service, personal/dialect overlay, or real recording.

## Current intended use

NRLIS may:

- assess which intentional communication channels remain usable;
- route a person to residual-speech, touch, gaze, switch, symbol, or research
  interfaces;
- generate calibrated candidate meanings;
- require user confirmation before speech or message output;
- personalize only from confirmed interactions; and
- monitor performance drift across sessions and changing conditions.

NRLIS is not currently intended to:

- diagnose a neurological or speech-language condition;
- infer unexpressed thoughts;
- substitute AI output for a participant's authorship;
- provide emergency, medical, legal, financial, or consent communication as the
  sole channel;
- claim treatment efficacy or cross-patient clinical generalization; or
- deploy EEG, sEMG, or implanted BCI as part of the initial case.

## Project map

- [Content of Work master index](CONTENT_OF_WORK.md)
- [Project change log](PROJECT_CHANGE_LOG.md)
- [Repository governance](REPOSITORY_GOVERNANCE.md)
- [Contribution workflow](CONTRIBUTING.md)
- [Security and privacy reporting](SECURITY.md)
- [Codex-Grok collaboration bridge](AgentCollaboration/README.md)
- [Project objective and roadmap](GrossTree/__init__/PROJECT_OBJECTIVE_AND_ROADMAP.md)
- [WP1 governance and determination plan](GrossTree/__init__/WP1_GOVERNANCE_AND_DETERMINATION_PLAN.md)
- [Research charter](GrossTree/__init__/PROJECT_CHARTER.md)
- [Generalization boundaries](GrossTree/__init__/GENERALIZATION_BOUNDARIES.md)
- [Workflow and algorithm design](GrossTree/__init__/WORKFLOW_AND_ALGORITHMS.md)
- [Evaluation, safety, and governance](GrossTree/__init__/EVALUATION_SAFETY_GOVERNANCE.md)
- [Evidence register](GrossTree/__init__/EVIDENCE_REGISTER.md)
- [Decision log](GrossTree/__init__/DECISION_LOG.md)
- [Profile schema](GrossTree/Basic/Profiles/PROFILE_SCHEMA.md)
- [Participant P001 pre-enrollment profile](GrossTree/Basic/Profiles/NRLIS-P001/PROFILE.md)
- [P001 intake checklist](GrossTree/Basic/Profiles/NRLIS-P001/INTAKE_CHECKLIST.md)
- [T001 N-of-1 shadow protocol](GrossTree/Basic/Trials/NRLIS-T001/PROTOCOL.md)
- [Accessible consent, agreement, and dissent plan](GrossTree/Basic/Trials/NRLIS-T001/ACCESSIBLE_CONSENT_ASSENT_DISSENT_PLAN.md)
- [T001 reference and authorship SOP](GrossTree/Basic/Trials/NRLIS-T001/TASK_REFERENCE_AUTHORSHIP_SOP.md)
- [Dataset contract](GrossTree/Basic/Training/Dataset/DATA_CONTRACT.md)
- [Data management and withdrawal plan](GrossTree/Basic/Training/Dataset/DATA_MANAGEMENT_WITHDRAWAL_PLAN.md)
- [WP2.1 recording intake and provenance framework](GrossTree/Basic/Training/Dataset/RECORDING_INTAKE_AND_PROVENANCE.md)
- [Care-mode AAC synthetic MVP](GrossTree/Basic/CareAAC/README.md)
- [WP2.3 synthetic model-to-concept routing](GrossTree/Basic/Training/Evaluation/SYNTHETIC_INTENT_ROUTING.md)
- [WP2.2 vocabulary and interaction architecture](GrossTree/Basic/CareAAC/VOCABULARY_ARCHITECTURE.md)
- [T001 analysis specification](GrossTree/Basic/Training/Evaluation/T001_ANALYSIS_SPEC.md)
- [Initial pre-data configuration](GrossTree/Basic/Training/Config/baseline_v0.yaml)
- [Machine-readable WP1 gate registry](GrossTree/Basic/Training/Config/wp1_gate_registry.json)
- [Synthetic G0, neural-training, and WP1 verification implementation](GrossTree/Basic/Training/Implementation/README.md)

The existing architecture image remains at
[`GrossTree/__init__/Overall_view.png`](GrossTree/__init__/Overall_view.png).

## Non-negotiable rules

1. The workflow, not a universal decoder, is the initial unit of
   generalization.
2. A participant must have at least one independently verifiable intentional
   response channel before open-ended AI output can be attributed to them.
3. Shadow mode precedes assistive output mode.
4. "None of these", "repeat", "cancel", and a non-AI fallback are always
   available.
5. Only explicitly confirmed labels may update a personal model.
6. Random utterance-level train/test splitting is not accepted as evidence of
   real-world generalization.
7. Family participation does not remove consent, privacy, independent review,
   or conflict-of-interest requirements.
