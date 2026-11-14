# Quant Strategy Master Catalog

Compiled 15 Nov 2026. Step 1 of the trading-setup build: list everything publicly known, filter later.

**Scope caveat.** This covers what is public: academic literature, practitioner books, regulatory filings, court cases, vendor catalogs, trade press. The live signals inside Renaissance, Jane Street, Citadel and the rest are secret by design, so nobody outside can list those. What is public is the *families* they draw from, and that is what is here. Education and research only, not investment advice.

**Tags** (how reachable each item is for one person on paper trading)

- `[R]` doable solo with free or cheap data
- `[D]` gated by paid or hard-to-get data
- `[I]` gated by infrastructure, capital, licence or market access
- `[X]` illegal or manipulative. Listed so you can recognise and avoid it, never to do

Section tags are defaults; exceptions are tagged inline.

---

## 1. Equity cross-sectional factors (the "factor zoo") `[R]`

About 450 published anomalies exist; roughly two thirds fail replication once microcaps are controlled (Hou-Xue-Zhang). Survivors cluster in the families below.

**Value**
- Book/price, earnings/price, cash-flow/price, sales/price, EBITDA/EV, dividend yield
- Shareholder yield (dividends + buybacks + debt paydown), net payout yield
- Intangible-adjusted value, industry-relative value, composite value
- Magic Formula (earnings yield + return on capital), Acquirer's Multiple, net-nets (NCAV)
- Long-term reversal (3-5 year losers win)

**Momentum**
- 12-1 month price momentum, 6-month, intermediate (12-7)
- Industry momentum, 52-week-high proximity, residual (idiosyncratic) momentum
- Factor momentum, momentum with volatility scaling (crash-managed)
- "Frog in the pan" (smooth momentum beats jumpy), momentum acceleration
- Earnings momentum (SUE), analyst-revision momentum
- Overnight vs intraday momentum split

**Reversal**
- 1-month and 1-week reversal, industry-adjusted reversal
- Reversal conditioned on no-news (liquidity-driven moves revert, news-driven moves do not)
- Intraday reversal, overnight-intraday "tug of war"

**Quality and profitability**
- Gross profitability, ROE, ROA, ROIC, operating and cash-based operating profitability
- Piotroski F-score, Mohanram G-score, Quality-minus-Junk
- Accruals (Sloan), net operating assets, earnings persistence, margin stability
- Distress screens: Altman Z, Ohlson O, Merton distance-to-default (distressed stocks underperform)
- Manipulation screen: Beneish M-score

**Investment and issuance**
- Asset growth, capex growth, inventory growth (low investment wins)
- Net share issuance, IPO/SEO long-run underperformance, debt issuance, composite issuance

**Low risk**
- Low volatility, low beta (Betting-Against-Beta), betting against correlation
- Idiosyncratic volatility puzzle, MAX / lottery effect, idiosyncratic skewness, co-skewness
- Downside beta, tail-risk beta

**Size and liquidity**
- Size (small minus big), microcap premium (mostly untradeable)
- Amihud illiquidity, turnover, bid-ask spread, liquidity beta, abnormal-volume shocks

**Earnings and analysts**
- Post-earnings-announcement drift (PEAD), earnings-announcement premium, pre-earnings run-up
- Analyst revisions, recommendation changes, target-price implied return, forecast dispersion
- Guidance surprises, earnings-date changes (delays are bad news)
- Crowd estimates vs sell-side (Estimize-style) `[D]`

**Intangibles**
- R&D/market cap, advertising, organisation capital
- Patent citations, innovative efficiency, employee satisfaction, hiring growth `[D]`

**Short side and ownership**
- Short-interest ratio, days-to-cover, borrow fee, lending utilisation `[D]`
- Fails-to-deliver, short-sale constraints
- Institutional ownership change, hedge-fund "best ideas", active-share crowding
- Insider buying, split into opportunistic vs routine (only opportunistic predicts)
- Mutual-fund flow-induced pressure and fire sales

**Option-implied stock signals** `[D]`
- IV skew (steep put skew predicts underperformance), put-call parity deviations
- Option/stock volume ratio, IV changes, IV minus realised spread, IV term slope
- Unusual options activity

**Cross-sectional seasonality**
- Same-calendar-month effect (Heston-Sadka), January effect, dividend-month premium

**Factor engineering**
- Fama-French 3/5/6, Carhart, q-factor, Stambaugh-Yuan mispricing factors
- Barra/Axioma risk models, statistical PCA factors
- Factor timing (valuation spreads, factor momentum), factor crowding
- Multi-factor / smart beta, 130/30, sector, country and style rotation, quantamental
- Formulaic price-volume alphas (WorldQuant "101 Alphas"; 0.6-6 day holding, low pairwise correlation) and mass alpha combination

## 2. Statistical arbitrage and mean reversion `[R]`

- Pairs trading: distance method, cointegration (Engle-Granger), Johansen baskets, copula pairs, Kalman-filter dynamic hedge ratios, Ornstein-Uhlenbeck optimal entry/exit
- PCA / eigenportfolio residual reversion (Avellaneda-Lee), sector-ETF residual reversion, cluster mean reversion
- Deep-learning stat arb (residual portfolios + sequence models)
- Index arbitrage (cash vs futures), ETF vs basket, ETF creation/redemption arbitrage `[I]`
- Dual-class shares, ADR/GDR vs ordinary, dual-listed companies, A/H-share premium
- Holding-company and stub trades, closed-end fund discount reversion
- Lead-lag: large caps lead small, futures lead cash, cross-asset lead-lag
- Cross-exchange and triangular arbitrage `[I]`
- Futures calendar-spread reversion
- Short-horizon retail classics: RSI(2), Bollinger reversion, VWAP reversion, opening-gap fade, overnight-gap strategies
- Liquidity-provision reversal (returns to supplying liquidity, rises with VIX)

## 3. Trend, CTA and managed futures `[R]`

