# Quorum

A paper-trading desk where every strategy votes and one net position per instrument comes out. Paper only. Not investment advice.

Live desk: https://santoshcheethiralame-dot.github.io/QUORUM/

## Run it

```bash
python run.py
```

That pulls free daily prices, computes each strategy's forecast, updates the paper ledger, and rebuilds `site/index.html`. Open that file in a browser, or serve it:

```bash
python -m http.server 8877 --directory site
```

Run it once a day after the US close. Orders decided at one close fill at the next open, so the ledger only moves when a new day of prices exists. Re-running on the same day changes nothing.

```bash
python -m pytest tests -q
```

## How it works

1. `quorum/data.py` pulls daily bars for 16 instruments (stocks, bonds, gold, commodities, real estate, the dollar, two crypto) and caches them in `data/cache`.
2. `quorum/engine.py` gives each strategy a forecast from -20 to +20 per instrument, adds them into one net forecast, sizes positions by volatility, then applies the risk limits.
3. `quorum/ledger.py` keeps the paper account in `data/ledger.json`: pending orders, fills, account value.
4. `quorum/radar.py` builds the market readings on the Radar page.
5. `quorum/site.py` writes everything into the dashboard.

All knobs are in `quorum/config.py`.

## Strategies today

| Sleeve | Status | What it does |
|---|---|---|
| Trend | Live | Follows multi-month price trends on every instrument |
| Calendar | Live | Holds stock funds over the turn of the month |
| Reversion | Shadow | Buys short-term dips in stock funds. Computed and shown, moves no money |

Reversion is in shadow because it tripled trading (24x to 67x capital a year) for about 9% gross over 16 years, which loses after costs. `python tests/compare_mixes.py` reproduces that comparison. A sleeve leaves shadow by paying for its own costs.

## Simulated history, 2011 to Nov 2026

Return 6.7% a year, swing 10.5%, return per unit of risk 0.67, deepest fall 18.6%, 55% of days positive. US stocks over the same window: 14.1% a year, 0.88, deepest fall 32%. The Lab page lists what the simulation leaves out.

## In the cloud

`.github/workflows/daily.yml` runs the daily job on GitHub Actions after the Indian close (10:45 UTC) and the US close (22:15 UTC), Monday to Friday. It runs the tests, rebuilds the signals, commits the paper ledger back to the repo, and publishes `site/` to GitHub Pages. It can also be started by hand from the Actions tab.

The hosted page has no server behind it, so it opens the public price streams itself (Yahoo and Binance websockets) and stays live in the browser. It also carries the last session's one-minute candles. Live stop alarms show on the page; phone alerts come from the daily run only.

One-time setup on GitHub: Settings, Pages, Source: GitHub Actions. For phone alerts, add a repository secret `QUORUM_NTFY_TOPIC` with your ntfy topic.

Run `python serve.py` locally for the full live desk with phone alerts on stop breaks.

## Not built yet

- India tickets, crypto carry, the volatility sleeve, the stock ranker
- Real company and trade data on the Radar (it uses price-based stand-ins)

Design and research notes are in `docs/`.
