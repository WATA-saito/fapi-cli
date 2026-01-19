# Change: Add StreamingResponse support to `fapi-cli request`

## Why
FastAPI の `StreamingResponse` を返すエンドポイントに対して、現状の `fapi-cli request` はレスポンス全体を読み切ってから出力するため、ストリーミング用途（大容量ダウンロード、逐次出力など）で実用的ではない。

## What Changes
- `fapi-cli request` に `--stream` オプションを追加し、レスポンスボディを **バッファせず** 受信した順に標準出力へ書き出す。
- `--stream` 指定時は、通常モードの JSON 出力（`status_code` / `body` / 任意で `headers`）を行わない（**出力形式が異なる**）。
- `--stream` と `--include-headers` の同時指定はエラーにする（出力形式の衝突を避けるため）。

## Impact
- Affected specs: `openspec/specs/cli-tool/spec.md`
- Affected code: `src/fapi_cli/cli.py`, `tests/test_request_command.py`, `README.md`, `README.ja.md`, `AGENTS.md`

