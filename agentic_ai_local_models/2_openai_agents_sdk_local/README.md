# Week 2 — OpenAI Agents SDK, pointed at a local model
### Mirrors original `2_openai` week

The OpenAI Agents SDK talks to anything that speaks the OpenAI Chat
Completions API — and **Ollama exposes exactly that** on
`http://localhost:11434/v1`. So students get the real SDK, the real
patterns (Agents, Handoffs, Guardrails, Tracing), with zero API spend.

## Labs

**`lab1_sdk_pointed_at_ollama.ipynb`**
Install `openai-agents`, configure the client's `base_url` to point at
Ollama instead of OpenAI, run a first Agent.

**`lab2_tools_and_function_calling.ipynb`**
Give the Agent real Python tools using the SDK's `@function_tool` decorator.

**`lab3_handoffs.ipynb`**
Two agents that hand off a conversation to each other (e.g. a triage agent
routing to a specialist agent).

**`lab4_guardrails.ipynb`**
Input/output guardrails — reject or reshape requests before/after the
model sees them.

**`lab5_mini_project.ipynb`**
A small multi-agent workflow using everything above, entirely on a local
model.

## Setup
```bash
pip install -r requirements.txt
```
`requirements.txt`: `openai-agents`, `ollama`

## Key config (used throughout this week's labs)

```python
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, set_default_openai_client

local_client = AsyncOpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
set_default_openai_client(local_client)

model = OpenAIChatCompletionsModel(model="llama3.2:3b", openai_client=local_client)
agent = Agent(name="Assistant", instructions="You are helpful.", model=model)
```

**Colab note:** Ollama needs a running local server, which Colab doesn't
have by default. For this week specifically, Colab students should either
(a) run this week's labs against a Hugging Face-served OpenAI-compatible
endpoint instead (see `guides/01_hf_openai_compatible_endpoint.md`), or
(b) treat this week as local-PC-only and revisit it later.
