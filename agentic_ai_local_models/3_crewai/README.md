# Week 3 — CrewAI
### Mirrors original `3_crewai` week

CrewAI natively supports local models through its LiteLLM integration —
just prefix the model name with `ollama/`.

## Labs

**`lab1_first_crew.ipynb`**
Define a Crew with two Agents (e.g. Researcher + Writer) and one Task each,
running on `ollama/llama3.2:3b`.

**`lab2_roles_goals_backstories.ipynb`**
Deeper dive into how role/goal/backstory prompting shapes agent behavior —
compare outputs across three different backstory framings.

**`lab3_sequential_vs_hierarchical.ipynb`**
Sequential process (agents run in order) vs. hierarchical process (a
manager agent delegates) — same task, both processes, compare results.

**`lab4_crew_with_tools.ipynb`**
Give a Crew agent a custom tool (e.g. a local calculator or a local
mock-search tool from Week 1).

**`lab5_mini_project.ipynb`**
A 3-agent crew that researches a topic, drafts content, and reviews its
own output — all local.

## Setup
```bash
pip install -r requirements.txt
```
`requirements.txt`: `crewai`, `crewai-tools`

## Key config

```python
from crewai import Agent, Task, Crew

researcher = Agent(
    role="Researcher",
    goal="Find accurate information about the topic",
    backstory="An experienced research analyst",
    llm="ollama/llama3.2:3b",   # <- this is the whole trick
)
```

**Colab note:** CrewAI's `ollama/` prefix needs a reachable Ollama server.
On Colab, either skip the free-hosted route and use CrewAI's Hugging Face
LLM wrapper instead (`llm="huggingface/Qwen/Qwen2.5-1.5B-Instruct"`), or
run this week on your local PC.
