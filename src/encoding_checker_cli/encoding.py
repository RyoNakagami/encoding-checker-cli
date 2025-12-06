from pathlib import Path
import chardet
import sys

JAPANESE_ENCODINGS = ["shift_jis", "cp932", "euc-jp"]


def looks_like_text(s: str) -> bool:
    printable = sum(c.isprintable() for c in s)
    return printable / max(len(s), 1) > 0.5


def is_valid_utf16(data: bytes, endian: str) -> bool:
    if len(data) < 4:  # too short to be real text
        return False
    if len(data) % 2 != 0:
        return False

    try:
        decoded = data.decode(endian)
    except UnicodeDecodeError:
        return False

    if "\ufffd" in decoded:
        return False

    if not looks_like_text(decoded):
        return False

    return True


def detect_file_encoding(file_path: Path) -> str | None:
    """
    Detect the text encoding of a file, prioritizing UTF-8 and ignoring emoji issues.

    Args:
        file_path (Path): Path to the file.

    Returns:
        str | None: Detected encoding, or None if detection fails.
    """
    try:
        raw_bytes = file_path.read_bytes()
    except Exception as e:  # catch OSError, IOError, etc.
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    # 1. BOM detection for UTF-16
    if raw_bytes.startswith(b"\xff\xfe") and is_valid_utf16(raw_bytes, "utf-16-le"):
        return "utf-16-le"

    if raw_bytes.startswith(b"\xfe\xff") and is_valid_utf16(raw_bytes, "utf-16-be"):
        return "utf-16-be"

    # 1. Try UTF-8 directly (handles emojis correctly)
    try:
        raw_bytes.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        pass

    # 2. Use chardet as fallback
    detector = chardet.universaldetector.UniversalDetector()
    for chunk_start in range(0, len(raw_bytes), 1024):
        chunk = raw_bytes[chunk_start : chunk_start + 1024]
        detector.feed(chunk)
        if detector.done:
            break
    detector.close()

    encoding = detector.result.get("encoding")
    if not encoding:
        return None

    encoding = encoding.lower()
    if encoding == "ascii":
        encoding = "utf-8"

    # 3. If chardet reports Windows-125x, try Japanese encodings
    if encoding.startswith("windows-125"):
        for enc in JAPANESE_ENCODINGS:
            try:
                raw_bytes.decode(enc)
                return enc
            except UnicodeDecodeError:
                continue

    # 4. Special handling for UTF-16
    if encoding in ("utf-16", "utf-16-le", "utf-16-be"):
        # Determine endianness based on BOM if present
        if encoding == "utf-16" and raw_bytes.startswith(b"\xff\xfe"):
            endian = "utf-16-le"
        elif encoding == "utf-16" and raw_bytes.startswith(b"\xfe\xff"):
            endian = "utf-16-be"
        else:
            endian = encoding

        # Use your UTF-16 checker to re-validate
        if not is_valid_utf16(raw_bytes, endian):
            return None

        # If OK, confirm
        return endian


    return encoding
