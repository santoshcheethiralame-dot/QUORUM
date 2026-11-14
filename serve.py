"""Live desk: serves the dashboard and pushes market prices to it every second.

    python serve.py          then open http://localhost:8877
"""
import asyncio
import json
import os
import time
from collections import deque

from aiohttp import ClientSession, WSMsgType, web

from quorum import alerts, config as C, data, feed, pipeline

PORT = int(os.environ.get("PORT", 8877))
LATEST = C.DATA / "latest.json"
REBUILD_AFTER_H = 6
MOVE = {"^GSPC": 0.02, "^IXIC": 0.025, "^NSEI": 0.02, "^VIX": 0.20, "GC=F": 0.025, "CL=F": 0.05,
        "BTC-USD": 0.06, "ETH-USD": 0.08}
HELD_MOVE = 0.06

S = {"quotes": {}, "stops": {}, "last": {}, "chg": {}, "seen": {}, "dirty": {}, "hist": {}, "clients": set(),
     "alerts": deque(maxlen=60), "fresh": [], "fired": set(), "ticks": 0, "intraday": {},
     "feeds": {"yahoo": "starting", "binance": "starting"}, "symbols": []}


def load():
    p = json.loads(LATEST.read_text(encoding="utf-8"))
    S["quotes"] = p["quotes"]
    S["symbols"] = p["live_symbols"]
    S["stops"] = {r["symbol"]: r["stop"] for m in p["markets"].values() for r in m["rows"]
                  if r["status"] in ("HOLD", "SELL") and r["stop"]}


def fire(key, level, title, body, tags):
    day = time.strftime("%Y-%m-%d")
    if (key, day) in S["fired"]:
        return
    S["fired"].add((key, day))
    a = {"t": int(time.time()), "level": level, "title": title, "body": body}
    S["alerts"].appendleft(a)
    S["fresh"].append(a)
    asyncio.get_running_loop().run_in_executor(
        None, alerts.send, title, body, "high" if level == "crit" else "default", tags)


def check(sym, price, chg):
    stop = S["stops"].get(sym)
    if stop and price < stop:
        fire(("stop", sym), "crit", f"{sym} is below its stop",
             f"Trading at {price:,.2f}, stop is {stop:,.2f}. The sell rule triggers if it closes below.", "red_circle")
    limit = MOVE.get(sym) or (HELD_MOVE if stop else None)
    if limit and chg is not None and abs(chg) >= limit:
        name = S["quotes"].get(sym, {}).get("name", sym)
        fire(("move", sym), "warn", f"{name} {'up' if chg > 0 else 'down'} {abs(chg):.1%} today",
             f"Now {price:,.2f}.", "chart_with_upwards_trend" if chg > 0 else "chart_with_downwards_trend")


def on_tick(sym, price, chg=None, src="yahoo"):
    if not price or price != price or price <= 0:
        return
    if src == "yahoo" and sym in C.BINANCE and S["feeds"]["binance"] == "connected":
        return
    ref = S["quotes"].get(sym, {}).get("ref")
    if chg is None and ref:
        chg = price / ref - 1
    price = float(f"{price:.7g}")
    S["last"][sym], S["chg"][sym], S["seen"][sym] = price, chg, time.time()
    S["dirty"][sym] = [price, None if chg is None else round(chg, 5)]
    S["ticks"] += 1
    check(sym, price, chg)


def yahoo_tick(t):
    ts = t.get("time") or 0
    ts = ts / 1000 if ts > 1e11 else ts
    if ts and time.time() - ts > 300:
        return      # a replayed quote from a closed market, not a live trade
    pc = t.get("change_pct")
    on_tick(t["id"], t["price"], None if pc is None else pc / 100)


async def binance():
    url = "wss://data-stream.binance.vision/stream?streams=" + "/".join(v + "@miniTicker" for v in C.BINANCE.values())
    back = {v.upper(): k for k, v in C.BINANCE.items()}
    wait = 1
    while True:
        try:
            async with ClientSession() as session:
                async with session.ws_connect(url, receive_timeout=40) as ws:
                    S["feeds"]["binance"], wait = "connected", 1
                    async for msg in ws:
                        if msg.type != WSMsgType.TEXT:
                            continue
                        d = json.loads(msg.data).get("data") or {}
                        if d.get("s") in back:
                            on_tick(back[d["s"]], float(d["c"]), src="binance")
        except Exception:
            pass
        S["feeds"]["binance"] = "reconnecting"
        await asyncio.sleep(wait)
        wait = min(30, wait * 2)


