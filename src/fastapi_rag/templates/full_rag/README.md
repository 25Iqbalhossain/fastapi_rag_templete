# {{ project_name }}

Open source FastAPI backend template for AI products, internal copilots, RAG systems, and enterprise SaaS platforms.

This repository is not a toy boilerplate. It is a working backend foundation with real implementations for authentication, async database access, caching, queues, vector search, background jobs, observability, and RAG orchestration.

It is designed for teams that want to start with a clean, modular architecture instead of assembling infrastructure from scratch.

## Why This Template Exists

Most FastAPI templates stop at folder structure. They generate empty services, placeholder auth, or fake RAG examples that are not useful in a real system.

This template takes the opposite approach:

- real JWT authentication
- real async SQLAlchemy setup
- real Redis cache integration
- real Celery worker
- real Qdrant vector search
- real provider abstraction
- real health and readiness endpoints
- real Docker startup

The goal is simple: clone the template, adapt business logic, and ship faster without rewriting core backend infrastructure.

## What You Get

### Application foundation

- FastAPI app with lifespan-based startup
- async-first architecture
- modular package layout
- dependency injection through FastAPI dependencies
- production-oriented settings with `pydantic-settings`

### Security and auth

- `POST {API_PREFIX}/auth/register`
- `POST {API_PREFIX}/auth/login`
- JWT bearer authentication
- password hashing with `passlib`
- protected route example with current-user dependency

### Data and persistence

- SQLAlchemy 2 async session management
- repository pattern
- sample `User` model
- Alembic migration setup
- provider abstraction for SQL and Mongo-style backends

### AI and RAG

- document chunking
- embedding generation
- vector document storage abstraction
- retrieval pipeline
- prompt building
- LLM response generation
- `POST {API_PREFIX}/rag/query`

### Infrastructure integrations

- cache provider abstraction
- queue provider abstraction
- vector store provider abstraction
- LLM provider abstraction
- Redis and Dragonfly cache support pattern
- Celery queue support pattern
- Qdrant, Chroma, PgVector, Pinecone provider support pattern

### Observability and ops

- structured JSON logging
- request IDs
- exception handling
- trusted host middleware
- CORS middleware
- Prometheus metrics endpoint
- optional OpenTelemetry wiring
- `/health`, `/live`, `/ready`, `{METRICS_PATH}`

### Local development

- Dockerfile
- Docker Compose stack
- Postgres
- Redis
- Qdrant
- Celery worker

## Project Structure

```text
app/
├── api/              # HTTP routes
├── core/             # config, middleware, security, dependency wiring
├── db/               # ORM models, repositories, sessions
├── modules/          # higher-level domain workflows such as RAG
├── observability/    # metrics and tracing bootstrap
├── providers/        # pluggable providers: db, cache, queue, llm, vectorstores
├── schemas/          # request/response models
├── services/         # business services
├── workers/          # Celery app and tasks
└── main.py           # FastAPI application entrypoint
```

## Provider Architecture

The template is built around abstraction layers so application logic does not depend directly on a single infrastructure vendor.

Current provider families:

- `providers/database/`
- `providers/cache/`
- `providers/queues/`
- `providers/llm/`
- `providers/vectorstores/`

This means your RAG pipeline, services, and routes should depend on interfaces and factories, not on vendor-specific SDK calls.

Example:

- good: `vectorstore.similarity_search(...)`
- bad: direct `qdrant_client.query_points(...)` inside route handlers

## Supported Patterns

The template currently includes concrete implementations or extension points for:

- Databases: PostgreSQL, MySQL pattern
- Cache: Redis, Dragonfly pattern, in-memory test provider
- Queues: Celery, in-memory test provider
- LLMs: OpenAI, Ollama, echo fallback
- Vector stores: Qdrant, Chroma, PgVector, Pinecone, in-memory test provider

Some providers are ready for direct use now. Others are implemented as clean extension paths so teams can finish environment-specific setup without redesigning the architecture.

MongoDB configuration keys are present for future persistence-layer expansion, but MongoDB is not currently a drop-in runtime option for the SQLAlchemy-based auth and repository flow.

## Quick Start

### 1. Clone and configure

Copy the environment file:

```bash
cp .env.example .env
```

Review and update:

- `SECRET_KEY`
- `DATABASE_PROVIDER`
- `DATABASE_URL`
- `CACHE_PROVIDER`
- `REDIS_URL`
- `QUEUE_PROVIDER`
- `VECTOR_DB`
- `LLM_PROVIDER`

### 2. Start the stack

```bash
docker compose up --build
```

