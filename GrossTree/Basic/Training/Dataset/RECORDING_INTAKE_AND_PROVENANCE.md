# WP2.1 Recording Intake and Provenance Framework

**Version:** 0.1

**Status:** Participant-neutral framework verified; real-recording ingest and
analysis not authorized

## 1. Purpose

This framework defines the minimum decisions needed before a recording can be
considered for later research. Version 0.1 is deliberately deny-only. It can
validate a checked-in synthetic example and define a future private metadata
shape, but it cannot authorize access to, ingest of, analysis of, training on,
or release of a real recording.

Possession is not eligibility. A recording remains a quarantined source asset
until provenance, speaker scope, permission scope, storage, labeling, split,
and external-determination records independently support a later transition.

## 2. Repository boundary

The repository may contain only:

- `recording_intake_v0.schema.json`;
- the explicitly synthetic `recording_intake_v0.synthetic.json` fixture;
- the participant-neutral validator and tests; and
- this framework description.

The repository must never contain real audio, an original filename or path,
content-derived text, a transcript, a precise recording time or location, a
speaker name, a direct identifier, or a participant-level integrity hash.
Actual metadata, if later authorized, belongs with the raw asset in an approved
private system and is referenced from research records only through approved
opaque record IDs.

## 3. Intake sequence

The future authorized sequence is:

1. **Contain** - preserve the original outside Git and unapproved AI services;
   do not play, transcribe, segment, hash, or transform it for research.
2. **Classify context** - distinguish naturalistic conversation, structured
   prompt, historical voice, or unknown; record whether collection was ordinary
   care, existing non-research activity, prospective research, or unknown.
3. **Resolve speakers** - determine whether other speakers are present and
   whether their speech can be retained, transformed, demonstrated, or must be
   removed under an approved process.
4. **Separate scopes** - care use, recognition analysis, model training,
   evaluation, personal voice rendering, demonstration, publication, and
   third-party speech are independent permissions.
5. **Qualify references** - a known prompt accepted by the participant or an
   independent pre-reveal participant expression may later be eligible. A
   caregiver interpretation, model proposal, or post-reveal selection is not
   promoted to supervised truth.
6. **Assign chronology before access** - keep recording instances and sessions
   together; never random-split repeated clips across development and test.
7. **Authorize an exact action** - only a later schema version, after the
   Human-ready and activity-specific gates, may represent real ingest,
   analysis, training, inference, candidate reveal, rendering, or release.

## 4. Recording-class routing

| Class | Initial disposition | Possible later role | Not established by the recording |
|---|---|---|---|
| Post-impairment structured prompt | quarantine | development or calibration after participant-accepted prompt/reference review | independent current intent unless the prompt and acceptance route support it |
| Post-impairment naturalistic conversation | quarantine | later ecological evaluation or separately justified development data | clean speaker ownership, unbiased transcript, or ground-truth intent |
| Pre-impairment historical voice | quarantine | downstream rendering of an already confirmed message | current intent, recognition accuracy, or permission to clone/publish |
| Unknown provenance | quarantine | none until resolved | any research eligibility |

Any inspected test recording that changes a model, phrase bank, threshold,
prompt, or analysis becomes development data in a new version.

## 5. Deny-only v0.1 state

The schema intentionally contains no `authorized` permission value. All action
authorizations are constant `false`; scoring and training eligibility are
constant `false`; `split_frozen` is constant `false`; and the only dispositions
are synthetic validation, non-Git quarantine, or metadata inventory.

The validator additionally rejects participant-classified records, sensitive
field names, authorization drift, care-to-research reuse, external approval
pointers inside the synthetic fixture, and any claim that the example is a
real recording. Passing the check proves only that the participant-neutral
contract remains closed.

## 6. Commands

Run the participant-free fixture check:

```bash
python3 GrossTree/Basic/Training/Implementation/validate_recording_intake.py check
```

Run its acceptance tests:

```bash
python3 -m unittest discover \
  -s GrossTree/Basic/Training/Implementation \
  -p 'test_validate_recording_intake.py' -v
```

Do not pass a private manifest or recording to these commands. Real-data
support requires a new reviewed schema and activity authorization; it is not a
hidden flag in v0.1.
