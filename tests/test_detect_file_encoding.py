import pytest
from pathlib import Path
from encoding_checker_cli.encoding import detect_file_encoding, JAPANESE_ENCODINGS

def test_utf8(tmp_path):
    """Detect UTF-8 files correctly, including emoji."""
    file = tmp_path / "utf8.txt"
    file.write_text("Hello 🌏", encoding="utf-8")

    result = detect_file_encoding(file)
    assert result == "utf-8"

def test_ascii(tmp_path):
    """Detect ASCII as UTF-8."""
    file = tmp_path / "ascii.txt"
    file.write_text("Hello World", encoding="ascii")

    result = detect_file_encoding(file)
    assert result == "utf-8"

def test_shift_jis(tmp_path):
    """Detect Shift_JIS correctly."""
    file = tmp_path / "sjis.txt"
    file.write_bytes("テストテスト".encode("shift_jis"))

    result = detect_file_encoding(file)
    assert result in JAPANESE_ENCODINGS

def test_utf16_le(tmp_path):
    """Detect UTF-16 LE via BOM."""
    file = tmp_path / "utf16le.txt"
    file.write_bytes(b"\xff\xfeH\x00i\x00")

    result = detect_file_encoding(file)
    assert result == "utf-16-le"

def test_utf16_be(tmp_path):
    """Detect UTF-16 BE via BOM."""
    file = tmp_path / "utf16be.txt"
    file.write_bytes(b"\xfe\xff\x00H\x00i")

    result = detect_file_encoding(file)
    assert result == "utf-16-be"

def test_unknown_encoding(tmp_path):
    """Return None if no encoding can decode the file."""
    file = tmp_path / "bad.bin"
    file.write_bytes(b"\xff\xfe\xfa\xfb")

    result = detect_file_encoding(file)
    assert result is None

def test_file_io_error(monkeypatch, tmp_path):
    """Raise SystemExit if the file cannot be read."""
    file = tmp_path / "nope.txt"

    # Patch Path.read_bytes at the class level to raise an OSError
    original_read_bytes = Path.read_bytes

    def fake_read_bytes(self):
        raise OSError("boom")

    monkeypatch.setattr(Path, "read_bytes", fake_read_bytes)

    with pytest.raises(SystemExit):
        detect_file_encoding(file)

    # Restore original read_bytes method if needed
    monkeypatch.setattr(Path, "read_bytes", original_read_bytes)
