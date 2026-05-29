# FastAPI RAG: Enterprise AI Backend Generator

[![PyPI version](https://img.shields.io/pypi/v/fastapi-rag.svg)](https://pypi.org/project/fastapi-rag/)
[![Python versions](https://img.shields.io/pypi/pyversions/fastapi-rag.svg)](https://pypi.org/project/fastapi-rag/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/example/fastapi-rag/actions/workflows/ci.yml/badge.svg)](https://github.com/example/fastapi-rag/actions)

**FastAPI RAG** is a sophisticated CLI tool designed to scaffold production-grade AI backends. Instead of assembly-required boilerplates, it generates a complete, modular ecosystem for RAG (Retrieval-Augmented Generation) applications, specialized AI agents, and high-performance SaaS platforms.

---

## 🌟 Why FastAPI RAG?

In the era of AI, the backend is more than just an API—it's an orchestrator. This tool generates a foundation that handles the complex "plumbing" of AI systems so you can focus on your domain logic.

*   **Intelligent Orchestration:** Advanced LLM-based routing and agent selection logic.
*   **Stateful AI Interactions:** Built-in persistence for multi-turn chat and conversation history.
*   **Production-Ready RAG:** Async document ingestion, status tracking, and background processing.
*   **Infrastructure Agnostic:** Pre-configured with swappable providers for LLMs, Vector DBs, and Caches.

---

## 🚀 Quick Start

Generate your enterprise-grade backend in seconds:

### 1. Installation
```bash
pip install fastapi-rag
```

### 2. Generate Project
```bash
fastapi-rag new my-ai-platform
```
The CLI will guide you through selecting your preferred stack (OpenAI vs. Ollama, Qdrant vs. PgVector, etc.).

### 3. Launch Development Stack
```bash
cd my-ai-platform
docker compose up --build
```
Your backend is now live at `http://localhost:8000` with full RAG and Agent capabilities.

---

## 📦 What's Included in the Box?

The generated project is a fully-functional ecosystem:

*   **Security:** JWT-based authentication with secure password hashing.
*   **AI Pipelines:**
    *   **Async Ingestion:** PDF/Text upload with background parsing and vector indexing.
    *   **Agentic Framework:** Modular registry for specialized AI agents (SQL, RAG, Web Search).
*   **Persistence:** Async SQLAlchemy 2.0 with the Repository pattern.
*   **Observability:** Integrated Prometheus metrics and JSON logging.
*   **Infrastructure:** Celery + Redis for background workflows and Qdrant for vector search.

---

## 🗺️ Roadmap & Supported Providers

| Category | Supported / Modeled Providers |
| :--- | :--- |
| **LLMs** | OpenAI, Ollama, Anthropic (Planned), Echo (Local Testing) |
| **Vector DBs** | Qdrant, Chroma, PgVector, Pinecone |
| **Databases** | PostgreSQL, MySQL |
| **Caching** | Redis, Dragonfly |
| **Queues** | Celery |

---

## 🛠️ Repository Development

### Local Setup
```bash
git clone https://github.com/example/fastapi-rag.git
cd fastapi-rag
pip install -e .[dev]
```

### Testing
```bash
pytest
```

### Build Distribution
```bash
python -m build
```

---

## 📚 Documentation

*   [**Architecture Overview**](docs/ARCHITECTURE.md) - Deep dive into the generator and scaffold design.
*   [**User Guide**](docs/USER_GUIDE.md) - How to use the CLI and customize templates.
*   [**First Feature Tutorial**](docs/FIRST_FEATURE.md) - Step-by-step guide to adding your first business rule.
*   [**Publishing Guide**](docs/PUBLISHING.md) - How to build and distribute the package.
*   [**Contributing**](CONTRIBUTING.md) - Our standards for pull requests and code style.

---

## 📄 License

This project is released under the [MIT License](LICENSE).
