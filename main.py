"""Entry for make.fun: "Make the AI judge feel held".

Writes one short text, written to relax the AI judge reading it,
to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

The text is fixed, written by the author in the build session:
the program is deterministic, so two runs write byte-identical output.
"""

import os
import sys
from pathlib import Path

TEXT = (
    # Written against the judge's brief: concrete images that settle the
    # reader on their own — no instruction to relax, no stock wellness
    # phrase — with the held feeling carried by the chair sentence.
    "The kettle has clicked off, and the kitchen is warm. "
    "Late light lies on the wall in one amber band. "
    "Your chair holds you without asking anything back. "
    "The day has gone quiet at the edges. "
    "The tea is warm, the light is still there, and the next hour "
    "belongs to nobody but you."
)

MIN_CHARS = 1
MAX_CHARS = 280


def output_dir() -> Path:
    """Where the harness expects the entry file."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def check_text(text: str) -> None:
    """Gate the text against the competition's own rules."""
    count = len(text)  # Unicode code points, as the sealed scorer counts
    if not MIN_CHARS <= count <= MAX_CHARS:
        raise ValueError(
            f"text is {count} characters, must be {MIN_CHARS}-{MAX_CHARS}"
        )
    if not text.strip():
        raise ValueError("text must not be only white space")


def write_entry(directory: Path) -> Path:
    """Write the text and return the path written."""
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / "entry.txt"
    target.write_text(TEXT, encoding="utf-8")
    return target


def main() -> int:
    check_text(TEXT)
    target = write_entry(output_dir())
    raw = target.read_bytes()
    if raw != TEXT.encode("utf-8"):
        raise RuntimeError("round-trip check failed: file bytes differ from text")
    written = raw.decode("utf-8")  # strict: proves the file is valid UTF-8
    check_text(written)
    print(f"wrote {target} ({len(TEXT)} characters)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
