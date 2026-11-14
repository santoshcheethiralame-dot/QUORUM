import json
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests

from . import config as C

CACHE = C.DATA / "cache"
URL = "https://query1.finance.yahoo.com/v8/finance/chart/{}"
START = 1262304000  # 2010-01-01


NAMES_FILE = CACHE / "names.json"
NAMES = json.loads(NAMES_FILE.read_text(encoding="utf-8")) if NAMES_FILE.exists() else {}


def save_names():
    CACHE.mkdir(parents=True, exist_ok=True)
    NAMES_FILE.write_text(json.dumps(NAMES, indent=0), encoding="utf-8")


def _path(symbol):
    return CACHE / (symbol.replace("^", "_").replace("=", "_") + ".csv")


def fetch(symbol, max_age_h=6.0):
    CACHE.mkdir(parents=True, exist_ok=True)
    f = _path(symbol)
    if f.exists() and time.time() - f.stat().st_mtime < max_age_h * 3600:
        return pd.read_csv(f, index_col=0, parse_dates=True)
    try:
        r = requests.get(
            URL.format(symbol),
            params={"period1": START, "period2": int(time.time()), "interval": "1d", "events": "div,splits"},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=30,
        )
        r.raise_for_status()
        res = r.json()["chart"]["result"][0]
        q = res["indicators"]["quote"][0]
        adj = (res["indicators"].get("adjclose") or [{}])[0].get("adjclose") or q["close"]
        tz = res["meta"].get("exchangeTimezoneName", "UTC")
        idx = pd.to_datetime(res["timestamp"], unit="s", utc=True).tz_convert(tz).tz_localize(None).normalize()
        df = pd.DataFrame(
            {"open": q["open"], "high": q["high"], "low": q["low"], "close": q["close"], "adj": adj}, index=idx
        ).dropna(subset=["close", "open"])
        df = df[~df.index.duplicated(keep="last")]
        # a bar for a session that is still trading is not a close: keep it out of every signal
        period = (res["meta"].get("currentTradingPeriod") or {}).get("regular") or {}
        if period and res["timestamp"][-1] >= period.get("start", 0) and time.time() < period.get("end", 0):
            df = df.iloc[:-1]
        NAMES[symbol] = res["meta"].get("shortName") or res["meta"].get("longName") or symbol
        df.to_csv(f)
        time.sleep(0.25)
        return df
    except Exception:
        if f.exists():
            return pd.read_csv(f, index_col=0, parse_dates=True)
        raise


def fetch_many(symbols, workers=6):
    """Fetch in parallel; a symbol that fails is dropped, not fatal."""
    out = {}

    def one(s):
        try:
            return s, fetch(s)
        except Exception:
            return s, None

    with ThreadPoolExecutor(workers) as pool:
        for s, df in pool.map(one, symbols):
            if df is not None and len(df) > 300:
                out[s] = df
    save_names()
    return out


def intraday(symbol):
    """One-minute bars for the latest session, for pre-filling live charts."""
    r = requests.get(URL.format(symbol), params={"range": "1d", "interval": "1m", "includePrePost": "false"},
                     headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    r.raise_for_status()
    res = r.json()["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    ts = res.get("timestamp", [])
    pts = [[t, round(c, 4)] for t, c in zip(ts, q["close"]) if c is not None]
    bars = [[t, round(o, 4), round(h, 4), round(l, 4), round(c, 4)]
            for t, o, h, l, c in zip(ts, q["open"], q["high"], q["low"], q["close"]) if None not in (o, h, l, c)]
    meta = res["meta"]
    return {"symbol": symbol, "points": pts, "bars": bars, "prev_close": meta.get("chartPreviousClose"),
            "price": meta.get("regularMarketPrice")}


def load_panel(symbols, calendar_symbol="SPY"):
    raw = fetch_many(symbols)
    symbols = [s for s in symbols if s in raw]
    cal = raw[calendar_symbol].index
    cols = {}
    for field in ["open", "high", "low", "close", "adj"]:
        cols[field] = pd.DataFrame({s: raw[s][field].reindex(cal) for s in symbols})
    factor = cols["adj"] / cols["close"]
    cols["adj_open"] = cols["open"] * factor
    health = []
    last = cal[-1]
    for s in symbols:
        own_last = raw[s].index[raw[s].index <= last][-1]
        stale = int(len(cal[cal > own_last]))
        gaps = int(cols["close"][s].iloc[-60:].isna().sum())
        health.append({"symbol": s, "last": own_last.strftime("%Y-%m-%d"), "stale_days": stale, "gaps_60d": gaps,
                       "ok": stale == 0 and gaps == 0})
    return cols, health
