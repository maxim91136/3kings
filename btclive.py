"""Bitcoin auch am Wochenende aktuell (REGELN 2026-11-22): aktualisiert nur den Bitcoin-Eintrag in site/assets.json
mit dem letzten abgeschlossenen Tag (UTC), Euro mit dem letzten verfügbaren Wechselkurs. Modelle und data/prices.csv bleiben unberührt."""
import bisect, csv, datetime as dt, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp
s = None
for k in range(3):
    try: s = fp.yahoo("BTC-USD"); break
    except Exception: time.sleep(5)
if not s: raise SystemExit("Bitcoin-Kurs nicht abrufbar")
today = dt.datetime.utcnow().date().isoformat()
ds = sorted(d for d in s if d < today)
fx = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
FD = sorted(fx)
eur = lambda d: s[d] / fx[FD[max(0, bisect.bisect_right(FD, d) - 1)]]
d1, d0 = ds[-1], ds[-2]
y = (dt.date.fromisoformat(d1) - dt.timedelta(days=365)).isoformat(); dy = ds[max(0, bisect.bisect_right(ds, y) - 1)]
p = eur(d1); ath = max(eur(d) for d in ds)
A = json.load(open("site/assets.json"))
for a in A["assets"]:
    if a["key"] == "BTC":
        if a.get("date", "") > d1: raise SystemExit("assets.json ist schon neuer")
        a.update(price=round(p), chg1d=round(p / eur(d0) - 1, 4), chg1y=round(p / eur(dy) - 1, 3), dd_ath=round(1 - p / ath, 4), date=d1, price_date=d1, live=True)
json.dump(A, open("site/assets.json", "w"), ensure_ascii=False)
print("Bitcoin", d1, round(p), "€")
