import json

from . import config as C

PATH = C.DATA / "ledger.json"


def _cost(sym):
    return C.COST_BPS.get(C.UNIVERSE[sym][1], C.COST_BPS["default"]) / 1e4


def drawdown(L):
    values = [v for _, v in L["equity"][-253:]]
    return 1 - values[-1] / max(values) if values else 0.0


def brake(L):
    from .engine import brake_multiplier
    return brake_multiplier(drawdown(L))


def _tickets(day, eng, px, units, equity, mult):
    out = []
    close = px["adj"].loc[day]
    shown = px["close"].loc[day]
    for s in eng["symbols"]:
        price = float(close[s])
        if price != price or price <= 0:
            continue
        cur_w = units.get(s, 0.0) * price / equity
        tgt_w = float(eng["unbraked"].loc[day, s]) * mult
        if abs(tgt_w - cur_w) <= C.BUFFER * float(eng["k"].loc[day, s]):
            continue
        qty = round((tgt_w - cur_w) * equity / price, 4)
        if qty == 0:
            continue
        out.append({
            "symbol": s, "side": "Buy" if qty > 0 else "Sell", "qty": abs(qty), "signed_qty": qty,
            "price": round(float(shown[s]), 2), "notional": round(abs(qty) * price, 2),
            "from_w": round(cur_w, 4), "to_w": round(tgt_w, 4), "decided": day.strftime("%Y-%m-%d"),
        })
    return out


def update(eng, px, path=PATH):
    idx = eng["index"]
    last = idx[-1]
    if path.exists():
        L = json.loads(path.read_text())
    else:
        L = {"inception": last.strftime("%Y-%m-%d"), "capital0": C.CAPITAL, "cash": C.CAPITAL, "units": {},
             "last_bar": None, "pending": [], "equity": [], "fills": []}
    days = idx if L["last_bar"] is None else idx[idx > L["last_bar"]]
    days = days[days >= L["inception"]]
    for day in days:
        opens = px["adj_open"].loc[day]
        for t in L["pending"]:
            s, q = t["symbol"], t["signed_qty"]
            p = float(opens[s])
            if p != p:
                continue
            L["units"][s] = round(L["units"].get(s, 0.0) + q, 4)
            L["cash"] -= q * p + abs(q) * p * _cost(s)
            L["fills"].append({"date": day.strftime("%Y-%m-%d"), "symbol": s, "side": t["side"], "qty": t["qty"],
                               "price": round(p, 2), "notional": round(abs(q) * p, 2)})
        close = px["adj"].loc[day]
        equity = L["cash"] + sum(u * float(close[s]) for s, u in L["units"].items() if float(close[s]) == float(close[s]))
        L["equity"].append([day.strftime("%Y-%m-%d"), round(equity, 2)])
        L["pending"] = _tickets(day, eng, px, L["units"], equity, brake(L))
        L["last_bar"] = day.strftime("%Y-%m-%d")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(L, indent=1))
    return L
