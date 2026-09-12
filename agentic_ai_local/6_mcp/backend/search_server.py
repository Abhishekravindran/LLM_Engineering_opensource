"""
backend/search_server.py — free web search MCP server, replacing Tavily.
Local Models Edition — by Abhishek

The original abhishek/agents course uses Tavily's hosted MCP server for
research, which needs a paid/signup API key (TAVILY_API_KEY). This is a
drop-in replacement using duckduckgo-search — genuinely free, no signup —
exposing a single `tavily_search`-shaped tool so templates.py's researcher
instructions ("use the research tool") still make sense unchanged.
"""
from mcp.server.fastmcp import FastMCP
from duckduckgo_search import DDGS

mcp = FastMCP("search_server")


@mcp.tool()
def web_search(query: str) -> str:
    """Search the web and return a short summary of the top results."""
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))
    if not results:
        return "No results found."
    return "\n\n".join(f"{r['title']}: {r['body']}" for r in results)


if __name__ == "__main__":
    mcp.run(transport="stdio")
