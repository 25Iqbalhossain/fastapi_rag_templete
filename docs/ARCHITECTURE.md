# Architecture Guide: FastAPI RAG

This document provides a technical deep-dive into the design philosophy, layering, and patterns used in the **FastAPI RAG** ecosystem. It is intended for architects and lead developers who need to extend or audit the system.

---

## 🏛️ Architectural Goals

The system is engineered to solve the "Day 1" problem of AI development: moving from a prototype to a production-ready infrastructure.

1.  **Async-First Core:** Leverages Python's `asyncio` for non-blocking IO across Database, LLM, and Vector stores.
2.  **Strict Separation of Concerns:** Logic is isolated into layers to prevent the "Fat Controller" anti-pattern.
3.  **Provider-Interface Pattern:** Application logic depends on abstract interfaces, ensuring no vendor lock-in.
4.  **Operational Maturity:** Built-in support for Prometheus metrics, structured logging, and health checks.

---

## 🏗️ High-Level Layers

### 1. API Layer (`app/api/`)
*   **Role:** Entry points, request validation (Pydantic), and response shaping.
*   **Rule:** Routes must stay thin. They should only orchestrate services or modules.

### 2. Module Layer (`app/modules/`)
*   **Role:** High-level domain workflows that coordinate multiple services and providers.
*   **Key Modules:** 
    *   `RAG Module`: Handles chunking, embedding, and retrieval.
    *   `Agent Module`: Manages the registry and execution of specialized AI agents.

### 3. Service Layer (`app/services/`)
*   **Role:** Fine-grained business logic (e.g., Auth, Chunking, Parsing).
*   **Rule:** Reusable components that don't belong in a specific module.

### 4. Provider Layer (`app/providers/`)
*   **Role:** Infrastructure adapters. This is the only place where vendor-specific SDKs (e.g., Qdrant, OpenAI) are allowed.
*   **Pattern:** Each provider family has a `BaseInterface` and a `Factory`.

### 5. Persistence Layer (`app/db/`)
*   **Role:** SQLAlchemy models and the **Repository Pattern** for clean data access.

---

## 🤖 AI & Agentic Design

### The Agent Registry
The system uses a centralized `AgentManager` that allows for "Easy-Add" agent registration.
*   **BaseAgent:** An abstract interface ensuring consistent execution.
*   **Specialized Agents:** Pre-built implementations for SQL-querying, RAG-retrieval, and Tool-calling.

### Async Ingestion Pipeline
To handle large documents (PDFs) without blocking the API, we use a decoupled ingestion flow:
1.  **API:** Receives file, saves to storage, and creates a `Document` record in `PENDING` state.
2.  **Celery Worker:** Picks up the task, parses the file, chunks text, generates embeddings, and indexes into the Vector Store.
3.  **Status Tracking:** The `Document` model allows the frontend to poll for processing progress.

---

## 📊 Observability & DevOps

*   **Logging:** Structured JSON logs via `structlog` or standard logging with JSON formatting.
*   **Metrics:** `/metrics` endpoint serving Prometheus-compatible data for API latency, error rates, and task completion.
*   **Tracing:** Optional OpenTelemetry wiring for distributed tracing across services.
*   **Docker:** Multi-stage `Dockerfile` and a comprehensive `docker-compose` for local development.

---

## 🛠️ Extension Guidelines

1.  **Adding a Provider:** Implement the `BaseProvider` interface and update the factory.
2.  **Adding an Agent:** Inherit from `BaseAgent` and register it in the DI container.
3.  **Modifying RAG logic:** Edit `app/modules/rag/pipeline.py`.
4.  **Adding Background Tasks:** Define the task in `app/workers/tasks/` and ensure it is async-compatible.

---

## 📄 License

This architectural design is part of the FastAPI RAG project and is licensed under the [MIT License](../LICENSE).
