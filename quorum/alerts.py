"""Phone alerts through ntfy.sh: no account, no key. Subscribe to the topic in the ntfy app."""
import json
import os
import secrets

import requests

from . import config as C

CONF = C.DATA / "alerts.json"
STATE = C.DATA / "alert_state.json"


def config():
    if os.environ.get("QUORUM_NTFY_TOPIC"):
        return {"topic": os.environ["QUORUM_NTFY_TOPIC"], "enabled": True}
    if not CONF.exists():
        C.DATA.mkdir(parents=True, exist_ok=True)
        CONF.write_text(json.dumps({"topic": "desk-" + secrets.token_urlsafe(12), "enabled": True}, indent=1))
    return json.loads(CONF.read_text())


def send(title, body, priority="default", tags=""):
    cfg = config()
    if not cfg.get("enabled"):
        return False
    try:
        r = requests.post("https://ntfy.sh/" + cfg["topic"], data=body.encode("utf-8"),
                          headers={"Title": title.encode("ascii", "replace").decode(), "Priority": priority,
                                   "Tags": tags}, timeout=10)
        return r.ok
    except Exception:
        return False


def _snapshot(payload):
    snap = {"regime": {k: v["label"] for k, v in payload["regimes"].items()}, "buy": [], "sell": [],
            "tickets": payload["meta"]["last_bar"] + ":" + str(len(payload["tickets"]))}
    for m in payload["markets"].values():
        snap["buy"] += [r["symbol"] for r in m["rows"] if r["status"] == "BUY"]
        snap["sell"] += [r["symbol"] for r in m["rows"] if r["status"] == "SELL"]
    return snap


def daily_digest(payload):
    """Send only what changed since the last run."""
    new = _snapshot(payload)
    old = json.loads(STATE.read_text()) if STATE.exists() else None
    sent = []
    names = {"US": "US stocks", "IN": "Indian stocks", "CRYPTO": "Crypto"}
    for k, label in new["regime"].items():
        if old is None or old["regime"].get(k) != label:
            was = f" (was {old['regime'][k]})" if old and k in old["regime"] else ""
            urgent = label in ("Crisis", "Bear market")
            sent.append(send(f"{names.get(k, k)}: {label}", payload["regimes"][k]["action"] + was,
                             "urgent" if urgent else "default", "rotating_light" if urgent else "bar_chart"))
    rows = {r["symbol"]: r for m in payload["markets"].values() for r in m["rows"]}
    fresh_sell = [s for s in new["sell"] if old is None or s not in old["sell"]]
    fresh_buy = [s for s in new["buy"] if old is None or s not in old["buy"]]
    if fresh_sell:
        lines = [f"{s}: {rows[s]['reason']}" for s in fresh_sell]
        sent.append(send(f"Sell signal: {', '.join(fresh_sell)}", "\n".join(lines), "high", "red_circle"))
    if fresh_buy:
        lines = [f"{s} near {rows[s]['price']}, sell if it closes below {rows[s]['stop']}" for s in fresh_buy]
        sent.append(send(f"Buy signal: {', '.join(fresh_buy)}", "\n".join(lines), "default", "green_circle"))
    if (old is None or old["tickets"] != new["tickets"]) and payload["tickets"]:
        sent.append(send(f"{len(payload['tickets'])} macro orders queued",
                         ", ".join(f"{t['side']} {t['symbol']}" for t in payload["tickets"][:8]), "low", "clipboard"))
    STATE.write_text(json.dumps(new, indent=1))
    return sent
