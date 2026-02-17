# app/services/llm/base.py
from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseLLM(ABC):
    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        response_schema: type[BaseModel],
    ) -> BaseModel:
        """
        Generate from the LLM. The model is instructed to return JSON matching
        response_schema; the response is parsed and validated into an instance of it.
        """
        pass
