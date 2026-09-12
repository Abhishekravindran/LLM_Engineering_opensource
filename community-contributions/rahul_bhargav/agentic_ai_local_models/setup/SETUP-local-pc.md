# Setup — Local PC track

## 1. Install Ollama
Download from https://ollama.com/download (Windows/Mac/Linux).
After install, it runs as a background service. Verify with:

```bash
ollama --version
```

## 2. Pull the models used in this course

```bash
ollama pull llama3.2:3b        # main chat/agent model, ~2GB
ollama pull qwen2.5:3b         # alternative, good tool-calling support
ollama pull nomic-embed-text   # for any embedding/RAG-adjacent labs
```

## 3. Confirm the server is reachable

```bash
curl http://localhost:11434/api/tags
```
You should see JSON listing the models you pulled. If this fails, run
`ollama serve` in a terminal and leave it running.

## 4. Python environment

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install --upgrade pip
```

Then install per-week requirements as you go — each week folder has its
own `requirements.txt` (kept separate so students aren't installing
CrewAI just to do the Week 1 foundations labs).

## 5. Jupyter

```bash
pip install jupyterlab
jupyter lab
```

Open any `labX_....ipynb` and run cells top to bottom.

## Troubleshooting

- **"Connection refused" errors** → Ollama isn't running. Run `ollama serve`.
- **Model responses look truncated** → some small models have short default
  context; check the lab notebook for a `num_ctx` option in the Ollama
  options dict.
- **Very slow on CPU** → try `llama3.2:3b` or `qwen2.5:3b` (avoid 7B+
  models without a GPU).
