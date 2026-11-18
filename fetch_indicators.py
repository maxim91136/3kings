"""Holt Bewertungs- und Marktindikatoren (laeuft im Heartbeat-Workflow, Fehler sind nicht fatal).
FRED: NCBEILQ027S (Boersenwert US-Firmen, Mio $) und GDP (Mrd $) -> Buffett-Indikator; VIXCLS (Angst-Index);
T10Y2Y (Zinskurve 10J-2J); DTB3 (Geldmarkt 3 Monate, taeglich); TB3MS (monatlich ab 1934, fuer Langzeittests).
multpl.com: Shiller-KGV (CAPE) monatlich ab 1871. Ausgabe: data/ind_<NAME>.csv (date,value)."""
import csv, json, os, re, sys, urllib.request
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp

BROWSER = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36",
           "Accept": "application/json", "Referer": "https://edition.cnn.com/"}


FRED = ["NCBEILQ027S", "GDP", "VIXCLS", "T10Y2Y", "DTB3", "TB3MS"]


def get(url, timeout=20):
    """Ein Versuch, kurzer Timeout: eine haengende Quelle darf den Heartbeat nicht aufhalten."""
    with urllib.request.urlopen(urllib.request.Request(url, headers=BROWSER), timeout=timeout) as r:
        return r.read().decode()


def fred(sid):
    last = None
    for ua in (BROWSER, {"User-Agent": "3kings/1.0"}):
        try:
            with urllib.request.urlopen(urllib.request.Request(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}", headers=ua), timeout=15) as r:
                rows = list(csv.reader(r.read().decode().splitlines()))[1:]
            return {r[0]: float(r[1]) for r in rows if len(r) > 1 and r[1] not in ("", ".")}
        except Exception as e:
            last = e
    raise last


def yahoo(sym, start=631152000):
    import time
    j = json.loads(get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?period1={start}&period2={int(time.time())}&interval=1d"))
    r = j["chart"]["result"][0]
    return {fp.day(t): round(float(c), 4) for t, c in zip(r["timestamp"], r["indicators"]["quote"][0]["close"]) if c}


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
    j = json.loads(urllib.request.urlopen(req, timeout=20).read().decode())
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
fred_ok = True
for sid in FRED:
    if not fred_ok:
        print(sid, "uebersprungen (FRED nicht erreichbar)"); continue
    try:
        d = fred(sid)
        if len(d) < 20: raise ValueError("zu wenige Werte")
        save(sid, d)
    except Exception as e:
        print(sid, "fehlgeschlagen:", type(e).__name__, e); fred_ok = False
# Ersatz ueber Yahoo, wenn FRED fehlt: VIX, Zinsen 10 J (^TNX) und 3 M (^IRX)
if not os.path.exists("data/ind_VIXCLS.csv") or not fred_ok:
    try: save("VIXCLS", yahoo("%5EVIX"))
    except Exception as e: print("VIX (Yahoo) fehlgeschlagen:", e)
try:
    tnx, irx = yahoo("%5ETNX", 1577836800), yahoo("%5EIRX", 1577836800)
    save("IRX", irx)
    save("CURVE", {d: round(tnx[d] - irx[d], 3) for d in tnx if d in irx})
except Exception as e:
    print("Zinsen (Yahoo) fehlgeschlagen:", e)
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
