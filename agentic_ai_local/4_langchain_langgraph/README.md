# Week 4 — LangChain & LangGraph
### Local Models Edition — by Abhishek
### Adapted line-for-line from `abhishek/agents/4_langchain_langgraph`

Same 5-day arc, same four-layer abstraction story, same capstone —
rebuilt so every model call is free and local. Runs on **Ollama** (local PC)
or **Hugging Face `transformers`** (Colab); every notebook auto-detects which
you're on.

## The four layers (same as the original)

| Layer | Packages | What it gives you |
|---|---|---|
| 1. Building blocks | `langchain-core` + `ChatOllama`/`ChatHuggingFace` | chat models, `@tool`, messages, structured output |
| 2. Orchestration | `langgraph` | a graph of steps, with state, memory, checkpointing |
| 3. Agent | `langchain` (`create_agent`) | the standard agent loop, prebuilt |
| 4. Harness | `deepagents` | planning, sub-agents, filesystem |

## Day by day

- **`1_lab1.ipynb`** — Layer 1: first local model call, streaming, messages,
  `@tool`, manual tool loop, structured output
- **`2_lab2.ipynb`** — Layer 2: LangGraph from scratch, tools node,
  conditional edges, a second LLM node (translator), memory & SQLite
  persistence, time travel, Gradio UI
- **`3_lab3.ipynb`** — Layer 3: `create_agent` in one line, memory,
  structured output, middleware, a real Playwright browser via MCP
- **`4_lab4.ipynb`** — Layer 4: Deep Agents — planning, filesystem, a
  sub-agent, and Agent Skills producing a real branded PowerPoint slide
- **`5_lab5.ipynb`** — Capstone: the **Sidekick**, a personal co-worker
  combining every layer, with human-in-the-loop approval

## What changed from the original, and why

| Original | This edition | Why |
|---|---|---|
| `ChatOpenAI(model="gpt-5.4-mini")` | `ChatOllama(model="llama3.2:3b")` or `ChatHuggingFace(...)` | no API key, runs offline |
| `GoogleSerperRun` (needs `SERPER_API_KEY`) | `duckduckgo-search` (`DDGS`) | genuinely free, no signup |
| Pushover push notifications | falls back to a local log file when no Pushover creds are set; real Pushover still works if you add them | works with zero setup |
| `slide_kit.py` (Voltway Research brand, needs a `logo.png` asset) | **unchanged**, logo made optional | fully local either way; runs without the asset |
| `sidekick.py` / `sidekick_tools.py` / `app.py` | **unchanged** except the model is now passed in (`Sidekick(model)`) instead of hardcoded `"openai:gpt-5.4-mini"` | same middleware stack, same evaluator loop, same Gradio UI — just pointed at a free local model |
| Playwright MCP server, filesystem MCP server | **unchanged** | already free & local in the original |
| `styles.py` (Sidekick's Gradio theme/CSS) | **unchanged** | pure styling, no model calls, needed no adaptation |
| LangSmith observability | **unchanged**, noted as provider-agnostic | traces local model calls too |

## Setup
```bash
pip install -r requirements.txt
```
Local PC also needs Node v22+ (for the Playwright/filesystem MCP servers) —
see the root `setup/SETUP-local-pc.md`.

## Honest caveat for students
Smaller local models (3B-class) are noticeably less reliable at multi-step
tool use and strict structured output than GPT-4-class models. This shows up
most in Lab 3's browser-driving agent and Lab 5's flight-finding errand.
That's not a bug in your code — it's the real capability trade-off of going
local, and it's worth discussing explicitly rather than hiding.
