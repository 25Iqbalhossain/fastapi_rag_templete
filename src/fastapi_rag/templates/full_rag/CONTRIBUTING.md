# Contributing

Thanks for contributing to this template.

The goal of this project is to provide a serious open source backend foundation for AI-native products. Contributions should improve real-world usefulness, code quality, maintainability, or developer experience.

## Project Principles

Please keep these principles in mind when contributing:

- prefer real implementations over placeholder architecture
- keep the project async-first
- protect modular boundaries
- use provider abstractions instead of hardcoding vendors into routes or services
- optimize for maintainability, not cleverness
- keep documentation as strong as the code

## Good Contribution Areas

Useful contributions include:

- new provider implementations
- stronger tests
- improved RAG orchestration
- better queue or worker patterns
- observability improvements
- deployment examples
- bug fixes in auth, DB, cache, worker, or vectorstore layers
- documentation improvements for junior developers

## Before You Start

1. read [README.md](/home/iqbal-ai/Downloads/industry_ai_backend_template/README.md)
2. read [docs/USER_GUIDE.md](/home/iqbal-ai/Downloads/industry_ai_backend_template/docs/USER_GUIDE.md)
3. read [docs/ARCHITECTURE.md](/home/iqbal-ai/Downloads/industry_ai_backend_template/docs/ARCHITECTURE.md)
4. understand which layer your change belongs to

## Local Setup

Copy the environment file:

```bash
cp .env.example .env
```

Start the local stack:

```bash
docker compose up --build
```

Useful endpoints:

- `http://localhost:8000/docs`
- `http://localhost:8000/health`
- `http://localhost:8000/ready`
- `http://localhost:8000/metrics`

## Development Rules

### Architecture rules

- routes should stay thin
- business logic belongs in services or modules
- repositories should focus on persistence
- provider-specific SDK logic belongs in `app/providers/`
- application-wide behavior belongs in `app/core/`

### Code rules

- add type hints
- keep functions focused
- avoid giant utility files
- do not introduce placeholder `pass` implementations
- do not add dead files or unused abstractions

### Documentation rules

If you add a major capability, update documentation too.

Examples:

- new provider support
- new env vars
- new Docker dependency
- new endpoint family

## Testing

Run tests before opening a contribution:

```bash
pytest
```

When possible, add tests for:

- success paths
- auth-sensitive behavior
- failure behavior
- provider factory selection
- API contract behavior

## Pull Request Checklist

Before submitting:

1. confirm the change fits the existing architecture
2. run tests
3. update docs if behavior changed
4. add config entries to `.env.example` if required
5. remove debug code and temporary prints
6. keep the PR focused

## What To Avoid

Please avoid:

- vendor lock-in inside routes or services
- large unrelated refactors mixed with small fixes
- adding placeholder scaffolding without implementation
- bypassing provider abstractions for convenience
- inflating the project with features that are not maintained

## Reporting Issues

Good issue reports include:

- what you expected
- what actually happened
- steps to reproduce
- environment details
- relevant logs or stack traces

## License

By contributing, you agree that your contributions will be distributed under the same license as this repository.
