## 1. Implementation
- [ ] 1.1 Add `--stream` option to `fapi-cli request` (CLI surface)
- [ ] 1.2 Enforce `--stream` incompatibility with `--include-headers` (clear error + exit code 1)
- [ ] 1.3 Implement streaming execution path using `httpx.AsyncClient.stream(...)`
- [ ] 1.4 Add tests for `StreamingResponse` (text stream at minimum)
- [ ] 1.5 Update docs: `README.md`, `README.ja.md`, and root `AGENTS.md`

## 2. Validation
- [ ] 2.1 Run `openspec validate add-streaming-response-support --strict` and fix findings

