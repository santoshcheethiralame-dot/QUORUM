from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SITE = ROOT / "site"

UNIVERSE = {
    "SPY": ("US large caps", "equity"),
    "QQQ": ("Nasdaq 100", "equity"),
    "IWM": ("US small caps", "equity"),
    "EFA": ("Developed markets ex-US", "equity"),
    "EEM": ("Emerging markets", "equity"),
    "SMH": ("Semiconductors", "equity"),
    "INDA": ("India", "equity"),
    "TLT": ("Long US Treasuries", "bonds"),
    "IEF": ("7-10 year Treasuries", "bonds"),
    "HYG": ("High-yield credit", "bonds"),
    "GLD": ("Gold", "real assets"),
    "DBC": ("Broad commodities", "real assets"),
    "VNQ": ("US real estate", "real assets"),
    "UUP": ("US dollar", "currency"),
    "BTC-USD": ("Bitcoin", "crypto"),
    "ETH-USD": ("Ether", "crypto"),
}
GROUP_ORDER = ["equity", "bonds", "real assets", "currency", "crypto"]

RADAR_EXTRA = ["^VIX", "^VIX3M", "^TNX", "^IRX", "HG=F", "GC=F", "CL=F",
               "DX-Y.NYB", "MU", "TSM", "RSP", "^NSEI", "INR=X"]

# ---- stock picks: individual names the model can flag buy / hold / sell ----
US_STOCKS = """AAPL MSFT NVDA GOOGL AMZN META TSLA AVGO BRK-B JPM LLY V UNH XOM MA COST HD PG JNJ ABBV WMT NFLX
BAC CRM ORCL CVX KO MRK AMD PEP ADBE TMO CSCO ACN LIN MCD ABT WFC GE IBM QCOM DHR CAT TXN INTU AMAT VZ DIS PFE
NOW GS MS AXP UBER ISRG BKNG RTX SPGI T LOW NEE HON UNP PLTR MU LRCX PANW ANET INTC BA NKE""".split()
IN_STOCKS = """RELIANCE.NS TCS.NS HDFCBANK.NS ICICIBANK.NS INFY.NS BHARTIARTL.NS SBIN.NS ITC.NS LT.NS
HINDUNILVR.NS KOTAKBANK.NS AXISBANK.NS BAJFINANCE.NS MARUTI.NS SUNPHARMA.NS TITAN.NS HCLTECH.NS NTPC.NS
ULTRACEMCO.NS ASIANPAINT.NS WIPRO.NS ADANIENT.NS POWERGRID.NS BAJAJFINSV.NS ONGC.NS TATASTEEL.NS JSWSTEEL.NS
COALINDIA.NS TECHM.NS NESTLEIND.NS""".split()
MARKETS = {
    "US": {"label": "US stocks", "stocks": US_STOCKS, "index": "SPY", "currency": "$", "max_names": 10},
    "IN": {"label": "Indian stocks", "stocks": IN_STOCKS, "index": "^NSEI", "currency": "₹", "max_names": 6},
}
PICKS = {
    "enter_pct": 0.15,   # buy when the score ranks in the top 15% of its market
    "hold_pct": 0.40,    # sell when it drops out of the top 40%
    "atr_mult": 3.0,     # trailing stop: highest close since entry minus 3 average daily ranges
    "atr_mult_crisis": 2.0,
    "cost_bps": 10.0,
    "capital": 100_000.0,
}
# symbols the live desk streams: tape first, then everything else
TAPE = ["^GSPC", "^IXIC", "^NSEI", "^VIX", "BTC-USD", "ETH-USD", "GC=F", "CL=F", "INR=X", "^TNX"]
TAPE_NAMES = {"^GSPC": "S&P 500", "^IXIC": "Nasdaq", "^NSEI": "Nifty 50", "^VIX": "Fear index (VIX)",
              "BTC-USD": "Bitcoin", "ETH-USD": "Ether", "GC=F": "Gold", "CL=F": "Crude oil",
              "INR=X": "Rupees per dollar", "^TNX": "US 10-year yield", "SOL-USD": "Solana"}
BINANCE = {"BTC-USD": "btcusdt", "ETH-USD": "ethusdt", "SOL-USD": "solusdt"}

CAPITAL = 100_000.0
TARGET_VOL = 0.12
IDM = 2.0
VOL_SPAN = 32
VOL_FLOOR = 0.05

# Carver's EWMAC speeds and forecast scalars
EWMAC = [(16, 3.75), (32, 2.65), (64, 1.87)]
TREND_FDM = 1.15

SLEEVES = ["trend", "reversion", "calendar"]
SLEEVE_LABEL = {"trend": "Trend", "reversion": "Reversion", "calendar": "Calendar"}
# A weight of 0 puts a sleeve in shadow: it is computed and displayed but moves no money.
# Reversion is in shadow because it tripled turnover for about 9% gross over 16 years
# (see tests/compare_mixes.py); it stays there until it pays for its own trading costs.
WEIGHTS = {
    "equity": ({"trend": 0.7, "reversion": 0.0, "calendar": 0.3}, 1.15),
    "default": ({"trend": 1.0}, 1.0),
}
CALENDAR_FORECAST = 15.0

MAX_WEIGHT = 0.35
MAX_GROSS = 2.0
MAX_EQUITY_NET = 1.0
THEME = {"name": "Tech and AI", "members": ["QQQ", "SMH"], "cap": 0.30}
BUFFER = 0.10
STRESS_SCALE = 0.75
BRAKE = [(0.10, 0.5), (0.20, 0.25)]
COST_BPS = {"crypto": 15.0, "default": 5.0}
