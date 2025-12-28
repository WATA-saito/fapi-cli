# Change: Add Streaming Response Support

## Why

FastAPIの`StreamingResponse`を使用するエンドポイントをテストする際、現在のCLI実装ではレスポンス全体が受信されるまで待機してから出力するため、以下の問題がある：

1. **リアルタイム性の欠如**: Server-Sent Events (SSE) やLLMストリーミングなど、チャンクごとの出力が見られない
2. **メモリ効率**: 大きなストリーミングレスポンスで全データをメモリに保持する必要がある
3. **デバッグ困難**: ストリーミングの動作確認やタイミング問題の調査ができない

## What Changes

- `--stream` オプションを追加し、ストリーミングモードを有効にする
- ストリーミングモードでは、チャンクごとにリアルタイムで標準出力に出力する
- httpxの `stream()` メソッドと `aiter_bytes()` / `aiter_lines()` を使用
- 通常モード（デフォルト）は既存の動作を維持

## Impact

- Affected specs: `cli-tool`
- Affected code: `src/fapi_cli/cli.py`
- 既存の動作への影響: なし（`--stream` を指定しない場合は従来通り）
