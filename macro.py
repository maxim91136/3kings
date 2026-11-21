"""Makro-Umfeld (nur Information, keine Regel; seit 2026-11-21): Öl (Brent), US-Zins 10 Jahre, EZB-Einlagenzins, Euro/Dollar, Inflation USA und Eurozone.
Quellen: Yahoo (BZ=F), FRED (DGS10, ECBDFR, CPIAUCSL), DBnomics/EZB (HICP Eurozone, Jahresrate), data/ind_EURUSD.csv. Schreibt site/macro.json."""
import csv, json, os, sys, time, urllib.request
from datetime import date
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp
UA = {"User-Agent": "Mozilla/5.0 3kings"}
def get(u, t=25):
    for i in range(3):
        try: return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=t).read().decode()
        except Exception as e: err = e; time.sleep(3 * (i + 1))
    raise err
def fred(sid):
    rows = list(csv.reader(get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}").splitlines()))[1:]
    return [(r[0], float(r[1])) for r in rows if len(r) > 1 and r[1] not in ("", ".")]
def ago(series, days):
    t = date.fromisoformat(series[-1][0]).toordinal() - days
    return next((v for d, v in reversed(series) if date.fromisoformat(d).toordinal() <= t), None)
out, err = {}, {}
fx = [(r["date"], float(r["value"])) for r in csv.DictReader(open("data/ind_EURUSD.csv"))]
try:
    b = sorted(fp.yahoo("BZ=F").items()); fxd = dict(fx); last = None; be = []
    for d, v in b:
        last = fxd.get(d, last)
        if last: be.append((d, v / last))
    out["oil"] = dict(date=b[-1][0], usd=round(b[-1][1], 2), eur=round(be[-1][1], 2), chg1m=round(be[-1][1] / ago(be, 30) - 1, 4), chg1y=round(be[-1][1] / ago(be, 365) - 1, 4))
except Exception as e: err["oil"] = str(e)
try:
    s = fred("DGS10"); out["us10y"] = dict(date=s[-1][0], value=s[-1][1], chg1m=round(s[-1][1] - ago(s, 30), 2), chg1y=round(s[-1][1] - ago(s, 365), 2))
except Exception as e: err["us10y"] = str(e)
try:
    s = fred("ECBDFR"); prev = next((v for d, v in reversed(s) if v != s[-1][1]), None)
    since = next((d for d, v in reversed(s) if v != s[-1][1]), None)
    out["ecb"] = dict(date=s[-1][0], value=s[-1][1], prev=prev, changed=next((s[i + 1][0] for i in range(len(s) - 2, -1, -1) if s[i][1] != s[-1][1]), None))
except Exception as e: err["ecb"] = str(e)
out["eurusd"] = dict(date=fx[-1][0], value=round(fx[-1][1], 4), chg1m=round(fx[-1][1] / ago(fx, 30) - 1, 4), chg1y=round(fx[-1][1] / ago(fx, 365) - 1, 4))
try:
    s = fred("CPIAUCSL"); m = s[-1][0]; prev = next(v for d, v in s if d == f"{int(m[:4]) - 1}{m[4:]}")
    p2 = s[-2]; pprev = next(v for d, v in s if d == f"{int(p2[0][:4]) - 1}{p2[0][4:]}")
    out["cpi_us"] = dict(month=m[:7], value=round(s[-1][1] / prev - 1, 4), prev=round(p2[1] / pprev - 1, 4))
except Exception as e: err["cpi_us"] = str(e)
try:
    j = json.loads(get("https://api.db.nomics.world/v22/series/ECB/ICP/M.U2.N.000000.4.ANR?observations=1&format=json", 30))
    d = j["series"]["docs"][0]; per, val = d["period"], d["value"]
    pts = [(p, v) for p, v in zip(per, val) if v not in (None, "NA")]
    out["cpi_ez"] = dict(month=pts[-1][0], value=round(float(pts[-1][1]) / 100, 4), prev=round(float(pts[-2][1]) / 100, 4))
except Exception as e: err["cpi_ez"] = str(e)
out["errors"] = err
json.dump(out, open("site/macro.json", "w"), indent=1)
print(json.dumps(out, indent=1))
