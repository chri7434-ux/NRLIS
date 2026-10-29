#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const COLLAB_ROOT = path.resolve(HERE, "..");
const PROJECT_ROOT = path.resolve(COLLAB_ROOT, "..");
const SCHEMA_ROOT = path.join(COLLAB_ROOT, "schemas");
const LEGACY_PROVENANCE_ALLOWLIST = new Set([
  "AgentCollaboration/runs/NRLIS-INFRA-BASELINE-001-R1/provenance.json",
  "AgentCollaboration/runs/NRLIS-SMOKE-001/provenance.json"
]);

async function loadJson(filePath) {
  return JSON.parse(await fs.readFile(filePath, "utf8"));
}

async function filesNamed(root, targetName) {
  const found = [];
  const entries = await fs.readdir(root, { withFileTypes: true });
  for (const entry of entries) {
    const item = path.join(root, entry.name);
    if (entry.isDirectory()) {
      found.push(...(await filesNamed(item, targetName)));
    } else if (entry.isFile() && entry.name === targetName) {
      found.push(item);
    }
  }
  return found.sort();
}

function assertValid(validate, value, label) {
  if (validate(value)) return;
  const detail = (validate.errors || [])
    .map((error) => `${error.instancePath || "/"} ${error.message}`)
    .join("; ");
  throw new Error(`${label} failed schema validation: ${detail}`);
}

function canonicalize(value) {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((key) => [key, canonicalize(value[key])])
    );
  }
  return value;
}

function sha256(value) {
  return crypto
    .createHash("sha256")
    .update(JSON.stringify(canonicalize(value)))
    .digest("hex");
}

const ajv = new Ajv2020({
  allErrors: true,
  strict: true,
  strictRequired: false
});
addFormats(ajv);

const taskSchema = await loadJson(path.join(SCHEMA_ROOT, "task.schema.json"));
const reviewSchema = await loadJson(
  path.join(SCHEMA_ROOT, "grok-review.schema.json")
);
const provenanceSchema = await loadJson(
  path.join(SCHEMA_ROOT, "provenance.schema.json")
);
const fixtureSchema = await loadJson(
  path.join(
    PROJECT_ROOT,
    "GrossTree",
    "Basic",
    "Training",
    "Dataset",
    "synthetic_g0.schema.json"
  )
);
const configSchema = await loadJson(
  path.join(
    PROJECT_ROOT,
    "GrossTree",
    "Basic",
    "Training",
    "Config",
    "synthetic_g0_config.schema.json"
  )
);
const wp1RegistrySchema = await loadJson(
  path.join(
    PROJECT_ROOT,
    "GrossTree",
    "Basic",
    "Training",
    "Config",
    "wp1_gate_registry.schema.json"
  )
);

for (const [label, schema] of [
  ["task.schema.json", taskSchema],
  ["grok-review.schema.json", reviewSchema],
  ["provenance.schema.json", provenanceSchema],
  ["synthetic_g0.schema.json", fixtureSchema],
  ["synthetic_g0_config.schema.json", configSchema],
  ["wp1_gate_registry.schema.json", wp1RegistrySchema]
]) {
  if (!ajv.validateSchema(schema)) {
    throw new Error(
      `${label} is not a valid JSON Schema: ${JSON.stringify(ajv.errors)}`
    );
  }
}

const validateTask = ajv.compile(taskSchema);
const validateReview = ajv.compile(reviewSchema);
const validateProvenance = ajv.compile(provenanceSchema);
const validateFixture = ajv.compile(fixtureSchema);
const validateConfig = ajv.compile(configSchema);
const validateWP1Registry = ajv.compile(wp1RegistrySchema);

const cliArgs = process.argv.slice(2);
if (cliArgs.length > 0) {
  if (cliArgs.length !== 2 || cliArgs[0] !== "--wp1-only") {
    throw new Error("Usage: validate-artifacts.mjs [--wp1-only REGISTRY_PATH]");
  }
  const wp1OnlyPath = path.resolve(cliArgs[1]);
  const wp1OnlyRegistry = await loadJson(wp1OnlyPath);
  assertValid(validateWP1Registry, wp1OnlyRegistry, wp1OnlyPath);
  process.stdout.write("WP1 JSON Schema validation: OK.\n");
  process.exit(0);
}

