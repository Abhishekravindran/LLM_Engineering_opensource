"""
backend/mcp_servers.py — the MCP servers handed to traders and researchers.
Local Models Edition — by Abhishek

Adapted from abhishek/agents: the researcher's web search server was
Tavily's hosted MCP server (needs TAVILY_API_KEY, a signup). We swap in our
own free `search_server.py` (duckduckgo-search, no key). The fetch and
memory servers were already free/local in the original — unchanged.
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from agents.mcp import MCPServerStdio
from .market import massive_api_key

load_dotenv(override=True)

PROJECT_DIR = str(Path(__file__).resolve().parent.parent)
TIMEOUT = 120

# The market data server for the trader.
# With a key, hand the agent Massive's own market data server, run locally over stdio.
# Without one, use our market server, which serves simulated prices.
if massive_api_key:
    market_params = {
        "command": "uvx",
        "args": [
            "--with", "mcp<2",
            "--from", "git+https://github.com/massive-com/mcp_massive@v0.10.0",
            "mcp_massive"
        ],
        "env": {"MASSIVE_API_KEY": massive_api_key},
    }
else:
    market_params = {
        "command": "python",
        "args": ["-m", "backend.market_server"],
        "cwd": PROJECT_DIR
    }


def trader_mcp_servers() -> list[MCPServerStdio]:
    """The trader's MCP servers: our Accounts server, Push Notification and Market data."""
    params = [
        {"command": "python", "args": ["-m", "backend.accounts_server"], "cwd": PROJECT_DIR},
        {"command": "python", "args": ["-m", "backend.push_server"], "cwd": PROJECT_DIR},
        market_params,
    ]
    return [MCPServerStdio(p, client_session_timeout_seconds=TIMEOUT) for p in params]


def researcher_mcp_servers(name: str) -> list[MCPServerStdio]:
    """The researcher's MCP servers: Fetch, free web search, and Memory.

    Fetch and Memory are launched with `npx`/`uvx` exactly as in the original
    course (free, local, no key). Search is our own local server instead of
    Tavily, so the whole floor runs with zero paid/signup services.
    """
    fetch = MCPServerStdio(
        {"command": "uvx", "args": ["--with", "mcp<2", "mcp-server-fetch"]},
        client_session_timeout_seconds=TIMEOUT,
    )
    search = MCPServerStdio(
        {"command": "python", "args": ["-m", "backend.search_server"], "cwd": PROJECT_DIR},
        client_session_timeout_seconds=TIMEOUT,
    )
    memory = MCPServerStdio(
        {
            "command": "npx",
            "args": ["-y", "mcp-memory-libsql"],
            "env": {"LIBSQL_URL": f"file:./memory/{name}.db"},
        },
        client_session_timeout_seconds=TIMEOUT,
    )
    return [fetch, search, memory]
