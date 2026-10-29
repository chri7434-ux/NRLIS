#!/usr/bin/env python3
"""Require project changes to append the authoritative project change log."""

from __future__ import annotations

import argparse
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = "PROJECT_CHANGE_LOG.md"
EXCLUDED_PARTS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "private",
    "tmp",
}
EXCLUDED_NAMES = {".DS_Store"}


def git_output(arguments: list[str]) -> bytes:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return result.stdout


def names_from(arguments: list[str]) -> set[str]:
    output = git_output(arguments).decode("utf-8")
    return {line for line in output.splitlines() if line}


def is_persistent(relative_text: str) -> bool:
    relative = PurePosixPath(relative_text)
    if relative.name in EXCLUDED_NAMES:
        return False
    if any(part in EXCLUDED_PARTS for part in relative.parts):
        return False
    if relative.suffix in {".pyc", ".pyo"}:
        return False
    return True


def local_changes() -> set[str]:
    return (
        names_from(["diff", "--name-only"])
        | names_from(["diff", "--cached", "--name-only"])
        | names_from(["ls-files", "--others", "--exclude-standard"])
    )


def base_for_environment(explicit: str | None) -> str | None:
    if explicit:
        return explicit
    configured = os.environ.get("NRLIS_DIFF_BASE")
    if configured:
        return configured
    if os.environ.get("GITHUB_EVENT_NAME") == "pull_request":
        branch = os.environ.get("GITHUB_BASE_REF")
        if branch:
            return f"origin/{branch}"
    if os.environ.get("GITHUB_EVENT_NAME") == "push":
        return "HEAD^"
    return None


def previous_log(base: str | None) -> bytes:
    reference = base or "HEAD"
    return git_output(["show", f"{reference}:{LOG_PATH}"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base",
        help="Git base ref for a committed change range; defaults to CI context.",
    )
    args = parser.parse_args()
    base = base_for_environment(args.base)

    if base:
        changed = names_from(
            ["diff", "--name-only", "--diff-filter=ACDMRTUXB", f"{base}...HEAD"]
        )
    else:
        changed = local_changes()

    persistent = {path for path in changed if is_persistent(path)}
    substantive = persistent - {LOG_PATH}
    if substantive and LOG_PATH not in persistent:
        print("Project change-log audit: FAILED")
        print(
            f"  - {len(substantive)} persistent project path(s) changed "
            f"without updating {LOG_PATH}."
        )
        return 1

    if LOG_PATH in persistent:
        prior = previous_log(base)
        current = (ROOT / LOG_PATH).read_bytes()
        if not current.startswith(prior) or len(current) <= len(prior):
            print("Project change-log audit: FAILED")
            print(f"  - {LOG_PATH} must be append-only.")
            return 1

    print(
        "Project change-log audit: OK "
        f"({len(persistent)} persistent changed path(s) checked)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
