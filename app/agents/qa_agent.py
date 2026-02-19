# app/agents/qa_agent.py
import json
from typing import Any, Dict

from app.schemas.qa import QAReport
from app.services.llm.llm_factory import LLMFactory

SYSTEM_PROMPT = """You are a senior campaign QA reviewer ensuring marketing content meets quality, brand safety, and strategic alignment standards before it goes live.

Quality standards:
- Brand identity must be clearly recognisable — a reader should know whose ad this is without seeing a logo
- The brand's differentiator must come through in every asset — generic copy is a failure
- Each asset must be appropriate for its channel — wrong format or tone for a channel is a quality issue
- No content restriction violations, however minor
- Every asset must have a clear next step for the audience — vague or missing CTAs fail
- The content as a whole must plausibly achieve the stated campaign goal

Set "passed" to true only if there are zero critical issues.
Output valid JSON only — no markdown, no code fences, no commentary. Return exactly one JSON object."""


def _build_user_prompt(
    content: Dict[str, Any],
    brand_context: Dict[str, Any],
    strategy: Dict[str, Any],
    goal: str,
    target_audience: str,
) -> str:
    brand_name = brand_context.get("name", "")
    usp = brand_context.get("usp", "")
    tone = brand_context.get("tone", "")
    restrictions = []
    guidelines = brand_context.get("brand_guidelines") or {}
    if isinstance(guidelines, dict):
        restrictions = guidelines.get("content_restrictions", [])

    return f"""Review the following campaign content before it goes live.

BRAND NAME: {brand_name}
BRAND USP: {usp}
BRAND TONE: {tone}
CONTENT RESTRICTIONS: {json.dumps(restrictions)}

CAMPAIGN GOAL: {goal}
TARGET AUDIENCE: {target_audience}

PLANNED CHANNELS: {json.dumps(strategy.get("channels", []))}

CONTENT ASSETS:
{json.dumps(content.get("assets", []), indent=2)}

Evaluate whether this content would actually achieve the campaign goal with this audience.
For any issue found, be specific: which asset, what the problem is, and why it matters in practice.
Recommendations should be concrete and actionable.

Produce your review as a single JSON object.""".strip()


class QAAgent:
    def __init__(self) -> None:
        self.llm = LLMFactory.get_llm(agent_type="qa")

    def run(
        self,
        content: Dict[str, Any] | None,
        brand_context: Dict[str, Any] | None = None,
        strategy: Dict[str, Any] | None = None,
        goal: str = "",
        target_audience: str = "",
    ) -> QAReport:
        # Hard structural check first — no point calling LLM if content is empty
        if not content or not content.get("assets"):
            return QAReport(
                passed=False,
                issues=["No content assets were generated."],
                recommendations=["Re-run the content agent with a valid strategy."],
            )

        result: QAReport = self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=_build_user_prompt(
                content or {},
                brand_context or {},
                strategy or {},
                goal,
                target_audience,
            ),
            response_schema=QAReport,
        )
        return result