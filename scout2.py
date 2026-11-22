"""Talent-Scouting Schritt 2 (nur Ausgabe): Gegenprobe und heutige Talente. Talent = 5 J.: Rendite >= 15 %, unter Wasser <= 15 %, Schwankung <= 30 %, Beta <= 1,15 (vorab aus Schritt 1). Treffer = innerhalb von 5 Jahren danach Kurs-Regeln der Kronjuwelen erfüllt."""

import csv, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp
mem = json.load(open("data/elite_members.json")); meta = json.load(open("data/elite_meta.json"))
import universe, fundamentals
U = json.load(open("data/elite_universe.json"))
pool = {r["sym"]: dict(name=r["name"], cur="USD") for r in universe.sp500() if r["sector"] not in U["cyclic_sectors"]}
for sym, nm, cur, cyc, br, br_en in U["extra"]:
    if not cyc: pool[sym] = dict(name=nm, cur=cur)
fx = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
import bisect; FXD = sorted(fx); FXV = [fx[x] for x in FXD]
def fxl(d):
    i = bisect.bisect_right(FXD, d) - 1; return FXV[i] if i >= 0 else None
def get(s):
    for k in range(3):
        try: return fp.yahoo(s)
        except Exception: time.sleep(3)
spx = get("SPY")
_SK = {}
def weekly(s, a, b):
    k = id(s)
    if k not in _SK:
        ds = sorted(s); wk = [str(np.datetime64(d, "W")) for d in ds]; _SK[k] = (ds, wk)
    ds, wk = _SK[k]
    i, j = bisect.bisect_left(ds, a), bisect.bisect_right(ds, b)
    out = {}
    for d, w in zip(ds[i:j], wk[i:j]): out[w] = (d, s[d])
    return [out[w] for w in sorted(out)]
def yrs_back(d, n): return f"{int(d[:4]) - n}{d[4:]}"
def prof(s, cur, d, n):
    w = weekly(s, yrs_back(d, n), d)
    if len(w) < n * 50: return None
    p = np.array([x[1] for x in w], float)
    dd = 1 - p / np.maximum.accumulate(p); r = np.diff(np.log(p))
    yr = (np.datetime64(w[-1][0]) - np.datetime64(w[0][0])).astype(int) / 365.25
    # Beta 5 J. in Euro gegen S&P 500 in Euro
    wb = weekly(s, yrs_back(d, 5), d); ws = dict(weekly(spx, yrs_back(d, 5), d))
    pairs = [(v / (fxl(dt) if cur == "USD" else 1), ws[dt] / fxl(dt)) for dt, v in wb if dt in ws]
    beta = None
    if len(pairs) > 200:
        a = np.diff(np.log([x[0] for x in pairs])); m = np.diff(np.log([x[1] for x in pairs])); beta = float(np.cov(a, m)[0, 1] / m.var(ddof=1))
    return dict(cagr=float((p[-1] / p[0]) ** (1 / yr) - 1), uw=float((dd > .2).mean()), vol=float(r.std(ddof=1) * np.sqrt(52)), mdd=float(dd.max()), beta=beta)

TAL = lambda p: p and p["cagr"] >= .15 and p["uw"] <= .15 and p["vol"] <= .30 and p["beta"] is not None and p["beta"] <= 1.15
KRO = lambda p: p and p["cagr"] >= .17 and p["uw"] <= .20 and p["vol"] <= .30 and p["beta"] is not None and p["beta"] <= 1.15
T0S = ["2011-11-15", "2013-11-15", "2016-11-15"]
res = {t: dict(n=0, tal=0, tal_hit=0, base_hit=0, names=[]) for t in T0S}; now = []
for sym, p in pool.items():
    s = get(sym); time.sleep(0.4)
    if not s or len(s) < 1500: continue
    _SK.pop(id(s), None)   # id kann von einer früheren Aktie wiederverwendet sein
    days = sorted(s)
    for t0 in T0S:
        if days[0] > yrs_back(t0, 5): continue
        pt = prof(s, p["cur"], t0, 5)
        if not pt: continue
        if KRO(prof(s, p["cur"], t0, 10)): continue          # war damals schon Kronjuwel: kein Talent mehr
        later = [d for d in days if t0 < d <= yrs_back(t0, -5)][::63]
        hit = any(KRO(prof(s, p["cur"], d, 10)) for d in later)
        r = res[t0]; r["n"] += 1; r["base_hit"] += hit
        if TAL(pt): r["tal"] += 1; r["tal_hit"] += hit; r["names"].append((sym, bool(hit)))
    pn = prof(s, p["cur"], days[-1], 5)
    if TAL(pn) and not KRO(prof(s, p["cur"], days[-1], 10)):
        f = fundamentals.fund(sym); time.sleep(0.4)
        now.append(dict(sym=sym, name=p["name"], **{k: round(v, 3) for k, v in pn.items() if v is not None}, margin=f["margin"] and round(f["margin"], 3), nd=f["nd_ebitda"] and round(f["nd_ebitda"], 2), member=sym in mem))
print("RESULT " + json.dumps(dict(test=res, now=sorted(now, key=lambda x: -x["cagr"])), ensure_ascii=False))
