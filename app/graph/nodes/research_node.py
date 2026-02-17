from app.services.llm.llm_factory import LLMFactory
from app.graph.node_wrapper import node_logger

llm = LLMFactory.get_llm(agent_type="research")

@node_logger("research")
def research_node(state):
    prompt = f"""
    Conduct market research for:
    Brand Context: {state['brand_context']}
    """

    result = llm.generate(
        system_prompt="You are a senior market research analyst.",
        user_prompt=prompt
    )

    state["research"] = result
    return state