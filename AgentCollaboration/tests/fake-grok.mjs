#!/usr/bin/env node

import fs from "node:fs";

const args = process.argv.slice(2);
const promptIndex = args.indexOf("--prompt-file");
const promptPath = promptIndex >= 0 ? args[promptIndex + 1] : "";
const prompt = fs.readFileSync(promptPath, "utf8");
if (process.env.UNRELATED_SECRET_SENTINEL) {
  throw new Error("The bridge leaked an unrelated parent environment value.");
}
const taskId = prompt.match(/^Task ID: (.+)$/m)?.[1] || "UNKNOWN";
const available = [
  ...prompt.matchAll(/^- ([^\n]+)$/gm)
].map((match) => match[1]);
const sourcePath = available.includes("README.md")
  ? "README.md"
  : "AGENTS.md";

if (process.env.FAKE_GROK_COUNTER) {
  fs.appendFileSync(process.env.FAKE_GROK_COUNTER, "called\n");
}

const review = {
  task_id: taskId,
  status:
    process.env.FAKE_GROK_INVALID_STATUS === "1"
      ? "invalid-status"
      : "supported",
  conclusion: "Synthetic bridge test response.",
  evidence: [
    {
      claim: "The supplied snapshot can be cited.",
      support: "The fake reviewer cites an allowlisted file.",
      source_path:
        process.env.FAKE_GROK_BAD_EVIDENCE === "1"
          ? "NOT_IN_SNAPSHOT.md"
          : sourcePath,
      locator: "test fixture",
      evidence_status: "repository_evidence",
      generalization_level: "none"
    }
  ],
  counterarguments: [],
  uncertainties: [],
  recommended_checks: [],
  boundary_flags: [],
  files_examined: [sourcePath]
};

process.stdout.write(`${JSON.stringify(review)}\n`);
