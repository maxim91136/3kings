"""Talent Scouting (REGELN 2026-11-22, nur Information): Wer könnte ein künftiges Kronjuwel sein?\nTalent = kein Mitglied; 5 J. Wochenkurse: Rendite >= 15 % p. a., höchstens 15 % der Zeit mehr als 20 % unter dem Hoch, Schwankung <= 30 %, Beta <= 1,15 (Euro gegen S&P 500); Bruttomarge >= 45 %; Nettoverschuldung < 2x EBITDA.\nLäuft zu jeder Saisonprüfung (oder --force). Schreibt site/talents.json und data/talents_hist.json (Vorwärtstest: wer wird später Kronjuwel?)."""
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


I = dict(cagr=.15, uw=.15, vol=.30, beta=1.15, margin=.45, nd=2.0)   # Talent-Regeln (REGELN 2026-11-22)
TAL = lambda p: p and p["cagr"] >= I["cagr"] and p["uw"] <= I["uw"] and p["vol"] <= I["vol"] and p["beta"] is not None and p["beta"] <= I["beta"]
sc = json.load(open("data/elite_screen.json")); season = sc.get("season")
old = json.load(open("site/talents.json")) if os.path.exists("site/talents.json") else {}
if old.get("season") == season and "--force" not in sys.argv:
    print("Talent Scouting: keine neue Saison", season); raise SystemExit(0)
rows = []
for sym, p in pool.items():
    if sym in mem: continue
    s = get(sym); time.sleep(0.4)
    if not s or len(s) < 1300: continue
    _SK.pop(id(s), None)
    pn = prof(s, p["cur"], sorted(s)[-1], 5)
    if not TAL(pn): continue
    f = fundamentals.fund(sym); time.sleep(0.4)
    m, nd = f["margin"], f["nd_ebitda"]
    ok = m is not None and m >= I["margin"] and nd is not None and nd < I["nd"]
    why = [] if ok else (["marge"] if m is None or m < I["margin"] else []) + (["schulden"] if nd is None or nd >= I["nd"] else [])
    rows.append(dict(sym=sym, name=p["name"], cagr5=round(pn["cagr"], 3), uw=round(pn["uw"], 3), vol=round(pn["vol"], 3), beta=round(pn["beta"], 2),
                     margin=None if m is None else round(m, 3), nd=None if nd is None else round(nd, 2), ok=ok, why=why))
rows.sort(key=lambda r: (-r["ok"], -r["cagr5"]))
d = sc.get("date") or sorted(spx)[-1]
out = dict(date=d, season=season, rules=I, talents=[r for r in rows if r["ok"]], near=[r for r in rows if not r["ok"]][:12],
           test=dict(t2011=[7, 6, 38, 346], t2013=[122, 38, 56, 355], t2016=[143, 110, 169, 375]))
json.dump(out, open("site/talents.json", "w"), ensure_ascii=False, indent=1)
h = json.load(open("data/talents_hist.json")) if os.path.exists("data/talents_hist.json") else []
h = [x for x in h if x["season"] != season] + [dict(date=d, season=season, talents=[r["sym"] for r in out["talents"]])]
json.dump(h, open("data/talents_hist.json", "w"), ensure_ascii=False, indent=1)
print("Talent Scouting:", [r["sym"] for r in out["talents"]])
