"""Acceptance tests for fail-closed WP1 governance validation."""

from __future__ import annotations

import copy
import importlib.util
import shutil
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("validate_wp1.py")
SPEC = importlib.util.spec_from_file_location("validate_wp1", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Could not load validate_wp1.py")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)

TODAY = date.today()
TODAY_TEXT = TODAY.isoformat()
FUTURE_TEXT = (TODAY + timedelta(days=365)).isoformat()
PAST_TEXT = (TODAY - timedelta(days=365)).isoformat()
SCOPE_HASH = VALIDATOR.compute_scope_sha256()
ARTIFACT_HASH = "b" * 64
RECORD_ID_HASH = "c" * 64


class WP1GateRegistryTests(unittest.TestCase):
    """Exercise the live closed registry and transition invariants."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.base = VALIDATOR.load_registry(VALIDATOR.DEFAULT_REGISTRY)

    def validate(self, value: dict) -> list[str]:
        return VALIDATOR.validate_registry(value)

    @staticmethod
    def role(value: dict, role_id: str) -> dict:
        return next(item for item in value["roles"] if item["role_id"] == role_id)

    @staticmethod
    def add_authority(
        value: dict,
        authority_id: str,
        authority_type: str,
        *,
        status: str = "verified",
    ) -> None:
        value["external_authorities"].append(
            {
                "authority_id": authority_id,
                "authority_name": f"Synthetic fixture {authority_id}",
                "authority_type": authority_type,
                "jurisdiction": "synthetic-test-only",
                "official_uri": "https://example.invalid/authority",
                "verification_artifact_sha256": ARTIFACT_HASH,
                "external_system_record_id_sha256": RECORD_ID_HASH,
                "status": status,
                "verified_on": TODAY_TEXT,
                "review_due_on": FUTURE_TEXT,
                "expires_on": FUTURE_TEXT,
                "revoked_on": None,
            }
        )

    @staticmethod
    def add_evidence(
        value: dict,
        *,
        record_id: str,
        issuer: str,
        record_type: str,
        recorder: str,
        covered_gate_ids: list[str] | None = None,
        covered_role_ids: list[str] | None = None,
        holder_id: str | None = None,
        status: str = "active",
        scope_hash: str = SCOPE_HASH,
        decision_outcome: str = "requirements_satisfied",
    ) -> None:
        recorder_role = next(
            role for role in value["roles"] if role["role_id"] == recorder
        )
        value["external_evidence_records"].append(
            {
                "record_id": record_id,
                "issuer_authority_id": issuer,
                "record_type": record_type,
                "decision_outcome": decision_outcome,
                "artifact_sha256": ARTIFACT_HASH,
                "external_system_record_id_sha256": RECORD_ID_HASH,
                "protocol_id": "NRLIS-T001",
                "protocol_version": "0.3",
                "scope_sha256": scope_hash,
                "covered_gate_ids": covered_gate_ids or [],
                "covered_role_ids": covered_role_ids or [],
                "subject_holder_id": holder_id,
                "status": status,
                "effective_on": TODAY_TEXT,
                "review_due_on": FUTURE_TEXT,
                "expires_on": FUTURE_TEXT,
                "revoked_on": None,
                "recorded_by_role_id": recorder,
                "recorded_by_holder_id": recorder_role["holder_id"],
            }
        )

    @staticmethod
    def add_training(
        value: dict,
        *,
        record_id: str,
        holder_id: str,
        issuer: str,
        role_id: str,
        training_type: str,
        status: str = "valid",
        expires_on: str = FUTURE_TEXT,
    ) -> None:
        value["training_records"].append(
            {
                "record_id": record_id,
                "holder_id": holder_id,
                "training_type": training_type,
                "covered_role_ids": [role_id],
                "issuer_authority_id": issuer,
                "artifact_sha256": ARTIFACT_HASH,
                "external_system_record_id_sha256": RECORD_ID_HASH,
                "status": status,
                "completed_on": TODAY_TEXT,
                "review_due_on": FUTURE_TEXT,
                "expires_on": expires_on,
                "revoked_on": None,
            }
        )

    def structurally_complete_fixture(self) -> dict:
        """Build synthetic metadata; this does not authenticate real approvals."""

        value = copy.deepcopy(self.base)
        value["determination_scope"]["scope_sha256"] = SCOPE_HASH
        authorities = {
            "irb": "AUTH-EXT-SYNTHETIC-IRB",
            "privacy": "AUTH-EXT-SYNTHETIC-PRIVACY",
            "device": "AUTH-EXT-SYNTHETIC-DEVICE",
            "training": "AUTH-EXT-SYNTHETIC-TRAINING",
        }
        self.add_authority(
            value,
            authorities["irb"],
            "institutional_irb_or_hrpp",
        )
        self.add_authority(
            value,
            authorities["privacy"],
            "privacy_or_security_office",
        )
        self.add_authority(
            value,
            authorities["device"],
            "device_regulatory_authority",
        )
        self.add_authority(
            value,
            authorities["training"],
            "training_provider",
        )

        for index, role in enumerate(value["roles"], start=1):
            holder_id = f"HOLDER-SYNTHETIC-{index:02d}"
            appointment_id = f"EXT-SYNTHETIC-APPOINTMENT-{index:02d}"
            role.update(
                {
                    "status": "verified",
                    "holder_id": holder_id,
                    "appointment_record_id": appointment_id,
                    "training_record_ids": [],
                    "expires_on": FUTURE_TEXT,
                }
            )

        for index, role in enumerate(value["roles"], start=1):
            role_id = role["role_id"]
            holder_id = role["holder_id"]
            appointment_id = role["appointment_record_id"]
            self.add_evidence(
                value,
                record_id=appointment_id,
                issuer=authorities["irb"],
                record_type="role_appointment",
                recorder="ROLE-ETHICS-CONTACT",
                covered_role_ids=[role_id],
                holder_id=holder_id,
            )
            for competency_index, training_type in enumerate(
                sorted(role["required_training_types"]),
                start=1,
            ):
                training_id = (
                    f"TRAIN-SYNTHETIC-{index:02d}-{competency_index:02d}"
                )
                self.add_training(
                    value,
                    record_id=training_id,
                    holder_id=holder_id,
                    issuer=authorities["training"],
                    role_id=role_id,
                    training_type=training_type,
                )
                role["training_record_ids"].append(training_id)
            if role["independence_required"]:
                independence_id = f"EXT-SYNTHETIC-INDEPENDENCE-{index:02d}"
                role["independence_record_id"] = independence_id
                self.add_evidence(
                    value,
                    record_id=independence_id,
                    issuer=authorities["irb"],
                    record_type="independence_review",
                    recorder="ROLE-ETHICS-CONTACT",
                    covered_role_ids=[role_id],
                    holder_id=holder_id,
                )

        for gate in value["gates"]:
            gate_id = gate["gate_id"]
            if gate_id == "WP1-G04":
                issuer = authorities["device"]
            elif gate_id == "WP1-G05" or gate_id in {
                f"WP1-G{number:02d}" for number in range(19, 24)
            }:
                issuer = authorities["privacy"]
            else:
                issuer = authorities["irb"]
            record_type = sorted(VALIDATOR.GATE_RECORD_TYPES[gate_id])[0]
            recorder = (
                "ROLE-INDEPENDENT-EVENT-REVIEWER"
                if gate_id == "WP1-G25"
                else "ROLE-ETHICS-CONTACT"
            )
            evidence_id = f"EXT-SYNTHETIC-{gate_id}-DECISION"
            self.add_evidence(
                value,
                record_id=evidence_id,
                issuer=issuer,
                record_type=record_type,
                recorder=recorder,
                covered_gate_ids=[gate_id],
            )
            gate.update(
                {
                    "status": "satisfied",
                    "evidence_record_ids": [evidence_id],
                    "recorded_by_role_id": recorder,
                    "recorded_by_holder_id": self.role(
                        value, recorder
                    )["holder_id"],
                    "issuing_authority_ids": [issuer],
                    "decided_on": TODAY_TEXT,
                    "review_due_on": FUTURE_TEXT,
                    "expires_on": FUTURE_TEXT,
                }
            )

        value["active_holds"] = []
        value["status"] = "complete"
        value["exit_rule"]["wp1_exit_authorized"] = True
        return value

    def test_current_registry_is_valid_and_closed(self) -> None:
        self.assertEqual(self.validate(copy.deepcopy(self.base)), [])
        self.assertFalse(any(self.base["authorizations"].values()))
        self.assertEqual(
            set(self.base["consent_scopes"].values()), {"not_authorized"}
        )
        self.assertEqual(self.base["external_evidence_records"], [])

    def test_activity_cannot_be_enabled_by_wp1(self) -> None:
        value = copy.deepcopy(self.base)
        value["authorizations"]["participant_facing_intake"] = True
        self.assertTrue(
            any(
                "cannot grant activity authorization" in item
                for item in self.validate(value)
            )
        )

    def test_activity_key_set_cannot_drift(self) -> None:
        value = copy.deepcopy(self.base)
        value["authorizations"].pop("research_contact")
        self.assertTrue(
            any("frozen activity key set" in item for item in self.validate(value))
        )

    def test_consent_scope_cannot_be_opened_during_planning(self) -> None:
        value = copy.deepcopy(self.base)
        value["consent_scopes"]["audio_recording"] = "authorized"
        self.assertTrue(
            any(
                "cannot record participant permission" in item
                for item in self.validate(value)
            )
        )

    def test_missing_gate_fails(self) -> None:
        value = copy.deepcopy(self.base)
        value["gates"].pop()
        self.assertTrue(
            any("missing required gates" in item for item in self.validate(value))
        )

    def test_duplicate_gate_fails(self) -> None:
        value = copy.deepcopy(self.base)
        value["gates"].append(copy.deepcopy(value["gates"][0]))
        self.assertTrue(
            any("duplicate gate IDs" in item for item in self.validate(value))
        )

    def test_satisfied_gate_requires_provenance_and_finite_review(self) -> None:
        value = copy.deepcopy(self.base)
        value["gates"][0]["status"] = "satisfied"
        errors = self.validate(value)
        self.assertTrue(any("without evidence" in item for item in errors))
        self.assertTrue(any("without recording role" in item for item in errors))
        self.assertTrue(any("without decision date" in item for item in errors))
        self.assertTrue(any("without review_due_on" in item for item in errors))

    def test_arbitrary_external_id_is_not_evidence(self) -> None:
        value = self.structurally_complete_fixture()
        gate = value["gates"][0]
        gate["evidence_record_ids"] = ["EXT-ARBITRARY-STRING"]
        self.assertTrue(
            any(
                "absent, inactive, expired, revoked" in item
                for item in self.validate(value)
            )
        )

    def test_unverified_issuing_authority_blocks_evidence(self) -> None:
        value = self.structurally_complete_fixture()
        value["external_authorities"][0]["status"] = "pending"
        self.assertTrue(
            any(
                "issued by an unverified authority" in item
                for item in self.validate(value)
            )
        )

    def test_scope_hash_mismatch_blocks_gate(self) -> None:
        value = self.structurally_complete_fixture()
        target_id = value["gates"][0]["evidence_record_ids"][0]
        record = next(
            item
            for item in value["external_evidence_records"]
            if item["record_id"] == target_id
        )
        record["scope_sha256"] = "d" * 64
        self.assertTrue(
            any(
                "not bound to the current protocol scope" in item
                for item in self.validate(value)
            )
        )

    def test_revoked_evidence_cannot_close_gate(self) -> None:
        value = self.structurally_complete_fixture()
        target_id = value["gates"][0]["evidence_record_ids"][0]
        record = next(
            item
            for item in value["external_evidence_records"]
            if item["record_id"] == target_id
        )
        record["status"] = "revoked"
        record["revoked_on"] = TODAY_TEXT
        self.assertTrue(
            any(
                "absent, inactive, expired, revoked" in item
                for item in self.validate(value)
            )
        )

    def test_applicability_gate_requires_domain_specific_record(self) -> None:
        value = self.structurally_complete_fixture()
        target_id = value["gates"][3]["evidence_record_ids"][0]
        record = next(
            item
            for item in value["external_evidence_records"]
            if item["record_id"] == target_id
        )
        record["record_type"] = "other_scoped_governance_record"
        self.assertTrue(
            any(
                "required gate-specific evidence type" in item
                for item in self.validate(value)
            )
        )

    def test_applicability_gate_requires_eligible_authority_type(self) -> None:
        value = self.structurally_complete_fixture()
        target_id = value["gates"][3]["evidence_record_ids"][0]
        record = next(
            item
            for item in value["external_evidence_records"]
            if item["record_id"] == target_id
        )
        authority = next(
            item
            for item in value["external_authorities"]
            if item["authority_id"] == record["issuer_authority_id"]
        )
        authority["authority_type"] = "training_provider"
        self.assertTrue(
            any(
                "ineligible authority type" in item
                for item in self.validate(value)
            )
        )

    def test_applicability_gate_requires_ethics_recorder(self) -> None:
        value = self.structurally_complete_fixture()
        gate = value["gates"][0]
        gate["recorded_by_role_id"] = "ROLE-TECHNICAL-LEAD"
        self.assertTrue(
            any(
                "ineligible recording role" in item
                for item in self.validate(value)
            )
        )

    def test_not_applicable_gate_status_cannot_close_a_control(self) -> None:
        value = self.structurally_complete_fixture()
        value["gates"][7]["status"] = "not_applicable"
        self.assertTrue(
            any(
                "gate status cannot be not_applicable" in item
                for item in self.validate(value)
            )
        )

    def test_not_applicable_outcome_cannot_close_mandatory_gate(self) -> None:
        value = self.structurally_complete_fixture()
        target_id = value["gates"][7]["evidence_record_ids"][0]
        record = next(
            item
            for item in value["external_evidence_records"]
            if item["record_id"] == target_id
        )
        record["decision_outcome"] = "not_applicable"
        self.assertTrue(
            any(
                "has an incompatible decision outcome" in item
                for item in self.validate(value)
            )
        )

    def test_not_applicable_outcome_can_resolve_applicability_gate(self) -> None:
        value = self.structurally_complete_fixture()
        target_id = value["gates"][3]["evidence_record_ids"][0]
        record = next(
            item
            for item in value["external_evidence_records"]
            if item["record_id"] == target_id
        )
        record["decision_outcome"] = "not_applicable"
        self.assertEqual(self.validate(value), [])

    def test_wrong_record_type_cannot_close_consent_gate(self) -> None:
        value = self.structurally_complete_fixture()
        target_id = value["gates"][7]["evidence_record_ids"][0]
        record = next(
            item
            for item in value["external_evidence_records"]
            if item["record_id"] == target_id
        )
        record["record_type"] = "role_appointment"
        self.assertTrue(
            any(
                "required gate-specific evidence type" in item
                for item in self.validate(value)
            )
        )

    def test_training_provider_cannot_close_consent_gate(self) -> None:
        value = self.structurally_complete_fixture()
        gate = value["gates"][7]
        target_id = gate["evidence_record_ids"][0]
        record = next(
            item
            for item in value["external_evidence_records"]
            if item["record_id"] == target_id
        )
        record["issuer_authority_id"] = "AUTH-EXT-SYNTHETIC-TRAINING"
        gate["issuing_authority_ids"] = ["AUTH-EXT-SYNTHETIC-TRAINING"]
        self.assertTrue(
            any(
                "ineligible authority type" in item
                for item in self.validate(value)
            )
        )

    def test_open_registry_requires_active_hold(self) -> None:
        value = copy.deepcopy(self.base)
        value["active_holds"] = []
        self.assertTrue(
            any("must retain an active hold" in item for item in self.validate(value))
        )

    def test_terminal_gate_review_due_must_be_future(self) -> None:
        value = self.structurally_complete_fixture()
        value["gates"][0]["review_due_on"] = TODAY_TEXT
        self.assertTrue(
            any("has reached review_due_on" in item for item in self.validate(value))
        )

    def test_future_gate_decision_is_invalid(self) -> None:
        value = self.structurally_complete_fixture()
        value["gates"][0]["decided_on"] = FUTURE_TEXT
        self.assertTrue(
            any("decision date is in the future" in item for item in self.validate(value))
        )

    def test_unassigned_role_cannot_carry_assignment_evidence(self) -> None:
        value = copy.deepcopy(self.base)
        value["roles"][0]["holder_id"] = "HOLDER-UNAUTHORIZED"
        self.assertTrue(
            any(
                "unassigned but carries assignment evidence" in item
                for item in self.validate(value)
            )
        )

    def test_verified_role_requires_stable_holder(self) -> None:
        value = self.structurally_complete_fixture()
        value["roles"][0]["holder_id"] = None
        self.assertTrue(
            any("without stable holder_id" in item for item in self.validate(value))
        )

    def test_verified_role_requires_finite_future_expiry(self) -> None:
        value = self.structurally_complete_fixture()
        value["roles"][0]["expires_on"] = None
        self.assertTrue(
            any("without a finite expires_on" in item for item in self.validate(value))
        )

    def test_role_appointment_must_match_current_scope(self) -> None:
        value = self.structurally_complete_fixture()
        appointment_id = value["roles"][0]["appointment_record_id"]
        appointment = next(
            item
            for item in value["external_evidence_records"]
            if item["record_id"] == appointment_id
        )
        appointment["scope_sha256"] = "d" * 64
        self.assertTrue(
            any(
                "appointment is not bound to the current protocol scope" in item
                for item in self.validate(value)
            )
        )

    def test_expired_training_invalidates_verified_role(self) -> None:
        value = self.structurally_complete_fixture()
        training_id = value["roles"][0]["training_record_ids"][0]
        training = next(
            item
            for item in value["training_records"]
            if item["record_id"] == training_id
        )
        training["status"] = "expired"
        training["expires_on"] = PAST_TEXT
        self.assertTrue(
            any(
                f"training {training_id} is not current" in item
                for item in self.validate(value)
            )
        )

    def test_wrong_training_competency_invalidates_verified_role(self) -> None:
        value = self.structurally_complete_fixture()
        role = self.role(value, "ROLE-TECHNICAL-LEAD")
        training_id = role["training_record_ids"][0]
        training = next(
            item
            for item in value["training_records"]
            if item["record_id"] == training_id
        )
        training["training_type"] = "human_research_protection"
        self.assertTrue(
            any(
                "lacks required training type(s)" in item
                for item in self.validate(value)
            )
        )

    def test_role_appointment_must_cover_role(self) -> None:
        value = self.structurally_complete_fixture()
        role = self.role(value, "ROLE-DATA-STEWARD")
        appointment = next(
            item
            for item in value["external_evidence_records"]
            if item["record_id"] == role["appointment_record_id"]
        )
        appointment["covered_role_ids"] = []
        self.assertTrue(
            any(
                "appointment does not cover the role" in item
                for item in self.validate(value)
            )
        )

    def test_training_record_must_cover_role(self) -> None:
        value = self.structurally_complete_fixture()
        role = self.role(value, "ROLE-DATA-STEWARD")
        training = next(
            item
            for item in value["training_records"]
            if item["record_id"] == role["training_record_ids"][0]
        )
        training["covered_role_ids"] = []
        self.assertTrue(
            any(
                "training " in item and "does not cover the role" in item
                for item in self.validate(value)
            )
        )

    def test_verified_independent_role_requires_independence_record(self) -> None:
        value = self.structurally_complete_fixture()
        role = self.role(value, "ROLE-CONSENT-ACCESS-REVIEWER")
        role["independence_record_id"] = None
        self.assertTrue(
            any(
                "verified without independence evidence" in item
                for item in self.validate(value)
            )
        )

    def test_combined_holder_requires_shared_approval(self) -> None:
        value = self.structurally_complete_fixture()
        first = self.role(value, "ROLE-ACCOUNTABLE-INVESTIGATOR")
        second = self.role(value, "ROLE-DATA-STEWARD")
        second["holder_id"] = first["holder_id"]
        self.assertTrue(
            any(
                "lacks one shared combination approval" in item
                for item in self.validate(value)
            )
        )

    def test_same_holder_different_appointments_cannot_bypass_independence(self) -> None:
        value = self.structurally_complete_fixture()
        technical = self.role(value, "ROLE-TECHNICAL-LEAD")
        reviewer = self.role(value, "ROLE-INDEPENDENT-EVENT-REVIEWER")
        self.assertNotEqual(
            technical["appointment_record_id"],
            reviewer["appointment_record_id"],
        )
        reviewer["holder_id"] = technical["holder_id"]
        self.assertTrue(
            any(
                "conflicts with required distinct role" in item
                for item in self.validate(value)
            )
        )

    def test_role_separation_policy_cannot_be_weakened(self) -> None:
        value = copy.deepcopy(self.base)
        reviewer = self.role(value, "ROLE-INDEPENDENT-EVENT-REVIEWER")
        reviewer["must_be_distinct_from_role_ids"] = []
        self.assertTrue(
            any(
                "role-separation policy is not frozen" in item
                for item in self.validate(value)
            )
        )

    def test_independence_policy_cannot_be_weakened(self) -> None:
        value = self.structurally_complete_fixture()
        reviewer = self.role(value, "ROLE-INDEPENDENT-EVENT-REVIEWER")
        reviewer["independence_required"] = False
        reviewer["independence_record_id"] = None
        self.assertTrue(
            any(
                "independence policy is not frozen" in item
                for item in self.validate(value)
            )
        )

    def test_g25_requires_independent_exit_review_record(self) -> None:
        value = self.structurally_complete_fixture()
        target_id = value["gates"][-1]["evidence_record_ids"][0]
        record = next(
            item
            for item in value["external_evidence_records"]
            if item["record_id"] == target_id
        )
        record["record_type"] = "other_scoped_governance_record"
        self.assertTrue(
            any(
                "required gate-specific evidence type" in item
                for item in self.validate(value)
            )
        )

    def test_g25_cannot_inherit_a_previous_reviewer_holder(self) -> None:
        value = self.structurally_complete_fixture()
        reviewer = self.role(value, "ROLE-INDEPENDENT-EVENT-REVIEWER")
        old_holder = reviewer["holder_id"]
        new_holder = "HOLDER-SYNTHETIC-REVIEWER-REPLACEMENT"
        reviewer["holder_id"] = new_holder
        appointment = next(
            item
            for item in value["external_evidence_records"]
            if item["record_id"] == reviewer["appointment_record_id"]
        )
        appointment["subject_holder_id"] = new_holder
        independence = next(
            item
            for item in value["external_evidence_records"]
            if item["record_id"] == reviewer["independence_record_id"]
        )
        independence["subject_holder_id"] = new_holder
        for training_id in reviewer["training_record_ids"]:
            training = next(
                item
                for item in value["training_records"]
                if item["record_id"] == training_id
            )
            training["holder_id"] = new_holder
        self.assertEqual(value["gates"][-1]["recorded_by_holder_id"], old_holder)
        self.assertTrue(
            any(
                "recording holder does not match the current" in item
                or "recording holder mismatch" in item
                for item in self.validate(value)
            )
        )

    def test_arbitrary_self_consistent_scope_hash_is_rejected(self) -> None:
        value = self.structurally_complete_fixture()
        arbitrary_hash = "d" * 64
        value["determination_scope"]["scope_sha256"] = arbitrary_hash
        for record in value["external_evidence_records"]:
            record["scope_sha256"] = arbitrary_hash
        self.assertTrue(
            any(
                "does not match the canonical document manifest" in item
                for item in self.validate(value)
            )
        )

    def test_scope_hash_covers_all_protocol_normative_documents(self) -> None:
        expected = (
            "GrossTree/__init__/PROJECT_CHARTER.md",
            "GrossTree/__init__/WP1_GOVERNANCE_AND_DETERMINATION_PLAN.md",
            "GrossTree/__init__/EVALUATION_SAFETY_GOVERNANCE.md",
            "GrossTree/Basic/Trials/NRLIS-T001/PROTOCOL.md",
            "GrossTree/Basic/Trials/NRLIS-T001/"
            "ACCESSIBLE_CONSENT_ASSENT_DISSENT_PLAN.md",
            "GrossTree/Basic/Trials/NRLIS-T001/TASK_REFERENCE_AUTHORSHIP_SOP.md",
            "GrossTree/Basic/Training/Dataset/DATA_CONTRACT.md",
            "GrossTree/Basic/Training/Dataset/"
            "DATA_MANAGEMENT_WITHDRAWAL_PLAN.md",
            "GrossTree/Basic/Training/Evaluation/METRICS.md",
            "GrossTree/Basic/Training/Evaluation/T001_ANALYSIS_SPEC.md",
        )
        self.assertEqual(VALIDATOR.SCOPE_DOCUMENT_PATHS, expected)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for relative_path in VALIDATOR.SCOPE_DOCUMENT_PATHS:
                destination = root / relative_path
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(VALIDATOR.PROJECT_ROOT / relative_path, destination)
            before = VALIDATOR.compute_scope_sha256(root)
            target = (
                root
                / "GrossTree"
                / "__init__"
                / "EVALUATION_SAFETY_GOVERNANCE.md"
            )
            target.write_text(
                target.read_text(encoding="utf-8")
                + "\nSynthetic scope-change sentinel.\n",
                encoding="utf-8",
            )
            after = VALIDATOR.compute_scope_sha256(root)
        self.assertNotEqual(before, after)

    def test_protocol_version_must_match_normative_document(self) -> None:
        value = self.structurally_complete_fixture()
        value["determination_scope"]["protocol_version"] = "9.9"
        for record in value["external_evidence_records"]:
            record["protocol_version"] = "9.9"
        self.assertTrue(
            any(
                "does not match the normative T001 document" in item
                for item in self.validate(value)
            )
        )

    def test_baseline_uses_registry_as_single_source(self) -> None:
        self.assertEqual(
            VALIDATOR.validate_baseline_reference(
                registry=copy.deepcopy(self.base)
            ),
            [],
        )

    def test_baseline_duplicate_wp1_state_fails(self) -> None:
        text = (
            "governance:\n"
            f"  wp1_authoritative_registry: {VALIDATOR.EXPECTED_BASELINE_REGISTRY}\n"
            f"  wp1_semantic_validator: {VALIDATOR.EXPECTED_BASELINE_VALIDATOR}\n"
            "  activity_authorization_inherited: false\n"
            "  wp1_status: complete\n"
        )
        self.assertTrue(
            any(
                "duplicates authoritative WP1 state fields" in item
                for item in VALIDATOR._validate_baseline_text(text)
            )
        )

    def test_baseline_duplicate_state_outside_governance_fails(self) -> None:
        text = (
            "project:\n"
            "  wp1_exit_authorized: true\n"
            "governance:\n"
            f"  wp1_authoritative_registry: {VALIDATOR.EXPECTED_BASELINE_REGISTRY}\n"
            f"  wp1_semantic_validator: {VALIDATOR.EXPECTED_BASELINE_VALIDATOR}\n"
            "  activity_authorization_inherited: false\n"
        )
        self.assertTrue(
            any(
                "duplicates authoritative WP1 state fields" in item
                for item in VALIDATOR._validate_baseline_text(text)
            )
        )

    def test_baseline_executable_flag_cannot_open(self) -> None:
        text = VALIDATOR.DEFAULT_BASELINE.read_text(encoding="utf-8")
        text = text.replace("  enrollment_open: false", "  enrollment_open: true")
        self.assertTrue(
            any(
                "protocol.enrollment_open must remain false" in item
                for item in VALIDATOR._validate_baseline_text(text)
            )
        )

    def test_baseline_cannot_duplicate_activity_authorization(self) -> None:
        text = VALIDATOR.DEFAULT_BASELINE.read_text(encoding="utf-8")
        text = text.replace(
            "  stage_d_enabled: false\n",
            "  stage_d_enabled: false\n"
            "  participant_facing_intake: true\n"
            "  shadow_inference: true\n"
            "  candidate_reveal: true\n",
        )
        errors = VALIDATOR._validate_baseline_text(text)
        self.assertTrue(
            any(
                "duplicates authoritative activity state" in item
                for item in errors
            )
        )

    def test_baseline_root_activity_leaf_fails(self) -> None:
        text = VALIDATOR.DEFAULT_BASELINE.read_text(encoding="utf-8")
        text += "\nparticipant_facing_intake: true\n"
        self.assertTrue(
            any(
                "duplicates authoritative activity state" in item
                for item in VALIDATOR._validate_baseline_text(text)
            )
        )

    def test_baseline_deep_activity_and_enabled_leaves_fail(self) -> None:
        text = VALIDATOR.DEFAULT_BASELINE.read_text(encoding="utf-8")
        text = text.replace(
            "  stage_d_enabled: false\n",
            "  stage_d_enabled: false\n"
            "  nested_authorization:\n"
            "    participant_facing_intake: true\n"
            "    candidate_reveal_enabled: true\n",
        )
        errors = VALIDATOR._validate_baseline_text(text)
        self.assertTrue(
            any(
                "duplicates authoritative activity state" in item
                for item in errors
            )
        )
        self.assertTrue(
            any(
                "unknown executable enabled flags" in item
                for item in errors
            )
        )

    def test_baseline_quoted_false_is_not_boolean_false(self) -> None:
        text = VALIDATOR.DEFAULT_BASELINE.read_text(encoding="utf-8")
        text = text.replace(
            "  output_enabled: false",
            '  output_enabled: "false"',
        )
        self.assertTrue(
            any(
                "protocol.output_enabled must remain false" in item
                for item in VALIDATOR._validate_baseline_text(text)
            )
        )

    def test_baseline_dotted_root_key_cannot_masquerade_as_nested_path(self) -> None:
        text = VALIDATOR.DEFAULT_BASELINE.read_text(encoding="utf-8")
        text = text.replace("  output_enabled: false\n", "")
        text += '\n"protocol.output_enabled": false\n'
        errors = VALIDATOR._validate_baseline_text(text)
        self.assertTrue(
            any(
                "must use lowercase snake_case" in item
                for item in errors
            )
        )
        self.assertTrue(
            any(
                "protocol.output_enabled must remain false" in item
                for item in errors
            )
        )

    def test_baseline_unknown_enabled_flag_fails(self) -> None:
        text = VALIDATOR.DEFAULT_BASELINE.read_text(encoding="utf-8")
        text = text.replace(
            "  stage_d_enabled: false\n",
            "  stage_d_enabled: false\n  candidate_reveal_enabled: false\n",
        )
        self.assertTrue(
            any(
                "unknown executable enabled flags" in item
                for item in VALIDATOR._validate_baseline_text(text)
            )
        )

    def test_baseline_project_status_cannot_claim_wp1_completion(self) -> None:
        text = VALIDATOR.DEFAULT_BASELINE.read_text(encoding="utf-8")
        text = text.replace(
            "  status: preparticipant_synthetic_g0_verified",
            "  status: wp1_complete",
        )
        self.assertTrue(
            any(
                "project.status must remain participant-neutral" in item
                for item in VALIDATOR._validate_baseline_text(text)
            )
        )

    def test_structurally_complete_fixture_still_grants_no_activity(self) -> None:
        value = self.structurally_complete_fixture()
        self.assertEqual(self.validate(value), [])
        self.assertFalse(any(value["authorizations"].values()))
        self.assertEqual(
            set(value["consent_scopes"].values()), {"not_authorized"}
        )


if __name__ == "__main__":
    unittest.main()
