# app/config.py
# Agent → provider/model mapping. Factory reads this to resolve LLM per agent.

AGENT_MODEL_MAP = {
    "research": {
        "provider": "ollama",
        "model": "llama3.1:8b-instruct-q8_0",
    },
    "strategy": {
        "provider": "ollama",
        "model": "llama3.1:8b-instruct-q8_0",
    },
    "content": {
        "provider": "ollama",
        "model": "llama3.1:8b-instruct-q8_0",
    },
}
