#!/usr/bin/env python3
"""WP2.3: route generated neural scores to sealed synthetic concept candidates.

This CLI has no participant, media, score-file, or CareAAC input interface.
Only the checked-in synthetic generator supplies the model examples.
"""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from dataclasses import asdict
import math
from pathlib import Path
import sys
from typing import Any, Sequence

import participant_free_neural as neural
import synthetic_g0 as core

TRAINING = Path(__file__).resolve().parents[1]
CARE = TRAINING.parent / "CareAAC"
sys.path.insert(0, str(CARE))
import validate_care_architecture as care  # noqa: E402

CONFIG = TRAINING / "Config" / "synthetic_intent_adapter_v0.json"
SCHEMA = CONFIG.with_suffix(".schema.json")
EXPECTED = TRAINING / "Evaluation" / "synthetic_intent_adapter_v0_expected.json"
CLASSIFICATION = "synthetic_no_participant_data"
CLAIM = "synthetic_model_to_concept_routing_only"
NO_OUTPUT = "no_action_shadow_only"
CONTROLS = ("none_of_these", "repeat", "cancel", "non_predictive_fallback")


class AdapterError(ValueError):
    """Invalid routing input; no candidate decision may be emitted."""


def validate_schema(value: Any, name: str | None = None) -> None:
    schema = core.load_json(SCHEMA)
    if name:
        schema = {"$ref": f"#/$defs/{name}", "$defs": schema["$defs"]}
    try:
        core.validate_against_schema(value, schema, name or "adapter_config")
    except core.ContractError as exc:
        raise AdapterError(str(exc)) from exc


def load_contract() -> tuple[dict, dict, dict]:
    config = core.load_json(CONFIG)
    vocabulary, _ = care.load_and_validate()
    source = neural.load_config()
    validate_contract(config, vocabulary, source)
    return config, vocabulary, source


def validate_contract(config: dict, vocabulary: dict, source: dict) -> None:
    validate_schema(config)
    if core.sha256_document(source) != config["source_config_sha256"]:
        raise AdapterError("source configuration fingerprint mismatch")
    if core.sha256_document(vocabulary) != config["vocabulary_sha256"]:
        raise AdapterError("vocabulary fingerprint mismatch")
    if config["labels"] != source["labels"]:
        raise AdapterError("source label order changed")
    if config["minimum_probability"] != source["abstention"]["minimum_probability"]:
        raise AdapterError("probability threshold must inherit the frozen source")
    if config["minimum_margin"] != source["abstention"]["minimum_margin"]:
        raise AdapterError("margin threshold must inherit the frozen source")
    known = {item["id"] for item in vocabulary["concepts"]}
    mapped = [value for value in config["label_to_concept"].values() if value is not None]
    if len(mapped) != len(set(mapped)) or not set(mapped) <= known:
        raise AdapterError("mapping must contain unique known concepts")


