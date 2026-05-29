from app.core.config import Settings
from app.providers.llm.base import BaseLLMProvider
from app.providers.llm.echo import EchoLLMProvider
from app.providers.llm.ollama import OllamaProvider
from app.providers.llm.openai import OpenAIProvider


def get_llm_provider(settings: Settings) -> BaseLLMProvider:
    provider = settings.llm_provider.lower()
    if provider == "openai":
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required for openai provider")
        return OpenAIProvider(settings.openai_api_key, settings.openai_model)
    if provider == "ollama":
        return OllamaProvider(settings.ollama_base_url, settings.ollama_model)
    return EchoLLMProvider()