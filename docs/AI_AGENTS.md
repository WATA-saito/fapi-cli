## AI Agent Guide for `fapi-cli`

This document is written for **AI coding agents** (LLMs, autonomous assistants, CI bots) that need a **precise, machine-friendly** understanding of `fapi-cli`’s CLI interface, output formats, and error patterns.

`fapi-cli` loads a FastAPI application from a local Python file and sends requests to the ASGI app directly via `httpx`’s `ASGITransport` (no server process is started).

---

## Quick Start (Agent-Friendly)

- Install:
  - Minimal: `pip install fapi-cli`
  - With form/file support: `pip install 'fapi-cli[form]'`
- Run:
  - `fapi-cli request path/to/app.py -P /`
- Parse result:
  - Read **stdout** as JSON on success (exit code 0).
  - On failure (exit code 1), stdout may be empty; read **stderr** for a human-readable error message.

---

## CLI Overview

### Executable

- Command: `fapi-cli`
- Entry point: `fapi_cli.__main__:main`

### Subcommands

Currently implemented subcommands:

- `request`: send one HTTP request to a FastAPI app loaded from a Python file.

---

## `fapi-cli request` — Exact Interface

### Synopsis

```bash
fapi-cli request APP_FILE [OPTIONS]
```

### Positional Arguments

- `APP_FILE` (required)
  - Type: string (path)
  - Meaning: path to a Python file containing a `fastapi.FastAPI` instance.

### Options

- `-P, --path PATH`
  - Type: string
  - Default: `/`
  - Normalization:
    - Empty/whitespace becomes `/`
    - If it does not start with `/`, a leading `/` is added.

- `-X, --method METHOD`
  - Type: string
  - Default: `GET`
  - Normalization: uppercased before validation
  - Allowed values:
    - `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `OPTIONS`, `HEAD`, `TRACE`

- `-d, --data JSON_STRING`
  - Type: string
  - Meaning: request body encoded as JSON (parsed by `json.loads`)
  - Mutually exclusive with `-F/--form`

- `-F, --form ITEM` (repeatable)
  - Type: string
  - Default: empty (no form)
  - Meaning: send multipart form fields and/or files (curl-like).
  - Requires the optional dependency `python-multipart`:
    - Install via `pip install 'fapi-cli[form]'`
  - Mutually exclusive with `-d/--data`
  - Item grammar:
    - Field: `key=value`
    - File: `key=@path`
    - File with metadata:
      - `key=@path;type=mime/type`
      - `key=@path;filename=override.ext`
      - `key=@path;type=mime/type;filename=override.ext`
    - Notes:
      - `key` is stripped; empty keys are rejected.
      - File paths must exist and be readable.
      - Metadata is separated by semicolons (`;`). Unknown metadata keys are ignored.
  - Repeating the same key is supported and preserved.

- `-H, --header HEADER` (repeatable)
  - Type: string
  - Meaning: add one HTTP header to the request.
  - Required format: `Key: Value`
    - The first `:` splits the name and value; both sides are stripped.
    - Empty header names are rejected.
  - Note: duplicate header keys overwrite earlier values (internally stored as a dict).

- `-q, --query QUERY` (repeatable)
  - Type: string
  - Meaning: append query parameters.
  - Format:
    - Each `QUERY` may be `key=value&k2=v2` (parsed like URL querystring)
    - Multiple `-q` are concatenated.
    - Blank values are preserved.
  - Note: repeating the same key is supported and preserved.

- `--include-headers`
  - Type: boolean flag
  - Default: false
  - Meaning: include a `headers` object in the JSON output.

- `--app-name NAME`
  - Type: string
  - Default: unset
  - Meaning: name of the FastAPI variable inside `APP_FILE`.
  - If unset, candidates are tried in order:
    - `app`, `application`, `fastapi_app`

### Request Execution Semantics

- Transport: `httpx.ASGITransport(app=fastapi_app)`
- Base URL: `http://testserver`
- Redirects: `follow_redirects=True`
- Body handling:
  - If `-d/--data` is provided: it is parsed with `json.loads` and sent via `httpx` `json=...`.
  - If any `-F/--form` is provided:
    - Request becomes `multipart/form-data`
    - Form fields are included as multipart items with filename `None`
    - Files are included as multipart items (filename and optional content type)
  - `-d` and `-F` together is an error.
- Response body decoding:
  - If response is valid JSON: `body` is the parsed JSON value (object/array/string/number/bool/null).
  - Otherwise: `body` is the raw response text (string).

---

## Output Format (Success)

On success, `fapi-cli request` prints one JSON object to **stdout** (pretty-printed, UTF-8, `ensure_ascii=false`, indentation 2).

### JSON Shape

- Required keys:
  - `status_code`: integer
  - `body`: any JSON value, OR a string for non-JSON response bodies
- Optional keys:
  - `headers`: object (string-to-string map), present only when `--include-headers` is set

