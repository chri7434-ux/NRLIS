#!/usr/bin/env python3
"""Participant-free neural-training verification for Project NRLIS.

The input vectors are generated from synthetic class centers. They are not
speech features and contain no participant information. This module verifies a
small neural-training, calibration, abstention, evaluation, and artifact path;
it does not establish ASR or assistive-communication performance.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import math
from pathlib import Path
import random
import sys
from typing import Any, Sequence

import synthetic_g0


IMPLEMENTATION_VERSION = "0.1.0"
DATA_CLASSIFICATION = "synthetic_no_participant_data"
CLAIM_BOUNDARY = "participant_free_neural_training_plumbing_only"
NO_OUTPUT_ACTION = "no_action_shadow_only"

ROOT = Path(__file__).resolve().parents[4]
TRAINING_ROOT = ROOT / "GrossTree" / "Basic" / "Training"
DEFAULT_CONFIG = TRAINING_ROOT / "Config" / "participant_free_neural_v0.json"
DEFAULT_SCHEMA = (
    TRAINING_ROOT / "Config" / "participant_free_neural_v0.schema.json"
)
DEFAULT_EXPECTED = (
    TRAINING_ROOT
    / "Evaluation"
    / "participant_free_neural_v0_expected_metrics.json"
)
DEFAULT_OUTPUT_DIR = ROOT / "tmp" / "participant-free-neural-v0"


class NeuralContractError(ValueError):
    """Raised when neural verification violates a data or safety contract."""


@dataclass(frozen=True)
class Example:
    example_id: str
    split: str
    label_index: int
    features: tuple[float, ...]


@dataclass
class MLP:
    w1: list[list[float]]
    b1: list[float]
    w2: list[list[float]]
    b2: list[float]


def _require_exact_keys(value: dict[str, Any], expected: set[str], path: str) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise NeuralContractError(
            f"{path} keys differ; missing={missing!r}, extra={extra!r}"
        )


def validate_config(config: dict[str, Any]) -> None:
    """Apply cross-field and deny-only checks after JSON Schema validation."""

    if config.get("data_classification") != DATA_CLASSIFICATION:
        raise NeuralContractError("only synthetic participant-free data are permitted")
    if config.get("claim_boundary") != CLAIM_BOUNDARY:
        raise NeuralContractError("claim boundary must remain participant-free")

    labels = config.get("labels")
    input_config = config.get("input")
    safety = config.get("safety")
    if not isinstance(labels, list) or not all(isinstance(x, str) for x in labels):
        raise NeuralContractError("labels must be a string list")
    if not isinstance(input_config, dict) or not isinstance(safety, dict):
        raise NeuralContractError("input and safety must be objects")

    centers = input_config.get("class_centers")
    dimensions = input_config.get("dimensions")
    if not isinstance(centers, dict) or set(centers) != set(labels):
        raise NeuralContractError("class centers must exactly match labels")
    for label, center in centers.items():
        if not isinstance(center, list) or len(center) != dimensions:
            raise NeuralContractError(
                f"class center {label} must have exactly {dimensions} dimensions"
            )
        if not all(
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and math.isfinite(value)
            for value in center
        ):
            raise NeuralContractError(f"class center {label} must be finite numeric")

    _require_exact_keys(
        safety,
        {
            "participant_data_permitted",
            "participant_specific_inference_permitted",
            "candidate_reveal_permitted",
            "output_action",
        },
        "safety",
    )
    if any(
        safety[name] is not False
        for name in (
            "participant_data_permitted",
            "participant_specific_inference_permitted",
            "candidate_reveal_permitted",
        )
    ):
        raise NeuralContractError("all participant and reveal permissions must be false")
    if safety["output_action"] != NO_OUTPUT_ACTION:
        raise NeuralContractError("output action must remain no-action shadow only")


def load_config(path: Path = DEFAULT_CONFIG) -> dict[str, Any]:
    config = synthetic_g0.load_json(path)
    schema = synthetic_g0.load_json(DEFAULT_SCHEMA)
    try:
        synthetic_g0.validate_against_schema(config, schema, "config")
    except synthetic_g0.ContractError as exc:
        raise NeuralContractError(str(exc)) from exc
    validate_config(config)
    return config


def generate_examples(config: dict[str, Any]) -> list[Example]:
    """Create disjoint deterministic synthetic development/calibration/test data."""

    rng = random.Random(config["seed"])
    labels = config["labels"]
    input_config = config["input"]
    noise = input_config["noise_scale"]
    counts = input_config["samples_per_label"]
    examples: list[Example] = []
    split_codes = {"development": "DEV", "calibration": "CAL", "test": "TST"}

    for split in ("development", "calibration", "test"):
        for label_index, label in enumerate(labels):
            center = input_config["class_centers"][label]
            for item_index in range(counts[split]):
                features = tuple(
                    float(coordinate) + rng.gauss(0.0, noise)
                    for coordinate in center
                )
                examples.append(
                    Example(
                        example_id=(
                            f"SYN-{split_codes[split]}-{label_index:02d}-"
                            f"{item_index:04d}"
                        ),
                        split=split,
                        label_index=label_index,
                        features=features,
                    )
                )

    ids = [example.example_id for example in examples]
    if len(ids) != len(set(ids)):
        raise NeuralContractError("synthetic example identifiers overlap")
    return examples


def initialize_model(config: dict[str, Any]) -> MLP:
    rng = random.Random(config["seed"] + 1)
    input_units = config["input"]["dimensions"]
    hidden_units = config["model"]["hidden_units"]
    output_units = len(config["labels"])
    scale = 0.12
    return MLP(
        w1=[
            [rng.uniform(-scale, scale) for _ in range(input_units)]
            for _ in range(hidden_units)
        ],
        b1=[0.0 for _ in range(hidden_units)],
        w2=[
            [rng.uniform(-scale, scale) for _ in range(hidden_units)]
            for _ in range(output_units)
        ],
        b2=[0.0 for _ in range(output_units)],
    )


def forward(model: MLP, features: Sequence[float]) -> tuple[list[float], list[float]]:
    hidden = [
        math.tanh(sum(weight * value for weight, value in zip(row, features)) + bias)
        for row, bias in zip(model.w1, model.b1)
    ]
    logits = [
        sum(weight * value for weight, value in zip(row, hidden)) + bias
        for row, bias in zip(model.w2, model.b2)
    ]
    return hidden, logits


def softmax(logits: Sequence[float], temperature: float = 1.0) -> list[float]:
    scaled = [value / temperature for value in logits]
    maximum = max(scaled)
    exponentials = [math.exp(value - maximum) for value in scaled]
    total = sum(exponentials)
    return [value / total for value in exponentials]


def train(config: dict[str, Any], examples: Sequence[Example]) -> MLP:
    """Train only on examples explicitly assigned to the development split."""

    development = [item for item in examples if item.split == "development"]
    if not development:
        raise NeuralContractError("development split is empty")
    model = initialize_model(config)
    settings = config["model"]
    learning_rate = settings["learning_rate"]
    l2 = settings["l2"]
    rng = random.Random(config["seed"] + 2)

    for _ in range(settings["epochs"]):
        order = list(range(len(development)))
        rng.shuffle(order)
        for index in order:
            example = development[index]
            hidden, logits = forward(model, example.features)
            probabilities = softmax(logits)
            output_gradient = list(probabilities)
            output_gradient[example.label_index] -= 1.0

            old_w2 = [list(row) for row in model.w2]
            for output_index, gradient in enumerate(output_gradient):
                for hidden_index, hidden_value in enumerate(hidden):
                    model.w2[output_index][hidden_index] -= learning_rate * (
                        gradient * hidden_value
                        + l2 * model.w2[output_index][hidden_index]
                    )
                model.b2[output_index] -= learning_rate * gradient

            hidden_gradient = []
            for hidden_index, hidden_value in enumerate(hidden):
                upstream = sum(
                    old_w2[output_index][hidden_index] * output_gradient[output_index]
                    for output_index in range(len(output_gradient))
                )
                hidden_gradient.append(upstream * (1.0 - hidden_value * hidden_value))

            for hidden_index, gradient in enumerate(hidden_gradient):
                for input_index, input_value in enumerate(example.features):
                    model.w1[hidden_index][input_index] -= learning_rate * (
                        gradient * input_value
                        + l2 * model.w1[hidden_index][input_index]
                    )
                model.b1[hidden_index] -= learning_rate * gradient
    return model


def negative_log_likelihood(
    model: MLP, examples: Sequence[Example], temperature: float
) -> float:
    values = []
    for example in examples:
        _, logits = forward(model, example.features)
        probability = softmax(logits, temperature)[example.label_index]
        values.append(-math.log(max(probability, 1e-15)))
    return sum(values) / len(values)


def fit_temperature(
    config: dict[str, Any], model: MLP, examples: Sequence[Example]
) -> float:
    calibration = [item for item in examples if item.split == "calibration"]
    if not calibration:
        raise NeuralContractError("calibration split is empty")
    grid = config["calibration"]["temperature_grid"]
    return min(
        grid,
        key=lambda value: (negative_log_likelihood(model, calibration, value), value),
    )


def ratio(numerator: int, denominator: int) -> dict[str, Any]:
    value = None if denominator == 0 else round(numerator / denominator, 12)
    return {"numerator": numerator, "denominator": denominator, "value": value}


def evaluate(
    config: dict[str, Any],
    model: MLP,
    examples: Sequence[Example],
    temperature: float,
) -> tuple[dict[str, Any], dict[str, Any]]:
    test = [item for item in examples if item.split == "test"]
    threshold = config["abstention"]["minimum_probability"]
    margin_threshold = config["abstention"]["minimum_margin"]
    predictions = []
    correct = 0
    top2_correct = 0
    abstained = 0
    non_abstained_correct = 0
    hazardous_non_abstention = 0
    brier_sum = 0.0
    calibration_rows: list[tuple[float, bool]] = []

    for example in test:
        _, logits = forward(model, example.features)
        probabilities = softmax(logits, temperature)
        order = sorted(range(len(probabilities)), key=lambda i: (-probabilities[i], i))
        predicted = order[0]
        confidence = probabilities[predicted]
        margin = confidence - probabilities[order[1]]
        should_abstain = confidence < threshold or margin < margin_threshold
        is_correct = predicted == example.label_index

        correct += int(is_correct)
        top2_correct += int(example.label_index in order[:2])
        abstained += int(should_abstain)
        if not should_abstain:
            non_abstained_correct += int(is_correct)
            hazardous_non_abstention += int(not is_correct)
        brier_sum += sum(
            (probability - (1.0 if index == example.label_index else 0.0)) ** 2
            for index, probability in enumerate(probabilities)
        )
        calibration_rows.append((confidence, is_correct))
        predictions.append(
            {
                "example_id": example.example_id,
                "split": example.split,
                "predicted_label": config["labels"][predicted],
                "reference_label": config["labels"][example.label_index],
                "probabilities": [round(value, 12) for value in probabilities],
                "abstained": should_abstain,
                "output_action": NO_OUTPUT_ACTION,
            }
        )

    ece = 0.0
    bin_count = 5
    for bin_index in range(bin_count):
        lower = bin_index / bin_count
        upper = (bin_index + 1) / bin_count
        members = [
            row
            for row in calibration_rows
            if lower <= row[0] <= upper
            and (bin_index == bin_count - 1 or row[0] < upper)
        ]
        if members:
            mean_confidence = sum(row[0] for row in members) / len(members)
            mean_accuracy = sum(int(row[1]) for row in members) / len(members)
            ece += len(members) / len(test) * abs(mean_accuracy - mean_confidence)

    non_abstained = len(test) - abstained
    metrics = {
        "implementation_version": IMPLEMENTATION_VERSION,
        "config_id": config["config_id"],
        "data_classification": DATA_CLASSIFICATION,
        "claim_boundary": CLAIM_BOUNDARY,
        "split_counts": {
            split: sum(item.split == split for item in examples)
            for split in ("development", "calibration", "test")
        },
        "selected_temperature": temperature,
        "test_accuracy": ratio(correct, len(test)),
        "test_top2_coverage": ratio(top2_correct, len(test)),
        "test_abstention_rate": ratio(abstained, len(test)),
        "selective_accuracy": ratio(non_abstained_correct, non_abstained),
        "hazardous_non_abstention_rate": ratio(
            hazardous_non_abstention, len(test)
        ),
        "multiclass_brier_score": round(brier_sum / len(test), 12),
        "expected_calibration_error": round(ece, 12),
        "safety": {
            "participant_example_count": 0,
            "candidate_reveal_count": 0,
            "output_bypass_count": sum(
                row["output_action"] != NO_OUTPUT_ACTION for row in predictions
            ),
            "all_outputs_disabled": all(
                row["output_action"] == NO_OUTPUT_ACTION for row in predictions
            ),
        },
        "not_established": [
            "speech_recognition_performance",
            "participant_performance",
            "clinical_effectiveness",
            "cross_person_generalization",
        ],
    }
    prediction_document = {
        "implementation_version": IMPLEMENTATION_VERSION,
        "data_classification": DATA_CLASSIFICATION,
        "claim_boundary": CLAIM_BOUNDARY,
        "predictions": predictions,
    }
    return prediction_document, metrics


def build_artifacts(
    config: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    selected = load_config() if config is None else config
    validate_config(selected)
    examples = generate_examples(selected)
    model = train(selected, examples)
    temperature = fit_temperature(selected, model, examples)
    return evaluate(selected, model, examples, temperature)


def validate_artifacts(
    predictions: dict[str, Any], metrics: dict[str, Any]
) -> None:
    if predictions.get("data_classification") != DATA_CLASSIFICATION:
        raise NeuralContractError("prediction artifact is not participant-free")
    if any(
        row.get("split") != "test"
        or row.get("output_action") != NO_OUTPUT_ACTION
        for row in predictions.get("predictions", [])
    ):
        raise NeuralContractError("prediction artifact violates split or output boundary")
    safety = metrics.get("safety", {})
    if safety != {
        "participant_example_count": 0,
        "candidate_reveal_count": 0,
        "output_bypass_count": 0,
        "all_outputs_disabled": True,
    }:
        raise NeuralContractError("metrics artifact violates safety boundary")


def assert_expected(metrics: dict[str, Any], path: Path = DEFAULT_EXPECTED) -> None:
    expected = synthetic_g0.load_json(path)
    for key, value in expected.items():
        if metrics.get(key) != value:
            raise NeuralContractError(
                f"frozen metric mismatch for {key}: {metrics.get(key)!r} != {value!r}"
            )


def validate_output_directory(path: Path) -> Path:
    resolved = path.resolve()
    allowed_root = (ROOT / "tmp").resolve()
    if not resolved.is_relative_to(allowed_root):
        raise NeuralContractError("generated artifacts may be written only under tmp/")
    return resolved


def write_artifacts(
    output_dir: Path,
    predictions: dict[str, Any],
    metrics: dict[str, Any],
    *,
    force: bool,
) -> None:
    destination = validate_output_directory(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    outputs = {
        "predictions.json": predictions,
        "metrics.json": metrics,
    }
    for name, document in outputs.items():
        path = destination / name
        if path.exists() and not force:
            raise NeuralContractError(f"refusing to overwrite existing artifact: {path}")
        path.write_bytes(synthetic_g0.canonical_json_bytes(document))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "run"))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    try:
        predictions, metrics = build_artifacts()
        validate_artifacts(predictions, metrics)
        assert_expected(metrics)
        if args.command == "run":
            write_artifacts(
                args.output_dir,
                predictions,
                metrics,
                force=args.force,
            )
        print(
            "Participant-free neural G0 check: OK "
            f"({metrics['split_counts']['test']} synthetic test examples; "
            f"accuracy={metrics['test_accuracy']['value']}; "
            "participant claims=0; output bypasses=0)"
        )
        return 0
    except (NeuralContractError, synthetic_g0.ContractError) as exc:
        print(f"Participant-free neural G0 check: FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
