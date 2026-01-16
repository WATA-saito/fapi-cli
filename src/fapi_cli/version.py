"""Utilities for FastAPI version compatibility."""

from __future__ import annotations

from packaging import version as pkg_version


def get_fastapi_version() -> str:
    """Get the installed FastAPI version."""
    try:
        from fastapi import __version__

        return __version__
    except ImportError:
        return "0.0.0"


def is_fastapi_version_at_least(min_version: str) -> bool:
    """Return True if FastAPI version is at least min_version."""
    try:
        current = get_fastapi_version()
        return pkg_version.parse(current) >= pkg_version.parse(min_version)
    except Exception:
        return False