### JSON Schema (Draft 2020-12 compatible)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/WATA-saito/fapi-cli/schemas/request-output.json",
  "title": "fapi-cli request output",
  "type": "object",
  "required": ["status_code", "body"],
  "properties": {
    "status_code": { "type": "integer" },
    "body": {},
    "headers": {
      "type": "object",
      "additionalProperties": { "type": "string" }
    }
  },
  "additionalProperties": false
}
```

### Example (JSON response)

```json
{
  "status_code": 200,
  "body": { "message": "hello" }
}
```

### Example (non-JSON response)

```json
{
  "status_code": 200,
  "body": "<html>...</html>"
}
```

---

## Exit Codes and Error Output

### Exit Codes

- `0`: success (JSON written to stdout)
- `1`: recoverable CLI error (no JSON contract; error text emitted)

### Error Channel

Recoverable errors are printed as a single human-readable message to **stderr** (colored red when supported).

### Common Error Patterns (and Fixes)

- Application file not found:
  - Pattern: `Application file not found: ...`
  - Fix: ensure the file path exists and is readable.

- FastAPI app variable not found:
  - Pattern: `FastAPI application not found. Ensure your file defines ... (or use --app-name).`
  - Fix: define `app = FastAPI()` (or pass `--app-name`).

- Invalid method:
  - Pattern: `Invalid HTTP method: ... Supported methods: ...`
  - Fix: use one of the allowed methods.

- Invalid header format:
  - Pattern: `Invalid header format: '...'. Use 'Key: Value'.`
  - Fix: include a colon and a non-empty header name.

- JSON parse failure:
  - Pattern: `Failed to parse JSON: ...`
  - Fix: pass valid JSON to `-d/--data`.

- `-d` and `-F` used together:
  - Pattern: `-d/--data and -F/--form cannot be used together. ...`
  - Fix: choose either JSON (`-d`) or form/file (`-F`) mode.

- `-F` used but `python-multipart` missing:
  - Pattern includes: `The -F/--form option requires 'python-multipart'.` and `pip install 'fapi-cli[form]'`
  - Fix: install `python-multipart` (or `fapi-cli[form]`).

- File upload path not found:
  - Pattern: `File not found: ...`
  - Fix: ensure the file path after `@` exists.

- Invalid `-F` format:
  - Pattern: `Invalid -F/--form value: '...'. Use 'key=value' or 'key=@path'.`
  - Fix: include `=` and a non-empty key.

---

## Example Workflows (Copy-Paste Friendly)

### 1) Smoke test an endpoint (GET)

```bash
fapi-cli request ./main.py -P /
```

Agent logic:
- If exit code is 0: parse stdout JSON, check `status_code == 200`.
- If exit code is 1: capture stderr and report it.

### 2) POST JSON payload

```bash
fapi-cli request ./main.py -X POST -P /items -d '{"name":"Alice"}'
```

### 3) Add headers and query parameters

```bash
fapi-cli request ./main.py -P /search -H "Authorization: Bearer token" -q "q=test&limit=5"
```

### 4) Submit form fields (multipart)

```bash
fapi-cli request ./main.py -X POST -P /form -F "name=Alice" -F "age=30"
```

### 5) Upload a file (multipart)

```bash
fapi-cli request ./main.py -X POST -P /upload -F "file=@./image.png"
```

### 6) Upload with content-type and filename override

```bash
fapi-cli request ./main.py -X POST -P /upload -F "file=@./data.bin;type=application/octet-stream;filename=payload.bin"
```

---

## MCP / Tool Descriptor (Proposal)

If you want to expose `fapi-cli request` as a tool in an agent runtime, the key is to make the tool’s I/O contract match the **stdout JSON schema** above, and treat non-zero exit codes as tool errors.

Here is a minimal descriptor-style JSON you can adapt (format varies by MCP host):

```json
{
  "name": "fapi_cli_request",
  "description": "Send one HTTP request to a FastAPI app loaded from a local Python file, and return a structured JSON result.",
  "inputSchema": {
    "type": "object",
    "required": ["app_file"],
    "properties": {
      "app_file": { "type": "string", "description": "Path to Python file containing FastAPI app." },
      "path": { "type": "string", "default": "/" },
      "method": { "type": "string", "default": "GET" },
      "data": { "type": "string", "description": "JSON string for request body. Mutually exclusive with form." },
      "form": {
        "type": "array",
        "items": { "type": "string" },
        "description": "Repeatable -F items: key=value or key=@path[;type=...][;filename=...]"
      },
      "header": { "type": "array", "items": { "type": "string" }, "description": "Repeatable headers: 'Key: Value'." },
      "query": { "type": "array", "items": { "type": "string" }, "description": "Repeatable query strings: 'a=1&b=2'." },
      "include_headers": { "type": "boolean", "default": false },
      "app_name": { "type": "string", "description": "FastAPI variable name in the module." }
    },
    "additionalProperties": false
  },
  "outputSchema": {
    "$ref": "https://github.com/WATA-saito/fapi-cli/schemas/request-output.json"
  }
}
```

---

## Notes for Robust Agent Integration

- Always validate stdout as JSON only when the process exit code is 0.
- Treat exit code 1 as a tool error and surface stderr to the user.
- When generating `-d/--data`, ensure the JSON string is valid and properly quoted for the target shell.
- Prefer `--app-name` if the app file does not define `app`/`application`/`fastapi_app`.

