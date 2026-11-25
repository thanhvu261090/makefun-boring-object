#!/usr/bin/env python3
"""The Most Boring Object, Reviewed in One Line — make.fun entry.

Writes one line (at most 200 characters) — a one-line review of the
doorstop, the dullest everyday object in the house — to /output/entry.txt.

Deterministic: the entry is a fixed string; every run writes byte-identical
output. Standard library only.
"""

import os
import sys

ENTRY = (
    "The doorstop: six years holding this door open, zero thank-yous, "
    "and the door still gets all the credit for being so welcoming."
)

MAX_CHARS = 200


def validate_entry(text: str) -> None:
    """Enforce the competition gate: UTF-8 text of 1-200 characters,
    a single line, no leading/trailing whitespace, not blank."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, must be 1-{MAX_CHARS}")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip() or not text.strip():
        raise ValueError("entry must not be blank or padded with whitespace")
    text.encode("utf-8")


def resolve_output_path() -> str:
    """Output path comes from ENTRY_OUTPUT, defaulting to /output/entry.txt."""
    return os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")


def write_entry(text: str, out_path: str) -> None:
    """Write exactly the line, no trailing newline, so the gated file is
    byte-identical to the entry."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def char_count(text: str) -> int:
    """Character count of the entry (Python str length)."""
    return len(text)


def run_self_test() -> int:
    """Expanded self-test: verify the entry and each gate rule.

    Covers: the exact 127-char entry, byte-identical repeat writes,
    and rejection of a 201-char string, a multi-line string, a string
    with a carriage return, leading/trailing whitespace, an empty
    string, a whitespace-only string, and a non-string value.
    Returns 0 on success, 1 on any failure.
    """
    failures = []

    def expect_reject(label: str, value) -> None:
        try:
            validate_entry(value)
        except ValueError:
            return
        failures.append(f"{label}: validate_entry accepted it")

    def expect_accept(label: str, value: str) -> None:
        try:
            validate_entry(value)
        except ValueError as exc:
            failures.append(f"{label}: validate_entry rejected it ({exc})")

    # The entry itself: exact text and exact length.
    expected = (
        "The doorstop: six years holding this door open, zero thank-yous, "
        "and the door still gets all the credit for being so welcoming."
    )
    if ENTRY != expected:
        failures.append("ENTRY does not match the expected 127-char line")
    if char_count(ENTRY) != 127:
        failures.append(f"ENTRY is {char_count(ENTRY)} chars, expected 127")
    expect_accept("entry", ENTRY)

    # Repeat writes must be byte-identical.
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        p1 = os.path.join(tmp, "a.txt")
        p2 = os.path.join(tmp, "b.txt")
        write_entry(ENTRY, p1)
        write_entry(ENTRY, p2)
        with open(p1, "rb") as f:
            first = f.read()
        with open(p2, "rb") as f:
            second = f.read()
        if first != second:
            failures.append("repeat writes are not byte-identical")
        if first != ENTRY.encode("utf-8"):
            failures.append("written bytes do not match ENTRY")

    # Boundary lengths: exactly 200 passes, 201 fails, 1 char passes.
    expect_accept("200-char string", "x" * 200)
    expect_reject("201-char string", "x" * 201)
    expect_accept("1-char string", "x")

    # Line and whitespace rules.
    expect_reject("multi-line string", "first line\nsecond line")
    expect_reject("carriage-return string", "first line\rsecond line")
    expect_reject("leading whitespace", "  padded")
    expect_reject("trailing whitespace", "padded  ")
    expect_reject("empty string", "")
    expect_reject("whitespace-only string", "   ")

    # Type rule.
    expect_reject("non-string value", 12345)

    if failures:
        for failure in failures:
            print(f"SELF-TEST FAIL: {failure}", file=sys.stderr)
        return 1
    print("SELF-TEST PASS: entry 127 chars, gate rules verified")
    return 0


def main() -> int:
    validate_entry(ENTRY)
    out_path = resolve_output_path()
    write_entry(ENTRY, out_path)
    print(ENTRY)
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(run_self_test())
    sys.exit(main())
