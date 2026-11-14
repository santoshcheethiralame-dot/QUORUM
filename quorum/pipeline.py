"""One call that rebuilds everything: macro book, stock picks, regimes, dashboard, alerts."""
from . import alerts, config as C, data, desk, engine, ledger, radar, site


def build(notify=True):
    px, health = data.load_panel(list(C.UNIVERSE))
    tiles, stress = radar.build()
    eng = engine.run(px, stress)
    book = ledger.update(eng, px)
    payload = site.build(eng, px, book, tiles, health, stress)
    payload.update(desk.build())
    site.write(payload)
    if notify:
        alerts.daily_digest(payload)
    return payload
