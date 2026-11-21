"""Makro-Umfeld (nur Information, keine Regel; seit 2026-11-21): Öl (Brent), US-Zins 10 Jahre, EZB-Einlagenzins, Euro/Dollar, Inflation USA und Eurozone.
Quellen: Yahoo (BZ=F, ^TNX), EZB-Datenportal (Einlagenzins), Eurostat (HICP), US-Statistikbehörde BLS (CPI-U), data/ind_EURUSD.csv. Schreibt site/macro.json."""
import csv, json, os, signal, sys, time, urllib.request
signal.signal(signal.SIGALRM, lambda *a: (_ for _ in ()).throw(TimeoutError("Quelle zu langsam")))
from datetime import date
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp
UA = {"User-Agent": "Mozilla/5.0 3kings"}
def get(u, t=10):   # harte Grenze: eine langsame Quelle darf nichts blockieren
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=t).read().decode()
def fred(sid):
    rows = list(csv.reader(get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}").splitlines()))[1:]
    return [(r[0], float(r[1])) for r in rows if len(r) > 1 and r[1] not in ("", ".")]
def ago(series, days):
    t = date.fromisoformat(series[-1][0]).toordinal() - days
    return next((v for d, v in reversed(series) if date.fromisoformat(d).toordinal() <= t), None)
out, err = {}, {}
fx = [(r["date"], float(r["value"])) for r in csv.DictReader(open("data/ind_EURUSD.csv"))]
signal.alarm(20)
try:
    b = sorted(fp.yahoo("BZ=F").items()); fxd = dict(fx); last = None; be = []
    for d, v in b:
        last = fxd.get(d, last)
        if last: be.append((d, v / last))
    out["oil"] = dict(date=b[-1][0], usd=round(b[-1][1], 2), eur=round(be[-1][1], 2), chg1m=round(be[-1][1] / ago(be, 30) - 1, 4), chg1y=round(be[-1][1] / ago(be, 365) - 1, 4))
except Exception as e: err["oil"] = str(e)
signal.alarm(20)
try:   # US-Zins 10 Jahre: Yahoo ^TNX (in Prozent)
    t = sorted(fp.yahoo("%5ETNX").items()); out["us10y"] = dict(date=t[-1][0], value=round(t[-1][1], 2), chg1m=round(t[-1][1] - ago(t, 30), 2), chg1y=round(t[-1][1] - ago(t, 365), 2))
except Exception as e: err["us10y"] = str(e)
signal.alarm(20)
def ecb(key, n):   # EZB-Datenportal, CSV
    rows = list(csv.DictReader(get(f"https://data-api.ecb.europa.eu/service/data/{key}?lastNObservations={n}&format=csvdata", 15).splitlines()))
    return [(r["TIME_PERIOD"], float(r["OBS_VALUE"])) for r in rows if r.get("OBS_VALUE")]
try:   # EZB-Einlagenzins
    s = ecb("FM/D.U2.EUR.4F.KR.DFR.LEV", 2000)
    out["ecb"] = dict(date=s[-1][0], value=s[-1][1], changed=next((s[i + 1][0] for i in range(len(s) - 2, -1, -1) if s[i][1] != s[-1][1]), None))
except Exception as e: err["ecb"] = str(e)
signal.alarm(0)
out["eurusd"] = dict(date=fx[-1][0], value=round(fx[-1][1], 4), chg1m=round(fx[-1][1] / ago(fx, 30) - 1, 4), chg1y=round(fx[-1][1] / ago(fx, 365) - 1, 4))
signal.alarm(20)
try:   # Inflation USA: US-Statistikbehörde (CPI-U, Vorjahresrate selbst gerechnet)
    j = json.loads(get("https://api.bls.gov/publicAPI/v1/timeseries/data/CUUR0000SA0", 15))
    d = {f'{x["year"]}-{x["period"][1:]}': float(x["value"]) for x in j["Results"]["series"][0]["data"] if x["period"].startswith("M") and x["period"] != "M13" and x["value"].replace(".", "", 1).isdigit()}
    yoy = lambda m: d[m] / d[f"{int(m[:4]) - 1}{m[4:]}"] - 1
    ks = [k for k in sorted(d) if f"{int(k[:4]) - 1}{k[4:]}" in d]; m0, m1 = ks[-1], ks[-2]
    out["cpi_us"] = dict(month=m0, value=round(yoy(m0), 4), prev=round(yoy(m1), 4))
except Exception as e: err["cpi_us"] = str(e)
signal.alarm(20)
try:   # Inflation Eurozone: Eurostat HICP, ab 2026 nach neuer Klassifikation (teicp000, Jahresrate)
    j = json.loads(get("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/teicp000?geo=EA&lastTimePeriod=3", 15))
    ids, size = j["id"], j["size"]; cat = {d: j["dimension"][d]["category"]["index"] for d in ids}
    fix = {d: (next((k for k in cat[d] if k in ("RCH_A", "PCH_M12")), None) if d == "unit" else None) for d in ids}
    per = sorted(cat["time"], key=cat["time"].get); v = []
    for p_ in per:
        pos = {d: (cat[d][p_] if d == "time" else cat[d][fix[d]] if fix[d] else 0) for d in ids}
        n = 0
        for d, sz in zip(ids, size): n = n * sz + pos[d]
        if str(n) in j["value"]: v.append((p_, float(j["value"][str(n)])))
    out["cpi_ez"] = dict(month=v[-1][0], value=round(v[-1][1] / 100, 4), prev=round(v[-2][1] / 100, 4) if len(v) > 1 else None)
except Exception as e: err["cpi_ez"] = str(e)
signal.alarm(0)
old = json.load(open("site/macro.json")) if os.path.exists("site/macro.json") else {}
for k in err:
    if k in old: out[k] = dict(old[k], stale=True)
out["errors"] = err
json.dump(out, open("site/macro.json", "w"), indent=1)
print(json.dumps(out, indent=1))
