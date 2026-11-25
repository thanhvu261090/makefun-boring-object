#!/usr/bin/env python3
"""One-line review of the most boring object: the doorstop.

make.fun bounty entry — "The Most Boring Object, Reviewed in One Line".
The program prints the review, validates it against the bounty gates
(1-200 characters, exactly one line, no surrounding whitespace), and
writes the exact same bytes to the output file so the judged file and
the printed line can never drift apart.

Run it:
    python3 main.py                 # print the review, write the file
    python3 main.py --self-test     # run the gate checks, print PASS/FAIL

Output file: /output/entry.txt by default, or $ENTRY_OUTPUT when set.
Standard library only; the output is deterministic on every run.
"""

import os
import sys
import tempfile

ENTRY = "The doorstop: six years holding this door open, zero thank-yous, and the door still gets all the credit for being so welcoming."

MAX_CHARS = 200
MIN_CHARS = 1
DEFAULT_OUTPUT = "/output/entry.txt"


def entry_chars(text):
    """How many characters the entry has (Python string length)."""
    return len(text)


def is_single_line(text):
    """True when the text contains no line break of either kind."""
    return "\n" not in text and "\r" not in text


def has_clean_edges(text):
    """True when the text is not blank and has no leading/trailing space."""
    return bool(text.strip()) and text == text.strip()


def validate_entry(text):
    """Raise ValueError unless the text passes every bounty gate.

    Gates, in order: it must be a string, 1-200 characters long, a
    single line, and free of leading/trailing whitespace. The checks
    are deliberately separate so a failure message names the rule
    that was broken instead of just saying "invalid".
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string, got %s" % type(text).__name__)
    if not MIN_CHARS <= entry_chars(text) <= MAX_CHARS:
        raise ValueError(
            "entry is %d chars, must be %d-%d" % (entry_chars(text), MIN_CHARS, MAX_CHARS)
        )
    if not is_single_line(text):
        raise ValueError("entry must be a single line (no newline or carriage return)")
    if not has_clean_edges(text):
        raise ValueError("entry must not be blank or padded with whitespace")
    text.encode("utf-8")
    return True


def output_path():
    """Where the entry file goes: $ENTRY_OUTPUT, else the default."""
    return os.environ.get("ENTRY_OUTPUT", DEFAULT_OUTPUT)


def write_entry(text, path):
    """Write the entry with no trailing newline, creating folders as needed.

    Writing without a newline matters: the judged file must hold exactly
    the entry bytes, nothing extra, so a trailing newline would change it.
    """
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def read_entry_bytes(path):
    """Read a file back as raw bytes, for byte-identity comparisons."""
    with open(path, "rb") as handle:
        return handle.read()


def check_repeat_writes(text):
    """Write the entry twice to temp files; both must match byte for byte."""
    with tempfile.TemporaryDirectory() as tmp:
        first_path = os.path.join(tmp, "first.txt")
        second_path = os.path.join(tmp, "second.txt")
        write_entry(text, first_path)
        write_entry(text, second_path)
        first = read_entry_bytes(first_path)
        second = read_entry_bytes(second_path)
        if first != second:
            return "repeat writes differ"
        if first != text.encode("utf-8"):
            return "written bytes do not match the entry"
    return None


def check_rejections():
    """Return a list of gate cases validate_entry wrongly accepted.

    Each case is a (label, value) pair that must be rejected. A case
    only appears in the result when the validator lets it through.
    """
    bad_cases = [
        ("201-char string", "x" * 201),
        ("multi-line string", "first line\nsecond line"),
        ("carriage-return string", "first line\rsecond line"),
        ("leading whitespace", "  padded"),
        ("trailing whitespace", "padded  "),
        ("empty string", ""),
        ("whitespace-only string", "   "),
        ("non-string value", 12345),
        ("None value", None),
        ("bytes value", b"not a string"),
    ]
    problems = []
    for label, value in bad_cases:
        try:
            validate_entry(value)
        except ValueError:
            continue
        problems.append("%s: validate_entry accepted it" % label)
    return problems


def describe_entry(text):
    """One-line summary of an entry: length, lines, and edge state.

    Handy when debugging a rejected entry without printing the entry
    itself: it reports the shape (how long, single line or not, clean
    edges or not) rather than the content.
    """
    return (
        "chars=%d single_line=%s clean_edges=%s"
        % (entry_chars(text) if isinstance(text, str) else -1,
           is_single_line(text) if isinstance(text, str) else False,
           has_clean_edges(text) if isinstance(text, str) else False)
    )


def check_acceptances():
    """Return a list of gate cases validate_entry wrongly rejected."""
    good_cases = [
        ("entry", ENTRY),
        ("200-char string", "x" * 200),
        ("1-char string", "x"),
        ("199-char string", "y" * 199),
    ]
    problems = []
    for label, value in good_cases:
        try:
            validate_entry(value)
        except ValueError as exc:
            problems.append("%s: validate_entry rejected it (%s)" % (label, exc))
    return problems


def run_self_test():
    """Run every gate check and report PASS or FAIL.

    Covers the exact entry text and length, repeat-write byte
    identity, the 1/200-char boundaries, and all rejection cases.
    Returns 0 when everything passes, 1 otherwise.
    """
    failures = []

    expected = "The doorstop: six years holding this door open, zero thank-yous, and the door still gets all the credit for being so welcoming."
    if ENTRY != expected:
        failures.append("ENTRY does not match the expected 127-char line")
    if entry_chars(ENTRY) != 127:
        failures.append("ENTRY is %d chars, expected 127" % entry_chars(ENTRY))
    if not is_single_line(ENTRY):
        failures.append("ENTRY is not a single line")
    if not has_clean_edges(ENTRY):
        failures.append("ENTRY has blank or padded edges")

    repeat_problem = check_repeat_writes(ENTRY)
    if repeat_problem is not None:
        failures.append(repeat_problem)

    failures.extend(check_rejections())
    failures.extend(check_acceptances())

    # The summary helper must agree with the entry's known shape.
    if describe_entry(ENTRY) != "chars=127 single_line=True clean_edges=True":
        failures.append("describe_entry disagrees: %s" % describe_entry(ENTRY))
    if describe_entry("") != "chars=0 single_line=True clean_edges=False":
        failures.append("describe_entry mishandles the empty string")

    if failures:
        for failure in failures:
            print("SELF-TEST FAIL: %s" % failure, file=sys.stderr)
        return 1
    print("SELF-TEST PASS: entry 127 chars, gate rules verified")
    return 0


def main():
    validate_entry(ENTRY)
    write_entry(ENTRY, output_path())
    print(ENTRY)
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(run_self_test())
    sys.exit(main())
