# app/graph/nodes/analytics_node.py
from app.agents.analytics_agent import AnalyticsAgent
from app.graph.node_wrapper import node_logger


@node_logger("analytics")
def analytics_node(state):
    agent = AnalyticsAgent()
    report = agent.run(content=state.get("content"))
    state["analytics"] = report.model_dump()
    return state
