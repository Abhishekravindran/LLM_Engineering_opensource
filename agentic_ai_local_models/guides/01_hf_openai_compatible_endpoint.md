# Hugging Face → OpenAI-compatible endpoint (Colab)

Weeks 2, 3, and 5 use libraries that expect an HTTP API shaped like OpenAI Chat Completions (`POST /v1/chat/completions`).

- **Local PC:** Ollama already provides that at `http://localhost:11434/v1`.
- **Colab:** there is no Ollama unless you install it (heavy, often blocked). This course starts a **tiny local server in the notebook process** that wraps the Hugging Face `transformers` model.

You do not call this yourself. Any lab that needs it runs:

```python
from shared.course_runtime import openai_client_kwargs
cfg = openai_client_kwargs()
# cfg["base_url"], cfg["api_key"], cfg["model"]
```

On Colab that call:

1. Loads `Qwen/Qwen2.5-1.5B-Instruct` (or `0.5B` on CPU).
2. Starts FastAPI/uvicorn on `127.0.0.1:8765`.
3. Translates Chat Completions requests into `pipeline("text-generation")`.
4. If the request includes **tools**, the server asks the model for JSON `{"name","arguments"}` and returns OpenAI-style `tool_calls`.

Dummy API key is the string `local` or `ollama` — it is never billed.

## Force a backend

```python
BACKEND = "huggingface"   # or "ollama"
```

in the detect cell, or set:

```bash
set COURSE_HF_MODEL=Qwen/Qwen2.5-0.5B-Instruct
set COURSE_OLLAMA_MODEL=qwen2.5:3b
set COURSE_COMPAT_PORT=8765
```

## If the server does not start

- Re-run the setup cell (imports `shared/`).
- Confirm you opened the **repo folder**, not an isolated notebook.
- On Colab, `127.0.0.1:8765` is inside the same runtime — other people on the internet cannot hit it.
