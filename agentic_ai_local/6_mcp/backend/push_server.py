"""
backend/push_server.py — MCP server for trader notifications.
Local Models Edition — by Abhishek

Adapted from abhishek/agents: the original always posts to Pushover (a free
account, but still a signup). Here we keep the exact same tool shape, but
fall back to a local log file when PUSHOVER_USER/PUSHOVER_TOKEN aren't set,
so the trading floor runs with zero signups. Set both env vars to get real
push notifications on your phone instead.
"""
import os
from dotenv import load_dotenv
import requests
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

load_dotenv(override=True)

pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_url = "https://api.pushover.net/1/messages.json"


mcp = FastMCP("push_server")


class PushModelArgs(BaseModel):
    message: str = Field(description="A brief message to push")


@mcp.tool()
def push(args: PushModelArgs):
    """Send a push notification with this brief message"""
    print(f"Push: {args.message}")
    if pushover_user and pushover_token:
        payload = {"user": pushover_user, "token": pushover_token, "message": args.message}
        requests.post(pushover_url, data=payload)
        return "Push notification sent"
    with open("notifications.log", "a") as f:
        f.write(args.message + "\n")
    return "Notification logged locally (set PUSHOVER_USER/PUSHOVER_TOKEN in .env for a real push)"


if __name__ == "__main__":
    mcp.run(transport="stdio")
