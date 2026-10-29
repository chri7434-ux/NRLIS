# Care-mode AAC Synthetic MVP — Interface v0.3

**Interface version:** 0.3.0 (`NRLISCareAAC.uiVersion`)

**Vocabulary/configuration version:** 0.2.0 (`NRLISCareAAC.version`)

**Mode:** Ordinary family-care demonstration; non-research

**Data capture:** None

## Purpose

This local, static prototype demonstrates a low-risk communication flow over a
versioned semantic vocabulary:

`choose a context -> inspect one fixed four-concept panel -> change panel or
surface form if needed -> select -> explicitly confirm or cancel -> show the
confirmed visual message`

It uses 40 generic synthetic concepts in five contexts and ten fixed panels.
Stable `concept_id` values are separate from canonical and compact Chinese
surface forms. It does not access a microphone, camera, recording, participant
profile, model, cloud API, browser storage, or analytics service. It does not
score performance or create a dataset.

The prototype is a communication aid, not an emergency, medical, legal,
financial, or consent channel. A non-AI communication board and ordinary care
path remain available.

## Safety behavior

- Candidate text is a suggestion until the user selects and confirms it.
- `都不是`, `重复这些选项`, `取消`, and `转到非AI沟通板` remain available.
- Visual output occurs only after explicit confirmation.
- No synthesized speech or automatic transmission occurs.
- No interaction history is persisted, logged, downloaded, or uploaded.
- Panel order is fixed; there is no hidden ranking or frequency learning.
- Switching between complete and compact phrases does not change concept ID.
- Reloading the page clears the transient in-memory state.
- Care use never creates research or training eligibility.

The interface cannot determine who pressed a control. During real family care,
the confirmation control must be operated through the intended user's reliable
access route; a care partner should not silently confirm a proposed message on
the user's behalf.

## Access methods

The page supports:

- touch or pointer activation;
- keyboard shortcuts `1`-`4` for visible candidates;
- `Escape` for cancel;
- optional auto-scan with `Space` to activate the highlighted control; and
- an adapter contract for future gaze or switch software.

The confirmation dialog opens with focus on the question. `Tab` and
`Shift+Tab` stay within its controls; rejecting returns focus to the selected
phrase. Holding down a shortcut cannot repeatedly activate confirmation.
Native phrase-display and scan-speed selectors keep their own keyboard input.
The four safety actions are available inside the dialog as well as on the board.
While the dialog is open, access-adapter events cannot activate the background
context, phrase, or navigation controls.

Auto-scan can continue from a selected phrase into the confirmation dialog,
starting at rejection. It can also be started or stopped inside the dialog.
Highlighting a control never confirms it; activation is a separate action.
`Escape` stops scanning and clears the temporary interaction state.

An adapter may dispatch either event on `window`. `controlId` can address a
context, visible concept, navigation control, confirmation, rejection, or a
global safety action:

```javascript
window.dispatchEvent(new CustomEvent("nrlis-access-focus", {
  detail: { controlId: "concept:need-water" }
}));

window.dispatchEvent(new CustomEvent("nrlis-access-activate", {
  detail: { controlId: "concept:need-water" }
}));
```

Examples include `context:basic-needs`, `action-next-panel`,
`action-confirm`, and `action-cancel`. The v0.1 `choiceId` property remains a
temporary compatibility alias but receives the same bounded control lookup.

This contract does not itself implement eye tracking. Gaze dwell thresholds,
calibration, cancel reliability, and device validity require separate testing.

## Interface design

The v0.3 presentation uses a desktop context sidebar and a compact mobile
context strip, four large phrase cards, a dedicated confirmation dialog, and
a clearly labelled current-message area. Operation help and scan speed sit
inside an expandable settings section. All visible buttons have targets of at
least 44 by 44 CSS pixels in the verified 320–1440 pixel viewport range.

System fonts, inline line icons, a neutral background, restrained blue accents,
soft borders, and brief transitions keep the flow readable. The design draws
on Apple's guidance for [materials](https://developer.apple.com/design/human-interface-guidelines/materials),
[motion](https://developer.apple.com/design/human-interface-guidelines/motion),
and [accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility).
There are no external fonts or image assets. Reduced-motion preferences disable
animations and smooth scrolling; CSS also provides reduced-transparency and
higher-contrast treatments. This refresh preserves the v0.2 vocabulary,
deterministic interaction core, and model/data boundaries.

The interface requires a modern browser with native modal `dialog` support.
Desktop and mobile viewport checks were run in Chromium; physical assistive
devices and other browser engines require separate verification.

## Architecture files

- `VOCABULARY_ARCHITECTURE.md` defines stable concept, surface, panel,
  interaction, and future private-overlay contracts.
- `synthetic_vocabulary_v1.schema.json` and
  `synthetic_vocabulary_v1.js` define and instantiate the strict 40-concept
  synthetic vocabulary.
- `interaction_core.js` is the DOM-independent transition system used by both
  the page and executable tests.
- `synthetic_interactions_v1.schema.json` and
  `synthetic_interactions_v1.json` define seven participant-free state-machine
  scenarios.
- `validate_care_architecture.py`, `test_validate_care_architecture.py`, and
  `test_interaction_core.mjs` enforce structure, semantics, safety boundaries,
  and executable transitions.

The earlier `synthetic_vocabulary_v0.js` is retained as a frozen superseded
reference. The current page loads only the v1 vocabulary architecture.

## Run locally

From the project root:

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory GrossTree/Basic/CareAAC
```

Then open `http://127.0.0.1:8765/`.

Run the static safety tests:

```bash
python3 GrossTree/Basic/CareAAC/validate_care_architecture.py check
python3 -m unittest discover \
  -s GrossTree/Basic/CareAAC -p 'test_*.py' -v
node --test GrossTree/Basic/CareAAC/test_interaction_core.mjs
```

## Research boundary

This is Lane B ordinary-care software, implemented and tested with generic
synthetic content under Lane A. Its interaction state, observations, phrases,
selections, timing, and outcomes must not be copied into NRLIS research,
training, evaluation, demonstration, or publication records. A later research
version requires the Human-ready checkpoint, an approved protocol, authorized
storage, and a new implementation/configuration version. Dialect and personal
vocabulary overlays remain unimplemented and unauthorized in this interface revision.
