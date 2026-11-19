"""Kopfkarten: Kurs, Veraenderung und Abstand zum Hoch je Asset, alles in Euro -> site/assets.json. Nur Anzeige."""
import csv, json, os
fx = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
fk = sorted(fx)
def rate(d):
    import bisect
    i = bisect.bisect_right(fk, d) - 1
    return fx[fk[max(i, 0)]]
P = list(csv.DictReader(open("data/prices.csv")))
def series(col):
    return {r["date"]: float(r[col]) / rate(r["date"]) for r in P if r.get(col)}
def stats(s):
    ks = sorted(s); last = ks[-1]; prev = ks[-2]
    yago = [k for k in ks if k <= f"{int(last[:4]) - 1}{last[4:]}"]
    return dict(chg1d=round(s[last] / s[prev] - 1, 4), chg1y=round(s[last] / s[yago[-1]] - 1, 4) if yago else None,
                dd_ath=round(1 - s[last] / max(s.values()), 4), date=last)
out = []
spy = stats(series("SPY"))
spx = list(csv.DictReader(open("data/spx_long.csv")))
spy["price"] = round(float(spx[-1]["SPX"]), 2); spy["unit"] = "pts"; spy["price_date"] = spx[-1]["date"]
out.append(dict(key="SPY", **spy))
btc = series("BTC"); b = stats(btc); b["price"] = round(btc[b["date"]], 0); b["unit"] = "eur"; b["price_date"] = b["date"]
out.append(dict(key="BTC", **b))
g = stats(series("GLD")); g["price"] = None; g["unit"] = "eur_oz"
if os.path.exists("data/gold_spot.csv"):
    gs = [r for r in csv.DictReader(open("data/gold_spot.csv")) if r["date"] <= g["date"]]
    if gs:
        g["price"] = round(float(gs[-1]["value"]) / rate(gs[-1]["date"]), 0); g["price_date"] = gs[-1]["date"]
out.append(dict(key="GLD", **g))
json.dump(dict(assets=out), open("site/assets.json", "w"), indent=1)
print("assets.json:", ", ".join(f"{a['key']} {a['price']} ({a['chg1d']*100:+.1f} %, Hoch -{a['dd_ath']*100:.0f} %)" for a in out))
