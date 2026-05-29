# Publishing Guide

This repository is packaged as a real Python CLI tool.

It includes automation for:

- CI build verification
- release versioning
- TestPyPI publishing
- PyPI publishing

## Build Locally

Create both the wheel and source distribution:

```bash
python -m build
```

This should generate:

- `dist/*.whl`
- `dist/*.tar.gz`

## Upload to TestPyPI

Use Twine:

```bash
twine upload --repository testpypi dist/*
```

TestPyPI index:

- `https://test.pypi.org`

GitHub workflow:

- `.github/workflows/publish-testpypi.yml`

## Install from TestPyPI

Example install command:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple fastapi-rag
```

## Local Editable Install

For development:

```bash
pip install -e .
```

Then verify:

```bash
fastapi-rag new demo
cd demo
docker compose up --build
```

## PyPI Publishing

Production release publishing is handled by:

- `.github/workflows/publish-pypi.yml`

The workflow runs when a GitHub release is published.

## Semantic Versioning

Version automation is handled by:

- `.github/workflows/release-please.yml`

The repository is configured for conventional commits and release-please.

Examples:

- `feat: add gemini prompt option`
- `fix: include template docs in wheel`
- `docs: improve install instructions`

## Release Checklist

Before publishing:

1. run `pytest`
2. run `python -m build`
3. inspect the generated `dist/` files
4. test an install in a clean virtual environment
5. run `fastapi-rag new demo`
6. verify the generated project starts with Docker
