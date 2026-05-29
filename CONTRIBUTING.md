# Contributing to FastAPI RAG

First off, thank you for considering contributing to **FastAPI RAG**! It’s people like you who make the AI developer ecosystem a better place.

This project is an **Enterprise Template Generator**. Contributions should aim to improve the quality, security, and scalability of the generated backends.

---

## 🏗️ Repository Architecture

Understanding the boundary between the **Generator** and the **Scaffold** is key:

*   **The Generator (`src/fastapi_rag/`):** The CLI and rendering logic that builds the project.
*   **The Template (`src/fastapi_rag/templates/full_rag/`):** The actual FastAPI code that users receive.

> **Note:** If you want to improve the RAG pipeline or Agent logic, you should primarily edit the files in the `templates/` directory.

---

## 📜 Principles & Standards

We maintain a high bar for "Production-Grade" code. Please adhere to these principles:

1.  **Real Implementations:** No placeholders. If a feature is added, it must be functional (e.g., real JWT, real SQL repositories).
2.  **Provider Abstraction:** Never tie business logic to a specific vendor. Always use the `providers/` interface.
3.  **Async-First:** All IO-bound operations (DB, LLM, Cache) must use `async/await`.
4.  **Security by Default:** Always follow OWASP best practices for FastAPI.

---

## 🛠️ Development Workflow

### 1. Environment Setup
```bash
git clone https://github.com/example/fastapi-rag.git
cd fastapi-rag
pip install -e .[dev]
```

### 2. Testing the Generator
```bash
pytest
```

### 3. Testing the Scaffold
To test changes to the generated code:
1. Generate a project: `fastapi-rag new test_app`
2. Enter the project: `cd test_app`
3. Run the scaffold's tests: `pytest` or `docker compose up --build`

---

## 🤝 Pull Request Process

1.  **Issue First:** For major changes, please open an issue first to discuss the architectural impact.
2.  **Atomic Commits:** Use [Conventional Commits](https://www.conventionalcommits.org/) (e.g., `feat:`, `fix:`, `docs:`).
3.  **Update Docs:** If you change template variables or provider logic, update `ARCHITECTURE.md` and `README.md`.
4.  **Quality Check:** Ensure all tests pass and your code follows the established linting patterns.

---

## 💡 Contribution Ideas

*   **New Providers:** Add support for Anthropic, Weaviate, or Azure AI Search.
*   **Advanced Agents:** Implement "Researcher" or "Code Interpreter" agents in the scaffold.
*   **DevOps:** Improve Helm charts or add Terraform modules to the `deployment/` folder.
*   **Observability:** Add deeper OpenTelemetry spans for RAG retrieval steps.

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
