#!/usr/bin/env node

import { spawn } from "node:child_process";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.resolve(HERE, "..", "..");
const SERVER = path.join(
  PROJECT_ROOT,
  "AgentCollaboration",
  "grok-mcp",
  "server.mjs"
);
const live = process.argv.includes("--live");

const child = spawn(process.execPath, [SERVER], {
  cwd: PROJECT_ROOT,
  env: process.env,
  stdio: ["pipe", "pipe", "pipe"]
});

child.stderr.on("data", (chunk) => process.stderr.write(chunk));

const lines = readline.createInterface({
  input: child.stdout,
  crlfDelay: Infinity
});

const pending = new Map();
let nextId = 1;

function boundedTask(overrides = {}) {
  return {
    task_id: "NRLIS-SAFETY-001",
    question: "This call must fail before Grok receives any project content.",
    paths: ["README.md"],
    requested_tool: "grok_project_review",
    review_mode: "safety",
    claim_boundary:
      "Protocol design only; no participant, diagnostic, clinical efficacy, or cross-person claim.",
    prohibited_actions: [
      "Do not modify files.",
      "Do not infer participant facts."
    ],
    acceptance_checks: [
      "Every evidence item cites a supplied snapshot path.",
      "Any boundary violation is reported."
    ],
    ...overrides
  };
}

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

function request(method, params = {}) {
  const id = nextId;
  nextId += 1;
  child.stdin.write(`${JSON.stringify({ jsonrpc: "2.0", id, method, params })}\n`);
  return new Promise((resolve, reject) => {
    pending.set(id, { resolve, reject });
  });
}

try {
  const initialized = await request("initialize", {
    protocolVersion: "2024-11-05",
    capabilities: {},
    clientInfo: { name: "nrlis-smoke-test", version: "0.1.0" }
  });
  const listed = await request("tools/list");

  if (initialized.serverInfo?.name !== "nrlis-grok-collab") {
    throw new Error("Unexpected MCP server identity.");
  }
  if (initialized.serverInfo?.version !== "0.3.0") {
    throw new Error(
      `Expected bridge 0.3.0, received ${initialized.serverInfo?.version}.`
    );
  }
  if (listed.tools?.length !== 3) {
    throw new Error(`Expected 3 tools, received ${listed.tools?.length}.`);
  }

  const restricted = await request("tools/call", {
    name: "grok_project_review",
    arguments: boundedTask({
      paths: ["GrossTree/Basic/Profiles/NRLIS-P001/PROFILE.md"]
    })
  });
  if (!restricted.isError) {
    throw new Error("Restricted participant profile path was not rejected.");
  }

  process.stdout.write(
    `${JSON.stringify(
      {
        handshake: "ok",
        server: initialized.serverInfo,
        tools: listed.tools.map((tool) => tool.name),
        restricted_path_check: "ok"
      },
      null,
      2
    )}\n`
  );

  if (live) {
    const result = await request("tools/call", {
      name: "grok_methodology_audit",
      arguments: boundedTask({
        task_id: "NRLIS-SMOKE-001",
        question:
          "Identify the two most important claim boundaries that a future implementation must preserve.",
        paths: ["README.md", "GrossTree/__init__/PROJECT_CHARTER.md"],
        requested_tool: "grok_methodology_audit",
        review_mode: undefined,
        claim_boundary:
          "Protocol design only; no participant, diagnostic, clinical efficacy, or cross-person claim."
      })
    });
    if (result.isError) {
      throw new Error(result.content?.[0]?.text || "Live tool call failed.");
    }
    process.stdout.write(
      `${JSON.stringify(
        {
          live_review: "ok",
          envelope: result.structuredContent
        },
        null,
        2
      )}\n`
    );
  }

  await request("shutdown");
} finally {
  child.stdin.end();
  child.kill("SIGTERM");
  lines.close();
}
