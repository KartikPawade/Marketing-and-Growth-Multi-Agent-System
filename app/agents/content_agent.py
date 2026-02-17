# app/agents/content_agent.py
import json

from app.schemas.content import ContentOutput
from app.services.llm.llm_factory import LLMFactory


def _strategy_text(strategy: dict | str | None) -> str:
    if strategy is None:
        return ""
    if isinstance(strategy, dict):
        return json.dumps(strategy, indent=2)
    return str(strategy)


SYSTEM_PROMPT = """You are a performance marketing copywriter. Your task is to produce campaign content as valid JSON only—no markdown, no code fences, no commentary.

Output rules:
- assets: An array of objects. Each object has exactly four string keys:
  - headline: Primary headline (string).
  - body: Main body copy (string).
  - call_to_action: Call-to-action statement (string).
  - channel: Publishing channel name, e.g. "LinkedIn", "Email" (string).

Return exactly one JSON object with one key "assets", whose value is an array of such objects. Each asset must be an object with headline, body, call_to_action, and channel—all strings. No extra keys."""


class ContentAgent:
    def __init__(self) -> None:
        self.llm = LLMFactory.get_llm(agent_type="content")

    def run(self, strategy: dict | str | None) -> ContentOutput:
        strategy_text = _strategy_text(strategy)
        user_prompt = f"""Based on the following growth strategy, create campaign content assets.

Strategy:
{strategy_text}

Produce your output as a single JSON object with one key "assets". The value of "assets" must be an array of objects. Each object must have exactly: headline (string), body (string), call_to_action (string), channel (string). Create at least one asset per recommended channel; each asset is one object with those four keys.""".strip()

        result: ContentOutput = self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_schema=ContentOutput,
        )
        return result
