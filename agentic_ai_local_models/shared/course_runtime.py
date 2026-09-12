"""
Shared helpers for every lab.

Goals:
- One import works on Google Colab (Hugging Face transformers) and on a local PC (Ollama).
- Frameworks that need an OpenAI-compatible HTTP API (Agents SDK, CrewAI, AutoGen,
  Pydantic AI) get a tiny local server wrapping the same model — no paid API key.
"""

from __future__ import annotations

import ast
import importlib.util
import json
import operator as op
import os
import re
import sys
import threading
import time
from pathlib import Path
from typing import Any, Callable


HF_MODEL_DEFAULT = os.environ.get("COURSE_HF_MODEL", "Qwen/Qwen2.5-1.5B-Instruct")
HF_MODEL_CPU = os.environ.get("COURSE_HF_MODEL_CPU", "Qwen/Qwen2.5-0.5B-Instruct")
OLLAMA_MODEL_DEFAULT = os.environ.get("COURSE_OLLAMA_MODEL", "llama3.2:3b")
COMPAT_PORT = int(os.environ.get("COURSE_COMPAT_PORT", "8765"))


def detect_backend(force: str | None = None) -> str:
    if force in {"huggingface", "ollama"}:
        return force
    in_colab = importlib.util.find_spec("google.colab") is not None
    return "huggingface" if in_colab else "ollama"


def find_course_root() -> Path:
    here = Path.cwd().resolve()
    candidates = [here, *here.parents]
    extra = [
        here / "agentic_ai_local",
        Path("/content/agentic_ai_local"),
        Path("/content"),
    ]
    for p in candidates + extra:
        if (p / "shared" / "course_runtime.py").exists():
            return p
        if (p / "1_foundations").is_dir() and (p / "shared").is_dir():
            return p
    return here


def ensure_on_path() -> Path:
    root = find_course_root()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    return root


# ---------------------------------------------------------------------------
# Tools used across weeks (deterministic — not the LLM)
# ---------------------------------------------------------------------------

_ALLOWED_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.Mod: op.mod,
}


def _safe_eval(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_safe_eval(node.operand))
    raise ValueError("unsupported expression")


def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression. Example: '45 * 12 + 30'."""
    try:
        tree = ast.parse(str(expression).strip(), mode="eval")
        return str(_safe_eval(tree.body))
    except Exception as exc:
        return f"Error: {exc}"


MOCK_KB = {
    "langgraph": "LangGraph builds stateful LLM workflows as graphs of nodes and edges.",
    "langchain": "LangChain is a toolkit for prompts, chains, retrievers, and tool-using agents.",
    "ollama": "Ollama runs open-weight LLMs locally and exposes an OpenAI-compatible API on port 11434.",
    "mcp": "The Model Context Protocol standardizes how agents connect to external tools and data sources.",
    "crewai": "CrewAI organizes agents into role-based crews that collaborate on tasks.",
    "autogen": "AutoGen (AG2) lets multiple conversational agents talk to each other, including group chats.",
    "pydantic ai": "Pydantic AI is a typed Python agent framework with structured outputs via Pydantic models.",
    "react": "ReAct means Reason then Act: the model thinks, calls a tool, observes the result, and repeats.",
    "agent": "An LLM agent is a language model wrapped in a loop that can use tools and stop when the task is done.",
    "openai agents sdk": "The OpenAI Agents SDK provides Agent, tools, handoffs, and guardrails on any OpenAI-compatible API.",
}


def lookup_fact(topic: str) -> str:
    """Look up a short local fact about an AI/agent topic. Not the live internet."""
    key = topic.lower().strip().strip('"').strip("'")
    if key in MOCK_KB:
        return MOCK_KB[key]
    for k, v in MOCK_KB.items():
        if k in key or key in k:
            return v
    return (
        f"No local knowledge entry for '{topic}'. "
        f"Known topics: {', '.join(sorted(MOCK_KB))}."
    )


def today_date() -> str:
    """Return today's date as ISO YYYY-MM-DD."""
    from datetime import date

    return date.today().isoformat()


TOOL_REGISTRY: dict[str, Callable[..., str]] = {
    "calculator": calculator,
    "lookup_fact": lookup_fact,
    "today_date": today_date,
}

