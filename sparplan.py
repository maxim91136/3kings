"""Kaufsignal fuer neues Geld + Schattenbuch Sparplan (laeuft taeglich nach dem Heartbeat).
Regel "nicht am Hoch" (REGELN.md): kaufen, wenn der S&P mindestens 3 % unter seinem Allzeithoch liegt, sonst sammeln.
Schattenbuch: ab Start jeden Monat 100 EUR virtuell, einmal nach Regel, einmal sofort. Papierrechnung ohne Kosten/Steuern.
Ausgabe: data/sparplan.json (Zustand), site/sparplan.json (Seite)."""
import csv, json, os

USE_EUR = True          # Signal und Schattenbuch in Euro (Entscheidung siehe REGELN.md), sonst Dollar
THRESH, RATE = -0.03, 100.0

rows = list(csv.DictReader(open("data/prices.csv")))
spy = [(r["date"], float(r["SPY"])) for r in rows if r["SPY"]]
cur = "USD"
if USE_EUR and os.path.exists("data/ind_EURUSD.csv"):
    fx = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
    out, last = [], None
    for d, p in spy:
        last = fx.get(d, last)
        if last: out.append((d, p / last))
    if len(out) > 200: spy, cur = out, "EUR"
ath = max(p for _, p in spy); date, price = spy[-1]
dd = price / ath - 1; buy = dd <= THRESH

st = json.load(open("data/sparplan.json")) if os.path.exists("data/sparplan.json") else \
    dict(start=date, last_date=None, last_month=None, plans={k: dict(units=0.0, cash=0.0, paid=0.0) for k in ("regel", "sofort")}, rows=[])
if st["last_date"] != date:
    if st["last_month"] != date[:7]:
        for pl in st["plans"].values(): pl["cash"] += RATE; pl["paid"] += RATE
        st["last_month"] = date[:7]
    for k, pl in st["plans"].items():
        if pl["cash"] > 0 and (k == "sofort" or buy):
            pl["units"] += pl["cash"] / price; pl["cash"] = 0.0
    val = {k: pl["units"] * price + pl["cash"] for k, pl in st["plans"].items()}
    st["rows"].append(dict(date=date, regel=round(val["regel"], 2), sofort=round(val["sofort"], 2), paid=st["plans"]["regel"]["paid"]))
    st["last_date"] = date
    json.dump(st, open("data/sparplan.json", "w"), indent=1)
pub = dict(date=date, currency=cur, dd_ath=round(dd, 4), signal="kaufen" if buy else "sammeln", thresh=THRESH,
           start=st["start"], plans={k: dict(value=round(pl["units"] * price + pl["cash"], 2), cash=round(pl["cash"], 2), paid=pl["paid"]) for k, pl in st["plans"].items()},
           rows=st["rows"][-400:])
json.dump(pub, open("site/sparplan.json", "w"), indent=1)
print(f"Sparplan {date}: S&P {dd*100:+.1f} % zum Allzeithoch ({cur}) -> {pub['signal']}; Regel {pub['plans']['regel']['value']:.2f} / sofort {pub['plans']['sofort']['value']:.2f} (eingezahlt {pub['plans']['regel']['paid']:.0f})")
