import numpy as np
import pandas as pd

from quorum import config as C
from quorum import engine

SYMS = list(C.UNIVERSE)


def make_px(n=600, seed=0, drift=0.0):
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range("2020-01-01", periods=n)
    rets = rng.normal(drift, 0.01, size=(n, len(SYMS)))
    close = pd.DataFrame(100 * np.exp(np.cumsum(rets, axis=0)), index=idx, columns=SYMS)
    op = close.shift(1).fillna(100.0)
    hi = np.maximum(op, close) * 1.002
    lo = np.minimum(op, close) * 0.998
    return {"open": op, "high": hi, "low": lo, "close": close, "adj": close, "adj_open": op}


def no_stress(px):
    return pd.Series(False, index=px["adj"].index)


def test_forecasts_are_capped():
    px = make_px()
    net, parts = engine.combine(engine.sleeve_forecasts(px))
    assert net.abs().max().max() <= 20
    for f in engine.sleeve_forecasts(px).values():
        assert f.abs().max().max() <= 20


def test_only_equities_get_reversion_and_calendar():
    f = engine.sleeve_forecasts(make_px())
    for s in SYMS:
        if C.UNIVERSE[s][1] != "equity":
            assert (f["reversion"][s] == 0).all() and (f["calendar"][s] == 0).all()


def test_disagreement_nets_to_a_smaller_position():
    idx = pd.bdate_range("2024-01-01", periods=3)
    mk = lambda v: pd.DataFrame(v, index=idx, columns=SYMS)
    agree, _ = engine.combine({"trend": mk(14.0), "reversion": mk(0.0), "calendar": mk(10.0)})
    clash, _ = engine.combine({"trend": mk(14.0), "reversion": mk(0.0), "calendar": mk(-10.0)})
    assert 0 < clash["SPY"].iloc[0] < agree["SPY"].iloc[0]
    assert clash["TLT"].iloc[0] == agree["TLT"].iloc[0] == 14.0


def test_shadow_sleeve_moves_no_money():
    idx = pd.bdate_range("2024-01-01", periods=3)
    mk = lambda v: pd.DataFrame(v, index=idx, columns=SYMS)
    quiet, _ = engine.combine({"trend": mk(5.0), "reversion": mk(0.0), "calendar": mk(0.0)})
    loud, _ = engine.combine({"trend": mk(5.0), "reversion": mk(-20.0), "calendar": mk(0.0)})
    pd.testing.assert_frame_equal(quiet, loud)


def test_limits_hold():
    w = engine.apply_limits(np.full(len(SYMS), 0.9), SYMS)
    assert np.abs(w).max() <= C.MAX_WEIGHT + 1e-9
    assert np.abs(w).sum() <= C.MAX_GROSS + 1e-9
    theme = sum(abs(w[SYMS.index(s)]) for s in C.THEME["members"])
    assert theme <= C.THEME["cap"] + 1e-9
    eq = sum(w[i] for i, s in enumerate(SYMS) if C.UNIVERSE[s][1] == "equity")
    assert eq <= C.MAX_EQUITY_NET + 1e-9


def test_limits_never_increase_or_flip_a_position():
    rng = np.random.default_rng(1)
    raw = rng.normal(0, 0.4, len(SYMS))
    w = engine.apply_limits(raw.copy(), SYMS)
    assert (np.abs(w) <= np.abs(raw) + 1e-12).all()
    assert (np.sign(w) == np.sign(raw)).all()


def test_brake_steps():
    assert engine.brake_multiplier(0.05) == 1.0
    assert engine.brake_multiplier(0.12) == 0.5
    assert engine.brake_multiplier(0.30) == 0.25


def test_no_lookahead_decisions_ignore_future_prices():
    px = make_px(seed=3)
    a = engine.run(px, no_stress(px))["target"]
    cut = 400
    px2 = {k: v.copy() for k, v in px.items()}
    for k in px2:
        px2[k].iloc[cut + 1:] *= 1.5
    b = engine.run(px2, no_stress(px2))["target"]
    pd.testing.assert_frame_equal(a.iloc[:cut], b.iloc[:cut])


def test_sleeves_plus_residual_equal_total_pnl():
    px = make_px(seed=5, drift=0.0003)
    out = engine.run(px, no_stress(px))
    total = sum(out["sleeve_pnl"].values())
    np.testing.assert_allclose(total.values, out["pnl"].values, atol=1e-12)


def test_stress_reduces_exposure():
    px = make_px(seed=7, drift=0.0005)
    calm = engine.run(px, no_stress(px))["target"].abs().sum(axis=1)
    hot = engine.run(px, pd.Series(True, index=px["adj"].index))["target"].abs().sum(axis=1)
    assert hot.iloc[300:].mean() < calm.iloc[300:].mean()


def test_calendar_window_is_turn_of_month():
    idx = pd.bdate_range("2024-01-01", "2024-03-29")
    f = engine.calendar_forecast(idx)
    assert f.loc["2024-01-30"] > 0 and f.loc["2024-01-31"] > 0
    assert f.loc["2024-02-01"] > 0 and f.loc["2024-02-02"] > 0
    assert f.loc["2024-02-15"] == 0
