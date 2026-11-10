# StockPulse: News Score prototype (US large caps)

A pipeline of agents that reads stock news and SEC filings and turns them into a 0–100 News Score per stock.

```
collector  ->  analyst (Claude)  ->  scorer (math)  ->  publisher (static site)
```

| Agent | File | What it does |
|---|---|---|
| Collector | `agents/collector.py` | Yahoo Finance headline RSS, SEC EDGAR 8-K filings, daily prices. No API keys. |
| Analyst | `agents/analyst.py` | Claude reads each item: relevant? sentiment −1..+1, materiality 1–5, event type, reason, and which other ticker it is really about. Results are cached, so you pay once per article. |
| Scorer | `agents/scorer.py` | Recency decay (3-day half-life) × source trust × materiality. Shrinks toward 50 when there's little news. |
| Publisher | `agents/publisher.py` | Bakes the scores into `site/index.html` (static, deploy anywhere). |

## Run it

```bash
export ANTHROPIC_API_KEY=sk-ant-...          # from console.anthropic.com
export SEC_USER_AGENT="StockPulse you@email.com"   # SEC asks for a contact
python3 run.py                # collect -> analyse -> score -> build site
open site/index.html
```

Python 3.10+, standard library only. Data lives in `data/stockpulse.db` (SQLite).
Change the stock list and scoring knobs in `config.py`.

## Put it on autopilot (GitHub Actions + GitHub Pages)

The workflow in `.github/workflows/update.yml` runs every 30 minutes on weekdays during US market hours, then publishes the site.

1. Create a free GitHub account and a new repository (e.g. `stockpulse`). Upload everything in this folder, including the hidden `.github` folder.
2. Get an Anthropic API key at console.anthropic.com. Add credit and set a monthly spending limit.
3. In the repo: **Settings → Secrets and variables → Actions → New repository secret**
   - `ANTHROPIC_API_KEY` = your key
   - `SEC_USER_AGENT` = `StockPulse your@email.com`
4. **Settings → Pages → Source: GitHub Actions.**
5. **Actions tab → Update StockPulse → Run workflow** for the first run. Check the log, then open the Pages link.

From then on it updates by itself. The database is committed back to the repo after each run, so articles are never scored twice.

## Next agents to add

1. **Backtester**: does a high score today predict the next 5-day return? Run this before you make claims about the score.
2. **Licensed news**: Yahoo RSS only returns the latest ~20 headlines per ticker, so history builds up over repeated runs. For a real product use a licensed feed (Finnhub, Polygon, Benzinga) that allows commercial display.
3. **Writer**: a short "why the score moved this week" per ticker, for SEO pages.
4. **QA**: spot-check a sample of analyst labels every day and flag wrong ticker matches.

## Notes

- The first batch of labels (`data/analyst_labels.json`, `scripts/seed_labels.py`) was produced by Claude during the build session, because no API key was set. New articles go through the API.
- Not investment advice. Present it as news sentiment, not as a buy/sell rating.
