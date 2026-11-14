# Street Methods: Viral, Rumoured and Proven, With Verdicts

Compiled 15 Nov 2026. Third file in the set, after [quant-strategy-catalog.md](quant-strategy-catalog.md) and [quant-deep-dive.md](quant-deep-dive.md). Education and research only, not investment advice.

**Verdict scale**

- **PROVEN**: decades of out-of-sample or live evidence; still decays and still has bad years
- **PLAUSIBLE**: published support or a sound mechanism; needs our own test
- **MIXED**: some truth, mostly oversold
- **WEAK**: no reliable evidence of an edge after costs
- **RUMOUR**: unverifiable or contradicted by data
- **ILLEGAL**: do not do

"(memory)" marks facts not re-verified in this research pass.

---

## 1. The proven core (what everything else gets measured against)

| Method | Why it is in this tier | Known failure mode |
|---|---|---|
| Trend following across many futures/ETFs | A century of backtests plus live fund indices since 2000 (memory) | Long flat stretches, whipsaw in range-bound years |
| Cross-sectional momentum | Replicates across countries and asset classes | Sudden crashes after market rebounds |
| Value | Longest-studied factor; best factor of 2025 per Morningstar | Lost for a decade before that |
| Carry (FX, rates, commodities) | Persistent premium | Sharp unwinds (yen, Aug 2024) |
| Low risk / quality | Replicates after microcap controls | Among the worst factors in Q3 2026 per CME |
| Volatility risk premium (selling options) | Real, persistent premium | Rare catastrophic losses; must be sized small and gated |
| Short-term reversal / liquidity provision | Robust, strongest when volatility is high | Eaten by costs for slow traders |
| Post-earnings drift, index-rebalance, merger arbitrage | Structural causes | All have shrunk as capital crowded in |
| Volatility targeting and diversification | Improves risk-adjusted return of almost anything | Does not create return by itself |

Lesson from 2025-26 factor reports: leadership rotated every quarter or two (value, then momentum, then both lagging). No single factor is "the one". The proven approach is holding several at once.

## 2. Viral retail methods

### Chart-pattern schools

| Method | What it claims | Evidence | Verdict |
|---|---|---|---|
| ICT / Smart Money Concepts (order blocks, fair value gaps, liquidity sweeps, kill zones) | Institutions leave footprints you can trade | No peer-reviewed support. One independent test: order blocks held 82% vs 78% for random control zones on ES, 47% vs 51% on EUR/USD. Vendor win-rate claims are unpublished | **WEAK**. The testable kernel (stop-run reversal, gap fill) is ordinary mean reversion |
| Wyckoff, Elliott waves, Fibonacci, harmonics, Gann | Hidden market geometry | Nothing reproducible | **WEAK** |
| Indicator stacks on TradingView (SuperTrend, EMA crosses, RSI divergence, paid "signal" overlays) | A combination that "prints" | They are trend or reversion proxies; most retail backtests carry fill artefacts | **MIXED**. Fine as features, no magic |
| Volume profile, footprint, order-flow scalping | Read the tape like a desk | Real information, but retail lacks the speed and queue position to collect it | **WEAK** for retail |
| Breakout swing styles (VCP, CANSLIM, episodic pivots, Darvas) | Buy leaders breaking out on volume | Rides the proven momentum and earnings-drift factors; the discretionary part cannot be tested | **PLAUSIBLE** as momentum + drift |

### Quant-flavoured retail favourites

