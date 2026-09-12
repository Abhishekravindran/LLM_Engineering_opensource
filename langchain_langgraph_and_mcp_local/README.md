# Agentic AI Engineering — Local Models Edition
### by Abhishek



```
4_langchain_langgraph/    <- Week 4: building blocks -> LangGraph -> create_agent -> Deep Agents -> Sidekick
6_mcp/                    <- Week 6: MCP intro -> your own server -> context engineering -> trading floor -> capstone
```

## Stack

| Original need | Free local replacement |
|---|---|
| OpenAI models | Ollama (`llama3.2:3b`, `qwen2.5:3b`) locally, or Hugging Face `transformers` on Colab |
| OpenAI Agents SDK | **unchanged** — pointed at Ollama's OpenAI-compatible `/v1` endpoint |
| Web search (Serper/Brave, paid) | `duckduckgo-search`, no key |
| Push notifications (Pushover) | local log file by default, real Pushover optional |
| Market data (Massive/Polygon, paid) | local random-walk simulator, real data as an opt-in swap |
| Vector DB (Qdrant Cloud) | Qdrant in-memory client, fully local |
| Tracing (OpenAI platform) | local JSONL event log |
| Playwright / filesystem / memory / fetch MCP servers | **unchanged** — already free & local in the original |
| Trading floor frontend (FastAPI + React) | single Gradio dashboard |

Each week folder has its own README with the full day-by-day breakdown and a
table of exactly what changed from the original and why.

## Setup
See each week's `requirements.txt`, plus the root course's
`setup/SETUP-local-pc.md` and `guides/00_colab_vs_local.md` for Node/`uv`
prerequisites (needed for the MCP servers).

## For instructors
Every notebook that deviates from a straightforward model swap says so
explicitly, in a markdown cell, with the reasoning — so you can decide
per-lesson whether to teach the simplification or have students build the
fuller original version as a stretch exercise.
