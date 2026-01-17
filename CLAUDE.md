## Claude / AI Agent Instructions (Repository Entry)

This repository contains both:

- A CLI tool (`fapi-cli`) and its agent-friendly interface contract
- An OpenSpec workflow for spec-driven changes

### fapi-cli interface contract (recommended)

Agents SHOULD treat `docs/AI_AGENTS.md` as the authoritative CLI contract:

- Exact CLI options and constraints
- Output JSON schema (`status_code`, `body`, optional `headers`)
- Exit codes and common error patterns

See:

- `docs/AI_AGENTS.md`

### OpenSpec workflow (when planning/proposals are involved)

If the request mentions planning/spec/proposals/changes (or is ambiguous and needs authoritative guidance), read and follow:

- `openspec/AGENTS.md`

### Reference style guide for agent specs

See:

- [Zenn: AIエージェント向け仕様書の置き方](https://zenn.dev/yusukebe/articles/ff69c13ccafb28)

