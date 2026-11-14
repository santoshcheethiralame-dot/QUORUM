import numpy as np
import pandas as pd

from . import config as C


def trend_forecast(close):
    vol_px = close.diff().ewm(span=36, min_periods=20).std()
    parts = []
    for fast, scalar in C.EWMAC:
        slow = 4 * fast
        raw = close.ewm(span=fast, min_periods=fast).mean() - close.ewm(span=slow, min_periods=slow).mean()
        parts.append((raw / vol_px * scalar).clip(-20, 20))
    return (sum(parts) / len(parts) * C.TREND_FDM).clip(-20, 20)


def rsi(close, n=2):
    d = close.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, min_periods=n).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, min_periods=n).mean()
    return 100 - 100 / (1 + up / dn.replace(0, np.nan))


def reversion_forecast(high, low, close, adj):
    rng = (high - low).replace(0, np.nan)
    ibs = ((close - low) / rng).fillna(0.5)
    f_ibs = (0.5 - ibs) * 40
    f_rsi = (50 - rsi(adj).fillna(50)) / 50 * 20
    return (0.5 * f_ibs + 0.5 * f_rsi).clip(-20, 20)


def calendar_forecast(index):
    d = index.values.astype("datetime64[D]")
    m0 = d.astype("datetime64[M]")
    start = m0.astype("datetime64[D]")
    nxt = (m0 + 1).astype("datetime64[D]")
    day_of_month = np.busday_count(start, d) + 1
    remaining = np.busday_count(d, nxt) - 1
    on = (remaining <= 1) | (day_of_month <= 2)
    return pd.Series(np.where(on, C.CALENDAR_FORECAST, 0.0), index=index)


def sleeve_forecasts(px):
    syms = list(px["adj"].columns)
    trend = trend_forecast(px["adj"])
    rev = reversion_forecast(px["high"], px["low"], px["close"], px["adj"])
    cal = calendar_forecast(px["adj"].index)
    zeros = pd.DataFrame(0.0, index=trend.index, columns=syms)
    out = {"trend": trend, "reversion": zeros.copy(), "calendar": zeros.copy()}
    for s in syms:
        if C.UNIVERSE[s][1] == "equity":
            out["reversion"][s] = rev[s]
            out["calendar"][s] = cal
    return out


def combine(forecasts):
    syms = list(forecasts["trend"].columns)
    base = forecasts["trend"]
    parts = {k: pd.DataFrame(0.0, index=base.index, columns=syms) for k in C.SLEEVES}
    for s in syms:
        weights, fdm = C.WEIGHTS.get(C.UNIVERSE[s][1], C.WEIGHTS["default"])
        for k, w in weights.items():
            parts[k][s] = forecasts[k][s] * w * fdm
    net = sum(parts.values()).clip(-20, 20)
    return net, parts


def annual_vol(adj):
    v = adj.pct_change(fill_method=None).ewm(span=C.VOL_SPAN, min_periods=20).std() * np.sqrt(256)
    return v.clip(lower=C.VOL_FLOOR)


def apply_limits(w, syms):
    w = np.clip(w, -C.MAX_WEIGHT, C.MAX_WEIGHT)
    eq = np.array([C.UNIVERSE[s][1] == "equity" for s in syms])
    th = np.array([s in C.THEME["members"] for s in syms])
    theme = np.abs(w[th]).sum()
    if theme > C.THEME["cap"]:
        w[th] *= C.THEME["cap"] / theme
    eq_net = w[eq].sum()
    if eq_net > C.MAX_EQUITY_NET:
        w[eq] *= C.MAX_EQUITY_NET / eq_net
    gross = np.abs(w).sum()
    if gross > C.MAX_GROSS:
        w *= C.MAX_GROSS / gross
    return w


def brake_multiplier(drawdown):
    m = 1.0
    for level, mult in C.BRAKE:
        if drawdown >= level:
            m = mult
    return m