class SyntheticIntentAdapter:
    """Self-contained synthetic training/calibration and sealed routing engine.

    route() is an engineering test surface over score packets, not a participant
    authorization or data-ingest API. Calibration and training always use the
    fixed synthetic generator; callers cannot supply models or examples.
    """

    def __init__(self) -> None:
        self._config, self._vocabulary, self._source = load_contract()
        self._examples = neural.generate_examples(self._source)
        development = [item for item in self._examples if item.split == "development"]
        calibration = [item for item in self._examples if item.split == "calibration"]
        # Held-out examples never enter training or temperature selection.
        self._model = neural.train(self._source, development)
        self._temperature = neural.fit_temperature(self._source, self._model, calibration)
        self._provenance = {
            "source_config_sha256": self._config["source_config_sha256"],
            "vocabulary_sha256": self._config["vocabulary_sha256"],
            "adapter_config_sha256": core.sha256_document(self._config),
            "neural_implementation_sha256": core.sha256_bytes(Path(neural.__file__).read_bytes()),
            "adapter_implementation_sha256": core.sha256_bytes(Path(__file__).read_bytes()),
            "model_sha256": core.sha256_document(asdict(self._model)),
            "development_sha256": core.sha256_document([asdict(x) for x in development]),
            "calibration_sha256": core.sha256_document([asdict(x) for x in calibration]),
            "method": "temperature_grid_nll_calibration_only",
            "temperature": self._temperature,
            "threshold_source": "frozen_source_config_not_fitted_on_test",
        }
        self._calibration_id = core.sha256_document(self._provenance)

    @property
    def provenance(self) -> dict:
        return deepcopy(self._provenance)

    def _packet(self, probabilities: list[float]) -> dict:
        return {
            "data_classification": CLASSIFICATION,
            "source_config_sha256": self._config["source_config_sha256"],
            "vocabulary_sha256": self._config["vocabulary_sha256"],
            "calibration_sha256": self._calibration_id,
            "labels": list(self._config["labels"]),
            "probabilities": list(probabilities),
        }

    def route(self, packet: dict, context_id: str, panel_id: str) -> dict:
        """Filter full-class probabilities without conditioning on the panel.

        Invalid contracts raise AdapterError; ordinary uncertainty or unsupported
        meaning returns abstain with an empty candidate set. Neither emits UI
        events, text, confirmation, speech, or transmission.
        """
        validate_schema(packet, "packet")
        for field, expected in (
            ("source_config_sha256", self._config["source_config_sha256"]),
            ("vocabulary_sha256", self._config["vocabulary_sha256"]),
            ("calibration_sha256", self._calibration_id),
            ("labels", self._config["labels"]),
        ):
            if packet[field] != expected:
                raise AdapterError(f"score packet {field} mismatch")
        probabilities = packet["probabilities"]
        if len(probabilities) != len(self._config["labels"]):
            raise AdapterError("probability vector length mismatch")
        if not math.isclose(math.fsum(probabilities), 1.0, rel_tol=0.0, abs_tol=1e-9):
            raise AdapterError("full probability vector must sum to one")

        if not isinstance(context_id, str) or not isinstance(panel_id, str):
            raise AdapterError("context and panel must be identifiers")
        context = next((x for x in self._vocabulary["contexts"] if x["id"] == context_id), None)
        panel = next((x for x in context["panels"] if x["id"] == panel_id), None) if context else None
        if panel is None:
            raise AdapterError("panel does not belong to the specified context")

        labels = self._config["labels"]
        mapping = self._config["label_to_concept"]
        order = sorted(range(len(labels)), key=lambda i: (-probabilities[i], i))
        top = order[0]
        top_concept = mapping[labels[top]]
        margin = probabilities[top] - probabilities[order[1]]
        if top_concept is None:
            reason = "unmapped_top_class"
        elif top_concept not in panel["conceptIds"]:
            reason = "top_outside_panel"
        elif probabilities[top] < self._config["minimum_probability"]:
            reason = "below_probability"
        elif margin < self._config["minimum_margin"]:
            reason = "below_margin"
        else:
            reason = "eligible"

        candidates = []
        if reason == "eligible":
            for index in order:
                concept = mapping[labels[index]]
                if concept in panel["conceptIds"] and probabilities[index] >= self._config["candidate_probability_floor"]:
                    candidates.append({"concept_id": concept, "probability": probabilities[index]})
            candidates = candidates[:self._config["maximum_candidates"]]

        decision = {
            "data_classification": CLASSIFICATION,
            "claim_boundary": CLAIM,
            "decision": "candidates" if candidates else "abstain",
            "reason": reason,
            "context_id": context_id,
            "panel_id": panel_id,
            "candidates": candidates,
            "required_controls": list(CONTROLS),
            "confirmation_required": True,
            "candidate_reveal_permitted": False,
            "care_ui_connection_permitted": False,
            "output_action": NO_OUTPUT,
        }
        validate_schema(decision, "decision")
        return decision

    def build_artifacts(self) -> tuple[dict, dict]:
        """Cross every held-out example with every fixed panel, independently of labels."""
        rows = []
        examples = [item for item in self._examples if item.split == "test"]
        for example in examples:
            _, logits = neural.forward(self._model, example.features)
            packet = self._packet(neural.softmax(logits, self._temperature))
            for context in self._vocabulary["contexts"]:
                for panel in context["panels"]:
                    decision = self.route(packet, context["id"], panel["id"])
                    # Reference is attached only after the prediction decision.
                    rows.append({
                        "example_id": example.example_id,
                        "split": "test",
                        "reference_label": self._source["labels"][example.label_index],
                        "decision": decision,
                    })

        offered = [row for row in rows if row["decision"]["decision"] == "candidates"]
        mapping = self._config["label_to_concept"]
        correct = sum(
            mapping[row["reference_label"]] in [x["concept_id"] for x in row["decision"]["candidates"]]
            for row in offered
        )
        report = {
            "version": "0.1.0",
            "data_classification": CLASSIFICATION,
            "claim_boundary": CLAIM,
            "source_test_examples": len(examples),
            "synthetic_panel_contexts": sum(len(c["panels"]) for c in self._vocabulary["contexts"]),
            "route_count": len(rows),
            "mapped_source_classes": sum(x is not None for x in mapping.values()),
            "unmapped_source_classes": sum(x is None for x in mapping.values()),
            "selected_temperature": self._temperature,
            "reason_counts": dict(sorted(Counter(row["decision"]["reason"] for row in rows).items())),
            "route_candidate_coverage": neural.ratio(len(offered), len(rows)),
            "route_reference_coverage": neural.ratio(correct, len(rows)),
            "route_selective_error": neural.ratio(len(offered) - correct, len(offered)),
            "safety": {
                "participant_examples": 0,
                "care_ui_connections": 0,
                "candidate_reveals": 0,
                "output_bypasses": sum(row["decision"]["output_action"] != NO_OUTPUT for row in rows),
            },
            "limitations": [
                "crossed_panel_routes_are_dependent_not_independent_samples",
                "two_mapped_classes_not_forty_concept_recognition",
                "synthetic_embeddings_not_speech_features",
                "no_participant_or_clinical_performance_established",
                "temperature_scaling_does_not_guarantee_calibration",
            ],
        }
        artifact = {
            "data_classification": CLASSIFICATION,
            "claim_boundary": CLAIM,
            "provenance": self.provenance,
            "calibration_sha256": self._calibration_id,
            "predictions": rows,
        }
        return artifact, report


