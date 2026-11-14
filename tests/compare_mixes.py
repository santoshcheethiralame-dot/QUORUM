"""Research script: how each sleeve mix and buffer size performs after costs. Run: python tests/compare_mixes.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from quorum import config as C, data, engine, radar

px, _ = data.load_panel(list(C.UNIVERSE))
_, stress = radar.build()
START = "2011-01-07"


def go(name, weights, fdm, buf):
    C.WEIGHTS["equity"] = (weights, fdm)
    C.BUFFER = buf
    e = engine.run(px, stress)
    p = e["pnl"][START:]
    s = engine.stats(p)
    turnover = e["turnover"][START:].sum() / 5e-4 / (len(p) / 256)
    sleeves = {k: round(float(v[START:].sum() * 100), 1) for k, v in e["sleeve_pnl"].items()}
    print(f"{name:26s} sharpe {s['sharpe']:.2f}  cagr {s['cagr']:.1%}  vol {s['vol']:.1%}  "
          f"maxdd {s['max_dd']:.1%}  turnover {turnover:.0f}x  {sleeves}")


FULL = {"trend": 0.5, "reversion": 0.3, "calendar": 0.2}
for buf in (0.10, 0.25):
    go(f"all three, buffer {buf}", FULL, 1.3, buf)
    go(f"trend+calendar, buffer {buf}", {"trend": 0.7, "calendar": 0.3}, 1.15, buf)
    go(f"trend only, buffer {buf}", {"trend": 1.0}, 1.0, buf)
