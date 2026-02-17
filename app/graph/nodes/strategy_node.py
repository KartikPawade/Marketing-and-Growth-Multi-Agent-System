# app/graph/nodes/strategy_node.py
from app.agents.strategy_agent import StrategyAgent
from app.graph.node_wrapper import node_logger


@node_logger("strategy")
def strategy_node(state):
    agent = StrategyAgent()
    strategy_output = agent.run(research=state.get("research"))
    state["strategy"] = strategy_output.model_dump()
    return state