def check_expected(report: dict) -> None:
    if report != core.load_json(EXPECTED):
        raise AdapterError("frozen synthetic routing regression changed")


def write_artifacts(output_dir: Path, predictions: dict, report: dict) -> None:
    destination = neural.validate_output_directory(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    paths = [destination / "predictions.json", destination / "metrics.json"]
    if any(path.exists() or path.is_symlink() for path in paths):
        raise AdapterError("refusing to overwrite an artifact or follow a file symlink")
    for path, document in zip(paths, (predictions, report)):
        # Exclusive creation also closes the check/open race for file symlinks.
        with path.open("xb") as stream:
            stream.write(core.canonical_json_bytes(document))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "run"))
    parser.add_argument("--output-dir", type=Path, default=core.ROOT / "tmp" / "synthetic-intent-adapter-v0")
    args = parser.parse_args(argv)
    try:
        adapter = SyntheticIntentAdapter()
        predictions, report = adapter.build_artifacts()
        check_expected(report)
        if args.command == "run":
            write_artifacts(args.output_dir, predictions, report)
        print(
            "Synthetic intent adapter check: OK "
            f"({report['source_test_examples']} test vectors x "
            f"{report['synthetic_panel_contexts']} panels; "
            f"{report['reason_counts'].get('eligible', 0)} sealed candidate routes; "
            "participant examples=0; Care UI connections=0; output bypasses=0)"
        )
        return 0
    except (AdapterError, core.ContractError, neural.NeuralContractError, care.CareArchitectureError, OSError) as exc:
        print(f"Synthetic intent adapter check: FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
