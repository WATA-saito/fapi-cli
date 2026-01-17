# fapi-cli

CLI tool to invoke FastAPI endpoints **without starting a server**. It loads a FastAPI application from a local Python file and calls the ASGI app directly via `httpx` ASGI transport, providing a curl-like interface.

## Features

- Send requests to any FastAPI application with `fapi-cli request`
- curl-like options: `-X/--method`, `-P/--path`, `-d/--data`, `-H/--header`, `-q/--query`
- Form fields & file uploads with `-F/--form` (`multipart/form-data`)
- Pretty-printed JSON response output to stdout
- Include response headers with `--include-headers`

> **Note**: Some combinations of `starlette` TestClient and `httpx` may have compatibility issues. This tool avoids that by calling the ASGI app directly via `httpx` ASGI transport.

## Installation

### Install from PyPI

```bash
pip install fapi-cli
```

### Install with pipx (recommended)

```bash
pipx install fapi-cli
```

### Run with uvx (one-off)

```bash
uvx fapi-cli request main.py -P /
```

> **Note (uvx / TestPyPI)**: On TestPyPI, dependency resolution may pick untested versions (especially for pre-releases). Pin dependencies explicitly if needed. Example:
>
> ```bash
> uvx fapi-cli request main.py -P / --with "fastapi<1.0"
> uvx fapi-cli request main.py -P / -F "name=Alice" --with "fastapi<1.0" --with "python-multipart<1.0"
> ```

## Requirements

- Python 3.9+
- FastAPI 0.100.0+
- A FastAPI application (target)

## Usage

```bash
# GET request to an app defined in a file
fapi-cli request src/main.py

# POST with JSON body
fapi-cli request src/main.py -X POST -P /items -d '{"name": "Alice"}'

# Add headers and query parameters
fapi-cli request src/main.py -H "Authorization: Bearer token" -q "page=1"

# If your FastAPI variable name is not `app`
fapi-cli request src/api.py --app-name fastapi_app
```

## For AI Agents

If you are building an AI agent / automation that needs an exact interface contract (options, output JSON schema, exit codes, and common error patterns), see:

- `docs/AI_AGENTS.md`

### Form fields and file uploads

Use `-F` to send form fields and files (equivalent to curl's `-F`).

> **Note**: Form/file support requires `python-multipart`. If your FastAPI app uses `Form()` / `File()`, it’s likely already installed. Otherwise:
>
> ```bash
> pip install 'fapi-cli[form]'
> ```

```bash
# Send form fields
fapi-cli request src/main.py -X POST -P /form -F "name=Alice" -F "age=30"

# Same key multiple times (e.g., Form(List[str]))
fapi-cli request src/main.py -X POST -P /tags -F "tag=python" -F "tag=fastapi"

# Upload a file (with @ prefix)
fapi-cli request src/main.py -X POST -P /upload -F "file=@./image.png"

# Specify Content-Type
fapi-cli request src/main.py -X POST -P /upload -F "document=@./file.pdf;type=application/pdf"

# Override filename
fapi-cli request src/main.py -X POST -P /upload -F "file=@./temp.txt;filename=report.txt"

# Mix form fields and files
fapi-cli request src/main.py -X POST -P /profile -F "name=Alice" -F "avatar=@./photo.jpg"

# Multiple files under the same key (e.g., File(List[UploadFile]))
fapi-cli request src/main.py -X POST -P /upload-many -F "files=@./a.txt" -F "files=@./b.txt"
```

> **Note**: `-d` (JSON body) and `-F` (form/file) cannot be used together.

## License

MIT License
