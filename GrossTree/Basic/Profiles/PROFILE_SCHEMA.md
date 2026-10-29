# Capability Profile Schema

**Version:** 0.2

**Status:** Participant-neutral schema; completed profiles require approved
private storage

**Purpose:** Describe communication-relevant capabilities without converting
observations into an unsupported diagnosis.

Each field must include a source:

- `participant_confirmed`
- `clinician_documented`
- `care_partner_reported`
- `researcher_observed`
- `device_measured`
- `unknown`

## 1. Administrative fields

- Project participant ID
- Profile version and date
- Enrollment status
- Consent/permission path
- Independent consent-access reviewer
- Approved data uses
- Prohibited data uses

Do not store name, exact birth date, address, phone number, medical-record
number, or re-identification key in this profile.

A project ID does not make a single-person capability profile anonymous. The
completed profile is sensitive participant-level research data and must remain
in the approved private store. The Git version for P001 remains an empty
pre-enrollment placeholder unless an authority and data steward explicitly
approve a disclosure-reviewed aggregate.

Permission scopes for capability assessment, audio, video, gaze, recognition,
historical-media ingest, personalized training, voice cloning, rendering,
demonstration, publication, sharing, and future use are separate. A profile
records only opaque permission-state/evidence IDs, never signatures or legal
authority documents.

## 2. Clinical context

- Age band
- Stable, fluctuating, or progressive course
- Clinician-established diagnoses, if available
- Onset interval rather than exact identifying date
- Relevant treatment or assistive-device context
- Acute-change warning status

Observed symptoms must remain separate from diagnoses.

## 3. Language and cultural profile

- Primary language(s)
- Dialect or regional variety
- Language used before impairment
- Language currently attempted
- Reading and writing languages
- Familiar communication partners
- Preferred form of written semantic labels
- Whether pictures, text, audio, or combinations are easiest
- Personal names, household words, and culturally specific vocabulary

## 4. Receptive communication

Assess separately:

- spoken single words;
- spoken short instructions;
- written words and sentences;
- pictures and symbols;
- familiar versus unfamiliar partners;
- yes/no question consistency; and
- ability to detect an intentionally incorrect option.

## 5. Expressive and speech profile

- spontaneous vocalization
- prompted word or phrase production
- intelligibility to familiar listener
- intelligibility to unfamiliar listener
- repetition, initiation, rate, loudness, and variability
- oral versus written formulation
- gesture and facial expression
- known reliable messages
- known ambiguous signals

## 6. Access profile

For each access method, record accuracy, latency, fatigue, positioning, and
failure mode:

- direct touch
- keyboard
- head movement
- eye gaze
- blink
- switch
- vocal yes/no
- gesture
- partner-assisted scanning
- other

## 7. Sensory and cognitive access

- visual acuity or relevant limitation
- visual field or attention concern
- hearing access
- sustained attention
- fatigue pattern
- ability to learn a stable interface layout
- ability to correct or cancel

This is not a cognitive diagnosis section.

## 8. Communication-needs inventory

- highest-priority people and settings
- urgent fixed messages
- daily needs
- social and emotional expression
- open-ended conversation
- telephone or remote communication
- privacy-sensitive messages
- messages that must never be AI-generated

## 9. Historical voice and language assets

- type and approximate quantity of pre-impairment audio
- recording quality and number of speakers
- transcript availability
- dialect coverage
- consent for recognition research
- consent for personal voice synthesis
- consent for demonstrations or publication

## 10. Initial routing decision

- primary input route
- secondary route
- independent confirmation route
- non-AI fallback
- prohibited routes
- rationale
- unresolved questions
- reviewer and date
