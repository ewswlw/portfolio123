from __future__ import annotations

import argparse
import sys
from pathlib import Path


BAD_CODEPOINTS = {
    "\ufffd": "replacement character U+FFFD",
    "\ufeff": "byte-order mark U+FEFF inside text",
}

C1_CONTROL_RANGE = range(0x80, 0xA0)

MOJIBAKE_MARKERS = [
    "â€™",
    "â€œ",
    "â€\u009d",
    "â€“",
    "â€”",
    "Â ",
    "ï»¿",
    "Ã—",
    "Ã©",
]


def iter_markdown_files(root: Path) -> list[Path]:
    skipped = {".git", ".venv", "__pycache__"}
    files: list[Path] = []
    for path in root.rglob("*.md"):
        if any(part in skipped for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def scan_file(path: Path) -> list[str]:
    issues: list[str] = []
    try:
        raw = path.read_bytes()
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return [f"invalid UTF-8 byte sequence at byte {exc.start}"]

    for char, label in BAD_CODEPOINTS.items():
        if char in text:
            issues.append(label)

    for index, char in enumerate(text):
        codepoint = ord(char)
        if codepoint in C1_CONTROL_RANGE:
            issues.append(f"C1 control U+{codepoint:04X} at character {index}")

    for marker in MOJIBAKE_MARKERS:
        if marker in text:
            issues.append(f"possible mojibake marker {marker!r}")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan Markdown files for bad Unicode and mojibake.")
    parser.add_argument("root", nargs="?", default=".", help="Root directory to scan")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    failures: list[tuple[Path, list[str]]] = []
    for path in iter_markdown_files(root):
        issues = scan_file(path)
        if issues:
            failures.append((path, issues))

    if failures:
        for path, issues in failures:
            rel = path.relative_to(root).as_posix()
            for issue in issues:
                print(f"{rel}: {issue}", file=sys.stderr)
        return 1

    print(f"Scanned {len(iter_markdown_files(root))} Markdown files; no bad Unicode found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
