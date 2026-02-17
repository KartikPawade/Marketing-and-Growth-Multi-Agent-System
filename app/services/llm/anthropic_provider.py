from app.core.settings import settings

from .base import BaseLLM


class AnthropicProvider(BaseLLM):
    def __init__(self, model: str | None = None):
        import anthropic
        self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = model or settings.anthropic_model_default

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = self._client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return response.content[0].text
