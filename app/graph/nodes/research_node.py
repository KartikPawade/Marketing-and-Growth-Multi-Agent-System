# app/graph/nodes/research_node.py

from app.graph.node_wrapper import node_logger
from app.agents.research_agent import ResearchAgent


@node_logger("research")
def research_node(state):
    agent = ResearchAgent()

    research_output = agent.run(
        brand_context=state.get("brand_context", "")
    )

    # Node controls state mutation
    state["research"] = research_output.model_dump()

    return state