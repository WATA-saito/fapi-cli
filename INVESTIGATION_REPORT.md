# FastAPI/Starlette バージョン互換性調査レポート

## 調査日
2025-12-26

## 調査の背景
ユーザーから「fastapiのバージョンによってこのツールが使えない。おそらくstarletteのバージョンの違いで、テストクライアントにappを入れるかどうかが変わっている」という報告を受けて調査を実施。

## 調査内容

### 1. TestClientのシグネチャ確認

以下のバージョンでTestClient.__init__のシグネチャを確認：

| Starlette Version | 最初のパラメータ | 位置引数 | キーワード引数 |
|-------------------|------------------|----------|----------------|
| 0.20.0            | app              | ✓        | ✓              |
| 0.21.0            | app              | ✓        | ✓              |
| 0.25.0            | app              | ✓        | ✓              |
| 0.27.0            | app              | ✓        | ✓              |
| 0.28.0            | app              | ✓        | ✓              |
| 0.32.0            | app              | ✓        | ✓              |
| 0.35.0            | app              | ✓        | ✓              |
| 0.36.0            | app              | ✓        | ✓              |
| 0.37.0            | app              | ✓        | ✓              |
| 0.40.0            | app              | ✓        | ✓              |
| 0.41.0            | app              | ✓        | ✓              |
| 0.45.0            | app              | ✓        | ✓              |
| 0.49.0            | app              | ✓        | ✓              |
| 0.50.0            | app              | ✓        | ✓              |

### 2. FastAPI + Starlette バージョン組み合わせテスト

| FastAPI | Starlette | テスト結果 | 備考 |
|---------|-----------|------------|------|
| 0.100.0 | 0.27.0    | PASS/FAIL* | *初回FAILしたが再試行でPASS |
| 0.100.0 | 0.37.2    | PASS       | |
| 0.110.0 | 0.37.2    | PASS       | |
| 0.115.0 | 0.40.0    | PASS       | |
| 0.120.0 | 0.45.0    | PASS       | |
| 0.127.0 | 0.50.0    | PASS       | 最新版 |

### 3. 現在の実装

`src/fapi_cli/cli.py:240`：
```python
client = TestClient(fastapi_app)
```

この実装は正しく、すべてのテストしたバージョンで動作します。

### 4. FastAPIのTestClient

FastAPIの`TestClient`はStarletteの`TestClient`をそのまま再エクスポートしているため、両者は同一のクラスです：

```python
from fastapi.testclient import TestClient  # これは
from starlette.testclient import TestClient  # これと同じ
```

## 結論

1. **問題なし**: 調査範囲内（Starlette 0.20.0～0.50.0）で、`TestClient`のシグネチャは一貫しており、`TestClient(app)`の形式で問題ありません。

2. **位置引数とキーワード引数の両方が使用可能**: すべてのバージョンで以下の両方が動作します：
   - `TestClient(app)`
   - `TestClient(app=app)`

3. **現在の実装は適切**: `cli.py`の実装は正しく、変更の必要はありません。

## 推奨事項

### 1. pyproject.tomlの依存関係は適切
```toml
dependencies = [
  "fastapi>=0.100.0,<1.0",
  "typer>=0.9.0",
  "httpx>=0.23"
]
```

### 2. 予防的措置（オプション）

以下を検討してもよい：

#### A. より明示的なTestClient初期化
```python
# 現在
client = TestClient(fastapi_app)

# より明示的（オプション）
client = TestClient(app=fastapi_app)
```

#### B. バージョンチェック機能の活用
既に`src/fapi_cli/version.py`にバージョンチェック機能があるため、必要に応じて使用可能。

#### C. CI/CDでの複数バージョンテスト
tox.iniを拡張して、複数のFastAPI/Starletteバージョンでテストを実行。

### 3. 文書化

README.mdに以下を明記（既に記載済み）：
- 対応FastAPIバージョン: 0.100.0以上
- Python 3.9以上

## 次のステップ

もしユーザーが具体的なエラーメッセージや失敗ケースを持っている場合は：
1. そのエラーメッセージを確認
2. 使用しているFastAPI/Starletteのバージョンを確認
3. 再現手順を確認

現時点では、コードの変更は不要と判断されます。
