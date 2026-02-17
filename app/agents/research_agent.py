# app/agents/research_agent.py

from typing import Dict, Any
from app.schemas.research import ResearchOutput
from app.services.llm.llm_factory import LLMFactory


SYSTEM_PROMPT = """You are a senior market research analyst. Your task is to produce structured market research in valid JSON only—no markdown, no code fences, no commentary.

Output rules:
- target_audience: One string (3–500 chars) describing the demographic and psychographic profile.
- market_size: A single number (float), e.g. 1400 for 1.4 billion USD. No currency symbols or prose.
- growth_rate: A single number 0–100 (float), e.g. 25 for 25% annual growth. No units or prose.
- key_insights: An array of strings only, e.g. ["Insight one.", "Insight two."]. Each item is one string—not objects.
- competitors: An array of strings only, e.g. ["Company A", "Company B"]. Competitor names as plain strings—not objects.

Return exactly one JSON object with these five keys. All array fields must be arrays; all numeric fields must be numbers."""


class ResearchAgent:
    def __init__(self) -> None:
        self.llm = LLMFactory.get_llm(agent_type="research")

    def run(self, brand_context: Dict[str, Any]) -> ResearchOutput:
        user_prompt = f"""Conduct market research for the following brand.

Brand context:
{brand_context}

Produce your analysis as a single JSON object with: target_audience (string), market_size (number, USD millions), growth_rate (number, 0–100), key_insights (array of strings), competitors (array of strings). Use only the data and structure described above.""".strip()

        result: ResearchOutput = self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_schema=ResearchOutput,
        )
        return result