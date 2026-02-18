# app/agents/research_agent.py

from typing import Dict, Any
from app.schemas.research import ResearchOutput
from app.services.llm.llm_factory import LLMFactory


SYSTEM_PROMPT = """You are a senior market research analyst. Your task is to produce structured market research in valid JSON only—no markdown, no code fences, no commentary.

Return exactly one JSON object."""


class ResearchAgent:
    def __init__(self) -> None:
        self.llm = LLMFactory.get_llm(agent_type="research")

    def run(self, brand_context: Dict[str, Any]) -> ResearchOutput:
        user_prompt = f"""Conduct market research for the following brand.

Brand context:
{brand_context}

Produce your analysis as a single JSON object.""".strip()

        result: ResearchOutput = self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_schema=ResearchOutput,
        )
        return result