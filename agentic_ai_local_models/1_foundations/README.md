# Week 1 — Foundations
### No framework yet — understand the raw mechanics first

Mirrors `1_foundations`course, rebuilt for local
models. The point of this week: by the end, students understand what every
framework in weeks 2–6 is automating for them.

## Labs

**`lab1_intro_and_first_call.ipynb`** *(included, working — see below)*
Environment detection (Colab vs local), first call to a local model via
Hugging Face `transformers` or Ollama, basic prompting patterns.

**`lab2_structured_output.ipynb`**
Getting a local model to reliably return JSON — schema-constrained
generation with Pydantic, retry-on-parse-failure pattern.

**`lab3_tools_from_scratch.ipynb`**
Define a Python function as a "tool," describe it to the model in a
system prompt (no native tool-calling API needed), parse the model's
intent to call it, execute it, return the result. This is what
`OpenAI Agents SDK` / `CrewAI` / `LangChain` are doing under the hood.

**`lab4_simple_agent_loop.ipynb`**
Combine labs 2–3 into a minimal ReAct-style loop: Reason → Act → Observe →
repeat until done. Compare against the more polished agent frameworks
coming in later weeks.

**`lab5_mini_project.ipynb`**
Build a small end-to-end agent (e.g. a "research and summarize" assistant)
using nothing but what was taught this week. This is the checkpoint before
moving to frameworks — if a student can build this from scratch, they're
ready to appreciate what the frameworks save them.

## Setup
```bash
pip install -r requirements.txt
```
`requirements.txt`: `transformers`, `torch`, `ollama`, `pydantic`
