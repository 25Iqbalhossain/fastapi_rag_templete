# User Guide: Building with FastAPI RAG

This guide provides a comprehensive onboarding path for developers using the **FastAPI RAG** template. It explains how to navigate the architecture, implement new features, and maintain production standards.

---

## 🧭 Architecture Navigation

The template follows a strict **Layered Architecture** to ensure that infrastructure and business logic remain decoupled.

### 1. `app/api/` (Routing)
*   **Purpose:** Define HTTP endpoints and validate incoming data (Pydantic).
*   **Standard:** Routes should be "thin." They only parse the request, call a Service or Module, and return a response.

### 2. `app/services/` (Business Logic)
*   **Purpose:** Fine-grained business rules (e.g., Auth, Document Parsing).
*   **Standard:** If a piece of logic is reusable and handles a single business concern, it belongs here.

### 3. `app/modules/` (Orchestration)
*   **Purpose:** High-level workflows that coordinate multiple services and providers.
*   **Current Modules:**
    *   `RAG Module`: The retrieval and generation pipeline.
    *   `Agent Module`: The extensible framework for AI agents.

### 4. `app/providers/` (Infrastructure)
*   **Purpose:** Adapters for external vendors (OpenAI, Qdrant, Redis).
*   **Standard:** All vendor-specific SDK calls must live here, hidden behind a base interface.

---

## 🤖 Working with AI Agents

The template includes an "Easy-Add" agent framework.

### How to Add a New Agent
1.  **Define Implementation:** Create a class in `app/modules/agents/implementations/` inheriting from `BaseAgent`.
2.  **Logic:** Implement the `async def run(...)` method.
3.  **Registration:** Open `app/core/dependencies.py` and add `agent_manager.register(MyNewAgent())`.

### Calling Agents via API
You can execute any registered agent using the centralized endpoint:
`POST /api/v1/agents/{agent_name}/execute?task=your_task_here`

---

## 📄 Advanced RAG: Document Management

Unlike basic templates, this system handles real files asynchronously.

### The Ingestion Flow
1.  **Upload:** `POST /api/v1/rag/upload` accepts `.pdf` and `.txt`.
2.  **Tracking:** The system returns a `Document` object with a `PENDING` status.
3.  **Processing:** A background worker (Celery) extracts text, chunks it, and indexes vectors.
4.  **Verification:** Poll `GET /api/v1/rag/documents` to check for `COMPLETED` or `FAILED` status.

---

## 🛠️ Feature Development Checklist

Follow this workflow to add a new feature (e.g., a "Project Management" module):

1.  **Schemas:** Define request/response models in `app/schemas/project.py`.
2.  **Persistence:** Create the SQLAlchemy model in `app/db/models/project.py`.
3.  **Repository:** Build the data access layer in `app/db/repositories/project_repository.py`.
4.  **Service:** Implement business rules in `app/services/project_service.py`.
5.  **API:** Expose the feature in `app/api/v1/projects.py`.
6.  **Wire Up:** Register the new router in `app/main.py`.
7.  **Test:** Add unit and integration tests in `tests/`.

---

## 🧪 Testing Standards

We prioritize behavior-driven testing. Your tests should simulate how a user interacts with the API.

*   **Integration Tests:** Test the full flow (e.g., Upload → Index → Query).
*   **Auth Tests:** Ensure protected routes correctly handle missing or invalid JWTs.
*   **Provider Mocks:** Use the `InMemory` test providers during CI to avoid external API costs.

---

## 📄 License

This guide is part of the FastAPI RAG project and is licensed under the [MIT License](../LICENSE).
