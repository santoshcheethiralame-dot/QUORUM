import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from . import config as C
from . import engine
from . import ledger as ledger_mod
from .desk import bars_of


def _r(x, n=4):
    return [None if v != v else round(float(v), n) for v in x]


def _weights(s):
    return C.WEIGHTS.get(C.UNIVERSE[s][1], C.WEIGHTS["default"])[0]


def _votes(eng, day, s):
    return {k: round(float(eng["parts"][k].loc[day, s]), 1) for k in C.SLEEVES if _weights(s).get(k, 0) > 0}


def _shadow(eng, day, s):
    return {k: round(float(eng["forecasts"][k].loc[day, s]), 1) for k in C.SLEEVES
            if k in _weights(s) and _weights(s)[k] == 0}


def _why(votes, net):
    bits = [f"{C.SLEEVE_LABEL[k]} {v:+.0f}" for k, v in votes.items()]
    lean = "long" if net > 0 else "short" if net < 0 else "flat"
    return f"{', '.join(bits)}. Net {net:+.0f} on a scale of -20 to +20, so the book leans {lean}."


def build(eng, px, ledger, tiles, health, stress):
    idx = eng["index"]
    day = idx[-1]
    syms = eng["symbols"]
    pnl, bench = eng["pnl"], eng["bench"]
    eq = (1 + pnl).cumprod()
    beq = (1 + bench).cumprod()
    dd = eq / eq.cummax() - 1
    start = pnl.index[(eng["held"].abs().sum(axis=1) > 0).values[: len(pnl)]][0]

    equity_now = ledger["equity"][-1][1]
    brake = ledger_mod.brake(ledger)
    dd_now = ledger_mod.drawdown(ledger)
    tw = eng["unbraked"].loc[day] * brake
    close = px["adj"].loc[day]
    positions, signals = [], []
    for s in syms:
        name, group = C.UNIVERSE[s]
        votes = _votes(eng, day, s)
        net = round(float(eng["net"].loc[day, s]), 1)
        units = ledger["units"].get(s, 0.0)
        value = units * float(close[s])
        spread = max(votes.values()) - min(votes.values()) if len(votes) > 1 else 0
        row = {"symbol": s, "name": name, "group": group, "votes": votes, "net": net,
               "shadow": _shadow(eng, day, s),
               "contested": bool(spread >= 15 and abs(net) <= 5),
               "target_w": round(float(tw[s]), 4),
               "vol": round(float(eng["vol"].loc[day, s]), 3), "ohlc": bars_of(px, s)}
        signals.append(row)
        positions.append({**row, "units": units, "price": round(float(px["close"].loc[day, s]), 2),
                          "value": round(value, 2), "w": round(value / equity_now, 4)})

    tickets = []
    for t in ledger["pending"]:
        s = t["symbol"]
        votes = _votes(eng, day, s)
        net = round(float(eng["net"].loc[day, s]), 1)
        tickets.append({**t, "name": C.UNIVERSE[s][0], "group": C.UNIVERSE[s][1], "votes": votes, "net": net,
                        "shadow": _shadow(eng, day, s),
                        "why": _why(votes, net)})
    tickets.sort(key=lambda t: -t["notional"])

    gross = float(tw.abs().sum())
    longs = float(tw[tw > 0].sum())
    shorts = float(-tw[tw < 0].sum())
    theme = float(tw[C.THEME["members"]].abs().sum())
    eq_net = float(tw[[s for s in syms if C.UNIVERSE[s][1] == "equity"]].sum())
    realised = float(pnl.iloc[-60:].std() * np.sqrt(256))
    stressed = bool(stress.reindex(idx).fillna(False).iloc[-1])
    regime = "Stressed" if stressed else "Calm"
    if brake < 1:
        regime = "Braking"

    monthly = (1 + pnl[start:]).groupby([pnl[start:].index.year, pnl[start:].index.month]).prod() - 1
    years = sorted({y for y, _ in monthly.index})
    heat = [{"year": int(y), "months": [None if (y, m) not in monthly.index else round(float(monthly[(y, m)]), 4)
                                        for m in range(1, 13)],
             "total": round(float((1 + monthly[y]).prod() - 1), 4),
             "bench": round(float((1 + bench[start:][bench[start:].index.year == y]).prod() - 1), 4)} for y in years]

    sleeves = {k: _r((v[start:]).cumsum() * 100, 3) for k, v in eng["sleeve_pnl"].items()}
    by_group = {}
    for g in C.GROUP_ORDER:
        members = [s for s in syms if C.UNIVERSE[s][1] == g]
        by_group[g] = round(float(tw[members].sum()), 4)

    nxt = (day + pd.offsets.BDay(1)).strftime("%Y-%m-%d")
    out = {
        "meta": {"generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
                 "last_bar": day.strftime("%Y-%m-%d"), "next_session": nxt, "inception": ledger["inception"],
                 "capital0": ledger["capital0"], "equity": equity_now, "sim_start": start.strftime("%Y-%m-%d")},
        "regime": {"label": regime, "stressed": stressed, "brake": brake},
        "book": {"gross": round(gross, 4), "long": round(longs, 4), "short": round(shorts, 4),
                 "by_group": by_group},
        "risk": [
            {"label": "Recent volatility", "value": realised, "limit": C.TARGET_VOL, "fmt": "pct",
             "note": "The model's 60-day realised swings against the 12% target"},
            {"label": "Paper account drawdown", "value": dd_now, "limit": C.BRAKE[0][0], "fmt": "pct",
             "note": "Risk halves at 10% below the past year's high and quarters at 20%"},
            {"label": "Total exposure", "value": gross, "limit": C.MAX_GROSS, "fmt": "x",
             "note": "Longs plus shorts as a multiple of capital"},
            {"label": C.THEME["name"] + " exposure", "value": theme, "limit": C.THEME["cap"], "fmt": "pct",
             "note": "Nasdaq and chip positions combined"},
            {"label": "Net stock exposure", "value": max(eq_net, 0.0), "limit": C.MAX_EQUITY_NET, "fmt": "pct",
             "note": "All equity funds, longs minus shorts"},
        ],
        "tickets": tickets, "positions": positions, "signals": signals,
        "sleeve_labels": C.SLEEVE_LABEL, "group_order": C.GROUP_ORDER,
        "sim": {"dates": [d.strftime("%Y-%m-%d") for d in pnl[start:].index],
                "strategy": _r(eq[start:] / eq[start:].iloc[0] * 100, 2),
                "benchmark": _r(beq[start:] / beq[start:].iloc[0] * 100, 2),
                "drawdown": _r(dd[start:] * 100, 2), "sleeves": sleeves,
                "stats": {"strategy": engine.stats(pnl[start:]), "benchmark": engine.stats(bench[start:])},
                "turnover": round(float(eng["turnover"][start:].sum() / C.COST_BPS["default"] * 1e4
                                        / (len(pnl[start:]) / 256)), 1),
                "heat": heat},
        "radar": tiles, "health": health,
        "journal": {"fills": ledger["fills"][-200:][::-1], "equity": ledger["equity"]},
        "limits": {"target_vol": C.TARGET_VOL, "buffer": C.BUFFER},
    }
    return out


def write(payload):
    tpl = (C.SITE / "template.html").read_text(encoding="utf-8")
    blob = json.dumps(payload, separators=(",", ":")).replace("</", "<\\/")
    C.SITE.mkdir(exist_ok=True)
    (C.SITE / "index.html").write_text(tpl.replace("/*__DATA__*/null", blob), encoding="utf-8")
    (C.DATA / "latest.json").write_text(json.dumps(payload, indent=1), encoding="utf-8")
