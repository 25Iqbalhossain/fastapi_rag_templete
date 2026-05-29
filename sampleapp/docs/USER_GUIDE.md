# User Guide: Building Production-Ready AI with sampleapp

This guide provides a comprehensive developer onboarding path. It moves from architectural theory to practical implementation, ensuring you can build, scale, and maintain a production-grade AI system using this template.

---

## 🧭 1. Architecture & Layering

The template follows a strict **Layered Architecture**. This separation is not just "good practice"—it is what allows you to swap infrastructure (like moving from Qdrant to PgVector) without touching your business logic.

### 🏛️ The Hierarchy of Code
1.  **API Layer (`app/api/`)**: Handlers for HTTP requests. Use Pydantic schemas for validation. **Rule:** No business logic here.
2.  **Service Layer (`app/services/`)**: Fine-grained business rules (e.g., `AuthService`, `ParsingService`). Use this for reusable logic.
3.  **Module Layer (`app/modules/`)**: Orchestration of complex, multi-step workflows like RAG or Agentic routing.
4.  **Provider Layer (`app/providers/`)**: The "Adapters." This is where you call external SDKs. **Rule:** Application code should only ever depend on the *Interface*, not the implementation.
5.  **Persistence Layer (`app/db/`)**: Data models and repositories. Use Repositories to keep your queries centralized and testable.

---

## 🤖 2. Intelligent Agent Orchestration

The template features a sophisticated **Agentic System** that goes beyond simple prompts.

### 🧠 The Orchestration Lifecycle
When a user sends a message through the `/chat` API, the following happens:
1.  **Context Loading:** The `ConversationRepository` retrieves previous messages to provide context.
2.  **Intelligent Routing:** The `Orchestrator` uses an LLM to analyze the query against the descriptions of all registered agents.
3.  **Agent Selection:** It dynamically selects the best tool (e.g., `SQLAgent` for data, `RAGAgent` for docs).
4.  **Execution:** The selected agent runs its specialized logic.
5.  **Persistence:** Both the query and the agent's output are saved to the `Message` history.

### 🛠️ How to Add a New Agent (Step-by-Step)
1.  **Implement Logic:** Create `app/modules/agents/implementations/my_agent.py`.
    ```python
    class MyAgent(BaseAgent):
        def __init__(self):
            super().__init__(name="my_agent", description="Handles specific task X")
        async def run(self, task: str, **kwargs):
            return {"result": "Done!"}
    ```
2.  **Register:** In `app/core/dependencies.py`, add `agent_manager.register(MyAgent())` to the `build_service_container` function.
3.  **Ready!** The `Orchestrator` will now automatically consider `my_agent` when routing user requests.

---

## 📄 3. Production RAG: Document Management

Production RAG requires more than just `text.split()`. It requires **Persistence** and **Asynchronicity**.

### ⚡ The Async Pipeline
*   **Upload:** Files are saved to local storage immediately, and a `Document` record is created with a `PENDING` status.
*   **Background Processing:** A Celery task extracts text (supporting PDF/Text), chunks it, and indexes it. This ensures your API stays responsive even during heavy ingestion.
*   **State Tracking:** Always check `doc.status` before querying. The `RAGAgent` automatically filters for processed documents.

---

## 🚀 4. "Day in the Life" Developer Workflow

To build a new feature (e.g., "AI Search for Projects"):

1.  **Database:** Define `Project` and `Document` models in `app/db/models/`.
2.  **Repository:** Create `ProjectRepository` in `app/db/repositories/`.
3.  **Service:** Write a `ProjectService` to handle creation/validation.
4.  **Agent:** Create a `ProjectSearchAgent` that uses the `ProjectRepository`.
5.  **API:** Expose a simple `POST /projects` endpoint.
6.  **Test:** Add an integration test in `tests/` that uploads a project doc and queries it via the Orchestrator.

---

## 🧪 5. Testing & Validation

A production system is only as good as its tests.
*   **Integration Tests:** Use the `tests/test_rag.py` as a template for testing the full upload -> process -> search flow.
*   **Mocks:** When testing agents, you can mock the `LLMProvider` to return deterministic JSON decisions.
*   **Manual Verification:** Use the included `docker-compose.yml` to run the full stack (Redis, Postgres, Qdrant) and verify via the `/docs` (Swagger) UI.

---

## 📄 License

This guide is part of the FastAPI RAG project and is licensed under the MIT License.