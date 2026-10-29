#!/usr/bin/env python3
"""Validate the participant-free WP2.2 vocabulary and interaction contracts."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


CARE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = CARE_ROOT.parents[2]
IMPLEMENTATION_ROOT = (
    PROJECT_ROOT / "GrossTree" / "Basic" / "Training" / "Implementation"
)
sys.path.insert(0, str(IMPLEMENTATION_ROOT))

import synthetic_g0  # noqa: E402


IMPLEMENTATION_VERSION = "0.1.0"
VOCABULARY_VERSION = "0.2.0"
ARCHITECTURE_VERSION = "1.0.0"
SCENARIO_SCHEMA_VERSION = "1.0.0"
DATA_CLASSIFICATION = "synthetic_no_participant_data"

DEFAULT_VOCABULARY = CARE_ROOT / "synthetic_vocabulary_v1.js"
DEFAULT_VOCABULARY_SCHEMA = CARE_ROOT / "synthetic_vocabulary_v1.schema.json"
DEFAULT_SCENARIOS = CARE_ROOT / "synthetic_interactions_v1.json"
DEFAULT_SCENARIO_SCHEMA = CARE_ROOT / "synthetic_interactions_v1.schema.json"

EXPECTED_ACTIONS = {
    "action-none",
    "action-repeat",
    "action-cancel",
    "action-fallback",
    "action-previous-panel",
    "action-next-panel",
}
EXPECTED_DOMAINS = {
    "basic_need",
    "daily_routine",
    "physical_comfort",
    "environment_control",
    "conversation_repair",
    "response",
    "social_connection",
    "leisure",
    "assistance",
    "interaction_control",
}
EXPECTED_PROHIBITED_DOMAINS = {
    "emergency_instruction",
    "diagnosis",
    "medication_or_treatment_decision",
    "legal_decision",
    "financial_decision",
    "consent_or_capacity",
}
EXPECTED_SCENARIO_PURPOSES = {
    "direct_confirmation",
    "rejection_and_correction",
    "panel_navigation_and_compact_surface",
    "none_to_fallback",
    "repeat_is_non_output",
    "cancel_clears_state",
    "hidden_concept_rejected",
}
ACTION_ARGUMENTS = {
    "SELECT_CONTEXT": {"contextId"},
    "NEXT_PANEL": set(),
    "PREVIOUS_PANEL": set(),
    "PROPOSE": {"conceptId"},
    "CONFIRM": set(),
    "REJECT": set(),
    "NONE": set(),
    "REPEAT": set(),
    "FALLBACK": set(),
    "CANCEL": set(),
    "SET_SURFACE": {"surfaceMode"},
}
FORBIDDEN_FIELD_NAMES = {
    "userId",
    "participantId",
    "speakerId",
    "patientName",
    "audio",
    "transcript",
    "recordingPath",
    "filePath",
    "timestamp",
    "durationMs",
    "confidence",
    "probability",
    "score",
    "eventLog",
    "interactionLog",
    "modelOutput",
}


class CareArchitectureError(ValueError):
    """Raised when the WP2.2 architecture violates its frozen boundary."""


def _walk(value: Any, path: str = "$document"):
    if isinstance(value, dict):
        for key, child in value.items():
            yield path, key, child
            yield from _walk(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, f"{path}[{index}]")


def _require_unique(values: list[str], label: str) -> None:
    duplicates = sorted(name for name, count in Counter(values).items() if count > 1)
    if duplicates:
        raise CareArchitectureError(f"{label} must be unique: {duplicates}")


def load_vocabulary(path: Path = DEFAULT_VOCABULARY) -> dict[str, Any]:
    program = """
