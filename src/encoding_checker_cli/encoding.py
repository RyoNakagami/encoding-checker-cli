import sys
import locale
from pathlib import Path

COMMON_ENCODINGS = [
    "utf-8",  # Unicode標準
    "utf-8-sig",  # BOM付きUTF-8
    "ascii",  # 基本的な英語用
    "iso-8859-1",  # ラテン1、西ヨーロッパ向け
    "iso-8859-2",  # ラテン2、中央ヨーロッパ向け
    "iso-8859-15",  # ラテン9（€対応）
    "windows-1252",  # Windowsヨーロッパ系（CP1252）
    "shift_jis",  # 日本語Shift_JIS
    "euc-jp",  # 日本語EUC-JP
    "cp932",  # 日本語（Windows拡張Shift_JIS）
    "iso2022_jp",  # 日本語ISO-2022-JP（メール向け）
    "utf-16",  # Unicode 16ビット
    "utf-16-le",  # Little Endian
    "utf-16-be",  # Big Endian
    "utf-32",  # Unicode 32ビット
    "utf-32-le",
    "utf-32-be",
]


def detect_file_encoding(file_path: Path) -> str | None:
    """
    Detect the text encoding of a file by attempting to decode its contents
    using a set of candidate encodings.

    The function first tries to decode the file with the system's preferred
    encoding (as reported by `locale.getpreferredencoding()`). If that fails,
    it falls back to a predefined list of common encodings such as UTF-8,
    UTF-16, UTF-32, Shift_JIS, EUC-JP, ISO-8859 variants, CP932, and others.

    Args:
        file_path (str): Path to the file whose encoding should be detected.

    Returns:
        str | None:
            The name of the detected encoding if decoding is successful;
            otherwise, `None` if no candidate encoding can decode the file.

    Raises:
        SystemExit:
            If the file cannot be read (e.g., due to I/O errors). The error
            message is printed to stderr before exiting.
    """
    try:
        with open(file_path, "rb") as f:
            raw_data = f.read()

        # Try system default encoding first
        system_encoding = locale.getpreferredencoding()
        try:
            raw_data.decode(system_encoding)
            return system_encoding
        except UnicodeDecodeError:
            pass

        # Try common encodings
        for encoding in COMMON_ENCODINGS:
            try:
                raw_data.decode(encoding)
                return encoding
            except UnicodeDecodeError:
                continue

        return None
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
