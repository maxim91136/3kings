"""Test 'nur die Groessten': XLG (Top 50), OEF (S&P 100) gegen SPY, in Euro. Kriterien in REGELN.md 2026-11-19."""
import csv, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp
fx = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
def get(s):
    for i in range(3):
        try: return fp.yahoo(s)
        except Exception as e: print(s, e); time.sleep(10)
def eur(d):
    out, last = {}, None
    for k in sorted(d):
        last = fx.get(k, last)
        if last: out[k] = d[k] / last
    return out
S = {k: eur(get(k)) for k in ["SPY", "XLG", "OEF", "IVV"] if not time.sleep(2)}
def st(p, ds):
    x = np.array([p[d] for d in ds]); eq = x / x[0]; r = x[1:] / x[:-1] - 1
    return (x[-1] / x[0]) ** (252 / len(r)) - 1, float((1 - eq / np.maximum.accumulate(eq)).max())
for k in ["XLG", "OEF"]:
    ds = sorted(set(S[k]) & set(S["SPY"])); ds = [d for d in ds if d >= "2005-06-01"]
    mid = [d for d in ds if d < "2015-01-01"], [d for d in ds if d >= "2015-01-01"]
    print(f"\n{k} vs SPY ab {ds[0]}:")
    for lab, dd in (("gesamt", ds), ("bis 2015", mid[0]), ("ab 2015", mid[1])):
        a, b = st(S[k], dd), st(S["SPY"], dd)
        print(f"  {lab:9s} {k}: {a[0]*100:5.1f} %/J Rueckg {a[1]*100:3.0f} %   SPY: {b[0]*100:5.1f} %/J Rueckg {b[1]*100:3.0f} %")
