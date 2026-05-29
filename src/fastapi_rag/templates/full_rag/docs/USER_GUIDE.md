# User Guide

This guide explains how to use this template if you are a junior developer, intern, or any engineer who is new to modular backend architecture.

The goal is simple:

- understand what each folder does
- know where to add your code
- avoid breaking the template structure
- ship features with confidence

If you read this file carefully, you should be able to build your own backend features on top of this template without guessing where things belong.

## Start Here

Before writing code, understand one important rule:

This template already solves infrastructure problems for you.

That means you usually do not need to build:

- auth from scratch
- database connection logic
- Redis connection logic
- Celery setup
- JWT token creation
- vector database setup
- request logging middleware
- health endpoints

Your job is mostly to add product-specific business logic on top of the existing foundation.

## What This Template Already Gives You

The template includes working implementations for:

- FastAPI app startup
- JWT auth
- protected routes
- SQLAlchemy async DB layer
- Alembic migrations
- Redis-style cache abstraction
- Celery queue integration
- vector store abstraction
- RAG pipeline
- logging and metrics
- Docker-based local development

You should reuse these pieces instead of creating parallel versions.

## Folder Guide

This section explains the main folders in plain language.

### `app/api/`

This folder contains HTTP route files.

Use it when you need to create or update API endpoints such as:

- `GET /projects`
- `POST /documents`
- `DELETE /conversations/{id}`

Route files should stay thin. They should accept requests, call services, and return responses.

Do not put heavy business logic here.

### `app/core/`

This folder contains application-wide infrastructure:

- settings
- middleware
- auth helpers
- dependency injection
- logging
- exception handling

If something affects the whole app, it probably belongs here.

Examples:

- adding a new environment variable
- changing middleware behavior
- changing how services are created

### `app/db/`

This folder contains database logic:

- models
- repositories
- session setup
- migrations

Use this folder when you need to store or query data.

### `app/services/`

This is where business logic should usually live.

Examples:

- creating a project
- validating access to a document
- sending an invitation
- handling business rules before writing to the database

If your route starts becoming too smart, move that logic into a service.

### `app/modules/`

This folder is for larger workflows that combine multiple services or providers.

Examples:

- RAG pipeline
- ingestion pipeline
- workflow orchestration
- agent execution

Use a module when the feature is bigger than one small service.

### `app/providers/`

This folder contains pluggable integrations.

Current provider groups:

- `database`
- `cache`
- `queues`
- `llm`
- `vectorstores`

Use this folder if you are integrating a new external platform or infrastructure vendor.

Examples:

- add a new LLM provider
- add a new vector database
- add a new queue backend

### `app/schemas/`

This folder contains request and response models.

Use it for:

- request body validation
- response models
- typed API contracts

### `app/workers/`

This folder contains background task logic.

Use it for work that should not block the API request:

- indexing documents
- sending emails
- processing uploads
- generating reports

### `tests/`

This folder contains tests.

When you add a feature, add or update tests here.

## How To Build a Feature Correctly

Use this order when adding a new feature:

1. define the API request and response schemas
2. create the database model if data must be stored
3. create a repository for DB access
4. create a service for business logic
5. create an API route that calls the service
6. add tests

This is the safest way to keep the code clean.

## Example Feature: Build a Projects API

Let’s say your product needs `projects`.

You would create:

1. `app/db/models/project.py`
2. `app/db/repositories/project_repository.py`
3. `app/schemas/project.py`
4. `app/services/project_service.py`
5. `app/api/v1/projects.py`
6. update `app/main.py` to include the new router
7. `tests/test_projects.py`

## What Goes In Each File

### Model

The model describes how data is stored in the database.

Example fields:

- `id`
- `name`
- `owner_id`
- `created_at`

### Repository

The repository performs database queries.

Examples:

- get a project by ID
- list all projects for a user
- create a project
- delete a project

Repository rule:

Keep repositories focused on database access only.

### Service

The service applies business rules.

Examples:

- check that the current user owns the project
- prevent duplicate names
- validate project state before deletion

Service rule:

Put decision-making logic here, not in routes.

### Route

The route handles HTTP.

Examples:

- read request data
- call the service
- return JSON response
- enforce authentication

Route rule:

Keep routes small and easy to read.

## Example: Protected Route

Use `get_current_user` when a route requires authentication.

```python
from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.db.models.user import User

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])


@router.get("/")
async def list_projects(current_user: User = Depends(get_current_user)) -> dict[str, str]:
    return {"user_email": current_user.email}
```

If a route should only work for logged-in users, use this pattern.

The example above uses the default `API_PREFIX=/api/v1`. In this template, the real route files read the prefix from settings, so project code should follow that pattern when you wire production routes.

## Example: Service Pattern

This is the mindset you should use:

- route receives request
- service applies business logic
- repository talks to the database

That separation makes the system easier to test and maintain.

## How To Add a New Environment Variable

If your feature needs configuration:

