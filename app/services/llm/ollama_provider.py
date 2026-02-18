import logging

from openai import OpenAI
from pydantic import BaseModel

from app.core.settings import settings

from .base import BaseLLM
from .structured import parse_structured_response, schema_instruction

logger = logging.getLogger("ollama_provider")


class OllamaProvider(BaseLLM):
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
        response = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format=response_schema,  # pydantic model directly
            temperature=0.7,
            max_tokens=7048,
        )
        usage = response.usage
        logger.info(
            f"LLM_CALL | tokens={usage.total_tokens} | "
            f"prompt_tokens={usage.prompt_tokens} | "
            f"completion_tokens={usage.completion_tokens}"
        )
        
        return response.choices[0].message.parsed

