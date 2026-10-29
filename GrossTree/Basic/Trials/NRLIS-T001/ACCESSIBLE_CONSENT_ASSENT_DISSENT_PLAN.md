# T001 Accessible Consent, Assent, and Dissent Plan

**Version:** 0.2

**Status:** WP1 submission draft; not approved for participant use

**Consent records permitted in this repository:** None

## 1. Purpose

This plan defines how a future approved T001 consent process would preserve
autonomy when speech is difficult, inconsistent, dialect-specific, or
unavailable. It is not a consent form, capacity instrument, enrollment record,
or substitute for institutional review.

Communication access and decision-making capacity are different questions.
Dysarthria, aphasia, repetition, slow response, dialect use, eye-gaze use, or
inability to speak does not by itself show inability to consent. Conversely, a
care partner's confidence in understanding the person does not establish
legally effective consent.

## 2. Preconditions

Before any participant-facing research consent or accessibility interaction:

- all applicable institutions or authorities have determined their governing
  paths, or a documented reliance/authorization agreement identifies the
  reviewing IRB and all remaining local responsibilities;
- the approved protocol specifies whether any pre-consent access check may
  occur and what, if anything, may be retained;
- `ROLE-CONSENT-ACCESS-REVIEWER` is appointed and independent;
- the participant's preferred language/dialect and accessible formats can be
  offered without relying on AI-generated interpretation;
- the family-investigator conflict plan is active;
- a non-AI communication route and a visible stop/cancel route are available;
  and
- the consent form/process and documentation method are approved.

Existing ordinary-care or family knowledge may inform accessibility planning
only as permitted by the deciding body. It is not silently converted into
NRLIS research data.

## 3. Accessible process

The approved process should:

1. present the study in the participant's preferred accessible combination of
   familiar dialect, standard written language, pictures, audio, demonstration,
   and supported communication;
2. separate one concept per screen, card, or spoken segment;
3. provide enough response time and fatigue breaks;
4. explain research purpose, procedures, risks, alternatives, privacy limits,
   voluntary choice, withdrawal, contacts, and separate data-use options;
5. verify understanding through neutral teach-back, known-answer checks, or
   independent choice without requiring fluent speech;
6. allow questions through the same accessible route;
7. separate participant response from care-partner interpretation in the
   record;
8. repeat or stop when the response is inconsistent or the route fails; and
9. provide the participant or authorized representative an accessible copy of
   the approved information.

The model under study must not translate, infer, score, or validate consent.
Candidate prediction, voice cloning, and personalized inference remain off
during consent.

## 4. Consent authority and representative permission

The participant is presumed to be the decision-maker unless the applicable
process determines otherwise. If capacity is uncertain:

- use the institutionally approved, decision-specific assessment pathway;
- preserve supported decision-making and direct participant involvement;
- identify a legally authorized representative only under the definition
  governing the activity: applicable law, plus the institutional-policy
  fallback in 45 CFR 46.102(i) when that rule applies and no law addresses the
  issue; do not import that fallback into an FDA-regulated pathway whose
  21 CFR 50.3(l) definition refers only to applicable law;
- do not treat a spouse, child, caregiver, family investigator, or health-care
  proxy as a research LAR solely because of that relationship;
- record the legal/ethical basis in approved private storage; and
- obtain the participant's own consent if capacity later becomes sufficient.

Representative permission never authorizes overriding current participant
dissent.

## 5. Participant agreement, dissent, and cancel

For an adult, `participant_agreement` is the preferred operational term.
`Assent` is retained in the filename and cross-project wording only as a
general protection concept or when the governing authority specifically uses
it. Participant agreement is never a substitute for legally effective consent.

The approved plan must operationalize at least:

- affirmative agreement or assent;
- a stop/cancel response;
- rejection or dissent;
- no response or ambiguous response; and
- loss of the access route.

Dissent, distress, repeated avoidance, active resistance, or a previously
reliable cancel signal stops the activity even when representative permission
exists. Ambiguous or absent responses are not assent. A care partner or model
cannot reinterpret dissent as fatigue, confusion, or agreement to preserve the
session.

The approved protocol defines whether and how assent is checked at session
start, before each new modality, and during the session. Every stop is
respected without penalty and is not scored as participant failure.

## 6. Separate permission scopes

No permission implies another. The current state of every scope is
`not_authorized`.

| Activity/permission scope | Separate decision required | Current state |
|---|---|---|
| Research contact | yes, under the approved recruitment path | not authorized |
| Minimal pre-consent access check | yes, only if the deciding body approves its procedure and retention boundary | not authorized |
| Enrollment | yes | not authorized |
| Participant-facing intake | yes | not authorized |
| Non-recorded capability assessment | yes | not authorized |
| Audio recording | yes | not authorized |
| Video recording | yes | not authorized |
| Raw gaze/camera recording | yes | not authorized |
| Derived gaze-coordinate collection | yes | not authorized |
| Historical-media ingest | yes | not authorized |
| Participant-data model training | yes | not authorized |
| Participant-specific inference | yes | not authorized |
| Shadow inference | yes | not authorized |
| Candidate reveal | yes and a later assistive protocol | not authorized |
| Personal voice-clone training | yes | not authorized |
| Rendering an already confirmed message in a cloned voice | yes and a later output protocol | not authorized |
| Message transmission or external action | yes and a later output protocol | not authorized |
| Demonstration to collaborators or the public | yes | not authorized |
| Quoted or media examples in a publication | yes | not authorized |
| External data sharing or transfer | yes | not authorized |
| Future secondary research or model training | yes | not authorized |

Historical audio cannot establish present intent. A voice model, if ever
authorized, is a renderer for an independently confirmed message and never an
authorship or consent channel.

## 7. Re-consent and pause triggers

Pause and obtain institutional guidance or re-consent when applicable after:

- protocol, purpose, risk, compensation, or data-use change;
- adding audio, video, gaze, historical media, AI training, or output;
- adding voice cloning, demonstration, publication, or external sharing;
- a new investigator, institution, site, vendor, or storage location;
- a change in the participant's communication access or decisional ability;
- a privacy, authorship, or adverse event;
- expiration or amendment of an external determination;
- a model or interface change that alters participant experience; or
- movement from shadow to candidate reveal or confirmed-assistive mode.

## 8. Withdrawal

The consent process must explain, in accessible language:

- how to stop the current session;
- how to stop future contact and collection;
- how to request no further use;
- which raw, derived, model, backup, audit, or already disseminated materials
  can or cannot be deleted;
- whether withdrawal requires model rollback or retraining; and
- who independently receives a withdrawal request.

No deletion promise is made until the approved storage and model plan has shown
it is technically and legally feasible. Withdrawal decisions and signatures
stay in approved private storage; this repository may retain only an opaque
status/evidence ID.

## 9. Documentation and quality check

Before enrollment, the consent-access reviewer verifies:

- approved version and language/format;
- identity and authority of the person giving consent, outside Git;
- route used and route reliability;
- understanding checks and unresolved questions;
- absence of family or investigator coercion;
- assent/dissent/cancel status;
- exact permission-scope choices;
- re-consent date or trigger; and
- participant receipt of the accessible information.

A failed or inconclusive check blocks enrollment. It is not overridden by the
technical lead, care partner, family investigator, or model.