1. add the setting to [app/core/config.py](/home/iqbal-ai/Downloads/industry_ai_backend_template/app/core/config.py)
2. add it to [.env.example](/home/iqbal-ai/Downloads/industry_ai_backend_template/.env.example)
3. use the setting through dependency injection or `get_settings()`

Do not hardcode secrets, URLs, or API keys inside services or routes.

## How To Add a New Provider

Use providers when the feature depends on an external service or infrastructure vendor.

Examples:

- new LLM
- new vector database
- new cache engine
- new queue backend

Steps:

1. choose the correct provider group in `app/providers/`
2. create a new provider class
3. implement the same base interface
4. update that provider group’s factory
5. add required settings to `app/core/config.py`
6. add env vars to `.env.example`

Important rule:

Do not call a vendor SDK directly from routes or business services if the project already has a provider layer for that concern.

## How To Work With the RAG Pipeline

The RAG workflow is in [app/modules/rag/pipeline.py](/home/iqbal-ai/Downloads/industry_ai_backend_template/app/modules/rag/pipeline.py).

The current flow is:

1. split document into chunks
2. embed each chunk
3. store vectors in the configured vector store
4. search similar chunks for a user query
5. build a prompt from retrieved context
6. generate an answer with the configured LLM provider

If you want to improve RAG, the common places to edit are:

- [app/services/chunking.py](/home/iqbal-ai/Downloads/industry_ai_backend_template/app/services/chunking.py)
- [app/services/embeddings.py](/home/iqbal-ai/Downloads/industry_ai_backend_template/app/services/embeddings.py)
- [app/modules/rag/pipeline.py](/home/iqbal-ai/Downloads/industry_ai_backend_template/app/modules/rag/pipeline.py)
- `app/providers/vectorstores/`
- `app/providers/llm/`

Common upgrades:

- metadata filtering
- better prompt templates
- reranking
- citations
- tenant-aware retrieval

## How To Use Background Jobs

Use background jobs when work is slow and should not block the API response.

Examples:

- document indexing
- batch import
- webhook processing
- export generation

Pattern:

1. route receives the request
2. route sends the job to the queue provider
3. worker processes the task
4. service or module handles the actual logic

Keep task functions thin. Move the real logic into services or modules.

## Local Development Workflow

Use this workflow every time you start working:

### Step 1. Configure environment

```bash
cp .env.example .env
```

Update values if needed.

### Step 2. Start the stack

```bash
docker compose up --build
```

### Step 3. Verify infrastructure

Open:

- `http://localhost:8000/health`
- `http://localhost:8000/ready`
- `http://localhost:8000/docs`

If `/ready` is not healthy, check the container logs first.

### Step 4. Build one feature at a time

Do not edit everything at once.

Good approach:

1. add one model
2. add one repository
3. add one service
4. add one route
5. test it

## Testing Guide

When you add a feature, usually add:

- one happy-path test
- one auth test if protected
- one validation test
- one failure-case test

Look at existing tests:

- [tests/test_auth.py](/home/iqbal-ai/Downloads/industry_ai_backend_template/tests/test_auth.py)
- [tests/test_health.py](/home/iqbal-ai/Downloads/industry_ai_backend_template/tests/test_health.py)
- [tests/test_rag.py](/home/iqbal-ai/Downloads/industry_ai_backend_template/tests/test_rag.py)
- [tests/test_metrics.py](/home/iqbal-ai/Downloads/industry_ai_backend_template/tests/test_metrics.py)

Try to test behavior the same way a user would experience it through the API.

## Common Mistakes Junior Developers Make

Avoid these:

- putting all logic in route files
- writing direct database queries inside routes
- hardcoding secrets or URLs in code
- creating duplicate auth logic
- adding new provider code outside the provider layer
- skipping tests because the feature “looks simple”
- modifying shared infrastructure without understanding where else it is used

## Safe Decision Rules

If you are unsure where code belongs, use these rules:

- if it handles HTTP, put it in `api/`
- if it stores or fetches DB data, put it in `db/repositories/`
- if it contains business rules, put it in `services/`
- if it orchestrates multiple steps, put it in `modules/`
- if it integrates a vendor or external system, put it in `providers/`
- if it affects the whole application, put it in `core/`

## What To Do Before Opening a Pull Request

Before sharing your work:

1. run tests
2. review your new files for naming consistency
3. check that routes stay thin
4. check that business logic lives in services or modules
5. confirm no secrets were hardcoded
6. confirm new settings were added to `.env.example`

## Recommended First Tasks for an Intern

If you are new to this repository, a good learning path is:

1. read [README.md](/home/iqbal-ai/Downloads/industry_ai_backend_template/README.md)
2. run the project with Docker
3. register a user and log in through `/docs`
4. read the auth route and auth service
5. read the RAG route and pipeline
6. build a simple `projects` feature
7. add tests for that feature

This will teach you the main architecture without overwhelming you.

## Final Advice

Do not try to redesign the template before you understand it.

First:

- use the existing patterns
- follow the existing folder structure
- build one feature fully
- test it

After you understand the flow, then improve the architecture if your product needs it.

That is the fastest and safest way to succeed with this template.
