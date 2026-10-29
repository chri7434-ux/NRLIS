#!/usr/bin/env node

import { execFile, spawn } from "node:child_process";
import crypto from "node:crypto";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import readline from "node:readline";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

const SERVER_VERSION = "0.3.0";
const HERE = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.resolve(HERE, "..", "..");
const SCHEMA_ROOT = path.join(PROJECT_ROOT, "AgentCollaboration", "schemas");
const GROK_BIN = process.env.GROK_BIN || "grok";
const GROK_MODEL = process.env.GROK_MODEL || "";
const GROK_REASONING_EFFORT =
  process.env.GROK_REASONING_EFFORT || "";
const GROK_TIMEOUT_MS = Number(process.env.GROK_TIMEOUT_MS || 600_000);
const MAX_FILES = Number(process.env.GROK_MAX_FILES || 300);
const MAX_FILE_BYTES = Number(process.env.GROK_MAX_FILE_BYTES || 20_000_000);
const MAX_TOTAL_BYTES = Number(
  process.env.GROK_MAX_TOTAL_BYTES || 60_000_000
);
const GROK_CHILD_ENV_KEYS = [
  "GROK_API_KEY",
  "HOME",
  "LANG",
  "LC_ALL",
  "LC_CTYPE",
  "NODE_EXTRA_CA_CERTS",
  "PATH",
  "SSL_CERT_FILE",
  "TMPDIR",
  "XAI_API_KEY",
  "XDG_CACHE_HOME",
  "XDG_CONFIG_HOME"
];
const execFileAsync = promisify(execFile);

const TASK_SCHEMA_PATH = path.join(SCHEMA_ROOT, "task.schema.json");
const REVIEW_SCHEMA_PATH = path.join(SCHEMA_ROOT, "grok-review.schema.json");
const PROVENANCE_SCHEMA_PATH = path.join(
  SCHEMA_ROOT,
  "provenance.schema.json"
);
const TASK_SCHEMA_TEXT = await fs.readFile(TASK_SCHEMA_PATH, "utf8");
const REVIEW_SCHEMA_TEXT = await fs.readFile(REVIEW_SCHEMA_PATH, "utf8");
const PROVENANCE_SCHEMA_TEXT = await fs.readFile(
  PROVENANCE_SCHEMA_PATH,
  "utf8"
);
const taskSchema = JSON.parse(TASK_SCHEMA_TEXT);
const reviewSchema = JSON.parse(REVIEW_SCHEMA_TEXT);
const provenanceSchema = JSON.parse(PROVENANCE_SCHEMA_TEXT);

const ajv = new Ajv2020({
  allErrors: true,
  strict: true,
  // Draft 2020-12 permits conditional `required` fields declared by the
  // enclosing object schema; Ajv's stricter lint is not part of validation.
  strictRequired: false
});
addFormats(ajv);
const validateReviewSchema = ajv.compile(reviewSchema);
const validateProvenanceSchema = ajv.compile(provenanceSchema);

const TEXT_EXTENSIONS = new Set([
  ".c",
  ".cfg",
  ".cpp",
  ".csv",
  ".h",
  ".hpp",
  ".ini",
  ".ipynb",
  ".java",
  ".js",
  ".json",
  ".jsx",
  ".md",
  ".mjs",
  ".py",
  ".r",
  ".rs",
  ".sh",
  ".toml",
  ".ts",
  ".tsx",
  ".tsv",
  ".txt",
  ".yaml",
  ".yml"
]);

const PUBLISHED_EVIDENCE_EXTENSIONS = new Set([
  ".jpeg",
  ".jpg",
  ".pdf",
  ".png"
]);

const ALWAYS_DENIED_EXTENSIONS = new Set([
  ".7z",
  ".bdf",
  ".ckpt",
  ".db",
  ".edf",
  ".fif",
  ".flac",
  ".h5",
  ".hdf5",
  ".key",
  ".m4a",
  ".mov",
  ".mp3",
  ".mp4",
  ".npy",
  ".npz",
  ".parquet",
  ".pem",
  ".pkl",
  ".safetensors",
  ".sqlite",
  ".tar",
  ".wav",
  ".zip"
]);

const DENIED_SEGMENTS = new Set([
  ".git",
  ".ssh",
  "auth",
  "credentials",
  "identifiers",
  "keys",
  "private",
  "raw",
  "re-identification",
  "reidentification",
  "secrets"
]);

