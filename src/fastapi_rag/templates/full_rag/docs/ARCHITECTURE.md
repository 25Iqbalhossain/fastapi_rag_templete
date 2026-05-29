# Architecture Guide

This document explains how the template is structured and why the architecture is organized this way.

It is written for senior developers, leads, and contributors who need to understand the design decisions behind the template.

## Architectural Goals

The template is optimized for these goals:

- async-first application flow
- clear separation of concerns
- provider abstraction across infrastructure and AI integrations
- low-friction local development
- production-friendly observability
- easy extension by small teams

This project is intentionally not organized as a monolith with route handlers doing everything.

## High-Level Layers

The application is organized into these layers:

### API layer

Location:

- `app/api/`

Responsibilities:

- define HTTP endpoints
- validate requests
- call dependencies and services
- return structured responses

Routes should remain thin.

### Core layer

Location:

- `app/core/`

Responsibilities:

- settings and environment configuration
- security helpers
- middleware
- exception handling
- service container wiring

This layer owns cross-cutting runtime behavior.

### Persistence layer

Location:

- `app/db/`

Responsibilities:

- ORM models
- repositories
- DB session management
- migrations

This layer should not contain business workflows.

### Service layer

Location:

- `app/services/`

Responsibilities:

- reusable business logic
- orchestration of repositories and providers at a smaller scope

Use services when the logic is business-specific but not broad enough to be a full module.

### Module layer

Location:

- `app/modules/`

Responsibilities:

- higher-order workflows
- multi-step orchestration
- feature subsystems such as RAG

Modules are appropriate when multiple services or providers interact in one flow.

### Provider layer

Location:

- `app/providers/`

Responsibilities:

- infrastructure adapters
- third-party integrations
- swappable implementations hidden behind stable interfaces

This is the main mechanism used to avoid vendor lock-in.

## Provider Strategy

The template includes provider groups for:

- database
- cache
- queues
- llm
- vectorstores

Each group follows the same basic pattern:

1. a base abstract interface
2. one or more implementations
3. a factory that selects the provider from config

This is important because it keeps application logic stable while infrastructure choices change.

Example:

- the RAG pipeline depends on a vector store interface
- it does not depend on Qdrant-specific code

That means switching from Qdrant to PgVector should not require rewriting the pipeline.

## Dependency Container

The service container is built in:

- [app/core/dependencies.py](/home/iqbal-ai/Downloads/industry_ai_backend_template/app/core/dependencies.py)

This container creates and holds runtime dependencies such as:

- DB provider
- cache service
- vector store provider
- LLM provider
- queue provider
- RAG pipeline

The container is attached to `app.state` during application startup.

## Startup Philosophy

The template uses lifespan startup in:

- [app/main.py](/home/iqbal-ai/Downloads/industry_ai_backend_template/app/main.py)

Startup is dependency-aware:

- external systems are initialized during startup
- readiness state is tracked
- the application can optionally remain alive even if a dependency is unavailable

This allows `/live` and `/ready` to be operationally meaningful.

## RAG Architecture

The RAG pipeline lives in:

- [app/modules/rag/pipeline.py](/home/iqbal-ai/Downloads/industry_ai_backend_template/app/modules/rag/pipeline.py)

Current flow:

1. chunk document
2. embed chunks
3. insert chunk vectors into the selected vector store
4. retrieve top matches for a query
5. build a prompt
6. call the selected LLM provider
7. return answer plus retrieval matches

This architecture is intentionally modular so teams can improve each step independently.

Extension points:

- chunking
- embedding model
- retrieval strategy
- metadata filtering
- reranking
- prompt templates
- generation provider

## Authentication Architecture

Auth is intentionally simple and production-oriented:

- register
- login
- JWT access token
- protected route dependency

Key files:

- `app/api/v1/auth.py`
- `app/core/security.py`
- `app/services/auth.py`

The current setup is a strong base for future additions such as:

- refresh tokens
- RBAC
- organization membership
- API keys

## Observability Architecture

The observability layer includes:

- JSON logs
- request IDs
- exception logging
- Prometheus metrics
- optional OpenTelemetry tracing

Key files:

- `app/core/logging.py`
- `app/core/middleware.py`
- `app/observability/metrics.py`
- `app/observability/tracing.py`

This is intended to give teams an operational baseline from day one.

## Database Strategy

For relational persistence, the template uses:

- SQLAlchemy 2 async
- repositories
- Alembic migrations

This provides:

- clean persistence boundaries
- easy testing
- controlled schema changes

MongoDB settings are reserved for future persistence-layer expansion, but MongoDB is not currently a drop-in runtime replacement for the SQLAlchemy-backed auth and repository model.

## Why Repositories Exist

Repositories are used to centralize persistence queries.

Benefits:

- route handlers stay clean
- services do not duplicate query logic
- testing becomes easier
- future schema changes are easier to control

Without repositories, query logic tends to leak everywhere.

## Why Services and Modules Both Exist

This separation is deliberate.

Use a service when:

- the logic is focused
- it supports one business concern

Use a module when:

- the flow spans multiple providers or services
- the process has several coordinated steps

This prevents the service layer from turning into a dump of unrelated orchestration logic.

## Docker Philosophy

The local Docker stack is designed to give a working enterprise-style development environment quickly.

The default stack starts:

- FastAPI
- PostgreSQL
- Redis
- Qdrant
- Celery worker

This is the template’s opinionated happy path for local development.

Provider abstraction still allows the application logic to evolve away from those defaults later.

## Current Tradeoffs

This template is intentionally pragmatic.

It chooses:

- a strong default stack
- clear extension points
- moderate complexity

It does not try to solve every enterprise concern immediately.

Still likely needed for some production systems:

- RBAC
- tenant isolation
- rate limiting
- audit logging
- deployment manifests
- secret management integration

## How To Extend Safely

If you extend the template:

1. preserve layer boundaries
2. add provider logic only in provider folders
3. keep routes thin
4. keep business rules in services or modules
5. update docs when architecture changes

That keeps the project coherent as it grows.
