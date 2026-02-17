from app.graph.node_wrapper import node_logger

@node_logger("analytics")
def analytics_node(state):
    state["analytics"] = {
        "predicted_ctr": "4.5%",
        "predicted_cvr": "2.1%"
    }
    return state