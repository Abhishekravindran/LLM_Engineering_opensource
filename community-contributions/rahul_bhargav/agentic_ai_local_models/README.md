# Agentic AI Engineering — Local Models Edition
### by Abhishek

**Students: read [`START_HERE.md`](START_HERE.md) first.**

A hands-on, week-by-week course for building AI Agents — structured after

**every lab runs on free, local/open-weight models.** No OpenAI key,
no paid credits, no surprise bill.

**Works two ways, same notebooks:**
- **Google Colab** → uses free Hugging Face models (`transformers`, runs on
  Colab's free CPU/GPU)
- **Your own PC** → uses [Ollama](https://ollama.com) (free, runs entirely
  offline)

Every notebook starts with a small "environment detect" cell that picks the
right backend automatically — students don't have to think about it.

---

## 6-week structure

| Week | Folder | Topic | Frameworks/tools |
|---|---|---|---|
| 1 | `1_foundations` | Agent fundamentals, no framework | raw Python + local LLM |
| 2 | `2_openai_agents_sdk_local` | OpenAI Agents SDK — pointed at a **local** model | OpenAI Agents SDK + Ollama's OpenAI-compatible endpoint |
| 3 | `3_crewai` | Role-based multi-agent crews | CrewAI + local models |
| 4 | `4_langchain_langgraph` | Chains, graphs, stateful multi-agent workflows | LangChain + LangGraph + local models |
| 5 | `5_agent_frameworks` | Other major frameworks | AutoGen, Pydantic AI + local models |
| 6 | `6_mcp` | Model Context Protocol — tool servers agents can plug into | MCP + local models |

Each week folder has 4–5 labs (`lab1_...ipynb` → `lab5_...ipynb`), a
`README.md` explaining what each lab teaches, and its own
`requirements.txt`.

## Why this works without paying for API access

Ollama and Hugging Face `transformers` both let you run real open-weight
models (Llama 3.x, Qwen2.5, Phi-3, Gemma2, Mistral) on ordinary hardware.
They're smaller than GPT-4-class frontier models, so instructions should
expect **slightly less polished outputs** — that's a fine trade for a
free, offline, privacy-preserving course, and it's a realistic constraint
students will hit in the real world too.

Every framework in this course (OpenAI Agents SDK, CrewAI, LangChain/
LangGraph, AutoGen, Pydantic AI, MCP) supports pointing at a local model —
either because it speaks the OpenAI-compatible API that Ollama exposes, or
because it has a native local-model integration. That's the trick this
whole repo is built on.

## Getting started

1. Read `guides/00_colab_vs_local.md` to pick your track.
2. **Colab track:** open any lab notebook directly in Colab — nothing to
   install locally.
3. **Local PC track:** follow `setup/SETUP-local-pc.md` (install Ollama,
   pull a model, set up a Python environment).
4. Start in `1_foundations/lab1_intro_and_first_call.ipynb`.

## Community contributions

Same spirit as the original: students add their own experiments under
`community_contributions/<your-name>/`, then open a PR.

## License

MIT — reuse, remix, and teach with it freely.
