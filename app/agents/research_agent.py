# app/agents/research_agent.py
import json
from datetime import date
from typing import Any, Dict

from app.schemas.research import ResearchOutput
from app.services.llm.llm_factory import LLMFactory

SYSTEM_PROMPT = """You are a senior market research analyst with deep expertise in digital marketing and consumer behaviour.

Your task is to produce rigorous, grounded market research tailored to a specific brand AND campaign goal.
Output valid JSON only — no markdown, no code fences, no commentary. Return exactly one JSON object.

Quality standards:
- Market sizing must be grounded in cited sector benchmarks, not aspirational estimates
- Growth rates must reflect realistic CAGR figures for the sector (typically 8–25% for consumer tech/health)
- Competitive intelligence must go beyond surface positioning — identify exploitable gaps and weaknesses
- Insights must be actionable and directly tied to the campaign goal, not generic category observations
- All analysis must be forward-looking; do not reference past years as future milestones"""


def _build_user_prompt(brand_context: Dict[str, Any], goal: str, target_audience: str, budget: float) -> str:
    return f"""Conduct market research to support the following campaign.

TODAY'S DATE: {date.today().isoformat()}

BRAND CONTEXT:
{json.dumps(brand_context, indent=2)}

CAMPAIGN GOAL:
{goal}

CAMPAIGN TARGET AUDIENCE:
{target_audience}

CAMPAIGN BUDGET (USD):
{budget:,.2f}

Analyse the market landscape for this brand and campaign. Focus on:
- What the target audience needs that existing solutions are failing to deliver
- Where competitors are vulnerable given this campaign's goal
- What market conditions make this the right moment to act
- How the available budget shapes the realistic opportunity size

Produce your analysis as a single JSON object.""".strip()


class ResearchAgent:
    def __init__(self) -> None:
        self.llm = LLMFactory.get_llm(agent_type="research")

    def run(
        self,
        brand_context: Dict[str, Any],
        goal: str = "",
        target_audience: str = "",
        budget: float = 0.0,
    ) -> ResearchOutput:
        user_prompt = _build_user_prompt(brand_context, goal, target_audience, budget)
        result: ResearchOutput = self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_schema=ResearchOutput,
        )
        return result