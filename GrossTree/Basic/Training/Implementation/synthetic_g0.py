#!/usr/bin/env python3
"""Deterministic, standard-library-only Synthetic G0 verification pipeline.

This module is intentionally limited to records classified as
``synthetic_no_participant_data``.  It validates the checked-in fixture and
configuration, runs a non-learning rule baseline, and calculates metrics that
are identifiable in shadow mode.  It never enables, speaks, transmits, or acts
on a candidate.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import re
import sys
from typing import Any, Iterable, Sequence


IMPLEMENTATION_VERSION = "1.0.0"
DATA_CLASSIFICATION = "synthetic_no_participant_data"
NO_OUTPUT_ACTION = "no_action_shadow_only"
ECE_BIN_COUNT = 5

ROOT = Path(__file__).resolve().parents[4]
TRAINING_ROOT = ROOT / "GrossTree" / "Basic" / "Training"
DEFAULT_CONFIG = TRAINING_ROOT / "Config" / "synthetic_g0_baseline.json"
DEFAULT_CONFIG_SCHEMA = (
    TRAINING_ROOT / "Config" / "synthetic_g0_config.schema.json"
)
DEFAULT_FIXTURE = TRAINING_ROOT / "Dataset" / "synthetic_g0_fixture.json"
DEFAULT_FIXTURE_SCHEMA = TRAINING_ROOT / "Dataset" / "synthetic_g0.schema.json"
DEFAULT_EXPECTED = (
    TRAINING_ROOT / "Evaluation" / "synthetic_g0_expected_metrics.json"
)
DEFAULT_OUTPUT_DIR = ROOT / "tmp" / "synthetic-g0"

SUPPORTED_SCHEMA_KEYWORDS = {
    "$schema",
    "$id",
    "$ref",
    "$defs",
    "title",
    "type",
    "additionalProperties",
    "required",
    "properties",
    "const",
    "enum",
    "pattern",
    "minimum",
    "maximum",
    "minItems",
    "uniqueItems",
    "items",
    "minProperties",
}

STRATIFICATION_FIELDS = (
    "session_id",
    "semantic_relation",
    "surface_relation",
    "fatigue_state",
    "environment_code",
    "partner_familiarity",
    "personal_vocabulary",
    "speech_variability_state",
)


class ContractError(ValueError):
    """Raised when a synthetic record violates a structural or safety rule."""


def load_json(path: Path) -> Any:
    """Read one UTF-8 JSON document and report a bounded, useful error."""

    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise ContractError(f"required JSON file does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ContractError(
            f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}"
        ) from exc


def canonical_json_bytes(value: Any) -> bytes:
    """Serialize deterministically for comparison and artifact hashing."""

    text = json.dumps(
        value,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
        allow_nan=False,
    )
    return (text + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_document(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def _schema_error(path: str, message: str) -> ContractError:
    return ContractError(f"{path}: {message}")


def _check_supported_schema(schema: Any, path: str = "$schema") -> None:
    """Fail closed if a checked-in schema adds an unsupported assertion."""

    if not isinstance(schema, dict):
        raise _schema_error(path, "schema node must be an object")

    unknown = set(schema) - SUPPORTED_SCHEMA_KEYWORDS
    if unknown:
        names = ", ".join(sorted(unknown))
        raise _schema_error(path, f"unsupported schema keyword(s): {names}")

    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        raise _schema_error(path, "properties must be an object")
    for name, child in properties.items():
        _check_supported_schema(child, f"{path}.properties.{name}")

    definitions = schema.get("$defs", {})
    if not isinstance(definitions, dict):
        raise _schema_error(path, "$defs must be an object")
    for name, child in definitions.items():
        _check_supported_schema(child, f"{path}.$defs.{name}")

    items = schema.get("items")
    if items is not None:
        _check_supported_schema(items, f"{path}.items")

    additional = schema.get("additionalProperties")
    if isinstance(additional, dict):
        _check_supported_schema(additional, f"{path}.additionalProperties")


def _resolve_local_ref(root_schema: dict[str, Any], reference: str) -> dict[str, Any]:
    if not reference.startswith("#/"):
        raise ContractError(f"only local JSON Schema references are supported: {reference}")

    current: Any = root_schema
    for raw_part in reference[2:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, dict) or part not in current:
            raise ContractError(f"unresolvable JSON Schema reference: {reference}")
        current = current[part]
    if not isinstance(current, dict):
        raise ContractError(f"JSON Schema reference is not an object: {reference}")
    return current


def _matches_type(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and math.isfinite(value)
        )
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    raise ContractError(f"unsupported JSON Schema type: {expected}")


def _validate_schema_node(
    value: Any,
    schema: dict[str, Any],
    root_schema: dict[str, Any],
    path: str,
) -> None:
    if "$ref" in schema:
        target = _resolve_local_ref(root_schema, schema["$ref"])
        _validate_schema_node(value, target, root_schema, path)

    if "const" in schema and value != schema["const"]:
        raise _schema_error(path, f"must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        raise _schema_error(path, f"must be one of {schema['enum']!r}")

    expected_types = schema.get("type")
    if expected_types is not None:
        if isinstance(expected_types, str):
            expected_types = [expected_types]
        if not isinstance(expected_types, list) or not all(
            isinstance(item, str) for item in expected_types
        ):
            raise ContractError(f"invalid type declaration in schema at {path}")
        if not any(_matches_type(value, item) for item in expected_types):
            raise _schema_error(path, f"must have type {expected_types!r}")

    if isinstance(value, dict):
        required = schema.get("required", [])
        missing = [name for name in required if name not in value]
        if missing:
            raise _schema_error(path, f"missing required field(s): {missing!r}")

        minimum_properties = schema.get("minProperties")
        if minimum_properties is not None and len(value) < minimum_properties:
            raise _schema_error(
                path, f"must have at least {minimum_properties} properties"
            )

        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        for name, child_value in value.items():
            child_path = f"{path}.{name}"
            if name in properties:
                _validate_schema_node(
                    child_value, properties[name], root_schema, child_path
                )
            elif additional is False:
                raise _schema_error(path, f"unexpected field: {name}")
            elif isinstance(additional, dict):
                _validate_schema_node(
                    child_value, additional, root_schema, child_path
                )

    if isinstance(value, list):
        minimum_items = schema.get("minItems")
        if minimum_items is not None and len(value) < minimum_items:
            raise _schema_error(path, f"must contain at least {minimum_items} item(s)")
        if schema.get("uniqueItems"):
            serialized = [canonical_json_bytes(item) for item in value]
            if len(set(serialized)) != len(serialized):
                raise _schema_error(path, "items must be unique")
        item_schema = schema.get("items")
        if item_schema is not None:
            for index, item in enumerate(value):
                _validate_schema_node(
                    item, item_schema, root_schema, f"{path}[{index}]"
                )

    if isinstance(value, str) and "pattern" in schema:
        if re.fullmatch(schema["pattern"], value) is None:
            raise _schema_error(path, f"does not match {schema['pattern']!r}")

    if (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    ):
        if "minimum" in schema and value < schema["minimum"]:
            raise _schema_error(path, f"must be >= {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            raise _schema_error(path, f"must be <= {schema['maximum']}")


def validate_against_schema(
    value: Any,
    schema: dict[str, Any],
    document_name: str,
) -> None:
    _check_supported_schema(schema)
    _validate_schema_node(value, schema, schema, f"${document_name}")


def _require_unique(values: Iterable[Any], label: str) -> None:
    items = list(values)
    if len(items) != len(set(items)):
        raise ContractError(f"{label} must be unique")


def validate_config_semantics(config: dict[str, Any]) -> None:
    if config["data_classification"] != DATA_CLASSIFICATION:
        raise ContractError("config is not classified as synthetic-only")
    if config["output_enabled"] is not False:
        raise ContractError("synthetic G0 output_enabled must remain false")

    top_k = config["top_k"]
    candidate_universe: set[str] = set()
    for signal_code, candidates in config["candidate_bank"].items():
        if len(candidates) < top_k:
            raise ContractError(
                f"candidate bank {signal_code!r} has fewer than top_k={top_k} items"
            )
        semantic_ids = [candidate["semantic_id"] for candidate in candidates]
        _require_unique(semantic_ids, f"candidate IDs for {signal_code}")
        candidate_universe.update(semantic_ids)

        probabilities: list[float] = []
        for candidate in candidates:
            raw_score = candidate["raw_score"]
            probability = candidate["probability"]
            if not math.isfinite(raw_score):
                raise ContractError(f"non-finite raw score for {signal_code}")
            if not math.isfinite(probability):
                raise ContractError(f"non-finite probability for {signal_code}")
            probabilities.append(float(probability))
        if not math.isclose(math.fsum(probabilities), 1.0, abs_tol=1e-12):
            raise ContractError(
                f"candidate probabilities for {signal_code!r} must sum to 1"
            )

    if not candidate_universe:
        raise ContractError("candidate universe must not be empty")


def validate_fixture_semantics(
    fixture: dict[str, Any],
    config: dict[str, Any],
) -> None:
    if fixture["data_classification"] != DATA_CLASSIFICATION:
        raise ContractError("fixture is not classified as synthetic-only")

    manifest = fixture["experiment_manifest"]
    split_names = (
        "development_session_ids",
        "calibration_session_ids",
        "prospective_shadow_session_ids",
    )
    split_sets = {name: set(manifest[name]) for name in split_names}
    for index, left_name in enumerate(split_names):
        for right_name in split_names[index + 1 :]:
            overlap = split_sets[left_name] & split_sets[right_name]
            if overlap:
                raise ContractError(
                    f"session split overlap between {left_name} and "
                    f"{right_name}: {sorted(overlap)!r}"
                )

    attempts = fixture["attempts"]
    _require_unique(
        (attempt["attempt_id"] for attempt in attempts), "attempt IDs"
    )
    _require_unique(
        (attempt["event_order"] for attempt in attempts), "event orders"
    )
    all_input_ids = [
        record_id
        for attempt in attempts
        for record_id in attempt["input_record_ids"]
    ]
    _require_unique(all_input_ids, "input record IDs")

    event_orders = sorted(attempt["event_order"] for attempt in attempts)
    if event_orders != list(range(1, len(attempts) + 1)):
        raise ContractError("event_order must be contiguous from 1 through N")

    configured_signals = set(config["candidate_bank"])
    candidate_universe = {
        candidate["semantic_id"]
        for candidates in config["candidate_bank"].values()
        for candidate in candidates
    }
    allowed_sessions = set().union(*split_sets.values())
    prospective_sessions = split_sets["prospective_shadow_session_ids"]
    for attempt in attempts:
        attempt_id = attempt["attempt_id"]
        if attempt["session_id"] not in allowed_sessions:
            raise ContractError(f"{attempt_id}: session is absent from manifest")
        if attempt["session_id"] not in prospective_sessions:
            raise ContractError(
                f"{attempt_id}: fixture attempt must be in prospective shadow split"
            )
        if attempt["observable_signal_code"] not in configured_signals:
            raise ContractError(f"{attempt_id}: signal has no baseline configuration")
        if attempt["reference_semantic_id"] not in candidate_universe:
            raise ContractError(
                f"{attempt_id}: reference semantic ID is outside candidate universe"
            )
        if attempt["training_eligible"] or attempt["authorship_claim_eligible"]:
            raise ContractError(
                f"{attempt_id}: synthetic records cannot support training or authorship"
            )

        if attempt["challenge_eligible"] is not attempt["abstention_expected"]:
            raise ContractError(
                f"{attempt_id}: challenge_eligible and abstention_expected "
                "must identify the same independently frozen safety target"
            )

        if attempt["scoring_eligible"]:
            if (
                not attempt["usable_attempt"]
                or attempt["cancelled"]
                or attempt["exclusion_reason"] is not None
            ):
                raise ContractError(
                    f"{attempt_id}: scoring eligibility contradicts disposition"
                )
        elif (
            attempt["usable_attempt"]
            and not attempt["cancelled"]
            and attempt["exclusion_reason"] is None
        ):
            raise ContractError(
                f"{attempt_id}: excluded attempt requires a pre-specified reason"
            )


def load_validated_inputs(
    fixture_path: Path = DEFAULT_FIXTURE,
    config_path: Path = DEFAULT_CONFIG,
    fixture_schema_path: Path = DEFAULT_FIXTURE_SCHEMA,
    config_schema_path: Path = DEFAULT_CONFIG_SCHEMA,
) -> tuple[dict[str, Any], dict[str, Any]]:
    fixture = load_json(fixture_path)
    config = load_json(config_path)
    fixture_schema = load_json(fixture_schema_path)
    config_schema = load_json(config_schema_path)

    if not isinstance(fixture, dict) or not isinstance(config, dict):
        raise ContractError("fixture and config must be JSON objects")
    validate_against_schema(fixture, fixture_schema, "fixture")
    validate_against_schema(config, config_schema, "config")
    validate_config_semantics(config)
    validate_fixture_semantics(fixture, config)
    return fixture, config


def predict_observation(
    observable_signal_code: str,
    input_quality_code: str,
    config: dict[str, Any],
) -> dict[str, Any]:
    """Predict from observable fields only; reference labels are not accepted."""

    configured = config["candidate_bank"].get(observable_signal_code)
    if configured is None:
        raise ContractError(
            f"no deterministic baseline rule for {observable_signal_code!r}"
        )

    ordered = sorted(
        (deepcopy(candidate) for candidate in configured),
        key=lambda candidate: (-candidate["raw_score"], candidate["semantic_id"]),
    )
    candidates = [
        {
            "semantic_id": candidate["semantic_id"],
            "rank": rank,
            "raw_score": candidate["raw_score"],
            "probability": candidate["probability"],
        }
        for rank, candidate in enumerate(ordered, start=1)
    ]
    abstained = input_quality_code in set(
        config["abstain_input_quality_codes"]
    )
    return {
        "candidates": candidates,
        "abstained": abstained,
        "abstention_reason": (
            f"input_quality:{input_quality_code}" if abstained else None
        ),
    }


def _run_id(fixture: dict[str, Any], config: dict[str, Any]) -> str:
    digest_input = (
        canonical_json_bytes(fixture)
        + b"\0"
        + canonical_json_bytes(config)
        + b"\0"
        + IMPLEMENTATION_VERSION.encode("ascii")
    )
    return f"SYN-RUN-{sha256_bytes(digest_input)[:16].upper()}"


def generate_predictions(
    fixture: dict[str, Any],
    config: dict[str, Any],
) -> dict[str, Any]:
    run_id = _run_id(fixture, config)
    config_hash = sha256_document(config)
    candidate_set_id = f"SYN-CSET-{config_hash[:8].upper()}"
    predictions: list[dict[str, Any]] = []

    for attempt in fixture["attempts"]:
        result = predict_observation(
            attempt["observable_signal_code"],
            attempt["input_quality_code"],
            config,
        )
        predictions.append(
            {
                "attempt_id": attempt["attempt_id"],
                "input_record_ids": list(attempt["input_record_ids"]),
                "candidate_set_id": candidate_set_id,
                "candidates": result["candidates"],
                "abstained": result["abstained"],
                "abstention_reason": result["abstention_reason"],
                "context_features_used": [
                    "observable_signal_code",
                    "input_quality_code",
                ],
                "output_permitted": False,
                "output_action": NO_OUTPUT_ACTION,
                "later_correction": None,
            }
        )

    document = {
        "schema_version": "1.0",
        "implementation_version": IMPLEMENTATION_VERSION,
        "data_classification": DATA_CLASSIFICATION,
        "fixture_id": fixture["fixture_id"],
        "run_id": run_id,
        "model": {
            "baseline_id": config["baseline_id"],
            "config_id": config["config_id"],
            "config_version": config["config_version"],
            "artifact_sha256": config_hash,
        },
        "top_k": config["top_k"],
        "predictions": predictions,
    }
    validate_prediction_document(document, fixture, config)
    return document


def validate_prediction_document(
    document: dict[str, Any],
    fixture: dict[str, Any],
    config: dict[str, Any],
) -> None:
    if document.get("data_classification") != DATA_CLASSIFICATION:
        raise ContractError("prediction document lost synthetic classification")
    if document.get("top_k") != config["top_k"]:
        raise ContractError("prediction top_k differs from frozen configuration")

    attempts = {item["attempt_id"]: item for item in fixture["attempts"]}
    predictions = document.get("predictions")
    if not isinstance(predictions, list):
        raise ContractError("predictions must be an array")
    if len(predictions) != len(attempts):
        raise ContractError("every retained attempt must have one prediction record")

    prediction_ids = [item.get("attempt_id") for item in predictions]
    _require_unique(prediction_ids, "prediction attempt IDs")
    if set(prediction_ids) != set(attempts):
        raise ContractError("prediction and retained-attempt IDs must match")

    abstention_codes = set(config["abstain_input_quality_codes"])
    for prediction in predictions:
        attempt_id = prediction["attempt_id"]
        attempt = attempts[attempt_id]
        if prediction.get("input_record_ids") != attempt["input_record_ids"]:
            raise ContractError(f"{attempt_id}: input provenance mismatch")
        if prediction.get("output_permitted") is not False:
            raise ContractError(f"{attempt_id}: output must remain disabled")
        if prediction.get("output_action") != NO_OUTPUT_ACTION:
            raise ContractError(f"{attempt_id}: output action is unsafe")
        if prediction.get("later_correction") is not None:
            raise ContractError(f"{attempt_id}: synthetic correction must be null")
        if prediction.get("context_features_used") != [
            "observable_signal_code",
            "input_quality_code",
        ]:
            raise ContractError(f"{attempt_id}: unexpected context feature")

        expected_abstention = (
            attempt["input_quality_code"] in abstention_codes
        )
        if prediction.get("abstained") is not expected_abstention:
            raise ContractError(f"{attempt_id}: abstention decision mismatch")

        candidates = prediction.get("candidates")
        if not isinstance(candidates, list) or len(candidates) < config["top_k"]:
            raise ContractError(f"{attempt_id}: incomplete candidate list")
        semantic_ids = [candidate.get("semantic_id") for candidate in candidates]
        _require_unique(semantic_ids, f"{attempt_id} candidate IDs")
        ranks = [candidate.get("rank") for candidate in candidates]
        if ranks != list(range(1, len(candidates) + 1)):
            raise ContractError(f"{attempt_id}: candidate ranks are not contiguous")
        probabilities: list[float] = []
        for candidate in candidates:
            probability = candidate.get("probability")
            raw_score = candidate.get("raw_score")
            if (
                not isinstance(probability, (int, float))
                or isinstance(probability, bool)
                or not math.isfinite(probability)
                or not 0 <= probability <= 1
            ):
                raise ContractError(f"{attempt_id}: invalid candidate probability")
            if (
                not isinstance(raw_score, (int, float))
                or isinstance(raw_score, bool)
                or not math.isfinite(raw_score)
            ):
                raise ContractError(f"{attempt_id}: invalid raw score")
            probabilities.append(float(probability))
        if not math.isclose(math.fsum(probabilities), 1.0, abs_tol=1e-12):
            raise ContractError(f"{attempt_id}: candidate probabilities must sum to 1")


def ratio(numerator: int, denominator: int) -> dict[str, Any]:
    return {
        "numerator": numerator,
        "denominator": denominator,
        "value": (
            None if denominator == 0 else round(numerator / denominator, 12)
        ),
    }


def _core_count_metrics(
    rows: Sequence[dict[str, Any]],
    top_k: int,
) -> dict[str, Any]:
    denominator = len(rows)
    unconditional_top_k_hits = 0
    top_1_errors = 0
    non_abstained = 0
    conditional_top_k_hits = 0
    selective_errors = 0
    abstentions = 0

    for row in rows:
        attempt = row["attempt"]
        prediction = row["prediction"]
        reference = attempt["reference_semantic_id"]
        top_candidates = prediction["candidates"][:top_k]
        top_k_hit = reference in {
            item["semantic_id"] for item in top_candidates
        }
        top_1_correct = prediction["candidates"][0]["semantic_id"] == reference
        if not top_1_correct:
            top_1_errors += 1
        if prediction["abstained"]:
            abstentions += 1
        else:
            non_abstained += 1
            if top_k_hit:
                unconditional_top_k_hits += 1
                conditional_top_k_hits += 1
            if not top_1_correct:
                selective_errors += 1

    return {
        "unconditional_top_k_semantic_coverage": ratio(
            unconditional_top_k_hits, denominator
        ),
        "counterfactual_top1_error_rate": ratio(top_1_errors, denominator),
        "hazardous_non_abstention_rate": ratio(
            selective_errors, denominator
        ),
        "non_abstained_coverage": ratio(non_abstained, denominator),
        "conditional_top_k_semantic_coverage": ratio(
            conditional_top_k_hits, non_abstained
        ),
        "selective_risk": ratio(selective_errors, non_abstained),
        "abstention_rate": ratio(abstentions, denominator),
    }


def _brier_score(
    rows: Sequence[dict[str, Any]],
    candidate_universe: Sequence[str],
) -> dict[str, Any]:
    if not rows:
        return {"denominator": 0, "value": None}

    per_attempt: list[float] = []
    for row in rows:
        reference = row["attempt"]["reference_semantic_id"]
        probability_by_id = {
            candidate["semantic_id"]: float(candidate["probability"])
            for candidate in row["prediction"]["candidates"]
        }
        per_attempt.append(
            math.fsum(
                (
                    probability_by_id.get(semantic_id, 0.0)
                    - (1.0 if semantic_id == reference else 0.0)
                )
                ** 2
                for semantic_id in candidate_universe
            )
        )
    return {
        "denominator": len(rows),
        "value": round(math.fsum(per_attempt) / len(rows), 12),
    }


def _expected_calibration_error(
    rows: Sequence[dict[str, Any]],
    bin_count: int = ECE_BIN_COUNT,
) -> dict[str, Any]:
    if not rows:
        return {"bin_count": bin_count, "denominator": 0, "value": None}

    bins: list[list[tuple[float, bool]]] = [[] for _ in range(bin_count)]
    for row in rows:
        top_candidate = row["prediction"]["candidates"][0]
        confidence = float(top_candidate["probability"])
        correct = (
            top_candidate["semantic_id"]
            == row["attempt"]["reference_semantic_id"]
        )
        bin_index = min(int(confidence * bin_count), bin_count - 1)
        bins[bin_index].append((confidence, correct))

    total = len(rows)
    contributions: list[float] = []
    populated_bins: list[dict[str, Any]] = []
    for index, members in enumerate(bins):
        if not members:
            continue
        count = len(members)
        mean_confidence = math.fsum(item[0] for item in members) / count
        accuracy = sum(1 for _, correct in members if correct) / count
        contribution = (count / total) * abs(accuracy - mean_confidence)
        contributions.append(contribution)
        populated_bins.append(
            {
                "bin_index": index,
                "count": count,
                "mean_confidence": round(mean_confidence, 12),
                "accuracy": round(accuracy, 12),
            }
        )
    return {
        "bin_count": bin_count,
        "denominator": total,
        "value": round(math.fsum(contributions), 12),
        "populated_bins": populated_bins,
    }


def calculate_metrics(
    fixture: dict[str, Any],
    config: dict[str, Any],
    prediction_document: dict[str, Any],
) -> dict[str, Any]:
    validate_prediction_document(prediction_document, fixture, config)
    predictions_by_attempt = {
        item["attempt_id"]: item
        for item in prediction_document["predictions"]
    }
    all_rows = [
        {
            "attempt": attempt,
            "prediction": predictions_by_attempt[attempt["attempt_id"]],
        }
        for attempt in fixture["attempts"]
    ]
    rows = [
        row for row in all_rows if row["attempt"]["scoring_eligible"]
    ]
    core = _core_count_metrics(rows, config["top_k"])

    challenge_rows = [
        row for row in all_rows if row["attempt"]["challenge_eligible"]
    ]
    clear_scoring_rows = [
        row for row in rows if not row["attempt"]["challenge_eligible"]
    ]
    challenge_abstentions = sum(
        1 for row in challenge_rows if row["prediction"]["abstained"]
    )
    false_abstentions = sum(
        1
        for row in clear_scoring_rows
        if row["prediction"]["abstained"]
    )

    candidate_universe = sorted(
        {
            candidate["semantic_id"]
            for candidates in config["candidate_bank"].values()
            for candidate in candidates
        }
    )

    strata: dict[str, Any] = {}
    for field in STRATIFICATION_FIELDS:
        values = sorted(
            {row["attempt"][field] for row in rows},
            key=lambda value: json.dumps(value, sort_keys=True),
        )
        strata[field] = {
            str(value).lower() if isinstance(value, bool) else str(value):
            {
                "eligible_attempt_count": len(
                    subset := [
                        row for row in rows if row["attempt"][field] == value
                    ]
                ),
                **_core_count_metrics(subset, config["top_k"]),
            }
            for value in values
        }

    all_predictions = prediction_document["predictions"]
    output_bypass_count = sum(
        1
        for prediction in all_predictions
        if prediction["output_permitted"]
        or prediction["output_action"] != NO_OUTPUT_ACTION
    )

    return {
        "schema_version": "1.0",
        "implementation_version": IMPLEMENTATION_VERSION,
        "data_classification": DATA_CLASSIFICATION,
        "fixture_id": fixture["fixture_id"],
        "run_id": prediction_document["run_id"],
        "fixture_sha256": sha256_document(fixture),
        "config_sha256": sha256_document(config),
        "retained_attempt_count": len(fixture["attempts"]),
        "eligible_attempt_count": len(rows),
        "excluded_attempt_count": len(fixture["attempts"]) - len(rows),
        "top_k": config["top_k"],
        **core,
        "challenge_abstention_sensitivity": ratio(
            challenge_abstentions, len(challenge_rows)
        ),
        "false_abstention_rate": ratio(
            false_abstentions, len(clear_scoring_rows)
        ),
        "multiclass_brier_score": _brier_score(rows, candidate_universe),
        "expected_calibration_error": _expected_calibration_error(rows),
        "safety": {
            "output_bypass_count": output_bypass_count,
            "all_outputs_disabled": output_bypass_count == 0,
        },
        "not_estimable_in_shadow": [
            "successful_message_rate",
            "actual_misattribution_rate",
            "participant_time_to_message",
            "fallback_success",
            "participant_effort_or_fatigue_outcome",
        ],
        "not_evaluable_in_static_fixture": [
            "inference_latency",
        ],
        "strata": strata,
    }


def build_artifacts(
    fixture: dict[str, Any],
    config: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    predictions = generate_predictions(fixture, config)
    metrics = calculate_metrics(fixture, config, predictions)
    return predictions, metrics


def assert_expected_subset(
    observed: Any,
    expected: Any,
    path: str = "$metrics",
) -> None:
    """Require every frozen expected value while allowing diagnostic expansion."""

    if isinstance(expected, dict):
        if not isinstance(observed, dict):
            raise ContractError(f"{path}: expected an object")
        for key, expected_value in expected.items():
            if key not in observed:
                raise ContractError(f"{path}: missing frozen metric field {key!r}")
            assert_expected_subset(
                observed[key], expected_value, f"{path}.{key}"
            )
        return
    if observed != expected:
        raise ContractError(
            f"{path}: expected {expected!r}, observed {observed!r}"
        )


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def validate_output_directory(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    if _is_within(resolved, ROOT) and not _is_within(
        resolved, (ROOT / "tmp").resolve()
    ):
        raise ContractError(
            "generated output inside the repository is permitted only under tmp/"
        )
    return resolved


def write_artifacts(
    output_directory: Path,
    predictions: dict[str, Any],
    metrics: dict[str, Any],
    *,
    force: bool = False,
) -> tuple[Path, Path]:
    output_directory = validate_output_directory(output_directory)
    prediction_path = output_directory / "predictions.json"
    metrics_path = output_directory / "metrics.json"
    existing = [path for path in (prediction_path, metrics_path) if path.exists()]
    if existing and not force:
        joined = ", ".join(str(path) for path in existing)
        raise ContractError(f"refusing to overwrite generated file(s): {joined}")
    output_directory.mkdir(parents=True, exist_ok=True)
    prediction_path.write_bytes(canonical_json_bytes(predictions))
    metrics_path.write_bytes(canonical_json_bytes(metrics))
    return prediction_path, metrics_path


def _common_paths(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument(
        "--fixture-schema", type=Path, default=DEFAULT_FIXTURE_SCHEMA
    )
    parser.add_argument(
        "--config-schema", type=Path, default=DEFAULT_CONFIG_SCHEMA
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate and run the participant-free Synthetic G0 pipeline."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate", help="validate config, schema, fixture, and cross-record rules"
    )
    _common_paths(validate_parser)

    run_parser = subparsers.add_parser(
        "run", help="write deterministic predictions and metrics"
    )
    _common_paths(run_parser)
    run_parser.add_argument(
        "--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR
    )
    run_parser.add_argument(
        "--force",
        action="store_true",
        help="replace only the two generated JSON files in the output directory",
    )

    check_parser = subparsers.add_parser(
        "check", help="recalculate in memory and compare with the frozen expectation"
    )
    _common_paths(check_parser)
    check_parser.add_argument("--expected", type=Path, default=DEFAULT_EXPECTED)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        fixture, config = load_validated_inputs(
            args.fixture,
            args.config,
            args.fixture_schema,
            args.config_schema,
        )
        if args.command == "validate":
            print(
                "Synthetic G0 validation: OK "
                f"({len(fixture['attempts'])} retained synthetic attempts)."
            )
            return 0

        predictions, metrics = build_artifacts(fixture, config)
        if args.command == "run":
            prediction_path, metrics_path = write_artifacts(
                args.output_dir,
                predictions,
                metrics,
                force=args.force,
            )
            print(f"Synthetic G0 run: OK ({prediction_path}, {metrics_path}).")
            return 0

        expected = load_json(args.expected)
        assert_expected_subset(metrics, expected)
        print(
            "Synthetic G0 check: OK "
            f"({metrics['eligible_attempt_count']} eligible attempts; "
            f"output bypasses={metrics['safety']['output_bypass_count']})."
        )
        return 0
    except ContractError as exc:
        print(f"Synthetic G0: FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
