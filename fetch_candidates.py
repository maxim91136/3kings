"""Holt Kandidatenkurse (Aktien-ETFs, Reserve) und die lange Bitcoin-Historie. Einmaliger Lauf (Workflow 'candidates').
Ausgabe: data/candidates.csv (date + je Kandidat eine Spalte, leer = kein Kurs) und data/btc_long.csv (ab 2010).
Gruppe 1 (aus dem Anleger-Guide): URTH Welt, VT All-World, QUAL Quality, MTUM Momentum, USMV Min-Volatility, XLK IT.
Gruppe 2 (Reserve): TLT/IEF Anleihen, EFA Welt ohne USA, EEM Schwellenlaender, ETH Ethereum.
HINWEIS: gegen die echten APIs noch nicht getestet - das Log des ersten Laufs zeigt es."""
import csv, json, os, sys, time
from datetime import datetime, timedelta, timezone
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp

G1 = ["URTH", "VT", "QUAL", "MTUM", "USMV", "XLK"]
G2 = ["TLT", "IEF", "EFA", "EEM"]


def coinbase(product, start):
    out, t0, now = {}, datetime.fromisoformat(start).replace(tzinfo=timezone.utc), datetime.now(timezone.utc)
    while t0 < now:
        t1 = min(t0 + timedelta(days=299), now)
        url = (f"https://api.exchange.coinbase.com/products/{product}/candles?granularity=86400"
               f"&start={t0:%Y-%m-%dT%H:%M:%SZ}&end={t1:%Y-%m-%dT%H:%M:%SZ}")
        for c in json.loads(fp.get(url)):
            out[fp.day(c[0])] = float(c[4])
        t0 = t1 + timedelta(seconds=1)
        time.sleep(0.4)
    return out


def btc_long():
    d = json.loads(fp.get("https://api.blockchain.info/charts/market-price?timespan=all&sampled=false&metadata=false&format=json"))
    return {fp.day(v["x"]): float(v["y"]) for v in d["values"] if v["y"] and v["y"] > 0}


def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    data = {}
    for t in G1 + G2:
        try:
            data[t] = fp.first_ok(t, lambda t=t: fp.yahoo(t))
        except SystemExit as e:
            print(t, "uebersprungen:", e)
    try:
        data["ETH"] = fp.first_ok("ETH", lambda: coinbase("ETH-USD", "2016-05-01"))
    except SystemExit as e:
        print("ETH uebersprungen:", e)
    days = sorted({d for s in data.values() for d in s if d < today})
    cols = list(data)
    os.makedirs("data", exist_ok=True)
    with open("data/candidates.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["date"] + cols)
        for d in days:
            w.writerow([d] + [round(data[c][d], 6) if d in data[c] else "" for c in cols])
    print(f"candidates.csv: {len(days)} Tage, Spalten: {', '.join(cols)}")
    try:
        b = btc_long()
        with open("data/btc_long.csv", "w", newline="") as f:
            w = csv.writer(f); w.writerow(["date", "BTC"])
            for d in sorted(b):
                if d < today:
                    w.writerow([d, round(b[d], 6)])
        print(f"btc_long.csv: {len(b)} Tage, {min(b)} .. {max(b)}")
    except Exception as e:
        print("btc_long uebersprungen:", e)


if __name__ == "__main__":
    main()
