# app/graph/nodes/strategy_node.py
import json

from app.graph.node_wrapper import node_logger
from app.schemas.strategy import StrategyOutput
from app.services.llm.llm_factory import LLMFactory

llm = LLMFactory.get_llm(agent_type="strategy")


def _research_text(research) -> str:
    if isinstance(research, dict):
        return json.dumps(research, indent=2)
    return str(research or "")


@node_logger("strategy")
def strategy_node(state):
    research_text = _research_text(state.get("research"))
    prompt = f"""
    Based on research:
    {research_text}
    Create a growth strategy.
    """

    result = llm.generate(
        system_prompt="You are a CMO designing growth strategy.",
        user_prompt=prompt,
        response_schema=StrategyOutput,
    )
    state["strategy"] = result.model_dump()
    return state