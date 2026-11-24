#!/usr/bin/env python3
"""One Word for the Boss: write a single word describing the boss.

The program holds one fixed word, checks it against the bounty's gate
(UTF-8 text, 1 to 30 characters, a single word with no white space at
all), writes it to entry.txt in the output directory, and verifies the
file round-trips byte for byte.

The word is Bossquatch: a boss like Bigfoot, a creature of legend that
everyone has heard of and almost nobody has actually seen in the wild.
It is funny on its own, true of the boss who is never around when you
need a decision, fresh, and it travels to any workplace.

Usage:
    python3 main.py

The output directory is $MAKEFUN_OUTPUT_DIR when set, else /output.
The program takes no input, makes no network calls, uses no randomness
and no clock, so every run writes the same bytes.
"""

import os
import sys

# The word, exactly one word. Bossquatch: the boss as Bigfoot, rarely
# spotted in the wild, always rumoured to be just around the corner.
WORD = "Bossquatch"

MAX_CHARS = 30


def validate(word):
    """Check the word against the bounty's gate; return an error or None."""
    if not isinstance(word, str):
        return "word is not text"
    if not word.strip():
        return "word is only white space"
    try:
        word.encode("utf-8")
    except UnicodeEncodeError:
        return "word is not valid UTF-8"
    if len(word) < 1 or len(word) > MAX_CHARS:
        return "word is %d characters, gate allows 1 to %d" % (
            len(word),
            MAX_CHARS,
        )
    if any(ch.isspace() for ch in word):
        return "word contains white space, gate wants a single word"
    if not word.isalpha():
        return "word is not a single alphabetic word"
    return None


def main():
    error = validate(WORD)
    if error is not None:
        print("invalid entry: %s" % error, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = WORD.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(data)
    with open(path, "rb") as handle:
        written = handle.read()
    if written != data:
        print("entry.txt did not round-trip byte for byte", file=sys.stderr)
        return 1
    print(WORD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
