from pathlib import Path

from typer.testing import CliRunner

from fastapi_rag.cli.main import app


runner = CliRunner()


def test_cli_new_generates_project(monkeypatch, tmp_path: Path) -> None:
    answers = iter(["sampleapp", "echo", "qdrant", "postgresql", "redis"])
    monkeypatch.setattr("fastapi_rag.cli.main.Prompt.ask", lambda *args, **kwargs: next(answers))

    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["new", "sampleapp"])

    assert result.exit_code == 0
    assert (tmp_path / "sampleapp" / "app" / "main.py").exists()
    assert "Generated project:" in result.stdout
