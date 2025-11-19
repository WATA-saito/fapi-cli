"""FastAPI CLIツールのパッケージエントリ。"""

from importlib.metadata import version, PackageNotFoundError

__all__ = ["__version__"]


def _resolve_version() -> str:
    try:
        return version("fapi-cli")
    except PackageNotFoundError:  # pragma: no cover - fallback during development
        return "0.0.0"


__version__ = _resolve_version()