const fs = require('fs');
const vm = require('vm');
const sandbox = { window: {} };
vm.createContext(sandbox);
vm.runInContext(fs.readFileSync(process.argv[1], 'utf8'), sandbox);
process.stdout.write(JSON.stringify(sandbox.window.NRLIS_CARE_CONFIG));
"""
    result = subprocess.run(
        ["node", "-e", program, str(path)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise CareArchitectureError(
            f"cannot load synthetic vocabulary with Node.js: {result.stderr.strip()}"
        )
    try:
        value = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise CareArchitectureError("vocabulary did not export valid JSON") from exc
    if not isinstance(value, dict):
        raise CareArchitectureError("vocabulary export must be an object")
    return value


def validate_vocabulary_semantics(config: dict[str, Any]) -> None:
    sensitive = sorted(
        f"{path}.{key}"
        for path, key, _ in _walk(config, "$vocabulary")
        if key in FORBIDDEN_FIELD_NAMES
    )
    if sensitive:
        raise CareArchitectureError(
            "content, identity, model-score, or interaction-log fields are prohibited: "
            + ", ".join(sensitive)
        )

    if config.get("version") != VOCABULARY_VERSION:
        raise CareArchitectureError("vocabulary version must remain 0.2.0")
    if config.get("architectureVersion") != ARCHITECTURE_VERSION:
        raise CareArchitectureError("architecture version must remain 1.0.0")
    if config.get("dataClassification") != DATA_CLASSIFICATION:
        raise CareArchitectureError("vocabulary must remain synthetic-only")

    closed_flags = ("recording", "persistence", "logging", "externalNetwork", "modelInference")
    if any(config.get(name) is not False for name in closed_flags):
        raise CareArchitectureError("recording, persistence, logging, network, and model inference must remain false")
    if config.get("personalization") != "none" or config.get("dialectClaim") != "none":
        raise CareArchitectureError("WP2.2 cannot claim personalization or dialect support")
    if config.get("surfaceModes") != ["canonical", "compact"]:
        raise CareArchitectureError("surface modes must be canonical then compact")
    if config.get("defaultSurfaceMode") != "canonical":
        raise CareArchitectureError("canonical must remain the default surface mode")

    candidate_policy = config.get("candidateSetPolicy", {})
    if candidate_policy != {
        "panelSize": 4,
        "ordering": "fixed_versioned",
        "generation": "curated_lookup_only",
        "modelReranking": False,
    }:
        raise CareArchitectureError("candidate-set policy drifted from fixed four-item lookup")

    safety = config.get("safetyPolicy", {})
    if safety.get("confirmationRequired") is not True:
        raise CareArchitectureError("confirmation must remain mandatory")
    if any(
        safety.get(name) is not False
        for name in ("autoConfirmation", "freeTextGeneration", "careDataResearchReuse")
    ):
        raise CareArchitectureError("auto-confirmation, free text, and care-data reuse must remain false")
    if set(safety.get("prohibitedDomains", [])) != EXPECTED_PROHIBITED_DOMAINS:
        raise CareArchitectureError("prohibited high-risk domains do not match the frozen set")
    if set(config.get("globalActions", [])) != EXPECTED_ACTIONS:
        raise CareArchitectureError("global action set does not match the frozen safe controls")
    if set(config.get("semanticDomains", [])) != EXPECTED_DOMAINS:
        raise CareArchitectureError("semantic domain set does not match the frozen taxonomy")

    contexts = config.get("contexts", [])
    concepts = config.get("concepts", [])
    if len(contexts) != 5 or len(concepts) != 40:
        raise CareArchitectureError("v0.2 fixture must contain 5 contexts and 40 concepts")

    context_ids = [item["id"] for item in contexts]
    concept_ids = [item["id"] for item in concepts]
    panel_ids = [panel["id"] for context in contexts for panel in context["panels"]]
    _require_unique(context_ids, "context IDs")
    _require_unique(concept_ids, "concept IDs")
    _require_unique(panel_ids, "panel IDs")

    concept_by_id = {item["id"]: item for item in concepts}
    references: list[str] = []
    for context in contexts:
        if len(context["panels"]) != 2:
            raise CareArchitectureError(
                f"context {context['id']} must contain exactly two panels"
            )
        for panel in context["panels"]:
            ids = panel["conceptIds"]
            if len(ids) != 4 or len(set(ids)) != 4:
                raise CareArchitectureError(
                    f"panel {panel['id']} must contain four distinct concepts"
                )
            unknown = sorted(set(ids) - set(concept_by_id))
            if unknown:
                raise CareArchitectureError(
                    f"panel {panel['id']} references unknown concepts: {unknown}"
                )
            references.extend(ids)

    counts = Counter(references)
    if set(counts) != set(concept_ids) or any(count != 1 for count in counts.values()):
        raise CareArchitectureError(
            "every synthetic concept must appear in exactly one versioned panel"
        )

    canonical = [item["canonicalText"].strip() for item in concepts]
    compact = [item["compactText"].strip() for item in concepts]
    if any(not text for text in canonical + compact):
        raise CareArchitectureError("surface forms cannot be blank")
    _require_unique(canonical, "canonical surface forms")
    _require_unique(compact, "compact surface forms")
    for concept in concepts:
        if concept["domain"] not in EXPECTED_DOMAINS:
            raise CareArchitectureError(f"unknown semantic domain for {concept['id']}")
        if concept["riskClass"] != "ordinary_care_low_risk":
            raise CareArchitectureError(f"risk class must remain low-risk for {concept['id']}")
        if concept["confirmationPolicy"] != "always_required":
            raise CareArchitectureError(f"confirmation drift for {concept['id']}")
        if concept["outputPolicy"] != "confirmed_visual_only":
            raise CareArchitectureError(f"output policy drift for {concept['id']}")
        if concept["provenance"] != "curated_synthetic":
            raise CareArchitectureError(f"provenance drift for {concept['id']}")


def validate_scenario_semantics(
    suite: dict[str, Any], config: dict[str, Any]
) -> None:
    if suite.get("schemaVersion") != SCENARIO_SCHEMA_VERSION:
        raise CareArchitectureError("scenario schema version must remain 1.0.0")
    if suite.get("dataClassification") != DATA_CLASSIFICATION:
        raise CareArchitectureError("interaction suite must remain synthetic-only")
    if suite.get("participantRecords") != 0 or suite.get("persistence") is not False:
        raise CareArchitectureError("synthetic suite cannot contain or persist interaction records")

    sensitive = sorted(
        f"{path}.{key}"
        for path, key, _ in _walk(suite, "$scenarios")
        if key in FORBIDDEN_FIELD_NAMES
    )
    if sensitive:
        raise CareArchitectureError(
            "synthetic scenarios contain prohibited fields: " + ", ".join(sensitive)
        )

    scenarios = suite.get("scenarios", [])
    scenario_ids = [item["id"] for item in scenarios]
    purposes = [item["purpose"] for item in scenarios]
    _require_unique(scenario_ids, "scenario IDs")
    _require_unique(purposes, "scenario purposes")
    if set(purposes) != EXPECTED_SCENARIO_PURPOSES:
        raise CareArchitectureError("scenario purposes do not cover the frozen suite")

    context_ids = {item["id"] for item in config["contexts"]}
    concept_ids = {item["id"] for item in config["concepts"]}
    optional_argument_names = {"contextId", "conceptId", "surfaceMode"}
    for scenario in scenarios:
        for index, step in enumerate(scenario["steps"]):
            action = step["action"]
            actual_arguments = set(step) & optional_argument_names
            if actual_arguments != ACTION_ARGUMENTS[action]:
                raise CareArchitectureError(
                    f"{scenario['id']} step {index} has invalid arguments for {action}"
                )
            if "contextId" in step and step["contextId"] not in context_ids:
                raise CareArchitectureError(
                    f"{scenario['id']} references unknown context {step['contextId']}"
                )
            if "conceptId" in step and step["conceptId"] not in concept_ids:
                raise CareArchitectureError(
                    f"{scenario['id']} references unknown concept {step['conceptId']}"
                )


def load_and_validate(
    vocabulary_path: Path = DEFAULT_VOCABULARY,
    vocabulary_schema_path: Path = DEFAULT_VOCABULARY_SCHEMA,
    scenarios_path: Path = DEFAULT_SCENARIOS,
    scenario_schema_path: Path = DEFAULT_SCENARIO_SCHEMA,
) -> tuple[dict[str, Any], dict[str, Any]]:
    config = load_vocabulary(vocabulary_path)
    vocabulary_schema = synthetic_g0.load_json(vocabulary_schema_path)
    scenarios = synthetic_g0.load_json(scenarios_path)
    scenario_schema = synthetic_g0.load_json(scenario_schema_path)
    if not isinstance(scenarios, dict):
        raise CareArchitectureError("scenario suite must be an object")
    try:
        synthetic_g0.validate_against_schema(
            config, vocabulary_schema, "care_vocabulary"
        )
        synthetic_g0.validate_against_schema(
            scenarios, scenario_schema, "care_interactions"
        )
    except synthetic_g0.ContractError as exc:
        raise CareArchitectureError(str(exc)) from exc
    validate_vocabulary_semantics(config)
    validate_scenario_semantics(scenarios, config)
    return config, scenarios


def check() -> None:
    config, scenarios = load_and_validate()
    panel_count = sum(len(context["panels"]) for context in config["contexts"])
    print(
        "Care vocabulary architecture check: OK "
        f"({len(config['contexts'])} contexts; {panel_count} panels; "
        f"{len(config['concepts'])} synthetic concepts; "
        f"{len(scenarios['scenarios'])} synthetic interactions; "
        "participant records=0; model inference=0)."
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
    except (CareArchitectureError, synthetic_g0.ContractError) as exc:
        print(f"Care vocabulary architecture check: FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