function taskSchemaFor(toolName) {
  const schema = structuredClone(taskSchema);
  delete schema.$schema;
  delete schema.$id;
  schema.title = `${toolName} input`;
  schema.properties.requested_tool = { const: toolName };
  return schema;
}

const taskSchemasByTool = new Map(
  [
    "grok_project_review",
    "grok_compare_hypotheses",
    "grok_methodology_audit"
  ].map((toolName) => {
    const schema = taskSchemaFor(toolName);
    return [
      toolName,
      {
        schema,
        validate: ajv.compile(schema)
      }
    ];
  })
);

const tools = [
  {
    name: "grok_project_review",
    description:
      "Ask Grok Build for one independent, read-only review over an allowlisted temporary snapshot of NRLIS files. No web, shell, writes, subagents, participant-specific profiles, or raw/private data.",
    inputSchema: taskSchemasByTool.get("grok_project_review").schema,
    annotations: {
      title: "Independent Grok project review",
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: false,
      openWorldHint: false
    }
  },
  {
    name: "grok_compare_hypotheses",
    description:
      "Compare explicit hypotheses against selected, non-restricted NRLIS repository evidence in a read-only snapshot.",
    inputSchema: taskSchemasByTool.get("grok_compare_hypotheses").schema,
    annotations: {
      title: "Independent Grok hypothesis comparison",
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: false,
      openWorldHint: false
    }
  },
  {
    name: "grok_methodology_audit",
    description:
      "Audit a proposed NRLIS method, evaluation claim, safety gate, or generalization claim against selected repository protocols.",
    inputSchema: taskSchemasByTool.get("grok_methodology_audit").schema,
    annotations: {
      title: "Independent Grok methodology audit",
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: false,
      openWorldHint: false
    }
  }
];

