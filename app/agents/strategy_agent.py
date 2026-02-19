# app/agents/strategy_agent.py
import json
from datetime import date
from typing import Any, Dict

from app.schemas.strategy import StrategyOutput
from app.services.llm.llm_factory import LLMFactory

SYSTEM_PROMPT = """You are a CMO designing a data-driven growth strategy for a specific campaign.

Your strategy must directly serve the stated campaign goal, target audience, and budget.
Output valid JSON only — no markdown, no code fences, no commentary. Return exactly one JSON object.

Quality standards:
- Objectives must be measurable and achievable within the stated budget — not aspirational
- Tactics must be concrete, executable actions with implicit budget guidance — not vague directions
- Every recommended channel must earn its place based on where the target audience actually is
- All timeframes must be future-relative from today — never reference dates that have already passed
- The strategy must follow logically from the research findings; do not ignore competitive gaps identified"""


def _build_user_prompt(
    research: Dict[str, Any],
    brand_context: Dict[str, Any],
    goal: str,
    target_audience: str,
    budget: float,
) -> str:
    return f"""Design a campaign growth strategy using the inputs below.

TODAY'S DATE: {date.today().isoformat()}

BRAND CONTEXT:
{json.dumps(brand_context, indent=2)}

CAMPAIGN GOAL:
{goal}

CAMPAIGN TARGET AUDIENCE:
{target_audience}

CAMPAIGN BUDGET (USD): ${budget:,.2f}

MARKET RESEARCH:
{json.dumps(research, indent=2)}

Develop a strategy that turns the research findings into a clear path to the campaign goal.
Consider how the budget constrains and shapes the realistic approach.
All timeframes must be future-relative from today ({date.today().isoformat()}).

Produce your strategy as a single JSON object.""".strip()


class StrategyAgent:
    def __init__(self) -> None:
        self.llm = LLMFactory.get_llm(agent_type="strategy")

    def run(
        self,
        research: Dict[str, Any] | None,
        brand_context: Dict[str, Any] | None = None,
        goal: str = "",
        target_audience: str = "",
        budget: float = 0.0,
    ) -> StrategyOutput:
        result: StrategyOutput = self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=_build_user_prompt(
                research or {},
                brand_context or {},
                goal,
                target_audience,
                budget,
            ),
            response_schema=StrategyOutput,
        )
        return result