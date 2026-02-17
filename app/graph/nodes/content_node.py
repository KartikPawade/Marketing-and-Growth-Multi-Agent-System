# app/graph/nodes/content_node.py
from app.agents.content_agent import ContentAgent
from app.graph.node_wrapper import node_logger


@node_logger("content")
def content_node(state):
    agent = ContentAgent()
    content_output = agent.run(strategy=state.get("strategy"))
    state["content"] = content_output.model_dump()
    return state
