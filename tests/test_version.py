import builtins
import importlib
from importlib.metadata import PackageNotFoundError
from pathlib import Path

import pytest

from encoding_checker_cli.library.helper_func import get_version


def test_get_version_from_metadata(monkeypatch):
    """
    importlib.metadata.version returns something → use that value.
    """

    def fake_version(_):
        return "7.7.7"

    monkeypatch.setattr(
        "encoding_checker_cli.library.helper_func.version", fake_version
    )

    assert get_version() == "7.7.7"


def test_get_version_fallback(monkeypatch, tmp_path):
    """
    No metadata, no pyproject → return 0.0.0
    """

    # 1. Simulate metadata not found
    def raise_pkg_not_found(_):
        raise PackageNotFoundError()

    monkeypatch.setattr(
        "encoding_checker_cli.library.helper_func.version", raise_pkg_not_found
    )

    # 2. Simulate that no pyproject exists in parents
    fake_file = tmp_path / "dummy.py"
    fake_file.write_text("")
    monkeypatch.setattr(
        "encoding_checker_cli.library.helper_func.__file__", str(fake_file)
    )

    assert get_version() == "0.0.0"
