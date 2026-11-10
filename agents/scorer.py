"""Scorer agent: plain math, no AI. Turns analysed articles into a 0-100 News Score.

For every relevant article in the lookback window:
    weight = time_decay(age) * source_weight * materiality
    signal = sum(weight * sentiment) / (sum(weight) + PRIOR_STRENGTH)
    score  = 50 + 50 * tanh(2 * signal)
50 = neutral news flow. PRIOR_STRENGTH pulls stocks with only a few articles toward 50,
so one stray headline can't send a quiet stock to 95.
"""
import json
import math
from datetime import datetime, timezone, timedelta

from config import (UNIVERSE, LOOKBACK_DAYS, HALF_LIFE_DAYS, SOURCE_WEIGHTS, PRIOR_STRENGTH, SITE_DATA)


def _rows(con, ticker):
    return con.execute("""SELECT a.*, x.sentiment, x.materiality, x.event_type, x.reason, x.relevant
                          FROM articles a JOIN analyses x ON x.article_id=a.id
                          WHERE a.ticker=? ORDER BY a.published_at DESC""", (ticker,)).fetchall()


def score_at(rows, as_of):
    num = den = 0.0
    contrib = []
    for r in rows:
        if not r["relevant"]:
            continue
        pub = datetime.fromisoformat(r["published_at"])
        age = (as_of - pub).total_seconds() / 86400
        if age < -0.01 or age > LOOKBACK_DAYS:
            continue
        w = 0.5 ** (max(age, 0) / HALF_LIFE_DAYS) * SOURCE_WEIGHTS.get(r["source_type"], 1.0) * r["materiality"]
        num += w * r["sentiment"]
        den += w
        contrib.append((w * r["sentiment"], w, r))
    signal = num / (den + PRIOR_STRENGTH)
    return round(50 + 50 * math.tanh(2 * signal), 1), den, contrib


def run(con):
    now = datetime.now(timezone.utc)
    out = {"generated_at": now.isoformat(), "method": __doc__.strip(), "stocks": []}
    for ticker, (_cik, name, sector) in UNIVERSE.items():
        rows = _rows(con, ticker)
        score, buzz, contrib = score_at(rows, now)
        prev, _, _ = score_at(rows, now - timedelta(days=3))
        drivers = sorted(contrib, key=lambda c: -abs(c[0]))[:3]
        con.execute("INSERT OR REPLACE INTO scores VALUES (?,?,?,?,?)",
                    (ticker, now.date().isoformat(), score, len(contrib),
                     json.dumps([d[2]["id"] for d in drivers])))

        prices = con.execute("SELECT date, close FROM prices WHERE ticker=? ORDER BY date", (ticker,)).fetchall()
        closes = [p["close"] for p in prices]
        chg5 = (closes[-1] / closes[-6] - 1) * 100 if len(closes) > 6 else None

        events = {}
        for _, w, r in contrib:
            e = events.setdefault(r["event_type"], [0, 0.0])
            e[0] += 1
            e[1] += w * r["sentiment"]
        top = {d[2]["id"] for d in drivers}
        out["stocks"].append(dict(
            ticker=ticker, name=name, sector=sector, score=score, prev_score=prev,
            n_articles=len(contrib), n_scanned=len(rows), buzz=round(buzz, 1),
            price=round(closes[-1], 2) if closes else None,
            change_5d=round(chg5, 2) if chg5 is not None else None,
            prices=[[p["date"], round(p["close"], 2)] for p in prices[-60:]],
            events={k: {"count": v[0], "impact": round(v[1], 2)} for k, v in events.items()},
            articles=[dict(title=r["title"], url=r["url"], source=r["source"], source_type=r["source_type"],
                           date=r["published_at"], sentiment=r["sentiment"], materiality=r["materiality"],
                           event=r["event_type"], reason=r["reason"], impact=round(c, 2), driver=r["id"] in top)
                      for c, w, r in sorted(contrib, key=lambda c: c[2]["published_at"], reverse=True)],
        ))
    con.commit()
    out["stocks"].sort(key=lambda s: -s["score"])
    with open(SITE_DATA, "w") as f:
        json.dump(out, f, indent=1)
    print("scorer: " + ", ".join(f'{s["ticker"]} {s["score"]:.0f}' for s in out["stocks"]))
    return out
