import logging

from openai import OpenAI
from pydantic import BaseModel

from app.core.settings import settings

from .base import BaseLLM
from .structured import parse_structured_response, schema_instruction

logger = logging.getLogger("ollama_provider")


class OllamaProvider(BaseLLM):
    """
    Uses Ollama via its OpenAI-compatible endpoint.
    Default base URL: http://localhost:11434/v1
    """

    def __init__(self, model: str | None = None):
        self.client = OpenAI(
            base_url=settings.ollama_base_url,
            api_key=settings.ollama_api_key,
        )
        self.model = model or settings.ollama_model_default

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        response_schema: type[BaseModel],
    ) -> BaseModel:
        system_prompt = system_prompt + schema_instruction(response_schema)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
        )
        usage = response.usage
        logger.info(
            f"LLM_CALL | tokens={usage.total_tokens} | "
            f"prompt_tokens={usage.prompt_tokens} | "
            f"completion_tokens={usage.completion_tokens}"
        )
        content = response.choices[0].message.content or ""
        return parse_structured_response(content, response_schema)

