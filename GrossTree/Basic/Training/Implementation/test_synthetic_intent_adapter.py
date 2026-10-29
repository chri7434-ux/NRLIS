#!/usr/bin/env python3
"""WP2.3 acceptance tests for exact meaning, calibration isolation and no output."""

from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import synthetic_intent_adapter as adapter


class SyntheticIntentAdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = adapter.SyntheticIntentAdapter()
        cls.artifact, cls.report = cls.engine.build_artifacts()

    def route(self, values, context="basic-needs", panel="basic-essential"):
        return self.engine.route(self.engine._packet(values), context, panel)

    def test_exact_mapping_preserves_full_probability(self):
        decision = self.route([0.7, 0.15, 0.1, 0.05])
        self.assertEqual(decision["candidates"], [{"concept_id": "need-water", "probability": 0.7}])
        decision = self.route([0.1, 0.1, 0.7, 0.1], "comfort", "comfort-body")
        self.assertEqual(decision["candidates"][0]["concept_id"], "comfort-position")

    def test_pain_and_other_abstain_without_semantic_substitution(self):
        for values in ([0.01, 0.97, 0.01, 0.01], [0.01, 0.01, 0.01, 0.97]):
            with self.subTest(values=values):
                decision = self.route(values, "comfort", "comfort-body")
                self.assertEqual(decision["reason"], "unmapped_top_class")
                self.assertEqual(decision["candidates"], [])

    def test_excluded_top_class_cannot_promote_a_low_probability_alternative(self):
        decision = self.route([0.2, 0.01, 0.78, 0.01])
        self.assertEqual(decision["reason"], "top_outside_panel")
        self.assertEqual(decision["candidates"], [])

    def test_low_confidence_and_ties_abstain_without_renormalizing(self):
        for values in ([0.4, 0.3, 0.2, 0.1], [0.5, 0.5, 0.0, 0.0]):
            decision = self.route(values)
            self.assertEqual(decision["reason"], "below_probability")
            self.assertEqual(decision["candidates"], [])
        self.assertEqual(self.route([0.65, 0.35, 0.0, 0.0])["decision"], "candidates")

    def test_all_other_panels_abstain(self):
        for context in self.engine._vocabulary["contexts"]:
            for panel in context["panels"]:
                if panel["id"] == "basic-essential":
                    continue
                decision = self.route([0.97, 0.01, 0.01, 0.01], context["id"], panel["id"])
                self.assertEqual(decision["reason"], "top_outside_panel")

    def test_unknown_or_mismatched_context_is_rejected(self):
        for context, panel in (("missing", "basic-essential"), ("basic-needs", "comfort-body"), (None, "basic-essential")):
            with self.assertRaises(adapter.AdapterError):
                self.route([0.7, 0.1, 0.1, 0.1], context, panel)

    def test_invalid_probability_vectors_fail_closed(self):
        for values in ([1, 0, 0], [1, 0, 0, 0, 0], [0, 0, 0, 0], [0.7, 0.2, 0.2, 0.1],
                       [-0.1, 0.5, 0.3, 0.3], [True, 0, 0, 0], [float("nan"), 0, 0, 0],
                       [float("inf"), 0, 0, 0], ["0.7", 0.1, 0.1, 0.1]):
            with self.subTest(values=values), self.assertRaises(adapter.AdapterError):
                self.route(values)

    def test_label_order_unknown_classes_and_stale_provenance_are_rejected(self):
        for key, value in (("labels", list(reversed(self.engine._source["labels"]))),
                           ("labels", ["unknown"] * 4),
                           ("source_config_sha256", "0" * 64),
                           ("vocabulary_sha256", "0" * 64),
                           ("calibration_sha256", "0" * 64)):
            packet = self.engine._packet([0.7, 0.1, 0.1, 0.1])
            packet[key] = value
            with self.subTest(key=key), self.assertRaises(adapter.AdapterError):
                self.engine.route(packet, "basic-needs", "basic-essential")

    def test_content_reference_identity_and_permission_fields_are_rejected(self):
        for key in ("participant_id", "audio", "transcript", "reference_label", "care_event",
                    "free_text", "confirmation", "output_action", "temperature"):
            packet = self.engine._packet([0.7, 0.1, 0.1, 0.1])
            packet[key] = "synthetic_invalid_field"
            with self.subTest(key=key), self.assertRaises(adapter.AdapterError):
                self.engine.route(packet, "basic-needs", "basic-essential")
        packet = self.engine._packet([0.7, 0.1, 0.1, 0.1])
        packet["data_classification"] = "participant_data"
        with self.assertRaises(adapter.AdapterError):
            self.engine.route(packet, "basic-needs", "basic-essential")

    def test_config_mapping_threshold_and_safety_changes_require_a_new_contract(self):
        config, vocabulary, source = adapter.load_contract()
        mutations = [
            ("label_to_concept", {**config["label_to_concept"], "SYN-SEM-PAIN": "comfort-unwell"}),
            ("minimum_probability", 0.0), ("maximum_candidates", 40),
            ("participant_inputs_permitted", True), ("candidate_reveal_permitted", 0),
            ("care_ui_connection_permitted", "false"), ("output_action", "confirm"),
        ]
        for key, value in mutations:
            changed = deepcopy(config)
            changed[key] = value
            with self.subTest(key=key), self.assertRaises(adapter.AdapterError):
                adapter.validate_contract(changed, vocabulary, source)

    def test_same_version_source_and_vocabulary_changes_are_detected(self):
        config, vocabulary, source = adapter.load_contract()
        vocabulary["concepts"][0]["canonicalText"] = "changed synthetic wording"
        with self.assertRaises(adapter.AdapterError):
            adapter.validate_contract(config, vocabulary, source)
        config, vocabulary, source = adapter.load_contract()
        source["seed"] += 1
        with self.assertRaises(adapter.AdapterError):
            adapter.validate_contract(config, vocabulary, source)

    def test_test_data_do_not_change_training_or_calibration(self):
        generated = adapter.neural.generate_examples(self.engine._source)
        changed = [replace(x, label_index=(x.label_index + 1) % 4, features=(99.0,) * 4)
                   if x.split == "test" else x for x in generated]
        with patch.object(adapter.neural, "generate_examples", return_value=changed):
            independent = adapter.SyntheticIntentAdapter()
        self.assertEqual(self.engine.provenance, independent.provenance)
        for examples in (generated, changed):
            by_split = [{x.example_id for x in examples if x.split == split}
                        for split in ("development", "calibration", "test")]
            self.assertFalse(by_split[0] & by_split[1] or by_split[0] & by_split[2] or by_split[1] & by_split[2])

    def test_calibration_is_grid_nll_optimum_and_thresholds_are_not_fitted(self):
        calibration = [x for x in self.engine._examples if x.split == "calibration"]
        losses = {t: adapter.neural.negative_log_likelihood(self.engine._model, calibration, t)
                  for t in self.engine._source["calibration"]["temperature_grid"]}
        optimum = min(losses, key=lambda t: (losses[t], t))
        self.assertEqual(self.engine.provenance["temperature"], optimum)
        self.assertEqual(self.engine._config["minimum_probability"], 0.65)

    def test_end_to_end_is_deterministic_and_preserves_observed_errors(self):
        other = adapter.SyntheticIntentAdapter()
        artifact, report = other.build_artifacts()
        self.assertEqual(adapter.core.canonical_json_bytes(artifact), adapter.core.canonical_json_bytes(self.artifact))
        adapter.check_expected(report)
        self.assertEqual(report["route_count"], 480)
        self.assertEqual(report["route_selective_error"]["numerator"], 1)
        # All ten panels are exercised for every example; reference cannot choose a favorable panel.
        counts = adapter.Counter(row["example_id"] for row in artifact["predictions"])
        self.assertEqual(set(counts.values()), {10})

    def test_every_route_preserves_controls_and_has_no_output_authority(self):
        for row in self.artifact["predictions"]:
            decision = row["decision"]
            self.assertTrue(decision["confirmation_required"])
            self.assertFalse(decision["candidate_reveal_permitted"])
            self.assertFalse(decision["care_ui_connection_permitted"])
            self.assertEqual(decision["output_action"], adapter.NO_OUTPUT)
            self.assertEqual(decision["required_controls"], list(adapter.CONTROLS))
            if decision["decision"] == "abstain":
                self.assertEqual(decision["candidates"], [])
        for name in ("index.html", "app.js", "interaction_core.js"):
            self.assertNotIn("synthetic_intent_adapter", (adapter.CARE / name).read_text())

    def test_artifacts_are_tmp_only_no_overwrite_and_no_leaf_symlinks(self):
        with self.assertRaises(adapter.neural.NeuralContractError):
            adapter.write_artifacts(adapter.TRAINING / "forbidden", self.artifact, self.report)
        tmp_root = adapter.core.ROOT / "tmp"
        tmp_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=tmp_root) as directory:
            destination = Path(directory)
            adapter.write_artifacts(destination, self.artifact, self.report)
            with self.assertRaises(adapter.AdapterError):
                adapter.write_artifacts(destination, self.artifact, self.report)
        with tempfile.TemporaryDirectory(dir=tmp_root) as directory:
            destination = Path(directory)
            target = destination / "uncreated-target"
            (destination / "predictions.json").symlink_to(target)
            with self.assertRaises(adapter.AdapterError):
                adapter.write_artifacts(destination, self.artifact, self.report)
            self.assertFalse(target.exists())

    def test_check_cli_and_no_external_input_interface(self):
        command = [sys.executable, str(Path(adapter.__file__))]
        result = subprocess.run([*command, "check"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Synthetic intent adapter check: OK", result.stdout)
        for option in ("--input", "--audio", "--scores", "--model", "--care-log"):
            result = subprocess.run([*command, "check", option, "forbidden"], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
