"""Analyst agent: reads each new article and returns structured JSON.

Uses Claude via the Messages API when ANTHROPIC_API_KEY is set. Articles are
sent in batches per ticker, so one call scores ~20 headlines.
Results are cached in the `analyses` table so an article is never paid for twice.

Optional: data/analyst_labels.json ({article_id: {...}}) is loaded first, which
lets you import labels produced elsewhere (e.g. a human-reviewed batch).
"""
import hashlib
import json
import os
import urllib.request
from datetime import datetime, timezone

from config import UNIVERSE

MODEL = os.getenv("ANALYST_MODEL", "claude-haiku-4-5")
LABELS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "analyst_labels.json")

EVENT_TYPES = ["earnings", "guidance", "analyst_rating", "product", "deal_mna", "legal_regulatory",
               "management", "capital_return", "macro_sector", "governance_scandal", "filing_routine", "other"]

PROMPT = """You are an equity news analyst. For the company {name} (ticker {ticker}), score each item below.

Return ONLY a JSON array, one object per item, in the same order:
{{"id": str,
  "relevant": bool,        // false if the item is mainly about another company, a market roundup, or a listicle that only mentions {ticker}
  "sentiment": float,      // -1 (very negative for {ticker}'s shareholders) .. +1 (very positive); 0 if neutral
  "materiality": int,      // 1 trivial/opinion .. 5 could move the stock >5% (earnings surprise, scandal, M&A, major guidance)
  "event_type": one of {events},
  "reason": str,           // max 15 words, factual, why this score
  "also_about": [str]      // other tickers from {universe} this item is mainly about (often the real subject)
}}
Judge the news, not the headline's tone. Opinion pieces ("Should you buy...") get materiality 1.

Items:
{items}"""


def _call_claude(prompt):
    req = urllib.request.Request(
        os.getenv("ANTHROPIC_API_URL", "https://api.anthropic.com/v1/messages"),
        data=json.dumps({"model": MODEL, "max_tokens": 4000,
                         "messages": [{"role": "user", "content": prompt}]}).encode(),
        headers={"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01",
                 "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        text = json.loads(r.read())["content"][0]["text"]
    return json.loads(text[text.index("["): text.rindex("]") + 1])


def _save(con, aid, res, model):
    con.execute("INSERT OR REPLACE INTO analyses VALUES (?,?,?,?,?,?,?,?)", (
        aid, int(bool(res["relevant"])), max(-1.0, min(1.0, float(res["sentiment"]))),
        max(1, min(5, int(res["materiality"]))), res.get("event_type", "other"),
        res.get("reason", "")[:200], model, datetime.now(timezone.utc).isoformat()))


def run(con):
    # 1) import any pre-made labels
    if os.path.exists(LABELS_FILE):
        labels = json.load(open(LABELS_FILE))
        known = {r[0] for r in con.execute("SELECT id FROM articles")}
        for aid, res in labels.items():
            if aid in known:
                _save(con, aid, res, res.get("model", "imported"))
        con.commit()

    pending = con.execute("""SELECT a.* FROM articles a LEFT JOIN analyses x ON x.article_id=a.id
                             WHERE x.article_id IS NULL ORDER BY ticker""").fetchall()
    if not pending:
        print("analyst: nothing new")
        return 0
    if not os.getenv("ANTHROPIC_API_KEY"):
        print(f"analyst: {len(pending)} articles waiting; set ANTHROPIC_API_KEY to score them")
        return 0

    by_ticker = {}
    for a in pending:
        by_ticker.setdefault(a["ticker"], []).append(a)
    done = 0
    for ticker, arts in by_ticker.items():
        for i in range(0, len(arts), 25):
            chunk = arts[i:i + 25]
            items = "\n".join(f'- id={a["id"]} | {a["source"]} | {a["published_at"][:10]} | {a["title"]}'
                              + (f' | {a["summary"][:200]}' if a["summary"] else "") for a in chunk)
            try:
                results = _call_claude(PROMPT.format(name=UNIVERSE[ticker][1], ticker=ticker,
                                                     events=EVENT_TYPES, items=items,
                                                     universe=list(UNIVERSE)))
            except Exception as e:
                print(f"  ! analyst {ticker}: {e}")
                continue
            by_id = {a["id"]: a for a in chunk}
            for res in results:
                a = by_id.get(res.get("id"))
                if not a:
                    continue
                _save(con, a["id"], res, MODEL)
                done += 1
                # Route the article to the company it is really about; it gets scored
                # from that company's point of view on the next run.
                for other in res.get("also_about") or []:
                    if other in UNIVERSE and other != ticker:
                        nid = hashlib.sha1(f"{other}|{a['url']}".encode()).hexdigest()[:16]
                        con.execute("INSERT OR IGNORE INTO articles VALUES (?,?,?,?,?,?,?,?,?)",
                                    (nid, other, a["title"], a["url"], a["source"], a["source_type"],
                                     a["published_at"], a["summary"], a["fetched_at"]))
        con.commit()
    print(f"analyst: scored {done} articles")
    return done
