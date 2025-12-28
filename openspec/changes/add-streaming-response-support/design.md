# Design: Streaming Response Support

## Context

FastAPIでは`StreamingResponse`を使用して、チャンクごとにデータを送信できる。これはLLM応答のストリーミング、Server-Sent Events (SSE)、大きなファイルのダウンロードなどで使用される。

現在のCLI実装は`httpx.AsyncClient.request()`を使用し、レスポンス全体を受信後に処理している。これをストリーミング対応にするには`stream()`メソッドを使用する必要がある。

## Goals / Non-Goals

### Goals

- ストリーミングレスポンスをチャンクごとにリアルタイム出力
- 既存の動作を維持（後方互換性）
- シンプルなオプション追加で機能を有効化

### Non-Goals

- WebSocket対応（別途提案が必要）
- ストリーミングデータの解析・整形（生データをそのまま出力）
- JSON Lines形式の自動パース

## Decisions

### Decision 1: 出力形式

**選択**: ストリーミングモードでは、チャンクをそのまま標準出力に出力する（JSON wrappingなし）

**理由**:
- ストリーミングデータの性質上、JSONでラップすると全データ受信後にしか出力できない
- curlの`--no-buffer`と同様のシンプルな動作
- パイプライン処理との親和性（例: `fapi-cli request app.py --stream | jq --stream`）

**代替案**:
- チャンクごとにJSON出力 → 実装複雑化、フォーマットの標準化が難しい
- NDJSON形式 → SSE以外のストリーミングには不適切

### Decision 2: オプション設計

**選択**: `--stream` / `-s` フラグで有効化

```bash
fapi-cli request app.py -P /stream --stream
fapi-cli request app.py -P /stream -s
```

**理由**:
- curlの`-N`/`--no-buffer`に類似した直感的なUX
- デフォルトは従来動作を維持（後方互換性）

### Decision 3: ステータスコードとヘッダーの扱い

**選択**: 
- ステータスコードは受信時に標準エラー出力に表示
- `--include-headers`指定時はヘッダーも標準エラーに出力
- ボディのみ標準出力に出力

**理由**:
- 標準出力をストリーミングデータのみに保つことで、パイプライン処理が容易
- メタデータは標準エラーに分離

**出力例**:
```bash
$ fapi-cli request app.py -P /stream --stream
# stderr: Status: 200
# stdout: (streaming data...)
```

### Decision 4: httpxのストリーミングAPI

**選択**: `client.stream()` + `response.aiter_bytes()` を使用

```python
async with client.stream(method, path, ...) as response:
    async for chunk in response.aiter_bytes():
        sys.stdout.buffer.write(chunk)
        sys.stdout.buffer.flush()
```

**理由**:
- バイナリデータを正しく扱える
- メモリ効率が良い
- チャンクごとの即時出力が可能

## Risks / Trade-offs

| リスク | 影響 | 緩和策 |
|--------|------|--------|
| 出力形式の不統一 | 通常モードとストリーミングモードで出力形式が異なる | ドキュメントで明確に説明 |
| バイナリデータの扱い | 非テキストデータが端末に出力される可能性 | `--output`オプションの将来追加を検討 |

## Migration Plan

- 新機能追加のみで、既存機能の変更なし
- マイグレーション不要

## Open Questions

1. ストリーミング中のエラー（途中で接続が切れた場合など）の扱いは？
   - 案: エラーメッセージを標準エラーに出力し、非ゼロ終了コードで終了
