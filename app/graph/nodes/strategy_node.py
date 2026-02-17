# app/graph/nodes/strategy_node.py
from app.services.llm.llm_factory import LLMFactory
from app.graph.node_wrapper import node_logger


llm = LLMFactory.get_llm(agent_type="strategy")


@node_logger("strategy")
def strategy_node(state):
    prompt = f"""
    Based on research:
    {state['research']}
    Create a growth strategy.
    """

    result = llm.generate(
        system_prompt="You are a CMO designing growth strategy.",
        user_prompt=prompt
    )

    state["strategy"] = result
    return state