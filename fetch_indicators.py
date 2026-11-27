"""Holt Bewertungs- und Marktindikatoren (laeuft im Heartbeat-Workflow, Fehler sind nicht fatal).
Quellen: CBOE (VIX ab 1990), US-Finanzministerium (Zinsen 3 M, 2 J, 10 J), DBnomics (BEA-Wirtschaftsleistung, Fed-Z.1-Boersenwert -> Buffett),
T10Y2Y (Zinskurve 10J-2J); DTB3 (Geldmarkt 3 Monate, taeglich); TB3MS (monatlich ab 1934, fuer Langzeittests).
multpl.com: Shiller-KGV (CAPE) monatlich ab 1871. Ausgabe: data/ind_<NAME>.csv (date,value)."""
import csv, json, os, re, sys, urllib.request
import netz
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp

BROWSER = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36",
           "Accept": "application/json", "Referer": "https://edition.cnn.com/"}


FRED = ["NCBEILQ027S", "GDP", "VIXCLS", "T10Y2Y", "DTB3", "TB3MS"]


def get(url, timeout=20):
    """Ein Versuch, kurzer Timeout: eine haengende Quelle darf den Heartbeat nicht aufhalten."""
    with netz.oeffne(urllib.request.Request(url, headers=BROWSER), timeout=timeout) as r:
        return r.read().decode()


def fred(sid):
    last = None
    for ua in (BROWSER, {"User-Agent": "3kings/1.0"}):
        try:
            with netz.oeffne(urllib.request.Request(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}", headers=ua), timeout=15) as r:
                rows = list(csv.reader(r.read().decode().splitlines()))[1:]
            return {r[0]: float(r[1]) for r in rows if len(r) > 1 and r[1] not in ("", ".")}
        except Exception as e:
            last = e
    raise last


def yahoo(sym, start=631152000):
    import time
    j = json.loads(fp.get(f"https://query2.finance.yahoo.com/v8/finance/chart/{sym}?period1={start}&period2={int(time.time())}&interval=1d"))
    r = j["chart"]["result"][0]
    return {fp.day(t): round(float(c), 4) for t, c in zip(r["timestamp"], r["indicators"]["quote"][0]["close"], strict=False) if c}


def cape():
    html = get("https://www.multpl.com/shiller-pe/table/by-month")
    out = {}
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S):
        txt = re.sub(r"&[#a-zA-Z0-9]+;", " ", re.sub(r"<[^>]+>", " ", tr))
        m = re.search(r"([A-Z][a-z]{2}) (\d{1,2}), (\d{4})\s+([\d.]+)", txt)
        if m:
            mon = "JanFebMarAprMayJunJulAugSepOctNovDec".index(m.group(1)) // 3 + 1
            out[f"{m.group(3)}-{mon:02d}-{int(m.group(2)):02d}"] = float(m.group(4))
    return out


def cnn_fng():
    """CNN Fear & Greed (Aktien, 0-100). Liefert nur ca. 1 Jahr - die Datei waechst taeglich weiter."""
    req = urllib.request.Request("https://production.dataviz.cnn.io/index/fearandgreed/graphdata", headers=BROWSER)
    j = json.loads(netz.oeffne(req, timeout=20).read().decode())
    d = {datetime.fromtimestamp(p["x"] / 1000, timezone.utc).strftime("%Y-%m-%d"): round(float(p["y"]), 1)
         for p in j["fear_and_greed_historical"]["data"]}
    d[datetime.now(timezone.utc).strftime("%Y-%m-%d")] = round(float(j["fear_and_greed"]["score"]), 1)
    return d


def crypto_fng():
    """Crypto Fear & Greed (alternative.me, 0-100, ab 2018)."""
    j = json.loads(get("https://api.alternative.me/fng/?limit=0"))
    return {fp.day(int(p["timestamp"])): float(p["value"]) for p in j["data"]}


def merged(name, new):
    f = f"data/ind_{name}.csv"
    old = {r["date"]: float(r["value"]) for r in csv.DictReader(open(f))} if os.path.exists(f) else {}
    old.update(new); return old


