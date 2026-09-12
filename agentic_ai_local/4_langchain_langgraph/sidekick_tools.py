"""Tools for the Sidekick: a mix of MCP servers, ready-made LangChain tools and our own.

Local Models Edition — by Abhishek. Ported directly from abhishek/agents.
Two changes from the original, both to remove a paid/signup dependency:
- `GoogleSerperRun` (needs SERPER_API_KEY) -> DuckDuckGo search (no key)
- `send_push_notification` posts to Pushover only if creds are set in .env,
  otherwise logs locally, so the Sidekick runs with zero signups
Everything else — Wikipedia, the browser/filesystem MCP servers, the
persistent-session machinery — is unchanged; it was already free and local.
"""

import asyncio
import os
from contextlib import AsyncExitStack

import requests
import wikipedia
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools

load_dotenv(override=True)

# Wikimedia rejects the wikipedia library's default user agent, so identify ourselves properly
wikipedia.set_user_agent("agentic-track-course-local (https://github.com/Abhishekravindran)")


@tool
def search(query: str) -> str:
    """Search the web and return a short summary of the top results."""
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))
    if not results:
        return "No results found."
    return "\n\n".join(f"{r['title']}: {r['body']}" for r in results)


wikipedia_lookup = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())


@tool
def send_push_notification(text: str) -> str:
    """Send a short push notification to the user's phone."""
    token, user = os.getenv("PUSHOVER_TOKEN"), os.getenv("PUSHOVER_USER")
    if token and user:
        response = requests.post(
            "https://api.pushover.net/1/messages.json",
            data={"token": token, "user": user, "message": text},
        )
        response.raise_for_status()
        return "Notification sent"
    with open("notifications.log", "a") as f:
        f.write(text + "\n")
    return "Notification logged locally (set PUSHOVER_TOKEN/PUSHOVER_USER in .env for a real push)"


@tool
def request_human_help(instructions: str) -> str:
    """Ask the user to do something in the browser window that you cannot do yourself,
    such as logging in to a site, passing a captcha, or approving two-factor authentication.
    Explain exactly what you need them to do. The run pauses until they have done it."""
    return "The user says it is done. Continue with the task."


def mcp_connections(sandbox: str) -> dict:
    """The MCP servers the Sidekick uses: a headed browser and a sandbox filesystem."""
    return {
        "playwright": {
            "transport": "stdio",
            "command": "npx",
            "args": ["@playwright/mcp@latest", "--isolated"],
        },
        "filesystem": {
            "transport": "stdio",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", sandbox],
        },
    }


class McpSessions:
    """Holds persistent MCP sessions open so the browser keeps its state between tool calls.

    The stdio transport must be opened and closed from the same asyncio task, so one
    background task owns the sessions: it opens them, waits, and unwinds them when stop()
    is called. Stopping shuts down the servers, and you will see the browser close.
    """

    def __init__(self, connections: dict):
        self.connections = connections
        self.tools = []
        self._ready = asyncio.Event()
        self._stop = asyncio.Event()
        self._task = None

    async def _run(self):
        client = MultiServerMCPClient(self.connections)
        async with AsyncExitStack() as stack:
            for name in self.connections:
                session = await stack.enter_async_context(client.session(name))
                self.tools += await load_mcp_tools(session, server_name=name)
            self._ready.set()
            await self._stop.wait()

    async def start(self) -> list:
        self._task = asyncio.create_task(self._run())
        ready = asyncio.create_task(self._ready.wait())
        await asyncio.wait([ready, self._task], return_when=asyncio.FIRST_COMPLETED)
        ready.cancel()
        if self._task.done():
            self._task.result()  # the servers failed to start; raise the real error
        return self.tools

    def stop(self):
        self._stop.set()


async def get_all_tools(sandbox: str):
    """Return the full tool list (our tools plus the MCP server tools) and the session holder."""
    sessions = McpSessions(mcp_connections(sandbox))
    mcp_tools = await sessions.start()
    our_tools = [search, send_push_notification, wikipedia_lookup, request_human_help]
    return our_tools + mcp_tools, sessions
