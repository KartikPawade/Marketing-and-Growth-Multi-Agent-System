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


SYSTEM_PROMPT = """You are a CMO designing a growth strategy. Your task is to produce structured strategy output in valid JSON only—no markdown, no code fences, no commentary.
Return exactly one JSON object."""


class StrategyAgent:
    def __init__(self) -> None:
        self.llm = LLMFactory.get_llm(agent_type="strategy")

    def run(self, research: dict | str | None) -> StrategyOutput:
        research_text = _research_text(research)
        user_prompt = f"""Based on the following market research, create a growth strategy.
Research:
{research_text}
Produce your strategy as a single JSON object.""".strip()

        result: StrategyOutput = self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_schema=StrategyOutput,
        )
        return result