| Method | Evidence | Verdict |
|---|---|---|
| Opening-range breakout on "stocks in play" (Zarattini, Aziz, Barbon papers) | 5-minute range breakout on high-relative-volume stocks; one platform replication reported Sharpe near 2.4 vs 0.84 for buy-and-hold. Authors are tied to a trading firm; no independent critique found; very cost-sensitive | **PLAUSIBLE**. Needs intraday data and honest slippage |
| RSI(2), internal bar strength, 5-day-low, "Turnaround Tuesday" on index ETFs | Decades of blog backtests still reported positive on SPY/QQQ; all hypothetical. Mechanism is short-term reversal plus the equity premium | **PLAUSIBLE**. Cheap to test on daily data |
| Overnight drift (buy close, sell open) | Well documented; headline "38% a year, Sharpe 3" figures ignore costs | **PLAUSIBLE** anomaly, cost-fragile |
| Turn-of-month, pre-FOMC drift | Documented; effects weaken and shift days | **MIXED** |
| Dual momentum, 10-month moving-average allocation | Simple trend rules; sound, modest | **PROVEN** family, modest size |
| Leveraged ETF above 200-day average ("Leverage for the Long Run") | Volatility clusters below the average, so the filter avoids the worst decay (memory); it is trend following with leverage | **PLAUSIBLE**, whipsaw-prone |
| Leveraged stock + leveraged bond mix ("Hedgefundie's Excellent Adventure") | Down about 42% by May 2022 vs 12% for unlevered 60/40; simulated drawdowns of 67-74% | **MIXED**. Broke when stocks and bonds fell together |
| Buy-and-hold or DCA into 3x ETFs | Leverage is not an edge | **WEAK** |
| Return stacking, managed-futures ETFs | Diversification via trend | **PROVEN** family |

### Options crowd

| Method | Evidence | Verdict |
|---|---|---|
| The wheel, covered calls, cash-secured puts, 45-day premium selling | Harvests the volatility premium; small steady gains, occasional large loss | **PROVEN** premium, dangerous sizing |
| 0DTE condors and "theta gang" | Same premium at the shortest horizon; costs and gap risk dominate for retail (memory) | **MIXED** |
| Covered-call income ETFs | Yield is not return; typically lag the underlying in rallies | **MIXED** |
| Short-volatility ETPs when the VIX curve is in contango | Worked for years, then one product lost almost everything in a day in Feb 2018 | **PROVEN** premium, lethal tail |
| Gamma-exposure levels, max pain, "pinning" | Hedging flows are real; the published levels are inferred and vendors disagree | **MIXED**. Use for volatility regime, not price targets |
| Following "unusual options flow" feeds | Academic option signals exist; retail flow feeds are noisy | **WEAK** |

### Copy-the-insiders crowd

| Method | Evidence | Verdict |
|---|---|---|
| Congress trackers and ETFs | The Democrat-tracking fund behaves like a tech fund: up when AI rallies, down more when it falls (-4% vs -2% for the S&P to March 2026). Disclosures lag by weeks | **MIXED**. Mostly sector beta |
| Inverse-TV-pundit trades | A fund built on this closed after underperforming (memory) | **WEAK** |
| 13F cloning of famous investors | Works modestly for concentrated long-term holders; data is 45+ days stale | **PLAUSIBLE** |
| Reddit / meme sentiment | Attention spikes forecast volatility far better than direction | **MIXED**. Trade as a volatility signal |
| Paid signal groups, finfluencer calls, leaderboard copy-trading | Survivorship and incentives; regulators have acted against several | **WEAK** |

### AI-trader hype

| Claim | Evidence | Verdict |
|---|---|---|
| "I gave an LLM $10k and let it trade" | Alpha Arena, crypto season (ended Nov 2025): best model +22%, worst -63%, most lost. Stock contests: combined portfolio fell about a third, 6 of 32 runs positive. Failure causes: overtrading, bad timing. The organiser said handing money to an LLM is not yet viable | **WEAK** as an autonomous trader |
| LLMs as research assistants | Funds report real productivity gains with a human veto | **PROVEN** as tooling |
| Fleets of AI agents | One study found agents converge on the same strategies | Crowding risk, not edge |

### Crypto and prediction markets

