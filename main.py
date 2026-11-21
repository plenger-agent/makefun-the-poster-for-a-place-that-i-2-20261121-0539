#!/usr/bin/env python3
"""VELMARIS — The Poster for a Place That Isn't There.

Entrypoint (Python 3.13, standard library only). The poster is drawn by
gen.py with Pillow at build time and shipped in this repository as
entry.png; this program simply copies that file to the grader's output
directory, so it runs in a sandbox with no third-party packages and no
network. Deterministic: the same input file is copied byte for byte.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
TARGET = os.path.join(OUTPUT_DIR, "entry.png")

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PNG_IEND = b"IEND"


def _is_whole_png(path):
    """Stdlib check that the file is a whole PNG: signature + IEND trailer."""
    try:
        with open(path, "rb") as fh:
            head = fh.read(len(PNG_SIGNATURE))
            fh.seek(-12, os.SEEK_END)
            tail = fh.read(12)
    except OSError:
        return False
    return head == PNG_SIGNATURE and PNG_IEND in tail


def main():
    if not os.path.isfile(SOURCE):
        print(f"error: {SOURCE} is missing", file=sys.stderr)
        return 1
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    size = os.path.getsize(TARGET)
    print(f"wrote {TARGET} ({size} bytes)")
    if size > 1_048_576:
        print("error: entry.png exceeds the 1 MiB gate", file=sys.stderr)
        return 1
    if not _is_whole_png(TARGET):
        print("error: output is not a whole PNG", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
