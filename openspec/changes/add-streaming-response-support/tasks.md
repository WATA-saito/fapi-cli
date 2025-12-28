# Tasks: Streaming Response Support

## 1. Implementation

- [ ] 1.1 `RequestConfig` に `stream: bool` フィールドを追加
- [ ] 1.2 `request` コマンドに `--stream` / `-s` オプションを追加
- [ ] 1.3 `_execute_request_async` にストリーミングモードのロジックを実装
  - `client.stream()` を使用
  - `response.aiter_bytes()` でチャンクごとに出力
  - ステータスコードを標準エラーに出力
- [ ] 1.4 `--include-headers` との組み合わせ時の動作を実装

## 2. Testing

- [ ] 2.1 ストリーミングレスポンスを返すテスト用FastAPIアプリを作成
- [ ] 2.2 `--stream` オプションの基本動作テスト
- [ ] 2.3 `--stream` と `--include-headers` の組み合わせテスト
- [ ] 2.4 ストリーミング中のエラーハンドリングテスト

## 3. Documentation

- [ ] 3.1 READMEに `--stream` オプションの使用例を追加
- [ ] 3.2 ヘルプテキストの更新確認