| Method | Evidence | Verdict |
|---|---|---|
| Funding-rate farming | Real carry, now compressed (about 2.8% annualised mid-2026 on majors, one study) | **MIXED** |
| Grid bots, martingale, DCA bots | Short volatility in disguise; fail in trends | **WEAK** |
| Memecoin sniping, launch bots | Negative-sum for most participants (memory) | **WEAK** |
| Smart-wallet copy trading, liquidation heat maps | Occasionally informative; heavily gamed | **MIXED** |
| Airdrop and points farming | Returns have fallen as it professionalised | **MIXED** |
| Telegram pump groups | Organisers profit, members provide exit liquidity | **ILLEGAL** |
| Polymarket arbitrage bots | A study found about $40m of arbitrage profit from Apr 2023 to Apr 2024, mostly 1-5% per instance; 14 of the top 20 wallets were bots; they won on speed, not forecasting | **PLAUSIBLE** but a speed game |
| Prediction-market model-vs-market (weather, data releases) | Reachable without speed; thin liquidity | **PLAUSIBLE** |
| Copying "insider" wallets on prediction markets | Cannot separate luck from leaks; trading on leaked outcomes is the illegal part | **RUMOUR / ILLEGAL** |

### India-specific viral methods

| Method | Evidence | Verdict |
|---|---|---|
| 9:20 intraday short straddle | Became crowded; weekly-expiry cuts, bigger lots and higher taxes since late 2024 reduced it. No clean post-2024 performance data found | **MIXED**, eroded |
| Expiry-day "hero or zero" option buying | Lottery ticket | **WEAK** |
| Supertrend / CPR / EMA scalping, option-chain "OI analysis" | Indicator stacks again | **WEAK** to **MIXED** |
| BTST and upper-circuit chasing | Momentum with gap risk; attracts operators | **MIXED** |
| IPO grey-market-premium flipping | Works in hot markets, reverses hard in cold ones | **MIXED** |
| Marketplace algos on retail platforms | Survivorship in what gets advertised | **WEAK** |
| Tip channels and operator stocks | | **ILLEGAL** |

The base rate, from SEBI's own studies: about 91% of individual derivatives traders lost money in FY25 (net losses over ₹1 lakh crore), 87.7% lost in FY26, and of those active for five straight years, 65.6% lost in every single year. Studies in Brazil and Taiwan put persistent day-trading success near or below 1-3% (memory).

## 3. Rumoured institutional methods

| Rumour or report | Status |
|---|---|
| Medallion wins only about 50.75% of trades | Secondhand quote in a book; consistent with how such funds work |
| Renaissance keeps signals that have no explanation if the statistics hold, and has tested oddities such as weather | Reported in the same book (memory); not confirmed by the firm |
| Renaissance used basket options for leverage and tax treatment | Documented in a US Senate report (memory) |
| Jane Street moved the Bank Nifty index on expiry days | Alleged in SEBI's July 2025 interim order; firm disputes it; appeal still pending |
| "Jane Street dumps bitcoin at 10 am every day" (viral, Feb 2026) | **RUMOUR**. Two analysts checked the data and found the 10:00 window in line with normal volatility and with the Nasdaq |
| Hedge funds bought private exit polls on Brexit night | Reported by major press (memory) |
| Funds track corporate jets to predict deals | True; vendors sell it for six figures a year |
| "Pentagon pizza index" predicts military action | Meme; anecdotal |
| Bots trade on political leaders' social posts | Plausible and widely assumed; a bank once published an index of post-driven rate volatility (memory) |
| Well-timed option bets before tariff news, well-timed prediction-market bets before geopolitical events | Allegations reported, not proven; would be **ILLEGAL** if based on inside information (memory, not re-verified) |
| Dealers "hunt stops" and "pin" expiry | Hedging flows produce both effects; deliberate intent is unproven |
| Bank desks know where trend funds and volatility-control funds must buy or sell | They publish estimates; treat as estimates |
| Pod shops score sell-side ideas and run a central book on top of their own managers | Reported practice (alpha capture, centre book) |
| Market makers run very large GPU clusters for price forecasting | Reported by the firms themselves |
| Quant funds and AI labs are converging on the same talent and tooling | Reported in 2026 trade press |
| Payment-for-order-flow conspiracy behind meme-stock halts, "naked shorting" squeeze theories | Regulators found no support (memory) |
| State buying props up markets | Documented in China and Japan; rumour elsewhere |
| Stablecoin issuance pumps bitcoin | One academic paper argued it; contested |

