"""Market regime: bull run, uptrend, correction, bear market, crisis. Plain rules, no fitting."""
import numpy as np
import pandas as pd

LABELS = ["Bull run", "Uptrend", "Correction", "Bear market", "Crisis"]
MEANING = {
    "Bull run": "Prices are rising, most stocks are taking part, and falls have been shallow.",
    "Uptrend": "The long-term trend is up, but participation or momentum is not at full strength.",
    "Correction": "The market is well off its high or under its long-term average. Trend is in doubt.",
    "Bear market": "A deep fall with the long-term trend pointing down.",
    "Crisis": "Panic conditions: fear is spiking and prices are dropping fast.",
}
ACTION = {
    "Bull run": "New buys allowed at full size.",
    "Uptrend": "New buys allowed at full size.",
    "Correction": "New buys allowed, held positions keep their stops.",
    "Bear market": "No new stock buys. Existing positions exit on their stops.",
    "Crisis": "No new stock buys. Stops tighten, the macro book cuts risk.",
}


def classify(close, breadth=None, vix=None, vix3m=None):
    """Label every day. `close` is the index; breadth is the share of stocks above their 200-day average."""
    sma200 = close.rolling(200, min_periods=150).mean()
    sma50 = close.rolling(50, min_periods=40).mean()
    dd = 1 - close / close.rolling(252, min_periods=60).max()
    daily = close.pct_change(fill_method=None)
    ann = (daily.rolling(252, min_periods=120).std() * np.sqrt(256)).clip(lower=0.08)
    bear_dd = (1.25 * ann).clip(upper=0.5)
    r21 = close / close.shift(21) - 1
    above = close > sma200
    golden = sma50 > sma200
    if vix is not None and vix3m is not None:
        vix = vix.reindex(close.index).ffill()
        ratio = (vix / vix3m.reindex(close.index).ffill())
        crisis = (ratio > 1) & ((vix >= 28) | (r21 <= -0.08))
    else:
        ratio = pd.Series(np.nan, index=close.index)
        crisis = r21 <= -(2.5 * ann * np.sqrt(21 / 256))
    wide = breadth.reindex(close.index).ffill() >= 0.6 if breadth is not None else pd.Series(True, index=close.index)
    label = pd.Series("Uptrend", index=close.index)
    label[golden & wide & (dd < 0.05) & above] = "Bull run"
    label[(dd >= bear_dd / 2) | ~above] = "Correction"
    label[(dd >= bear_dd) | (~above & ~golden)] = "Bear market"
    label[crisis] = "Crisis"
    label[sma200.isna()] = "Uptrend"
    raw, label = label, confirm(label)
    parts = pd.DataFrame({"raw": raw, "above200": above, "golden": golden, "drawdown": dd, "month": r21, "ratio": ratio,
                          "vix": vix if vix is not None else np.nan,
                          "breadth": breadth.reindex(close.index).ffill() if breadth is not None else np.nan})
    return label, parts


def confirm(label, days=3, crisis_exit=5):
    """Stop the label flickering: a change must hold for `days` closes in a row before it counts.
    Crisis is the exception. It applies the same day and only lifts after `crisis_exit` calm closes."""
    raw = label.values
    out = raw.copy()
    cur, streak = raw[0], 0
    for i, v in enumerate(raw):
        if v == cur:
            streak = 0
        elif v == "Crisis":
            cur, streak = v, 0
        else:
            streak += 1         # closes in a row that disagree with the current label
            if streak >= (crisis_exit if cur == "Crisis" else days):
                cur, streak = v, 0
        out[i] = cur
    return pd.Series(out, index=label.index)


def score(parts_row):
    """0 (maximum fear) to 100 (maximum confidence): a single dial for the banner."""
    s = 0.0
    s += 25 if parts_row["above200"] else 0
    s += 15 if parts_row["golden"] else 0
    s += 20 * max(0.0, 1 - parts_row["drawdown"] / 0.20)
    b = parts_row["breadth"]
    s += 20 * (b if b == b else 0.5)
    v = parts_row["vix"]
    s += 20 * (1 - min(1.0, max(0.0, ((v if v == v else 20) - 12) / 28)))
    return int(round(min(100, max(0, s))))


def runs(label, since="2011-01-01"):
    """Compress the daily labels into [start, end, label] spans for the history ribbon."""
    lab = label[since:]
    out, start, cur = [], lab.index[0], lab.iloc[0]
    for d, v in lab.items():
        if v != cur:
            out.append([start.strftime("%Y-%m-%d"), d.strftime("%Y-%m-%d"), cur])
            start, cur = d, v
    out.append([start.strftime("%Y-%m-%d"), lab.index[-1].strftime("%Y-%m-%d"), cur])
    return out


def forward_table(label, close, horizon=63):
    """What the index did over the following quarter, by regime. Shows whether the labels mean anything."""
    fwd = close.shift(-horizon) / close - 1
    rows = []
    for name in LABELS:
        mask = label == name
        f = fwd[mask].dropna()
        rows.append({"label": name, "share": float(mask.mean()),
                     "next_quarter": float(f.mean()) if len(f) else None,
                     "worst": float(f.min()) if len(f) else None,
                     "up": float((f > 0).mean()) if len(f) else None})
    return rows