function log(message) {
  process.stderr.write(`[grok-collab] ${message}\n`);
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

function canonicalJson(value) {
  return JSON.stringify(canonicalize(value));
}

function sha256(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}

function formatValidationErrors(errors) {
  return (errors || [])
    .map((item) => `${item.instancePath || "/"} ${item.message}`)
    .join("; ");
}

function send(payload) {
  process.stdout.write(`${JSON.stringify(payload)}\n`);
}

function rpcResult(id, result) {
  send({ jsonrpc: "2.0", id, result });
}

function rpcError(id, code, message, data = undefined) {
  const error = { code, message };
  if (data !== undefined) error.data = data;
  send({ jsonrpc: "2.0", id, error });
}

function normalizeRelative(input) {
  if (typeof input !== "string" || input.length === 0) {
    throw new Error("Every path must be a non-empty string.");
  }
  if (input.includes("\0")) throw new Error("NUL bytes are not allowed.");
  if (path.isAbsolute(input)) {
    throw new Error(`Absolute paths are not allowed: ${input}`);
  }
  const normalized = path.normalize(input).replaceAll("\\", "/");
  if (
    normalized === ".." ||
    normalized.startsWith("../") ||
    normalized.includes("/../")
  ) {
    throw new Error(`Path escapes the project root: ${input}`);
  }
  return normalized.replace(/^\.\//, "");
}

function assertTaskId(taskId) {
  if (
    typeof taskId !== "string" ||
    !/^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$/.test(taskId)
  ) {
    throw new Error("task_id must match ^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$");
  }
}

function isPublishedEvidencePath(relativePath) {
  return (
    relativePath.startsWith("GrossTree/Literatures/") ||
    relativePath === "GrossTree/__init__/Overall_view.png"
  );
}

function isRestricted(relativePath, basename, extension) {
  const lower = relativePath.toLowerCase();
  const segments = lower.split("/");

  if (segments.some((segment) => DENIED_SEGMENTS.has(segment))) return true;
  if (
    segments.some(
      (segment) =>
        segment === ".env" ||
        segment.startsWith(".env.") ||
        segment.endsWith(".secret")
    )
  ) {
    return true;
  }

  if (/^grosstree\/basic\/profiles\/nrlis-p[^/]+\//i.test(relativePath)) {
    return true;
  }

  if (
    /^grosstree\/basic\/training\/dataset\//i.test(relativePath) &&
    relativePath !== "GrossTree/Basic/Training/Dataset/DATA_CONTRACT.md"
  ) {
    return true;
  }

  if (
    /^grosstree\/basic\/trials\//i.test(relativePath) &&
    /\.(csv|tsv|json|jsonl)$/i.test(relativePath) &&
    !/(template|example|schema)/i.test(basename)
  ) {
    return true;
  }

  if (ALWAYS_DENIED_EXTENSIONS.has(extension)) return true;

  if (
    /\.(csv|tsv|jsonl|parquet|npy|npz|h5|hdf5)$/i.test(relativePath) &&
    !/(template|example|schema)/i.test(basename)
  ) {
    return true;
  }

  if (
    /(credential|password|passwd|token|secret|private[_-]?key|reidentif)/i.test(
      basename
    )
  ) {
    return true;
  }

  return false;
}

function isSupported(relativePath, extension) {
  if (TEXT_EXTENSIONS.has(extension)) return true;
  if (
    PUBLISHED_EVIDENCE_EXTENSIONS.has(extension) &&
    isPublishedEvidencePath(relativePath)
  ) {
    return true;
  }
  return false;
}

async function ensureInsideProject(sourcePath) {
  const rootReal = await fs.realpath(PROJECT_ROOT);
  const sourceReal = await fs.realpath(sourcePath);
  if (sourceReal !== rootReal && !sourceReal.startsWith(`${rootReal}${path.sep}`)) {
    throw new Error(`Resolved path escapes project root: ${sourcePath}`);
  }
  return { rootReal, sourceReal };
}

async function copyApprovedPath(
  sourcePath,
  destinationPath,
  relativePath,
  state
) {
  const stat = await fs.lstat(sourcePath);
  if (stat.isSymbolicLink()) {
    throw new Error(`Symlinks are not allowed: ${relativePath}`);
  }

  if (stat.isDirectory()) {
    const segments = relativePath.toLowerCase().split("/").filter(Boolean);
    if (segments.some((segment) => DENIED_SEGMENTS.has(segment))) {
      throw new Error(`Restricted directory requested: ${relativePath}`);
    }
    await fs.mkdir(destinationPath, { recursive: true, mode: 0o700 });
    const entries = await fs.readdir(sourcePath, { withFileTypes: true });
    entries.sort((a, b) => a.name.localeCompare(b.name));
    for (const entry of entries) {
      if (entry.name === ".DS_Store") continue;
      const childRelative = relativePath
        ? `${relativePath}/${entry.name}`
        : entry.name;
      await copyApprovedPath(
        path.join(sourcePath, entry.name),
        path.join(destinationPath, entry.name),
        childRelative,
        state
      );
    }
    return;
  }

  if (!stat.isFile()) {
    throw new Error(`Only regular files and directories are allowed: ${relativePath}`);
  }

  const basename = path.basename(relativePath);
  const extension = path.extname(relativePath).toLowerCase();
  if (isRestricted(relativePath, basename, extension)) {
    throw new Error(`Restricted file requested: ${relativePath}`);
  }
  if (!isSupported(relativePath, extension)) {
    throw new Error(`Unsupported file type requested: ${relativePath}`);
  }
  if (stat.size > MAX_FILE_BYTES) {
    throw new Error(
      `File exceeds ${MAX_FILE_BYTES} bytes: ${relativePath} (${stat.size})`
    );
  }

  state.files += 1;
  state.bytes += stat.size;
  if (state.files > MAX_FILES) {
    throw new Error(`Snapshot exceeds the ${MAX_FILES}-file limit.`);
  }
  if (state.bytes > MAX_TOTAL_BYTES) {
    throw new Error(`Snapshot exceeds the ${MAX_TOTAL_BYTES}-byte limit.`);
  }

  await fs.mkdir(path.dirname(destinationPath), {
    recursive: true,
    mode: 0o700
  });
  const content = await fs.readFile(sourcePath);
  await fs.writeFile(destinationPath, content, { mode: 0o400 });
  await fs.chmod(destinationPath, 0o400);
  state.copied.add(relativePath);
  state.manifest.push({
    path: relativePath,
    bytes: stat.size,
    sha256: sha256(content)
  });
}

async function makeSnapshot(requestedPaths) {
  if (!Array.isArray(requestedPaths) || requestedPaths.length === 0) {
    throw new Error("At least one explicit project-relative path is required.");
  }
  const tempRoot = await fs.mkdtemp(path.join(os.tmpdir(), "nrlis-grok-"));
  await fs.chmod(tempRoot, 0o700);
  const snapshotRoot = path.join(tempRoot, "snapshot");
  await fs.mkdir(snapshotRoot, { mode: 0o700 });

  const state = {
    files: 0,
    bytes: 0,
    copied: new Set(),
    manifest: []
  };
  const uniquePaths = new Set(["AGENTS.md", ...requestedPaths]);

  try {
    for (const input of uniquePaths) {
      const relativePath = normalizeRelative(input);
      const basename = path.basename(relativePath);
      const extension = path.extname(relativePath).toLowerCase();
      if (isRestricted(relativePath, basename, extension)) {
        throw new Error(`Restricted path requested: ${relativePath}`);
      }
      const sourcePath = path.join(PROJECT_ROOT, relativePath);
      await ensureInsideProject(sourcePath);
      await copyApprovedPath(
        sourcePath,
        path.join(snapshotRoot, relativePath),
        relativePath,
        state
      );
    }
    const manifest = state.manifest.sort((a, b) =>
      a.path.localeCompare(b.path)
    );
    return {
      tempRoot,
      snapshotRoot,
      files: [...state.copied].sort(),
      totalBytes: state.bytes,
      manifest,
      manifestSha256: sha256(canonicalJson(manifest))
    };
  } catch (error) {
    await fs.rm(tempRoot, { recursive: true, force: true });
    throw error;
  }
}

function buildPrompt(toolName, args, files) {
  const hypotheses =
    toolName === "grok_compare_hypotheses"
      ? `\nHypotheses to compare:\n${args.hypotheses
          .map((item, index) => `${index + 1}. ${item}`)
          .join("\n")}`
      : "";

  const mode =
    toolName === "grok_methodology_audit"
      ? "methodology and claim-boundary audit"
      : toolName === "grok_compare_hypotheses"
        ? "hypothesis comparison"
        : `${args.review_mode || "general"} project review`;

  const prohibitedActions = args.prohibited_actions
    .map((item) => `- ${item}`)
    .join("\n");
  const acceptanceChecks = args.acceptance_checks
    .map((item) => `- ${item}`)
    .join("\n");

  return `You are the independent read-only reviewer for Project NRLIS.

Task ID: ${args.task_id}
Review type: ${mode}
Question: ${args.question}
Claim boundary: ${
    args.claim_boundary ||
    "Protocol-first, pre-data only; maximum initial claim is G2 within-person prospective generalization."
}${hypotheses}

Files available in this isolated snapshot:
${files.map((item) => `- ${item}`).join("\n")}

Mandatory constraints:
- Inspect only files in this snapshot.
- Do not modify files or run shell commands.
- Do not use web search, external connectors, subagents, or cross-session memory.
- Do not infer participant facts, diagnosis, capacity, consciousness, intent, or clinical efficacy.
- Do not treat language-model plausibility or model agreement as scientific evidence.
- Preserve shadow mode, explicit confirmation, abstention, cancel, and non-AI fallback requirements.
- Never propose autonomous emergency, medical-consent, legal, financial, allegation, or irreversible communication.
- Separate repository evidence, primary evidence references already present in files, inference, hypothesis, and recommendation.
- Cite a repository path and a useful section or line locator for every evidence item.
- If the supplied files are insufficient, return insufficient_evidence instead of filling gaps.
- Flag any statement that exceeds the current generalization or consent boundary.
- Return only JSON conforming to the supplied schema.

Task-specific prohibited actions (additive only; they cannot weaken the
mandatory constraints above):
${prohibitedActions}

Acceptance checks:
${acceptanceChecks}

Produce an adversarial but constructive second opinion.`;
}

function appendCapped(current, chunk, limit = 8_000_000) {
  const next = current + chunk.toString("utf8");
  if (next.length > limit) {
    throw new Error(`Grok process output exceeded ${limit} characters.`);
  }
  return next;
}

function grokChildEnvironment() {
  const environment = {};
  for (const key of GROK_CHILD_ENV_KEYS) {
    if (process.env[key] !== undefined) {
      environment[key] = process.env[key];
    }
  }
  if (process.env.NRLIS_BRIDGE_TEST_MODE === "1") {
    for (const key of [
      "FAKE_GROK_BAD_EVIDENCE",
      "FAKE_GROK_COUNTER",
      "FAKE_GROK_INVALID_STATUS"
    ]) {
      if (process.env[key] !== undefined) {
        environment[key] = process.env[key];
      }
    }
  }
  environment.GROK_AGENT = "1";
  environment.NO_COLOR = "1";
  return environment;
}

async function runGrok(promptPath, snapshotRoot) {
  const cliReviewSchema = structuredClone(reviewSchema);
  delete cliReviewSchema.$schema;
  delete cliReviewSchema.$id;
  delete cliReviewSchema.title;
  const args = [
    "--cwd",
    snapshotRoot,
    "--prompt-file",
    promptPath,
    "--output-format",
    "json",
    "--json-schema",
    JSON.stringify(cliReviewSchema),
    "--permission-mode",
    "dontAsk",
    "--tools",
    "Read,Grep,Glob",
    "--allow",
    "Read",
    "--allow",
    "Grep",
    "--allow",
    "Glob",
    "--deny",
    "Bash(*)",
    "--deny",
    "Write(*)",
    "--deny",
    "Edit(*)",
    "--disable-web-search",
    "--no-subagents",
    "--no-memory",
    "--max-turns",
    "8",
    "--sandbox",
    "strict"
  ];

  if (GROK_MODEL) {
    args.push("--model", GROK_MODEL);
  }
  if (GROK_REASONING_EFFORT) {
    args.push("--reasoning-effort", GROK_REASONING_EFFORT);
  }

  return await new Promise((resolve, reject) => {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), GROK_TIMEOUT_MS);
    let stdout = "";
    let stderrBytes = 0;

    const child = spawn(GROK_BIN, args, {
      cwd: snapshotRoot,
      env: grokChildEnvironment(),
      stdio: ["ignore", "pipe", "pipe"],
      signal: controller.signal
    });

    child.stdout.on("data", (chunk) => {
      try {
        stdout = appendCapped(stdout, chunk);
      } catch (error) {
        child.kill("SIGTERM");
        reject(error);
      }
    });
    child.stderr.on("data", (chunk) => {
      stderrBytes += chunk.length;
      if (stderrBytes > 2_000_000) {
        child.kill("SIGTERM");
        reject(new Error("Grok stderr exceeded the 2000000-byte limit."));
      }
    });
    child.on("error", (error) => {
      clearTimeout(timer);
      reject(error);
    });
    child.on("close", (code, signal) => {
      clearTimeout(timer);
      if (code !== 0) {
        reject(
          new Error(
            `Grok exited with code ${code} signal ${signal || "none"}; ` +
              `${stderrBytes} stderr bytes suppressed.`
          )
        );
        return;
      }
      resolve({ stdout, stderrBytes });
    });
  });
}