def save(name, d):
    with open(f"data/ind_{name}.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["date", "value"])
        for k in sorted(d): w.writerow([k, d[k]])
    print(f"{name}: {len(d)} Werte, {min(d)} .. {max(d)}, zuletzt {d[max(d)]}")


os.makedirs("data", exist_ok=True)
def cboe_vix():
    rows = list(csv.reader(get("https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv").splitlines()))[1:]
    out = {}
    for r in rows:
        if len(r) >= 5 and r[4]:
            m, d, y = r[0].split("/"); out[f"{y}-{int(m):02d}-{int(d):02d}"] = float(r[4])
    return out


def treasury():
    """US-Finanzministerium, Tageszinsen. Rueckgabe: {datum: (3 Monate, 2 Jahre, 10 Jahre)}."""
    from datetime import date
    out = {}
    for y in (date.today().year - 1, date.today().year):
        url = (f"https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/{y}/all"
               f"?type=daily_treasury_yield_curve&field_tdr_date_value={y}&page&_format=csv")
        rows = list(csv.reader(get(url, 30).splitlines()))
        h = rows[0]; i3, i2, i10 = h.index("3 Mo"), h.index("2 Yr"), h.index("10 Yr")
        for r in rows[1:]:
            try:
                m, d, yy = r[0].split("/"); out[f"{yy}-{int(m):02d}-{int(d):02d}"] = (float(r[i3]), float(r[i2]), float(r[i10]))
            except (ValueError, IndexError):
                pass
    return out


def dbnomics(sid):
    j = json.loads(get(f"https://api.db.nomics.world/v22/series/{sid}?observations=1&format=json", 30))
    doc = j["series"]["docs"][0]; out = {}
    for per, v in zip(doc["period"], doc["value"], strict=False):
        if v in (None, "NA"): continue
        y, q = per.split("-Q"); out[f"{y}-{(int(q) - 1) * 3 + 1:02d}-01"] = float(v)
    return out


def z1_equities():
    last = None
    for sid in ("FED/Z1/LM103164103.Q", "FED/Z1/FL103164103.Q", "FED/Z1/LM103164103"):
        try:
            return dbnomics(sid)
        except Exception as e:
            last = e; print("  Z.1-Kandidat", sid, "->", e)
    raise last


for name, fn in (("VIXCLS", cboe_vix),
                 ("GDP", lambda: {k: v / 1000 for k, v in dbnomics("BEA/NIPA-T10105/A191RC-Q").items()}),   # Mio -> Mrd $
                 ):                                         # Boersenwert: Wilshire 5000 (unten), Z.1 nicht frei abrufbar
    try:
        d = fn()
        if len(d) < 20: raise ValueError(f"nur {len(d)} Werte")
        save(name, d)
    except Exception as e:
        print(name, "fehlgeschlagen:", type(e).__name__, e)
import time as _t
for k in range(3):                                         # Wilshire 5000 (Gesamtmarkt, 1 Punkt ~ 1 Mrd $) fuer den Buffett-Indikator
    try:
        save("W5000", yahoo("%5EW5000", 599616000)); break
    except Exception as e:
        print("W5000 Versuch", k + 1, "fehlgeschlagen:", e); _t.sleep(15)
for k in range(3):                                         # Euro/Dollar (Yahoo ab 2003) fuer die Euro-Sicht
    try:
        save("EURUSD", yahoo("EURUSD%3DX", 946684800)); break
    except Exception as e:
        print("EURUSD Versuch", k + 1, "fehlgeschlagen:", e); _t.sleep(15)
try:
    t = treasury()
    save("T10Y2Y", {d: round(v[2] - v[1], 3) for d, v in t.items()})
    save("DTB3", {d: v[0] for d, v in t.items()})
except Exception as e:
    print("Zinsen (Treasury) fehlgeschlagen:", type(e).__name__, e)
try:
    d = cape()
    if len(d) < 100: raise ValueError(f"nur {len(d)} Werte erkannt")
    save("CAPE", d)
except Exception as e:
    print("CAPE fehlgeschlagen:", e)
for name, fn in (("FNG", cnn_fng), ("CFNG", crypto_fng)):
    try:
        d = fn()
        if len(d) < 5: raise ValueError("zu wenige Werte")
        save(name, merged(name, d))
    except Exception as e:
        print(name, "fehlgeschlagen:", e)
