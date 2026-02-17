# app/services/llm_service.py
"""
Backward-compatible wrapper (legacy).

Prefer using:
    from app.services.llm import LLMFactory
    llm = LLMFactory.get_llm(agent_type="research")
    llm.generate(...)
"""

from app.services.llm.llm_factory import LLMFactory


class LLMService:
    def __init__(self, agent_type: str = "default"):
        self._llm = LLMFactory.get_llm(agent_type=agent_type)

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        return self._llm.generate(system_prompt=system_prompt, user_prompt=user_prompt)
