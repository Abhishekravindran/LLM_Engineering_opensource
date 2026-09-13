"""Second MCP server: a tiny notes store (used in the multi-server lab)."""

from __future__ import annotations

from mcp.server.mcpserver import MCPServer 

mcp = MCPServer("notes")

_NOTES: list[str] = []


@mcp.tool()
def add_note(text: str) -> str:
    """Save a short note in memory for this process."""
    _NOTES.append(text.strip())
    return f"Saved note #{len(_NOTES)}."


@mcp.tool()
def list_notes() -> str:
    """List all notes saved in this process."""
    if not _NOTES:
        return "(no notes yet)"
    return "\n".join(f"{i+1}. {n}" for i, n in enumerate(_NOTES))


if __name__ == "__main__":
    mcp.run()
