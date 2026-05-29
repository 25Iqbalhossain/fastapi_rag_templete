# Architecture Guide: {{ project_name }}

This document explains the design philosophy and technical structure of your generated AI backend.

---

## 🏛️ Architectural Goals

Your project is built with an **Enterprise-First** mindset, prioritizing scalability, maintainability, and vendor neutrality.

*   **Async-First:** Non-blocking IO for all database, AI, and cache operations.
*   **Decoupled Infrastructure:** Business logic depends on interfaces, allowing you to swap LLMs or Vector DBs with minimal code changes.
*   **Scalable Tasks:** Heavy workloads (like PDF parsing and indexing) are handled by background workers.
*   **Observability:** Built-in Prometheus metrics and structured logging for production monitoring.

---

## 🏗️ Technical Layering

### API Layer (`app/api/`)
*   Contains your FastAPI routes.
*   **Rule:** Keep routes thin. Move complex logic to Services or Modules.

### Module Layer (`app/modules/`)
*   High-level domain logic that spans multiple services.
*   **RAG Module:** Orchestrates chunking, embedding, and vector search.
*   **Agent Module:** Manages the registration and execution of specialized AI agents.

### Provider Layer (`app/providers/`)
*   Adapters for third-party services (OpenAI, Qdrant, PostgreSQL).
*   **Goal:** Keep vendor-specific SDK calls isolated here.

### Persistence Layer (`app/db/`)
*   SQLAlchemy models and Repositories. Use repositories to centralize your queries.

---

## 🤖 AI & Agentic Design

### Agent Registry
Your project includes a centralized `AgentManager` that makes it easy to add new AI capabilities.
1.  **Define:** Create a new class inheriting from `BaseAgent`.
2.  **Register:** Add it to the container in `app/core/dependencies.py`.
3.  **Execute:** Call it via the `/api/v1/agents/{name}/execute` endpoint.

### Asynchronous Ingestion
To prevent API timeouts, document ingestion is decoupled:
1.  User uploads a file via `POST /rag/upload`.
2.  The API saves the file and returns a `PENDING` status.
3.  A **Celery Worker** picks up the file, parses it, and indexes it into the Vector Store.
4.  User can poll `GET /rag/documents` to see when the document is `COMPLETED`.

---

## 📊 Monitoring & DevOps

*   **Metrics:** Accessible at `/metrics` for Prometheus scraping.
*   **Health Checks:** `/health`, `/live`, and `/ready` for Kubernetes probes.
*   **Logging:** Centralized configuration in `app/core/logging.py`.

---

## 🛠️ How to Extend

1.  **New API:** Add a file in `app/api/v1/` and register it in `app/main.py`.
2.  **New DB Model:** Add to `app/db/models/`, run `alembic revision --autogenerate`, then `alembic upgrade head`.
3.  **New AI Tool:** Add a new Agent implementation in `app/modules/agents/implementations/`.

---

## 📄 License

This project is released under the [MIT License](../LICENSE).
