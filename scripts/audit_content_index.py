#!/usr/bin/env python3
"""Audit the project-root Content of Work file manifest.

The script is read-only. It reports persistent workspace files that are missing
from CONTENT_OF_WORK.md and indexed paths that no longer exist.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
INDEX_FILE = ROOT / "CONTENT_OF_WORK.md"
START = "<!-- INDEXED_FILES_START -->"
END = "<!-- INDEXED_FILES_END -->"

EXCLUDED_DIR_NAMES = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "tmp",
}
EXCLUDED_FILE_NAMES = {
    ".DS_Store",
}


def is_excluded(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    if path.name in EXCLUDED_FILE_NAMES:
        return True
    if any(part in EXCLUDED_DIR_NAMES for part in relative.parts):
        return True
    if "private" in relative.parts:
        return True
    if path.suffix in {".pyc", ".pyo"}:
        return True
    return False


def actual_files() -> set[str]:
    return {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and not is_excluded(path)
    }


def indexed_files() -> set[str]:
    text = INDEX_FILE.read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise RuntimeError("Indexed-file manifest markers are missing.")
    block = text.split(START, 1)[1].split(END, 1)[0]
    return set(re.findall(r"^- `([^`]+)`$", block, flags=re.MULTILINE))


def main() -> int:
    actual = actual_files()
    indexed = indexed_files()
    missing = sorted(actual - indexed)
    stale = sorted(indexed - actual)

    if not missing and not stale:
        print(
            f"Content index audit: OK "
            f"({len(actual)} persistent files indexed)."
        )
        return 0

    if missing:
        print("Missing from CONTENT_OF_WORK.md manifest:")
        for path in missing:
            print(f"  + {path}")
    if stale:
        print("Indexed paths that do not exist:")
        for path in stale:
            print(f"  - {path}")
    print(
        "Update CONTENT_OF_WORK.md and PROJECT_CHANGE_LOG.md "
        "before completing the task."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
