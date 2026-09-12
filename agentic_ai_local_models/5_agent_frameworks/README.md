# Week 5 — Other Agent Frameworks
### Mirrors original `5_agent_frameworks` week (AutoGen + Pydantic AI)

## Labs

**`lab1_autogen_local.ipynb`**
AutoGen's `ConversableAgent` pointed at Ollama via its OpenAI-compatible
client config. Two agents having a structured back-and-forth conversation.

**`lab2_autogen_groupchat.ipynb`**
AutoGen `GroupChat` — 3+ agents plus a manager, on a local model.

**`lab3_pydantic_ai_local.ipynb`**
Pydantic AI's typed-output agents, pointed at Ollama through its
`OpenAIModel` + custom `base_url`. Focus: guaranteed structured output.

**`lab4_framework_comparison.ipynb`**
Rebuild the exact same task (router + 2 tools, from Week 4 lab 4) in
AutoGen and Pydantic AI. Side-by-side code comparison table.

**`lab5_mini_project.ipynb`**
Student's choice of framework — same mini-project brief as Week 4,
different implementation.

## Setup
```bash
pip install -r requirements.txt
```
`requirements.txt`: `pyautogen`, `pydantic-ai`, `ollama`

## Key config

```python
# AutoGen -> Ollama
config_list = [{
    "model": "llama3.2:3b",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama",
}]

# Pydantic AI -> Ollama
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
model = OpenAIModel("llama3.2:3b", base_url="http://localhost:11434/v1", api_key="ollama")
agent = Agent(model)
```

**Colab note:** as with Week 2, these frameworks' local-model paths assume
a reachable Ollama server. On Colab, use each framework's Hugging Face
integration where available, or treat this week as local-PC-only.
