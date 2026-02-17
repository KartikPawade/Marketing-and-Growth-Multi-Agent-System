# app/config.py
# Agent → provider/model mapping. Factory reads this to resolve LLM per agent.

AGENT_MODEL_MAP = {
    "research": {
        "provider": "ollama",
        "model": "llama3",
    },
    "strategy": {
        "provider": "ollama",
        "model": "llama3",
    },
    "content": {
        "provider": "ollama",
        "model": "llama3",
    },
}
