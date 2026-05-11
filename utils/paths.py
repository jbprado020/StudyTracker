"""Path helpers for Study Tracker."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def project_path(*parts: str) -> Path:
    """Return an absolute path inside the repository root."""
    return PROJECT_ROOT.joinpath(*parts)


def resource_path(*parts: str) -> Path:
    """Return an absolute path to a bundled project resource."""
    return project_path(*parts)