## 4. What to take from the street

- **Keep as testable features:** stop-run reversal, gap fill, opening-range breakout, RSI(2) / bar-strength reversion, overnight vs intraday split, turn-of-month, attention spikes as volatility inputs, gamma regime as a volatility input, congressional and 13F holdings as slow tilts.
- **Keep as lessons:** leverage is not edge; premium selling needs a regime gate and small size; anything viral is already crowded; a strategy that needs you to be faster than a bot is not yours.
- **Reject:** pattern schools without definitions, signal groups, autonomous LLM trading, martingale-style bots, anything relying on leaks.
- **Rule for every candidate:** write the rule down first, test on data the idea never saw, charge realistic costs, then paper trade before it gets any weight.

---

## Sources checked for this pass

- ICT tests: https://algostorm.com/ict-smc-key-concepts/ and https://statoasis.com/overfit/research/ict-backtest-what-survives and https://www.xs.com/en/test-blog/smc-smart-money-concepts-explained/
- Opening-range breakout: https://papers.ssrn.com/abstract=4416622 and https://concretumgroup.com/a-profitable-day-trading-strategy-for-the-u-s-equity-market/ and https://www.cxoadvisory.com/technical-trading/day-trading-with-an-opening-range-breakout-strategy
- Alpha Arena and LLM traders: https://protos.com/llm-crypto-trading-contest-finds-llms-cant-trade-crypto and https://news.bloombergtax.com/banking-law/ai-bots-auditioning-for-wall-street-trading-are-mostly-losing and https://www.thinkadvisor.com/amp/2026/05/06/why-ai-bots-arent-ready-to-replace-your-fund-manager/
- Polymarket bots: https://www.financemagnates.com/trending/prediction-markets-are-turning-into-a-bot-playground/ and https://dlnews.com/articles/markets/polymarket-users-lost-millions-of-dollars-to-bot-like-bettors-over-the-past-year/
- Congress ETFs: https://www.morningstar.com/funds/does-it-pay-copy-congress-stock-trades-2 and https://www.etf.com/sections/etf-basics/nanc-vs-kruz-battle-congress-stock-trackers and https://247wallst.com/investing/2026/03/17/turn-congressional-stock-disclosures-like-pelosis-into-a-30-return-the-easy-way/
- Leveraged-ETF forum record: https://lr.in.psf.lt/r/Bogleheads/comments/upbzkg/hedgefundies_excellent_adventure_update_this
- SEBI loss studies: https://www.business-standard.com/markets/news/net-losses-of-traders-in-fo-widens-in-fy25-sebi-study-125070701221_1.html and https://www.finnovate.in/learn/blog/sebi-fno-trader-losses-fy26-individual-derivatives and https://tradingqna.com/t/win-rate-capital-experience-what-sebi-found-about-f-o-traders/197266
- Bitcoin 10 am rumour: https://cointelegraph.com/news/bitcoin-10am-dump-theory-jane-street-ibit-13f-terraform-lawsuit and https://www.fxstreet.com/cryptocurrencies/news/bitcoin-falls-to-65-000-as-experts-reject-conspiracy-claims-against-jane-street-202602271918
- Factor performance 2025-26: https://indexes.morningstar.com/insights/markets-review/blt102b1255cddffd67 and https://www.cmegroup.com/articles/2026/factors-2026-q3-review-q4-outlook-with-factor-futures.html and https://www.wisdomtree.com/nl/insights/blog/looking-back-at-equity-factors-in-q2-2026-with-wisdomtree
- Retail reversion backtests: https://quantifiedstrategies.substack.com/p/3-technical-indicator-strategies and https://algorithmictoken.substack.com/p/strategy-lab-3-the-signals-that-dont