TOOL_SCHEMAS = [
    {
        "name": "calculator",
        "description": "Evaluate a basic arithmetic expression like '12 * 7 + 3'.",
        "parameters": {
            "type": "object",
            "properties": {"expression": {"type": "string"}},
            "required": ["expression"],
        },
    },
    {
        "name": "lookup_fact",
        "description": "Look up a short fact from the local knowledge base about agentic AI topics.",
        "parameters": {
            "type": "object",
            "properties": {"topic": {"type": "string"}},
            "required": ["topic"],
        },
    },
    {
        "name": "today_date",
        "description": "Return today's date (YYYY-MM-DD).",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
]


def extract_json_object(text: str) -> dict[str, Any] | None:
    """Best-effort JSON object extraction from a small-model reply."""
    if not text:
        return None
    text = text.strip()
    try:
        obj = json.loads(text)
        return obj if isinstance(obj, dict) else None
    except json.JSONDecodeError:
        pass
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence:
        try:
            obj = json.loads(fence.group(1))
            return obj if isinstance(obj, dict) else None
        except json.JSONDecodeError:
            pass
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end > start:
        try:
            obj = json.loads(text[start : end + 1])
            return obj if isinstance(obj, dict) else None
        except json.JSONDecodeError:
            return None
    return None


def parse_tool_call(text: str) -> dict[str, Any] | None:
    obj = extract_json_object(text)
    if not obj:
        return None
    name = obj.get("name") or obj.get("tool") or obj.get("function")
    args = obj.get("arguments") or obj.get("args") or obj.get("parameters") or {}
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except json.JSONDecodeError:
            args = {"value": args}
    if name and isinstance(args, dict):
        return {"name": str(name), "arguments": args}
    return None


# ---------------------------------------------------------------------------
# Chat backends
# ---------------------------------------------------------------------------

_hf_generator = None
_hf_model_name = None


def _load_hf_pipeline(model_name: str | None = None):
    global _hf_generator, _hf_model_name
    import torch
    from transformers import pipeline

    name = model_name or HF_MODEL_DEFAULT
    if not torch.cuda.is_available() and name == HF_MODEL_DEFAULT:
        # 1.5B on CPU is painful in a class; fall back unless the user overrode it.
        if os.environ.get("COURSE_FORCE_HF_MODEL") != "1":
            name = HF_MODEL_CPU
    if _hf_generator is not None and _hf_model_name == name:
        return _hf_generator
    device = 0 if torch.cuda.is_available() else -1
    print(f"Loading Hugging Face model {name} on {'GPU' if device == 0 else 'CPU'} ...")
    _hf_generator = pipeline("text-generation", model=name, device=device)
    _hf_model_name = name
    return _hf_generator


def local_chat(
    messages: list[dict[str, str]],
    *,
    backend: str | None = None,
    max_new_tokens: int = 256,
    temperature: float = 0.3,
    model: str | None = None,
) -> str:
    """Chat with the course model. `messages` is OpenAI-style role/content dicts."""
    backend = detect_backend(backend)
    if backend == "huggingface":
        generator = _load_hf_pipeline(model)
        output = generator(
            messages,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=temperature > 0,
        )
        generated = output[0]["generated_text"]
        if isinstance(generated, list) and generated:
            last = generated[-1]
            if isinstance(last, dict) and "content" in last:
                return str(last["content"])
            return str(last)
        return str(generated)
    import ollama

    response = ollama.chat(
        model=model or OLLAMA_MODEL_DEFAULT,
        messages=messages,
        options={"num_predict": max_new_tokens, "temperature": temperature},
    )
    return response["message"]["content"]


def get_langchain_llm(backend: str | None = None, temperature: float = 0.2):
    backend = detect_backend(backend)
    if backend == "huggingface":
        from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
        from transformers import pipeline as hf_pipeline
        import torch

        name = HF_MODEL_DEFAULT if torch.cuda.is_available() else HF_MODEL_CPU
        pipe = hf_pipeline(
            "text-generation",
            model=name,
            max_new_tokens=200,
            device=0 if torch.cuda.is_available() else -1,
        )
        return ChatHuggingFace(llm=HuggingFacePipeline(pipeline=pipe))
    from langchain_ollama import ChatOllama

    return ChatOllama(model=OLLAMA_MODEL_DEFAULT, temperature=temperature)


def openai_client_kwargs(backend: str | None = None) -> dict[str, str]:
    """base_url + api_key + model_name for any OpenAI-compatible SDK."""
    backend = detect_backend(backend)
    if backend == "ollama":
        return {
            "base_url": os.environ.get("OLLAMA_HOST", "http://localhost:11434") + "/v1",
            "api_key": "ollama",
            "model": OLLAMA_MODEL_DEFAULT,
        }
    start_openai_compat_server()
    return {
        "base_url": f"http://127.0.0.1:{COMPAT_PORT}/v1",
        "api_key": "local",
        "model": _hf_model_name or HF_MODEL_DEFAULT,
    }


_compat_started = False
_compat_lock = threading.Lock()


def start_openai_compat_server(port: int = COMPAT_PORT) -> str:
    """Start (once) a local OpenAI Chat Completions server wrapping the HF model."""
    global _compat_started
    with _compat_lock:
        if _compat_started:
            return f"http://127.0.0.1:{port}/v1"
        from shared.openai_compat_server import run_in_thread

        _load_hf_pipeline()
        run_in_thread(port=port, generate_fn=_hf_chat_raw, model_name=_hf_model_name or HF_MODEL_DEFAULT)
        for _ in range(50):
            time.sleep(0.1)
            try:
                import urllib.request

                urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=0.5)
                break
            except Exception:
                continue
        _compat_started = True
        print(f"OpenAI-compatible server on http://127.0.0.1:{port}/v1 (model={_hf_model_name})")
        return f"http://127.0.0.1:{port}/v1"


def _hf_chat_raw(messages: list[dict[str, Any]], max_tokens: int, temperature: float) -> str:
    clean = []
    for m in messages:
        role = m.get("role", "user")
        content = m.get("content") or ""
        if isinstance(content, list):
            content = " ".join(
                part.get("text", "") if isinstance(part, dict) else str(part) for part in content
            )
        if role == "tool":
            clean.append({"role": "user", "content": f"TOOL RESULT: {content}"})
        elif role == "assistant" and m.get("tool_calls"):
            clean.append(
                {
                    "role": "assistant",
                    "content": json.dumps({"tool_calls": m.get("tool_calls")}),
                }
            )
        else:
            clean.append({"role": role, "content": str(content)})
    return local_chat(
        clean,
        backend="huggingface",
        max_new_tokens=max_tokens,
        temperature=temperature,
    )


def print_banner(week: str, lab: str) -> str:
    backend = detect_backend()
    in_colab = importlib.util.find_spec("google.colab") is not None
    print(f"{week} / {lab}")
    print(f"Environment: {'Google Colab' if in_colab else 'Local PC'}")
    print(f"Backend: {backend}")
    if backend == "huggingface":
        print("Tip: Runtime → Change runtime type → T4 GPU for faster generation.")
    else:
        print("Need Ollama running: `ollama serve` and `ollama pull llama3.2:3b`")
    return backend
