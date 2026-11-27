"""Holt den S&P 500 (Preisindex ^GSPC, ohne Dividenden) ab 1928 fuer den Langzeittest. Workflow 'spx'.
Ausgabe: data/spx_long.csv (date,SPX). Quelle Yahoo, Ersatz Stooq."""
import csv, os, sys, json
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp

def yahoo_gspc():
    now = int(datetime.now(timezone.utc).timestamp())
    j = json.loads(fp.get(f"https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC?period1=-1325635200&period2={now}&interval=1d"))
    r = j["chart"]["result"][0]
    return {fp.day(t): float(c) for t, c in zip(r["timestamp"], r["indicators"]["quote"][0]["close"], strict=False) if c}

def stooq_spx():
    rows = list(csv.reader(fp.get("https://stooq.com/q/d/l/?s=%5Espx&i=d").splitlines()))[1:]
    return {r[0]: float(r[4]) for r in rows if len(r) > 4 and r[4]}

d = fp.first_ok("SPX", yahoo_gspc, stooq_spx)
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
os.makedirs("data", exist_ok=True)
with open("data/spx_long.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["date", "SPX"])
    for k in sorted(d):
        if k < today:
            w.writerow([k, round(d[k], 4)])
print("spx_long.csv:", len(d), "Tage", min(d), "..", max(d))