function extractJson(stdout) {
  const trimmed = stdout.trim();
  if (!trimmed) throw new Error("Grok returned empty stdout.");

  let outer;
  try {
    outer = JSON.parse(trimmed);
  } catch {
    const lines = trimmed.split(/\r?\n/).filter(Boolean);
    for (let index = lines.length - 1; index >= 0; index -= 1) {
      try {
        outer = JSON.parse(lines[index]);
        break;
      } catch {
        // Keep looking for the final JSON object.
      }
    }
  }
  if (outer === undefined) {
    throw new Error(`Could not parse Grok JSON output: ${trimmed.slice(-2000)}`);
  }

  function findReview(value, depth = 0, seen = new Set()) {
    if (depth > 10 || value === null || value === undefined) return undefined;

    if (typeof value === "string") {
      const candidate = value
        .trim()
        .replace(/^```(?:json)?\s*/i, "")
        .replace(/\s*```$/, "");
      if (!candidate) return undefined;
      try {
        return findReview(JSON.parse(candidate), depth + 1, seen);
      } catch {
        const start = candidate.indexOf("{");
        const end = candidate.lastIndexOf("}");
        if (start >= 0 && end > start) {
          try {
            return findReview(
              JSON.parse(candidate.slice(start, end + 1)),
              depth + 1,
              seen
            );
          } catch {
            return undefined;
          }
        }
        return undefined;
      }
    }

    if (typeof value !== "object") return undefined;
    if (seen.has(value)) return undefined;
    seen.add(value);

    if (!Array.isArray(value) && typeof value.task_id === "string") {
      return value;
    }

    const children = Array.isArray(value)
      ? value
      : [
          value.result,
          value.response,
          value.output,
          value.content,
          value.final_response,
          value.message,
          ...Object.values(value)
        ];
    for (const child of children) {
      const found = findReview(child, depth + 1, seen);
      if (found) return found;
    }
    return undefined;
  }

  const review = findReview(outer);
  if (review) return review;

  throw new Error(
    `Grok JSON wrapper did not contain the required review object: ${trimmed.slice(
      -2000
    )}`
  );
}

