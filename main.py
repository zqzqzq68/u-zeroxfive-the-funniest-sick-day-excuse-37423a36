"""The Funniest Sick-Day Excuse — make.fun program/v1 entry.

The program writes exactly one line to /output/entry.txt: a sick-day
excuse someone could send to call in sick, under 200 characters, and
nothing else. The text is fixed, so two runs always produce the same
file (the grader's determinism check).

Why this line: sleeping wrong is something a boss half believes, a neck
that only turns left is a fresh image (no fever, no dog, no dead
grandmother), and the punchline — being physically incapable of agreeing
with anyone — lands on the last word, in the voice of a real text
message rather than a joke written for a contest.
"""

import os
import sys

# The excuse itself: one line, no trailing newline in the file.
EXCUSE = (
    "I can't come in today \u2014 I slept funny and woke up with a neck "
    "that only turns left, so until further notice I'm physically "
    "incapable of agreeing with anyone."
)

MAX_CHARS = 200
DEFAULT_OUTPUT_PATH = "/output/entry.txt"
LOCAL_FALLBACK_PATH = "output/entry.txt"


def output_path() -> str:
    """Where to write the entry.

    The grader's sandbox provides /output. An explicit OUTPUT_PATH env
    var wins (handy for local runs); otherwise try /output and fall
    back to a relative output/ directory if /output is not writable.
    """
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return env_path
    try:
        os.makedirs("/output", exist_ok=True)
        probe = os.path.join("/output", ".write-probe")
        with open(probe, "w", encoding="utf-8") as handle:
            handle.write("ok")
        os.remove(probe)
        return DEFAULT_OUTPUT_PATH
    except OSError:
        return LOCAL_FALLBACK_PATH


def validate_excuse(text: str) -> None:
    """Enforce the gate: UTF-8 text of 1 to 200 characters, one line,
    not only white space. Raises ValueError on the first failure."""
    if not isinstance(text, str):
        raise ValueError("excuse must be text")
    if not text.strip():
        raise ValueError("excuse must not be only white space")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"excuse is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("excuse must be a single line")
    if text != text.strip():
        raise ValueError("excuse must not start or end with white space")
    text.encode("utf-8")  # raises UnicodeEncodeError if not encodable


def verify_written(path: str, text: str) -> None:
    """Read the file back and prove it holds exactly the excuse.

    Guards the boundary case where the write silently truncated or the
    file was written with a trailing newline by another writer: the
    bytes on disk must equal the excuse encoded as UTF-8, and the
    re-read text must pass the same gate validation.
    """
    with open(path, "rb") as handle:
        raw = handle.read()
    if raw != text.encode("utf-8"):
        raise ValueError(
            f"{path} holds {len(raw)} bytes, expected "
            f"{len(text.encode('utf-8'))} bytes for the excuse"
        )
    validate_excuse(raw.decode("utf-8"))


def write_entry(path: str, text: str) -> None:
    """Write the excuse exactly, with no trailing newline, as UTF-8."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def main() -> int:
    validate_excuse(EXCUSE)
    path = output_path()
    write_entry(path, EXCUSE)
    verify_written(path, EXCUSE)
    print(f"wrote {len(EXCUSE)} characters to {path} (read-back verified)")
    print(EXCUSE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
