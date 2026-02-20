# 🚀 Multi-Agent Marketing & Growth System

> **An autonomous AI pipeline that takes a brand and a campaign goal — and outputs a fully researched, strategized, written, QA'd, and analytics-forecasted marketing campaign. Zero human intervention required between steps.**

---

## 🧩 The Problem It Solves

Marketing campaigns require a chain of specialists — researcher, strategist, copywriter, compliance reviewer, analyst — each handing off manually, inconsistently, and slowly. Most AI tools patch one step. None of them connect the chain.

This system replaces the entire workflow. One brief in, one complete campaign out — researched, strategized, written, QA-gated, and analytics-forecasted autonomously. Brand memory compounds across every run.

Given a brand and a campaign brief, it autonomously:

1. **Researches** the market using live web search and competitor intelligence
2. **Designs a strategy** grounded in that research and the brand's historical memory
3. **Writes channel-native content** (LinkedIn posts, emails, ads — each native to its channel)
4. **QA-reviews** every asset against brand guidelines, blocking anything that violates them
5. **Forecasts performance analytics** including impressions, CTR, conversions, and budget allocation per channel
6. **Publishes** the campaign to the database with full auditability

Each step is an **autonomous AI agent** — specialized, tool-equipped, and orchestrated by a **LangGraph state machine**.

---

## 🏗️ System Workflow for Brand Campaign

<img width="3000" height="1220" alt="agent_pipeline (2)" src="https://github.com/user-attachments/assets/10b13425-b188-42b9-905e-3edf89304fe4" />

---

## 🤖 The Agent Pipeline

| Agent | Tools(Optional Use) | LLM Calls | Output Schema(Pydantic Validated) |
|---|---|---|---|
| Research | `web_search`, `serper_competitor_lookup` | Multi-step (ReAct tool loop) | `ResearchOutput` |
| Strategy | `get_brand_memory`, `get_past_campaigns`, `get_brand_guidelines` | Multi-step (ReAct tool loop) | `StrategyOutput` |
| Content | `get_brand_guidelines`, `get_brand_tone` | Multi-step (ReAct tool loop) | `ContentOutput` |
| QA | None (reasoning only) | Single | `QAReport` |
| Analytics | None (reasoning only) | Single | `AnalyticsReport` |

---

## ✨ Key Features

**⚛ ReAct Agent Flow** — Agents follow Reason → Act → Observe, invoking tools iteratively before producing output. No single-pass guessing — each agent works like a human expert would.

**🛠 Isolated Tool Registries** — Each agent has a strictly scoped toolset. Cross-domain tool calls are impossible by design. Hallucinated tool names return structured errors the agent reasons around.

**✅ Pydantic v2 Validated I/O** — Every agent input and output is a typed Pydantic model. LLMs return strict JSON; malformed responses surface as API errors, never propagate silently downstream.

**🗂 Single Shared Graph State** — All 6 nodes share one `CampaignState` TypedDict. Data flows automatically — research into strategy, strategy into content — with conditional routing handled declaratively by LangGraph.

**🧠 Context Management** — Each agent receives only the context slice relevant to its task. No agent sees the full accumulated history, keeping prompts focused and preventing token overflow. 
- Tools like Web search results from Tavily are also trimmed at the source before being passed into the agent, cutting noise and preserving context budget.

**🔀 LLM Agnostic** — `LLMFactory` resolves provider and model per agent from a single config map. Swap any agent from GPT-4o to Claude to local Ollama in one line. Full offline support included.

**⚙️ Conditional Pipeline Routing** — The QA node uses LangGraph's conditional edges. If zero critical issues → continue to publish. Any critical issues → pipeline halts entirely. Recommendations are logged but never block publishing (they're advisory, not blocking).

---

## 📊 LangSmith Trace

<img width="1543" height="901" alt="Langsmith trace v2" src="https://github.com/user-attachments/assets/45edff50-23e5-43ad-a113-876966a53a2b" />

---

## 🤖 Agents Explained

### 1. 🔍 Research Agent
- Calls **Tavily** (semantic web search) and **Serper** (Google Search API) for live market data
- Gathers competitor intelligence, trend signals, and audience insights
- Outputs structured research JSON fed directly into the strategy agent

