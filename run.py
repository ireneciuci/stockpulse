"""Orchestrator: runs the agents in order. Schedule every 30 min (cron / GitHub Actions).

    python run.py              # collect -> analyse -> score -> export site/data.json
    python run.py --no-collect # re-score without fetching
"""
import sys

import db
from agents import collector, analyst, scorer, publisher


def main():
    con = db.connect()
    if "--no-collect" not in sys.argv:
        collector.run(con)
    analyst.run(con)
    scorer.run(con)
    publisher.run()


if __name__ == "__main__":
    main()
