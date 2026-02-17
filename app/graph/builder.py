from langgraph.graph import StateGraph
from app.graph.state import CampaignState

from app.graph.nodes.research_node import research_node
from app.graph.nodes.strategy_node import strategy_node
from app.graph.nodes.content_node import content_node
from app.graph.nodes.qa_node import qa_node
from app.graph.nodes.publish_node import publish_node
from app.graph.nodes.analytics_node import analytics_node


def build_campaign_graph():
    graph = StateGraph(CampaignState)

    graph.add_node("research", research_node)
    graph.add_node("strategy", strategy_node)
    graph.add_node("content", content_node)
    graph.add_node("qa", qa_node)
    graph.add_node("publish", publish_node)
    graph.add_node("analytics", analytics_node)

    graph.set_entry_point("research")

    graph.add_edge("research", "strategy")
    graph.add_edge("strategy", "content")
    graph.add_edge("content", "qa")
    graph.add_edge("qa", "publish")
    graph.add_edge("publish", "analytics")

    graph.set_finish_point("analytics")

    return graph.compile()