- Time-series momentum across ~50-100 futures (Moskowitz-Ooi-Pedersen)
- Moving-average crossover, Donchian/channel breakout (Turtle rules), ATR stops
- Multi-horizon trend blends, volatility-targeted trend
- Trend on "alternative markets" (Chinese commodities, power, credit, exotic rates) and on synthetic spreads `[I]`
- Cross-sectional momentum, value and carry in futures
- Carry / roll yield (backwardation vs contango), basis momentum, curve trades
- Hedging pressure (COT positioning), commodity skewness, inventory signals
- Economic trend (trend in fundamentals instead of prices)
- Short-term CTA (pattern and reversion models, days horizon)
- Crisis alpha / convexity as portfolio hedge
- Tactical asset allocation: Faber 10-month SMA, dual momentum (Antonacci), risk parity, All Weather, permanent portfolio
- Intraday momentum (first half-hour return predicts last half-hour), opening-range breakout, gap-and-go
- Classic technical analysis: RSI, MACD, Bollinger, Ichimoku, candlesticks, support/resistance, volume and market profile, Fibonacci/Elliott (weak evidence; listed for completeness)

## 4. Microstructure, HFT and market making `[I]`

**Liquidity provision**
- Passive market making with inventory control (Avellaneda-Stoikov, Guéant-Lehalle-Fernandez-Tapia)
- ETF market making and create/redeem arbitrage (Jane Street's core)
- Options market making (Citadel Securities, SIG, Optiver, IMC)
- Retail wholesaling / payment-for-order-flow internalisation (Citadel Securities, Virtu)
- FX market making (XTX), bond and credit electronic market making, portfolio trading

**Speed and cross-venue**
- Latency arbitrage on stale quotes, futures-to-cash lead (Chicago to New Jersey)
- Cross-exchange arbitrage, millisecond index-futures stat arb, high-frequency ETF arb
- News-feed and economic-release trading on machine-readable feeds
- Rebate capture (maker-taker and inverted venues), tick-size and queue games
- Opening/closing auction imbalance strategies

**Short-horizon signals** (`[R]` to study on crypto order books, `[I]` to monetise)
- Order-book imbalance, order-flow imbalance (Cont-Kukanov-Stoikov), multi-level OFI
- Microprice, queue imbalance, queue-position modelling
- Trade-flow toxicity (VPIN, contested), trade-sign autocorrelation, Hawkes-process flow models
- Order anticipation: detecting icebergs and large institutional parent orders
- Dark-pool liquidity seeking and hidden-liquidity detection

**Infrastructure edge**
- Co-location, microwave / millimetre-wave / laser / shortwave-radio links, hollow-core fibre
- FPGAs and ASICs, kernel bypass, direct feeds vs consolidated tape
- Exotic order types (ISO, hide-not-slide), speed-bump venues (IEX)

**Manipulative tactics** `[X]`
- Spoofing, layering, quote stuffing, momentum ignition
- Wash trading, painting the tape, marking / banging the close
- Front-running client orders, pump-and-dump, corners and squeezes, stop hunting
- Expiry-day index manipulation (what SEBI alleged against Jane Street in its July 2025 interim order; appeal still pending at SAT)

## 5. Execution and trading-cost practice `[R]` concepts, `[I]` at scale

- VWAP, TWAP, percent-of-volume, implementation shortfall (Almgren-Chriss), arrival price, close targeting
- Liquidity-seeking, iceberg, sniper, dark aggregation, smart order routing
- Reinforcement-learning limit-order placement
- Market-impact models (square-root law), transaction-cost analysis, capacity estimation
- Internal crossing and netting before going to market
- Block trading, RFQ, program trades, auction participation
- Short-locate and borrow optimisation, prime-broker financing optimisation, tax-aware execution

## 6. Options and volatility `[R]` listed options, `[I]` OTC

**Selling volatility (variance risk premium)**
- Short straddles/strangles, iron condors, iron flies, put writing, covered calls, cash-secured puts, the wheel
- Delta-hedged option selling, variance swaps, volatility-carry indices
- VIX futures roll-down (short-vol ETPs), VIX term-structure as equity-timing signal

**Buying or relative-value volatility**
- Gamma scalping, IV vs forecast realised vol (GARCH, HAR-RV, ML forecasts)
- Dispersion / correlation trading (short index vol, long single-stock vol)
- Skew trades (risk reversals), term-structure trades (calendars), forward variance
- Surface arbitrage (butterfly and calendar no-arbitrage violations, SVI fits)
- Put-call parity, conversions/reversals, box spreads as financing
- Vol-of-vol (VVIX), VIX basis arbitrage, cross-asset vol relative value (equity vs rates vs FX), swaption vol RV
- Tail hedging with deep out-of-the-money puts (Universa style), long-convexity funds

**Events and expiry**
- Earnings vol: pre-earnings IV run-up, straddles through earnings, IV crush
- 0DTE: intraday premium selling, 0DTE flow effects
- Weekly-expiry premium selling (India), pin risk, max pain
- OPEX-week and triple-witching effects, vanna and charm flows

**Structural flows to position around**
- Dealer gamma exposure (positive gamma dampens, negative amplifies; estimates are inferred, vendors disagree)
- Overwriting-ETF supply, autocallable issuance hedging (Korea, Japan, Europe)
- Large systematic collars rolled at quarter-end, vol-control fund rebalancing

**Dividends and exercise**
- Dividend futures, dividend capture, early-exercise dividend plays on calls

**Models and estimators**
- Black-Scholes Greeks, local vol (Dupire), Heston, SABR, sticky-strike vs sticky-delta regimes
- Realised-vol estimators: Parkinson, Garman-Klass, Yang-Zhang

## 7. Rates and fixed-income relative value `[I]`

- Treasury cash-futures basis trade (largest FI-RV trade; highly leveraged via repo)
- Swap-spread arbitrage, asset swaps, on-the-run vs off-the-run
- Curve steepeners, flatteners, butterflies; carry and roll-down; PCA rich/cheap vs fitted curve
- Auction cycle (concession before, recovery after), month-end index-extension buying, when-issued
- Cheapest-to-deliver and delivery-option trades, bond-futures rolls
- Repo specials and financing arbitrage, SOFR/fed-funds basis, FRA-OIS
- Cross-currency basis (covered-interest-parity deviations)
- TIPS breakevens vs inflation swaps, TIPS-Treasury arbitrage, STRIPS arbitrage
- Inter-market spreads (Bund-Treasury, peripheral-core Europe), sovereign country selection by carry/value/momentum
- Central-bank meeting pricing (OIS-implied path vs own forecast), QE/QT flow trades
- Liquidity plumbing watch: Treasury refunding, TGA, reverse repo, reserves
- Mortgage basis, TBA dollar rolls, prepayment modelling, convexity-hedging flows, agency vs non-agency, CMO tranches
- Muni/Treasury ratio and muni tax arbitrage, covered and supranational spreads
- Swaption straddles and vol surface RV, yield-curve-control break trades (JGB "widowmaker")
- Bond-ETF create/redeem arbitrage
- Yield curve as recession signal, term-premium models `[R]`

## 8. Credit `[I]`

- CDS-bond basis (negative-basis packages), capital-structure arbitrage (equity vs credit via Merton models)
- Index vs single-name skew arbitrage, tranche / correlation trading, credit-curve trades, CDS auctions
- Systematic credit factors: carry, value, momentum, equity momentum applied to bonds, duration-times-spread sizing
- Fallen angels, rising stars, new-issue concession, high-yield vs investment-grade rotation
- Convertible arbitrage (delta, gamma, credit, new-issue cheapness)
- Distressed debt, loan-to-own, DIP financing, claims trading, post-reorg equity, liability-management fights
- CLO equity and tranche RV, structured credit (ABS, CMBS, RMBS), significant-risk-transfer deals
- Private credit, direct lending, asset-based finance, trade finance
- Sovereign CDS vs bonds, EM hard-currency spreads
- Default-prediction ML, rating-change anticipation
- Litigation finance

## 9. Foreign exchange `[R]` majors, `[I]` EM and OTC

- Carry (G10 and EM), carry with volatility filter, carry-unwind risk (yen, Aug 2024)
- Momentum, value (PPP, real effective exchange rate), dollar factor, "dollar smile"
- Terms-of-trade and commodity currencies, rate-differential changes
- FX vol selling, risk reversals, option-expiry and barrier magnets
- Covered-interest-parity / cross-currency basis, triangular arbitrage
- Fixing flows (4 pm London), month-end hedge rebalancing
- Central-bank intervention tracking, reserve-manager flows
- Peg and band trades (attacking or defending pegs), redenomination risk
- NDF vs onshore (CNH-CNY, INR), capital-control premia
- Positioning (IMM/COT), economic-surprise trading
- Intraday seasonality (currencies weaken in own local hours), Japanese settlement-day effects
- Hedged-yield flows (foreign buyers of Treasuries after hedge cost)
- Balance of payments and current-account models

## 10. Commodities: financial and physical

**Curve and factor** `[R]`
- Roll yield / backwardation carry, momentum, value, basis momentum, hedging pressure, skewness
- Calendar spreads and seasonal spreads (gas March-April, gasoline summer, heating oil winter)
- Index-roll congestion (pre-positioning ahead of GSCI/BCOM rolls)
- Commodity equities vs underlying, commodity options vol

**Processing and cross-commodity spreads** `[R]`
- Crack (3-2-1), crush (soy), spark and dark spreads, frac spread, refinery margins
- Brent-WTI, gasoil-Brent, oil-gas ratio, gold-silver, platinum-palladium, corn-wheat
- Copper/gold ratio as a growth and yields signal

**Physical arbitrage (trading houses: Vitol, Trafigura, Glencore, Gunvor, Mercuria, Cargill, Bunge, ADM)** `[I]`
- Location arbitrage, time arbitrage (storage, contango cash-and-carry, floating storage), quality and blending arbitrage
- Asset-backed optionality: owning terminals, storage, ships, refineries
- Exchange arbitrage (Shanghai-LME, COMEX-London; tariff-driven dislocations in 2025)

**Fundamental data signals** `[D]` mostly, some `[R]`
- Weekly inventories (EIA, API, Cushing), rig and frac-crew counts, pipeline flows `[R]` for public series
- Tanker tracking by AIS, cargo-flow analytics, floating-storage counts, anchorage times
- Dark-fleet and sanctioned-barrel tracking, ship-to-ship transfers, AIS spoofing detection
- Satellite tank-roof shadows and SAR for crude stocks; refinery flaring and outages by thermal imaging
- OPEC+ meetings and compliance, strategic-reserve releases, China import quotas
- LME/SHFE warehouse stocks, cancelled warrants, treatment charges, scrap spreads, smelter activity from satellites
- Gold: real yields, central-bank buying, ETF flows, Shanghai premium
- Agriculture: NDVI and soil-moisture satellite yield models, USDA reports (WASDE, acreage, crop progress), export inspections, crop tours
- Weather: ENSO state, frost (coffee), hurricanes (Gulf energy), monsoon, cold snaps (gas)
- Livestock: cattle-on-feed, hog cycle, disease outbreaks
- Freight: Baltic Dry, forward freight agreements, container rates, port congestion, canal and strait chokepoints
- Policy shocks: export bans (rice, wheat, sugar, nickel ore), tariffs, stockpiling, resource nationalism
- Physical squeezes and corners (LME nickel 2022, cocoa) `[X]` to engineer, legal to trade around

## 11. Power, gas, weather, emissions `[I]`

- Day-ahead vs real-time spreads via virtual bids (INC/DEC)
- Congestion: financial transmission rights, point-to-point spreads, outage-driven flow shifts
- Nodal price, load, wind and solar forecasting; negative-price and ramp events; scarcity pricing
- Battery arbitrage, heat-rate and spark-spread trades, capacity markets
- Gas storage spreads, pipeline basis, LNG arbitrage (Henry Hub vs TTF vs JKM)
- Weather-model trading: run-to-run forecast changes (ECMWF vs GFS ensembles) `[R]` data is public
- Weather derivatives (heating/cooling degree days), hydro and snowpack, nuclear-outage tracking
- Catastrophe bonds and insurance-linked securities
- Carbon allowances (EU ETS, California), renewable certificates, policy-driven carbon trades
- Data-centre / AI power-demand theme

## 12. Event-driven and corporate actions `[R]` mostly

**Deals**
- Merger arbitrage (cash, stock, collars, contingent value rights), antitrust analysis, deal-break models
- Pre-announcement takeover prediction, tender offers, odd-lot tenders, Dutch auctions
- Appraisal arbitrage, "bumpitrage", cross-border and national-security review risk

**Restructuring of the share base**
- Spin-offs (forced selling by funds that cannot hold them), carve-outs, split-offs, stubs
- Rights offerings, SPAC arbitrage (trust yield plus optionality), SPAC warrants
- IPOs: first-day, lock-up expiry, quiet-period expiry; secondary placements and block discounts
- Convertible issuance (hedging short pressure), buyback announcements and blackout windows
- Dividend initiations, cuts, specials; splits and reverse splits; share-class conversions

**Index and fund mechanics**
- Index inclusion/deletion (S&P, Russell reconstitution, MSCI, FTSE, Nifty), float and weight changes
- Leveraged and thematic ETF rebalance pre-positioning, ETF closures, closed-end fund activism

**Information events**
- Earnings (PEAD, guidance, date changes), analyst days, management turnover
- Activist 13D filings, short-seller reports, insider cluster buying
- Restatements, auditor resignations, late filings, Friday-night 8-Ks, credit-rating changes
- Biotech binaries: PDUFA dates, trial readouts, advisory committees
- Court dockets: patent rulings, class actions, bankruptcy milestones
- Product recalls, cyber breaches, regulatory rulings
- Tax-loss selling and January rebound, delistings and relistings
- Privatisations and government stake sales

## 13. Flow, positioning and "what other players must do" `[R]` for public data, `[D]` for vendor estimates

**Forced or rule-based flows you can predict**
- Index rebalances, leveraged-ETF daily rebalance, target-date and balanced-fund rebalancing
- Pension and sovereign month-end / quarter-end rebalancing
- Vol-control and risk-parity deleveraging, CTA trend trigger levels (bank desks model these)
- Dealer gamma, vanna and charm hedging; option-expiry pinning
- Buyback execution windows and blackouts, beginning-of-month retirement inflows
- Mutual-fund redemptions and fire sales, margin calls and forced liquidations
- Scheduled supply: lock-up expiries, sponsor sell-downs, issuance calendars

**Positioning gauges**
- COT reports, IMM FX positioning, futures and options open interest, put/call ratios
- Short interest, securities-lending data, squeeze screens
- Prime-broker crowding and gross/net leverage reports, degrossing detection
- Margin debt, sentiment surveys (AAII, fund-manager surveys) as contrarian signals
- ETF creations/redemptions and flows, retail flow trackers, social-attention spikes
- Dark-pool prints, off-exchange short volume, block-trade detection
- Central-bank and state buying (BOJ ETF purchases, China "national team"), Stock Connect flows
- Net-liquidity measures (central-bank balance sheet minus Treasury account minus reverse repo)

**Following other firms**
- 13F cloning of top stock pickers, "hotel" and VIP baskets, crowding as a risk factor
- 13D/13G activist following, Form 4 insiders, N-PORT fund holdings, EU short disclosures
- Hedge-fund letters and conference pitches (idea dinners, Sohn-style events)
- Alpha capture: scoring sell-side trade ideas systematically (Marshall Wace TOPS)
- Reverse-engineering public rulebooks (index, ETF, structured-product, vol-control) to pre-position
- Reading rivals' job postings and patents to infer where they are building

## 14. Calendar and seasonality `[R]`

- Turn-of-month, January effect, turn-of-year small caps, Santa rally, Sell-in-May / Halloween
- Day-of-week, pre-holiday, payday effect, quarter-end window dressing
- Pre-FOMC drift, FOMC-cycle weeks, macro-announcement-day premium
- Overnight vs intraday return gap, last-half-hour momentum
- Options-expiration week, triple witching
- Presidential cycle, earnings-season premium, dividend-month premium
- Treasury-auction cycle, month-end FX fix
- Commodity seasonals, crypto weekend and funding-time effects
- Local calendars: Lunar New Year, Ramadan, Diwali/Muhurat, Indian budget day, monsoon
- Sunshine, lunar and sports-result effects (spurious or tiny; listed for completeness)

## 15. Global macro `[R]` for liquid futures/ETFs

**Systematic**
- Carry, value, momentum and defensive applied across equities, bonds, FX, commodities
- Macro momentum (trends in growth, inflation, trade, monetary policy)
- Nowcasting growth and inflation; scraped-price inflation; economic-surprise indices
- Data-release trading (payrolls, CPI) with forecast models
- Central-bank reaction-function models (Taylor rules), hawk/dove scoring of communications
- Regime models: growth/inflation quadrants, investment clock, hidden-Markov risk-on/off
- Cross-asset lead-lag (credit leads equity, copper/gold leads yields)
- Financial-conditions indices, credit impulse, global liquidity, dollar cycle
- Leading indicators: PMI new orders minus inventories, yield curve, building permits, early Korean and Taiwanese export data, freight, Sahm rule
- Risk parity and All Weather, diversified uncorrelated-bets book (Bridgewater Pure Alpha style)

**Discretionary themes**
- Reflexivity and peg-break trades (Soros), sovereign-debt sustainability and default trades
- EM crisis early-warning (reserves, current account, short-term external debt), IMF-programme trades
- Inflation-regime and stagflation hedges, fiscal-stress "bond vigilante" trades
- Tariff and trade-war baskets, reshoring, de-dollarisation and gold accumulation
- Carry-unwind episodes, China stimulus trades, AI-capex cycle, private-credit stress
- Country equity selection (CAPE, momentum), EM local-debt carry
- Tail-risk and black-swan positioning

**Activity proxies for opaque economies** `[D]`
- Night-lights, electricity use, rail freight, bank loans ("Li Keqiang index")
- NO2 and pollution as industrial activity, AIS-based trade nowcasts, mobility data

## 16. Geopolitics, policy, conflict, sanctions `[R]` to track, harder to trade

**Indices and systematic signals**
- Geopolitical Risk index (Caldara-Iacoviello) timing rules, Economic Policy Uncertainty, Trade Policy Uncertainty
- Conflict-event databases (GDELT, ACLED) as features, news-count shock models
- Safe-haven baskets: gold, Swiss franc, yen, Treasuries, defence equities
- "Buy the invasion" pattern (equities often rally after the feared event lands)

**Conflict and chokepoints**
- Defence and aerospace rotation on escalation; reconstruction and peace-deal baskets; war-linked sovereign instruments (GDP warrants)
- Strait and canal risk: Hormuz, Bab el-Mandeb/Red Sea, Suez, Malacca, Panama, Taiwan Strait (tanker rates, container rates, insurers, energy)
- Taiwan-risk hedges (semiconductors, currency, shipping insurance)
- Energy-security trades (gas storage levels, LNG, pipeline outages)
- OSINT: troop build-up on satellite imagery, government and military flight tracking, naval movements, airspace closure notices

**Sanctions and controls**
- Sanctioned-crude discounts, dark-fleet growth, tanker-equity effects
- Sanctions-relief speculation on defaulted sovereign debt; frozen-asset claims
- Secondary-sanctions risk on banks; payment-system exclusion
- Export controls (chips, lithography, rare earths, gallium/germanium), critical-mineral nationalism
- Capital-control arbitrage (parallel FX rates, crypto premia, dual-listed share gaps)
- Expropriation and arbitration-award trading

**Elections and policy**
- Poll models plus prediction-market odds mapped to sector, currency and rates baskets
- Referendum trades with private polling (Brexit night)
- Policy-beneficiary baskets (industrial subsidies, defence budgets, infrastructure, production-linked incentives)
- Legislative tracking: bill-passage probability from text and whip counts; regulatory dockets
- Government-contract awards data, lobbying-intensity factor, political-connection factor
- Congressional trade disclosures (copy strategies and ETFs built on them)
- Leader social-media shock models (post-driven volatility indices)
- State-plan sector following (five-year plans, national champions)
- Sovereign-wealth and state-bank flows; delisting and structure risk for foreign listings
- Supply-chain relocation ("China+1": Vietnam, India, Mexico)
- Cyberattack, terror and pandemic event-reaction playbooks; climate-summit policy trades

## 17. Alternative data `[D]` unless noted

**Satellite, aerial, geospatial**
- Retail parking-lot car counts (same-store-sales nowcast)
- Oil-tank floating-roof shadows; SAR imaging through cloud for tanks, ships, construction
- Factory activity: thermal signatures, truck counts, staff car parks, finished-vehicle lots
- Mines: stockpiles, pit activity; smelters; steel mills
- Crops: NDVI, soil moisture, acreage classification `[R]` Sentinel/Landsat/MODIS are free
- Night-lights for GDP in opaque economies `[R]` VIIRS is free
- Port and anchorage congestion, ship counts, parked aircraft
- Construction progress, housing starts, empty-development detection
- Gas flaring, methane plumes, NO2/SO2 pollution `[R]` public satellites
- Reservoir levels, snowpack, deforestation, solar and wind build-out

**Location and mobility**
- Phone-geolocation foot traffic: stores, restaurants, casinos, theme parks, hotels, factory shifts
- Connected-car and road-congestion data, transit ridership, airport security throughput `[R]`
- Flight tracking (ADS-B): corporate jets for deal and partnership detection, cargo flights `[R]` for unfiltered feeds
- Ship tracking (AIS), bills of lading and customs records (supplier links, import volumes)
- Truck telematics, spot freight rates, rail carloads `[R]` weekly public reports

**Consumer transactions**
- Credit/debit-card panels, email-receipt panels, point-of-sale scanner data, bank-aggregation data
- E-commerce scraping: best-seller ranks, prices, stock-outs, delivery lead times, discount depth `[R]` if you scrape
- App downloads, active users, time spent; web traffic; search trends `[R]` Google Trends
- Ad-spend trackers, TV and streaming charts, box office, game concurrent players `[R]` Steam/Twitch
- Vehicle registrations and insurance registrations, used-car prices
- Housing listings, rents, hotel rates, air fares, restaurant reservations
- Prescription volumes, medical claims, clinical-trial registry changes `[R]` registry
- Product reviews and ratings, subscription churn, SKU counts

**Workforce and company exhaust**
- Job postings (growth, tech adoption, strategy shifts), headcount and attrition from professional profiles
- Employee reviews (sentiment, CEO approval), layoffs trackers `[R]`
- Small-business payroll and scheduling data
- GitHub activity, package downloads (npm, PyPI, Docker) for software adoption `[R]`
- Website-change monitoring (pricing pages, careers pages), tech-stack detection, domain registrations `[R]`
- Outage trackers, customer-support forum volume `[R]`

**Sentiment and attention**
- Machine-readable news sentiment, novelty and relevance scores
- Social platforms: X, Reddit, StockTwits, Telegram/Discord; mention velocity; bot filtering `[R]` partly
- Wikipedia page views, search-query volume `[R]`
- Expert-network and podcast transcripts, surveys, consumer panels

**Government, legal, regulatory** `[R]` mostly public
- SEC filings text and diffs, EDGAR access logs, comment letters
- Patents and trademarks, FDA databases (adverse events, inspections, approvals)
- Court dockets, bankruptcy filings, liens, building permits, business registrations
- Government contracts, lobbying and campaign finance, freedom-of-information requests
- Environmental and safety violations, emissions inventories
- Import/export statistics, central-bank and statistical-agency microdata

**Networks and links**
- Customer-supplier links (customer momentum, supplier momentum)
- Shared analyst coverage, text-based industry peers, technology/patent similarity
- Geographic links, common ownership, news co-mentions, board interlocks
- Graph models over these networks for lead-lag

**People signals**
- Executive vocal stress and tone on calls (audio), facial-expression studies on central bankers (video)
- Executive departures, insider selling plans, CEO social media
- Corporate-jet destinations, conference attendance

**Environmental and physical sensors**
- Weather stations and forecasts `[R]`, grid load and generation mix `[R]`, IoT/smart-meter feeds
- Seismic and natural-hazard feeds, epidemiological and wastewater data `[R]`

**Compliance practice around alt data**
- Vendor diligence for MNPI and personal data, scraping terms-of-service risk, exclusivity and decay tracking

## 18. Text, NLP and LLM methods `[R]`

- Finance-specific dictionaries (Loughran-McDonald), FinBERT-class sentiment
- Earnings-call tone, Q&A evasiveness, analyst-question tone, management vs analyst divergence
- 10-K/10-Q change detection ("Lazy Prices": changed filings predict underperformance), risk-factor additions, readability
- News novelty, event extraction, headline trading, rumour detection
- Central-bank minutes and press-conference parsing
- Topic models, text-derived industry and supply-chain maps, patent and job-posting text
- LLM embeddings as return features; LLM headline scoring
- LLM agents as research analysts and code writers (Man Group AlphaGPT, Bridgewater AIA Labs); humans keep the veto
- LLM / genetic-programming formula mining for alphas
- Chart images through CNNs (price-trend images)
- Local-language edge: translating foreign filings and regional news ahead of consensus
- Known trap: LLM look-ahead bias in backtests (the model has read the future)
- Consensus view in 2026 reporting: LLMs speed up research more than they originate alpha, and LLM-derived edges decay fast

## 19. Machine-learning and maths toolkit `[R]`

- Ridge, lasso, elastic net; random forests; gradient boosting; neural nets (Gu-Kelly-Xiu)
- Instrumented PCA, conditional autoencoders, "virtue of complexity" debate
- LSTM, temporal CNNs, transformers; limit-order-book deep learning (DeepLOB); time-series foundation models (mixed evidence)
- Reinforcement learning for execution, market making, allocation
- Hidden Markov models, regime switching, change-point detection (Renaissance heritage: speech-recognition maths)
- Kalman filters and state-space models, Bayesian methods, Gaussian processes, kernel regression
- Clustering, hierarchical risk parity, PCA/ICA, random-matrix covariance cleaning, Ledoit-Wolf shrinkage
- Graph neural networks, genetic programming and symbolic regression
- Online learning and bandits for strategy allocation, ensembles and stacking
- Meta-labeling, triple-barrier labels, fractional differentiation, tick/volume/dollar bars
- Feature importance (MDA, SHAP), causal inference, conformal prediction
- Wavelets and spectral methods, entropy measures
- Hawkes processes, stochastic control (HJB), optimal stopping, copulas, extreme-value theory
- Monte Carlo, agent-based simulators, generative models for synthetic markets

## 20. Crypto

**Centralised venues** `[R]`
- Spot-perp funding arbitrage, dated-futures basis, perp-perp funding spreads across venues (crowded: one mid-2026 study put mainstream funding near 2.8% annualised)
- Cross-exchange and triangular arbitrage, regional premia (kimchi premium), stablecoin depegs
- Trend and momentum (strong historically), cross-sectional size/momentum/reversal/carry, pairs (ETH/BTC), dominance rotation
- Funding, open interest and cumulative volume delta as sentiment; liquidation-cascade maps
- Options: vol selling, skew, vol-index trades
- Listing and delisting effects, token-unlock shorts, airdrop and points farming
- CME basis vs spot ETFs, ETF-flow signals, treasury-company NAV-premium trades
- Market making `[I]`

**On-chain analytics** `[R]`
- Exchange inflows/outflows, stablecoin mint/burn, whale and smart-wallet tracking, copy-trading wallets
- Valuation ratios: MVRV, NVT, SOPR, realised cap, HODL waves, Puell multiple
- Miner flows, hash ribbons, halving cycle
- Protocol fundamentals: TVL, fees, revenue multiples, developer activity, governance events
- Hack and exploit news reaction

**DeFi and MEV** `[I]` mostly
- DEX-CEX and DEX-DEX atomic arbitrage, backrunning, just-in-time liquidity, liquidation keepers
- Sandwiching (harms users; legal grey zone) `[X]`-adjacent
- Block building, searchers, relays, priority-fee auctions, Solana latency games
- Concentrated-liquidity LP management, delta-neutral LP, yield farming
- Lending-rate arbitrage, recursive looping, liquid-staking and restaking basis
- Tokenised basis yield (Ethena style), fixed-vs-floating yield trading (Pendle style)
- Perp-DEX funding arbitrage and vaults; equity/commodity perps vs TradFi; tokenised-stock 24/7 vs market-hours gaps
- Cross-chain and bridge arbitrage, flash loans, new-pool sniping, memecoin sniper bots
- Oracle manipulation, governance attacks, rug pulls `[X]`

## 21. Prediction markets and betting `[R]`

- Cross-venue arbitrage (Polymarket vs Kalshi), within-market arbitrage (outcome prices not summing to 1)
- Market making with venue incentive programmes `[I]`
- Model-vs-market: election models, weather contracts vs forecast ensembles, economic-release contracts vs nowcasts, rate decisions vs futures
- Favourite-longshot bias, resolution-rule reading, news latency
- Using odds as inputs for asset baskets; hedging macro books with event contracts
- 2026 context: SIG, DRW, Jump, IMC, Wintermute are building desks; liquidity still patchy
- Sports-betting quant: rating models, closing-line value, arbitrage and matched betting, Kelly staking, syndicate models
- Trading on inside knowledge of outcomes `[X]`

## 22. Structured, tax and niche `[I]`

- Convertible and warrant arbitrage, contingent convertibles, preferreds
- Tax-loss harvesting and direct indexing `[R]`, dividend-withholding schemes (cum-ex is criminal fraud) `[X]`
- Regulatory-capital arbitrage, structured-product hedging flows
- Insurance-linked: cat bonds, life settlements, reinsurance sidecars
- Royalties (music, pharma), aircraft and ship leasing, trade claims
- Real assets: REIT NAV discounts, farmland, timber, infrastructure, water rights
- Private-market secondaries, pre-IPO tenders, GP stakes, BDC discounts
- Collectibles (art, wine, watches) funds
- Cash management: bills, repo, money funds, securities-lending income
- Portable alpha, overlays, synthetic prime (total-return swaps)

## 23. India-specific `[R]` unless noted

**Derivatives**
- Weekly-expiry option selling (Nifty Tuesday on NSE, Sensex Thursday on BSE; other weeklies were discontinued), intraday short straddles with stops, iron flies
- Cash-futures arbitrage (what arbitrage mutual funds do), calendar spreads, rollover analysis
- Participant-wise open interest (FII index-futures long/short), F&O ban list, max pain
- GIFT Nifty overnight lead, ADR premium on Indian names

**Flows and disclosures**
- FII/DII daily flows, bulk and block deals, delivery percentage
- Promoter buying and pledging, insider (PIT) disclosures, takeover-code (SAST) filings
- Quarterly shareholding-pattern changes, monthly mutual-fund holdings, SIP inflows
- AMFI large/mid/small reclassification (forces mutual-fund buying and selling twice a year)
- Nifty/Sensex and MSCI/FTSE India rebalances with passive-flow estimates
- Surveillance lists (ASM/GSM), circuit-filter momentum

**Corporate events**
- IPO grey-market premium, subscription multiples, anchor lock-in expiry (30 and 90 days)
- Buyback tender arbitrage (small-shareholder quota), open offers, delisting reverse book-building
- Demergers, merger swap-ratio arbitrage, rights-entitlement arbitrage, holding-company discounts
- QIP and offer-for-sale discounts
- Exchange-announcement feed parsing (order wins, capacity additions, auditor exits)

**Macro and alt data (free, high frequency)**
- GST collections, e-way bills, UPI volumes, FASTag tolls
- Vahan vehicle registrations (daily), fuel sales, power demand (daily), rail freight, port cargo, air traffic
- Monsoon rainfall, reservoir levels, sowing progress, mandi prices
- Bank credit growth (fortnightly), card spends, hiring indices, payroll additions
- RBI intervention and forward book, USDINR onshore vs NDF

**Commodities**
- MCX vs international parity (gold, silver, crude) and duty changes; gold ETF vs sovereign gold bond vs futures

**Market structure**
- SEBI retail algo framework in force since 1 April 2026: exchange algo-ID on automated orders, broker-API routing, static-IP whitelisting, 2FA, order-to-trade limits (verify details against the circular)
- Higher STT and larger lot sizes have cut retail option-selling edge
- Domestic and global HFT firms dominate index options (Jane Street case is the reference reading)
- Operator-driven smallcaps and Telegram pump groups `[X]`

## 24. Portfolio construction, sizing and risk `[R]`

- Mean-variance, Black-Litterman, minimum variance, maximum diversification
- Risk parity / equal risk contribution, hierarchical risk parity, risk budgeting
- Kelly and fractional Kelly, volatility targeting, drawdown-based scaling
- Fundamental law of active management (IR ≈ IC × √breadth): many small uncorrelated bets beat a few big ones
- Signal combination (IC-weighting, stacking), turnover and decay control
- Cost-aware and multi-period optimisation, robust optimisation, covariance shrinkage
- Neutralisation: dollar, beta, sector, style-factor; isolating idiosyncratic return
- Limits: gross/net, single-name, sector, liquidity (% of daily volume), factor exposure
- VaR, expected shortfall, stress tests, scenario analysis, correlation-spike monitoring
- Crowding monitors, tail hedges, liquidity-adjusted exits
- Hard drawdown stops per book (the pod-shop rule: capital is cut at a first loss threshold and pulled at a second; exact levels are not public)
- PnL attribution (factor vs idiosyncratic), live-vs-backtest tracking, alpha-decay monitoring
- Capital allocation across strategies by marginal Sharpe and drawdown
- Centre book / alpha-capture overlay on top of individual books; internal netting
- Kill switches, pre-trade checks, reconciliation, counterparty diversification
- Compliance: restricted lists, information barriers, trade surveillance

## 25. Research and operating practice `[R]`

- Hypothesis first, then test; keep a research log; version everything
- Point-in-time data, survivorship-bias-free universes, correct corporate-action handling
- Realistic costs, slippage, borrow fees, capacity; exclude microcaps or value-weight
- Walk-forward and out-of-sample tests, purged k-fold with embargo, combinatorial purged CV
- Deflated Sharpe ratio, probability of backtest overfitting, multiple-testing bar (t > 3)
- Expect decay: published anomalies lose about a quarter out of sample and over half after publication (McLean-Pontiff)
- Incubation ladder: backtest, paper trade, tiny live size, scale
- Randomised live experiments for execution; simulator fidelity (queue and impact models)
- Signal library / "alpha factory" at scale; crowd-sourced alpha (Numerai, WorldQuant BRAIN)
- One shared model and codebase (Renaissance) vs independent pods (Millennium) vs collaborative single book (Jane Street)
- Hire scientists, pay with ownership, enforce secrecy and non-competes
- Data engineering as the main cost centre: ingestion, cleaning, feature store, monitoring

## 26. Who is known for what (public record only)

| Firm type | Examples | Publicly known style |
|---|---|---|
| Single-model stat arb | Renaissance (Medallion), TGS, PDT | Short-horizon, thousands of small signals, high leverage, one unified model |
| Systematic multi-strategy | Two Sigma, D. E. Shaw, WorldQuant, QRT, Squarepoint, G-Research, Cubist | Alt data plus ML, alpha libraries, stat arb, systematic macro |
| Factor / premia | AQR, Arrowstreet, Acadian, Dimensional | Value, momentum, quality, carry, defensive; long horizon |
| Trend / CTA | Man AHL, Winton, Aspect, Systematica | Multi-asset trend, alternative markets |
| Pod platforms | Citadel, Millennium, Point72, Balyasny, ExodusPoint | Many market-neutral books, tight drawdown stops, central risk |
| Market makers / prop | Jane Street, Citadel Securities, SIG, Optiver, IMC, HRT, Jump, Tower, DRW, Virtu, XTX, Flow Traders | ETF and options market making, latency-sensitive arbitrage, crypto and prediction markets |
| Discretionary macro | Bridgewater, Brevan Howard, Rokos, Element, Tudor, Caxton | Rates, FX, themes; Bridgewater is rules-based |
| Tail risk | Universa | Deep out-of-the-money convexity |
| Physical commodities | Vitol, Trafigura, Glencore, Gunvor, Mercuria, Cargill | Logistics, storage and information arbitrage |
| India prop/HFT | Graviton, AlphaGrep, Quadeye, iRage, NK Securities plus global firms | Index-options market making, arbitrage |

---

## Sources checked for this pass

Strategy references
- Kakushadze & Serur, *151 Trading Strategies*: https://papers.ssrn.com/abstract=3247865 (Springer edition retracted over image-copyright concerns, not content: https://link.springer.com/content/pdf/10.1007/978-3-030-02792-6.pdf)
- Kakushadze, *101 Formulaic Alphas*: https://www.arxiv.org/abs/1601.00991
- Hou, Xue, Zhang, *Replicating Anomalies*: https://www.nber.org/papers/w23394.pdf
- Jensen, Kelly, Pedersen, *Is There a Replication Crisis in Finance?*: https://research-api.cbs.dk/ws/portalfiles/portal/95651880/theis_ingerslev_jensen_et_al_is_there_a_replication_crisis_in_finance_publishersversion.pdf
- HFR strategy classification: https://www.hfr.com/hfr-hedge-fund-strategy-definitions-macro
- Cohen, Malloy, Pomorski, *Decoding Inside Information*: https://www.nber.org/papers/w16454.pdf
- Quantpedia seasonality: https://quantpedia.com/quantpedias-composite-seasonalcalendar-strategy-case-study/
- CXO Advisory seasonal survey: https://www.cxoadvisory.com/calendar-effects/survey-of-seasonal-anomalies/
- Momentum spillovers / economic links: https://www.nber.org/system/files/working_papers/w25201/w25201.pdf

Microstructure, vol, rates
- HFT strategy list: https://daytrading.com/hft-strategies
- CFA digest on HFT: https://rpc.cfainstitute.org/research/cfa-digest/2015/11/high-frequency-market-microstructure-digest-summary
- Volatility premia: https://resonanzcapital.com/insights/volatility-premia-there-are-many-ways-to-skin-a-cat
- Dealer gamma: https://spotgamma.com/gex/
- Basis vs swap-spread trades: https://hedgeweek.com/news/hedge-funds-shift-into-riskier-swap-spread-trades-as-treasury-basis-strategy-stalls
- Fixed-income arbitrage overview: https://en.wikipedia.org/wiki/Fixed_income_arbitrage

Alt data, commodities, power, geopolitics
- Neudata on alt data: https://www.neudata.co/alternative-data
- Jet tracking: https://www.neudata.co/intelligence/from-runway-to-returns-jet-tracking-revisited
- Kpler oil inventories: https://www.kpler.com/solutions/fundamental-intelligence/oil-inventories
- Kayrros crude: https://energyaspects.com/energy-markets/oil-market-analysis/kayrros-crude-oil-inventories
- Vortexa floating storage: https://www.vortexa.com/?p=12854
- Planet crop acreage and yield: https://planet.com/pulse/satellite-data-commodities-crop-acreage-yield
- Power trade types: https://www.yesenergy.com/blog/2020/financial-power-markets-trade-types
- FTR and weather: https://www.enverus.com/blog/finding-the-edge-how-ftr-traders-can-leverage-weather-intelligence/
- GPR index hedging: https://rpc.cfainstitute.org/research/cfa-digest/2020/12/dig-v50-n12-1
- Central-bank intervention and FX factors: https://quantpedia.com/systematic-interventions-of-central-banks-and-major-currency-risk-premiums/
- Central-bank minutes NLP: https://rpc.cfainstitute.org/blogs/enterprising-investor/2026/nlp-and-yield-curve-prediction-from-central-bank-minutes

Crypto, prediction markets, AI
- Crypto arbitrage in 2026: https://docs.ccxt.com/blog/crypto-arbitrage-strategies
- Funding-rate crowding: https://blog.1token.tech/tradfi-perpetual-arbitrage/
- Quant firms in prediction markets: https://www.tradermath.org/articles/prediction-markets-trading-at-quant-firms and https://www.ai-cio.com/?p=102989
- AI use by hedge funds: https://resonanzcapital.com/insights/ai-use-by-hedge-funds-made-tangible-from-lego-bots-to-alpha-assistants
- Hedge funds and AI labs: https://hedgeweek.com/news/the-blurring-lines-between-hedge-funds-and-ai-labs

India
- SEBI v Jane Street analysis: https://blogs.law.ox.ac.uk/oblb/blog-post/2025/07/jane-street-and-expiry-day-trap-unpacking-sebis-crackdown-algorithmic
- SAT hearing status: https://www.businesstoday.in/markets/story/jane-street-vs-sebi-sat-adjourns-hearing-in-market-manipulation-case-517925-2026-02-25
- Retail algo rules: https://support.fyers.in/portal/en/kb/articles/what-are-the-new-sebi-rules-for-retail-algo-trading-from-april-01-2026
- Expiry-day changes: https://www.business-standard.com/markets/news/nse-bids-adieu-to-thursday-expiry-as-dates-swap-come-into-effect-explained-125082800635_1.html

Research practice and industry
- Why ML funds fail (López de Prado): https://quantpedia.com/why-machine-learning-funds-fail/
- Hedge-fund outlook H2 2026: https://research-center.amundi.com/article/hedge-fund-outlook-h2-2026
- Pod-shop model: https://www.hedgeweek.com/millenniums-dominance-highlights-rise-of-mega-pod-shop-hedge-fund-model/
