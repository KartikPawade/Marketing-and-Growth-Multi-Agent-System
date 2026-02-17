# app/graph/nodes/qa_node.py
def qa_node(state):
    state["qa_report"] = {
        "length": len(state["content"]),
        "checked": True
    }
    return state