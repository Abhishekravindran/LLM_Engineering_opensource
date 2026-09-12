"""Week-1 tools exposed over MCP (stdio)."""

from __future__ import annotations

import ast
import operator as op

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("local-tools")

_ALLOWED = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.Mod: op.mod,
}

KB = {
    "langgraph": "LangGraph builds stateful LLM workflows as graphs of nodes and edges.",
    "ollama": "Ollama runs open-weight LLMs locally with an OpenAI-compatible API.",
    "mcp": "MCP standardizes how agents discover and call external tools and data.",
    "crewai": "CrewAI organizes agents into role-based crews.",
}


def _eval(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED:
        return _ALLOWED[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED:
        return _ALLOWED[type(node.op)](_eval(node.operand))
    raise ValueError("unsupported expression")


@mcp.tool()
def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression such as '45 * 12 + 30'."""
    try:
        return str(_eval(ast.parse(expression.strip(), mode="eval").body))
    except Exception as exc:
        return f"Error: {exc}"


@mcp.tool()
def lookup_fact(topic: str) -> str:
    """Look up a short local fact about an agentic-AI topic."""
    key = topic.lower().strip()
    if key in KB:
        return KB[key]
    for k, v in KB.items():
        if k in key or key in k:
            return v
    return f"No entry for '{topic}'. Known: {', '.join(sorted(KB))}."


if __name__ == "__main__":
    mcp.run()
