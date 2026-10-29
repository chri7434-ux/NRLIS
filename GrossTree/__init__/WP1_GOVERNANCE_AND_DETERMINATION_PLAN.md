# WP1 Ethics, Roles, and Data-Governance Plan

**Version:** 0.4

**Status:** Human-ready checkpoint open but not met; WP1-Lite participant-free
engineering active; external determinations pending

**WP1 exit:** Not achieved

**Participant-facing research authorization:** None

**Preparation sources consulted:** 2026-07-29

## 1. Purpose and authority boundary

WP1 converts the WP0 ethical and data-protection principles into an auditable
pre-participant governance package. It prepares the material needed for the
applicable institution, IRB or ethics body, privacy/security authority, and
qualified collaborators to make decisions that this repository cannot make.

### 1.1 Right-sized current operating profile

`WP1-Lite` is the project name for work that does not involve a participant:
synthetic or appropriately licensed public data, model and interface code,
simulated access methods, evaluation, calibration, abstention, output
interlocks, and participant-neutral preparation. It is active now and does not
require the seven formal roles to be staffed.

WP1-Lite is not a registry exit state, institutional determination, exemption,
enrollment, or participant authorization. The authoritative WP1 registry
remains fail-closed. The full role and evidence package below is activated at
the first of these transition points:

- a formal external determination or protocol request;
- systematic participant-facing collection or analysis for research;
- retention of a completed participant profile, audio, video, gaze, health, or
  historical-media information;
- participant-specific training or inference; or
- candidate reveal, personal-voice rendering, transmission, demonstration, or
  publication using participant information.

Ordinary family-care AAC is a separate non-research lane. It may help P001 now,
but its observations and records are not retrospectively converted into NRLIS
research data.

Opening WP1 authorizes only:

- drafting and reviewing participant-neutral governance documents;
- assigning role IDs and seeking qualified collaborators;
- requesting an institutional or ethics determination;
- selecting a proposed storage class without placing participant data there;
- validating fail-closed machine-readable gates; and
- synthetic or appropriately licensed public-data model development and
  testing under participant-free claim limits.

Opening WP1 does **not** authorize participant contact for research,
pre-consent access checking, enrollment, intake, capability profiling,
recording, historical-media ingest, participant-specific inference,
participant-data model training, candidate display, voice synthesis,
transmission, publication examples, or secondary use.

## 2. Applicability matrix

The project records an authoritative external determination rather than
self-classifying an activity as exempt, minimal risk, non-device, or outside a
privacy rule.

| Domain | Current state | Question requiring an authoritative answer | Fail-closed consequence |
|---|---|---|---|
| Human-participant research | unresolved | Does the proposed systematic, generalizable P001 work require institutional/IRB review, exemption determination, or another pathway? | No participant-facing research |
| Institutional engagement | unresolved | Under whose auspices will the work occur, and which institution is engaged? | No use of institutional role, systems, or affiliation to conduct the study |
| Sites and jurisdiction | unresolved | Where are participant, investigator, storage, and analysis activities located, and which local rules apply? | No enrollment or cross-site transfer |
| Consent authority | unresolved | Can the participant consent through an accessible route; if not, who qualifies under the LAR definition governing the activity? Under 45 CFR 46.102(i), this includes the institutional-policy fallback when no applicable law addresses the issue; the FDA definition does not add that fallback. | No enrollment; family status alone confers no authority |
| Additional safeguards | unresolved | What protections are required for communication or possible decision-making impairment and family-investigator conflict? | Independent consent-access and conflict review required |
| HIPAA/health-data rules | unresolved/conditional | Will a covered entity, business associate, or protected health information be involved? | Apply the stricter project privacy controls regardless; do not claim HIPAA compliance |
| Device/FDA/IDE pathway | unresolved/conditional | Does the intended use or investigation involve a device software function, and is a study-risk determination required? | No clinical/device claim or investigational-device activity |
| International/cross-border transfer | unresolved/conditional | Will any participant data cross national or institutional boundaries? | No transfer |
| Voice and biometric-like data | in scope for project controls | What separate permissions and third-party rights apply to voice, video, gaze, and historical recordings? | No collection, ingest, cloning, demonstration, or publication |

If the work is conducted under Cornell auspices, Cornell states that its IRB
oversees human-participant research conducted by affiliated faculty, staff, and
students, and that investigators cannot self-exempt. The actual institutional
route remains unresolved until the relevant office provides a written
determination. Work involving multiple institutions or jurisdictions may have
parallel obligations. NRLIS must obtain determinations from all applicable
institutions or authorities unless a documented reliance or authorization
agreement designates a reviewing IRB and records the remaining local
responsibilities.

## 3. Full Human-ready roles and separation

Names, contact information, signatures, credentials, and appointment documents
remain outside this repository. The repository records only role IDs, stable
opaque holder IDs, status, hashes, and opaque evidence-record IDs.

