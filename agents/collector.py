"""Collector agent: pulls news, SEC filings and prices for every ticker.

Sources (all free, no API key):
  - Yahoo Finance headline RSS per ticker
  - SEC EDGAR recent 8-K filings (material events) per company
  - Yahoo chart API for daily closes
For production, add a licensed news API (Finnhub / Polygon / Benzinga) here.
"""
import hashlib
import json
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from urllib.parse import urlparse

from config import UNIVERSE, USER_AGENT, LOOKBACK_DAYS

WIRE = ("reuters", "bloomberg", "businesswire", "prnewswire", "globenewswire", "wsj", "ft.com", "cnbc", "apnews")
OPINION = ("fool.com", "247wallst", "zacks", "seekingalpha", "investorplace", "benzinga.com/markets/prediction", "beincrypto", "trefis")

# 8-K item codes -> human readable event (subset)
ITEMS_8K = {
    "1.01": "Material agreement", "1.02": "Agreement terminated", "1.03": "Bankruptcy",
    "2.01": "Acquisition/disposal completed", "2.02": "Earnings results", "2.05": "Restructuring / exit costs",
    "2.06": "Impairment", "3.01": "Delisting notice", "4.02": "Restatement (non-reliance)",
    "5.02": "Executive / board change", "5.07": "Shareholder vote", "7.01": "Reg FD disclosure",
    "8.01": "Other material event", "9.01": "Financial exhibits",
}


def _get(url, ua="Mozilla/5.0 (StockPulse)"):
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read()


def _id(*parts):
    return hashlib.sha1("|".join(parts).encode()).hexdigest()[:16]


def _source_type(domain, url):
    s = (domain + url).lower()
    if any(k in s for k in OPINION):
        return "opinion"
    if any(k in s for k in WIRE):
        return "wire"
    return "news"


def fetch_yahoo_news(ticker):
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
    root = ET.fromstring(_get(url))
    out = []
    for it in root.iter("item"):
        link = it.findtext("link") or ""
        title = (it.findtext("title") or "").strip()
        pub = parsedate_to_datetime(it.findtext("pubDate")).astimezone(timezone.utc)
        domain = urlparse(link).netloc.replace("www.", "")
        out.append(dict(
            id=_id(ticker, link or title), ticker=ticker, title=title, url=link,
            source=domain, source_type=_source_type(domain, link),
            published_at=pub.isoformat(), summary=(it.findtext("description") or "")[:500],
        ))
    return out


def fetch_sec_8k(ticker, cik):
    data = json.loads(_get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json", ua=USER_AGENT))
    rec = data["filings"]["recent"]
    cutoff = (datetime.now(timezone.utc) - timedelta(days=LOOKBACK_DAYS)).date().isoformat()
    out = []
    for form, date, acc, doc, items in zip(rec["form"], rec["filingDate"], rec["accessionNumber"],
                                           rec["primaryDocument"], rec["items"]):
        if form not in ("8-K", "8-K/A") or date < cutoff:
            continue
        codes = [c.strip() for c in items.split(",") if c.strip()]
        labels = [ITEMS_8K.get(c, f"Item {c}") for c in codes if c != "9.01"] or ["Filing"]
        link = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc.replace('-', '')}/{doc}"
        out.append(dict(
            id=_id(ticker, acc), ticker=ticker, title=f"{form}: " + "; ".join(labels), url=link,
            source="SEC EDGAR", source_type="sec_filing",
            published_at=f"{date}T21:00:00+00:00", summary="8-K items: " + items,
        ))
    return out


def fetch_prices(ticker):
    j = json.loads(_get(f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=3mo&interval=1d"))
    r = j["chart"]["result"][0]
    closes = r["indicators"]["quote"][0]["close"]
    return [(ticker, datetime.fromtimestamp(t, timezone.utc).date().isoformat(), c)
            for t, c in zip(r["timestamp"], closes) if c is not None]


def run(con):
    now = datetime.now(timezone.utc).isoformat()
    new = 0
    for ticker, (cik, _name, _sector) in UNIVERSE.items():
        items = []
        for fn, args in ((fetch_yahoo_news, (ticker,)), (fetch_sec_8k, (ticker, cik))):
            try:
                items += fn(*args)
            except Exception as e:  # one bad source never kills the run
                print(f"  ! {fn.__name__} {ticker}: {e}")
        for a in items:
            cur = con.execute(
                "INSERT OR IGNORE INTO articles VALUES (:id,:ticker,:title,:url,:source,:source_type,:published_at,:summary,:f)",
                {**a, "f": now})
            new += cur.rowcount
        try:
            con.executemany("INSERT OR REPLACE INTO prices VALUES (?,?,?)", fetch_prices(ticker))
        except Exception as e:
            print(f"  ! prices {ticker}: {e}")
        time.sleep(0.3)  # be polite (SEC limit is 10 req/s)
    con.commit()
    print(f"collector: {new} new articles")
    return new
