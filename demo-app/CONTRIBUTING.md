# Contributing to demo-app

This project follows a high standard for production-grade AI development. Please adhere to the following guidelines when contributing.

---

## 🛠️ Development Principles

1.  **Separation of Concerns:** Business logic belongs in **Services** or **Modules**, not in API routes.
2.  **Provider Pattern:** Do not call external SDKs (OpenAI, Pinecone) directly. Use or extend the `app/providers/` layer.
3.  **Async/Await:** All IO operations must be asynchronous.
4.  **Test-Driven:** Every new feature should include unit or integration tests.

---

## 🏗️ Adding New Capabilities

### Adding an AI Agent
1. Create a class in `app/modules/agents/implementations/`.
2. Inherit from `BaseAgent`.
3. Register the agent in `app/core/dependencies.py`.

### Adding a Data Model
1. Define the model in `app/db/models/`.
2. Create an Alembic migration: `alembic revision --autogenerate -m "description"`.
3. Apply migration: `alembic upgrade head`.

---

## 🧪 Quality Control

Before submitting a Pull Request:
*   Ensure all tests pass: `pytest`.
*   Verify Docker build: `docker compose build`.
*   Check that your code follows the existing style and type hints.

---

## 📄 License

This project is licensed under the MIT License.