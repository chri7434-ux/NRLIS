#!/usr/bin/env python3
"""Static safety and contract tests for Care-mode AAC synthetic MVP v0.2."""

from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
APP = ROOT / "app.js"
CORE = ROOT / "interaction_core.js"
VOCABULARY = ROOT / "synthetic_vocabulary_v1.js"
STYLES = ROOT / "styles.css"


class PageInventory(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.scripts: list[str] = []
        self.stylesheets: list[str] = []
        self.csp = ""
        self.tags: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        attributes = dict(attrs)
        self.tags.append(tag)
        if "id" in attributes:
            self.ids.add(attributes["id"])
        if tag == "script" and attributes.get("src"):
            self.scripts.append(attributes["src"])
        if tag == "link" and attributes.get("rel") == "stylesheet":
            self.stylesheets.append(attributes.get("href", ""))
        if (
            tag == "meta"
            and attributes.get("http-equiv", "").lower()
            == "content-security-policy"
        ):
            self.csp = attributes.get("content", "")


def load_config() -> dict:
    program = """
const fs = require('fs');
const vm = require('vm');
const sandbox = { window: {} };
vm.createContext(sandbox);
vm.runInContext(fs.readFileSync(process.argv[1], 'utf8'), sandbox);
process.stdout.write(JSON.stringify(sandbox.window.NRLIS_CARE_CONFIG));
"""
    result = subprocess.run(
        ["node", "-e", program, str(VOCABULARY)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout)


class CareAACStaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = INDEX.read_text(encoding="utf-8")
        cls.app = APP.read_text(encoding="utf-8")
        cls.core = CORE.read_text(encoding="utf-8")
        cls.vocabulary = VOCABULARY.read_text(encoding="utf-8")
        cls.styles = STYLES.read_text(encoding="utf-8")
        cls.page = PageInventory()
        cls.page.feed(cls.html)
        cls.config = load_config()

    def test_local_assets_and_content_security_policy(self) -> None:
        self.assertEqual(
            self.page.scripts,
            ["synthetic_vocabulary_v1.js", "interaction_core.js", "app.js"],
        )
        self.assertEqual(self.page.stylesheets, ["styles.css"])
        self.assertIn("connect-src 'none'", self.page.csp)
        self.assertIn("media-src 'none'", self.page.csp)
        self.assertIn("object-src 'none'", self.page.csp)

    def test_no_capture_persistence_or_exfiltration_api(self) -> None:
        combined = "\n".join(
            (self.html, self.app, self.core, self.vocabulary, self.styles)
        )
        forbidden = (
            "fetch(",
            "XMLHttpRequest",
            "WebSocket",
            "sendBeacon",
            "localStorage",
            "sessionStorage",
            "indexedDB",
            "getUserMedia",
            "MediaRecorder",
            "speechSynthesis",
            "serviceWorker",
            "http://",
            "https://",
        )
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, combined)

    def test_page_has_no_media_upload_or_form_surface(self) -> None:
        self.assertNotIn("audio", self.page.tags)
        self.assertNotIn("video", self.page.tags)
        self.assertNotIn("form", self.page.tags)
        self.assertNotIn("input", self.page.tags)

    def test_config_is_synthetic_nonresearch_and_no_data(self) -> None:
        self.assertEqual(self.config["version"], "0.2.0")
        self.assertEqual(self.config["architectureVersion"], "1.0.0")
        self.assertEqual(self.config["mode"], "care_nonresearch")
        self.assertEqual(
            self.config["dataClassification"],
            "synthetic_no_participant_data",
        )
        for key in (
            "recording",
            "persistence",
            "logging",
            "externalNetwork",
            "modelInference",
        ):
            self.assertIs(self.config[key], False)
        self.assertEqual(self.config["outputMode"], "confirmed_visual_only")
        self.assertEqual(self.config["personalization"], "none")
        self.assertEqual(self.config["dialectClaim"], "none")

    def test_candidate_and_context_ids_are_unique(self) -> None:
        contexts = self.config["contexts"]
        context_ids = [item["id"] for item in contexts]
        candidate_ids = [candidate["id"] for candidate in self.config["concepts"]]
        referenced_ids = [
            concept_id
            for context in contexts
            for panel in context["panels"]
            for concept_id in panel["conceptIds"]
        ]
        self.assertEqual(len(context_ids), len(set(context_ids)))
        self.assertEqual(len(candidate_ids), len(set(candidate_ids)))
        self.assertEqual(len(contexts), 5)
        self.assertEqual(len(candidate_ids), 40)
        self.assertEqual(set(referenced_ids), set(candidate_ids))
        self.assertTrue(
            all(
                len(panel["conceptIds"]) == 4
                for context in contexts
                for panel in context["panels"]
            )
        )

    def test_all_required_safety_controls_are_present(self) -> None:
        required = {
            "action-none",
            "action-repeat",
            "action-cancel",
            "action-fallback",
            "action-previous-panel",
            "action-next-panel",
        }
        self.assertEqual(set(self.config["globalActions"]), required)
        self.assertTrue(required <= self.page.ids)
        self.assertIn("confirm-button", self.page.ids)
        self.assertIn("reject-button", self.page.ids)
        self.assertIn("surface-mode", self.page.ids)

    def test_confirmation_and_cancel_are_explicit_in_code(self) -> None:
        self.assertIn("function confirmPending()", self.app)
        self.assertIn("function rejectPending()", self.app)
        self.assertIn("function cancelAll()", self.app)
        self.assertIn("elements.confirmButton.addEventListener", self.app)
        self.assertIn("elements.cancelButton.addEventListener", self.app)
        self.assertIn("confirmationRequired !== true", self.core)
        self.assertIn("autoConfirmation !== false", self.core)
        self.assertIn("confirmPending", self.core)

    def test_future_access_adapter_is_bounded(self) -> None:
        self.assertIn('"nrlis-access-focus"', self.app)
        self.assertIn('"nrlis-access-activate"', self.app)
        self.assertIn("focusControl", self.app)
        self.assertIn("activateControl", self.app)
        self.assertIn("interactionHistory: null", self.core)

    def test_v02_loads_core_and_not_superseded_vocabulary(self) -> None:
        self.assertIn("interaction_core.js", self.page.scripts)
        self.assertNotIn("synthetic_vocabulary_v0.js", self.page.scripts)
        self.assertIn("40 条 synthetic 通用短句", self.html)

    def test_no_emergency_or_autonomous_claim(self) -> None:
        self.assertIn("不能用于紧急或重要医疗决定", self.html)
        self.assertIn("候选只是建议", self.html)
        self.assertIn("请由使用者确认", self.html)
        self.assertIn("无录音", self.html)
        self.assertIn("无上传", self.html)
        self.assertIn("无保存", self.html)


if __name__ == "__main__":
    unittest.main()