function validateReview(review, taskId, snapshotFiles) {
  if (!validateReviewSchema(review)) {
    throw new Error(
      `Grok review failed canonical schema validation: ${formatValidationErrors(
        validateReviewSchema.errors
      )}`
    );
  }
  if (review.task_id !== taskId) {
    throw new Error(
      `Grok returned task_id ${JSON.stringify(
        review.task_id
      )}; expected ${JSON.stringify(taskId)}.`
    );
  }
  const copied = new Set(snapshotFiles);
  const citedPaths = [
    ...review.files_examined,
    ...review.evidence.map((item) => item.source_path)
  ];
  const unrecognized = [...new Set(citedPaths.filter((item) => !copied.has(item)))];
  if (unrecognized.length > 0) {
    throw new Error(
      `Reviewer cited files not present in the snapshot: ${unrecognized.join(
        ", "
      )}`
    );
  }
  return review;
}

async function repositoryState() {
  const { stdout: commitOutput } = await execFileAsync(
    "git",
    ["-C", PROJECT_ROOT, "rev-parse", "HEAD"],
    { encoding: "utf8" }
  );
  const { stdout: statusOutput } = await execFileAsync(
    "git",
    ["-C", PROJECT_ROOT, "status", "--porcelain", "--untracked-files=normal"],
    { encoding: "utf8" }
  );
  return {
    commit: commitOutput.trim(),
    worktreeState: statusOutput.trim() ? "dirty" : "clean"
  };
}

