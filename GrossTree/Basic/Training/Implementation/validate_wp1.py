#!/usr/bin/env python3
"""Fail-closed semantic validation for the NRLIS WP1 gate registry."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

try:
    import yaml
except ModuleNotFoundError:
    yaml = None


PROJECT_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_REGISTRY = (
    PROJECT_ROOT
    / "GrossTree"
    / "Basic"
    / "Training"
    / "Config"
    / "wp1_gate_registry.json"
)
DEFAULT_BASELINE = DEFAULT_REGISTRY.with_name("baseline_v0.yaml")

REQUIRED_GATE_IDS = {f"WP1-G{number:02d}" for number in range(1, 26)}
REQUIRED_ROLE_IDS = {
    "ROLE-ACCOUNTABLE-INVESTIGATOR",
    "ROLE-ETHICS-CONTACT",
    "ROLE-CONSENT-ACCESS-REVIEWER",
    "ROLE-SLP-CLINICAL-COLLABORATOR",
    "ROLE-TECHNICAL-LEAD",
    "ROLE-DATA-STEWARD",
    "ROLE-INDEPENDENT-EVENT-REVIEWER",
}
REQUIRED_ACTIVITY_KEYS = {
    "research_contact",
    "pre_consent_access_check",
    "enrollment",
    "participant_facing_intake",
    "non_recorded_capability_assessment",
    "audio_recording",
    "video_recording",
    "raw_gaze_recording",
    "derived_gaze_collection",
    "historical_media_ingest",
    "participant_data_training",
    "participant_specific_inference",
    "shadow_inference",
    "candidate_reveal",
    "voice_clone_training",
    "voice_rendering",
    "message_transmission",
    "demonstration",
    "publication_examples",
    "external_data_sharing",
    "future_secondary_use",
}
ACCEPTABLE_GATE_STATUSES = {"satisfied"}
GATE_RECORD_TYPES = {
    "WP1-G01": {"human_research_determination", "ethics_approval"},
    "WP1-G02": {
        "institutional_engagement_determination",
        "reliance_or_authorization_agreement",
    },
    "WP1-G03": {
        "site_or_jurisdiction_determination",
        "reliance_or_authorization_agreement",
    },
    "WP1-G04": {"device_or_ide_determination"},
    "WP1-G05": {"privacy_or_health_data_determination"},
    "WP1-G06": {"research_care_boundary_approval"},
    "WP1-G07": {"risk_or_safety_approval"},
    "WP1-G08": {"consent_process_approval"},
    "WP1-G09": {"capacity_and_lar_pathway_approval"},
    "WP1-G10": {"consent_process_approval"},
    "WP1-G11": {"consent_process_approval"},
    "WP1-G12": {"conflict_management_approval"},
    "WP1-G13": {"role_verification"},
    "WP1-G14": {"role_verification"},
    "WP1-G15": {"role_verification"},
    "WP1-G16": {"role_verification"},
    "WP1-G17": {"role_verification"},
    "WP1-G18": {"training_verification"},
    "WP1-G19": {"data_governance_approval"},
    "WP1-G20": {"data_governance_approval"},
    "WP1-G21": {"data_governance_approval"},
    "WP1-G22": {"data_governance_approval"},
    "WP1-G23": {"incident_response_approval"},
    "WP1-G24": {"activity_scope_approval"},
    "WP1-G25": {"independent_exit_review"},
}
GATE_AUTHORITY_TYPES = {
    "WP1-G01": {
        "institutional_irb_or_hrpp",
        "relying_institution",
        "legal_or_jurisdictional_authority",
    },
    "WP1-G02": {
        "institutional_irb_or_hrpp",
        "relying_institution",
        "legal_or_jurisdictional_authority",
    },
    "WP1-G03": {
        "institutional_irb_or_hrpp",
        "relying_institution",
        "legal_or_jurisdictional_authority",
    },
    "WP1-G04": {
        "institutional_irb_or_hrpp",
        "device_regulatory_authority",
    },
    "WP1-G05": {
        "institutional_irb_or_hrpp",
        "privacy_or_security_office",
        "legal_or_jurisdictional_authority",
    },
    "WP1-G06": {"institutional_irb_or_hrpp", "relying_institution"},
    "WP1-G07": {"institutional_irb_or_hrpp", "relying_institution"},
    "WP1-G08": {"institutional_irb_or_hrpp", "relying_institution"},
    "WP1-G09": {
        "institutional_irb_or_hrpp",
        "relying_institution",
        "legal_or_jurisdictional_authority",
    },
    "WP1-G10": {"institutional_irb_or_hrpp", "relying_institution"},
    "WP1-G11": {"institutional_irb_or_hrpp", "relying_institution"},
    "WP1-G12": {"institutional_irb_or_hrpp", "relying_institution"},
    "WP1-G13": {
        "institutional_irb_or_hrpp",
        "relying_institution",
        "independent_project_governance_body",
    },
    "WP1-G14": {
        "institutional_irb_or_hrpp",
        "relying_institution",
        "independent_project_governance_body",
    },
    "WP1-G15": {
        "institutional_irb_or_hrpp",
        "relying_institution",
        "independent_project_governance_body",
    },
    "WP1-G16": {
        "institutional_irb_or_hrpp",
        "relying_institution",
        "independent_project_governance_body",
    },
    "WP1-G17": {
        "institutional_irb_or_hrpp",
        "relying_institution",
        "independent_project_governance_body",
    },
    "WP1-G18": {
        "institutional_irb_or_hrpp",
        "relying_institution",
        "independent_project_governance_body",
    },
    "WP1-G19": {
        "institutional_irb_or_hrpp",
        "relying_institution",
        "privacy_or_security_office",
    },
    "WP1-G20": {
        "institutional_irb_or_hrpp",
        "relying_institution",
        "privacy_or_security_office",
    },
    "WP1-G21": {
        "institutional_irb_or_hrpp",
        "relying_institution",
        "privacy_or_security_office",
    },
    "WP1-G22": {
        "institutional_irb_or_hrpp",
        "relying_institution",
        "privacy_or_security_office",
    },
    "WP1-G23": {
        "institutional_irb_or_hrpp",
        "relying_institution",
        "privacy_or_security_office",
    },
    "WP1-G24": {"institutional_irb_or_hrpp", "relying_institution"},
    "WP1-G25": {
        "institutional_irb_or_hrpp",
        "relying_institution",
        "independent_project_governance_body",
    },
}
GATES_ALLOWING_NOT_APPLICABLE_OUTCOME = {
    "WP1-G01",
    "WP1-G02",
    "WP1-G03",
    "WP1-G04",
    "WP1-G05",
}
GATE_RECORDER_ROLES = {
    **{
        f"WP1-G{number:02d}": {"ROLE-ETHICS-CONTACT"}
        for number in range(1, 25)
    },
    "WP1-G25": {"ROLE-INDEPENDENT-EVENT-REVIEWER"},
}
ROLE_EVIDENCE_AUTHORITY_TYPES = {
    "institutional_irb_or_hrpp",
    "relying_institution",
    "independent_project_governance_body",
}
TRAINING_AUTHORITY_TYPES = {
    "institutional_irb_or_hrpp",
    "relying_institution",
    "training_provider",
}
REQUIRED_TRAINING_TYPES = {
    "ROLE-ACCOUNTABLE-INVESTIGATOR": {
        "human_research_protection",
        "protocol_accountability",
        "conflict_of_interest",
    },
    "ROLE-ETHICS-CONTACT": {
        "human_research_protection",
        "institutional_ethics_process",
    },
    "ROLE-CONSENT-ACCESS-REVIEWER": {
        "human_research_protection",
        "accessible_consent_and_capacity",
        "conflict_of_interest",
    },
    "ROLE-SLP-CLINICAL-COLLABORATOR": {
        "human_research_protection",
        "accessible_communication_and_aac",
        "participant_safety",
    },
    "ROLE-TECHNICAL-LEAD": {
        "human_research_protection",
        "privacy_data_security",
        "authorship_and_output_safety",
    },
    "ROLE-DATA-STEWARD": {
        "human_research_protection",
        "privacy_data_security",
        "incident_response",
    },
    "ROLE-INDEPENDENT-EVENT-REVIEWER": {
        "human_research_protection",
        "adverse_event_and_authorship_review",
        "conflict_of_interest",
    },
}
SCOPE_DOCUMENT_PATHS = (
    "GrossTree/__init__/PROJECT_CHARTER.md",
    "GrossTree/__init__/WP1_GOVERNANCE_AND_DETERMINATION_PLAN.md",
    "GrossTree/__init__/EVALUATION_SAFETY_GOVERNANCE.md",
    "GrossTree/Basic/Trials/NRLIS-T001/PROTOCOL.md",
    "GrossTree/Basic/Trials/NRLIS-T001/ACCESSIBLE_CONSENT_ASSENT_DISSENT_PLAN.md",
    "GrossTree/Basic/Trials/NRLIS-T001/TASK_REFERENCE_AUTHORSHIP_SOP.md",
    "GrossTree/Basic/Training/Dataset/DATA_CONTRACT.md",
    "GrossTree/Basic/Training/Dataset/DATA_MANAGEMENT_WITHDRAWAL_PLAN.md",
    "GrossTree/Basic/Training/Evaluation/METRICS.md",
    "GrossTree/Basic/Training/Evaluation/T001_ANALYSIS_SPEC.md",
)
REQUIRED_ROLE_SEPARATION = {
    "ROLE-ETHICS-CONTACT": {"ROLE-TECHNICAL-LEAD"},
    "ROLE-CONSENT-ACCESS-REVIEWER": {
        "ROLE-ACCOUNTABLE-INVESTIGATOR",
        "ROLE-TECHNICAL-LEAD",
    },
    "ROLE-SLP-CLINICAL-COLLABORATOR": {"ROLE-TECHNICAL-LEAD"},
    "ROLE-DATA-STEWARD": {"ROLE-TECHNICAL-LEAD"},
    "ROLE-INDEPENDENT-EVENT-REVIEWER": {
        "ROLE-ACCOUNTABLE-INVESTIGATOR",
        "ROLE-TECHNICAL-LEAD",
    },
}
REQUIRED_INDEPENDENCE = {
    "ROLE-ACCOUNTABLE-INVESTIGATOR": False,
    "ROLE-ETHICS-CONTACT": True,
    "ROLE-CONSENT-ACCESS-REVIEWER": True,
    "ROLE-SLP-CLINICAL-COLLABORATOR": True,
    "ROLE-TECHNICAL-LEAD": False,
    "ROLE-DATA-STEWARD": True,
    "ROLE-INDEPENDENT-EVENT-REVIEWER": True,
}
FORBIDDEN_BASELINE_WP1_STATE_KEYS = {
    "wp1_gate_registry",
    "wp1_status",
    "wp1_exit_authorized",
    "participant_facing_research_authorized",
    "external_determination_status",
    "required_roles_verified",
    "accessible_consent_path_approved",
    "storage_and_withdrawal_plan_approved",
    "active_hold",
}
EXPECTED_BASELINE_REGISTRY = (
    "GrossTree/Basic/Training/Config/wp1_gate_registry.json"
)
EXPECTED_BASELINE_VALIDATOR = (
    "GrossTree/Basic/Training/Implementation/validate_wp1.py"
)
REGISTRY_SCHEMA_VERSION = "1.2"
SCOPE_MANIFEST_VERSION = "1.1"
ALLOWED_BASELINE_WP1_KEYS = {
    "wp1_governance_plan_version",
    "wp1_gate_registry_version",
    "wp1_gate_registry_schema_version",
    "wp1_scope_manifest_version",
    "wp1_authoritative_registry",
    "wp1_semantic_validator",
}
BASELINE_DENY_INTERLOCKS = {
    "participant.enrollment_status": "not_enrolled",
    "protocol.authorization_semantics": "deny_only_interlock",
    "protocol.output_enabled": False,
    "protocol.enrollment_open": False,
    "protocol.participant_recording_enabled": False,
    "protocol.stage_d_enabled": False,
    "boundaries.diagnosis_enabled": False,
    "boundaries.thought_reading_claim_enabled": False,
    "boundaries.high_risk_generation_enabled": False,
    "boundaries.unsupervised_personal_update_enabled": False,
    "boundaries.bci_core_enabled": False,
    "boundaries.semg_core_enabled": False,
    "boundaries.eeg_core_enabled": False,
    "learning.post_reveal_selection_training_enabled": False,
}
ALLOWED_BASELINE_ENABLED_KEYS = {
    qualified
    for qualified in BASELINE_DENY_INTERLOCKS
    if qualified.split(".", 1)[1].endswith("_enabled")
}
BASELINE_DOCUMENT_VERSION_FIELDS = {
    "contracts.project_charter_version": (
        "GrossTree/__init__/PROJECT_CHARTER.md",
        "Version",
    ),
    "contracts.wp1_governance_plan_version": (
        "GrossTree/__init__/WP1_GOVERNANCE_AND_DETERMINATION_PLAN.md",
        "Version",
    ),
    "contracts.evaluation_safety_governance_version": (
        "GrossTree/__init__/EVALUATION_SAFETY_GOVERNANCE.md",
        "Version",
    ),
    "contracts.accessible_consent_plan_version": (
        "GrossTree/Basic/Trials/NRLIS-T001/"
        "ACCESSIBLE_CONSENT_ASSENT_DISSENT_PLAN.md",
        "Version",
    ),
    "contracts.data_contract_version": (
        "GrossTree/Basic/Training/Dataset/DATA_CONTRACT.md",
        "Version",
    ),
    "contracts.data_management_withdrawal_plan_version": (
        "GrossTree/Basic/Training/Dataset/"
        "DATA_MANAGEMENT_WITHDRAWAL_PLAN.md",
        "Version",
    ),
    "contracts.task_reference_authorship_sop_version": (
        "GrossTree/Basic/Trials/NRLIS-T001/"
        "TASK_REFERENCE_AUTHORSHIP_SOP.md",
        "Version",
    ),
    "contracts.t001_analysis_spec_version": (
        "GrossTree/Basic/Training/Evaluation/T001_ANALYSIS_SPEC.md",
        "Version",
    ),
    "contracts.metrics_version": (
        "GrossTree/Basic/Training/Evaluation/METRICS.md",
        "Version",
    ),
}


def _duplicates(values: list[str]) -> set[str]:
    """Return repeated non-empty strings."""

    return {value for value, count in Counter(values).items() if value and count > 1}


def _protocol_version(project_root: Path = PROJECT_ROOT) -> str:
    """Read the actual T001 protocol version from the normative document."""

    protocol_path = (
        project_root
        / "GrossTree"
        / "Basic"
        / "Trials"
        / "NRLIS-T001"
        / "PROTOCOL.md"
    )
    match = re.search(
        r"^\*\*Protocol version:\*\*\s*([0-9]+\.[0-9]+)\s*$",
        protocol_path.read_text(encoding="utf-8"),
        flags=re.MULTILINE,
    )
    if match is None:
        raise ValueError("Could not read the normative T001 protocol version")
    return match.group(1)


def build_scope_manifest(project_root: Path = PROJECT_ROOT) -> dict[str, Any]:
    """Build the canonical, participant-free determination-scope manifest."""

    documents = []
    for relative_path in SCOPE_DOCUMENT_PATHS:
        content = (project_root / relative_path).read_bytes()
        documents.append(
            {
                "path": relative_path,
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )
    return {
        "manifest_version": SCOPE_MANIFEST_VERSION,
        "protocol_id": "NRLIS-T001",
        "protocol_version": _protocol_version(project_root),
        "registry_schema_version": REGISTRY_SCHEMA_VERSION,
        "activity_keys": sorted(REQUIRED_ACTIVITY_KEYS),
        "documents": documents,
    }


def compute_scope_sha256(project_root: Path = PROJECT_ROOT) -> str:
    """Hash the canonical determination-scope manifest."""

    encoded = json.dumps(
        build_scope_manifest(project_root),
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _optional_date(value: Any, label: str, errors: list[str]) -> date | None:
    """Parse an optional ISO date and report malformed values."""

    if value is None:
        return None
    if not isinstance(value, str):
        errors.append(f"{label} must be an ISO date or null")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"{label} is not a valid ISO date")
        return None


def _require_current_record(
    record: dict[str, Any],
    label: str,
    today: date,
    errors: list[str],
    *,
    start_field: str,
) -> bool:
    """Return whether an authority/evidence/training record is currently valid."""

    status = record.get("status")
    start_on = _optional_date(record.get(start_field), f"{label}.{start_field}", errors)
    review_due_on = _optional_date(
        record.get("review_due_on"), f"{label}.review_due_on", errors
    )
    expires_on = _optional_date(
        record.get("expires_on"), f"{label}.expires_on", errors
    )
    revoked_on = _optional_date(
        record.get("revoked_on"), f"{label}.revoked_on", errors
    )

    if status in {"verified", "active", "valid"}:
        valid = True
        if start_on is None:
            errors.append(f"{label} {status} without {start_field}")
            valid = False
        elif start_on > today:
            errors.append(f"{label} {status} before {start_field}")
            valid = False
        if review_due_on is None:
            errors.append(f"{label} {status} without review_due_on")
            valid = False
        elif review_due_on <= today:
            errors.append(f"{label} {status} has reached review_due_on")
            valid = False
        if expires_on is not None and expires_on <= today:
            errors.append(f"{label} {status} has expired")
            valid = False
        if revoked_on is not None:
            errors.append(f"{label} {status} has revoked_on")
            valid = False
        return valid

    if status == "revoked":
        if revoked_on is None or revoked_on > today:
            errors.append(f"{label} revoked without a current or past revoked_on")
        return False
    if status == "expired":
        if (
            (expires_on is None or expires_on > today)
            and (review_due_on is None or review_due_on > today)
        ):
            errors.append(f"{label} expired without a reached expiry/review date")
        return False
    if status in {"pending", "superseded"}:
        return False

    errors.append(f"{label} has unsupported status {status!r}")
    return False


def _record_ids(
    records: Any,
    collection_name: str,
    errors: list[str],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """Validate an object array enough to build a unique record-id index."""

    if not isinstance(records, list):
        errors.append(f"{collection_name} must be an array")
        return [], {}
    normalized: list[dict[str, Any]] = []
    ids: list[str] = []
    for record in records:
        if not isinstance(record, dict):
            errors.append(f"each {collection_name} entry must be an object")
            continue
        normalized.append(record)
        ids.append(record.get("record_id", ""))
    duplicates = _duplicates(ids)
    if duplicates:
        errors.append(
            f"duplicate {collection_name} record IDs: "
            + ", ".join(sorted(duplicates))
        )
    return normalized, {
        record["record_id"]: record
        for record in normalized
        if isinstance(record.get("record_id"), str) and record.get("record_id")
    }


def _baseline_fields(text: str) -> tuple[dict[str, Any], list[str]]:
    """Safely parse YAML and flatten every mapping leaf with strict types."""

    errors: list[str] = []
    fields: dict[str, Any] = {}
    if yaml is None:
        errors.append(
            "baseline_v0.yaml validation requires PyYAML; install requirements.txt"
        )
        return fields, errors

    class UniqueKeySafeLoader(yaml.SafeLoader):
        """SafeLoader variant that rejects duplicate and merge keys."""

    def construct_unique_mapping(
        loader: Any,
        node: Any,
        deep: bool = False,
    ) -> dict[Any, Any]:
        if not isinstance(node, yaml.MappingNode):
            raise yaml.constructor.ConstructorError(
                None,
                None,
                "expected a mapping node",
                node.start_mark,
            )
        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            if key_node.tag == "tag:yaml.org,2002:merge":
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    "YAML merge keys are not allowed",
                    key_node.start_mark,
                )
            key = loader.construct_object(key_node, deep=deep)
            try:
                already_seen = key in mapping
            except TypeError as exc:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    "found an unhashable mapping key",
                    key_node.start_mark,
                ) from exc
            if already_seen:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    f"found duplicate key {key!r}",
                    key_node.start_mark,
                )
            mapping[key] = loader.construct_object(value_node, deep=deep)
        return mapping

    UniqueKeySafeLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_unique_mapping,
    )
    try:
        root = yaml.load(text, Loader=UniqueKeySafeLoader)
    except yaml.YAMLError as exc:
        errors.append(f"baseline_v0.yaml is not safe, valid YAML: {exc}")
        return fields, errors
    if not isinstance(root, dict):
        errors.append("baseline_v0.yaml root must be a mapping")
        return fields, errors

    seen_containers: set[int] = set()

    def visit(value: Any, path: str) -> None:
        if isinstance(value, dict):
            identity = id(value)
            if identity in seen_containers:
                errors.append(
                    f"baseline_v0.yaml contains an alias or recursive mapping at {path}"
                )
                return
            seen_containers.add(identity)
            for key, child in value.items():
                if not isinstance(key, str):
                    errors.append(
                        f"baseline_v0.yaml mapping key at {path or '<root>'} "
                        "must be a string"
                    )
                    continue
                if re.fullmatch(r"[a-z0-9_]+", key) is None:
                    errors.append(
                        f"baseline_v0.yaml mapping key {key!r} at "
                        f"{path or '<root>'} must use lowercase snake_case"
                    )
                    continue
                qualified = f"{path}.{key}" if path else key
                visit(child, qualified)
            return
        if isinstance(value, list):
            identity = id(value)
            if identity in seen_containers:
                errors.append(
                    f"baseline_v0.yaml contains an alias or recursive list at {path}"
                )
                return
            seen_containers.add(identity)
            for index, child in enumerate(value):
                visit(child, f"{path}[{index}]")
            return
        if path in fields:
            errors.append(f"baseline_v0.yaml duplicates path {path}")
        fields[path] = value

    visit(root, "")
    return fields, errors


def _validate_baseline_text(text: str) -> list[str]:
    """Enforce registry pointers and deny-only executable interlocks."""

    fields, errors = _baseline_fields(text)
    governance = {
        qualified.split(".", 1)[1]: value
        for qualified, value in fields.items()
        if qualified.startswith("governance.")
    }
    def leaf_name(qualified: str) -> str:
        return qualified.rsplit(".", 1)[-1]

    forbidden_seen = {
        leaf_name(qualified)
        for qualified in fields
        if leaf_name(qualified) in FORBIDDEN_BASELINE_WP1_STATE_KEYS
    }
    unapproved_wp1_keys = sorted(
        qualified
        for qualified in fields
        if "wp1" in leaf_name(qualified)
        and leaf_name(qualified) not in ALLOWED_BASELINE_WP1_KEYS
    )
    embedded_wp1_state = sorted(
        qualified
        for qualified, value in fields.items()
        if isinstance(value, str)
        and "wp1" in value.lower()
        and leaf_name(qualified) not in ALLOWED_BASELINE_WP1_KEYS
    )
    duplicate_activity_state = sorted(
        qualified
        for qualified in fields
        if leaf_name(qualified) in REQUIRED_ACTIVITY_KEYS
    )
    unknown_enabled_fields = sorted(
        qualified
        for qualified in fields
        if leaf_name(qualified).endswith("_enabled")
        and qualified not in ALLOWED_BASELINE_ENABLED_KEYS
    )

    if not governance:
        errors.append("baseline_v0.yaml must contain a governance block")
    forbidden = sorted(forbidden_seen)
    if forbidden:
        errors.append(
            "baseline_v0.yaml duplicates authoritative WP1 state fields: "
            + ", ".join(forbidden)
        )
    if unapproved_wp1_keys:
        errors.append(
            "baseline_v0.yaml contains unapproved WP1 keys: "
            + ", ".join(unapproved_wp1_keys)
        )
    if embedded_wp1_state:
        errors.append(
            "baseline_v0.yaml embeds derived WP1 state outside the registry: "
            + ", ".join(embedded_wp1_state)
        )
    if duplicate_activity_state:
        errors.append(
            "baseline_v0.yaml duplicates authoritative activity state: "
            + ", ".join(duplicate_activity_state)
        )
    if unknown_enabled_fields:
        errors.append(
            "baseline_v0.yaml contains unknown executable enabled flags: "
            + ", ".join(unknown_enabled_fields)
        )
    if (
        type(governance.get("wp1_authoritative_registry")) is not str
        or governance.get("wp1_authoritative_registry")
        != EXPECTED_BASELINE_REGISTRY
    ):
        errors.append("baseline_v0.yaml has an invalid WP1 registry pointer")
    if (
        type(governance.get("wp1_semantic_validator")) is not str
        or governance.get("wp1_semantic_validator")
        != EXPECTED_BASELINE_VALIDATOR
    ):
        errors.append("baseline_v0.yaml has an invalid WP1 validator pointer")
    if governance.get("activity_authorization_inherited") is not False:
        errors.append(
            "baseline_v0.yaml must retain activity_authorization_inherited=false"
        )
    if (
        type(fields.get("project.status")) is not str
        or fields.get("project.status") != "preparticipant_synthetic_g0_verified"
    ):
        errors.append(
            "baseline_v0.yaml project.status must remain participant-neutral"
        )
    for qualified, expected in BASELINE_DENY_INTERLOCKS.items():
        actual = fields.get(qualified)
        if type(actual) is not type(expected) or actual != expected:
            expected_text = (
                str(expected).lower()
                if isinstance(expected, bool)
                else str(expected)
            )
            errors.append(
                f"baseline_v0.yaml {qualified} must remain {expected_text}; "
                "the baseline is a deny-only interlock"
            )
    return errors


def _document_version(relative_path: str, label: str) -> str:
    """Read one Markdown **Version:**-style field."""

    text = (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")
    match = re.search(
        rf"^\*\*{re.escape(label)}:\*\*\s*([0-9]+(?:\.[0-9]+)+)\s*$",
        text,
        flags=re.MULTILINE,
    )
    if match is None:
        raise ValueError(f"Could not read {label} from {relative_path}")
    return match.group(1)


def validate_baseline_reference(
    path: Path = DEFAULT_BASELINE,
    registry: dict[str, Any] | None = None,
) -> list[str]:
    """Validate baseline interlocks and cross-file version references."""

    text = path.read_text(encoding="utf-8")
    errors = _validate_baseline_text(text)
    if registry is None:
        return errors
    fields, parse_errors = _baseline_fields(text)
    errors.extend(parse_errors)
    scope = registry.get("determination_scope", {})
    expected_pairs = {
        "protocol.id": scope.get("protocol_id"),
        "protocol.version": scope.get("protocol_version"),
        "contracts.wp1_gate_registry_version": registry.get("registry_version"),
        "contracts.wp1_gate_registry_schema_version": registry.get(
            "schema_version"
        ),
        "contracts.wp1_scope_manifest_version": scope.get("manifest_version"),
    }
    for qualified, expected in expected_pairs.items():
        actual = fields.get(qualified)
        if type(actual) is not type(expected) or actual != expected:
            errors.append(
                f"baseline_v0.yaml {qualified} does not match the "
                "authoritative registry"
            )
    for qualified, (relative_path, label) in (
        BASELINE_DOCUMENT_VERSION_FIELDS.items()
    ):
        expected = _document_version(relative_path, label)
        actual = fields.get(qualified)
        if type(actual) is not str or actual != expected:
            errors.append(
                f"baseline_v0.yaml {qualified} does not match {relative_path}"
            )
    return errors


def validate_registry(registry: dict[str, Any]) -> list[str]:
    """Return semantic validation errors for one parsed WP1 registry."""

    errors: list[str] = []
    today = date.today()

    if registry.get("schema_version") != REGISTRY_SCHEMA_VERSION:
        errors.append(f"schema_version must be {REGISTRY_SCHEMA_VERSION}")
    if registry.get("work_package") != "WP1":
        errors.append("work_package must be WP1")
    if registry.get("earned_claim_level") != "G0_component_verified_synthetic_only":
        errors.append("WP1 must not increase the earned claim level")
    if registry.get("participant_evidence_level") != "none":
        errors.append("WP1 preparation must retain participant_evidence_level=none")

    authorizations = registry.get("authorizations", {})
    if not isinstance(authorizations, dict):
        errors.append("authorizations must be an object")
        authorizations = {}
    elif set(authorizations) != REQUIRED_ACTIVITY_KEYS:
        errors.append("authorizations do not match the frozen activity key set")
    enabled = sorted(
        key for key, value in authorizations.items() if value is not False
    )
    if enabled:
        errors.append(
            "WP1 cannot grant activity authorization; non-false fields: "
            + ", ".join(enabled)
        )

    consent_scopes = registry.get("consent_scopes", {})
    if not isinstance(consent_scopes, dict):
        errors.append("consent_scopes must be an object")
        consent_scopes = {}
    elif set(consent_scopes) != REQUIRED_ACTIVITY_KEYS:
        errors.append("consent_scopes do not match the frozen activity key set")
    opened_scopes = sorted(
        key
        for key, value in consent_scopes.items()
        if value != "not_authorized"
    )
    if opened_scopes:
        errors.append(
            "WP1 planning cannot record participant permission; opened scopes: "
            + ", ".join(opened_scopes)
        )
    if set(consent_scopes) != set(authorizations):
        errors.append("consent_scopes and authorizations must use identical keys")

    scope = registry.get("determination_scope", {})
    if not isinstance(scope, dict):
        errors.append("determination_scope must be an object")
        scope = {}
    protocol_id = scope.get("protocol_id")
    protocol_version = scope.get("protocol_version")
    scope_sha256 = scope.get("scope_sha256")
    if scope.get("manifest_version") != SCOPE_MANIFEST_VERSION:
        errors.append("determination_scope manifest_version is not current")
    if tuple(scope.get("document_paths", [])) != SCOPE_DOCUMENT_PATHS:
        errors.append("determination_scope document_paths are not canonical")
    actual_protocol_version = _protocol_version()
    if protocol_id != "NRLIS-T001" or protocol_version != actual_protocol_version:
        errors.append(
            "determination_scope protocol does not match the normative T001 document"
        )
    expected_scope_sha256 = compute_scope_sha256()
    if scope_sha256 is not None and scope_sha256 != expected_scope_sha256:
        errors.append(
            "determination_scope scope_sha256 does not match the canonical "
            "document manifest"
        )

    def matches_current_scope(record: dict[str, Any]) -> bool:
        return bool(
            scope_sha256
            and record.get("protocol_id") == protocol_id
            and record.get("protocol_version") == protocol_version
            and record.get("scope_sha256") == scope_sha256
        )

    roles = registry.get("roles", [])
    if not isinstance(roles, list):
        errors.append("roles must be an array")
        roles = []
    role_ids = [
        role.get("role_id", "") for role in roles if isinstance(role, dict)
    ]
    duplicate_roles = _duplicates(role_ids)
    if duplicate_roles:
        errors.append("duplicate role IDs: " + ", ".join(sorted(duplicate_roles)))
    if set(role_ids) != REQUIRED_ROLE_IDS:
        missing = sorted(REQUIRED_ROLE_IDS - set(role_ids))
        extra = sorted(set(role_ids) - REQUIRED_ROLE_IDS)
        if missing:
            errors.append("missing required roles: " + ", ".join(missing))
        if extra:
            errors.append("unexpected WP1 roles: " + ", ".join(extra))
    role_by_id = {
        role["role_id"]: role
        for role in roles
        if isinstance(role, dict) and role.get("role_id")
    }

    authorities = registry.get("external_authorities", [])
    if not isinstance(authorities, list):
        errors.append("external_authorities must be an array")
        authorities = []
    authority_ids = [
        item.get("authority_id", "")
        for item in authorities
        if isinstance(item, dict)
    ]
    duplicate_authorities = _duplicates(authority_ids)
    if duplicate_authorities:
        errors.append(
            "duplicate external authority IDs: "
            + ", ".join(sorted(duplicate_authorities))
        )
    authority_by_id = {
        item["authority_id"]: item
        for item in authorities
        if isinstance(item, dict) and item.get("authority_id")
    }
    valid_authority_ids: set[str] = set()
    for authority_id, authority in authority_by_id.items():
        if _require_current_record(
            authority,
            authority_id,
            today,
            errors,
            start_field="verified_on",
        ):
            valid_authority_ids.add(authority_id)

    evidence_records, evidence_by_id = _record_ids(
        registry.get("external_evidence_records", []),
        "external_evidence_records",
        errors,
    )
    valid_evidence_ids: set[str] = set()
    for record in evidence_records:
        record_id = record.get("record_id", "<missing-evidence>")
        issuer = record.get("issuer_authority_id")
        recorder = record.get("recorded_by_role_id")
        record_type = record.get("record_type")
        if issuer not in authority_by_id:
            errors.append(f"{record_id} cites unknown issuing authority {issuer}")
        if recorder not in role_by_id:
            errors.append(f"{record_id} cites unknown recording role {recorder}")
        issuer_eligible = True
        if record_type in {
            "role_appointment",
            "independence_review",
            "role_combination_approval",
        } and authority_by_id.get(issuer, {}).get(
            "authority_type"
        ) not in ROLE_EVIDENCE_AUTHORITY_TYPES:
            errors.append(
                f"{record_id} role evidence has an ineligible authority type"
            )
            issuer_eligible = False
        current = _require_current_record(
            record,
            record_id,
            today,
            errors,
            start_field="effective_on",
        )
        if current and issuer in valid_authority_ids and issuer_eligible:
            valid_evidence_ids.add(record_id)

    training_records, training_by_id = _record_ids(
        registry.get("training_records", []),
        "training_records",
        errors,
    )
    valid_training_ids: set[str] = set()
    for record in training_records:
        record_id = record.get("record_id", "<missing-training>")
        issuer = record.get("issuer_authority_id")
        if issuer not in authority_by_id:
            errors.append(f"{record_id} cites unknown training issuer {issuer}")
        issuer_eligible = authority_by_id.get(issuer, {}).get(
            "authority_type"
        ) in TRAINING_AUTHORITY_TYPES
        if issuer in authority_by_id and not issuer_eligible:
            errors.append(f"{record_id} has an ineligible training authority type")
        current = _require_current_record(
            record,
            record_id,
            today,
            errors,
            start_field="completed_on",
        )
        if current and issuer in valid_authority_ids and issuer_eligible:
            valid_training_ids.add(record_id)

    invalid_role_ids: set[str] = set()
    holder_to_roles: dict[str, list[dict[str, Any]]] = {}
    for role in roles:
        if not isinstance(role, dict):
            errors.append("each role must be an object")
            continue
        role_id = role.get("role_id", "<missing-role>")
        status = role.get("status")
        holder_id = role.get("holder_id")
        appointment = role.get("appointment_record_id")
        training = role.get("training_record_ids", [])
        independence_required = role.get("independence_required")
        independence_record = role.get("independence_record_id")
        combination_record = role.get("combination_approval_record_id")
        required_separation = REQUIRED_ROLE_SEPARATION.get(role_id, set())
        declared_separation = set(role.get("must_be_distinct_from_role_ids", []))
        required_training_types = REQUIRED_TRAINING_TYPES.get(role_id, set())
        declared_training_types = set(role.get("required_training_types", []))
        required_independence = REQUIRED_INDEPENDENCE.get(role_id)
        expires_on = _optional_date(
            role.get("expires_on"), f"{role_id}.expires_on", errors
        )

        if declared_separation != required_separation:
            errors.append(f"{role_id} role-separation policy is not frozen")
            invalid_role_ids.add(role_id)
        if declared_training_types != required_training_types:
            errors.append(f"{role_id} required training policy is not frozen")
            invalid_role_ids.add(role_id)
        if independence_required is not required_independence:
            errors.append(f"{role_id} independence policy is not frozen")
            invalid_role_ids.add(role_id)
        if status == "verified":
            role_valid = True
            if not holder_id:
                errors.append(f"{role_id} verified without stable holder_id")
                role_valid = False
            if not appointment:
                errors.append(f"{role_id} verified without appointment evidence")
                role_valid = False
            elif appointment not in valid_evidence_ids:
                errors.append(f"{role_id} appointment evidence is not current")
                role_valid = False
            else:
                record = evidence_by_id[appointment]
                if record.get("record_type") != "role_appointment":
                    errors.append(f"{role_id} appointment has wrong record type")
                    role_valid = False
                if record.get("decision_outcome") != "requirements_satisfied":
                    errors.append(f"{role_id} appointment outcome is not valid")
                    role_valid = False
                if record.get("subject_holder_id") != holder_id:
                    errors.append(f"{role_id} appointment does not bind its holder_id")
                    role_valid = False
                if role_id not in record.get("covered_role_ids", []):
                    errors.append(f"{role_id} appointment does not cover the role")
                    role_valid = False
                recorder_role = role_by_id.get(record.get("recorded_by_role_id"), {})
                if (
                    recorder_role.get("status") != "verified"
                    or recorder_role.get("holder_id")
                    != record.get("recorded_by_holder_id")
                ):
                    errors.append(
                        f"{role_id} appointment recorder holder is not current"
                    )
                    role_valid = False
                if not matches_current_scope(record):
                    errors.append(
                        f"{role_id} appointment is not bound to the current "
                        "protocol scope"
                    )
                    role_valid = False
            if not training:
                errors.append(f"{role_id} verified without training evidence")
                role_valid = False
            observed_training_types: set[str] = set()
            for training_id in training:
                if training_id not in valid_training_ids:
                    errors.append(f"{role_id} training {training_id} is not current")
                    role_valid = False
                else:
                    training_record = training_by_id[training_id]
                    if training_record.get("holder_id") != holder_id:
                        errors.append(
                            f"{role_id} training {training_id} does not bind "
                            "its holder_id"
                        )
                        role_valid = False
                    if role_id not in training_record.get("covered_role_ids", []):
                        errors.append(
                            f"{role_id} training {training_id} does not cover the role"
                        )
                        role_valid = False
                    observed_training_types.add(
                        training_record.get("training_type")
                    )
            missing_training_types = sorted(
                required_training_types - observed_training_types
            )
            if missing_training_types:
                errors.append(
                    f"{role_id} lacks required training type(s): "
                    + ", ".join(missing_training_types)
                )
                role_valid = False
            if independence_required:
                if not independence_record:
                    errors.append(f"{role_id} verified without independence evidence")
                    role_valid = False
                elif independence_record not in valid_evidence_ids:
                    errors.append(f"{role_id} independence evidence is not current")
                    role_valid = False
                else:
                    record = evidence_by_id[independence_record]
                    if record.get("record_type") != "independence_review":
                        errors.append(
                            f"{role_id} independence evidence has wrong record type"
                        )
                        role_valid = False
                    if record.get("decision_outcome") != "requirements_satisfied":
                        errors.append(
                            f"{role_id} independence outcome is not valid"
                        )
                        role_valid = False
                    if record.get("subject_holder_id") != holder_id:
                        errors.append(
                            f"{role_id} independence evidence does not bind its holder_id"
                        )
                        role_valid = False
                    if role_id not in record.get("covered_role_ids", []):
                        errors.append(
                            f"{role_id} independence evidence does not cover the role"
                        )
                        role_valid = False
                    recorder_role = role_by_id.get(
                        record.get("recorded_by_role_id"), {}
                    )
                    if (
                        recorder_role.get("status") != "verified"
                        or recorder_role.get("holder_id")
                        != record.get("recorded_by_holder_id")
                    ):
                        errors.append(
                            f"{role_id} independence recorder holder is not current"
                        )
                        role_valid = False
                    if not matches_current_scope(record):
                        errors.append(
                            f"{role_id} independence evidence is not bound to "
                            "the current protocol scope"
                        )
                        role_valid = False
            if expires_on is None:
                errors.append(f"{role_id} verified without a finite expires_on")
                role_valid = False
            elif expires_on <= today:
                errors.append(f"{role_id} verified role has expired")
                role_valid = False
            if not role_valid:
                invalid_role_ids.add(role_id)
        elif status == "unassigned":
            if (
                holder_id
                or appointment
                or training
                or independence_record
                or combination_record
                or expires_on
            ):
                errors.append(f"{role_id} unassigned but carries assignment evidence")
                invalid_role_ids.add(role_id)
        elif status == "expired":
            if expires_on is None or expires_on > today:
                errors.append(f"{role_id} expired without a reached expires_on")
        if holder_id:
            holder_to_roles.setdefault(holder_id, []).append(role)

    for holder_id, combined_roles in holder_to_roles.items():
        combined_ids = {
            role.get("role_id", "<missing-role>") for role in combined_roles
        }
        for role in combined_roles:
            role_id = role.get("role_id", "<missing-role>")
            prohibited = set(role.get("must_be_distinct_from_role_ids", []))
            conflicts = sorted(prohibited & combined_ids)
            if conflicts:
                errors.append(
                    f"{role_id} holder {holder_id} conflicts with required distinct "
                    "role(s): " + ", ".join(conflicts)
                )
                invalid_role_ids.add(role_id)
                invalid_role_ids.update(conflicts)
        if len(combined_roles) < 2:
            continue
        approvals = {
            role.get("combination_approval_record_id") for role in combined_roles
        }
        if None in approvals or len(approvals) != 1:
            errors.append(
                f"combined holder {holder_id} for {', '.join(sorted(combined_ids))} "
                "lacks one shared combination approval"
            )
            invalid_role_ids.update(combined_ids)
            continue
        approval_id = next(iter(approvals))
        if approval_id not in valid_evidence_ids:
            errors.append(f"combined holder {holder_id} approval is not current")
            invalid_role_ids.update(combined_ids)
        else:
            approval = evidence_by_id[approval_id]
            if approval.get("record_type") != "role_combination_approval":
                errors.append(
                    f"combined holder {holder_id} approval has wrong record type"
                )
                invalid_role_ids.update(combined_ids)
            if approval.get("decision_outcome") != "requirements_satisfied":
                errors.append(
                    f"combined holder {holder_id} approval outcome is not valid"
                )
                invalid_role_ids.update(combined_ids)
            if approval.get("subject_holder_id") != holder_id:
                errors.append(
                    f"combined holder {holder_id} approval does not bind holder_id"
                )
                invalid_role_ids.update(combined_ids)
            if set(approval.get("covered_role_ids", [])) != combined_ids:
                errors.append(
                    f"combined holder {holder_id} approval does not cover exactly "
                    "the combined roles"
                )
                invalid_role_ids.update(combined_ids)
            recorder_role = role_by_id.get(
                approval.get("recorded_by_role_id"), {}
            )
            if (
                recorder_role.get("status") != "verified"
                or recorder_role.get("holder_id")
                != approval.get("recorded_by_holder_id")
            ):
                errors.append(
                    f"combined holder {holder_id} approval recorder is not current"
                )
                invalid_role_ids.update(combined_ids)
            if not matches_current_scope(approval):
                errors.append(
                    f"combined holder {holder_id} approval is not bound to the "
                    "current protocol scope"
                )
                invalid_role_ids.update(combined_ids)

    gates = registry.get("gates", [])
    if not isinstance(gates, list):
        errors.append("gates must be an array")
        gates = []
    gate_ids = [
        gate.get("gate_id", "") for gate in gates if isinstance(gate, dict)
    ]
    duplicate_gates = _duplicates(gate_ids)
    if duplicate_gates:
        errors.append("duplicate gate IDs: " + ", ".join(sorted(duplicate_gates)))
    if set(gate_ids) != REQUIRED_GATE_IDS:
        missing = sorted(REQUIRED_GATE_IDS - set(gate_ids))
        extra = sorted(set(gate_ids) - REQUIRED_GATE_IDS)
        if missing:
            errors.append("missing required gates: " + ", ".join(missing))
        if extra:
            errors.append("unexpected WP1 gates: " + ", ".join(extra))

    gates_by_id: dict[str, dict[str, Any]] = {}
    invalid_gate_ids: set[str] = set()
    for gate in gates:
        if not isinstance(gate, dict):
            errors.append("each gate must be an object")
            continue
        gate_id = gate.get("gate_id", "<missing-gate>")
        gates_by_id[gate_id] = gate
        status = gate.get("status")
        evidence_ids = gate.get("evidence_record_ids", [])
        recorder = gate.get("recorded_by_role_id")
        recorder_holder = gate.get("recorded_by_holder_id")
        issuer_ids = set(gate.get("issuing_authority_ids", []))
        decided_on = _optional_date(
            gate.get("decided_on"), f"{gate_id}.decided_on", errors
        )
        review_due_on = _optional_date(
            gate.get("review_due_on"), f"{gate_id}.review_due_on", errors
        )
        expires_on = _optional_date(
            gate.get("expires_on"), f"{gate_id}.expires_on", errors
        )

        if status == "not_applicable":
            errors.append(
                f"{gate_id} gate status cannot be not_applicable; record the "
                "external decision outcome and satisfy the determination gate"
            )
            invalid_gate_ids.add(gate_id)
        if status in ACCEPTABLE_GATE_STATUSES:
            gate_valid = True
            if not evidence_ids:
                errors.append(f"{gate_id} {status} without evidence")
                gate_valid = False
            if not recorder:
                errors.append(f"{gate_id} {status} without recording role")
                gate_valid = False
            elif recorder not in role_by_id:
                errors.append(f"{gate_id} cites unknown recording role {recorder}")
                gate_valid = False
            elif role_by_id[recorder].get("status") != "verified":
                errors.append(
                    f"{gate_id} {status} recording role {recorder} is not verified"
                )
                gate_valid = False
            elif (
                not recorder_holder
                or role_by_id[recorder].get("holder_id") != recorder_holder
            ):
                errors.append(
                    f"{gate_id} recording holder does not match the current "
                    f"{recorder} holder"
                )
                gate_valid = False
            if decided_on is None:
                errors.append(f"{gate_id} {status} without decision date")
                gate_valid = False
            elif decided_on > today:
                errors.append(f"{gate_id} decision date is in the future")
                gate_valid = False
            if review_due_on is None:
                errors.append(f"{gate_id} {status} without review_due_on")
                gate_valid = False
            elif review_due_on <= today:
                errors.append(f"{gate_id} {status} has reached review_due_on")
                gate_valid = False
            if expires_on is not None and expires_on <= today:
                errors.append(f"{gate_id} {status} has expired")
                gate_valid = False

            records: list[dict[str, Any]] = []
            for evidence_id in evidence_ids:
                if evidence_id not in valid_evidence_ids:
                    errors.append(
                        f"{gate_id} evidence {evidence_id} is absent, inactive, "
                        "expired, revoked, or issued by an unverified authority"
                    )
                    gate_valid = False
                    continue
                record = evidence_by_id[evidence_id]
                records.append(record)
                if gate_id not in record.get("covered_gate_ids", []):
                    errors.append(
                        f"{gate_id} evidence {evidence_id} does not cover the gate"
                    )
                    gate_valid = False
                if record.get("recorded_by_role_id") != recorder:
                    errors.append(
                        f"{gate_id} evidence {evidence_id} recording role mismatch"
                    )
                    gate_valid = False
                if (
                    record.get("recorded_by_holder_id") != recorder_holder
                    or record.get("recorded_by_holder_id")
                    != role_by_id.get(recorder, {}).get("holder_id")
                ):
                    errors.append(
                        f"{gate_id} evidence {evidence_id} recording holder mismatch"
                    )
                    gate_valid = False
                if (
                    record.get("protocol_id") != protocol_id
                    or record.get("protocol_version") != protocol_version
                    or not scope_sha256
                    or record.get("scope_sha256") != scope_sha256
                ):
                    errors.append(
                        f"{gate_id} evidence {evidence_id} is not bound to the "
                        "current protocol scope"
                    )
                    gate_valid = False
                outcome = record.get("decision_outcome")
                allowed_outcomes = {"requirements_satisfied"}
                if gate_id in GATES_ALLOWING_NOT_APPLICABLE_OUTCOME:
                    allowed_outcomes.add("not_applicable")
                if outcome not in allowed_outcomes:
                    errors.append(
                        f"{gate_id} evidence {evidence_id} has an incompatible "
                        f"decision outcome {outcome!r}"
                    )
                    gate_valid = False
            actual_issuers = {
                record.get("issuer_authority_id") for record in records
            }
            if not issuer_ids or issuer_ids != actual_issuers:
                errors.append(
                    f"{gate_id} issuing_authority_ids do not match evidence issuers"
                )
                gate_valid = False

            allowed_types = GATE_RECORD_TYPES.get(gate_id, set())
            if not records or any(
                record.get("record_type") not in allowed_types
                for record in records
            ):
                errors.append(
                    f"{gate_id} lacks its required gate-specific evidence type"
                )
                gate_valid = False
            allowed_authority_types = GATE_AUTHORITY_TYPES.get(gate_id, set())
            if any(
                authority_by_id.get(
                    record.get("issuer_authority_id"), {}
                ).get("authority_type")
                not in allowed_authority_types
                for record in records
            ):
                errors.append(
                    f"{gate_id} evidence comes from an ineligible authority type"
                )
                gate_valid = False
            if recorder not in GATE_RECORDER_ROLES.get(gate_id, set()):
                errors.append(
                    f"{gate_id} terminal status uses an ineligible recording role"
                )
                gate_valid = False
            if not gate_valid:
                invalid_gate_ids.add(gate_id)
        elif status == "expired":
            if (
                (expires_on is None or expires_on > today)
                and (review_due_on is None or review_due_on > today)
            ):
                errors.append(f"{gate_id} expired without a reached review/expiry")

        if gate_id == "WP1-G25" and gate.get("domain") != "independent_exit_review":
            errors.append("WP1-G25 must use independent_exit_review domain")
            invalid_gate_ids.add(gate_id)

    exit_rule = registry.get("exit_rule", {})
    if not isinstance(exit_rule, dict):
        errors.append("exit_rule must be an object")
        exit_rule = {}
    if set(exit_rule.get("required_gate_ids", [])) != REQUIRED_GATE_IDS:
        errors.append("exit_rule required_gate_ids do not match the frozen registry")
    if set(exit_rule.get("required_role_ids", [])) != REQUIRED_ROLE_IDS:
        errors.append("exit_rule required_role_ids do not match the frozen registry")
    if set(exit_rule.get("acceptable_gate_statuses", [])) != (
        ACCEPTABLE_GATE_STATUSES
    ):
        errors.append("exit_rule acceptable_gate_statuses are inconsistent")
    if exit_rule.get("activity_authorization_inherited") is not False:
        errors.append("WP1 activity authorization must never be inherited")

    active_holds = registry.get("active_holds", [])
    if not isinstance(active_holds, list):
        errors.append("active_holds must be an array")
        active_holds = []
    all_gates_pass = (
        set(gates_by_id) == REQUIRED_GATE_IDS
        and not invalid_gate_ids
        and all(
            gates_by_id[gate_id].get("status") in ACCEPTABLE_GATE_STATUSES
            for gate_id in REQUIRED_GATE_IDS
        )
        and gates_by_id.get("WP1-G25", {}).get("status") == "satisfied"
    )
    roles_verified = (
        set(role_ids) == REQUIRED_ROLE_IDS
        and not invalid_role_ids
        and all(
            role.get("status") == "verified"
            for role in roles
            if isinstance(role, dict)
        )
    )
    computed_exit = all_gates_pass and roles_verified and not active_holds
    declared_exit = exit_rule.get("wp1_exit_authorized")
    if declared_exit is not computed_exit:
        errors.append(
            "wp1_exit_authorized does not match current gates, roles, and holds"
        )

    status = registry.get("status")
    if status == "complete" and not computed_exit:
        errors.append("status=complete without a valid WP1 exit")
    if status != "complete" and computed_exit:
        errors.append("all exit conditions pass but status is not complete")
    if status == "open_blocked_external_determinations" and not active_holds:
        errors.append("open WP1 registry must retain an active hold")

    return errors


def load_registry(path: Path) -> dict[str, Any]:
    """Load a registry and require a JSON object."""

    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("WP1 registry root must be a JSON object")
    return value


def validate_registry_schema(path: Path) -> None:
    """Run the canonical JSON Schema layer and fail closed if unavailable."""

    schema_runner = (
        PROJECT_ROOT
        / "AgentCollaboration"
        / "scripts"
        / "validate-artifacts.mjs"
    )
    try:
        result = subprocess.run(
            [
                "node",
                str(schema_runner),
                "--wp1-only",
                str(path),
            ],
            cwd=PROJECT_ROOT,
            capture_output=True,
            check=False,
            text=True,
        )
    except FileNotFoundError as exc:
        raise ValueError(
            "WP1 JSON Schema validation unavailable: Node.js was not found"
        ) from exc
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise ValueError(
            "WP1 JSON Schema validation failed or was unavailable"
            + (f":\n{detail}" if detail else "")
        )


def check(path: Path, baseline_path: Path = DEFAULT_BASELINE) -> None:
    """Run inseparable schema and semantic checks over WP1 state."""

    validate_registry_schema(path)
    registry = load_registry(path)
    errors = validate_registry(registry)
    errors.extend(validate_baseline_reference(baseline_path, registry))
    if errors:
        rendered = "\n".join(f"- {error}" for error in errors)
        raise ValueError(f"WP1 gate audit failed:\n{rendered}")
    print(
        "WP1 combined JSON Schema + semantic gate audit: OK "
        f"({len(registry['gates'])} gates, {len(registry['roles'])} roles, "
        f"{len(registry['authorizations'])} activity authorizations closed; "
        "external evidence and YAML single-source controls enforced)."
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line options."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check"])
    parser.add_argument(
        "--registry",
        type=Path,
        default=DEFAULT_REGISTRY,
        help="Path to the WP1 gate registry JSON.",
    )
    parser.add_argument(
        "--baseline",
        type=Path,
        default=DEFAULT_BASELINE,
        help="Path to the pointer-only baseline YAML.",
    )
    return parser.parse_args()


def main() -> int:
    """Run the requested validation command."""

    args = parse_args()
    check(args.registry.resolve(), args.baseline.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
