# app/agents/research_agent.py

from app.schemas.research import ResearchOutput
from app.services.llm.llm_factory import LLMFactory


class ResearchAgent:
    def __init__(self) -> None:
        self.llm = LLMFactory.get_llm(agent_type="research")

    def run(self, brand_context: str) -> ResearchOutput:
        prompt = f"""
        Conduct market research for:
        Brand Context: {brand_context}
        """.strip()

        result: ResearchOutput = self.llm.generate(
            system_prompt="You are a senior market research analyst.",
            user_prompt=prompt,
            response_schema=ResearchOutput,
        )

        # STRICT: must return validated Pydantic model
        return result