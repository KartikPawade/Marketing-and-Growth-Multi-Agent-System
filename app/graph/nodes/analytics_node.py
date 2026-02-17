# app/graph/nodes/analytics_node.py
def analytics_node(state):
    state["analytics"] = {
        "predicted_ctr": "4.5%",
        "predicted_cvr": "2.1%"
    }
    return state