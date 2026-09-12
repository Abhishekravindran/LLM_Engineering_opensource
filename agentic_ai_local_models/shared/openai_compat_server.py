"""Minimal OpenAI Chat Completions API wrapping a local generate() function.

Used on Colab so Agents SDK / CrewAI / AutoGen / Pydantic AI can talk to a
Hugging Face model with no API key. On a local PC, labs use Ollama's own /v1.
"""

from __future__ import annotations

import json
import threading
import uuid
from typing import Any, Callable

from fastapi import FastAPI
from pydantic import BaseModel, Field

GenerateFn = Callable[[list[dict[str, Any]], int, float], str]

app = FastAPI(title="Course local OpenAI-compatible server")
_generate: GenerateFn | None = None
_model_name = "local-instruct"


class ChatMessage(BaseModel):
    role: str
    content: Any = None
    tool_calls: list[Any] | None = None
    tool_call_id: str | None = None
    name: str | None = None


class ChatRequest(BaseModel):
    model: str = "local"
    messages: list[ChatMessage]
    temperature: float = 0.3
    max_tokens: int = 256
    tools: list[dict[str, Any]] | None = None
    tool_choice: Any = None
    stream: bool = False


def set_generate(fn: GenerateFn, model_name: str = "local-instruct") -> None:
    global _generate, _model_name
    _generate = fn
    _model_name = model_name


def _messages_to_dicts(messages: list[ChatMessage]) -> list[dict[str, Any]]:
    out = []
    for m in messages:
        d: dict[str, Any] = {"role": m.role, "content": m.content}
        if m.tool_calls:
            d["tool_calls"] = m.tool_calls
        if m.tool_call_id:
            d["tool_call_id"] = m.tool_call_id
        if m.name:
            d["name"] = m.name
        out.append(d)
    return out


def _tool_preamble(tools: list[dict[str, Any]]) -> str:
    names = []
    lines = [
        "You can call tools. When you need a tool, reply with ONLY JSON:",
        '{"name": "<tool_name>", "arguments": {<args>}}',
        "If you can answer without a tool, reply with normal text (no JSON).",
        "Available tools:",
    ]
    for t in tools:
        fn = t.get("function", t)
        name = fn.get("name", "unknown")
        names.append(name)
        lines.append(f"- {name}: {fn.get('description', '')}")
        params = fn.get("parameters") or fn.get("args") or {}
        lines.append(f"  parameters JSON schema: {json.dumps(params)}")
    return "\n".join(lines)


def _looks_like_tool_json(text: str) -> dict[str, Any] | None:
    import re

    if not text:
        return None
    blob = text.strip()
    obj = None
    try:
        obj = json.loads(blob)
    except json.JSONDecodeError:
        fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", blob, re.DOTALL)
        if fence:
            try:
                obj = json.loads(fence.group(1))
            except json.JSONDecodeError:
                obj = None
        if obj is None:
            start, end = blob.find("{"), blob.rfind("}")
            if start != -1 and end > start:
                try:
                    obj = json.loads(blob[start : end + 1])
                except json.JSONDecodeError:
                    return None
    if not isinstance(obj, dict):
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


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "model": _model_name}


@app.get("/v1/models")
def list_models() -> dict[str, Any]:
    return {
        "object": "list",
        "data": [{"id": _model_name, "object": "model", "owned_by": "local"}],
    }


@app.post("/v1/chat/completions")
def chat_completions(req: ChatRequest) -> dict[str, Any]:
    if _generate is None:
        raise RuntimeError("generate function not configured")

    messages = _messages_to_dicts(req.messages)
    if req.tools:
        messages = [
            {"role": "system", "content": _tool_preamble(req.tools)},
            *messages,
        ]

    text = _generate(messages, req.max_tokens, req.temperature).strip()
    tool_parsed = _looks_like_tool_json(text) if req.tools else None

    if tool_parsed:
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": f"call_{uuid.uuid4().hex[:12]}",
                    "type": "function",
                    "function": {
                        "name": tool_parsed["name"],
                        "arguments": json.dumps(tool_parsed["arguments"]),
                    },
                }
            ],
        }
        finish = "tool_calls"
    else:
        message = {"role": "assistant", "content": text}
        finish = "stop"

    return {
        "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
        "object": "chat.completion",
        "model": req.model or _model_name,
        "choices": [
            {
                "index": 0,
                "message": message,
                "finish_reason": finish,
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        },
    }


def run_in_thread(port: int, generate_fn: GenerateFn, model_name: str | None = None) -> None:
    import uvicorn

    set_generate(generate_fn, model_name or _model_name)

    def _serve() -> None:
        uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")

    t = threading.Thread(target=_serve, daemon=True)
    t.start()