This starts:

- API server
- PostgreSQL
- Redis
- Qdrant
- Celery worker

### 3. Open the service

- API docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`
- Readiness: `http://localhost:8000/ready`
- Metrics: `http://localhost:8000/metrics` by default, configurable through `METRICS_PATH`

## Default API Endpoints

### Auth

- `POST {API_PREFIX}/auth/register`
- `POST {API_PREFIX}/auth/login`
- `GET {API_PREFIX}/auth/me`

### RAG

- `POST {API_PREFIX}/rag/documents`
- `POST {API_PREFIX}/rag/query`

### Health

- `GET /health`
- `GET /live`
- `GET /ready`
- `GET {METRICS_PATH}`

## Example Usage

### Register

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "full_name": "Example User",
    "password": "Password123"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "Password123"
  }'
```

### Query the RAG pipeline

Use the returned JWT token:

```bash
curl -X POST http://localhost:8000/api/v1/rag/query \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What information is stored in the indexed documents?",
    "limit": 3
  }'
```

## Configuration

Key environment variables:

### Core

- `PROJECT_NAME`
- `APP_ENV`
- `DEBUG`
- `AUTO_MIGRATE`
- `STARTUP_DEPENDENCY_TOLERANCE`

### Security

- `SECRET_KEY`
- `JWT_ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`

### Database

- `DATABASE_PROVIDER`
- `DATABASE_URL`
- `MYSQL_URL`

### Cache

- `CACHE_PROVIDER`
- `REDIS_URL`
- `DRAGONFLY_URL`

### Queue

- `QUEUE_PROVIDER`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`

### Vector store

- `VECTOR_DB`
- `VECTORSTORE_PROVIDER`
- `QDRANT_URL`
- `CHROMA_HOST`
- `PGVECTOR_URL`
- `PINECONE_API_KEY`

### LLM

- `LLM_PROVIDER`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `OLLAMA_BASE_URL`
- `OLLAMA_MODEL`

### Observability

- `OTEL_ENABLED`
- `OTEL_SERVICE_NAME`
- `OTEL_EXPORTER_OTLP_ENDPOINT`

See [.env.example](/home/iqbal-ai/Downloads/industry_ai_backend_template/.env.example) for the complete list.

Default docs and curl examples use `API_PREFIX=/api/v1` and `METRICS_PATH=/metrics`. If you change those settings, your route paths will change accordingly.

## Development Workflow

Recommended workflow for teams using this template:

1. start the infrastructure with Docker
2. confirm `/ready` is healthy
3. create your first domain model
4. create a repository for that model
5. create a service containing business rules
6. expose the service through a route
7. add tests before adding more features
8. extend the RAG or worker flows only when your domain requires them

## Testing

Current tests cover:

- auth flow
- health endpoints
- metrics endpoint
- RAG flow
- vector store factory selection

Run tests with:

```bash
pytest
```

## Who This Template Is For

This template is useful if you are building:

- internal AI tools
- multi-tenant SaaS backends
- document intelligence systems
- knowledge assistants
- AI-enabled workflow engines
- enterprise RAG services

It is especially useful for teams that want to enforce structure early:

- solo founders who want a serious starting point
- startup teams building their first AI backend
- agencies shipping client AI systems
- junior developers working under a clear architecture

## What This Template Does Not Try To Be

This template is not:

- a no-code generator
- a single-file demo app
- a frontend starter
- a complete product with billing, RBAC, and tenant management already solved

It gives you the backend foundation. You still need to implement your product-specific domain logic.

## Documentation

- Developer onboarding guide: [docs/USER_GUIDE.md](/home/iqbal-ai/Downloads/industry_ai_backend_template/docs/USER_GUIDE.md)
- Architecture guide: [docs/ARCHITECTURE.md](/home/iqbal-ai/Downloads/industry_ai_backend_template/docs/ARCHITECTURE.md)
- First feature tutorial: [docs/FIRST_FEATURE.md](/home/iqbal-ai/Downloads/industry_ai_backend_template/docs/FIRST_FEATURE.md)
- Contribution guide: [CONTRIBUTING.md](/home/iqbal-ai/Downloads/industry_ai_backend_template/CONTRIBUTING.md)
- License: [LICENSE](/home/iqbal-ai/Downloads/industry_ai_backend_template/LICENSE)

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](/home/iqbal-ai/Downloads/industry_ai_backend_template/CONTRIBUTING.md) before opening a PR.

## License

This project is released under the [MIT License](/home/iqbal-ai/Downloads/industry_ai_backend_template/LICENSE).
