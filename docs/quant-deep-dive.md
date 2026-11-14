# Quant Deep Dive: Best Algorithms, Evidence, Firm Practice, New-Gen Market Drivers

Compiled 15 Nov 2026. Companion to [quant-strategy-catalog.md](quant-strategy-catalog.md). The catalog lists *what exists*; this file says *what works best, how the top firms run it, and what moves markets now*. Education and research only, not investment advice.

Items marked **(unverified)** come from memory or a single weak source and were not confirmed in this research pass.

---

## 1. The ceiling on "accuracy" (read this first)

"Highest accuracy in predicting the market" is the wrong target. The public evidence:

| Fact | Number | Source quality |
|---|---|---|
| Renaissance Medallion win rate | about 50.75% of trades | Secondhand (Mercer quote via Zuckerman's book) |
| Best ML models, monthly stock-level out-of-sample R² | about 0.3-0.4% | Gu-Kelly-Xiu, via secondary summary |
| Linear model with 900+ raw predictors | negative out-of-sample R² | Same |
| General time-series foundation models on returns | R² of -1.4% to -2.8%, direction near 50-51% | Rahimikia et al., Nov 2025 |
| Published anomalies after publication | lose over half their return | McLean-Pontiff |

What the best firms optimise instead:

- **Edge × breadth.** Risk-adjusted return scales roughly as (skill per bet) × √(number of independent bets). A 51% edge on millions of bets beats a 60% edge on ten.
- **Net of costs.** Most ML return-prediction profit sits in small, illiquid, hard-to-short stocks and shrinks sharply once costs are charged **(unverified citation: Avramov-Cheng-Metzker)**.
- **Sizing and survival.** Volatility targeting and hard drawdown stops matter more than a marginal point of accuracy.

**What is actually predictable, most to least**

1. Volatility (strongly persistent; simple models explain a large share of next-day variance)
2. Correlations and betas (moderately persistent)
3. Mechanical flows (index rebalances, expiry hedging, forced selling): known in advance, edge is in sizing and timing
4. Company fundamentals one quarter out (revenue nowcasts from alt data)
5. Order flow over seconds (real signal, but needs speed and queue priority to collect)
6. Relative returns across many stocks (tiny per-stock edge, tradeable through breadth)
7. Index direction day to day (close to a coin flip; nobody credible claims much above 52-54%)

Design implication: predict 1-4 well and 6 broadly; do not build the system around 7.

## 2. Algorithm scoreboard by task

| Task | What the evidence favours | Notes |
|---|---|---|
| Cross-sectional stock ranking (daily to monthly) | Gradient-boosted trees (LightGBM, XGBoost, CatBoost) plus shallow neural nets, ensembled | Gu-Kelly-Xiu: trees and neural nets best, gains come from nonlinear interactions; shallow beats deep; the dominant inputs are momentum, liquidity, volatility |
| Combining many weak signals | Ridge / IC-weighted blends, stacking, large ensembles | The most consistent winner across papers and competitions |
| Volatility forecasting | HAR-RV, GARCH family, realised-range estimators; boosted trees on HAR features; implied vol as an input | Highest-accuracy problem in finance; feeds sizing, options, regime filters |
| Regime detection | Hidden Markov / Markov-switching models, change-point detection | Use to scale risk, not to call direction |
| Pairs and spreads | Cointegration tests, Kalman-filter hedge ratios, Ornstein-Uhlenbeck thresholds | Mature and transparent |
| Intraday / order-book prediction | Order-flow-imbalance linear models first; DeepLOB (CNN+LSTM), TLOB (transformer, 2025) | Benchmarks find these models fail to generalise across assets and regimes; predictability has declined over time; latency and costs erase paper gains |
| Sequence models on daily bars | LSTM, temporal CNN, transformers | Rarely beat boosted trees on daily data; earn their keep on intraday data at scale |
| Time-series foundation models | Chronos, TimesFM, Moirai, TimeGPT; finance-specific Kronos | Off-the-shelf general models underperform on returns and fine-tuning does not close the gap; Kronos reports large rank-IC gains but only in its own paper |
| "More parameters is better" | Random-feature ridge models (Kelly-Malamud-Zhou "virtue of complexity") | Contested: Nagel (2025) argues the effect is largely an illusion that reduces to a simple momentum-like rule |
| Text signals | Finance dictionaries, FinBERT, LLM embeddings and headline scoring, filing-diff detection | Real but decays quickly; LLM backtests leak the future unless the model's knowledge cutoff precedes the test period |
| Alpha discovery | Genetic programming / symbolic regression over price-volume expressions; LLM-driven formula search | WorldQuant-style; value is in volume and low correlation, not any single formula |
| Execution | Almgren-Chriss scheduling, square-root impact model; reinforcement learning for order placement | RL has limited public production evidence |
| Market making | Avellaneda-Stoikov and successors (inventory-aware quoting) | Needs infrastructure; fine to study on crypto |
| Portfolio construction | Ledoit-Wolf shrinkage, hierarchical risk parity, risk parity, volatility targeting, fractional Kelly | Robust methods beat raw mean-variance out of sample |
| Labels | Cross-sectional rank targets, volatility-normalised returns, triple-barrier labels, meta-labeling | Label design often matters more than model choice |
| Validation | Walk-forward, purged k-fold with embargo, combinatorial purged CV, deflated Sharpe, probability of backtest overfitting | Non-negotiable; with 45 tries, luck alone yields a Sharpe above 1.5 |

**Competition evidence (closest thing to a public leaderboard of methods)**

- Optiver "Trading at the Close" (2023): winning entry was a CatBoost + GRU + Transformer ensemble with online retraining **(unverified; from memory of the Kaggle write-up)**. A published paper on the contest confirms that feeding revealed targets back into LightGBM online was a major gain.
- Jane Street Real-Time Market Data Forecasting (2024-25): top entries combined sequence neural nets with boosted trees and learned online during the test period **(unverified)**. Metric was weighted zero-mean R², and winning scores were around 1% R², which is what "state of the art" looks like on real data.
- Numerai: boosted trees on era-structured data, feature neutralisation, heavy ensembling **(unverified in this pass; widely documented on its forum)**.

Common thread: boosted trees + a modest neural net, ensembled, retrained continuously, on carefully engineered features.

## 3. Ten things the research converges on

1. Breadth beats accuracy.
2. Old, simple features carry most of the signal: momentum, short-term reversal, liquidity, volatility.
3. Nonlinear interactions add a little; depth adds nothing on daily data.
4. Markets drift, so retrain on a rolling basis and weight recent data.
5. Ensembles of weak, uncorrelated signals beat any single strong model.
6. Costs decide. A signal that needs daily turnover in small caps is usually not real money.
7. Every published edge decays. Budget for half.
8. Predict relative, trade neutral. Ranking stocks against each other is easier than calling the index.
9. Data quality beats model choice. Point-in-time, survivorship-free, correctly adjusted.
10. Size by volatility, cut by drawdown, and paper trade before believing anything.

## 4. Top-firm practice (public record only)

| Firm | Practice worth copying | Source type |
|---|---|---|
| Renaissance | One shared model and codebase everyone can see; obsessive data cleaning; short horizons; market-neutral; tiny edge at huge breadth with leverage; fund size capped | Zuckerman's book, filings |
| Jane Street | ML treated as an end-to-end engineering system (data quality, modelling, production feedback loop); traders, researchers and engineers on one team; expected-value thinking drilled with mock trading | Its own blog and podcast |
| Two Sigma | Data and engineering scale; thousands of datasets; many models combined | Public talks |
| D. E. Shaw | Blend of systematic and discretionary; rigorous hiring | Public record |
| AQR | Publishes its research; diversify across value, momentum, carry, defensive and across asset classes; hold through drawdowns | Its papers |
| Man AHL | Trend plus ML; internal LLM research assistant (AlphaGPT) that drafts but does not trade | Firm publications, trade press |
| WorldQuant | "Alpha factory": millions of small formulaic alphas, then combination | Its papers |
| Citadel, Millennium, Point72 | Many independent market-neutral books; factor exposure stripped out; automatic capital cuts on drawdown; central risk book on top | Trade press; exact limits not public |
| Bridgewater | Decision rules written down and systematised; AI lab with humans signing off | Public record |
| HRT, Jump, Tower, XTX | Simulator fidelity, latency engineering, ML price forecasts at scale | Engineering blogs, job posts |
| Numerai | Crowd-sourced ensemble on obfuscated data, contributors stake on their own models | Its docs |
| López de Prado school | Purged CV, deflated Sharpe, meta-labeling, "backtesting is not a research tool" | Books and papers |

2026 state of LLMs at funds, per trade-press reporting: used to speed research, summarise, and write code; every reported success keeps a human veto; LLM-derived alpha is expected to decay within a couple of years; one study found AI trading agents converge on similar strategies, which is a crowding risk.

## 5. New-generation market deciders

### 5a. Semiconductor cycle dashboard

Chips lead the tech cycle, and the supply chain publishes unusually frequent free data.

| Indicator | Cadence | Why it matters |
|---|---|---|
| TSMC monthly revenue | Monthly, about the 10th | Fastest hard number on AI and leading-edge demand (first month above NT$500bn reported for Sept 2026, single source) |
| Other Taiwan-listed monthly revenues (design-service houses, packaging, server builders) | Monthly, by the 10th | Design-service firms get paid before foundries, so they lead; server builders proxy AI-server shipments |
| Korea exports, first 10 and 20 days and full month | Three times a month | Memory is about three quarters of Korean chip exports; earliest global trade read |
| DRAM and NAND spot vs contract prices | Daily / monthly | Spot leads contract; a spot rollover lasting 60+ days is a classic peak warning |
| Semiconductor billings (WSTS/SIA), equipment billings (SEMI, Japan's SEAJ) | Monthly | Cycle confirmation |
| Micron results | Quarterly, off-cycle | Reports a month before peers, so it previews memory |
| ASML order intake, TSMC capex guidance | Quarterly | Two-year-forward capacity signal |
| Advanced-packaging and high-bandwidth-memory capacity | Irregular | The current bottlenecks; HBM reported sold out through 2026 |
| Inventory days, lead times | Quarterly / vendor | Rising inventory with falling lead times marks the turn `[D]` |
| Chip index relative to the broad market | Daily | Risk-appetite and cycle lead |

Policy layer to track (status as last reported; verify before relying on it):

- US Section 232 tariff of 25% on a narrow set of advanced AI chips from January 2026, tied to permitting certain Nvidia and AMD sales into China
- China weighing its own limits on imported high-end chips; continuing rare-earth and critical-mineral export curbs
- Broader US chip tariffs flagged as possible; tariffs on Chinese legacy chips delayed to June 2027
- Taiwan Strait risk: most leading-edge chips are still made there

### 5b. AI trade dashboard

| What to watch | Reading |
|---|---|
| Hyperscaler capex guidance | 2026 estimates range from about $650bn to $800bn depending on source; direction of revisions matters more than level |
| Capex vs operating cash flow | Spending above cash flow means debt-funded build-out |
| Hyperscaler and data-centre debt issuance, private-credit deals | 2026 bond issuance reportedly passed all of 2025 by June |
| AI revenue vs capex gap | One source: about $60-70bn annualised AI revenue at two hyperscalers against about $400bn of their 2026 capex |
| GPU rental prices | H100 around $3.5/hour in Nov 2026 on one tracker, rising; wide gap between specialist clouds and hyperscalers. Rising rents = compute still scarce |
| Token prices and volumes | Token prices reportedly hit a record low in Sept 2026; falling price with rising volume is healthy, falling price with flat volume is not |
| Specialist-cloud and leveraged-AI-name stress | Sharp drawdowns reported in several such names in 2026; treat as canaries, along with their credit spreads |
| Vendor / circular financing | Suppliers funding customers who buy from them; theme flagged widely, details not confirmed in this pass |
| Model-release shocks | Jan 2025 (cheap Chinese model release hit chip stocks); Feb 2026 "SaaSpocalypse" (agent and plugin releases triggered a software selloff put at $285bn to over $1tn, Nifty IT fell 6.8% in a session, foreign investors sold Indian IT heavily) |
| Winners vs losers baskets | Winners cited: chips, equipment, memory, networking, power and electrical equipment, cooling, utilities with contracted load, cybersecurity, data infrastructure. Losers cited: per-seat workflow software, IT services and outsourcing, speculative pre-revenue power developers |
| Power bottleneck | Gas turbines reported sold out for years, transformer lead times two to four years; US grid demand projected up about 25% by 2030 |
| Physical build tracking `[D]` | Satellite construction progress, grid-interconnection queues, large-load requests to utilities, permits, turbine order books |
| Adoption data `[R]` | Business AI-use surveys, AI-app downloads and usage, developer package downloads, AI job postings |
| Valuation and positioning | Index concentration in a few names, earnings share of the largest firms, leveraged single-stock ETF flows, options skew |
| Bubble checklist | Debt-funded capex, vendor financing, IPO wave, insider selling, margin debt. One Oct 2026 checklist judged the peak not yet reached; no lab or hyperscaler default as of Nov 2026 |
| Politics | Local opposition to data centres and electricity-price politics (one 2026 report ties a power-stock selloff to this; single source) |

Why this matters for a quant system: AI exposure is now a risk factor in its own right. A "market-neutral" book that is long AI beneficiaries and short AI losers is one concentrated bet. Measure it like a sector.

### 5c. Other emerging deciders

| Theme | What to monitor |
|---|---|
| Physical AI and humanoid robots | Shipment counts, pilot deployments, component supply (actuators, reducers, rare-earth magnets) |
| Quantum computing | Technical milestones, government funding; stocks trade on retail momentum |
| Space economy | Launch cadence, satellite-broadband subscribers, large listings (a 2026 SpaceX IPO is cited in one issuer outlook; verify) |
| Nuclear, small modular reactors, uranium | Offtake deals with data centres, licensing milestones, physical-uranium trust flows |
| Grid, storage, gas turbines | Order backlogs, lead times, interconnection reforms |
| Rare earths and critical minerals | China refines about 90% of rare earths; export-licence regimes, state offtake and price-floor deals |
| Defence tech and drones | European rearmament budgets, order backlogs, procurement shifts toward autonomy |
| Stablecoins and tokenisation | Stablecoin supply (now a buyer of Treasury bills), tokenised stocks and 24/7 trading, equity perpetuals |
| Prediction markets | Odds as a real-time information layer; record volumes in 2026 |
| Obesity drugs (GLP-1) | Weekly prescription data; second-order effects on food and medical devices |
| Private credit | Fund redemptions and outflows (reported in late 2025 and Q1 2026), marks vs public comparables |
| Retail flow, 0DTE, leveraged ETFs | Share of options volume, single-stock leveraged-ETF rebalancing |
| Passive concentration | Inelastic flows amplifying the largest names |
| Tariffs and industrial policy | Sector-specific duties, state equity stakes, subsidy programmes |
| Gold and reserve diversification | Central-bank purchases, real yields decoupling |
| Crypto treasury companies | Premium to net asset value, forced-selling risk |
| AI agents as traders | Strategy herding and faster alpha decay |
| India-specific | Domestic SIP flows offsetting foreign selling; IT-services exposure to AI; expiry and algo-rule changes |

## 6. Edge map for one person

Where a solo builder can be competitive, given everything above:

- **Yes:** volatility forecasting and vol-scaled sizing; cross-sectional ranking with boosted trees on liquid names at weekly or monthly horizons; trend and carry on futures or ETFs; calendar and forced-flow events; crypto funding and basis monitoring; free high-frequency macro and chip-cycle dashboards; text signals from filings and announcements.
- **Maybe:** pairs and stat arb (costs are tight); prediction-market mispricing; earnings nowcasts from scraped data.
- **No:** latency games, market making in listed markets, fixed-income relative value, anything needing paid alt-data panels or prime-broker leverage.

A sound first architecture: clean point-in-time data, a feature store, a boosted-tree ranker plus a volatility model plus a regime filter, a simple blend, volatility-targeted and neutralised sizing, paper execution, and a live-vs-backtest monitor. Strategy selection for that pipeline is the next step.

---

## Sources checked for this pass

Algorithms and evidence
- Gu, Kelly, Xiu, *Empirical Asset Pricing via Machine Learning*: https://www.nber.org/papers/w25398.pdf and https://www.aqr.com/insights/research/journal-article/empirical-asset-pricing-via-machine-learning
- Rahimikia et al., *Re(Visiting) Time Series Foundation Models in Finance*: https://arxiv.org/html/2511.18578v1
- *Pretrained Time-Series Foundation Models for Financial Return Forecasting*: https://arxiv.org/pdf/2606.27100
- Kronos (NeurIPS 2025): https://neurips.cc/virtual/2025/132504
- TLOB: https://arxiv.org/abs/2502.15757
- LOB representation-learning benchmark: https://arxiv.org/pdf/2505.02139
- Kelly, Malamud, Zhou, *The Virtue of Complexity in Return Prediction*: https://www.sfi.ch/en/publications/the-virtue-of-complexity-in-return-prediction
- Nagel, *Seemingly Virtuous Complexity in Return Prediction*: https://conference.nber.org/conf_papers/f221481/f221481.pdf
- Optiver contest paper (online target feedback): https://www.esann.org/sites/default/files/proceedings/2024/ES2024-159.pdf
- Backtest overfitting practice: https://quantpedia.com/why-machine-learning-funds-fail/
- Medallion hit rate: https://www.institutionalinvestor.com/article/b1k2fymby99nj0/Famed-Medallion-Fund-Stretches-Explanation-to-the-Limit-Professor-Claims

Firm practice
- Jane Street, *Real world machine learning*: https://blog.janestreet.com/real-world-machine-learning-part-1/
- AI use at hedge funds: https://resonanzcapital.com/insights/ai-use-by-hedge-funds-made-tangible-from-lego-bots-to-alpha-assistants
- LLMs in quant research: https://www.zerve.ai/blog/llms-in-quantitative-research

Chips
- TSMC revenue and peak-out debate: https://view.asiae.co.kr/en/article/2026081109561537661
- Semiconductor cycle read-through: https://en.macromicro.me/blog/assessing-the-semiconductor-cycle-by-looking-at-the-latest-earnings-reports-of-tsmc-micron-and-lam-research
- Section 232 chip tariff: https://www.axios.com/2026/01/14/trump-tariff-nvidia-chips-china and https://news.bloomberglaw.com/artificial-intelligence/white-house-details-chip-import-tariff-order-under-section-232
- Tariff delay on Chinese chips: https://investinglive.com/news/washington-delays-semiconductor-tariffs-as-it-seeks-china-trade-truce-20251224

AI trade
- GPU rental trends, Nov 2026: https://www.thundercompute.com/blog/ai-gpu-rental-market-trends
- AI bubble checklist, Oct 2026: https://investorplace.com/hypergrowthinvesting/2026/10/our-13-signal-ai-bubble-checklist-says-the-peak-isnt-here-yet/
- GPU prices and credit: https://nexusresearchreports.substack.com/p/the-gpus-got-more-expensive-the-credit
- AI capex cycle: https://alcapitaladvisory.com/research/intelligence/ai-infrastructure.html
- Hedge-fund outlook H2 2026 (capex-driven market): https://research-center.amundi.com/article/hedge-fund-outlook-h2-2026
- AI demand and power: https://www.mizuhogroup.com/americas-insights/ai-is-the-demand-engine-for-2026---but-not-all-exposure-is-equal
- Utilities split: https://www.valuethemarkets.com/analysis/ai-power-demand-splits-utility-stocks-into-two-camps
- Software selloff: https://www.spglobal.com/market-intelligence/en/news-insights/articles/2026/2/software-sell-off-may-be-overdone-yet-exposes-deeper-concerns-97965687
- Indian IT and the selloff: https://www.outlookbusiness.com/markets/fiis-dump-it-stocks-amid-saaspocalypse-fears-holdings-touch-four-year-low

Emerging themes
- BlackRock 2026 thematic outlook: https://ishares.com/us/insights/portfolio-insights/thematic-investing-2026-outlook
- WisdomTree thematic outlook: https://www.wisdomtree.com/be/insights/blog/thematic-outlook-we-have-entered-the-age-of-thematic-investing
- BNP Paribas 2026 themes: https://wealthmanagement.bnpparibas.com/en/insights/investment-themes/our-2026-investment-themes-mid-year-update/Beyond-algorithms-the-new-AI-frontiers.html
