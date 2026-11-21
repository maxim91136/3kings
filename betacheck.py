"""Prüfung: Apple-Beta am 27.10. ungerundet."""
import csv, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp
U = json.load(open("data/elite_universe.json")); I, O = U["rules"]["in"], U["rules"]["out"]
sc = json.load(open("data/elite_screen.json")); hb = json.load(open("site/heartbeat.json"))
spyu = {r["date"]: float(r["SPY"]) for r in csv.DictReader(open("data/prices.csv")) if r.get("SPY")}
cal = sorted(spyu); D = cal[-(hb["season"]["day_in_season"] + 1)]
fxu = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
def get(sym):
    for i in range(3):
        try: return fp.yahoo(sym)
        except Exception: time.sleep(4 * (i + 1))
FX = {"USD": {d: 1 / v for d, v in fxu.items()}}
def eur(s, c):
    if c == "EUR": return s
    if c not in FX: FX[c] = get(f"{c}EUR=X")
    out, last, r = {}, None, FX[c]
    for d in sorted(s):
        last = r.get(d, last)
        if last: out[d] = s[d] * last * (0.01 if c == "GBP" else 1)
    return out
spy = eur(spyu, "USD")
def at(s, D):  # Kurse bis Stichtag
    return {d: v for d, v in s.items() if d <= D}
def beta(p):
    wk = {}
    for d in sorted(p):
        if d in spy: wk[np.datetime64(d, "W")] = d
    ds = list(wk.values())[-261:]
    a = np.array([p[d] for d in ds]); b = np.array([spy[d] for d in ds]); ra, rb = a[1:] / a[:-1] - 1, b[1:] / b[:-1] - 1
    return float(np.cov(ra, rb)[0, 1] / rb.var(ddof=1))
def cagr10(s):
    ds = sorted(s); d1 = ds[-1]; t = f"{int(d1[:4]) - 10}{d1[4:]}"; i0 = next((d for d in ds if d >= t), None)
    return None if not i0 or ds[0] > t else float((s[d1] / s[i0]) ** (365.25 / (np.datetime64(d1) - np.datetime64(i0)).astype(int)) - 1)
s = get("AAPL"); print("RAW", D, repr(beta(at(eur(s, "USD"), D))))
