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

Output rules:
- summary: One string—executive summary of the growth strategy.
- objectives: An array of strings only, e.g. ["Increase MQLs by 20%", "Improve lead quality"]. Each objective is one string—not objects with value/currency or other keys.
- tactics: An array of strings only, e.g. ["Launch ABM campaigns", "Optimize landing pages"]. Tactical recommendations as plain strings.
- channels: An array of strings only, e.g. ["LinkedIn", "Email", "Web"]. Recommended channels as plain strings.

Return exactly one JSON object with these four keys. All of objectives, tactics, and channels must be arrays of strings—never a single object or mixed types."""


class StrategyAgent:
    def __init__(self) -> None:
        self.llm = LLMFactory.get_llm(agent_type="strategy")

    def run(self, research: dict | str | None) -> StrategyOutput:
        research_text = _research_text(research)
        user_prompt = f"""Based on the following market research, create a growth strategy.

Research:
{research_text}

Produce your strategy as a single JSON object with: summary (string), objectives (array of strings), tactics (array of strings), channels (array of strings). Each of objectives, tactics, and channels must be an array of strings—e.g. ["Item 1", "Item 2"]—not single objects or numbers.""".strip()

        result: StrategyOutput = self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_schema=StrategyOutput,
        )
        return result
