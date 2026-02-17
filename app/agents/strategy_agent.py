# app/agents/strategy_agent.py
import json

from app.schemas.strategy import StrategyOutput
from app.services.llm.llm_factory import LLMFactory


def _research_text(research: dict | str | None) -> str:
    if research is None:
        return ""
    if isinstance(research, dict):
        return json.dumps(research, indent=2)
    return str(research)


class StrategyAgent:
    def __init__(self) -> None:
        self.llm = LLMFactory.get_llm(agent_type="strategy")

    def run(self, research: dict | str | None) -> StrategyOutput:
        research_text = _research_text(research)
        prompt = f"""
        Based on research:
        {research_text}
        Create a growth strategy.
        """.strip()

        result: StrategyOutput = self.llm.generate(
            system_prompt="You are a CMO designing growth strategy.",
            user_prompt=prompt,
            response_schema=StrategyOutput,
        )
        return result