async def broadcast():
    while True:
        await asyncio.sleep(1)
        now = time.time()
        for sym, seen in S["seen"].items():
            if now - seen < 180:
                S["hist"].setdefault(sym, deque(maxlen=1800)).append([int(now), S["last"][sym]])
        body = {"t": int(now), "q": S["dirty"], "n": S["ticks"], "feeds": S["feeds"]}
        if S["fresh"]:
            body["a"] = S["fresh"]
        S["dirty"], S["fresh"], S["ticks"] = {}, [], 0
        line = ("data: " + json.dumps(body, separators=(",", ":")) + "\n\n").encode()
        for q in list(S["clients"]):
            try:
                q.put_nowait(line)
            except asyncio.QueueFull:
                S["clients"].discard(q)


async def rebuild():
    """Refresh the daily signals when they go stale, then tell open pages to reload."""
    loop = asyncio.get_running_loop()
    while True:
        await asyncio.sleep(900)
        if time.time() - LATEST.stat().st_mtime > REBUILD_AFTER_H * 3600:
            try:
                await loop.run_in_executor(None, pipeline.build)
                load()
                line = b'data: {"reload":true}\n\n'
                for q in list(S["clients"]):
                    q.put_nowait(line)
            except Exception as exc:
                print("rebuild failed:", exc)


async def stream(request):
    resp = web.StreamResponse(headers={"Content-Type": "text/event-stream", "Cache-Control": "no-cache"})
    await resp.prepare(request)
    q = asyncio.Queue(maxsize=60)
    now = time.time()
    hello = {"t": int(now), "n": 0, "feeds": S["feeds"], "alerts": list(S["alerts"]),
             "q": {s: [p, None if S["chg"].get(s) is None else round(S["chg"][s], 5)]
                   for s, p in S["last"].items() if now - S["seen"][s] < 180}}
    await resp.write(("data: " + json.dumps(hello, separators=(",", ":")) + "\n\n").encode())
    S["clients"].add(q)
    try:
        while True:
            await resp.write(await q.get())
    except (ConnectionResetError, ConnectionError, asyncio.CancelledError):
        pass
    finally:
        S["clients"].discard(q)
    return resp


async def intraday(request):
    sym = request.query.get("s", "")
    if sym not in S["quotes"]:
        return web.json_response({"error": "unknown symbol"}, status=404)
    hit = S["intraday"].get(sym)
    if not hit or time.time() - hit[0] > 45:
        try:
            body = await asyncio.get_running_loop().run_in_executor(None, data.intraday, sym)
        except Exception:
            body = {"symbol": sym, "points": [], "prev_close": None, "price": None}
        hit = S["intraday"][sym] = (time.time(), body)
    return web.json_response(dict(hit[1], recent=list(S["hist"].get(sym, []))))


async def phone(request):
    cfg = alerts.config()
    return web.json_response({"topic": cfg["topic"], "enabled": cfg.get("enabled", True),
                              "url": "https://ntfy.sh/" + cfg["topic"]})


async def test_alert(request):
    ok = await asyncio.get_running_loop().run_in_executor(
        None, alerts.send, "Quorum test alert", "If you can read this on your phone, alerts work.", "default", "bell")
    return web.json_response({"ok": bool(ok)})


async def index(request):
    return web.FileResponse(C.SITE / "index.html", headers={"Cache-Control": "no-store"})


async def start(app):
    app["tasks"] = [asyncio.create_task(feed.stream(S["symbols"], yahoo_tick,
                                                    lambda s: S["feeds"].__setitem__("yahoo", s))),
                    asyncio.create_task(binance()), asyncio.create_task(broadcast()), asyncio.create_task(rebuild())]


async def stop(app):
    for t in app["tasks"]:
        t.cancel()


def main():
    if not LATEST.exists() or time.time() - LATEST.stat().st_mtime > REBUILD_AFTER_H * 3600:
        print("signals are stale, rebuilding first...")
        pipeline.build()
    load()
    app = web.Application()
    app.add_routes([web.get("/", index), web.get("/stream", stream), web.get("/intraday", intraday),
                    web.get("/phone", phone), web.post("/test-alert", test_alert)])
    app.on_startup.append(start)
    app.on_cleanup.append(stop)
    print(f"Quorum live desk: http://localhost:{PORT}  ({len(S['symbols'])} symbols)")
    web.run_app(app, host="127.0.0.1", port=PORT, print=None)


if __name__ == "__main__":
    main()
