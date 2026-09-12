# Week 6 — Model Context Protocol (MCP)
### Mirrors original `6_mcp` week

MCP standardizes how an agent discovers and calls external tools/data
sources through a client-server protocol — independent of which model
powers the agent. Everything here plugs into the local model from any
earlier week.

## Labs

**`lab1_mcp_intro.ipynb`**
What MCP is and why it exists — client/server roles, tools vs resources
vs prompts. Connect to a public example MCP server as a read-only demo.

**`lab2_build_a_local_mcp_server.ipynb`**
Build your own minimal MCP server in Python exposing the Week 1 tools
(`calculator`, `lookup_fact`) as MCP tools.

**`lab3_local_agent_as_mcp_client.ipynb`**
Connect a local-model agent (Ollama or Hugging Face backend, your choice
of framework from Weeks 2–5) as an MCP client to the server from lab 2.

**`lab4_multiple_mcp_servers.ipynb`**
Register two MCP servers with one agent (e.g. the Week 2 server plus a
second one for a different tool set) and watch it pick the right one.

**`lab5_capstone.ipynb`**
Capstone: an agent (any framework from Weeks 2–5) using MCP-exposed tools,
running end-to-end on a local model — this is the "everything together"
final project for the course.

## Setup
```bash
pip install -r requirements.txt
```
`requirements.txt`: `mcp`, plus whichever framework's package you use for
the agent side (`langgraph`, `crewai`, `pydantic-ai`, etc.)

## Key idea

```python
# MCP server (runs locally, exposes tools over stdio or SSE)
from mcp.server.fastmcp import FastMCP

mcp_server = FastMCP("local-tools")

@mcp_server.tool()
def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression."""
    ...

if __name__ == "__main__":
    mcp_server.run()
```

The agent side (whichever framework you picked) then connects to this
server as an MCP client and gets `calculator` as a tool automatically —
no manual JSON schema writing, unlike Week 1's from-scratch version.

**Works on both tracks:** the MCP server and client are just local Python
processes talking over stdio — no Ollama-specific dependency. Colab users
can run the server and client in adjacent cells of the same notebook.
