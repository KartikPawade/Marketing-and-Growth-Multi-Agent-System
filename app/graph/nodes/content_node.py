# app/graph/nodes/content_node.py
import json

from app.graph.node_wrapper import node_logger
from app.schemas.content import ContentOutput
from app.services.llm.llm_factory import LLMFactory

llm = LLMFactory.get_llm(agent_type="content")


def _strategy_text(strategy) -> str:
    if isinstance(strategy, dict):
        return json.dumps(strategy, indent=2)
    return str(strategy or "")


@node_logger("content")
def content_node(state):
    strategy_text = _strategy_text(state.get("strategy"))
    prompt = f"""
    Based on strategy:
    {strategy_text}
    Create campaign content.
    """
    result = llm.generate(
        system_prompt="You are a performance marketing copywriter.",
        user_prompt=prompt,
        response_schema=ContentOutput,
    )
    state["content"] = result.model_dump()
    return state