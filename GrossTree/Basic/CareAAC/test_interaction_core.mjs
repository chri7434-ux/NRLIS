import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import vm from "node:vm";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";


const here = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const core = require(path.join(here, "interaction_core.js"));

function loadVocabulary() {
  const sandbox = { window: {} };
  vm.createContext(sandbox);
  vm.runInContext(
    fs.readFileSync(path.join(here, "synthetic_vocabulary_v1.js"), "utf8"),
    sandbox
  );
  return sandbox.window.NRLIS_CARE_CONFIG;
}

const config = loadVocabulary();
const suite = JSON.parse(
  fs.readFileSync(path.join(here, "synthetic_interactions_v1.json"), "utf8")
);

test("all declarative synthetic interactions satisfy expected state", () => {
  for (const scenario of suite.scenarios) {
    const controller = core.createController(config);
    for (const [index, step] of scenario.steps.entries()) {
      const { expect, action: type, ...parameters } = step;
      const state = controller.dispatch({ type, ...parameters });
      for (const [key, expected] of Object.entries(expect)) {
        assert.deepEqual(
          state[key],
          expected,
          `${scenario.id} step ${index} expected ${key}`
        );
      }
    }
  }
});

test("confirmation is the only route to output", () => {
  const controller = core.createController(config);
  assert.equal(controller.confirmPending().confirmed, false);
  assert.equal(controller.confirmPending().confirmedText, null);

  controller.selectContext("basic-needs");
  assert.equal(controller.proposeConcept("need-water").confirmedText, null);
  assert.equal(controller.repeatPanel().confirmedText, null);
  controller.proposeConcept("need-water");
  assert.equal(controller.rejectPending().confirmedText, null);
  controller.proposeConcept("need-water");
  const confirmed = controller.confirmPending();
  assert.equal(confirmed.confirmedConceptId, "need-water");
  assert.equal(confirmed.confirmedText, "我想喝水");
});

test("a concept outside the visible panel cannot become pending", () => {
  const controller = core.createController(config);
  controller.selectContext("basic-needs");
  const state = controller.proposeConcept("control-stop");
  assert.equal(state.statusCode, "concept_not_visible");
  assert.equal(state.pendingConceptId, null);
  assert.equal(state.confirmed, false);
});

test("panel navigation is deterministic, wraps, and clears pending state", () => {
  const controller = core.createController(config);
  controller.selectContext("comfort");
  controller.proposeConcept("comfort-cold");
  assert.equal(controller.nextPanel().panelId, "comfort-environment");
  assert.equal(controller.getState().pendingConceptId, null);
  assert.equal(controller.nextPanel().panelId, "comfort-body");
  assert.equal(controller.previousPanel().panelId, "comfort-environment");
});

test("compact mode changes rendering without changing semantic identity", () => {
  const controller = core.createController(config);
  controller.selectContext("basic-needs");
  controller.setSurfaceMode("compact");
  const pending = controller.proposeConcept("need-water");
  assert.equal(pending.pendingConceptId, "need-water");
  assert.equal(pending.pendingText, "喝水");
  const confirmed = controller.confirmPending();
  assert.equal(confirmed.confirmedConceptId, "need-water");
  assert.equal(confirmed.confirmedText, "喝水");
});

test("fallback and cancel clear user-message state", () => {
  const controller = core.createController(config);
  controller.selectContext("conversation");
  controller.proposeConcept("conversation-time");
  controller.confirmPending();
  const fallback = controller.useFallback();
  assert.equal(fallback.contextId, null);
  assert.equal(fallback.confirmedText, null);
  assert.equal(fallback.fallbackActive, true);
  const cancelled = controller.cancelAll();
  assert.equal(cancelled.confirmedText, null);
  assert.equal(cancelled.fallbackActive, false);
});

test("public state is immutable and contains no interaction history", () => {
  const controller = core.createController(config);
  const state = controller.getState();
  assert.equal(Object.isFrozen(state), true);
  assert.equal(Object.isFrozen(state.visibleConceptIds), true);
  assert.equal(state.interactionHistory, null);
  assert.equal(state.recording, false);
  assert.equal(state.persistence, false);
});
