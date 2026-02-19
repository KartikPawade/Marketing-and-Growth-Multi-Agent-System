# app/agents/content_agent.py
import json
from typing import Any, Dict

from app.schemas.content import ContentOutput
from app.services.llm.llm_factory import LLMFactory

SYSTEM_PROMPT = """You are a performance marketing copywriter who writes channel-native campaign content.

Quality standards:
- Every asset must feel like it was written by a human who understands that channel deeply
- The brand identity (name, USP, tone) must come through naturally — never forced or bolted on
- Respect all brand content restrictions without exception
- CTAs must create genuine urgency specific to the channel context, not generic instructions

Output valid JSON only — no markdown, no code fences, no commentary. Return exactly one JSON object."""


def _build_user_prompt(
    strategy: Dict[str, Any],
    brand_context: Dict[str, Any],
    goal: str,
    target_audience: str,
    budget: float,
) -> str:
    brand_name = brand_context.get("name", "the brand")
    usp = brand_context.get("usp", "")
    tone = brand_context.get("tone", "")
    restrictions = []
    guidelines = brand_context.get("brand_guidelines") or {}
    if isinstance(guidelines, dict):
        restrictions = guidelines.get("content_restrictions", [])
    channels = strategy.get("channels", [])

    return f"""Write campaign content assets for each channel in the strategy below.

BRAND NAME: {brand_name}
BRAND USP: {usp}
BRAND TONE: {tone}
CONTENT RESTRICTIONS: {json.dumps(restrictions)}

CAMPAIGN GOAL: {goal}
TARGET AUDIENCE: {target_audience}
BUDGET: ${budget:,.2f}

STRATEGY:
{json.dumps(strategy, indent=2)}

CHANNELS TO COVER: {json.dumps(channels)}

Write one content asset per channel. Each asset should feel native to its channel —
a TikTok script reads nothing like an email, which reads nothing like an app store description.
The brand identity and USP should be present in every asset but woven in naturally.

Produce your output as a single JSON object.""".strip()


class ContentAgent:
    def __init__(self) -> None:
        self.llm = LLMFactory.get_llm(agent_type="content")

    def run(
        self,
        strategy: Dict[str, Any] | None,
        brand_context: Dict[str, Any] | None = None,
        goal: str = "",
        target_audience: str = "",
        budget: float = 0.0,
    ) -> ContentOutput:
        result: ContentOutput = self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=_build_user_prompt(
                strategy or {},
                brand_context or {},
                goal,
                target_audience,
                budget,
            ),
            response_schema=ContentOutput,
        )
        return result