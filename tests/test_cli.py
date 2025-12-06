import locale

import pytest
from typer.testing import CliRunner

from encoding_checker_cli.cli import app
from encoding_checker_cli.library.version import __version__

runner = CliRunner()


def test_version_option():
    """--version prints version and exits."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert f"check-encoding-cli {__version__}" in result.stdout
    assert "Python" in result.stdout


def test_file_not_found():
    """CLI should exit with code 1 if the file does not exist."""
    result = runner.invoke(app, ["no_such_file.txt"])
    assert result.exit_code == 1
    assert "does not exist" in result.stderr


def test_detect_success(tmp_path, monkeypatch):
    """CLI should print detected encoding when detect_file_encoding succeeds."""
    file = tmp_path / "sample.txt"
    file.write_text("hello", encoding="utf-8")

    monkeypatch.setattr("encoding_checker_cli.cli.detect_file_encoding", lambda p: "utf-8")

    result = runner.invoke(app, [str(file)])

    assert result.exit_code == 0
    assert f"Detected encoding for '{file}'" in result.stdout
    assert "utf-8" in result.stdout


@pytest.mark.parametrize(
    "encoding, expected",
    [
        ("shift_jis", "shift_jis"),
        ("utf-16-le", "utf-16-le"),
        ("utf-16-be", "utf-16-be"),
        ("utf-32-le", "utf-32-le"),
        ("utf-32-be", "utf-32-be"),
    ],
)
def test_detect_various_encodings(tmp_path, monkeypatch, encoding, expected):
    """CLI prints correct encoding for various encoding types."""
    file = tmp_path / "sample.txt"
    file.write_bytes(b"dummy")

    monkeypatch.setattr(
        "encoding_checker_cli.cli.detect_file_encoding",
        lambda p, enc=encoding: enc,
    )

    result = runner.invoke(app, [str(file)])

    assert result.exit_code == 0
    assert f"Detected encoding for '{file}'" in result.stdout
    assert expected in result.stdout


def test_detect_system_default(tmp_path, monkeypatch):
    """If encoding equals system default, '(System default encoding)' should appear."""
    file = tmp_path / "test.txt"
    file.write_text("abc", encoding=locale.getpreferredencoding())

    monkeypatch.setattr(
        "encoding_checker_cli.cli.detect_file_encoding",
        lambda p: locale.getpreferredencoding(),
    )

    result = runner.invoke(app, [str(file)])

    assert result.exit_code == 0
    assert "(System default encoding)" in result.stdout


def test_detect_failure(tmp_path, monkeypatch):
    """CLI should exit with code 1 when encoding cannot be detected."""
    file = tmp_path / "unknown.bin"
    file.write_bytes(b"\x00\xFF\x00\xFF")

    monkeypatch.setattr("encoding_checker_cli.cli.detect_file_encoding", lambda p: None)

    result = runner.invoke(app, [str(file)])

    assert result.exit_code == 1
    assert "Could not detect encoding" in result.stderr
