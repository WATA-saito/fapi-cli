<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

## AI Agent Notes (Recommended)

If your AI agent / automation needs an exact interface contract for `fapi-cli` (options, output JSON schema, exit codes, common error patterns), use:

- `docs/AI_AGENTS.md`

For OpenSpec-driven planning/proposals, follow:

- `openspec/AGENTS.md`