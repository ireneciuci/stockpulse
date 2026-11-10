"""StockPulse configuration: stock universe and scoring knobs."""
import os

# SEC requires a descriptive User-Agent with a contact email.
USER_AGENT = os.getenv("SEC_USER_AGENT", "StockPulse research contact@example.com")

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "stockpulse.db")
SITE_DATA = os.path.join(os.path.dirname(__file__), "site", "data.json")

# ticker: (SEC CIK, display name, sector)
UNIVERSE = {
    "AAPL": (320193, "Apple", "Technology"),
    "MSFT": (789019, "Microsoft", "Technology"),
    "NVDA": (1045810, "NVIDIA", "Semiconductors"),
    "AMD": (2488, "AMD", "Semiconductors"),
    "INTC": (50863, "Intel", "Semiconductors"),
    "AMZN": (1018724, "Amazon", "Consumer"),
    "GOOGL": (1652044, "Alphabet", "Communication"),
    "META": (1326801, "Meta Platforms", "Communication"),
    "NFLX": (1065280, "Netflix", "Communication"),
    "DIS": (1744489, "Disney", "Communication"),
    "TSLA": (1318605, "Tesla", "Consumer"),
    "WMT": (104169, "Walmart", "Consumer"),
    "KO": (21344, "Coca-Cola", "Consumer"),
    "JPM": (19617, "JPMorgan Chase", "Financials"),
    "V": (1403161, "Visa", "Financials"),
    "UNH": (731766, "UnitedHealth", "Healthcare"),
    "LLY": (59478, "Eli Lilly", "Healthcare"),
    "PFE": (78003, "Pfizer", "Healthcare"),
    "XOM": (2115436, "ExxonMobil", "Energy"),
    "BA": (12927, "Boeing", "Industrials"),
}

# --- scoring knobs ---
LOOKBACK_DAYS = 14          # only news from the last N days counts
HALF_LIFE_DAYS = 3.0        # a 3-day-old article counts half as much as a fresh one
SOURCE_WEIGHTS = {          # how much we trust each source type
    "sec_filing": 1.5,
    "wire": 1.2,            # Reuters, Bloomberg, Business Wire, PR Newswire, company PR
    "news": 1.0,
    "opinion": 0.5,         # Motley Fool / listicles / "should you buy"
}
PRIOR_STRENGTH = 3.0        # shrinks scores toward 50 when a stock has little news
