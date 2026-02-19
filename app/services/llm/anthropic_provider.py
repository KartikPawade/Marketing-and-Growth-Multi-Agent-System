from pydantic import BaseModel

from app.core.settings import settings
import logging
from .base import BaseLLM

logger = logging.getLogger("anthropic_provider")

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
        response = self._client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=7048,
            response_format=response_schema,
        )
        usage = response.usage
        logger.info(
            f"LLM_CALL | tokens={usage.total_tokens} | "
            f"prompt_tokens={usage.prompt_tokens} | "
            f"completion_tokens={usage.completion_tokens}"
        )
        return response.choices[0].message.parsed
