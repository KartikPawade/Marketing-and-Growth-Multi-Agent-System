# app/graph/nodes/content_node.py
from app.services.llm.llm_factory import LLMFactory
from app.graph.node_wrapper import node_logger


llm = LLMFactory.get_llm(agent_type="content")

@node_logger("content")
def content_node(state):
    prompt = f"""
    Based on strategy:
    {state['strategy']}
    Create campaign content.
    """

    result = llm.generate(
        system_prompt="You are a performance marketing copywriter.",
        user_prompt=prompt
    )

    state["content"] = result
    return state