def run(px, stress):
    """Simulate the book. A decision at close j is filled at open j+1 and earns open-to-open returns."""
    syms = list(px["adj"].columns)
    idx = px["adj"].index
    n, m = len(idx), len(syms)
    forecasts = sleeve_forecasts(px)
    net, parts = combine(forecasts)
    vol = annual_vol(px["adj"])
    valid = net.notna() & vol.notna() & px["adj_open"].notna()
    n_avail = valid.sum(axis=1).clip(lower=1)
    k = (C.TARGET_VOL / vol).mul(C.IDM / n_avail, axis=0).where(valid, 0.0)
    raw_w = (net / 10 * k).fillna(0.0)

    oo = px["adj_open"].shift(-1) / px["adj_open"] - 1  # return over day j, open j to open j+1
    R = oo.fillna(0.0).values
    cost = np.array([C.COST_BPS.get(C.UNIVERSE[s][1], C.COST_BPS["default"]) / 1e4 for s in syms])

    K, RAW = k.values, raw_w.values
    stress_v = stress.reindex(idx).fillna(False).values
    target = np.zeros((n, m))
    unbraked = np.zeros((n, m))  # targets before the drawdown brake; the live ledger applies its own
    held = np.zeros((n, m))
    scale = np.ones(n)
    pnl = np.zeros(n)
    turnover = np.zeros(n)
    equity = np.ones(n)
    H = np.zeros(m)   # weights held from open j to open j+1
    eq = 1.0          # equity at open j: all a decision at close j is allowed to know
    tc = 0.0
    for j in range(n):
        equity[j] = eq
        held[j] = H
        peak = equity[max(0, j - 252): j + 1].max()
        regime = C.STRESS_SCALE if stress_v[j] else 1.0
        mult = brake_multiplier(1 - eq / peak) * regime
        unbraked[j] = apply_limits(RAW[j] * regime, syms)
        limited = apply_limits(RAW[j] * mult, syms)
        denom = np.abs(RAW[j]).sum()
        scale[j] = np.abs(limited).sum() / denom if denom > 0 else mult
        target[j] = limited
        move = np.abs(limited - H) > C.BUFFER * K[j]
        gain = float(H @ R[j])
        pnl[j] = gain - tc
        turnover[j] = tc
        eq *= 1 + pnl[j]
        drifted = H * (1 + R[j]) / (1 + gain)
        new = np.where(move, limited, drifted)
        tc = float(np.abs(new - drifted) @ cost)
        H = new

    sleeve_pnl = {}
    for name in C.SLEEVES:
        ideal = (parts[name] / 10 * k).fillna(0.0).values * scale[:, None]
        sleeve_pnl[name] = np.concatenate([[0.0], (ideal[:-1] * R[1:]).sum(axis=1)])
    explained = sum(sleeve_pnl.values())
    sleeve_pnl["other"] = pnl - explained

    bench = np.concatenate([[0.0], R[1:, syms.index("SPY")]])
    end = n - 1  # last bar has no realised open-to-open return yet
    return {
        "index": idx, "symbols": syms, "forecasts": forecasts, "parts": parts, "net": net, "vol": vol, "k": k,
        "target": pd.DataFrame(target, index=idx, columns=syms),
        "unbraked": pd.DataFrame(unbraked, index=idx, columns=syms),
        "held": pd.DataFrame(held, index=idx, columns=syms),
        "scale": pd.Series(scale, index=idx),
        "pnl": pd.Series(pnl, index=idx).iloc[:end],
        "bench": pd.Series(bench, index=idx).iloc[:end],
        "sleeve_pnl": {a: pd.Series(b, index=idx).iloc[:end] for a, b in sleeve_pnl.items()},
        "turnover": pd.Series(turnover, index=idx).iloc[:end],
    }


def stats(r):
    r = r.dropna()
    eq = (1 + r).cumprod()
    years = len(r) / 256
    vol = r.std() * np.sqrt(256)
    dd = 1 - eq / eq.cummax()
    return {
        "cagr": float(eq.iloc[-1] ** (1 / years) - 1),
        "vol": float(vol),
        "sharpe": float(r.mean() * 256 / vol) if vol > 0 else 0.0,
        "max_dd": float(dd.max()),
        "hit": float((r > 0).sum() / max(1, (r != 0).sum())),
        "worst_day": float(r.min()),
    }
