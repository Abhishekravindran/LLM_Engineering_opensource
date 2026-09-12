"""
backend/trading_floor.py — the scheduler that runs all four traders.
Local Models Edition — by Abhishek

Adapted from abhishek/agents: model_names now defaults to four free local
Ollama models instead of four paid frontier models. USE_MANY_MODELS still
toggles "one model per trader" vs "same model for all" — just with local
models on both sides of that toggle, so the comparison remains genuinely free.
"""
from .traders import Trader
from typing import List
import asyncio
from .tracers import LogTracer
from agents import add_trace_processor
from .market import is_market_open
from dotenv import load_dotenv
import os

load_dotenv(override=True)

RUN_EVERY_N_MINUTES = int(os.getenv("RUN_EVERY_N_MINUTES", "60"))
RUN_EVEN_WHEN_MARKET_IS_CLOSED = (
    os.getenv("RUN_EVEN_WHEN_MARKET_IS_CLOSED", "false").strip().lower() == "true"
)
USE_MANY_MODELS = os.getenv("USE_MANY_MODELS", "false").strip().lower() == "true"

names = ["Warren", "George", "Ray", "Cathie"]
lastnames = ["Patience", "Bold", "Systematic", "Crypto"]

if USE_MANY_MODELS:
    # Four different free local models, one per trader - pull them first:
    #   ollama pull llama3.2:3b && ollama pull qwen2.5:3b
    #   ollama pull phi3:mini   && ollama pull gemma2:2b
    model_names = [
        "ollama:llama3.2:3b",
        "ollama:qwen2.5:3b",
        "ollama:phi3:mini",
        "ollama:gemma2:2b",
    ]
    short_model_names = ["Llama 3.2 3B", "Qwen2.5 3B", "Phi-3 Mini", "Gemma2 2B"]
else:
    model_names = ["ollama:llama3.2:3b"] * 4
    short_model_names = ["Llama 3.2 3B"] * 4


def create_traders() -> List[Trader]:
    traders = []
    for name, lastname, model_name in zip(names, lastnames, model_names):
        traders.append(Trader(name, lastname, model_name))
    return traders


async def run_every_n_minutes():
    add_trace_processor(LogTracer())
    traders = create_traders()
    while True:
        if RUN_EVEN_WHEN_MARKET_IS_CLOSED or is_market_open():
            await asyncio.gather(*[trader.run() for trader in traders])
        else:
            print("Market is closed, skipping run")
        await asyncio.sleep(RUN_EVERY_N_MINUTES * 60)


if __name__ == "__main__":
    print(f"Starting scheduler to run every {RUN_EVERY_N_MINUTES} minutes")
    asyncio.run(run_every_n_minutes())
