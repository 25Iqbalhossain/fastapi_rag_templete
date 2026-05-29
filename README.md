# fastapi-rag

`fastapi-rag` is an installable Python CLI that generates production-grade FastAPI backends for AI applications, RAG systems, internal copilots, and enterprise SaaS platforms.

It is intended to behave like a real developer tool, not a local scaffold script.

## What It Does

After installation:

```bash
fastapi-rag new myapp
cd myapp
docker compose up --build
```

The generated project includes:

- FastAPI application structure
- JWT authentication
- SQLAlchemy async setup
- provider abstractions for DB, cache, queue, LLM, and vector stores
- RAG ingestion and query pipeline
- Redis and Celery integration
- Docker Compose startup
- health endpoints, metrics, and observability wiring
- tests and developer docs

## Repository Structure

```text
src/fastapi_rag/
├── cli/
│   └── main.py
├── generators/
│   └── project_generator.py
├── renderer/
│   └── jinja_renderer.py
├── templates/
│   └── full_rag/
└── utils/
    └── package_resources.py
```

## Installation

### Local development install

```bash
pip install -e .
```

### Package build

```bash
python -m build
```

This generates:

- wheel in `dist/*.whl`
- source distribution in `dist/*.tar.gz`

### Install after publishing

```bash
pip install fastapi-rag
```

## Quick Start

Generate a new backend:

```bash
fastapi-rag new myapp
```

The CLI will ask for:

1. project name
2. LLM provider
3. vector database
4. database provider
5. cache provider

Then it will:

1. load the packaged template
2. copy it into `./myapp`
3. render all Jinja variables
4. output a complete backend project

Run the generated project:

```bash
cd myapp
docker compose up --build
```

## Supported Provider Defaults

The packaged template currently supports or models:

- LLM: `echo`, `openai`, `ollama`
- Vector DB: `qdrant`, `chroma`, `pgvector`, `pinecone`
- Database: `postgresql`, `mysql`
- Cache: `redis`, `dragonfly`
- Queue: `celery`

## Architecture Overview

The generated backend uses a modular architecture with:

- `app/api/`
- `app/core/`
- `app/db/`
- `app/modules/`
- `app/providers/`
- `app/services/`
- `app/workers/`

The generator itself is separated from the scaffold so packaging and runtime template access stay reliable after installation.

## Package-Safe Template Loading

Templates are loaded with `importlib.resources`, not fragile relative paths.

That means `fastapi-rag` can work after:

- `pip install -e .`
- `pip install fastapi-rag`
- wheel installation
- source distribution installation

## Development Workflow

Install local dependencies:

```bash
pip install -e .[dev]
```

Run tests:

```bash
pytest
```

Build distributions:

```bash
python -m build
```

Validate package metadata:

```bash
twine check dist/*
```

## CI and Release Automation

This repository includes GitHub Actions workflows for:

- CI test and build verification
- version and release automation
- TestPyPI publishing
- PyPI publishing

Workflows:

- `.github/workflows/ci.yml`
- `.github/workflows/release-please.yml`
- `.github/workflows/publish-testpypi.yml`
- `.github/workflows/publish-pypi.yml`

## Publishing

### Build locally

```bash
python -m build
```

### Upload to TestPyPI

```bash
twine upload --repository testpypi dist/*
```

### Install from TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple fastapi-rag
```

## Versioning

This repository is configured for conventional commits and release-please.

Expected examples:

- `feat: add anthropic provider prompt option`
- `fix: include templates in sdist build`
- `docs: improve publishing guide`

Release automation updates:

- version in `pyproject.toml`
- release PR
- git tag
- GitHub release
- changelog

## Documentation

- [docs/ARCHITECTURE.md](/home/iqbal-ai/Downloads/industry_ai_backend_template/docs/ARCHITECTURE.md)
- [docs/USER_GUIDE.md](/home/iqbal-ai/Downloads/industry_ai_backend_template/docs/USER_GUIDE.md)
- [docs/FIRST_FEATURE.md](/home/iqbal-ai/Downloads/industry_ai_backend_template/docs/FIRST_FEATURE.md)
- [docs/PUBLISHING.md](/home/iqbal-ai/Downloads/industry_ai_backend_template/docs/PUBLISHING.md)
- [CONTRIBUTING.md](/home/iqbal-ai/Downloads/industry_ai_backend_template/CONTRIBUTING.md)

## License

This project is released under the [MIT License](/home/iqbal-ai/Downloads/industry_ai_backend_template/LICENSE).