### 2. 📊 Strategy Agent
- Consumes research output + brand memory (past campaigns, guidelines, insights)
- Designs a data-driven campaign strategy: objectives, channels, tactics, timeframes
- Uses `get_brand_memory` and `get_past_campaigns` tools to ensure brand continuity
- Explicitly constrained: no aspirational fluff — only measurable, budget-realistic objectives

### 3. ✍️ Content Agent
- Writes channel-native assets (copy varies dramatically per channel — TikTok ≠ email ≠ ad)
- Respects brand tone, USP, and content restrictions via `get_brand_guidelines` / `get_brand_tone` tools
- Uses multi-step tool calling (up to 4 steps) before producing final JSON output

### 4. 🔎 QA Agent
- Reviews every content asset against 5 quality dimensions:
  - Brand identity without name-dropping
  - USP clarity
  - Channel-native format/tone
  - Content restriction compliance
  - CTA specificity and goal alignment
- **Hard gate**: critical issues block publishing and halt the pipeline

### 5. 📈 Analytics Agent
- Forecasts impressions, clicks, CTR, conversion rate, and budget allocation per channel
- Arithmetically consistent channel-level breakdowns
- Returns structured `AnalyticsReport` for storage and display

### 6. 📤 Publish Node
- Persists finalized campaign (strategy + content + QA report + analytics) to MongoDB
- Associates campaign with brand for historical memory and future strategy improvement

---

## 🛠 Tools Explained

### Research Agent Tools

- **`web_search`** — Calls Tavily's semantic search API for live market trends, audience signals, and industry news. Results are trimmed before injection to preserve context budget.
- **`serper_competitor_lookup`** — Hits the Serper Google Search API to pull real-time competitor positioning, messaging, and share of voice signals.

### Strategy Agent Tools

- **`get_brand_memory`** — Fetches the brand's full memory from MongoDB: past campaign IDs, accumulated insights, and brand guidelines. Always called first — constrains every strategic decision.
- **`get_past_campaigns`** — Retrieves historical campaign records for the brand. Lets the strategy agent build on what worked and avoid repeating what didn't.
- **`get_brand_guidelines`** — Loads preferred channels, visual style rules, and hard content restrictions. Strategy never recommends a tactic that violates these.

### Content Agent Tools

- **`get_brand_guidelines`** — Pulls content restrictions and channel preferences before writing a single word. Non-negotiable constraints — violations are caught by QA regardless.
- **`get_brand_tone`** — Retrieves the brand's tone of voice, USP, and target audience. Ensures every asset sounds like the brand, not a generic AI output.

---

## 📂 Project Structure

```
├── app/
│   ├── main.py                    # FastAPI app, middleware, router registration
│   ├── config.py                  # Agent → provider/model mapping
│   ├── core/
│   │   ├── settings.py            # Pydantic settings (env-driven)
│   │   └── logging.py             # Structured logging setup
│   ├── api/
│   │   ├── routes_brand.py        # CRUD: brands
│   │   ├── routes_campaign.py     # CRUD: campaigns (nested under brands)
│   │   └── routes_analytics.py    # Analytics endpoints
│   ├── agents/
│   │   ├── research_agent.py      # Market research + competitor intel
│   │   ├── strategy_agent.py      # Campaign strategy generation
│   │   ├── content_agent.py       # Multi-channel content writing
│   │   ├── qa_agent.py            # Content quality & compliance review
│   │   └── analytics_agent.py     # Performance forecasting
│   ├── graph/
│   │   ├── builder.py             # LangGraph pipeline definition + conditional routing
│   │   ├── state.py               # CampaignState TypedDict
│   │   └── nodes/                 # One node per agent (research, strategy, content, qa, publish, analytics)
│   ├── tools/
│   │   ├── research/              # web_search, serper_competitor_lookup
│   │   ├── strategy/              # get_brand_memory, get_past_campaigns, get_brand_guidelines
│   │   └── content/               # get_brand_guidelines, get_brand_tone
│   ├── services/
│   │   ├── brand_service.py       # Brand business logic
│   │   ├── campaign_service.py    # Campaign orchestration (triggers graph)
│   │   └── llm/
│   │       └── llm_factory.py     # Provider-agnostic LLM factory
│   ├── db/
│   │   ├── mongodb.py             # MongoDB client singleton
│   │   └── repositories/          # brand_repo, campaign_repo, analytics_repo
│   ├── memory/
│   │   └── brand_memory.py        # Brand memory read/write (persistent cross-campaign)
│   └── schemas/                   # Pydantic models: brand, campaign, strategy, content, analytics, qa
├── Frontend/
├── docker/
│   └── docker-compose.yml         # MongoDB + Redis services
├── requirements.txt
└── .env.example
```

