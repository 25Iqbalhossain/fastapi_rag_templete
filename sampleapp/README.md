# sampleapp

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?style=flat&logo=Python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-336791.svg?style=flat&logo=PostgreSQL&logoColor=white)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**sampleapp** is an enterprise-grade FastAPI foundation designed for high-performance AI applications, RAG systems, and Agentic workflows. Unlike simple boilerplates, this template provides a robust, modular architecture with production-ready implementations for authentication, background processing, and infrastructure abstraction.

---

## 🚀 Key Value Proposition

Most templates provide folder structures; **we provide infrastructure**.

*   **Intelligent Orchestration:** Advanced LLM-based routing system that dynamically selects the best agent (SQL, RAG, Tool) for any task.
*   **Stateful Chat History:** Built-in persistence for multi-turn conversations and message state management.
*   **Production-Ready RAG:** Asynchronous document ingestion with status tracking and background processing (Celery + Redis).
*   **Vendor Agnostic:** Swap LLMs (OpenAI/Ollama), Vector DBs (Qdrant/Chroma/PgVector), and Caches (Redis/Dragonfly) via stable Provider interfaces.
*   **Observability First:** Built-in Prometheus metrics, JSON logging, and OpenTelemetry tracing.

---

## 🛠️ Tech Stack & Features

### Core Infrastructure
- **FastAPI:** Modern, async-first web framework.
- **SQLAlchemy 2.0:** High-performance async ORM with the Repository pattern.
- **Celery:** Distributed task queue for heavy AI workloads.
- **Alembic:** Database migrations for safe schema evolution.

### AI & Agentic Capabilities
- **Intelligent Orchestration:** Dynamic LLM-based routing to select the best specialized agent for any task.
- **Conversation History:** State-aware multi-turn chat management with persistent message history.
- **Document Management:** Secure file upload (`.pdf`, `.txt`) with async status tracking.
- **RAG Pipeline:** Intelligent chunking, embedding, and vector search abstraction.
- **Agent Registry:** Centralized `AgentManager` supporting specialized agents:
    - `SQLAgent`: Intelligent database querying.
    - `RAGAgent`: Context-aware document QA.
    - `WeatherAgent`: External tool integration example.

### Security & DevOps
- **JWT Auth:** Robust Bearer authentication with password hashing.
- **Docker Ready:** Complete Compose stack for local development.
- **Cloud Native:** Ready for K8s deployment with structured health and readiness checks.

---

## 📂 Project Architecture

```text
app/
├── api/              # thin route handlers & request validation
├── core/             # centralized config, security, and DI container
├── db/               # persistence layer: models, repositories, sessions
├── modules/          # complex domain workflows: RAG & Agents
├── observability/    # monitoring: metrics, tracing, and logging
├── providers/        # infrastructure adapters (DB, Cache, LLM, VectorStore)
├── schemas/          # pydantic data models
├── services/         # business logic & external integrations
└── workers/          # background task definitions (Celery)
```

---

## ⚡ Quick Start

### 1. Environment Setup
```bash
cp .env.example .env
# Update SECRET_KEY, DATABASE_URL, and LLM_PROVIDER in .env
```

### 2. Launch Stack
```bash
docker compose up --build
```
*   **API Docs:** `http://localhost:8000/docs`
*   **Metrics:** `http://localhost:8000/metrics`
*   **Health:** `http://localhost:8000/health`

---

## 🤖 Building Agents

The framework is designed for extreme extensibility. Adding a new specialized agent takes minutes.

### Create a Custom Agent
```python
# app/modules/agents/implementations/coding_agent.py
from app.modules.agents.base import BaseAgent

class CodingAgent(BaseAgent):
    async def run(self, task: str, **kwargs) -> dict:
        # Implement your logic (e.g., code generation/execution)
        return {"code": "...", "result": "..."}
```

### Register & Execute
Register your agent in `app/core/dependencies.py` and call it via API:
```bash
curl -X POST http://localhost:8000/api/v1/agents/coding_agent/execute?task=Write_a_sort_algorithm
```

---

## 📖 API Documentation (Highlights)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/auth/login` | Obtain JWT Access Token. |
| `POST` | `/rag/upload` | Upload PDF/TXT for async indexing. |
| `GET` | `/rag/documents` | List uploaded documents and their status. |
| `POST` | `/chat/conversations` | Create a new intelligent chat session. |
| `POST` | `/chat/conversations/{id}/message` | Send a message to the Orchestrator. |
| `POST` | `/agents/{name}/execute` | Trigger a specific AI agent manually. |

---

## 🤝 Contributing

We welcome high-quality contributions! Please review our [CONTRIBUTING.md](CONTRIBUTING.md) for architectural guidelines and coding standards.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.