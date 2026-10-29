import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import readline from "node:readline";
import test from "node:test";
import { fileURLToPath, pathToFileURL } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.resolve(HERE, "..", "..");
const PYTHON = process.env.NRLIS_PYTHON || "python3";
const SERVER = path.join(
  PROJECT_ROOT,
  "AgentCollaboration",
  "grok-mcp",
  "server.mjs"
);
const FAKE_GROK = path.join(HERE, "fake-grok.mjs");
const WP1_VALIDATOR = path.join(
  PROJECT_ROOT,
  "GrossTree",
  "Basic",
  "Training",
  "Implementation",
  "validate_wp1.py"
);
const WP1_REGISTRY = path.join(
  PROJECT_ROOT,
  "GrossTree",
  "Basic",
  "Training",
  "Config",
  "wp1_gate_registry.json"
);
const TASK_EXAMPLE = JSON.parse(
  await fs.readFile(
    path.join(
      PROJECT_ROOT,
      "AgentCollaboration",
      "templates",
      "task.example.json"
    ),
    "utf8"
  )
);

async function runProgram(command, args, cwd = PROJECT_ROOT) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, {
      cwd,
      env: process.env,
      stdio: ["ignore", "pipe", "pipe"]
    });
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (chunk) => {
      stdout += chunk.toString("utf8");
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString("utf8");
    });
    child.on("error", reject);
    child.on("close", (code, signal) => {
      resolve({ code, signal, stdout, stderr });
    });
  });
}

async function startServer(extraEnv = {}, launch = {}) {
  const temporary = await fs.mkdtemp(path.join(os.tmpdir(), "nrlis-fake-grok-"));
  const fakeLauncher = path.join(temporary, "fake-grok.mjs");
  await fs.writeFile(
    fakeLauncher,
    `#!/usr/bin/env node\nawait import(${JSON.stringify(
      pathToFileURL(FAKE_GROK).href
    )});\n`,
    { mode: 0o700 }
  );
  const child = spawn(
    launch.command || process.execPath,
    launch.args || [SERVER],
    {
    cwd: launch.cwd || os.tmpdir(),
    env: {
      ...process.env,
      GROK_BIN: fakeLauncher,
      GROK_MODEL: "fake-model",
      GROK_REASONING_EFFORT: "test",
      NRLIS_BRIDGE_TEST_MODE: "1",
      ...extraEnv
    },
    stdio: ["pipe", "pipe", "pipe"]
    }
  );
  const lines = readline.createInterface({
    input: child.stdout,
    crlfDelay: Infinity
  });
  const pending = new Map();
  let stderr = "";
  let nextId = 1;
  child.stderr.on("data", (chunk) => {
    stderr += chunk.toString("utf8");
  });
  lines.on("line", (line) => {
    const message = JSON.parse(line);
    const waiter = pending.get(message.id);
    if (!waiter) return;
    pending.delete(message.id);
    if (message.error) {
      waiter.reject(new Error(message.error.message));
    } else {
      waiter.resolve(message.result);
    }
  });
  child.on("exit", (code, signal) => {
    const detail =
      `Bridge exited before replying (code=${code}, signal=${signal}): ` +
      stderr.slice(-2000);
    for (const waiter of pending.values()) waiter.reject(new Error(detail));
    pending.clear();
  });
  function request(method, params = {}) {
    const id = nextId;
    nextId += 1;
    child.stdin.write(
      `${JSON.stringify({ jsonrpc: "2.0", id, method, params })}\n`
    );
    return new Promise((resolve, reject) =>
      pending.set(id, { resolve, reject })
    );
  }
  async function close() {
    child.stdin.end();
    child.kill("SIGTERM");
    lines.close();
    await fs.rm(temporary, { recursive: true, force: true });
  }
  return { child, request, close };
}

test("portable startup exposes canonical v0.3 tools", async (t) => {
  const config = await fs.readFile(
    path.join(PROJECT_ROOT, ".codex", "config.toml"),
    "utf8"
  );
  assert.doesNotMatch(config, /\/Users\/|GROK_PROJECT_ROOT|GROK_BIN/);
  const server = await startServer();
  t.after(server.close);
  const initialized = await server.request("initialize");
  const listed = await server.request("tools/list");
  assert.equal(initialized.serverInfo.version, "0.3.0");
  assert.equal(listed.tools.length, 3);
  assert.ok(
    listed.tools.every((tool) =>
      tool.inputSchema.required.includes("requested_tool")
    )
  );
});

test("repository Codex config launches the relative v0.3 server", async (t) => {
  const config = await fs.readFile(
    path.join(PROJECT_ROOT, ".codex", "config.toml"),
    "utf8"
  );
  const command = config.match(/^command = "([^"]+)"$/m)?.[1];
  const relativeServer = config.match(/^args = \["([^"]+)"\]$/m)?.[1];
  assert.equal(command, "node");
  assert.equal(
    relativeServer,
    "AgentCollaboration/grok-mcp/server.mjs"
  );
  const server = await startServer(
    {},
    {
      command,
      args: [relativeServer],
      cwd: PROJECT_ROOT
    }
  );
  t.after(server.close);
  const initialized = await server.request("initialize");
  assert.equal(initialized.serverInfo.version, "0.3.0");
});

