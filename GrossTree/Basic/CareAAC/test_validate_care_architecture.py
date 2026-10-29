#!/usr/bin/env python3
"""Acceptance tests for the WP2.2 synthetic vocabulary architecture."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import validate_care_architecture as validator  # noqa: E402


class CareArchitectureValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config, cls.scenarios = validator.load_and_validate()
        cls.vocabulary_schema = validator.synthetic_g0.load_json(
            validator.DEFAULT_VOCABULARY_SCHEMA
        )
        cls.scenario_schema = validator.synthetic_g0.load_json(
            validator.DEFAULT_SCENARIO_SCHEMA
        )

    def test_checked_in_architecture_is_valid_and_synthetic(self) -> None:
        self.assertEqual(self.config["version"], "0.2.0")
        self.assertEqual(self.config["architectureVersion"], "1.0.0")
        self.assertEqual(
            self.config["dataClassification"], "synthetic_no_participant_data"
        )
        self.assertEqual(len(self.config["contexts"]), 5)
        self.assertEqual(len(self.config["concepts"]), 40)
        self.assertEqual(len(self.scenarios["scenarios"]), 7)

    def test_schema_rejects_unknown_vocabulary_field(self) -> None:
        changed = deepcopy(self.config)
        changed["unexpected"] = True
        with self.assertRaises(validator.synthetic_g0.ContractError):
            validator.synthetic_g0.validate_against_schema(
                changed, self.vocabulary_schema, "care_vocabulary"
            )

    def test_every_panel_has_exactly_four_distinct_concepts(self) -> None:
        changed = deepcopy(self.config)
        changed["contexts"][0]["panels"][0]["conceptIds"].pop()
        with self.assertRaisesRegex(
            validator.CareArchitectureError, "four distinct concepts"
        ):
            validator.validate_vocabulary_semantics(changed)

    def test_unknown_or_repeated_concept_reference_is_rejected(self) -> None:
        changed = deepcopy(self.config)
        changed["contexts"][0]["panels"][0]["conceptIds"][0] = "unknown-concept"
        with self.assertRaisesRegex(
            validator.CareArchitectureError, "unknown concepts"
        ):
            validator.validate_vocabulary_semantics(changed)

    def test_duplicate_concept_or_surface_is_rejected(self) -> None:
        changed = deepcopy(self.config)
        changed["concepts"][1]["id"] = changed["concepts"][0]["id"]
        with self.assertRaisesRegex(validator.CareArchitectureError, "concept IDs"):
            validator.validate_vocabulary_semantics(changed)

        changed = deepcopy(self.config)
        changed["concepts"][1]["canonicalText"] = changed["concepts"][0][
            "canonicalText"
        ]
        with self.assertRaisesRegex(
            validator.CareArchitectureError, "canonical surface forms"
        ):
            validator.validate_vocabulary_semantics(changed)

    def test_confirmation_free_text_and_model_paths_remain_closed(self) -> None:
        for path, value in (
            (("modelInference",), True),
            (("safetyPolicy", "confirmationRequired"), False),
            (("safetyPolicy", "freeTextGeneration"), True),
            (("candidateSetPolicy", "modelReranking"), True),
        ):
            with self.subTest(path=path):
                changed = deepcopy(self.config)
                target = changed
                for key in path[:-1]:
                    target = target[key]
                target[path[-1]] = value
                with self.assertRaises(validator.CareArchitectureError):
                    validator.validate_vocabulary_semantics(changed)

    def test_personalization_and_dialect_claim_are_rejected(self) -> None:
        for key, value in (("personalization", "private_overlay"), ("dialectClaim", "supported")):
            with self.subTest(key=key):
                changed = deepcopy(self.config)
                changed[key] = value
                with self.assertRaisesRegex(
                    validator.CareArchitectureError,
                    "personalization or dialect",
                ):
                    validator.validate_vocabulary_semantics(changed)

    def test_content_identity_score_and_log_fields_are_rejected(self) -> None:
        for key in ("participantId", "audio", "confidence", "interactionLog"):
            with self.subTest(key=key):
                changed = deepcopy(self.config)
                changed["concepts"][0][key] = "synthetic-placeholder"
                with self.assertRaisesRegex(
                    validator.CareArchitectureError, "fields are prohibited"
                ):
                    validator.validate_vocabulary_semantics(changed)

    def test_scenario_schema_rejects_unknown_field(self) -> None:
        changed = deepcopy(self.scenarios)
        changed["scenarios"][0]["steps"][0]["timestamp"] = "none"
        with self.assertRaises(validator.synthetic_g0.ContractError):
            validator.synthetic_g0.validate_against_schema(
                changed, self.scenario_schema, "care_interactions"
            )

    def test_scenario_action_arguments_are_exact(self) -> None:
        changed = deepcopy(self.scenarios)
        changed["scenarios"][0]["steps"][0]["conceptId"] = "need-water"
        with self.assertRaisesRegex(
            validator.CareArchitectureError, "invalid arguments"
        ):
            validator.validate_scenario_semantics(changed, self.config)

    def test_scenario_participant_or_persistence_drift_is_rejected(self) -> None:
        for key, value in (("participantRecords", 1), ("persistence", True)):
            with self.subTest(key=key):
                changed = deepcopy(self.scenarios)
                changed[key] = value
                with self.assertRaisesRegex(
                    validator.CareArchitectureError,
                    "cannot contain or persist",
                ):
                    validator.validate_scenario_semantics(changed, self.config)

    def test_scenario_unknown_concept_is_rejected(self) -> None:
        changed = deepcopy(self.scenarios)
        changed["scenarios"][0]["steps"][1]["conceptId"] = "unknown-concept"
        with self.assertRaisesRegex(
            validator.CareArchitectureError, "unknown concept"
        ):
            validator.validate_scenario_semantics(changed, self.config)

    def test_check_cli_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "validate_care_architecture.py"), "check"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("participant records=0", result.stdout)
        self.assertIn("model inference=0", result.stdout)


if __name__ == "__main__":
    unittest.main()
