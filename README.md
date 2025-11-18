# fapi-cli

FastAPIアプリケーションに対してサーバーを起動せずにHTTPリクエストを送信できるCLIツールです。`fastapi.testclient.TestClient`を活用して、ローカルファイルからFastAPIアプリケーションを読み込み、curlライクなインターフェースでエンドポイントを呼び出します。

## 特長

- `fapi-cli request` コマンドで任意のFastAPIアプリケーションにリクエストを送信
- `-X/--method`, `-P/--path`, `-d/--data`, `-H/--header`, `-q/--query` といったcurl互換のオプション
- JSONレスポンスを整形して標準出力に表示
- `--include-headers` でレスポンスヘッダーも表示可能

## インストール

### PyPIからインストール

```bash
pip install fapi-cli
```

### pipxでインストール（推奨）

```bash
pipx install fapi-cli
```

### uvxで一時実行

```bash
uvx fapi-cli request main.py -P /
```

### 開発用インストール

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## 要件

- Python 3.9以上
- FastAPIアプリケーション（テスト対象）

## 使い方

```bash
# アプリケーションを定義したファイルからGETリクエスト
fapi-cli request src/main.py

# POSTメソッドでJSONボディを送信
fapi-cli request src/main.py -X POST -P /items -d '{"name": "Alice"}'

# ヘッダーとクエリパラメータを付与
fapi-cli request src/main.py -H "Authorization: Bearer token" -q "page=1"

# アプリケーションの変数名が app 以外の場合
fapi-cli request src/api.py --app-name fastapi_app
```

## 開発

```bash
source .venv/bin/activate
pip install -e .[dev]
pytest
```

### パッケージング

```bash
python -m build
twine check dist/*
```

TestPyPIへアップロードする場合は、事前に`~/.pypirc`を設定した上で以下のコマンドを実行してください。

```bash
twine upload --repository testpypi dist/*
```

## ライセンス

MIT License
