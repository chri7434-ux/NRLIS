#!/usr/bin/env python3
"""Acceptance tests for the WP2.1 recording-intake contract."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import subprocess
import sys
import unittest

import validate_recording_intake as intake


class RecordingIntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.record = intake.load_and_validate()

    def test_checked_in_fixture_is_synthetic_and_closed(self) -> None:
        self.assertEqual(
            self.record["data_classification"],
            "synthetic_no_participant_data",
        )
        self.assertEqual(self.record["handling_state"], "synthetic_fixture")
        self.assertTrue(
            all(
                value is False
                for key, value in self.record["authorizations"].items()
                if key in intake.AUTHORIZATION_KEYS
            )
        )

    def test_schema_rejects_unknown_or_content_fields(self) -> None:
        changed = deepcopy(self.record)
        changed["transcript"] = "forbidden content"
        schema = intake.synthetic_g0.load_json(intake.DEFAULT_SCHEMA)
        with self.assertRaises(intake.synthetic_g0.ContractError):
            intake.synthetic_g0.validate_against_schema(
                changed, schema, "recording_intake"
            )

    def test_semantics_reject_sensitive_nested_field_names(self) -> None:
        changed = deepcopy(self.record)
        changed["source_provenance"]["filename"] = "do-not-store.wav"
        with self.assertRaises(intake.IntakeContractError):
            intake.validate_semantics(changed)

    def test_real_participant_classification_is_rejected(self) -> None:
        changed = deepcopy(self.record)
        changed["data_classification"] = "private_participant_metadata"
        changed["participant_code"] = "NRLIS-P001"
        with self.assertRaises(intake.IntakeContractError):
            intake.validate_semantics(changed)

    def test_real_recording_context_is_rejected(self) -> None:
        for key, value in (
            ("structure", "naturalistic_conversation"),
            ("relative_time_bucket", "post_impairment"),
            ("collection_purpose", "ordinary_care_existing"),
        ):
            changed = deepcopy(self.record)
            changed["recording_context"][key] = value
            with self.subTest(key=key):
                with self.assertRaises(intake.IntakeContractError):
                    intake.validate_semantics(changed)

    def test_permission_drift_is_rejected(self) -> None:
        changed = deepcopy(self.record)
        changed["permission_scopes"]["model_training"] = "not_authorized"
        with self.assertRaises(intake.IntakeContractError):
            intake.validate_semantics(changed)

    def test_action_authorization_is_rejected(self) -> None:
        for key in intake.AUTHORIZATION_KEYS:
            changed = deepcopy(self.record)
            changed["authorizations"][key] = True
            with self.subTest(key=key):
                with self.assertRaises(intake.IntakeContractError):
                    intake.validate_semantics(changed)

    def test_external_approval_pointer_is_rejected(self) -> None:
        changed = deepcopy(self.record)
        changed["authorizations"][
            "external_determination_record_id"
        ] = "EXT-FAKE"
        with self.assertRaises(intake.IntakeContractError):
            intake.validate_semantics(changed)

    def test_reference_or_split_claim_is_rejected(self) -> None:
        changed = deepcopy(self.record)
        changed["reference_and_label"][
            "reference_source"
        ] = "known_prompt_participant_accepted"
        with self.assertRaises(intake.IntakeContractError):
            intake.validate_semantics(changed)

        changed = deepcopy(self.record)
        changed["split"]["role"] = "test"
        with self.assertRaises(intake.IntakeContractError):
            intake.validate_semantics(changed)

    def test_care_to_research_reuse_prohibition_is_required(self) -> None:
        changed = deepcopy(self.record)
        changed["disposition"]["care_data_reuse_prohibited"] = False
        with self.assertRaises(intake.IntakeContractError):
            intake.validate_semantics(changed)

    def test_checked_in_fixture_contains_no_sensitive_key_names(self) -> None:
        observed = {key for _path, key, _value in intake._walk(self.record)}
        self.assertFalse(observed & intake.FORBIDDEN_KEYS)

    def test_check_cli_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(Path(intake.__file__)), "check"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("real recordings accessed=0", result.stdout)
        self.assertIn("authorizations opened=0", result.stdout)


if __name__ == "__main__":
    unittest.main()
