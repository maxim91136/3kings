"""Talent-Scouting: Wachstumsfilter testen (nur Ausgabe). Wachstum = Umsatz p. a. über 3 Jahre aus SEC-Jahresberichten, nur was zum Stichtag schon veröffentlicht war; Grenze 10 % (vorab festgelegt). Nur US-Firmen."""
import csv, json, os, sys, time
import netz
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp
mem = json.load(open("data/elite_members.json")); meta = json.load(open("data/elite_meta.json"))
import universe
U = json.load(open("data/elite_universe.json"))
pool = {r["sym"]: dict(name=r["name"], cur="USD") for r in universe.sp500() if r["sector"] not in U["cyclic_sectors"]}
for sym, nm, cur, cyc, _br, _br_en in U["extra"]:
    if not cyc: pool[sym] = dict(name=nm, cur=cur)
fx = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
import bisect; FXD = sorted(fx); FXV = [fx[x] for x in FXD]
def fxl(d):
    i = bisect.bisect_right(FXD, d) - 1; return FXV[i] if i >= 0 else None
def get(s):
    for _k in range(3):
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
    for d, w in zip(ds[i:j], wk[i:j], strict=False): out[w] = (d, s[d])
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


SECH = {"User-Agent": "3kings research kontakt@3kings.dev"}
def secget(u):
    for _k in range(3):
        try: return json.loads(netz.oeffne(urllib.request.Request(u, headers=SECH), timeout=30).read())
        except Exception: time.sleep(2)
import urllib.request
CIK = {v["ticker"].replace(".", "-"): str(v["cik_str"]).zfill(10) for v in (secget("https://www.sec.gov/files/company_tickers.json") or {}).values()}
TAGS = ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet", "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueGoodsNet"]
def revenues(sym):
    c = CIK.get(sym)
    if not c: return None
    j = secget(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{c}.json"); time.sleep(0.15)
    if not j: return None
    g = j.get("facts", {}).get("us-gaap", {}); out = {}
    for t in TAGS:
        for x in g.get(t, {}).get("units", {}).get("USD", []):
            if x.get("form") == "10-K" and x.get("fp") == "FY" and x.get("start") and x.get("end"):
                days = (np.datetime64(x["end"]) - np.datetime64(x["start"])).astype(int)
                if 350 <= days <= 380:
                    k = x["end"]
                    if k not in out or x["filed"] < out[k][1]: out[k] = (x["val"], x["filed"])
    return out or None
def growth(rv, t0, yrs=3):
    if not rv: return None
    known = sorted((e, v) for e, (v, f) in rv.items() if f <= t0)
    if not known: return None
    e1, v1 = known[-1]; tgt = np.datetime64(e1) - np.timedelta64(int(365.25 * yrs), "D")
    old = [(e, v) for e, v in known if abs((np.datetime64(e) - tgt).astype(int)) <= 60]
    if not old or old[-1][1] <= 0: return None
    return float((v1 / old[-1][1]) ** (1 / yrs) - 1)

TAL = lambda p: p and p["cagr"] >= .15 and p["uw"] <= .15 and p["vol"] <= .30 and p["beta"] is not None and p["beta"] <= 1.15
KRO = lambda p: p and p["cagr"] >= .17 and p["uw"] <= .20 and p["vol"] <= .30 and p["beta"] is not None and p["beta"] <= 1.15
G = 0.10
T0S = ["2011-11-15", "2013-11-15", "2016-11-15"]
res = {t: dict(n=0, base=0, tal=0, tal_hit=0, gtal=0, gtal_hit=0, grow=0, grow_hit=0, nodata=0, gnames=[]) for t in T0S}; now = []
for sym, p in pool.items():
    if p["cur"] != "USD": continue
    s = get(sym); time.sleep(0.3)
    if not s or len(s) < 1500: continue
    _SK.pop(id(s), None); days = sorted(s); rv = revenues(sym)
    for t0 in T0S:
        if days[0] > yrs_back(t0, 5): continue
        pt = prof(s, p["cur"], t0, 5)
        if not pt or KRO(prof(s, p["cur"], t0, 10)): continue
        later = [d for d in days if t0 < d <= yrs_back(t0, -5)][::63]
        hit = any(KRO(prof(s, p["cur"], d, 10)) for d in later)
        g = growth(rv, t0); r = res[t0]; r["n"] += 1; r["base"] += hit
        if g is None: r["nodata"] += 1
        if g is not None and g >= G: r["grow"] += 1; r["grow_hit"] += hit
        if TAL(pt):
            r["tal"] += 1; r["tal_hit"] += hit
            if g is not None and g >= G: r["gtal"] += 1; r["gtal_hit"] += hit; r["gnames"].append((sym, bool(hit)))
    pn = prof(s, p["cur"], days[-1], 5)
    if TAL(pn) and not KRO(prof(s, p["cur"], days[-1], 10)):
        now.append(dict(sym=sym, name=p["name"], cagr5=round(pn["cagr"], 3), growth3=None if growth(rv, "2099") is None else round(growth(rv, "2099"), 3)))
print("RESULT " + json.dumps(dict(test=res, now=now), ensure_ascii=False))
