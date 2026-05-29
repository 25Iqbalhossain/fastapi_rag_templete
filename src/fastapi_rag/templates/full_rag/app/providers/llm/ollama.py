import httpx

from app.providers.llm.base import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):
    def __init__(self, base_url: str, model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    async def generate(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
            )
            response.raise_for_status()
            return response.json()["response"]
