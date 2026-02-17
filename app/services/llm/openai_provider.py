from openai import OpenAI

from app.core.settings import settings

from .base import BaseLLM


class OpenAIProvider(BaseLLM):
    def __init__(self, model: str | None = None):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = model or settings.openai_model_default

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content or ""

