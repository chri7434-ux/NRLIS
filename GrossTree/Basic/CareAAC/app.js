(function initializeCareAAC() {
  "use strict";

  const config = window.NRLIS_CARE_CONFIG;
  const core = window.NRLISCareCore;
  if (!config || !core) {
    throw new Error("Care AAC requires the frozen vocabulary and interaction core.");
  }
  const controller = core.createController(config);


  const icons = {
    speech: '<path d="M5 4.5h14a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-8l-5 3v-3H5a2 2 0 0 1-2-2v-9a2 2 0 0 1 2-2Z"/><path d="M7 9h10M7 13h6"/>',
    shield: '<path d="m12 3 7 3v5c0 4-3 7-7 10-4-3-7-6-7-10V6Z"/><path d="m8.5 11.5 2.5 2.5 4.5-5"/>',
    scan: '<path d="M8 3H5a2 2 0 0 0-2 2v3m13-5h3a2 2 0 0 1 2 2v3M3 16v3a2 2 0 0 0 2 2h3m8 0h3a2 2 0 0 0 2-2v-3M7 12h10"/><circle cx="12" cy="12" r="3"/>',
    hand: '<path d="M8 12V6a1.5 1.5 0 0 1 3 0v5-7a1.5 1.5 0 0 1 3 0v7-5a1.5 1.5 0 0 1 3 0v6-3a1.5 1.5 0 0 1 3 0v6c0 4-2 6-6 6h-1c-3 0-5-2-6-4l-3-4a1.6 1.6 0 0 1 2.5-2Z"/>',
    water: '<path d="M12 3c-2 4-6 7-6 11a6 6 0 0 0 12 0c0-4-4-7-6-11Z"/><path d="M9 14a3 3 0 0 0 3 3"/>',
    food: '<path d="M5 3v6m3-6v6m-6-6v6c0 2 6 2 6 0M5 11v10M17 3c-3 3-4 7-3 10h4M18 3v18"/>',
    moon: '<path d="M20 14A8.5 8.5 0 0 1 10 4a8.5 8.5 0 1 0 10 10Z"/>',
    bathroom: '<path d="M5 3h6v7H5zM5 10h14v2c0 4-4 6-8 6H8a3 3 0 0 1-3-3Zm6 8v3h6M7.5 6h1"/>',
    sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/>',
    heart: '<path d="M20 5c-3-3-6-1-8 1-2-2-5-4-8-1-3 4 1 8 8 14 7-6 11-10 8-14Z"/>',
    chevronLeft: '<path d="m14.5 5-7 7 7 7"/>',
    chevronRight: '<path d="m9.5 5 7 7-7 7"/>',
    chevronDown: '<path d="m6 9 6 6 6-6"/>',
    none: '<circle cx="12" cy="12" r="8"/><path d="m6.5 6.5 11 11"/>',
    repeat: '<path d="M20 8a8 8 0 0 0-14-3L3 8m0-5v5h5m-4 8a8 8 0 0 0 14 3l3-3m0 5v-5h-5"/>',
    close: '<path d="m6 6 12 12M18 6 6 18"/>',
    check: '<path d="m5 12 4.5 4.5L19 7"/>',
    board: '<rect x="3" y="4" width="18" height="16" rx="3"/><path d="M9 4v16m6-16v16M3 12h18"/>',
    keyboard: '<rect x="2" y="5" width="20" height="14" rx="3"/><path d="M6 9h.1m3.9 0h.1m3.9 0h.1m3.9 0h.1M6 12h.1m3.9 0h.1m3.9 0h.1m3.9 0h.1M7 15h10"/>',
    info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v6m0-10v.1"/>',
    shirt: '<path d="m8 3-5 4 3 4 2-2v12h8V9l2 2 3-4-5-4a4 4 0 0 1-8 0Z"/>',
    seat: '<path d="M7 3v10h11v5H7a3 3 0 0 1-3-3V9M7 18v3m10-3v3"/>',
    temperature: '<path d="M9 14V5a3 3 0 0 1 6 0v9a5 5 0 1 1-6 0Z"/><path d="M12 9v9m5-11h3m-3 4h3"/>',
    door: '<path d="M5 21V3h14v18M8 21V5l8-2v18M12 13h.1"/>',
    clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v6l4 2"/>',
    question: '<circle cx="12" cy="12" r="9"/><path d="M9 9a3 3 0 0 1 6 0c0 2-3 2-3 5m0 3v.1"/>',
    people: '<circle cx="9" cy="8" r="3"/><path d="M3 20v-2a6 6 0 0 1 12 0v2m1-15a3 3 0 0 1 0 6m2 3a5 5 0 0 1 3 4v2"/>',
    quiet: '<path d="m11 4-6 5H2v6h3l6 5Zm5 5 6 6m0-6-6 6"/>',
    television: '<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8m-4-4v4"/>',
    music: '<path d="M10 18V5l10-2v13M10 8l10-2"/><ellipse cx="7" cy="18" rx="3" ry="2.5"/><ellipse cx="17" cy="16" rx="3" ry="2.5"/>',
    photo: '<rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8" cy="8" r="1.5"/><path d="m3 17 5-5 4 4 4-7 5 6"/>',
    phone: '<rect x="6" y="2" width="12" height="20" rx="3"/><path d="M10 5h4m-3 14h2"/>',
    arrow: '<path d="M4 12h16m-6-6 6 6-6 6"/>',
    pause: '<path d="M8 5v14M16 5v14"/>',
    play: '<path d="m8 4 12 8-12 8Z"/>'
  };
  const compactContextLabels = { "basic-needs": "基本需要", comfort: "舒适环境", conversation: "交流回答", social: "陪伴活动", assistance: "帮助控制" };
  const contextIcons = { "basic-needs": "water", comfort: "sun", conversation: "speech", social: "heart", assistance: "hand" };
  const conceptIcons = {
    "need-water": "water", "need-food": "food", "need-rest": "moon", "need-toilet": "bathroom",
    "routine-wash": "water", "routine-mouth-care": "water", "routine-clothes": "shirt", "routine-sit-up": "seat",
    "comfort-unwell": "heart", "comfort-position": "seat", "comfort-cold": "temperature", "comfort-hot": "sun",
    "environment-light-on": "sun", "environment-light-off": "moon", "environment-door-open": "door", "environment-door-close": "door",
    "conversation-repeat": "repeat", "conversation-slower": "clock", "conversation-time": "clock", "conversation-dont-understand": "question",
    "response-yes": "check", "response-no": "close", "response-unsure": "question", "response-dont-know": "question",
    "social-stay": "people", "social-quiet": "quiet", "social-contact-family": "people", "social-thanks": "heart",
    "leisure-television": "television", "leisure-music": "music", "leisure-photos": "photo", "leisure-window": "sun",
    "assistance-closer": "arrow", "assistance-move-item": "arrow", "assistance-pass-item": "hand", "assistance-phone": "phone",
    "control-stop": "pause", "control-continue": "play", "control-wait": "clock", "control-finished": "check"
  };

  function createIcon(name) {
    const element = document.createElement("span");
    element.className = "ui-icon";
    element.setAttribute("aria-hidden", "true");
    // Only source-controlled paths enter this decorative markup; never phrase text.
    element.innerHTML = '<svg viewBox="0 0 24 24" focusable="false">' + (icons[name] || icons.speech) + '</svg>';
    return element;
  }

  document.querySelectorAll("[data-icon]").forEach((element) => {
    element.replaceChildren(createIcon(element.dataset.icon));
  });

  const scanState = {
    active: false,
    index: -1,
    timer: null
  };

  const elements = {
    contextGrid: document.getElementById("context-grid"),
    candidatePanel: document.getElementById("candidate-panel"),
    outputPanel: document.getElementById("output-panel"),
    outputBadge: document.getElementById("output-badge"),
    confirmationTitle: document.getElementById("confirmation-title"),
    scanToggles: Array.from(document.querySelectorAll("[data-scan-toggle]")),
    candidateGrid: document.getElementById("candidate-grid"),
    candidateDescription: document.getElementById("candidate-description"),
    panelPosition: document.getElementById("panel-position"),
    panelLabel: document.getElementById("panel-label"),
    panelCounter: document.getElementById("panel-counter"),
    previousPanelButton: document.getElementById("action-previous-panel"),
    nextPanelButton: document.getElementById("action-next-panel"),
    surfaceMode: document.getElementById("surface-mode"),
    confirmationPanel: document.getElementById("confirmation-panel"),
    pendingMessage: document.getElementById("pending-message"),
    confirmedMessage: document.getElementById("confirmed-message"),
    confirmButton: document.getElementById("confirm-button"),
    rejectButton: document.getElementById("reject-button"),
    noneButton: document.getElementById("action-none"),
    repeatButton: document.getElementById("action-repeat"),
    cancelButton: document.getElementById("action-cancel"),
    fallbackButton: document.getElementById("action-fallback"),
    scanToggle: document.getElementById("scan-toggle"),
    scanSpeed: document.getElementById("scan-speed"),
    statusMessage: document.getElementById("status-message")
  };

  function setStatus(message) {
    elements.statusMessage.textContent = message;
  }

  function clearScanFocus() {
    document.querySelectorAll(".scan-focus").forEach((element) => {
      element.classList.remove("scan-focus");
    });
  }

  function actionableButtons() {
    if (!elements.confirmationPanel.hidden) {
      return Array.from(
        elements.confirmationPanel.querySelectorAll("button[data-control-id]:not([disabled])")
      );
    }
    const state = controller.getState();
    const selector = state.contextId
      ? "#candidate-grid button:not([disabled]), .panel-navigation button:not([disabled]), " +
        ".always-controls button:not([disabled])"
      : "#context-grid button:not([disabled]), .always-controls button:not([disabled])";
    return Array.from(document.querySelectorAll(selector));
  }

  function focusControl(controlId) {
    clearScanFocus();
    const scope = elements.confirmationPanel.open ? elements.confirmationPanel : document;
    const button = Array.from(
      scope.querySelectorAll("[data-control-id]")
    ).find((candidate) => candidate.dataset.controlId === controlId);
    if (!button || button.disabled || button.closest("[hidden]")) {
      return false;
    }
    button.classList.add("scan-focus");
    button.focus({ preventScroll: false });
    return true;
  }

  function stopScanning(message) {
    if (scanState.timer !== null) {
      window.clearInterval(scanState.timer);
    }
    scanState.timer = null;
    scanState.active = false;
    scanState.index = -1;
    elements.scanToggles.forEach((button) => {
      button.querySelector(".scan-label").textContent = "开始扫描";
      button.setAttribute("aria-pressed", "false");
    });
    clearScanFocus();
    if (message) {
      setStatus(message);
    }
  }

  function scanStep() {
    const buttons = actionableButtons();
    if (buttons.length === 0) {
      stopScanning("当前没有可扫描的控制。");
      return;
    }
    scanState.index = (scanState.index + 1) % buttons.length;
    clearScanFocus();
    buttons[scanState.index].classList.add("scan-focus");
    buttons[scanState.index].focus({ preventScroll: false });
  }

  function startScanning() {
    stopScanning();
    const delay = Number(elements.scanSpeed.value);
    scanState.active = true;
    elements.scanToggles.forEach((button) => {
      button.querySelector(".scan-label").textContent = "停止扫描";
      button.setAttribute("aria-pressed", "true");
    });
    setStatus("扫描已开始。按一次空格，选择高亮项。");
    scanStep();
    scanState.timer = window.setInterval(scanStep, delay);
  }

  function toggleScanning() {
    if (scanState.active) {
      stopScanning("自动扫描已停止；没有保存扫描记录。");
    } else {
      startScanning();
    }
  }

  function renderContexts() {
    const state = controller.getState();
    if (elements.contextGrid.childElementCount === 0) {
      config.contexts.forEach((context) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "context-button";
        button.dataset.contextId = context.id;
        button.dataset.controlId = `context:${context.id}`;
        button.setAttribute("aria-label", `${context.label} ${context.hint}`);
        const symbol = document.createElement("span");
        symbol.className = "context-icon";
        symbol.append(createIcon(contextIcons[context.id]));
        const copy = document.createElement("span");
        copy.className = "context-copy";
        const label = document.createElement("strong");
        label.textContent = context.label;
        label.className = "context-label";
        const compactLabel = document.createElement("strong");
        compactLabel.className = "context-label-compact";
        compactLabel.textContent = compactContextLabels[context.id];
        const hint = document.createElement("span");
        hint.className = "context-hint";
        hint.textContent = context.hint;
        copy.append(label, compactLabel, hint);
        button.append(symbol, copy);
        button.addEventListener("click", () => selectContext(context.id));
        elements.contextGrid.append(button);
      });
    }
    elements.contextGrid.querySelectorAll("button").forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.contextId === state.contextId));
    });
  }

  function renderCandidates() {
    const state = controller.getState();
    const context = controller.getContext(state.contextId);
    const panel = controller.getCurrentPanel();
    elements.candidateGrid.replaceChildren();
    elements.candidateGrid.dataset.surface = state.surfaceMode;

    if (!context || !panel) {
      elements.candidateDescription.textContent = "每次只看四个选项，慢慢选。";
      elements.panelPosition.textContent = "第 2 步 · 选择短句";
      elements.panelLabel.textContent = "从一个情境开始";
      elements.panelCounter.textContent = "— / —";
      elements.previousPanelButton.disabled = true;
      elements.nextPanelButton.disabled = true;
      const placeholder = document.createElement("div");
      placeholder.className = "candidate-placeholder";
      const illustration = document.createElement("span");
      illustration.className = "empty-illustration";
      illustration.append(createIcon("speech"));
      const title = document.createElement("strong");
      title.textContent = "先选一个情境";
      const hint = document.createElement("p");
      hint.textContent = "从基本需要、感受或交流开始。合适的话，会出现在这里。";
      placeholder.append(illustration, title, hint);
      elements.candidateGrid.append(placeholder);
      return;
    }

    elements.candidateDescription.textContent = "轻点一个短句，再由你确认。";
    elements.panelPosition.textContent = `${context.label} · 第 ${state.panelIndex + 1} 组`;
    elements.panelLabel.textContent = panel.label;
    elements.panelCounter.textContent = `${state.panelIndex + 1} / ${state.panelCount}`;
    elements.previousPanelButton.disabled = false;
    elements.nextPanelButton.disabled = false;

    controller.getVisibleConcepts().forEach((concept, index) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "candidate-button";
      button.dataset.conceptId = concept.id;
      button.dataset.controlId = `concept:${concept.id}`;
      const renderedText = controller.conceptText(concept.id);
      button.setAttribute("aria-label", `${index + 1}，${renderedText}`);

      const shortcut = document.createElement("span");
      shortcut.className = "shortcut";
      shortcut.textContent = String(index + 1);
      const symbol = document.createElement("span");
      symbol.className = "candidate-symbol";
      symbol.append(createIcon(conceptIcons[concept.id]));
      const text = document.createElement("span");
      text.className = "candidate-text";
      text.textContent = renderedText;
      button.append(shortcut, symbol, text);
      button.addEventListener("click", () => proposeConcept(concept.id));
      elements.candidateGrid.append(button);
    });
  }

  function renderPending() {
    const state = controller.getState();
    if (!state.pendingConceptId) {
      if (elements.confirmationPanel.open) elements.confirmationPanel.close();
      elements.pendingMessage.textContent = "";
      elements.confirmationPanel.hidden = true;
      return;
    }
    elements.pendingMessage.textContent = state.pendingText;
    elements.confirmationPanel.hidden = false;
    if (!elements.confirmationPanel.open) {
      elements.confirmationPanel.showModal();
      // Focus the question, never make an affirmative action the default.
      elements.confirmationTitle.focus({ preventScroll: true });
    }
  }

  function renderOutput() {
    const state = controller.getState();
    const kind = state.confirmedText ? "confirmed" : state.fallbackActive ? "fallback" : "empty";
    elements.outputPanel.dataset.state = kind;
    elements.outputBadge.textContent = kind === "confirmed" ? "已确认" : kind === "fallback" ? "切换沟通方式" : "等待确认";
    if (state.confirmedText) {
      elements.confirmedMessage.textContent = state.confirmedText;
    } else if (state.fallbackActive) {
      elements.confirmedMessage.textContent = "请使用非AI沟通板或直接确认方式";
    } else {
      elements.confirmedMessage.textContent = "尚未确认任何消息";
    }
  }

  function renderAll() {
    renderContexts();
    renderCandidates();
    renderPending();
    renderOutput();
  }

  function selectContext(contextId) {
    stopScanning();
    const state = controller.selectContext(contextId);
    if (state.statusCode === "invalid_context") {
      return false;
    }
    renderAll();
    const context = controller.getContext(contextId);
    setStatus(`已打开${context.label}。选一句想说的话。`);
    return true;
  }

  function movePanel(direction) {
    stopScanning();
    const state = direction > 0 ? controller.nextPanel() : controller.previousPanel();
    if (!state.contextId) {
      setStatus("请先选择情境，再切换候选小组。");
      return false;
    }
    renderCandidates();
    renderPending();
    setStatus(`已换到第 ${state.panelIndex + 1} 组。请选择合适的短句。`);
    elements.candidateGrid.querySelector("button")?.focus();
    return true;
  }

  function proposeConcept(conceptId) {
    const resumeScan = scanState.active;
    stopScanning();
    const state = controller.proposeConcept(conceptId);
    if (state.statusCode !== "candidate_pending") {
      setStatus("这个候选不在当前小组中，未进入确认。");
      return false;
    }
    renderPending();
    setStatus("这句话还未确认。请确认，或选择“不是这个”。");
    if (resumeScan) startScanning();
    return true;
  }

  function confirmPending() {
    stopScanning();
    const state = controller.confirmPending();
    if (state.statusCode !== "message_confirmed") {
      setStatus("当前没有等待确认的候选。");
      return false;
    }
    renderPending();
    renderOutput();
    setStatus("已确认。这句话现在显示在“当前消息”中。");
    elements.outputPanel.focus({ preventScroll: true });
    elements.outputPanel.scrollIntoView({
      behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth",
      block: "nearest"
    });
    return true;
  }

  function rejectPending() {
    stopScanning();
    const previousConcept = controller.getState().pendingConceptId;
    controller.rejectPending();
    renderPending();
    setStatus("没关系。选另一句，或者选择“都不是”。");
    Array.from(elements.candidateGrid.querySelectorAll("button"))
      .find((button) => button.dataset.conceptId === previousConcept)?.focus({ preventScroll: true });
  }

  function noCandidateMatches() {
    stopScanning();
    controller.noCandidateMatches();
    renderPending();
    setStatus("都不合适？看看下一组，或换用非AI沟通板。");
    elements.nextPanelButton.disabled
      ? elements.fallbackButton.focus()
      : elements.nextPanelButton.focus();
  }

  function repeatCandidates() {
    stopScanning();
    const state = controller.repeatPanel();
    if (state.statusCode === "context_required") {
      setStatus("请先选择情境，再重复候选。");
      elements.contextGrid.querySelector("button")?.focus();
      return;
    }
    renderCandidates();
    renderPending();
    setStatus("还是刚才这四句。可以再看一次。");
    elements.candidateGrid.querySelector("button")?.focus();
  }

  function cancelAll() {
    stopScanning();
    controller.cancelAll();
    renderAll();
    setStatus("已取消。这一页已经清空，可以重新开始。");
    elements.contextGrid.querySelector("button")?.focus();
  }

  function useFallback() {
    stopScanning();
    controller.useFallback();
    renderAll();
    setStatus("候选流程已停止。当前提示不是替使用者生成的消息。");
    elements.fallbackButton.focus();
  }

  function changeSurfaceMode() {
    stopScanning();
    const state = controller.setSurfaceMode(elements.surfaceMode.value);
    renderCandidates();
    renderPending();
    const label = state.surfaceMode === "compact" ? "大字短句" : "完整句";
    setStatus(`已切换为${label}。意思保持不变。`);
  }

  function activateControl(controlId) {
    if (typeof controlId !== "string") {
      return false;
    }
    if (elements.confirmationPanel.open && ![
      "action-confirm", "action-reject", "action-none", "action-repeat", "action-cancel", "action-fallback"
    ].includes(controlId)) return false;
    if (controlId.startsWith("context:")) {
      return selectContext(controlId.slice("context:".length));
    }
    if (controlId.startsWith("concept:")) {
      return proposeConcept(controlId.slice("concept:".length));
    }
    const actions = {
      "action-none": noCandidateMatches,
      "action-repeat": repeatCandidates,
      "action-cancel": cancelAll,
      "action-fallback": useFallback,
      "action-previous-panel": () => movePanel(-1),
      "action-next-panel": () => movePanel(1),
      "action-confirm": confirmPending,
      "action-reject": rejectPending
    };
    if (!actions[controlId]) {
      return false;
    }
    actions[controlId]();
    return true;
  }

  function normalizeLegacyChoiceId(choiceId) {
    if (controller.getConcept(choiceId)) {
      return `concept:${choiceId}`;
    }
    return choiceId;
  }

  function handleKeyboard(event) {
    if (event.key === "Escape") {
      event.preventDefault();
      cancelAll();
      return;
    }
    if (event.key === "Tab" && elements.confirmationPanel.open) {
      const buttons = Array.from(elements.confirmationPanel.querySelectorAll("button:not([disabled])"));
      const first = buttons[0];
      const last = buttons[buttons.length - 1];
      const active = document.activeElement;
      if (event.shiftKey && (active === first || active === elements.confirmationTitle || !elements.confirmationPanel.contains(active))) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && (active === last || !elements.confirmationPanel.contains(active))) {
        event.preventDefault();
        first.focus();
      }
      return;
    }
    if (event.repeat && (event.key === "Enter" || event.key === " " || /^[1-4]$/.test(event.key))) {
      event.preventDefault();
      return;
    }
    if (event.target instanceof Element && event.target.closest("select, summary")) return;
    if (event.key === " " && scanState.active) {
      event.preventDefault();
      const focused = document.querySelector(".scan-focus");
      if (focused instanceof HTMLButtonElement) {
        focused.click();
      }
      return;
    }
    if (/^[1-4]$/.test(event.key) && elements.confirmationPanel.hidden) {
      const buttons = elements.candidateGrid.querySelectorAll("button");
      const index = Number(event.key) - 1;
      if (buttons[index]) {
        event.preventDefault();
        buttons[index].click();
      }
    }
  }

  elements.confirmButton.addEventListener("click", confirmPending);
  elements.rejectButton.addEventListener("click", rejectPending);
  elements.noneButton.addEventListener("click", noCandidateMatches);
  elements.repeatButton.addEventListener("click", repeatCandidates);
  elements.cancelButton.addEventListener("click", cancelAll);
  elements.fallbackButton.addEventListener("click", useFallback);
  elements.previousPanelButton.addEventListener("click", () => movePanel(-1));
  elements.nextPanelButton.addEventListener("click", () => movePanel(1));
  elements.surfaceMode.addEventListener("change", changeSurfaceMode);
  elements.scanToggles.forEach((button) => button.addEventListener("click", toggleScanning));
  const dialogActions = { none: noCandidateMatches, repeat: repeatCandidates, cancel: cancelAll, fallback: useFallback };
  elements.confirmationPanel.querySelectorAll("[data-dialog-action]").forEach((button) => {
    button.addEventListener("click", dialogActions[button.dataset.dialogAction]);
  });
  elements.confirmationPanel.addEventListener("cancel", (event) => {
    event.preventDefault();
    cancelAll();
  });
  elements.scanSpeed.addEventListener("change", () => {
    if (scanState.active) {
      startScanning();
    }
  });
  document.addEventListener("keydown", handleKeyboard);

  window.addEventListener("nrlis-access-focus", (event) => {
    const controlId =
      event.detail?.controlId || normalizeLegacyChoiceId(event.detail?.choiceId);
    focusControl(controlId);
  });
  window.addEventListener("nrlis-access-activate", (event) => {
    const controlId =
      event.detail?.controlId || normalizeLegacyChoiceId(event.detail?.choiceId);
    activateControl(controlId);
  });

  window.NRLISCareAAC = Object.freeze({
    version: config.version,
    uiVersion: "0.3.0",
    architectureVersion: config.architectureVersion,
    focusControl,
    activateControl,
    focusChoice: (choiceId) => focusControl(normalizeLegacyChoiceId(choiceId)),
    activateChoice: (choiceId) =>
      activateControl(normalizeLegacyChoiceId(choiceId)),
    cancel: cancelAll,
    getState: () =>
      Object.freeze({
        ...controller.getState(),
        scanning: scanState.active
      })
  });

  renderAll();
})();
