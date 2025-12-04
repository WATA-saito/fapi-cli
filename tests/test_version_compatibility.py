"""FastAPIバージョン互換性のテスト。"""

from __future__ import annotations

import pytest

from fapi_cli.version import get_fastapi_version, is_fastapi_version_at_least


def test_get_fastapi_version() -> None:
    """FastAPIのバージョンを取得できることを確認する。"""
    version = get_fastapi_version()
    assert version != "0.0.0"
    # バージョン形式の確認（例: "0.87.0" や "0.115.0"）
    assert "." in version


def test_is_fastapi_version_at_least() -> None:
    """バージョン比較が正しく動作することを確認する。"""
    # 現在のバージョンは0.87.0以上であるべき
    assert is_fastapi_version_at_least("0.87.0")
    # 0.0.0より大きいことを確認
    assert is_fastapi_version_at_least("0.0.0")
    # 非常に大きなバージョンより小さいことを確認
    assert not is_fastapi_version_at_least("999.0.0")


@pytest.mark.parametrize(
    "min_version",
    [
        "0.87.0",  # 最小サポートバージョン
        "0.100.0",
        "0.115.0",
    ],
)
def test_fastapi_version_compatibility(min_version: str) -> None:
    """FastAPIのバージョンが最小要件を満たしていることを確認する。"""
    assert is_fastapi_version_at_least(min_version), (
        f"FastAPI {get_fastapi_version()} should be >= {min_version}"
    )
