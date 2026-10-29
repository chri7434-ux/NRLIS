# NRLIS Data Management and Withdrawal Plan

**Version:** 0.2

**Status:** WP1 planning baseline; storage and retention approval pending

**Participant data currently authorized:** None

## 1. Governing boundary

This plan operationalizes `DATA_CONTRACT.md` without selecting or approving a
real storage system. A store name, path, account, credential, encryption key,
contact, participant identity, signature, or re-identification key must never
be added to this repository.

The future completed P001 capability profile is sensitive single-person
research data. A project ID does not make an N-of-1 profile anonymous. The
completed profile and participant-level logs therefore belong in approved
private storage by default. Git retains only the participant-neutral schema,
the empty P001 placeholder, synthetic fixtures, code, and
disclosure-reviewed, release-approved reporting material.

## 2. Data classes and default locations

| Class | Examples | Repository | Approved private store | Current authorization |
|---|---|---:|---:|---|
| Governance metadata | schema versions, empty gates, opaque approval IDs | allowed | optional | internal preparation only |
| Consent/identity | names, signatures, authority documents, contacts, re-identification key | prohibited | required and separated | none |
| Raw signal | audio, video, gaze, screen capture, device stream | prohibited | required | none |
| Historical media | pre-impairment audio/video and speaker metadata | prohibited | required | none |
| Derived signal | segments, features, embeddings, quality measures | prohibited at participant level | required | none |
| Profile/reference | completed capability profile, prompts, labels, semantic content | placeholder/schema only | required | none |
| Prediction/audit | candidate sets, scores, selections, events, session logs | schema or synthetic only | required | none |
| Personal model | adapter, recognizer, voice model, checkpoint, cache | prohibited | required | none |
| Reporting | disclosure-reviewed, release-approved aggregates and approved examples | conditionally allowed | source copy required | none |

No consumer sync folder, source repository, chat, email attachment, or
unapproved AI service is an approved participant-data store.

## 3. Storage approval record

Before any collection or ingest, an external approval record must document:

- opaque store ID and approved data classes;
- institutional owner and `ROLE-DATA-STEWARD`;
- encryption in transit and at rest;
- authentication, least privilege, and account lifecycle;
- device and endpoint controls;
- audit logging and review frequency;
- backup location, encryption, recovery objective, and restore test;
- vendor and subcontractor status, if any;
- geographic location and transfer restrictions;
- incident contacts and reporting deadlines;
- retention and secure-destruction mechanism; and
- amendment/expiry conditions.

The current values are `unresolved`. A proposed platform, encrypted laptop, or
cloud subscription does not count as approval.

## 4. Access matrix

Access is need-to-know, time-limited, and recorded outside Git.

| Role | Identity/consent | Raw/historical | Derived/profile | Model | Release-approved report |
|---|---:|---:|---:|---:|---:|
| Accountable investigator | as approved | as approved | as approved | as approved | yes |
| Consent-access reviewer | consent scope only | no by default | consent status only | no | no |
| SLP/clinical collaborator | no by default | minimum necessary | minimum necessary | no by default | as approved |
| Technical lead | no | minimum necessary if approved | coded minimum | as approved | yes |
| Data steward | administrative minimum | custodial | custodial | custodial | yes |
| Independent event reviewer | event-specific minimum | event-specific minimum | event-specific minimum | no by default | event outcome |
| Family investigator/care partner | no research-store access by relationship alone | no by relationship alone | contributed observation only as approved | no | approved summary only |

Role combination does not expand access. Emergency or break-glass access
requires a documented process and later independent review.

## 5. Data minimization and provenance

Collect only fields required by the approved task and analysis. Each retained
record must include:

- opaque participant/session/attempt/asset IDs;
- consent-scope and protocol version;
- acquisition purpose and modality;
- creator/transformer role ID;
- source and transformation provenance;
- data-layer classification;
- retention class;
- split and training eligibility;
- correction/supersession link; and
- deletion-hold or withdrawal status.

Free-text notes are minimized because dialect examples, household vocabulary,
rare conditions, dates, and narrative context can re-identify an N-of-1
participant.

## 6. Retention schedule

WP1 does not invent retention periods. Before collection, all applicable
institutions or authorities, subject to any documented reliance/authorization
agreement, and the data steward must approve a duration and trigger for each:

- consent/authority records;
- re-identification key;
- raw and historical media;
- derived features and embeddings;
- profile, reference, prediction, and audit records;
- model checkpoints and voice artifacts;
- encrypted backups;
- adverse-event/noncompliance records; and
- published or archived aggregate records.

Every duration must specify its start event, legal/institutional basis, secure
destruction method, backup propagation time, and owner. `indefinite` is not a
default.

## 7. Withdrawal and deletion workflow

An approved withdrawal request is translated into a versioned action manifest:

1. stop new contact, collection, training, and inference as requested;
2. freeze affected assets and model versions against further use;
3. identify raw, historical, derived, profile, prediction, model, backup, and
   reporting descendants through provenance;
4. determine which items can be deleted, must be retained, or have already
   been irreversibly disseminated under the approved consent;
5. delete or quarantine eligible primary copies;
6. propagate deletion to backups under the approved schedule;
7. retrain, unlearn, roll back, or retire affected personal models as
   pre-specified;
8. invalidate derived reports or test claims when required;
9. independently verify the action; and
10. provide an accessible outcome explanation.

If a model cannot be shown to exclude withdrawn data, it remains disabled.
NRLIS does not promise machine unlearning or total deletion until the approved
system demonstrates it.

## 8. Historical voice and third parties

Historical recordings may identify or contain other speakers. Before ingest:

- the participant's separate scope is authorized;
- ownership and lawful access are documented externally;
- third-party voices and private content are reviewed;
- non-participant segments are removed or separately authorized;
- demonstration/publication and training rights are not inferred from
  possession; and
- the original remains outside Git and unapproved AI services.

Recognition research, personal voice training, rendering, demonstration,
publication, and future training are separate scopes.

## 9. Incident and breach response

Any suspected unauthorized access, loss, disclosure, misrouting, unapproved
model use, participant-data commit, or scope violation triggers:

1. stop collection, transfer, training, inference, and output;
2. preserve minimal audit evidence without copying sensitive content;
3. contain credentials, links, accounts, and affected artifacts;
4. notify the data steward and accountable investigator;
5. follow institutional/IRB/privacy reporting requirements and deadlines;
6. assess participant notification through the authorized channel;
7. document corrective and preventive actions; and
8. obtain independent clearance before resumption.

A participant-data commit is not cured by deleting the working-tree file; Git
history and remote copies require the approved incident process.

## 10. WP1 data-plan exit evidence

This plan passes only when opaque records show:

- approved store and data-class mapping;
- verified role/access matrix;
- key and identity separation;
- approved retention schedule;
- tested backup and recovery;
- feasible withdrawal/deletion/model-disposition workflow;
- incident contacts and reporting route; and
- independent data-steward and ethics approval.

Until then, the gate status remains `unresolved` or `in_progress`, and all
participant-data authorizations remain false.
