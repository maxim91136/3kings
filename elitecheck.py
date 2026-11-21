"""Elite-Saisonprüfung (Regel: REGELN.md 2026-11-21): harte Regeln mit aktuellen Kursen neu rechnen.
Beta < 1,15 (5 Jahre täglich, in Euro gegen S&P 500 in Euro), 10-Jahres-Rendite >= 17 % p. a. (Heimatwährung, inkl. Dividenden).
Gleiche Methode wie screen.py. Nur Vorschau; Entscheidung am Saisonende. Schreibt site/elite_check.json."""
import csv, json, os
import numpy as np
from elite_steady import steady
O = json.load(open("data/elite_universe.json"))["rules"]["out"]
fx = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
def load(path, col):
    return {r["date"]: float(r[col]) for r in csv.DictReader(open(path)) if r.get(col)}
def eur(s):
    out, last = {}, None
    for d in sorted(s):
        last = fx.get(d, last)
        if last: out[d] = s[d] / last
    return out
spy = eur(load("data/prices.csv", "SPY"))
def beta(p):
    """Beta aus Wochenschlusskursen (letzter Handelstag je Kalenderwoche), 5 Jahre = 260 Wochen, beides in Euro (REGELN 2026-11-21)."""
    wk = {}
    for d in sorted(p):
        if d in spy: wk[np.datetime64(d, "W")] = d
    ds = list(wk.values())[-261:]
    if len(ds) < 120: return None
    a = np.array([p[d] for d in ds]); b = np.array([spy[d] for d in ds]); ra, rb = a[1:] / a[:-1] - 1, b[1:] / b[:-1] - 1
    return float(np.cov(ra, rb)[0, 1] / rb.var(ddof=1))
def cagr10(s):
    ds = sorted(s); d1 = ds[-1]; y = int(d1[:4]) - 10; t = f"{y}{d1[4:]}"
    i0 = next((d for d in ds if d >= t), None)
    if not i0 or ds[0] > t: return None
    return (s[d1] / s[i0]) ** (365.25 / (np.datetime64(d1) - np.datetime64(i0)).astype(int)) - 1
mem = json.load(open("data/elite_members.json"))
cols = [c for c in next(csv.reader(open("data/elite.csv")))[1:] if c in mem]
rows = []
for k in cols:
    s = load("data/elite.csv", k)
    hp = "data/elite_home.csv"; hs = load(hp, k) if os.path.exists(hp) and k in next(csv.reader(open(hp))) else s
    b, c = round(beta(eur(s)), 2), cagr10(hs)
    uw, vol = steady(hs)
    why = (["beta"] if b > O["beta_max"] else []) + (["cagr10"] if c is None or c < O["cagr10_min"] else []) \
        + (["uw"] if uw is not None and uw > O["uw_max"] else []) + (["vol"] if vol is not None and vol > O["vol_max"] else [])
    ok = not why   # Puffer-Grenzen für Mitglieder (REGELN 2026-11-21)
    rows.append({"key": k, "beta": b, "cagr10": None if c is None else round(float(c), 4), "uw": None if uw is None else round(uw, 3),
                 "vol": None if vol is None else round(vol, 3), "pass": ok, "why": why})
hb = json.load(open("site/heartbeat.json"))
out = {"date": sorted(spy)[-1], "season": hb.get("season"), "rows": rows}
json.dump(out, open("site/elite_check.json", "w"), separators=(",", ":"))
for r in rows: print(r)
print(out["date"], out["season"])
