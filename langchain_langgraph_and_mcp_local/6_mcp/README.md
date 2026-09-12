# Week 6 — Model Context Protocol (MCP)
### Local Models Edition — by Abhishek
### A faithful port of `abhishek/agents/6_mcp`'s real `backend/` package

This edition ports the actual course code — `backend/accounts.py`,
`accounts_server.py`, `database.py`, `market.py`, `market_simulator.py`,
`mcp_servers.py`, `push_server.py`, `reset.py`, `templates.py`,
`tracers.py`, `traders.py`, `trading_floor.py`, `api.py`, and the real
`demo/` Gradio dashboard — with the **minimum edits needed to remove every
paid/signup dependency.** Most of these files needed *no* change at all.

## Day by day

- **`1_lab1.ipynb`** — MCP intro: fetch, filesystem, and memory servers,
  handed to a local-model agent via the OpenAI Agents SDK
- **`2_lab2.ipynb`** — build your own MCP server: the real
  `backend/accounts.py` + `backend/accounts_server.py` (SQLite-backed,
  Pydantic models, resources as well as tools)
- **`3_lab3.ipynb`** — context engineering: the real
  `backend/mcp_servers.py`'s `researcher_mcp_servers()` — Fetch, free
  search, and per-trader persistent memory (`mcp-memory-libsql`)
- **`4_lab4.ipynb`** — the real `backend/traders.py` `Trader` class,
  researching and trading through its MCP servers, logged via the real
  (already-local) `LogTracer`
- **`5_lab5.ipynb`** — capstone: the real `backend/trading_floor.py`
  scheduler running all four traders, watched through the real `demo/ui.py`
  Gradio dashboard

## What's genuinely unmodified (already free/local in the original)

- `database.py`, `market_simulator.py`, `accounts.py`, `accounts_server.py`,
  `accounts_client.py`, `reset.py`, `templates.py`, `tracers.py`, `api.py`
  — copied verbatim, zero changes
- `tracers.py`'s `LogTracer` — the original course **already** logs every
  trace/span locally to SQLite, not to any OpenAI platform service
- `demo/ui.py`, `demo/util.py`, `app.py` — the real Gradio dashboard, pure
  data display, no LLM calls, so it needed no adaptation at all
- Fetch and Memory MCP servers (`mcp-server-fetch`, `mcp-memory-libsql`) —
  already free, local npx/uvx subprocesses in the original

## What changed, and exactly why

| File | What changed | Why |
|---|---|---|
| `traders.py` | `get_model()` gained an `ollama:` branch pointing at `http://localhost:11434/v1` | the original only routes to paid providers (OpenAI, DeepSeek, Grok, Gemini, OpenRouter) |
| `trading_floor.py` | `model_names` defaults to 4 local Ollama models instead of `gpt-5.4-mini` ×4 | zero-cost default; `USE_MANY_MODELS=true` now compares local models against each other |
| `mcp_servers.py` | Tavily's hosted search server (needs `TAVILY_API_KEY`) replaced with `search_server.py` (`duckduckgo-search`, no key) | Tavily requires signup; DuckDuckGo doesn't |
| `search_server.py` | **new file**, not in the original | the free replacement for Tavily, one tool, same role |
| `push_server.py` | falls back to a local log file when `PUSHOVER_USER`/`PUSHOVER_TOKEN` aren't set; identical tool shape otherwise | Pushover needs a signup; the fallback needs none |
| `market.py` | `massive` import wrapped in `try/except` | so the file doesn't crash if you never install the optional live-data package |

## Not reproduced in this edition

`frontend/` — the original's separate Vite/TypeScript dashboard that
consumes `backend/api.py`. `api.py` itself **is** included, unmodified, and
ready for a frontend — building one is flagged as a stretch exercise in
Lab 5, since a full TS/React rebuild is out of scope for a Python-notebook
course.

`community_contributions/` — not ported; that's student work from the
original cohort, not course material.

## Setup
```bash
pip install -r requirements.txt
```
Also needs Node v22+ and `uv`/`uvx` (for `npx`/`uvx`-launched MCP servers:
fetch, memory, and optionally the Massive market server) — see root
`setup/SETUP-local-pc.md`.

## Honest caveats for students
- A 3B local model juggling accounts, market, search, and memory tools at
  once is a genuinely hard multi-tool-use task. If trading decisions look
  erratic, that's a real capability signal, not a bug — try `qwen2.5:7b` or
  larger if your hardware allows.
- The market simulator (`market_simulator.py`) is deterministic smooth
  noise, not real prices — by design, so the agent/tool mechanics can be
  taught for free. Set `MASSIVE_API_KEY` (and `pip install massive`) for
  live data once students understand the plumbing.
