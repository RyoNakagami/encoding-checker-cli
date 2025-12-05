from pathlib import Path
import tomllib
from importlib.metadata import version, PackageNotFoundError


def get_version() -> str:
    """
    Retrieve the version of the installed package.

    Priority:
    1. Installed metadata (importlib.metadata.version)
    2. pyproject.toml in development mode
    3. fallback "0.0.0"
    """

    # 1. Installed package metadata
    try:
        return version("encoding-checker-cli")
    except PackageNotFoundError:
        pass

    # 2. Development mode: look for pyproject.toml
    current = Path(__file__).resolve()
    for parent in current.parents:
        pyproject = parent / "pyproject.toml"
        if pyproject.exists():
            try:
                with pyproject.open("rb") as f:
                    data = tomllib.load(f)
                project_version = data.get("project", {}).get("version")
                if project_version:
                    return project_version
            except Exception:
                pass

    # 3. fallback
    return "0.0.0"
