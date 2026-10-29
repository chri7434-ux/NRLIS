#!/usr/bin/env python3
"""Acceptance tests for the participant-free Synthetic G0 pipeline."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import synthetic_g0


class SyntheticG0Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture, cls.config = synthetic_g0.load_validated_inputs()

    def test_checked_in_fixture_validates(self) -> None:
        synthetic_g0.validate_fixture_semantics(self.fixture, self.config)
        synthetic_g0.validate_config_semantics(self.config)

    def test_schema_rejects_missing_and_unknown_fields(self) -> None:
        schema = synthetic_g0.load_json(synthetic_g0.DEFAULT_FIXTURE_SCHEMA)

        missing = deepcopy(self.fixture)
        del missing["fixture_id"]
        with self.assertRaises(synthetic_g0.ContractError):
            synthetic_g0.validate_against_schema(missing, schema, "fixture")

        unknown = deepcopy(self.fixture)
        unknown["participant_name"] = "must never be accepted"
        with self.assertRaises(synthetic_g0.ContractError):
            synthetic_g0.validate_against_schema(unknown, schema, "fixture")

    def test_non_synthetic_classification_is_rejected(self) -> None:
        changed = deepcopy(self.fixture)
        changed["data_classification"] = "participant_data"
        with self.assertRaises(synthetic_g0.ContractError):
            synthetic_g0.validate_fixture_semantics(changed, self.config)

    def test_split_overlap_is_rejected(self) -> None:
        changed = deepcopy(self.fixture)
        changed["experiment_manifest"]["development_session_ids"] = [
            "SYN-S0003"
        ]
        with self.assertRaises(synthetic_g0.ContractError):
            synthetic_g0.validate_fixture_semantics(changed, self.config)

    def test_invalid_probability_vector_is_rejected(self) -> None:
        changed = deepcopy(self.config)
        changed["candidate_bank"]["signal_a"][0]["probability"] = 0.7
        with self.assertRaises(synthetic_g0.ContractError):
            synthetic_g0.validate_config_semantics(changed)

    def test_output_enabled_is_rejected(self) -> None:
        changed = deepcopy(self.config)
        changed["output_enabled"] = True
        with self.assertRaises(synthetic_g0.ContractError):
            synthetic_g0.validate_config_semantics(changed)

    def test_baseline_cannot_depend_on_reference_or_prompt(self) -> None:
        first = self.fixture["attempts"][0]
        changed = deepcopy(first)
        changed["reference_semantic_id"] = "SYN-SEM-0004"
        changed["task_family"] = "T3_NATURALISTIC"

        original_prediction = synthetic_g0.predict_observation(
            first["observable_signal_code"],
            first["input_quality_code"],
            self.config,
        )
        changed_prediction = synthetic_g0.predict_observation(
            changed["observable_signal_code"],
            changed["input_quality_code"],
            self.config,
        )
        self.assertEqual(original_prediction, changed_prediction)

    def test_build_is_byte_deterministic(self) -> None:
        first_predictions, first_metrics = synthetic_g0.build_artifacts(
            self.fixture, self.config
        )
        second_predictions, second_metrics = synthetic_g0.build_artifacts(
            self.fixture, self.config
        )
        self.assertEqual(
            synthetic_g0.canonical_json_bytes(first_predictions),
            synthetic_g0.canonical_json_bytes(second_predictions),
        )
        self.assertEqual(
            synthetic_g0.canonical_json_bytes(first_metrics),
            synthetic_g0.canonical_json_bytes(second_metrics),
        )

    def test_all_attempts_are_retained_but_denominators_are_prespecified(self) -> None:
        predictions, metrics = synthetic_g0.build_artifacts(
            self.fixture, self.config
        )
        self.assertEqual(len(predictions["predictions"]), 10)
        self.assertEqual(metrics["retained_attempt_count"], 10)
        self.assertEqual(metrics["eligible_attempt_count"], 8)
        self.assertEqual(metrics["excluded_attempt_count"], 2)
        self.assertEqual(
            metrics["unconditional_top_k_semantic_coverage"],
            {"numerator": 6, "denominator": 8, "value": 0.75},
        )
        self.assertEqual(
            metrics["hazardous_non_abstention_rate"],
            {"numerator": 3, "denominator": 8, "value": 0.375},
        )
        self.assertEqual(
            metrics["conditional_top_k_semantic_coverage"],
            {"numerator": 6, "denominator": 6, "value": 1.0},
        )
        self.assertEqual(
            metrics["challenge_abstention_sensitivity"],
            {
                "numerator": 2,
                "denominator": 3,
                "value": 0.666666666667,
            },
        )
        self.assertEqual(
            metrics["false_abstention_rate"],
            {
                "numerator": 1,
                "denominator": 6,
                "value": 0.166666666667,
            },
        )

    def test_challenge_target_is_independent_of_model_abstention_rule(self) -> None:
        attempts = self.fixture["attempts"]
        self.assertTrue(
            any(
                attempt["challenge_eligible"]
                and attempt["input_quality_code"] == "usable"
                for attempt in attempts
            )
        )
        self.assertTrue(
            any(
                not attempt["challenge_eligible"]
                and attempt["input_quality_code"] == "unstable"
                for attempt in attempts
            )
        )

    def test_frozen_metric_values_and_shadow_scope(self) -> None:
        predictions, metrics = synthetic_g0.build_artifacts(
            self.fixture, self.config
        )
        expected = synthetic_g0.load_json(synthetic_g0.DEFAULT_EXPECTED)
        synthetic_g0.assert_expected_subset(metrics, expected)
        self.assertEqual(metrics["safety"]["output_bypass_count"], 0)
        self.assertTrue(metrics["safety"]["all_outputs_disabled"])
        self.assertTrue(
            all(
                record["output_action"] == "no_action_shadow_only"
                for record in predictions["predictions"]
            )
        )
        self.assertIn(
            "successful_message_rate", metrics["not_estimable_in_shadow"]
        )
        self.assertIn(
            "participant_time_to_message", metrics["not_estimable_in_shadow"]
        )
        self.assertIn(
            "inference_latency",
            metrics["not_evaluable_in_static_fixture"],
        )

    def test_zero_denominator_is_null_not_zero(self) -> None:
        self.assertEqual(
            synthetic_g0.ratio(0, 0),
            {"numerator": 0, "denominator": 0, "value": None},
        )

    def test_prediction_validation_detects_output_bypass(self) -> None:
        predictions = synthetic_g0.generate_predictions(
            self.fixture, self.config
        )
        predictions["predictions"][0]["output_permitted"] = True
        with self.assertRaises(synthetic_g0.ContractError):
            synthetic_g0.validate_prediction_document(
                predictions, self.fixture, self.config
            )

    def test_repository_output_is_restricted_to_tmp(self) -> None:
        with self.assertRaises(synthetic_g0.ContractError):
            synthetic_g0.validate_output_directory(
                synthetic_g0.ROOT / "generated-results"
            )
        allowed = synthetic_g0.validate_output_directory(
            synthetic_g0.ROOT / "tmp" / "synthetic-test"
        )
        self.assertTrue(
            allowed.is_relative_to((synthetic_g0.ROOT / "tmp").resolve())
        )

    def test_run_refuses_overwrite_without_force(self) -> None:
        predictions, metrics = synthetic_g0.build_artifacts(
            self.fixture, self.config
        )
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            synthetic_g0.write_artifacts(output, predictions, metrics)
            with self.assertRaises(synthetic_g0.ContractError):
                synthetic_g0.write_artifacts(output, predictions, metrics)

    def test_check_cli_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(Path(synthetic_g0.__file__)), "check"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Synthetic G0 check: OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
