"""SQLite storage shared by all agents. Swap for Postgres (Neon) in production."""
import sqlite3
from config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS articles (
    id TEXT PRIMARY KEY,          -- hash of url
    ticker TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT,
    source TEXT,                  -- publisher domain or 'SEC EDGAR'
    source_type TEXT,             -- sec_filing | wire | news | opinion
    published_at TEXT,            -- ISO UTC
    summary TEXT,
    fetched_at TEXT
);
CREATE TABLE IF NOT EXISTS analyses (
    article_id TEXT PRIMARY KEY REFERENCES articles(id),
    relevant INTEGER,             -- 1 if the article is materially about this ticker
    sentiment REAL,               -- -1 .. +1
    materiality INTEGER,          -- 1 .. 5
    event_type TEXT,
    reason TEXT,
    model TEXT,
    analyzed_at TEXT
);
CREATE TABLE IF NOT EXISTS prices (
    ticker TEXT, date TEXT, close REAL,
    PRIMARY KEY (ticker, date)
);
CREATE TABLE IF NOT EXISTS scores (
    ticker TEXT, as_of TEXT, score REAL, n_articles INTEGER, drivers TEXT,
    PRIMARY KEY (ticker, as_of)
);
"""


def connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    return con
