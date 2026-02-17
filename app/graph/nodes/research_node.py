from app.graph.node_wrapper import node_logger
from app.schemas.research import ResearchOutput
from app.services.llm.llm_factory import LLMFactory

llm = LLMFactory.get_llm(agent_type="research")


@node_logger("research")
def research_node(state):
    prompt = """
    Conduct market research for:
    Brand Context: {brand_context}
    """.format(brand_context=state["brand_context"] or "").strip()

    result = llm.generate(
        system_prompt="You are a senior market research analyst.",
        user_prompt=prompt,
        response_schema=ResearchOutput,
    )
    # Store as dict so state stays JSON-friendly
    state["research"] = result.model_dump()
    return state