test("canonical task returns review plus complete provenance", async (t) => {
  const server = await startServer({
    UNRELATED_SECRET_SENTINEL: "must-not-reach-reviewer"
  });
  t.after(server.close);
  await server.request("initialize");
  const result = await server.request("tools/call", {
    name: TASK_EXAMPLE.requested_tool,
    arguments: TASK_EXAMPLE
  });
  assert.equal(result.isError, false);
  assert.equal(result.structuredContent.review.task_id, TASK_EXAMPLE.task_id);
  assert.equal(
    result.structuredContent.provenance.provenance_level,
    "complete_v1"
  );
  assert.equal(
    result.structuredContent.provenance.requested_tool,
    TASK_EXAMPLE.requested_tool
  );
  assert.match(
    result.structuredContent.provenance.snapshot_manifest_sha256,
    /^[0-9a-f]{64}$/
  );
  assert.match(
    result.structuredContent.provenance.provenance_schema_sha256,
    /^[0-9a-f]{64}$/
  );
  assert.ok(result.structuredContent.provenance.snapshot_files.length >= 2);
});

test("pre-snapshot validation failures never start Grok", async (t) => {
  const temporary = await fs.mkdtemp(path.join(os.tmpdir(), "nrlis-counter-"));
  const counter = path.join(temporary, "calls.txt");
  const server = await startServer({ FAKE_GROK_COUNTER: counter });
  t.after(async () => {
    await server.close();
    await fs.rm(temporary, { recursive: true, force: true });
  });
  await server.request("initialize");
  const missingRequestedTool = { ...TASK_EXAMPLE };
  delete missingRequestedTool.requested_tool;
  const invalidCalls = [
    {
      name: "grok_methodology_audit",
      arguments: {
        ...TASK_EXAMPLE,
        requested_tool: "grok_project_review"
      }
    },
    {
      name: "grok_methodology_audit",
      arguments: { ...TASK_EXAMPLE, paths: ["../README.md"] }
    },
    {
      name: "grok_methodology_audit",
      arguments: {
        ...TASK_EXAMPLE,
        paths: ["GrossTree/Basic/Profiles/NRLIS-P001/PROFILE.md"]
      }
    },
    {
      name: "grok_methodology_audit",
      arguments: { ...TASK_EXAMPLE, unexpected: true }
    },
    {
      name: "grok_methodology_audit",
      arguments: { ...TASK_EXAMPLE, paths: ["/etc/passwd"] }
    },
    {
      name: "grok_methodology_audit",
      arguments: { ...TASK_EXAMPLE, question: "short" }
    },
    {
      name: "grok_methodology_audit",
      arguments: missingRequestedTool
    },
    {
      name: "grok_compare_hypotheses",
      arguments: {
        ...TASK_EXAMPLE,
        requested_tool: "grok_compare_hypotheses",
        hypotheses: ["Only one hypothesis"]
      }
    }
  ];
  for (const call of invalidCalls) {
    const result = await server.request("tools/call", {
      name: call.name,
      arguments: call.arguments
    });
    assert.equal(result.isError, true);
  }
  await assert.rejects(fs.access(counter));
});

test("review citations outside snapshot fail closed", async (t) => {
  const server = await startServer({ FAKE_GROK_BAD_EVIDENCE: "1" });
  t.after(server.close);
  await server.request("initialize");
  const result = await server.request("tools/call", {
    name: TASK_EXAMPLE.requested_tool,
    arguments: TASK_EXAMPLE
  });
  assert.equal(result.isError, true);
  assert.match(result.content[0].text, /not present in the snapshot/);
});

test("review schema violations fail closed", async (t) => {
  const server = await startServer({ FAKE_GROK_INVALID_STATUS: "1" });
  t.after(server.close);
  await server.request("initialize");
  const result = await server.request("tools/call", {
    name: TASK_EXAMPLE.requested_tool,
    arguments: TASK_EXAMPLE
  });
  assert.equal(result.isError, true);
  assert.match(result.content[0].text, /canonical schema validation/);
});

test("WP1 CLI composes JSON Schema and semantic validation", async (t) => {
  const temporary = await fs.mkdtemp(path.join(os.tmpdir(), "nrlis-wp1-schema-"));
  t.after(() => fs.rm(temporary, { recursive: true, force: true }));
  const invalidRegistryPath = path.join(temporary, "wp1-invalid.json");
  const invalidRegistry = JSON.parse(
    await fs.readFile(WP1_REGISTRY, "utf8")
  );
  invalidRegistry.external_authorities.push({
    authority_id: "AUTH-EXT-MISSING-PROVENANCE"
  });
  await fs.writeFile(
    invalidRegistryPath,
    `${JSON.stringify(invalidRegistry, null, 2)}\n`
  );

  const valid = await runProgram(PYTHON, [WP1_VALIDATOR, "check"]);
  assert.equal(valid.code, 0, valid.stderr);
  assert.match(valid.stdout, /combined JSON Schema \+ semantic gate audit: OK/);

  const invalid = await runProgram(PYTHON, [
    WP1_VALIDATOR,
    "check",
    "--registry",
    invalidRegistryPath
  ]);
  assert.notEqual(invalid.code, 0);
  assert.match(
    `${invalid.stdout}\n${invalid.stderr}`,
    /WP1 JSON Schema validation failed/
  );
});
