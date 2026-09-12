# Week 4 — LangChain & LangGraph
### Mirrors original `4_langchain_langgraph` week

`langchain-ollama` gives a native `ChatOllama` class; on Colab,
`langchain-huggingface` gives an equivalent `ChatHuggingFace` wrapper
around a local `transformers` pipeline. Same LangChain/LangGraph code,
different model object underneath.

## Labs

**`lab1_langchain_basics_local.ipynb`**
`ChatOllama` / `ChatHuggingFace` first calls, prompt templates, output
parsers.

**`lab2_chains_and_memory.ipynb`**
Sequential chains, conversation memory across turns.

**`lab3_langgraph_state_machine.ipynb`**
Your first LangGraph graph: nodes, edges, shared state — a simple
2-node graph (e.g. "draft" → "critique" → loop until approved).

**`lab4_langgraph_multiagent.ipynb`** *(included, working — see below)*
A multi-agent LangGraph workflow: a Router node dispatches to a
Researcher or a Calculator sub-agent based on the question, entirely on
a local model, dual-backend (Colab/local).

**`lab5_mini_project.ipynb`**
Extend lab 4 into a 3+ node graph with a human-in-the-loop checkpoint.

## Setup
```bash
pip install -r requirements.txt
```
`requirements.txt`: `langchain`, `langchain-ollama`, `langchain-huggingface`,
`langgraph`, `transformers`, `torch`

## Key config

```python
# Local PC
from langchain_ollama import ChatOllama
llm = ChatOllama(model="llama3.2:3b", temperature=0.3)

# Colab
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from transformers import pipeline
pipe = pipeline("text-generation", model="Qwen/Qwen2.5-1.5B-Instruct", max_new_tokens=256)
llm = ChatHuggingFace(llm=HuggingFacePipeline(pipeline=pipe))
```

Both `llm` objects are drop-in compatible with everything else in
LangChain/LangGraph — chains, agents, graphs — so the rest of each lab's
code doesn't change based on backend.
