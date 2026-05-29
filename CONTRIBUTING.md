# Contributing

Thanks for contributing to `fastapi-rag`.

This repository is a **template generator**, not a single backend application. Contributions should improve one of these areas:

- generator behavior
- template quality
- provider architecture
- developer experience
- documentation
- test coverage

## Repository Model

The repository has two main responsibilities:

1. generate a backend project
2. define the backend project template

Where things live:

- generator code: `src/fastapi_rag/cli.py` and `src/fastapi_rag/generator/`
- generated project scaffold: `src/fastapi_rag/template/`
- generator tests: `tests/`

If you want to change the backend that users receive, edit files under:

- `src/fastapi_rag/template/`

If you want to change prompts, rendering, or CLI behavior, edit files under:

- `src/fastapi_rag/generator/`

## Principles

Please keep these principles in mind:

- prefer real implementations over placeholder scaffolding
- keep the architecture modular
- avoid vendor lock-in in business-facing layers
- protect separation between generator logic and generated app logic
- keep docs aligned with actual behavior

## Good Contribution Areas

High-value contributions include:

- new provider implementations
- better rendering behavior
- richer generator tests
- stronger generated-project defaults
- improved RAG behavior
- observability improvements
- packaging fixes
- onboarding documentation improvements

## Local Development

Install in editable mode:

```bash
pip install -e .
```

Run tests:

```bash
pytest
```

If you want to manually inspect the generator:

```bash
fastapi-rag new myapp
```

That will render a backend project into `./myapp`.

Then you can test the generated backend separately:

```bash
cd myapp
docker compose up --build
```

## Development Rules

### Generator rules

- keep rendering deterministic
- keep template variables explicit
- do not hardcode project-specific values in generated files
- avoid mixing CLI prompt logic with file rendering logic

### Template rules

- routes should stay thin
- business logic belongs in services or modules
- provider-specific code belongs in provider folders
- generated code should be production-minded, not tutorial-grade

### Documentation rules

If you change:

- template variables
- provider support
- CLI prompts
- generated file layout
- runtime behavior in the scaffold

then update the relevant docs too.

## Testing Expectations

At minimum, contributions should preserve:

- generator render correctness
- CLI generation flow
- template file presence

If you add generator behavior, add or update tests in:

- `tests/`

If you change the generated backend structure significantly, also consider whether the template’s internal test suite under:

- `src/fastapi_rag/template/tests/`

should be updated.

## Pull Request Checklist

Before opening a PR:

1. run `pytest`
2. confirm the generator still renders a valid project tree
3. update docs if behavior changed
4. keep changes focused
5. avoid leaving partial scaffolding behind

## What To Avoid

Please avoid:

- adding abstractions with no real use
- bypassing provider interfaces for convenience
- turning the repo back into a single concrete backend app at the root
- mixing unrelated refactors with targeted fixes
- adding docs that overclaim unsupported runtime behavior

## License

By contributing, you agree that your contributions will be distributed under the same repository license.
