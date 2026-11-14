"""Everything the live desk needs beyond the macro book: regimes, stock picks, reference quotes."""
import numpy as np
import pandas as pd

from . import config as C
from . import data, engine, picks, regime

START = "2012-01-03"


def _weekly(series):
    s = series.iloc[::5]
    return [d.strftime("%Y-%m-%d") for d in s.index], [round(float(v), 2) for v in s.values]


def candles(o, h, l, c, n=60):
    """Last n daily bars as [yyyymmdd, open, high, low, close] for the candle charts."""
    df = pd.concat([o, h, l, c], axis=1).dropna().iloc[-n:]
    return [[int(d.strftime("%Y%m%d"))] + [float(f"{v:.6g}") for v in row] for d, row in zip(df.index, df.values)]


def bars_of(px, s, n=60):
    return candles(px["open"][s], px["high"][s], px["low"][s], px["close"][s], n)


def _regime_block(label, parts, close):
    now = label.iloc[-1]
    since = label[label != now].index
    began = label.index[label.index > since[-1]][0] if len(since) else label.index[0]
    row = parts.iloc[-1]
    return {"label": now, "meaning": regime.MEANING[now], "action": regime.ACTION[now],
            "since": began.strftime("%Y-%m-%d"), "score": regime.score(row),
            "leaning": row["raw"] if row["raw"] != now else None,
            "previous": label[:began].iloc[-2] if len(label[:began]) > 1 else now,
            "parts": {"above200": bool(row["above200"]), "golden": bool(row["golden"]),
                      "drawdown": round(float(row["drawdown"]), 4), "month": round(float(row["month"]), 4),
                      "breadth": None if row["breadth"] != row["breadth"] else round(float(row["breadth"]), 3),
                      "vix": None if row["vix"] != row["vix"] else round(float(row["vix"]), 2),
                      "ratio": None if row["ratio"] != row["ratio"] else round(float(row["ratio"]), 3)}}


def build():
    vix, vix3m = data.fetch("^VIX")["close"], data.fetch("^VIX3M")["close"]
    out = {"markets": {}, "regimes": {}, "quotes": {}}
    for key, m in C.MARKETS.items():
        px, _ = data.load_panel(m["stocks"] + [m["index"]], calendar_symbol=m["index"])
        index_close = px["adj"][m["index"]]
        stocks = [s for s in px["adj"].columns if s != m["index"]]
        spx = {k: v[stocks] for k, v in px.items()}
        ind = picks.indicators(spx)
        breadth = (spx["adj"] > ind["sma200"]).sum(axis=1) / spx["adj"].notna().sum(axis=1).clip(lower=1)
        label, parts = (regime.classify(index_close, breadth, vix, vix3m) if key == "US"
                        else regime.classify(index_close, breadth))
        sim = picks.simulate(spx, label, m["max_names"])
        rows = picks.table(sim, spx, label.iloc[-1], data.NAMES)
        for r in rows:
            r["ohlc"] = bars_of(spx, r["symbol"])
        daily = sim["daily"][START:]
        bench = index_close.pct_change(fill_method=None).fillna(0.0)[START:]
        eq, beq = (1 + daily).cumprod() * 100, (1 + bench).cumprod() * 100
        dates, strat = _weekly(eq)
        block = _regime_block(label, parts, index_close)
        block["runs"] = regime.runs(label, START)
        block["forward"] = regime.forward_table(label[START:], index_close[START:])
        idx_dates, idx_vals = _weekly(index_close[START:] / index_close[START:].iloc[0] * 100)
        block["index"] = {"dates": idx_dates, "values": idx_vals, "name": m["label"]}
        out["regimes"][key] = block
        trades = [t for t in sim["trades"] if t["entry"] >= eq.index[0]]
        out["markets"][key] = {
            "label": m["label"], "currency": m["currency"], "max_names": m["max_names"],
            "capital": C.PICKS["capital"], "universe": len(stocks),
            "last_bar": sim["index"][-1].strftime("%Y-%m-%d"), "rows": rows,
            "counts": {s: sum(1 for r in rows if r["status"] == s) for s in ["BUY", "SELL", "HOLD", "WATCH"]},
            "sim": {"dates": dates, "strategy": strat, "benchmark": _weekly(beq)[1],
                    "stats": {"strategy": engine.stats(daily), "benchmark": engine.stats(bench)},
                    "trades": picks.trade_stats(trades)},
            "recent": [{"symbol": t["symbol"], "entry": t["entry"].strftime("%Y-%m-%d"),
                        "exit": t["exit"].strftime("%Y-%m-%d"), "ret": round(float(t["ret"]), 4), "why": t["why"]}
                       for t in sim["trades"][-12:]][::-1],
        }
        for r in rows:
            out["quotes"][r["symbol"]] = {"ref": r["price"], "prev": r["prev_close"], "name": r["name"],
                                          "market": key}
    btc = data.fetch("BTC-USD")["close"]
    label, parts = regime.classify(btc)
    out["regimes"]["CRYPTO"] = _regime_block(label, parts, btc)

    extra = list(dict.fromkeys(C.TAPE + list(C.UNIVERSE) + list(C.BINANCE)))
    for s, df in data.fetch_many(extra).items():
        c = df["close"].dropna()
        ohlc = candles(df["open"], df["high"], df["low"], df["close"])
        name = C.TAPE_NAMES.get(s) or (C.UNIVERSE[s][0] if s in C.UNIVERSE else data.NAMES.get(s, s))
        out["quotes"][s] = {"ref": round(float(c.iloc[-1]), 4), "prev": round(float(c.iloc[-2]), 4), "name": name, "ohlc": ohlc,
                            "market": "CRYPTO" if s in C.BINANCE else "IN" if s in ("^NSEI",) else "US"}
    out["tape"] = [s for s in C.TAPE if s in out["quotes"]]
    # last session's one-minute candles, so a hosted copy with no server still opens on a full chart
    out["intraday"] = {}
    for s in out["tape"]:
        try:
            j = data.intraday(s)
            out["intraday"][s] = {"bars": j["bars"], "prev_close": j["prev_close"]}
        except Exception:
            pass
    out["live_symbols"] = list(out["quotes"])
    out["binance"] = C.BINANCE
    return out
