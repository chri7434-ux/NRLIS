#!/usr/bin/env python3
"""Deny-only validation for the WP2.1 recording-intake framework.

The executable validates a participant-free synthetic metadata fixture. It
does not accept an audio path or private participant manifest and performs no
recording access, transcription, feature extraction, or model operation.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any

import synthetic_g0


IMPLEMENTATION_VERSION = "0.1.0"
DATA_CLASSIFICATION = "synthetic_no_participant_data"
SCHEMA_VERSION = "0.1.0"

ROOT = Path(__file__).resolve().parents[4]
DATASET_ROOT = ROOT / "GrossTree" / "Basic" / "Training" / "Dataset"
DEFAULT_SCHEMA = DATASET_ROOT / "recording_intake_v0.schema.json"
DEFAULT_FIXTURE = DATASET_ROOT / "recording_intake_v0.synthetic.json"

PERMISSION_KEYS = {
    "care_use",
    "recognition_analysis",
    "model_training",
    "evaluation",
    "voice_rendering",
    "demonstration",
    "publication",
    "third_party_speech",
}
AUTHORIZATION_KEYS = {
    "human_ready_checkpoint",
    "recording_ingest_authorized",
    "analysis_authorized",
    "training_authorized",
    "participant_specific_inference_authorized",
    "candidate_reveal_authorized",
    "voice_rendering_authorized",
    "public_release_authorized",
}
FORBIDDEN_KEYS = {
    "name",
    "participant_name",
    "speaker_name",
    "filename",
    "original_filename",
    "file_path",
    "path",
    "uri",
    "content",
    "audio",
    "transcript",
    "prompt_text",
    "message_text",
    "recorded_at",
    "exact_date",
    "date_of_birth",
    "location",
    "diagnosis",
    "sha256",
    "hash",
}


class IntakeContractError(ValueError):
    """Raised when the deny-only intake contract is violated."""


def _walk(value: Any, path: str = "$fixture"):
    if isinstance(value, dict):
        for key, child in value.items():
            yield path, key, child
            yield from _walk(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, f"{path}[{index}]")


def validate_semantics(record: dict[str, Any]) -> None:
    """Enforce cross-field, repository, and closed-authorization rules."""

    sensitive = sorted(
        f"{path}.{key}" for path, key, _ in _walk(record) if key in FORBIDDEN_KEYS
    )
    if sensitive:
        raise IntakeContractError(
            "sensitive or content-bearing field names are prohibited: "
            + ", ".join(sensitive)
        )

    if record.get("schema_version") != SCHEMA_VERSION:
        raise IntakeContractError("schema version is not the frozen v0.1 contract")
    if record.get("data_classification") != DATA_CLASSIFICATION:
        raise IntakeContractError(
            "v0.1 executable accepts only synthetic participant-free metadata"
        )
    if record.get("handling_state") != "synthetic_fixture":
        raise IntakeContractError("checked-in v0.1 record must be a synthetic fixture")
    if not str(record.get("record_id", "")).startswith("SYN-R"):
        raise IntakeContractError("synthetic record_id must start with SYN-R")
    if not str(record.get("participant_code", "")).startswith("SYN-P"):
        raise IntakeContractError("synthetic participant_code must start with SYN-P")

    context = record.get("recording_context", {})
    if context.get("structure") != "synthetic_structured_prompt":
        raise IntakeContractError("checked-in fixture cannot represent real recording")
    if context.get("collection_purpose") != "synthetic_generation":
        raise IntakeContractError("fixture collection purpose must be synthetic")
    if context.get("relative_time_bucket") != "not_applicable_synthetic":
        raise IntakeContractError("fixture cannot encode a real impairment timeline")

    speakers = record.get("speaker_context", {})
    if speakers.get("primary_speaker_count") != 0:
        raise IntakeContractError("synthetic fixture must contain zero real speakers")
    if any(
        speakers.get(key) != "not_applicable_synthetic"
        for key in ("additional_speaker_presence", "third_party_review_state")
    ):
        raise IntakeContractError("synthetic fixture cannot claim speaker review")

    provenance = record.get("source_provenance", {})
    if not str(provenance.get("source_record_id", "")).startswith("SYN-SOURCE-"):
        raise IntakeContractError("source_record_id must identify a synthetic source")
    if any(
        provenance.get(key) is not False
        for key in (
            "original_filename_stored_here",
            "filesystem_path_stored_here",
            "content_stored_here",
            "transcript_stored_here",
        )
    ):
        raise IntakeContractError("repository fixture must contain no source material")
    if any(
        provenance.get(key) is not None
        for key in ("external_store_record_id", "integrity_record_id")
    ):
        raise IntakeContractError("synthetic fixture cannot cite private-store records")

    scopes = record.get("permission_scopes", {})
    if set(scopes) != PERMISSION_KEYS:
        raise IntakeContractError("permission scopes do not match the frozen key set")
    if any(value != "not_applicable_synthetic" for value in scopes.values()):
        raise IntakeContractError("synthetic fixture cannot assert human permission")

    reference = record.get("reference_and_label", {})
    if reference.get("reference_source") != "none":
        raise IntakeContractError("synthetic intake fixture cannot claim a reference")
    if reference.get("transcript_status") != "absent":
        raise IntakeContractError("synthetic intake fixture cannot claim a transcript")
    if reference.get("semantic_label_status") != "absent":
        raise IntakeContractError("synthetic intake fixture cannot claim a label")
    if reference.get("candidate_influenced") is not False:
        raise IntakeContractError("candidate influence must remain false")

    split = record.get("split", {})
    if split.get("role") != "unassigned":
        raise IntakeContractError("intake fixture cannot pre-assign a data split")
    if split.get("chronology_record") != "not_applicable_synthetic":
        raise IntakeContractError("fixture cannot claim a private chronology record")

    authorizations = record.get("authorizations", {})
    boolean_authorizations = {
        key: value for key, value in authorizations.items() if key in AUTHORIZATION_KEYS
    }
    if set(boolean_authorizations) != AUTHORIZATION_KEYS:
        raise IntakeContractError("authorizations do not match the frozen key set")
    if any(value is not False for value in boolean_authorizations.values()):
        raise IntakeContractError("all v0.1 action authorizations must remain false")
    if any(
        authorizations.get(key) is not None
        for key in (
            "external_determination_record_id",
            "approved_storage_record_id",
        )
    ):
        raise IntakeContractError("synthetic fixture cannot claim external approval")

    disposition = record.get("disposition", {})
    if disposition.get("research_eligibility") != "not_applicable_synthetic":
        raise IntakeContractError("fixture cannot claim research eligibility")
    if disposition.get("allowed_action") != "synthetic_validation_only":
        raise IntakeContractError("fixture is limited to synthetic validation")
    if disposition.get("care_data_reuse_prohibited") is not True:
        raise IntakeContractError("care-to-research reuse prohibition must remain true")


def load_and_validate(
    fixture_path: Path = DEFAULT_FIXTURE,
    schema_path: Path = DEFAULT_SCHEMA,
) -> dict[str, Any]:
    record = synthetic_g0.load_json(fixture_path)
    schema = synthetic_g0.load_json(schema_path)
    if not isinstance(record, dict):
        raise IntakeContractError("recording intake fixture must be an object")
    try:
        synthetic_g0.validate_against_schema(record, schema, "recording_intake")
    except synthetic_g0.ContractError as exc:
        raise IntakeContractError(str(exc)) from exc
    validate_semantics(record)
    return record


def check() -> None:
    record = load_and_validate()
    print(
        "Recording intake v0.1 check: OK "
        f"({record['record_id']}; synthetic records=1; real recordings accessed=0; "
        "authorizations opened=0)."
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check",))
    args = parser.parse_args(argv)
    if args.command == "check":
        check()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (IntakeContractError, synthetic_g0.ContractError) as exc:
        print(f"Recording intake v0.1 check: FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
