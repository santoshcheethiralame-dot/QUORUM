"""Stock picks: rank by momentum and strength, buy the leaders, sell on a trailing stop or a rank drop."""
import numpy as np
import pandas as pd

from . import config as C

BLOCKED = {"Bear market", "Crisis"}


def indicators(px):
    close, high, low, adj = px["close"], px["high"], px["low"], px["adj"]
    mom = adj.shift(21) / adj.shift(252) - 1
    hi52 = adj.rolling(252, min_periods=200).max()
    near = adj / hi52
    sma200 = adj.rolling(200, min_periods=150).mean()
    sma50 = adj.rolling(50, min_periods=40).mean()
    prev = close.shift(1)
    tr = pd.concat([(high - low), (high - prev).abs(), (low - prev).abs()]).groupby(level=0).max()
    atr_pct = (tr / close).rolling(20, min_periods=15).mean()
    z = lambda d: d.sub(d.mean(axis=1), axis=0).div(d.std(axis=1).replace(0, np.nan), axis=0)
    score = (z(mom) + z(near)) / 2
    rank = score.rank(axis=1, ascending=False, pct=True)
    trend_ok = (adj > sma200) & (sma50 > sma200)
    vol = adj.pct_change(fill_method=None).rolling(60, min_periods=40).std() * np.sqrt(256)
    return {"mom": mom, "near": near, "score": score, "rank": rank, "trend_ok": trend_ok, "atr_pct": atr_pct,
            "sma200": sma200, "vol": vol}


def simulate(px, regime, max_names):
    """Walk through history one close at a time. Signals at close t trade at close t+1."""
    ind = indicators(px)
    adj = px["adj"]
    syms = list(adj.columns)
    idx = adj.index
    P = C.PICKS
    A, RK, OK, ATR = adj.values, ind["rank"].values, ind["trend_ok"].values, ind["atr_pct"].values
    reg = regime.reindex(idx).ffill().fillna("Uptrend").values
    ret = adj.pct_change(fill_method=None).fillna(0.0).values
    held = {}           # symbol index -> {entry_i, entry_px, peak, stop}
    pending_buy, pending_sell = [], {}
    weights = np.zeros(len(syms))
    daily = np.zeros(len(idx))
    trades, events = [], []
    slot = 1.0 / max_names
    cost = P["cost_bps"] / 1e4
    for i in range(len(idx)):
        daily[i] = float(weights @ ret[i])
        # fill yesterday's decisions at today's close
        for j, why in pending_sell.items():
            if j in held:
                h = held.pop(j)
                trades.append({"symbol": syms[j], "entry": idx[h["entry_i"]], "exit": idx[i],
                               "ret": A[i, j] / h["entry_px"] - 1 - 2 * cost, "why": why})
                daily[i] -= weights[j] * cost
                weights[j] = 0.0
        for j in pending_buy:
            if j not in held and len(held) < max_names and A[i, j] == A[i, j]:
                held[j] = {"entry_i": i, "entry_px": A[i, j], "peak": A[i, j], "stop": 0.0}
                weights[j] = slot
                daily[i] -= slot * cost
        pending_buy, pending_sell = [], {}
        mult = P["atr_mult_crisis"] if reg[i] == "Crisis" else P["atr_mult"]
        for j, h in held.items():
            price = A[i, j]
            if price != price:
                continue
            h["peak"] = max(h["peak"], price)
            atr = ATR[i, j] if ATR[i, j] == ATR[i, j] else 0.03
            h["stop"] = max(h["stop"], h["peak"] * (1 - mult * atr))
            if price < h["stop"]:
                pending_sell[j] = "Closed below its trailing stop"
            elif RK[i, j] != RK[i, j] or RK[i, j] > P["hold_pct"]:
                pending_sell[j] = "Dropped out of the leaders"
            elif not OK[i, j]:
                pending_sell[j] = "Long-term trend broke"
        room = max_names - len(held) + len(pending_sell)
        if reg[i] not in BLOCKED and room > 0:
            cands = [j for j in np.argsort(np.where(RK[i] == RK[i], RK[i], 9.0))
                     if RK[i, j] == RK[i, j] and RK[i, j] <= P["enter_pct"] and OK[i, j] and j not in held]
            pending_buy = cands[:room]
        events.append((dict((j, dict(h)) for j, h in held.items()), list(pending_buy), dict(pending_sell)))
    return {"ind": ind, "index": idx, "symbols": syms, "daily": pd.Series(daily, index=idx), "trades": trades,
            "last": events[-1], "prev": events[-2] if len(events) > 1 else ({}, [], {}), "slot": slot}