const taskExample = await loadJson(
  path.join(COLLAB_ROOT, "templates", "task.example.json")
);
assertValid(validateTask, taskExample, "task.example.json");

const runRoot = path.join(COLLAB_ROOT, "runs");
const reviewFiles = await filesNamed(runRoot, "review.json");
const provenanceFiles = await filesNamed(runRoot, "provenance.json");
const reviewsByTask = new Map();
for (const filePath of reviewFiles) {
  const review = await loadJson(filePath);
  assertValid(validateReview, review, path.relative(PROJECT_ROOT, filePath));
  const directoryTask = path.basename(path.dirname(filePath));
  if (review.task_id !== directoryTask) {
    throw new Error(`${filePath} task_id does not match its run directory.`);
  }
  reviewsByTask.set(review.task_id, review);
}
for (const filePath of provenanceFiles) {
  const provenance = await loadJson(filePath);
  const relativePath = path.relative(PROJECT_ROOT, filePath).replaceAll("\\", "/");
  assertValid(
    validateProvenance,
    provenance,
    relativePath
  );
  const directoryTask = path.basename(path.dirname(filePath));
  if (provenance.task_id !== directoryTask) {
    throw new Error(`${filePath} task_id does not match its run directory.`);
  }
  if (provenance.provenance_level === "legacy_partial") {
    if (!LEGACY_PROVENANCE_ALLOWLIST.has(relativePath)) {
      throw new Error(
        `${relativePath} uses legacy_partial outside the historical allowlist.`
      );
    }
    continue;
  }

  const manifest = [...provenance.snapshot_files].sort((left, right) =>
    left.path.localeCompare(right.path)
  );
  if (manifest.length !== provenance.snapshot_file_count) {
    throw new Error(`${relativePath} snapshot_file_count is inconsistent.`);
  }
  const totalBytes = manifest.reduce((total, item) => total + item.bytes, 0);
  if (totalBytes !== provenance.snapshot_total_bytes) {
    throw new Error(`${relativePath} snapshot_total_bytes is inconsistent.`);
  }
  if (sha256(manifest) !== provenance.snapshot_manifest_sha256) {
    throw new Error(`${relativePath} snapshot manifest hash is inconsistent.`);
  }

  const review = reviewsByTask.get(provenance.task_id);
  if (review) {
    const snapshotPaths = new Set(manifest.map((item) => item.path));
    const citedPaths = [
      ...review.files_examined,
      ...review.evidence.map((item) => item.source_path)
    ];
    const outsideSnapshot = [
      ...new Set(citedPaths.filter((item) => !snapshotPaths.has(item)))
    ];
    if (outsideSnapshot.length > 0) {
      throw new Error(
        `${relativePath} review cites paths outside its snapshot: ` +
          outsideSnapshot.join(", ")
      );
    }
  }
}

const fixture = await loadJson(
  path.join(
    PROJECT_ROOT,
    "GrossTree",
    "Basic",
    "Training",
    "Dataset",
    "synthetic_g0_fixture.json"
  )
);
const config = await loadJson(
  path.join(
    PROJECT_ROOT,
    "GrossTree",
    "Basic",
    "Training",
    "Config",
    "synthetic_g0_baseline.json"
  )
);
const wp1Registry = await loadJson(
  path.join(
    PROJECT_ROOT,
    "GrossTree",
    "Basic",
    "Training",
    "Config",
    "wp1_gate_registry.json"
  )
);
assertValid(validateFixture, fixture, "synthetic_g0_fixture.json");
assertValid(validateConfig, config, "synthetic_g0_baseline.json");
assertValid(validateWP1Registry, wp1Registry, "wp1_gate_registry.json");

process.stdout.write(
  `JSON Schema validation: OK (${reviewFiles.length} reviews, ` +
    `${provenanceFiles.length} provenance records, 1 task, ` +
    "2 synthetic artifacts, 1 WP1 registry).\n"
);
