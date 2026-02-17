from app.graph.node_wrapper import node_logger

@node_logger("qa")
def qa_node(state):
    state["qa_report"] = {
        "length": len(state["content"]),
        "checked": True
    }
    return state