def table(sim, px, regime_now, names):
    """Today's verdict for every stock in the market."""
    ind, syms, idx = sim["ind"], sim["symbols"], sim["index"]
    held, buys, sells = sim["last"]
    day = idx[-1]
    adj_to_raw = (px["close"].loc[day] / px["adj"].loc[day]).fillna(1.0)
    rows = []
    for j, s in enumerate(syms):
        close = float(px["close"].loc[day, s])
        if close != close:
            continue
        prev = px["close"][s].dropna()
        prev_close = float(prev.iloc[-2]) if len(prev) > 1 else close
        rank = float(ind["rank"].loc[day, s]) if ind["rank"].loc[day, s] == ind["rank"].loc[day, s] else None
        atr = float(ind["atr_pct"].loc[day, s]) if ind["atr_pct"].loc[day, s] == ind["atr_pct"].loc[day, s] else 0.03
        row = {"symbol": s, "name": names.get(s, s), "price": round(close, 2), "prev_close": round(prev_close, 2),
               "rank": rank, "score": _f(ind["score"].loc[day, s]), "mom": _f(ind["mom"].loc[day, s]),
               "near": _f(ind["near"].loc[day, s]), "trend_ok": bool(ind["trend_ok"].loc[day, s]),
               "vol": _f(ind["vol"].loc[day, s]), "atr": round(atr, 4), "weight": 0.0, "stop": None,
               "entry_date": None, "entry_price": None, "gain": None, "reason": ""}
        if j in sells:
            h = held[j]
            row.update(status="SELL", reason=sells[j] + ".", stop=round(h["stop"] * adj_to_raw[s], 2),
                       entry_date=idx[h["entry_i"]].strftime("%Y-%m-%d"),
                       entry_price=round(h["entry_px"] * adj_to_raw[s], 2),
                       gain=float(px["adj"].loc[day, s] / h["entry_px"] - 1), weight=sim["slot"])
        elif j in held:
            h = held[j]
            row.update(status="HOLD", stop=round(h["stop"] * adj_to_raw[s], 2),
                       entry_date=idx[h["entry_i"]].strftime("%Y-%m-%d"),
                       entry_price=round(h["entry_px"] * adj_to_raw[s], 2),
                       gain=float(px["adj"].loc[day, s] / h["entry_px"] - 1), weight=sim["slot"],
                       reason="Still a leader and above its stop.")
        elif j in buys:
            mult = C.PICKS["atr_mult_crisis"] if regime_now == "Crisis" else C.PICKS["atr_mult"]
            row.update(status="BUY", stop=round(close * (1 - mult * atr), 2), weight=sim["slot"],
                       reason="Top-ranked for momentum and strength, long-term trend is up.")
        elif rank is not None and rank <= C.PICKS["enter_pct"] and row["trend_ok"]:
            why = "the market regime blocks new buys" if regime_now in BLOCKED else "the book is full"
            row.update(status="WATCH", reason=f"Qualifies, but {why}.")
        else:
            row.update(status="NONE", reason="Not a leader." if row["trend_ok"] else "Long-term trend is not up.")
        rows.append(row)
    order = {"SELL": 0, "BUY": 1, "HOLD": 2, "WATCH": 3, "NONE": 4}
    rows.sort(key=lambda r: (order[r["status"]], r["rank"] if r["rank"] is not None else 9))
    return rows


def _f(x):
    return None if x != x else round(float(x), 4)


def trade_stats(trades):
    if not trades:
        return {"count": 0}
    r = np.array([t["ret"] for t in trades])
    wins, losses = r[r > 0], r[r <= 0]
    days = np.array([(t["exit"] - t["entry"]).days for t in trades])
    return {"count": int(len(r)), "win_rate": float((r > 0).mean()),
            "avg_win": float(wins.mean()) if len(wins) else 0.0,
            "avg_loss": float(losses.mean()) if len(losses) else 0.0,
            "avg_days": float(days.mean()),
            "exits": {k: int(sum(1 for t in trades if t["why"] == k)) for k in {t["why"] for t in trades}}}