These are responsibility functions for the future participant-facing lane, not
a requirement to recruit seven people before participant-free engineering.
One person may hold multiple functions when the applicable process permits it,
but a second title never creates independence where independence is required.

| Role ID | Responsibility | Required independence | Current state |
|---|---|---|---|
| `ROLE-ACCOUNTABLE-INVESTIGATOR` | Accountable protocol owner and external submission | Must meet the governing institution's eligibility rules | unassigned |
| `ROLE-ETHICS-CONTACT` | Records and reconciles externally issued determinations and amendment conditions | Institutionally authorized contact; distinct from the technical lead | unassigned |
| `ROLE-CONSENT-ACCESS-REVIEWER` | Reviews accessible consent, assent/dissent, and voluntariness | Not the family investigator or sole care partner | unassigned |
| `ROLE-SLP-CLINICAL-COLLABORATOR` | Reviews communication access, AAC fallback, and burden | Qualified and represented by a stable holder ID distinct from the technical lead | unassigned |
| `ROLE-TECHNICAL-LEAD` | Owns versioned software, model, and output controls | Cannot self-approve safety promotion | unassigned |
| `ROLE-DATA-STEWARD` | Owns storage, access, retention, deletion, and incident controls | Cannot be the only auditor of their own access | unassigned |
| `ROLE-INDEPENDENT-EVENT-REVIEWER` | Reviews adverse, ambiguous, privacy, and authorship events | Not the family investigator or model developer for the reviewed event | unassigned |

The family investigator relationship is a material conflict that must be
disclosed and managed. The family investigator may provide observations or
technical work within an approved plan, but cannot be the sole person who:

- determines consent capacity or legal authority;
- obtains or validates consent;
- serves as the sole SLP/clinical collaborator;
- interprets assent, dissent, cancel, or intent;
- creates the reference truth;
- judges communication success;
- reviews an adverse or ambiguous authorship event; or
- promotes the project to a new activity or output mode.

Role combinations require written approval and an opaque combination-approval
record. Different appointment IDs do not make one person independent: required
separation is checked against the stable opaque holder ID. The
`independence_required` policy is frozen per role rather than accepted from
mutable registry input. Absence of a required role, current training, finite
role expiry, or independence evidence blocks WP1 exit.

## 4. WP1 exit gates

The machine-readable source is
`../Basic/Training/Config/wp1_gate_registry.json`. WP1 exits only when:

1. all applicable institutions or authorities have issued the required scoped
   determinations, or a documented reliance/authorization agreement identifies
   the reviewing IRB and all remaining local responsibilities;
2. site, jurisdiction, consent-authority, privacy, and device questions have
   a current scoped decision; only applicability gates `WP1-G01` through
   `WP1-G05` may carry a `not_applicable` evidence outcome, while the gate
   status itself must still be `satisfied`;
3. the accessible consent/assent/dissent pathway has been approved;
4. every required role is appointed, trained, and conflict-checked;
5. the storage, access, retention, withdrawal, deletion, backup, and incident
   plan has been approved;
6. the possible future participant-facing activities and modalities are
   bounded for a later, separate authorization decision; and
7. an independent WP1 exit review records `requirements_satisfied`.

`null`, `unresolved`, `in_progress`, `not_applicable` as a gate status,
`failed`, `expired`, missing evidence, scope mismatch, an incompatible
decision outcome, or an unapproved role combination is blocking. A document
draft, software check, family agreement, or collaborator conversation is not
an external determination.

Every gate requires a gate-specific current evidence type from an eligible
authority. Gates `WP1-G01` through `WP1-G24` must be recorded by a verified
`ROLE-ETHICS-CONTACT`; `WP1-G25` must be recorded by the verified independent
event reviewer. An arbitrary `EXT-*` string, internal memo, generic approval,
training-provider record, or technical-lead self-attestation cannot close a
gate. Each ledger record binds:

- an identified issuing authority with an official URI and verification
  hashes;
- record type, decision outcome, and covered gate or role IDs;
- immutable artifact and external-record-locator hashes;
- protocol version and a canonical determination-scope hash derived from the
  frozen activity-key set, registry-schema version, and hashes of the ten
  governing documents: the full T001 normative specification set plus the
  project charter;
- effective, review-due, expiry, and revocation state; and
- the internal role and stable holder who recorded the external outcome.

The issuing authority and the internal recorder are separate fields.
Terminal gates require a future `review_due_on`; verified roles and their
training require finite future validity. Each verified role must have an
appointment covering that role, the exact role-specific competency set, and
any required independence record, all bound to its current stable holder.
`WP1-G25` requires a current `independent_exit_review` record made by the
same reviewer holder recorded on the gate; changing the reviewer cannot
inherit an earlier holder's exit decision. That reviewer must remain distinct
from the accountable investigator and technical lead.

