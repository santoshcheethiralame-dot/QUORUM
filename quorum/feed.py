"""Free streaming quotes. One websocket, every symbol; messages are base64 protobuf."""
import asyncio
import base64
import json
import struct
import time

import aiohttp

URL = "wss://streamer.finance.yahoo.com/?version=2"
FIELDS = {1: "id", 2: "price", 3: "time", 8: "change_pct", 10: "high", 11: "low", 12: "change",
          15: "open", 16: "prev_close", 7: "hours"}


def _varint(b, i):
    shift = value = 0
    while True:
        c = b[i]
        i += 1
        value |= (c & 0x7F) << shift
        if not c & 0x80:
            return value, i
        shift += 7


def decode(raw):
    out, i = {}, 0
    while i < len(raw):
        tag, i = _varint(raw, i)
        field, wire = tag >> 3, tag & 7
        if wire == 0:
            v, i = _varint(raw, i)
            if field == 3:
                v = (v >> 1) ^ -(v & 1)
        elif wire == 5:
            v = struct.unpack_from("<f", raw, i)[0]
            i += 4
        elif wire == 1:
            v = struct.unpack_from("<d", raw, i)[0]
            i += 8
        elif wire == 2:
            n, i = _varint(raw, i)
            v = raw[i:i + n]
            i += n
        else:
            break
        if field in FIELDS:
            out[FIELDS[field]] = v.decode("utf-8", "replace") if isinstance(v, bytes) else v
    return out


async def stream(symbols, on_tick, status=None):
    """Reconnects forever. Calls on_tick(dict) for every quote."""
    backoff = 1
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.ws_connect(URL, heartbeat=20, headers={"User-Agent": "Mozilla/5.0"}) as ws:
                    await ws.send_str(json.dumps({"subscribe": list(symbols)}))
                    backoff = 1
                    if status:
                        status("connected")
                    async for msg in ws:
                        if msg.type != aiohttp.WSMsgType.TEXT:
                            continue
                        try:
                            body = json.loads(msg.data).get("message")
                            tick = decode(base64.b64decode(body)) if body else None
                        except Exception:
                            continue
                        if tick and "id" in tick and "price" in tick:
                            tick["recv"] = time.time()
                            on_tick(tick)
        except Exception as exc:
            if status:
                status(f"reconnecting ({type(exc).__name__})")
        await asyncio.sleep(backoff)
        backoff = min(30, backoff * 2)


if __name__ == "__main__":
    seen = []

    async def main():
        task = asyncio.create_task(stream(["BTC-USD", "ETH-USD", "SOL-USD", "EURUSD=X", "INR=X"],
                                          lambda t: seen.append(t), print))
        await asyncio.sleep(12)
        task.cancel()

    asyncio.run(main())
    print(len(seen), "ticks in 12s")
    for t in seen[:4]:
        print(t)
