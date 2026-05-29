from app.providers.llm.base import BaseLLMProvider


class EchoLLMProvider(BaseLLMProvider):
    async def generate(self, prompt: str) -> str:
        context_marker = "Context:\n"
        question_marker = "\n\nQuestion:\n"
        context = ""
        question = prompt
        if context_marker in prompt and question_marker in prompt:
            context = prompt.split(context_marker, 1)[1].split(question_marker, 1)[0].strip()
            question = prompt.split(question_marker, 1)[1].strip()
        if not context:
            return f"Answer based on available data: {question}"
        return f"Based on retrieved context, the answer to '{question}' is: {context[:280]}"
