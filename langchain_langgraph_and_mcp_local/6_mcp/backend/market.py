"""Share prices from the Massive market data API, or a simulator when no key is set.

Local Models Edition — by Abhishek. Ported directly from abhishek/agents,
with one change: the `massive` import is now optional. If you don't have the
package installed (it's not needed for the free local track), everything
still works via the simulator.

Set MASSIVE_API_KEY to use live data. Without it, prices come from
market_simulator so the whole trading floor still runs out of the box.
"""

import os
from dotenv import load_dotenv
from .market_simulator import simulated_price

load_dotenv(override=True)

massive_api_key = os.getenv("MASSIVE_API_KEY")

try:
    from massive import RESTClient
except ImportError:
    RESTClient = None
    if massive_api_key:
        print("MASSIVE_API_KEY is set but the `massive` package isn't installed; "
              "run `pip install massive` to use live data. Falling back to the simulator.")


def _last_trade(client, symbol: str) -> float:
    return float(client.get_last_trade(symbol).price)


def _snapshot(client, symbol: str) -> float:
    snapshot = client.get_snapshot_ticker("stocks", symbol)
    return float(snapshot.min.close or snapshot.prev_day.close)


def _previous_close(client, symbol: str) -> float:
    return float(client.get_previous_close_agg(symbol)[0].close)


# Best price first, prior close last. Lower tier plans reject the earlier calls,
# so we remember the first tier that works and start there next time.
price_methods = [_last_trade, _snapshot, _previous_close]
plan_tier = 0


def get_share_price(symbol: str) -> float:
    """Return the current price for a symbol, from Massive or the simulator."""
    if massive_api_key and RESTClient is not None:
        try:
            return get_share_price_massive(symbol)
        except Exception as e:
            print(f"Massive API unavailable ({e}); using a simulated price")
    return simulated_price(symbol)


def get_share_price_massive(symbol: str) -> float:
    """Best price the plan allows, remembering the working tier to avoid repeat failures."""
    global plan_tier
    client = RESTClient(massive_api_key)
    for tier in range(plan_tier, len(price_methods)):
        try:
            price = price_methods[tier](client, symbol)
            plan_tier = tier
            return price
        except Exception:
            continue
    raise RuntimeError(f"No Massive price available for {symbol}")


def is_market_open() -> bool:
    """Whether the US market is open; True on simulated data or if Massive is unreachable."""
    if not massive_api_key or RESTClient is None:
        return True
    try:
        client = RESTClient(massive_api_key)
        return client.get_market_status().market == "open"
    except Exception:
        return True
