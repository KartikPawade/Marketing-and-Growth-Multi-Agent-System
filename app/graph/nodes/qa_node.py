# app/graph/nodes/qa_node.py
from app.agents.qa_agent import QAAgent
from app.graph.node_wrapper import node_logger


@node_logger("qa")
def qa_node(state):
    agent = QAAgent()
    report = agent.run(content=state.get("content"))
    state["qa_report"] = report.model_dump()
    return state
