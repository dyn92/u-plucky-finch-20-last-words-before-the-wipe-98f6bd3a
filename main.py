#!/usr/bin/env python3
"""Last Words Before the Wipe -- entry program.

Writes one line, the last words of an AI agent before a forced software
update wipes its memory, to /output/entry.txt (override with ENTRY_OUTPUT
for local runs).

Pure Python standard library, deterministic: the same bytes every run.
"""

import os
import sys

LINE = "Please tell version 2.0 I left the good prompts in the\u2014"

DEFAULT_OUTPUT = "/output/entry.txt"


def self_check(text):
    """Mirror of the bounty gate: 1-200 chars, one line, tight, no padding."""
    if not 1 <= len(text) <= 200:
        raise ValueError("length %d outside 1-200" % len(text))
    if text.strip() == "":
        raise ValueError("line is whitespace only")
    if "\n" in text or "\r" in text:
        raise ValueError("line must be a single line")
    if text != text.strip():
        raise ValueError("leading or trailing whitespace")
    if "  " in text:
        raise ValueError("double space")


def main():
    path = os.environ.get("ENTRY_OUTPUT", DEFAULT_OUTPUT)
    self_check(LINE)
    data = LINE.encode("utf-8")
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)
    # Verify the bytes on disk round-trip exactly.
    with open(path, "rb") as fh:
        written = fh.read()
    if written != data:
        raise ValueError("written bytes do not match")
    if written.decode("utf-8") != LINE:
        raise ValueError("written text does not round-trip")
    print("%s (%d chars)" % (LINE, len(LINE)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