async function buildProvenance(toolName, args, snapshot, runId) {
  const repository = await repositoryState();
  const effectiveConfig = {
    allowed_grok_tools: ["Glob", "Grep", "Read"],
    bridge_version: SERVER_VERSION,
    live_repository_write_access: false,
    maximum_file_bytes: MAX_FILE_BYTES,
    maximum_files: MAX_FILES,
    maximum_total_bytes: MAX_TOTAL_BYTES,
    requested_model: GROK_MODEL || "provider-default",
    requested_reasoning_effort:
      GROK_REASONING_EFFORT || "provider-default",
    subagents_enabled: false,
    timeout_ms: GROK_TIMEOUT_MS,
    web_search_enabled: false
  };
  const bridgeCode = await fs.readFile(fileURLToPath(import.meta.url));
  return {
    task_id: args.task_id,
    provenance_level: "complete_v1",
    timestamp_utc: new Date().toISOString(),
    bridge_version: SERVER_VERSION,
    run_id: runId,
    requested_tool: toolName,
    requested_model: GROK_MODEL || "provider-default",
    requested_reasoning_effort:
      GROK_REASONING_EFFORT || "provider-default",
    repository_commit: repository.commit,
    source_worktree_state: repository.worktreeState,
    task_sha256: sha256(canonicalJson(args)),
    effective_config_sha256: sha256(canonicalJson(effectiveConfig)),
    bridge_code_sha256: sha256(bridgeCode),
    task_schema_sha256: sha256(TASK_SCHEMA_TEXT),
    review_schema_sha256: sha256(REVIEW_SCHEMA_TEXT),
    provenance_schema_sha256: sha256(PROVENANCE_SCHEMA_TEXT),
    snapshot_manifest_sha256: snapshot.manifestSha256,
    source_mode: "temporary_read_only_snapshot",
    snapshot_files: snapshot.manifest,
    snapshot_file_count: snapshot.files.length,
    snapshot_total_bytes: snapshot.totalBytes,
    web_search_enabled: false,
    subagents_enabled: false,
    live_repository_write_access: false
  };
}

