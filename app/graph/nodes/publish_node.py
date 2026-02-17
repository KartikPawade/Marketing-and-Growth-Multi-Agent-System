# app/graph/nodes/publish_node.py
def publish_node(state):
    state["status"] = "published"
    return state