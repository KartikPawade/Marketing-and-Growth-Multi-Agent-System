# app/agents/content_agent.py
import json

from app.schemas.content import ContentOutput
from app.services.llm.llm_factory import LLMFactory


def _strategy_text(strategy: dict | str | None) -> str:
    if strategy is None:
        return ""
    if isinstance(strategy, dict):
        return json.dumps(strategy, indent=2)
    return str(strategy)


SYSTEM_PROMPT = """You are a performance marketing copywriter. Your task is to produce campaign content as valid JSON only—no markdown, no code fences, no commentary.

Return exactly one JSON object."""


class ContentAgent:
    def __init__(self) -> None:
        self.llm = LLMFactory.get_llm(agent_type="content")

    def run(self, strategy: dict | str | None) -> ContentOutput:
        strategy_text = _strategy_text(strategy)
        user_prompt = f"""Based on the following growth strategy, create campaign content assets.

Strategy:
{strategy_text}

Produce your output as a single JSON object.""".strip()

        result: ContentOutput = self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_schema=ContentOutput,
        )
        return result
