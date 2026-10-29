#!/usr/bin/env python3
"""Acceptance tests for the participant-free neural G0 pipeline."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import subprocess
import sys
import unittest

import participant_free_neural as neural


class ParticipantFreeNeuralTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = neural.load_config()

    def test_checked_in_config_is_strict_and_participant_free(self) -> None:
        neural.validate_config(self.config)
        self.assertEqual(
            self.config["data_classification"], "synthetic_no_participant_data"
        )
        self.assertFalse(self.config["safety"]["participant_data_permitted"])

    def test_schema_rejects_unknown_fields(self) -> None:
        changed = deepcopy(self.config)
        changed["participant_name"] = "forbidden"
        schema = neural.synthetic_g0.load_json(neural.DEFAULT_SCHEMA)
        with self.assertRaises(neural.synthetic_g0.ContractError):
            neural.synthetic_g0.validate_against_schema(changed, schema, "config")

    def test_non_synthetic_data_is_rejected(self) -> None:
        changed = deepcopy(self.config)
        changed["data_classification"] = "participant_data"
        with self.assertRaises(neural.NeuralContractError):
            neural.validate_config(changed)

    def test_participant_or_output_permission_is_rejected(self) -> None:
        for key in (
            "participant_data_permitted",
            "participant_specific_inference_permitted",
            "candidate_reveal_permitted",
        ):
            changed = deepcopy(self.config)
            changed["safety"][key] = True
            with self.subTest(key=key):
                with self.assertRaises(neural.NeuralContractError):
                    neural.validate_config(changed)

    def test_synthetic_splits_are_disjoint_and_deterministic(self) -> None:
        first = neural.generate_examples(self.config)
        second = neural.generate_examples(self.config)
        self.assertEqual(first, second)
        by_split = {
            split: {item.example_id for item in first if item.split == split}
            for split in ("development", "calibration", "test")
        }
        self.assertFalse(by_split["development"] & by_split["calibration"])
        self.assertFalse(by_split["development"] & by_split["test"])
        self.assertFalse(by_split["calibration"] & by_split["test"])

    def test_training_is_byte_deterministic(self) -> None:
        first_predictions, first_metrics = neural.build_artifacts(self.config)
        second_predictions, second_metrics = neural.build_artifacts(self.config)
        self.assertEqual(
            neural.synthetic_g0.canonical_json_bytes(first_predictions),
            neural.synthetic_g0.canonical_json_bytes(second_predictions),
        )
        self.assertEqual(first_metrics, second_metrics)

    def test_only_test_split_appears_in_prediction_artifact(self) -> None:
        predictions, metrics = neural.build_artifacts(self.config)
        neural.validate_artifacts(predictions, metrics)
        self.assertTrue(predictions["predictions"])
        self.assertTrue(
            all(row["split"] == "test" for row in predictions["predictions"])
        )

    def test_frozen_metrics_and_claim_boundary(self) -> None:
        predictions, metrics = neural.build_artifacts(self.config)
        neural.validate_artifacts(predictions, metrics)
        neural.assert_expected(metrics)
        self.assertIn("speech_recognition_performance", metrics["not_established"])
        self.assertEqual(metrics["safety"]["participant_example_count"], 0)
        self.assertEqual(metrics["safety"]["output_bypass_count"], 0)

    def test_repository_output_is_restricted_to_tmp(self) -> None:
        with self.assertRaises(neural.NeuralContractError):
            neural.validate_output_directory(neural.ROOT / "generated-results")
        accepted = neural.validate_output_directory(neural.ROOT / "tmp" / "neural")
        self.assertTrue(accepted.is_relative_to((neural.ROOT / "tmp").resolve()))

    def test_check_cli_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(Path(neural.__file__)), "check"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Participant-free neural G0 check: OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
