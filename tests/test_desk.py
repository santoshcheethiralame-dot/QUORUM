import numpy as np
import pandas as pd

from quorum import config as C
from quorum import feed, picks, regime


def _index(n=600):
    return pd.bdate_range("2020-01-01", periods=n)


def test_confirm_ignores_a_one_day_flip_but_crisis_is_immediate():
    idx = _index(12)
    raw = pd.Series(["Uptrend"] * 4 + ["Correction"] + ["Uptrend"] * 3 + ["Crisis"] + ["Uptrend"] * 3, index=idx)
    out = regime.confirm(raw)
    assert out.iloc[4] == "Uptrend"            # one-day flip never shows
    assert out.iloc[8] == "Crisis"             # crisis shows the same day
    assert out.iloc[11] == "Crisis"            # and needs five calm closes to lift


def test_confirm_switches_when_the_old_label_stays_wrong():
    idx = _index(8)
    raw = pd.Series(["Uptrend", "Uptrend", "Correction", "Bear market", "Correction", "Bear market", "Bear market",
                     "Bear market"], index=idx)
    out = regime.confirm(raw)
    assert list(out.iloc[:4]) == ["Uptrend"] * 4
    assert out.iloc[4] == "Correction" and out.iloc[-1] == "Bear market"


def test_steady_climb_is_not_bearish_and_a_crash_is():
    idx = _index()
    up = pd.Series(100 * 1.0006 ** np.arange(len(idx)), index=idx)
    label, _ = regime.classify(up)
    assert label.iloc[-1] in ("Bull run", "Uptrend")
    crash = up.copy()
    crash.iloc[-60:] = crash.iloc[-61] * np.linspace(1, 0.6, 60)
    label, parts = regime.classify(crash)
    assert label.iloc[-1] in ("Bear market", "Crisis")
    assert regime.score(parts.iloc[-1]) < 50


def _panel(n=600, k=20, seed=3):
    idx = _index(n)
    rng = np.random.default_rng(seed)
    drift = np.linspace(-0.0004, 0.0012, k)
    adj = pd.DataFrame(100 * np.exp(np.cumsum(drift + rng.normal(0, 0.012, (n, k)), axis=0)), index=idx,
                       columns=[f"S{i}" for i in range(k)])
    return {"adj": adj, "close": adj, "high": adj * 1.01, "low": adj * 0.99, "open": adj}


def test_picks_never_hold_more_than_the_limit_and_use_only_past_data():
    px = _panel()
    label = pd.Series("Uptrend", index=px["adj"].index)
    full = picks.simulate(px, label, 5)
    assert len(full["last"][0]) <= 5
    cut = {k: v.iloc[:500] for k, v in px.items()}
    part = picks.simulate(cut, label.iloc[:500], 5)
    assert np.allclose(full["daily"].iloc[:500].values, part["daily"].values)


def test_no_new_buys_in_a_bear_market():
    px = _panel()
    sim = picks.simulate(px, pd.Series("Bear market", index=px["adj"].index), 5)
    assert not sim["trades"] and not sim["last"][0] and not sim["last"][1]


def test_table_flags_match_the_simulation_and_stops_sit_below_price():
    px = _panel()
    label = pd.Series("Uptrend", index=px["adj"].index)
    sim = picks.simulate(px, label, 5)
    rows = {r["symbol"]: r for r in picks.table(sim, px, "Uptrend", {})}
    held, buys, sells = sim["last"]
    syms = sim["symbols"]
    for j in held:
        assert rows[syms[j]]["status"] == ("SELL" if j in sells else "HOLD")
    for j in buys:
        assert rows[syms[j]]["status"] == "BUY" and rows[syms[j]]["stop"] < rows[syms[j]]["price"]
    assert all(r["stop"] is not None for r in rows.values() if r["status"] in ("HOLD", "SELL", "BUY"))
    assert max(len(held), 0) <= C.MARKETS["US"]["max_names"]


def test_feed_decodes_a_quote():
    def varint(v):
        out = b""
        while True:
            b, v = v & 0x7F, v >> 7
            out += bytes([b | (0x80 if v else 0)])
            if not v:
                return out
    import struct
    raw = bytes([0x0A, 3]) + b"SPY" + bytes([0x15]) + struct.pack("<f", 512.25) + bytes([0x18]) + varint(2 * 1700000000000)
    tick = feed.decode(raw)
    assert tick["id"] == "SPY" and abs(tick["price"] - 512.25) < 1e-4 and tick["time"] == 1700000000000
