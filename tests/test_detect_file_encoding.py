import pytest
from pathlib import Path
from encoding_checker_cli import encoding as encoding_module
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


class FakeDetector:
    """Minimal stand-in for chardet.UniversalDetector."""

    instances = []

    def __init__(self, encoding="shift_jis", done_after=None):
        self.result = {"encoding": encoding}
        self.done = False
        self.closed = False
        self.chunks = []
        self._done_after = done_after
        FakeDetector.instances.append(self)

    def feed(self, chunk):
        self.chunks.append(chunk)
        if self._done_after is not None and len(self.chunks) >= self._done_after:
            self.done = True

    def close(self):
        self.closed = True


@pytest.fixture
def fake_detector(monkeypatch):
    """Replace chardet.UniversalDetector with a configurable fake."""
    FakeDetector.instances = []

    def install(**kwargs):
        monkeypatch.setattr(
            encoding_module.chardet, "UniversalDetector", lambda: FakeDetector(**kwargs)
        )
        return FakeDetector.instances

    return install


def test_fallback_uses_top_level_universal_detector(tmp_path, fake_detector):
    """The chardet fallback is driven by chardet.UniversalDetector."""
    instances = fake_detector(encoding="SHIFT_JIS")
    file = tmp_path / "sjis.txt"
    file.write_bytes("テストテスト".encode("shift_jis"))

    result = detect_file_encoding(file)

    assert result == "shift_jis"
    assert len(instances) == 1
    assert instances[0].closed


def test_fallback_without_universaldetector_submodule(tmp_path, monkeypatch):
    """Detection works even if chardet does not expose the universaldetector submodule."""
    monkeypatch.delattr(encoding_module.chardet, "universaldetector", raising=False)
    file = tmp_path / "sjis.txt"
    file.write_bytes("テストテスト".encode("shift_jis"))

    result = detect_file_encoding(file)

    assert result in JAPANESE_ENCODINGS


def test_fallback_feeds_in_1024_byte_chunks(tmp_path, fake_detector):
    """Bytes are fed to the detector in 1024-byte chunks until EOF."""
    instances = fake_detector()
    raw = b"\x82" * 2500  # invalid UTF-8, forces the chardet fallback
    file = tmp_path / "big.bin"
    file.write_bytes(raw)

    detect_file_encoding(file)

    chunks = instances[0].chunks
    assert [len(c) for c in chunks] == [1024, 1024, 452]
    assert b"".join(chunks) == raw


def test_fallback_stops_feeding_when_detector_done(tmp_path, fake_detector):
    """Feeding stops as soon as the detector reports it is done."""
    instances = fake_detector(done_after=1)
    file = tmp_path / "big.bin"
    file.write_bytes(b"\x82" * 2500)

    detect_file_encoding(file)

    assert len(instances[0].chunks) == 1
    assert instances[0].closed


def test_fallback_returns_none_when_detector_has_no_result(tmp_path, fake_detector):
    """Return None if the detector cannot determine an encoding."""
    fake_detector(encoding=None)
    file = tmp_path / "bad.bin"
    file.write_bytes(b"\x82\xff\x00\x81")

    assert detect_file_encoding(file) is None
