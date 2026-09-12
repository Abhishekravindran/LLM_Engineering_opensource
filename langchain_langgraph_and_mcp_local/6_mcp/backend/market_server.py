"""
backend/market_server.py — MCP server exposing market.py's get_share_price.
Local Models Edition — by Abhishek. Ported directly from abhishek/agents
(this file was already free/local in the original — no changes needed).
"""
from mcp.server.fastmcp import FastMCP
from .market import get_share_price

mcp = FastMCP("market_server")


@mcp.tool()
async def lookup_share_price(symbol: str) -> float:
    """Get the current share price for a stock by its ticker symbol.

    Args:
        symbol: The stock ticker symbol
    """
    return get_share_price(symbol)


if __name__ == "__main__":
    mcp.run(transport="stdio")
