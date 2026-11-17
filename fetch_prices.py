"""Holt Tagesschlusskurse: BTC (Coinbase, Reserve Binance-Datenhost), SPY und GLD (Yahoo, Reserve Stooq).
Nur lesen, kein Konto. Ausgabe: data/prices.csv (Spalten date,BTC,SPY,GLD).
Es zaehlen nur ABGESCHLOSSENE Tage (alles ab heute UTC wird verworfen).
HINWEIS: gegen die echten APIs noch nicht getestet - der erste Lauf auf GitHub zeigt es im Log."""
import argparse, csv, json, os, time, urllib.request
from datetime import datetime, timedelta, timezone

UA = {"User-Agent": "Mozilla/5.0 3kings-heartbeat"}


def get(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return r.read().decode()
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))


def day(ts):
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d")


def coinbase_btc(start="2015-01-01"):
    out, t0 = {}, datetime.fromisoformat(start).replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    while t0 < now:
        t1 = min(t0 + timedelta(days=299), now)
        url = ("https://api.exchange.coinbase.com/products/BTC-USD/candles?granularity=86400"
               f"&start={t0:%Y-%m-%dT%H:%M:%SZ}&end={t1:%Y-%m-%dT%H:%M:%SZ}")
        for c in json.loads(get(url)):                      # [time, low, high, open, close, volume]
            out[day(c[0])] = float(c[4])
        t0 = t1 + timedelta(seconds=1)
        time.sleep(0.4)
    return out


def binance_btc(start="2017-09-01"):
    t = int(datetime.fromisoformat(start).replace(tzinfo=timezone.utc).timestamp() * 1000)
    out = {}
    while True:
        ks = json.loads(get(f"https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1d&startTime={t}&limit=1000"))
        if not ks:
            break
        for k in ks:
            out[day(k[0] / 1000)] = float(k[4])
        t = ks[-1][0] + 86400000
        if len(ks) < 1000:
            break
        time.sleep(0.3)
    return out


def yahoo(sym):
    d = json.loads(get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=max&interval=1d&events=div,splits"))
    r = d["chart"]["result"][0]
    px = r["indicators"].get("adjclose", [{}])[0].get("adjclose") or r["indicators"]["quote"][0]["close"]
    return {day(t): p for t, p in zip(r["timestamp"], px) if p}


def stooq(sym):
    rows = list(csv.reader(get(f"https://stooq.com/q/d/l/?s={sym.lower()}.us&i=d").splitlines()))[1:]
    return {r[0]: float(r[4]) for r in rows if len(r) > 4 and r[4]}


def first_ok(label, *fns):
    for fn in fns:
        try:
            d = fn()
            if len(d) > 200:
                print(f"{label}: {len(d)} Tage via {fn.__name__ if hasattr(fn, '__name__') else fn}")
                return d
        except Exception as e:
            print(f"{label}: Quelle fehlgeschlagen ({e})")
    raise SystemExit(f"{label}: keine Quelle erreichbar - Lauf abgebrochen (alte Daten bleiben unveraendert)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/prices.csv")
    a = ap.parse_args()
    data = {
        "BTC": first_ok("BTC", coinbase_btc, binance_btc),
        "SPY": first_ok("SPY", lambda: yahoo("SPY"), lambda: stooq("SPY")),
        "GLD": first_ok("GLD", lambda: yahoo("GLD"), lambda: stooq("GLD")),
    }
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    days = sorted(d for d in set(data["SPY"]) & set(data["GLD"]) & set(data["BTC"]) if d < today)
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "BTC", "SPY", "GLD"])
        for d in days:
            w.writerow([d] + [round(data[n][d], 6) for n in ("BTC", "SPY", "GLD")])
    print(f"{len(days)} gemeinsame Handelstage ({days[0]} .. {days[-1]}) -> {a.out}")


if __name__ == "__main__":
    main()
