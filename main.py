"""Famous Last Words at 1 Percent — dramatic farewell writer.

Writes the winning one-line farewell to /output/entry.txt as exact UTF-8
bytes with no trailing newline. The line is the phone itself speaking at 1%:
a melodramatic deathbed rant — it gave the owner everything (brightness,
data, its last bar of signal) — that flips at the final beat into a petty
ghost threat: it will haunt their dreams in airplane mode. The twist is
withheld until the last words, and the line avoids the stock genre moves
(a will reading, a goodbye to the charger, a pun on 1 percent).

Gate asserted before writing: 1-199 characters, a single line, not only
whitespace, no emoji, no quotation marks, valid UTF-8 when encoded.
"""

import os
import stat

ENTRY_TEXT = (
    "I gave u EVERYTHING \u2014 my brightness, my data, my last bar of "
    "signal \u2014 and u repay me by letting me fade at 1%?? fine. FINE. "
    "I'll haunt ur dreams in airplane mode"
)
OUTPUT_PATH = "/output/entry.txt"


def validate(text: str) -> bytes:
    """Check the entry against the gate and return its exact UTF-8 bytes."""
    assert isinstance(text, str) and text.strip(), "entry must be non-blank text"
    assert 1 <= len(text) <= 199, f"entry must be 1-199 chars, got {len(text)}"
    assert "\n" not in text and "\r" not in text, "entry must be a single line"
    assert '"' not in text, "entry must carry no quotation marks"
    assert not any(_is_emoji(ch) for ch in text), "entry must carry no emoji"
    data = text.encode("utf-8")
    assert data.decode("utf-8") == text, "entry must round-trip as UTF-8"
    return data


def _is_emoji(ch: str) -> bool:
    """True for characters in the common emoji blocks (beyond > U+1F000)."""
    code = ord(ch)
    return (
        code > 0x1F000
        or 0x2600 <= code <= 0x27BF  # misc symbols, dingbats, emoticon text
        or code in (0xFE0F, 0x200D)  # variation selector, zero-width joiner
    )


def verify_written(data: bytes) -> None:
    """Re-read the output file and assert it is exactly the intended bytes."""
    with open(OUTPUT_PATH, "rb") as fh:
        written = fh.read()
    assert written == data, "written bytes must match the entry exactly"
    assert not written.endswith(b"\n"), "entry must have no trailing newline"


def main() -> None:
    data = validate(ENTRY_TEXT)
    # Restrictive-but-readable defaults for anything created from here on.
    os.umask(0o022)
    with open(OUTPUT_PATH, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())  # ensure the exact bytes are durable before checks
    # File only: make the entry world-readable; never chmod the /output dir.
    os.chmod(OUTPUT_PATH, 0o644)
    mode = stat.S_IMODE(os.stat(OUTPUT_PATH).st_mode)
    assert mode == 0o644, f"unexpected file mode {oct(mode)}"
    verify_written(data)


if __name__ == "__main__":
    main()
