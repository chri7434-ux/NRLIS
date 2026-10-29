# WP2.2 Synthetic Interaction and Vocabulary Architecture

**Version:** 0.1.0

**Implementation target:** Care-mode AAC v0.2.0

**Data classification:** Synthetic, participant-free, non-research

## 1. Purpose

WP2.2 defines the stable contract between a future signal model and the
communication interface. A model must return a bounded semantic `concept_id`;
it must not directly generate, speak, transmit, or act on free text. The Care
interface maps that identifier to a versioned surface phrase, places it in a
pending state, and displays it as the current message only after a separate
confirmation action.

The architecture is designed to support different access routes and degrees of
speech limitation without claiming that one vocabulary is suitable for every
person. Its reusable contribution is the contract and state machine. The
checked-in Chinese phrases are generic synthetic fixtures, not a P001 profile,
dialect model, clinical vocabulary, or validated communication inventory.

## 2. Separation of concerns

The implementation keeps five layers separate:

1. **Concept layer:** stable machine-facing identifiers and semantic domains.
2. **Surface layer:** canonical and compact Chinese renderings of the same
   bounded meaning.
3. **Navigation layer:** contexts and fixed four-item panels that control visual
   burden without changing concept meaning.
4. **Interaction layer:** deterministic transitions for propose, reject,
   confirm, cancel, repeat, panel navigation, and fallback.
5. **Access layer:** pointer, keyboard, auto-scan, or a bounded external
   focus/activate adapter. Access methods invoke the same controls and cannot
   bypass confirmation.

The model-facing interface is therefore:

`bounded evidence -> concept_id or abstain -> pending surface form -> explicit
confirmation -> visual output`

`context_id` may constrain the candidate universe, but it is not itself a
semantic label. `panel_id` is a presentation device, not a training target.

## 3. Vocabulary rules

Every checked-in concept must have:

- a globally unique, stable `concept_id`;
- one controlled semantic domain and speech-act class;
- one canonical and one compact surface form with the same intended meaning;
- `ordinary_care_low_risk` classification;
- `always_required` confirmation;
- `confirmed_visual_only` output policy; and
- `curated_synthetic` provenance.

Every panel contains exactly four distinct concepts. Ordering is fixed and
versioned. No frequency learning, inferred personalization, hidden reranking,
or care-interaction logging is permitted. Changing a concept's meaning requires
a new identifier. Editing wording without changing meaning requires a new
vocabulary version and review of both surface forms.

The synthetic vocabulary excludes emergency instructions, diagnosis,
medication or treatment decisions, legal/financial decisions, consent, and
claims about decision-making capacity. A message may express an ordinary need
or feeling; it must not be presented as a verified medical fact.

## 4. Surface modes

`canonical` is the default complete sentence. `compact` reduces reading and
selection burden but is not a different intent. Switching modes is transient,
local, and global to the currently rendered panel. A pending candidate is
re-rendered from its `concept_id`; the surface selector cannot change the
underlying meaning.

No dialect form is included in v0.2. Dialect tokens, personal names, household
terms, culturally specific phrases, and historical voice style require a later
private, permission-scoped vocabulary overlay. That overlay must never alter
the base concept silently and is not authorized by this work package.

## 5. Interaction invariants

The pure interaction core enforces these invariants independently of the DOM:

- only a concept visible in the current panel may become pending;
- navigation never confirms or emits a message;
- rejection clears the pending concept and preserves the prior confirmed
  message;
- confirmation requires a pending concept and is the only transition that can
  create confirmed output;
- `none`, `repeat`, and panel navigation create no output;
- `cancel` clears context, pending state, fallback, and confirmed output;
- non-AI fallback clears pending and confirmed output and stops prediction flow;
- all state is memory-only and contains no event history, timestamps, user
  identifiers, confidence score, or response-time measurement; and
- external access events may focus or activate existing controls only.

## 6. Synthetic interaction suite

`synthetic_interactions_v1.json` exercises the core through declarative,
participant-free scenarios. It covers direct confirmation, rejection and
correction, panel navigation, compact rendering, none-to-fallback, repeat, and
cancel. The suite stores only synthetic control identifiers and expected state;
it is not an interaction log and cannot accept real observations.

Both the vocabulary and scenario suite have strict JSON Schemas plus semantic
validation. Node tests execute every scenario against the same core used by the
browser. CI also checks that no capture, persistence, networking, media,
speech-synthesis, or research-output surface has appeared.

## 7. Extension contract

Later signal or language modules may propose only a member of the currently
allowed concept set or abstain. They may supply calibrated scores to a future
research-only adapter after the relevant gates, but they cannot:

- introduce free text;
- remove `none/repeat/cancel/fallback`;
- auto-confirm from confidence;
- infer a personal phrase from care use;
- modify ordering or surface form without a version change; or
- convert a Care-mode interaction into a research record.

Future vocabulary personalization should use an immutable base vocabulary plus
a separately versioned private overlay with explicit provenance, meaning review,
permission scope, collision checks, and withdrawal behavior. That work remains
outside WP2.2 and outside the current repository.
