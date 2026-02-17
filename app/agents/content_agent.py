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


class ContentAgent:
    def __init__(self) -> None:
        self.llm = LLMFactory.get_llm(agent_type="content")

    def run(self, strategy: dict | str | None) -> ContentOutput:
        strategy_text = _strategy_text(strategy)
        prompt = f"""
        Based on strategy:
        {strategy_text}
        Create campaign content.
        """.strip()

        result: ContentOutput = self.llm.generate(
            system_prompt="You are a performance marketing copywriter.",
            user_prompt=prompt,
            response_schema=ContentOutput,
        )
        return result
