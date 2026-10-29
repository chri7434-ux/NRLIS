(function attachCareInteractionCore(globalObject, factory) {
  "use strict";

  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  }
  if (globalObject) {
    globalObject.NRLISCareCore = api;
  }
})(typeof window === "object" ? window : globalThis, function buildCore() {
  "use strict";

  function freezeSnapshot(value) {
    Object.freeze(value);
    Object.values(value).forEach((child) => {
      if (child && typeof child === "object" && !Object.isFrozen(child)) {
        freezeSnapshot(child);
      }
    });
    return value;
  }

  function createController(config) {
    if (
      !config ||
      config.version !== "0.2.0" ||
      config.mode !== "care_nonresearch" ||
      config.dataClassification !== "synthetic_no_participant_data" ||
      config.safetyPolicy?.confirmationRequired !== true ||
      config.safetyPolicy?.autoConfirmation !== false ||
      config.outputMode !== "confirmed_visual_only"
    ) {
      throw new Error("Care interaction core requires the frozen WP2.2 contract.");
    }

    const contextById = new Map(config.contexts.map((item) => [item.id, item]));
    const conceptById = new Map(config.concepts.map((item) => [item.id, item]));

    const state = {
      contextId: null,
      panelIndex: 0,
      surfaceMode: config.defaultSurfaceMode,
      pendingConceptId: null,
      confirmedConceptId: null,
      confirmedText: null,
      fallbackActive: false,
      statusCode: "ready"
    };

    function currentContext() {
      return contextById.get(state.contextId) || null;
    }

    function currentPanel() {
      const context = currentContext();
      return context?.panels[state.panelIndex] || null;
    }

    function currentConceptIds() {
      return currentPanel()?.conceptIds.slice() || [];
    }

    function conceptText(conceptId, surfaceMode = state.surfaceMode) {
      const concept = conceptById.get(conceptId);
      if (!concept) {
        return null;
      }
      return surfaceMode === "compact"
        ? concept.compactText
        : concept.canonicalText;
    }

    function snapshot() {
      const context = currentContext();
      const panel = currentPanel();
      return freezeSnapshot({
        version: config.version,
        architectureVersion: config.architectureVersion,
        mode: config.mode,
        contextId: state.contextId,
        panelId: panel?.id || null,
        panelIndex: state.panelIndex,
        panelCount: context?.panels.length || 0,
        surfaceMode: state.surfaceMode,
        visibleConceptIds: currentConceptIds(),
        pendingConceptId: state.pendingConceptId,
        pendingText: conceptText(state.pendingConceptId),
        confirmedConceptId: state.confirmedConceptId,
        confirmedText: state.confirmedText,
        confirmed: state.confirmedConceptId !== null,
        fallbackActive: state.fallbackActive,
        statusCode: state.statusCode,
        recording: false,
        persistence: false,
        interactionHistory: null
      });
    }

    function clearPending() {
      state.pendingConceptId = null;
    }

    function selectContext(contextId) {
      if (!contextById.has(contextId)) {
        state.statusCode = "invalid_context";
        return snapshot();
      }
      state.contextId = contextId;
      state.panelIndex = 0;
      state.fallbackActive = false;
      clearPending();
      state.statusCode = "context_selected";
      return snapshot();
    }

    function movePanel(offset) {
      const context = currentContext();
      if (!context) {
        state.statusCode = "context_required";
        return snapshot();
      }
      const count = context.panels.length;
      state.panelIndex = (state.panelIndex + offset + count) % count;
      clearPending();
      state.statusCode = offset > 0 ? "next_panel" : "previous_panel";
      return snapshot();
    }

    function proposeConcept(conceptId) {
      if (!currentConceptIds().includes(conceptId)) {
        state.statusCode = "concept_not_visible";
        return snapshot();
      }
      state.pendingConceptId = conceptId;
      state.fallbackActive = false;
      state.statusCode = "candidate_pending";
      return snapshot();
    }

    function confirmPending() {
      if (!state.pendingConceptId) {
        state.statusCode = "nothing_to_confirm";
        return snapshot();
      }
      state.confirmedConceptId = state.pendingConceptId;
      state.confirmedText = conceptText(state.pendingConceptId);
      clearPending();
      state.statusCode = "message_confirmed";
      return snapshot();
    }

    function rejectPending() {
      clearPending();
      state.statusCode = "candidate_rejected";
      return snapshot();
    }

    function noCandidateMatches() {
      clearPending();
      state.statusCode = "no_candidate_matches";
      return snapshot();
    }

    function repeatPanel() {
      clearPending();
      state.statusCode = currentPanel() ? "panel_repeated" : "context_required";
      return snapshot();
    }

    function useFallback() {
      state.contextId = null;
      state.panelIndex = 0;
      clearPending();
      state.confirmedConceptId = null;
      state.confirmedText = null;
      state.fallbackActive = true;
      state.statusCode = "fallback_active";
      return snapshot();
    }

    function cancelAll() {
      state.contextId = null;
      state.panelIndex = 0;
      clearPending();
      state.confirmedConceptId = null;
      state.confirmedText = null;
      state.fallbackActive = false;
      state.statusCode = "cancelled";
      return snapshot();
    }

    function setSurfaceMode(surfaceMode) {
      if (!config.surfaceModes.includes(surfaceMode)) {
        state.statusCode = "invalid_surface_mode";
        return snapshot();
      }
      state.surfaceMode = surfaceMode;
      state.statusCode = "surface_mode_changed";
      return snapshot();
    }

    function dispatch(action) {
      if (!action || typeof action.type !== "string") {
        state.statusCode = "invalid_action";
        return snapshot();
      }
      const actions = {
        SELECT_CONTEXT: () => selectContext(action.contextId),
        NEXT_PANEL: () => movePanel(1),
        PREVIOUS_PANEL: () => movePanel(-1),
        PROPOSE: () => proposeConcept(action.conceptId),
        CONFIRM: confirmPending,
        REJECT: rejectPending,
        NONE: noCandidateMatches,
        REPEAT: repeatPanel,
        FALLBACK: useFallback,
        CANCEL: cancelAll,
        SET_SURFACE: () => setSurfaceMode(action.surfaceMode)
      };
      if (!actions[action.type]) {
        state.statusCode = "invalid_action";
        return snapshot();
      }
      return actions[action.type]();
    }

    return Object.freeze({
      getState: snapshot,
      getConcept: (conceptId) => conceptById.get(conceptId) || null,
      getContext: (contextId) => contextById.get(contextId) || null,
      getCurrentPanel: currentPanel,
      getVisibleConcepts: () =>
        currentConceptIds().map((conceptId) => conceptById.get(conceptId)),
      conceptText,
      dispatch,
      selectContext,
      nextPanel: () => movePanel(1),
      previousPanel: () => movePanel(-1),
      proposeConcept,
      confirmPending,
      rejectPending,
      noCandidateMatches,
      repeatPanel,
      useFallback,
      cancelAll,
      setSurfaceMode
    });
  }

  return Object.freeze({
    version: "1.0.0",
    createController
  });
});
