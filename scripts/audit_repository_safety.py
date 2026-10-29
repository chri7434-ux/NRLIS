#!/usr/bin/env python3
"""Fail closed on repository paths and content that must not enter Git.

The audit examines tracked plus unignored files, so it can be run before
staging locally and against the checked-out tree in CI. It intentionally uses
only the Python standard library.
"""

from __future__ import annotations

from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
MAX_FILE_BYTES = 25 * 1024 * 1024
MAX_TEXT_SCAN_BYTES = MAX_FILE_BYTES

FORBIDDEN_PARTS = {
    ".aws",
    ".git",
    ".ssh",
    "__pycache__",
    "private",
    "tmp",
}
FORBIDDEN_NAMES = {
    ".DS_Store",
}
FORBIDDEN_SUFFIXES = {
    ".7z",
    ".aac",
    ".aif",
    ".aiff",
    ".avi",
    ".bdf",
    ".bz2",
    ".ckpt",
    ".db",
    ".edf",
    ".fif",
    ".flac",
    ".gz",
    ".h5",
    ".hdf5",
    ".joblib",
    ".keras",
    ".key",
    ".m4a",
    ".mov",
    ".mp3",
    ".mp4",
    ".mkv",
    ".npy",
    ".npz",
    ".ogg",
    ".onnx",
    ".opus",
    ".p12",
    ".parquet",
    ".pb",
    ".pem",
    ".pfx",
    ".pkl",
    ".pickle",
    ".pt",
    ".pth",
    ".safetensors",
    ".sqlite",
    ".sqlite3",
    ".tar",
    ".wav",
    ".webm",
    ".xz",
    ".zip",
}

SECRET_PATTERNS = {
    "private key": re.compile(
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    ),
    "GitHub token": re.compile(
        r"\b(?:github_pat_[A-Za-z0-9_]{20,}|"
        r"gh[pousr]_[A-Za-z0-9]{20,})\b"
    ),
    "OpenAI key": re.compile(
        r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"
    ),
    "AWS access key": re.compile(
        r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"
    ),
}


def repository_files() -> list[str]:
    result = subprocess.run(
        [
            "git",
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "-z",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return sorted(
        item.decode("utf-8")
        for item in result.stdout.split(b"\0")
        if item
    )


def is_forbidden_env_file(path: PurePosixPath) -> bool:
    name = path.name
    return (
        name == ".env"
        or (name.startswith(".env.") and name != ".env.example")
    )


def scan_text(path: Path) -> list[str]:
    if path.stat().st_size > MAX_TEXT_SCAN_BYTES:
        return []
    data = path.read_bytes()
    # Secret formats are ASCII-compatible. Ignoring invalid UTF-8 lets the
    # scanner detect embedded tokens even in binary or mixed-encoding files.
    text = data.decode("utf-8", errors="ignore")
    return [
        label
        for label, pattern in SECRET_PATTERNS.items()
        if pattern.search(text)
    ]


def main() -> int:
    problems: list[str] = []
    files = repository_files()

    for relative_text in files:
        relative = PurePosixPath(relative_text)
        path = ROOT / relative_text

        if path.is_symlink():
            problems.append(f"symlink is not allowed: {relative_text}")
            continue
        # `git ls-files --cached` includes tracked paths that have been deleted
        # or moved but not staged yet. There is no working-tree content to scan;
        # index/file-manifest checks are responsible for detecting stale paths.
        if not path.exists():
            continue
        if any(part in FORBIDDEN_PARTS for part in relative.parts):
            problems.append(f"forbidden path component: {relative_text}")
        if relative.name in FORBIDDEN_NAMES:
            problems.append(f"forbidden generated file: {relative_text}")
        if is_forbidden_env_file(relative):
            problems.append(f"environment secret file is not allowed: {relative_text}")
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            problems.append(f"forbidden sensitive file type: {relative_text}")

        size = path.stat().st_size
        if size > MAX_FILE_BYTES:
            problems.append(
                f"file exceeds {MAX_FILE_BYTES} bytes: "
                f"{relative_text} ({size} bytes)"
            )

        for label in scan_text(path):
            problems.append(f"possible {label}: {relative_text}")

    if problems:
        print("Repository safety audit: FAILED")
        for problem in problems:
            print(f"  - {problem}")
        return 1

    print(
        "Repository safety audit: OK "
        f"({len(files)} tracked or unignored files checked)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
