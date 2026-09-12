# Colab vs. Local PC — which track should you use?

Every lab in this course runs on **both**. Pick based on your hardware.

## Google Colab track
**Use if:** you don't want to install anything, or your laptop is
underpowered.

- Backend: Hugging Face `transformers`, running a small instruct model
  (default: `Qwen/Qwen2.5-1.5B-Instruct`) directly in the notebook process.
- Free Colab gives you a T4 GPU (Runtime → Change runtime type → T4 GPU) —
  turn this on, it makes a big difference in speed.
- Nothing persists between sessions — you'll re-download the model each
  time you open the notebook (a few GB, a couple of minutes).
- No sign-up needed for the models used in this course (all public,
  no-gated Hugging Face repos).

## Local PC track
**Use if:** you want an offline, persistent setup, or you're already
comfortable with a terminal.

- Backend: [Ollama](https://ollama.com) — runs a local model as a
  background service with a REST API on `localhost:11434`.
- Works on Windows, Mac, and Linux, CPU-only is fine for the small models
  we use (`llama3.2:3b`, `qwen2.5:3b`).
- Model is downloaded once (`ollama pull llama3.2:3b`) and reused across
  every notebook and every session — faster after the first run.
- See `setup/SETUP-local-pc.md` for the full walkthrough.

## How notebooks detect which track you're on

Every lab starts with a cell like this — you don't need to edit it, just
run it:

```python
import importlib.util

IN_COLAB = importlib.util.find_spec("google.colab") is not None

if IN_COLAB:
    BACKEND = "huggingface"
    print("Running in Colab -> using Hugging Face transformers backend")
else:
    BACKEND = "ollama"
    print("Running locally -> using Ollama backend (make sure `ollama serve` is running)")
```

If you want to force a specific backend regardless of environment (e.g.
you have Ollama installed inside Colab via a workaround, or you want to
run Hugging Face locally on a GPU), just hardcode `BACKEND = "ollama"` or
`BACKEND = "huggingface"` after this cell.

## Model size guidance

| Environment | Recommended model | Why |
|---|---|---|
| Colab (CPU only) | `Qwen/Qwen2.5-0.5B-Instruct` | Fast enough without a GPU |
| Colab (T4 GPU) | `Qwen/Qwen2.5-1.5B-Instruct` | Better quality, still fast |
| Local PC (CPU) | `llama3.2:3b` via Ollama | Good balance for CPU |
| Local PC (has a GPU) | `qwen2.5:7b` via Ollama | Noticeably better tool-use and reasoning |
