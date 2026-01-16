# Developer documentation

## Development installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Development

```bash
source .venv/bin/activate
pip install -e .[dev]
pytest
```

## Testing across multiple versions

This project is tested across multiple FastAPI versions.

### Testing with tox

```bash
# Run tests in all environments
tox

# Run a specific Python/FastAPI combo
tox -e py312-fastapilatest
```

### Supported FastAPI versions

- FastAPI >= 0.100.0, < 0.115.0
- FastAPI >= 0.115.0, < 0.120.0
- FastAPI >= 0.120.0 (latest)

In CI, tests run across combinations of Python 3.9, 3.10, 3.11, 3.12, 3.13, 3.14 and the FastAPI ranges above.

## Packaging

### Local build

```bash
python -m build
twine check dist/*
```

### Upload from local (manual)

Before running the commands below, configure `~/.pypirc`.

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

## Release flow

This project uses Git tag-based versioning and GitHub Actions for automated releases.

### Versioning

- Versions are automatically derived from Git tags (via hatch-vcs)
- Tag format: `v0.1.0`, `v1.2.3` (semantic versioning)

### Release to TestPyPI (for testing)

```bash
# Create a pre-release tag
git tag v0.1.0-rc1
git push origin v0.1.0-rc1
```

Alternatively, you can run the workflow manually from GitHub Actions.

### Release to PyPI (production)

```bash
# Create a stable release tag
git tag v0.1.0
git push origin v0.1.0
```

This triggers:
1. Tests (Python 3.9, 3.14)
2. Package build
3. Publish to PyPI
4. Create GitHub release notes

## Initial setup for PyPI/TestPyPI (Trusted Publisher)

To publish packages safely from GitHub Actions, configure a Trusted Publisher.

### 1. Create PyPI/TestPyPI accounts

- PyPI: https://pypi.org/account/register/
- TestPyPI: https://test.pypi.org/account/register/

### 2. Configure TestPyPI Trusted Publisher

1. Go to https://test.pypi.org/manage/account/publishing/
2. Click "Add a new pending publisher" and fill in:
   - PyPI Project Name: `fapi-cli`
   - Owner: `WATA-saito` (GitHub username)
   - Repository name: `fapi-cli`
   - Workflow name: `publish-testpypi.yml`
   - Environment name: `testpypi`

### 3. Configure PyPI Trusted Publisher

1. Go to https://pypi.org/manage/account/publishing/
2. Click "Add a new pending publisher" and fill in:
   - PyPI Project Name: `fapi-cli`
   - Owner: `WATA-saito` (GitHub username)
   - Repository name: `fapi-cli`
   - Workflow name: `release.yml`
   - Environment name: `pypi`

### 4. Configure GitHub Environments

1. Repository Settings → Environments
2. Create `testpypi` and `pypi`
3. Configure protection rules as needed (e.g., required reviewers)

### 5. First release test

```bash
# Test with TestPyPI
git tag v0.1.0-rc1
git push origin v0.1.0-rc1

# Install from TestPyPI and verify
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ fapi-cli
```
