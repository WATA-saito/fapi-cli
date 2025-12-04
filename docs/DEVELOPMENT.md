# 開発者向けドキュメント

## 開発用インストール

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## 開発

```bash
source .venv/bin/activate
pip install -e .[dev]
pytest
```

## 複数バージョンでのテスト

このプロジェクトは複数のFastAPIバージョンでテストされています。

### toxを使用したテスト

```bash
# すべての環境でテストを実行
tox

# 特定のPythonバージョンとFastAPIバージョンの組み合わせでテスト
tox -e py312-fastapilatest
```

### サポートされているFastAPIバージョン

- FastAPI 0.100.0以上、0.115.0未満
- FastAPI 0.115.0以上、0.120.0未満
- FastAPI 0.120.0以上（最新）

CIでは、Python 3.9、3.10、3.11、3.12、3.13、3.14と上記のFastAPIバージョンの組み合わせでテストが実行されます。

## パッケージング

```bash
python -m build
twine check dist/*
```

TestPyPIへアップロードする場合は、事前に`~/.pypirc`を設定した上で以下のコマンドを実行してください。

```bash
twine upload --repository testpypi dist/*
```
