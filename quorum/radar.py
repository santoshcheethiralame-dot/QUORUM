import numpy as np
import pandas as pd

from . import data

# key, group, label, how to build, unit, what a high reading means
TILES = [
    ("vix", "Risk appetite", "Volatility index", lambda s: s["^VIX"], "", "Markets are pricing bigger swings"),
    ("term", "Risk appetite", "Near-term fear vs 3-month", lambda s: s["^VIX"] / s["^VIX3M"], "x",
     "Above 1.0 means stress now, the book cuts risk"),
    ("credit", "Risk appetite", "Junk bonds vs Treasuries", lambda s: s["HYG"] / s["IEF"], "x",
     "Rising means investors are comfortable lending to weak firms"),
    ("chips", "Chips and AI", "Chip stocks vs the market", lambda s: s["SMH"] / s["SPY"], "x",
     "Rising means semiconductors are leading"),
    ("memory", "Chips and AI", "Memory maker vs chip sector", lambda s: s["MU"] / s["SMH"], "x",
     "Rising means the memory cycle is strengthening"),
    ("foundry", "Chips and AI", "Leading foundry share price", lambda s: s["TSM"], "$",
     "The clearest single read on advanced-chip demand"),
    ("breadth", "Chips and AI", "Average stock vs the index", lambda s: s["RSP"] / s["SPY"], "x",
     "Falling means gains are concentrated in a few giants"),
    ("ten", "Macro", "US 10-year yield", lambda s: s["^TNX"], "%", "Higher borrowing costs across the economy"),
    ("curve", "Macro", "10-year minus 3-month yield", lambda s: s["^TNX"] - s["^IRX"], "pt",
     "Below zero has preceded recessions"),
    ("dollar", "Macro", "US dollar index", lambda s: s["DX-Y.NYB"], "", "A strong dollar squeezes emerging markets"),
    ("growth", "Macro", "Copper vs gold", lambda s: s["HG=F"] / s["GC=F"] * 1000, "",
     "Rising means growth optimism over fear"),
    ("oil", "Macro", "Crude oil", lambda s: s["CL=F"], "$", "Energy cost and geopolitical stress"),
    ("btc", "Crypto and India", "Bitcoin", lambda s: s["BTC-USD"], "$", "Speculative appetite"),
    ("nifty", "Crypto and India", "Nifty 50", lambda s: s["^NSEI"], "", "Indian large caps"),
    ("inr", "Crypto and India", "Rupees per dollar", lambda s: s["INR=X"], "", "Higher means a weaker rupee"),
]


def build():
    needed = ["^VIX", "^VIX3M", "HYG", "IEF", "SMH", "SPY", "MU", "TSM", "RSP", "^TNX", "^IRX", "DX-Y.NYB",
              "HG=F", "GC=F", "CL=F", "BTC-USD", "^NSEI", "INR=X"]
    cal = data.fetch("SPY").index
    series = {}
    for s in needed:
        series[s] = data.fetch(s)["close"].reindex(cal).ffill()
    tiles = []
    for key, group, label, fn, unit, meaning in TILES:
        v = fn(series).dropna()
        year = v.iloc[-252:]
        now = float(v.iloc[-1])
        pct = float((year <= now).mean())
        state = "High for the past year" if pct >= 0.85 else "Low for the past year" if pct <= 0.15 else "Mid-range"
        month = float(now / v.iloc[-22] - 1) if unit != "pt" else float(now - v.iloc[-22])
        step = max(1, len(year) // 60)
        tiles.append({"key": key, "group": group, "label": label, "unit": unit, "value": round(now, 3),
                      "month_change": round(month, 4), "percentile": round(pct, 2), "state": state,
                      "meaning": meaning, "spark": [round(float(x), 4) for x in year.iloc[::step]]})
    stress = (series["^VIX"] / series["^VIX3M"]) > 1.0
    return tiles, stress
