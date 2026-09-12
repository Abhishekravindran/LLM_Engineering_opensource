# Start here (students)

This course teaches **AI agents** using **free local / Colab models only**. You do **not** need an OpenAI, Anthropic, or Google Gemini API key.

## Pick a track

| Track | Use when | Model |
|---|---|---|
| **Google Colab** | No install, weak laptop | Hugging Face `Qwen2.5` (turn on **T4 GPU**) |
| **Your PC** | You can install software | [Ollama](https://ollama.com) + `llama3.2:3b` |

Same notebooks. A helper picks the backend for you.

## Colab (most students)

1. Get the **whole course folder** from your instructor (GitHub clone or a `.zip`). A single `.ipynb` file is not enough after Lab 1 — later labs import `shared/`.
2. In Colab: **Runtime → Change runtime type → T4 GPU**.
3. Upload the zip, then in a cell:

```python
from google.colab import files
files.upload()  # pick the zip once
!unzip -q agentic_ai_local.zip
import os
# cd into the folder that contains README.md and 1_foundations/
os.chdir("agentic_ai_local")  # rename if your zip used a different top folder
print(os.listdir("."))
```

4. Open `1_foundations/lab1_intro_and_first_call.ipynb` and run all cells.

If your instructor published the repo on GitHub:

```python
!git clone https://github.com/<org>/<repo>.git
%cd <repo>
```

## Local PC

Follow `setup/SETUP-local-pc.md`, then:

```bash
jupyter lab
```

Start with `1_foundations/lab1_intro_and_first_call.ipynb`.

## Six weeks

1. Foundations (raw Python agent loop)
2. OpenAI Agents SDK → local model
3. CrewAI
4. LangChain + LangGraph
5. AutoGen + Pydantic AI
6. MCP + capstone

Each week folder has **5 labs**. Do them in order. Mini-projects are the checkpoint.

## What “good” looks like on small models

Answers will be shorter and less polished than ChatGPT. Labs are written for that: tiny tasks, JSON retries, deterministic tools (`calculator`, local facts). That is part of the lesson.

## Help

- Track choice: `guides/00_colab_vs_local.md`
- How Colab talks to Agents SDK / CrewAI / AutoGen: `guides/01_hf_openai_compatible_endpoint.md`
- Instructor sharing checklist: `guides/02_share_with_students.md`