---

## 🔌 API Reference

### Brands
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/brands` | List all brands |
| `POST` | `/brands` | Create brand with memory |
| `GET` | `/brands/{id}` | Get brand + full memory |
| `PUT` | `/brands/{id}` | Update brand context |
| `DELETE` | `/brands/{id}` | Delete brand + memory |

### Campaigns
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/brands/{brand_id}/campaigns` | List brand campaigns |
| `POST` | `/brands/{brand_id}/campaigns/` | **Trigger full AI pipeline** |
| `GET` | `/brands/{brand_id}/campaigns/{id}` | Get campaign with all agent outputs |
| `DELETE` | `/brands/{brand_id}/campaigns/{id}` | Delete campaign |

### Health
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Service health check |

---

## 🛠️ Tech Stack Deep Dive

### Backend
| Technology | Role |
|---|---|
| **LangGraph** | Stateful multi-agent orchestration with conditional routing |
| **FastAPI** | REST API framework , auto-documented via OpenAPI |
| **LangSmith** | Full pipeline tracing and observability |
| **Pydantic v2** | Schema validation across all agent I/O, API requests/responses |
| **MongoDB (PyMongo)** | Brand profiles, campaign history, memory storage |

### AI / LLM
| Technology | Role |
|---|---|
| **OpenAI GPT-4o-mini** | Default agent model (all 5 agents configurable independently) |
| **Anthropic Claude** | Alternate provider, agent-level configurable |
| **Ollama** | Local LLM fallback (llama3.1:8b) — full offline capability |
| **LLMFactory** | Provider-agnostic factory pattern — swap LLMs per agent with one config change |
| **Tavily** | Semantic web search for research agent |
| **Serper** | Google Search API for competitor lookup |

---

## 🚀 Setup & Running

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (for MongoDB + Redis)

### 1. Start Infrastructure
```bash
docker compose -f docker/docker-compose.yml up -d
```

### 2. Backend
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # Fill in API keys
uvicorn app.main:app --reload
# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### 3. Frontend (WSL recommended on Windows)
```bash
cd Frontend
npm install
npm run dev
# UI available at http://localhost:5173
```

---

## 🔑 Environment Variables

```bash
# LLM Providers (configure at least one)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
OLLAMA_BASE_URL=http://localhost:11434/v1   # For local LLMs

# Search tools
TAVILY_API_KEY=tvly-...
SERPER_API_KEY=...

# Infrastructure
MONGODB_URI=mongodb://localhost:27017
REDIS_URL=redis://localhost:6379/0

# Observability
LANGSMITH_API_KEY=...
LANGSMITH_TRACING=true
```

---

## 💡 What Makes This Stand Out

- **End-to-end autonomous pipeline** — not just an LLM wrapper. Real agents with tools, memory, and conditional logic.
- **Production-grade code structure** — repository pattern, service layer, Pydantic schemas throughout, environment-driven config, structured logging.
- **Graceful degradation** — works with OpenAI, Anthropic, or a fully local Ollama stack. Designed for real-world deployment constraints.
- **Agent specialization** — each agent has a distinct system prompt, tool set, and output schema. No monolithic "do everything" prompt.
- **Memory that compounds** — brand memory persists and improves across campaigns, making it genuinely more useful over time.
- **Observable by design** — LangSmith tracing gives full visibility into every LLM call, tool use, and routing decision across the pipeline.

---
---

*Built with FastAPI · LangGraph · LangChain · React · MongoDB · Docker*