The required machine gate is the combined JSON Schema and semantic-validation
toolchain. The schema layer enforces field structure and provenance-field
presence; the semantic layer enforces referential integrity, frozen policies,
scope binding, strict typed and recursive baseline interlocks, dates, and exit
computation. Neither layer is a complete gate alone. Even together they cannot
prove that an outside institution actually issued a record. The ethics contact
must reconcile each hash and opaque locator against the external system, and
the independent exit reviewer must review that reconciliation. Any governing
scope-document change invalidates a previously computed scope hash until the
relevant determinations are refreshed. The current authority, evidence, and
training ledgers are empty, and the current determination-scope hash is
`null`.

WP1 completion would make the project eligible to create a separately
authorized WP3 Stage A activity. It would not itself enable enrollment,
recording, participant-data training, shadow inference, candidate reveal,
voice rendering, message transmission, or publication.

The authorization rule is layered:

`project/institution gate AND enrollment gate AND session/activity gate AND
modality/data-layer gate AND record/output gate AND no active hold`

Only a later activity registry may record the resulting authorization. A
human-readable approval, a satisfied WP1 scope gate, or `wp1_exit_authorized`
never changes an activity while `authorizations.<activity>` is false.

## 5. Determination-request brief

The accountable investigator should provide the deciding body with a consistent
description:

- **Purpose:** develop prospective within-person evidence, capped at G2 for
  P001, and a workflow method that can later be tested for portability with
  independent participants.
- **Current state:** protocol/schema/synthetic preparation only; no participant
  enrolled and no participant data collected under NRLIS.
- **First possible future human interaction:** a minimal pre-consent access
  check only if the deciding body separately authorizes its procedure and
  retention boundary; after legally effective consent and enrollment, an
  accessible capability and non-AI communication baseline without raw media
  by default.
- **Later possible modalities:** residual speech audio, screen interaction, eye
  gaze, and historical audio, each separately scoped.
- **Initial AI mode:** shadow only; no candidate reveal, speech, transmission,
  or action.
- **Excluded uses:** diagnosis, treatment, an NRLIS model or research claim
  that determines decision-making capacity, emergency/high-risk communication,
  unconfirmed output, and thought reading. Consent validity still follows an
  externally approved, decision-specific process when capacity is uncertain.
- **Family conflict:** the investigator is related to P001 and will not be the
  sole consent, intent, reference, success, or event authority.
- **Data boundary:** no participant assets, signatures, re-identification key,
  or personal model in Git; proposed encrypted storage and deletion plan
  require approval.

The request should ask the authority to document:

1. whether and under whose auspices the activity is human-participant research,
   including every applicable institution and any reliance/authorization
   agreement;
2. required review category and conditions;
3. accountable-investigator and training requirements;
4. whether and how a family investigator may recruit, consent, observe, or
   collect data;
5. the approved accessible-consent and possible representative-permission
   pathway;
6. required safeguards for communication or fluctuating decision-making
   access;
7. whether physiological/device, international, privacy, or conflict reviews
   are required;
8. which Stage A activities and modalities could be eligible for a later
   separate authorization, if any;
9. approved storage and incident-reporting requirements; and
10. amendment triggers for recording, AI training, shadow inference, candidate
    reveal, voice cloning, or publication.

## 6. Official anchors

- HHS OHRP, [Federal Policy for the Protection of Human Subjects](https://www.hhs.gov/ohrp/regulations-and-policy/regulations/common-rule/index.html)
- HHS OHRP, [Informed Consent FAQs](https://www.hhs.gov/ohrp/regulations-and-policy/guidance/faq/informed-consent/index.html)
- HHS OHRP, [Exempt Research Determination FAQs](https://www.hhs.gov/ohrp/regulations-and-policy/guidance/faq/exempt-research-determination/index.html)
- eCFR, [45 CFR 46.102(i)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46/subpart-A/section-46.102)
- eCFR, [21 CFR 50.3(l)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50/subpart-A/section-50.3)
- HHS OCR, [HIPAA de-identification guidance](https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html)
- FDA, [How to Determine if Your Product is a Medical Device](https://www.fda.gov/medical-devices/classify-your-medical-device/how-determine-if-your-product-medical-device)
- FDA, [Investigational Device Exemption](https://www.fda.gov/medical-devices/premarket-submissions-selecting-and-preparing-correct-submission/investigational-device-exemption-ide)
- NIST, [AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- Cornell Research Services, [Research with Human Participants](https://researchservices.cornell.edu/compliance/human-research)
- Cornell Research Services, [IRB Informed Consent](https://researchservices.cornell.edu/resources/irb-informed-consent)
- Cornell Research Services, [Human-participant data considerations](https://researchservices.cornell.edu/resources/human-participant-data)
- Cornell Research Services, [IRB FAQs](https://researchservices.cornell.edu/resources/irb-faqs)

These sources guide preparation but do not decide NRLIS applicability. The
scoped written determination and approved institutional documents control.
