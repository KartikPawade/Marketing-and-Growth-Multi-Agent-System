from pydantic import BaseModel

from app.core.settings import settings

from .base import BaseLLM
from .structured import parse_structured_response, schema_instruction


class AnthropicProvider(BaseLLM):
    def __init__(self, model: str | None = None):
        import anthropic
        self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = model or settings.anthropic_model_default

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        response_schema: type[BaseModel],
    ) -> BaseModel:
        system_prompt = system_prompt + schema_instruction(response_schema)
        response = self._client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        content = response.content[0].text
        return parse_structured_response(content, response_schema)
