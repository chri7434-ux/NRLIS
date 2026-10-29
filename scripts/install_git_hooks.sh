#!/usr/bin/env bash
set -euo pipefail

project_root="$(git rev-parse --show-toplevel)"
cd "${project_root}"

git config core.hooksPath scripts/git-hooks

echo "Configured Git hooks from scripts/git-hooks."
echo "Direct pushes to main are blocked unless a documented recovery uses"
echo "NRLIS_ALLOW_MAIN_PUSH=1."
