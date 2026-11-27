"""Bitcoin jeden Tag, auch am Wochenende (REGELN 2026-11-22): Tagesschlusskurse in Euro direkt von Kraken (XBT/EUR, Tageskerzen UTC),
Ersatz Coinbase (BTC-EUR). Aktualisiert nur den Bitcoin-Eintrag in site/assets.json. Modelle und data/prices.csv bleiben unberührt."""
import datetime as dt, json, urllib.request
import netz
UA = {"User-Agent": "Mozilla/5.0 3kings"}
get = lambda u: json.loads(netz.oeffne(urllib.request.Request(u, headers=UA), timeout=20).read())
def kraken():
    j = get("https://api.kraken.com/0/public/OHLC?pair=XBTEUR&interval=1440")
    rows = next(v for k, v in j["result"].items() if k != "last")
    return {dt.datetime.utcfromtimestamp(r[0]).date().isoformat(): float(r[4]) for r in rows}
def coinbase():
    rows = get("https://api.exchange.coinbase.com/products/BTC-EUR/candles?granularity=86400")
    return {dt.datetime.utcfromtimestamp(r[0]).date().isoformat(): float(r[4]) for r in rows}
s = src = None
for name, fn in (("Kraken", kraken), ("Coinbase", coinbase)):
    try: s = fn(); src = name; break
    except Exception as e: print(name, "fehlgeschlagen:", e)
if not s: raise SystemExit("Bitcoin-Kurs nicht abrufbar")
today = dt.datetime.utcnow().date().isoformat()
ds = sorted(d for d in s if d < today)                # nur abgeschlossene Tage
d1, d0 = ds[-1], ds[-2]
A = json.load(open("site/assets.json")); a = next(x for x in A["assets"] if x["key"] == "BTC")
if a.get("date", "") > d1: raise SystemExit("assets.json ist schon neuer")
p = s[d1]
ath = max(max(s[d] for d in ds), a["price"] / (1 - a["dd_ath"]) if a.get("dd_ath") is not None and a["dd_ath"] < 1 else 0)
y = (dt.date.fromisoformat(d1) - dt.timedelta(days=365)).isoformat()
old = [d for d in ds if d <= y]
chg1y = round(p / s[old[-1]] - 1, 3) if old else a.get("chg1y")
a.update(price=round(p), chg1d=round(p / s[d0] - 1, 4), chg1y=chg1y, dd_ath=round(max(0, 1 - p / ath), 4), date=d1, price_date=d1, live=src)
json.dump(A, open("site/assets.json", "w"), ensure_ascii=False)
print("Bitcoin", src, ds[-3:], d1, round(p), "€", a["chg1d"])