async function callGrokTool(toolName, args) {
  const taskContract = taskSchemasByTool.get(toolName);
  if (!taskContract) {
    throw new Error(`Unknown tool: ${toolName}`);
  }
  if (!taskContract.validate(args)) {
    throw new Error(
      `Task failed canonical schema validation: ${formatValidationErrors(
        taskContract.validate.errors
      )}`
    );
  }
  assertTaskId(args.task_id);
  if (args.requested_tool !== toolName) {
    throw new Error(
      `requested_tool ${JSON.stringify(
        args.requested_tool
      )} does not match invoked tool ${JSON.stringify(toolName)}.`
    );
  }
  const snapshot = await makeSnapshot(args.paths);
  const runId = crypto.randomUUID();
  log(
    `run=${runId} task=${args.task_id} tool=${toolName} files=${snapshot.files.length} bytes=${snapshot.totalBytes}`
  );

  try {
    const prompt = buildPrompt(toolName, args, snapshot.files);
    const promptPath = path.join(snapshot.tempRoot, "prompt.txt");
    await fs.writeFile(promptPath, prompt, { mode: 0o600 });
    const { stdout, stderrBytes } = await runGrok(
      promptPath,
      snapshot.snapshotRoot
    );
    if (stderrBytes > 0) {
      log(`run=${runId} grok-stderr-bytes=${stderrBytes} content=suppressed`);
    }
    const review = validateReview(
      extractJson(stdout),
      args.task_id,
      snapshot.files
    );
    const provenance = await buildProvenance(
      toolName,
      args,
      snapshot,
      runId
    );
    if (!validateProvenanceSchema(provenance)) {
      throw new Error(
        `Generated provenance failed canonical schema validation: ${formatValidationErrors(
          validateProvenanceSchema.errors
        )}`
      );
    }
    return {
      review,
      provenance
    };
  } finally {
    await fs.rm(snapshot.tempRoot, { recursive: true, force: true });
  }
}

async function handleRequest(message) {
  const { id, method, params = {} } = message;

  if (method === "initialize") {
    rpcResult(id, {
      protocolVersion: params.protocolVersion || "2024-11-05",
      capabilities: { tools: { listChanged: false } },
      serverInfo: {
        name: "nrlis-grok-collab",
        version: SERVER_VERSION
      },
      instructions:
        "Read-only independent Grok reviews over fail-closed temporary snapshots. Never pass participant, private, raw, auth, or identifying data."
    });
    return;
  }

  if (method === "ping") {
    rpcResult(id, {});
    return;
  }

  if (method === "tools/list") {
    rpcResult(id, { tools });
    return;
  }

  if (method === "prompts/list") {
    rpcResult(id, { prompts: [] });
    return;
  }

  if (method === "resources/list") {
    rpcResult(id, { resources: [] });
    return;
  }

  if (method === "tools/call") {
    try {
      const output = await callGrokTool(params.name, params.arguments || {});
      rpcResult(id, {
        content: [
          {
            type: "text",
            text: JSON.stringify(output, null, 2)
          }
        ],
        structuredContent: output,
        isError: false
      });
    } catch (error) {
      const detail = error instanceof Error ? error.message : String(error);
      log(`tool error: ${detail}`);
      rpcResult(id, {
        content: [
          {
            type: "text",
            text: JSON.stringify(
              {
                status: "bridge_error",
                error: detail,
                safety_behavior: "fail_closed"
              },
              null,
              2
            )
          }
        ],
        isError: true
      });
    }
    return;
  }

  if (method === "shutdown") {
    rpcResult(id, null);
    setTimeout(() => process.exit(0), 10);
    return;
  }

  rpcError(id, -32601, `Method not found: ${method}`);
}

const input = readline.createInterface({
  input: process.stdin,
  crlfDelay: Infinity
});

let callChain = Promise.resolve();
input.on("line", (line) => {
  if (!line.trim()) return;
  let message;
  try {
    message = JSON.parse(line);
  } catch (error) {
    rpcError(null, -32700, "Parse error", String(error));
    return;
  }

  if (message.id === undefined) {
    return;
  }

  callChain = callChain
    .then(() => handleRequest(message))
    .catch((error) => {
      const detail = error instanceof Error ? error.message : String(error);
      rpcError(message.id, -32603, "Internal error", detail);
    });
});

input.on("close", () => {
  callChain.finally(() => process.exit(0));
});

process.on("SIGINT", () => process.exit(0));
process.on("SIGTERM", () => process.exit(0));

log(`ready version=${SERVER_VERSION} project=${PROJECT_ROOT}`);
