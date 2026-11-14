"""Daily run: pull prices, rebuild every signal and the dashboard, send phone alerts for what changed.

    python run.py            rebuild and alert
    python run.py --quiet    rebuild without alerts
"""
import sys

from quorum import pipeline


def main():
    payload = pipeline.build(notify="--quiet" not in sys.argv)
    s = payload["sim"]["stats"]["strategy"]
    print(f"last bar {payload['meta']['last_bar']}  macro orders {len(payload['tickets'])}  "
          f"macro sim sharpe {s['sharpe']:.2f}")
    for key, m in payload["markets"].items():
        st, r = m["sim"]["stats"]["strategy"], payload["regimes"][key]
        print(f"{key}: regime {r['label']} since {r['since']}  {m['counts']}  "
              f"picks sim sharpe {st['sharpe']:.2f} cagr {st['cagr']:.1%} maxdd {st['max_dd']:.1%}")
    print("crypto regime:", payload["regimes"]["CRYPTO"]["label"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
