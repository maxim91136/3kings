"""Chronik Einmalanlage S&P 500 (REGELN 2026-11-22): sofort, in 12 Raten, Warten auf minus 20 Prozent. In Euro, wie sparplan.py.
Ausgabe: data/einmal.json (Zustand), site/einmal.json (Seite). Papierrechnung ohne Kosten/Steuern, Bargeld 0 % Zins."""
import csv, json, os
START, THRESH, N = "2026-11-20", -0.20, 12
rows = list(csv.DictReader(open("data/prices.csv")))
spy = [(r["date"], float(r["SPY"])) for r in rows if r["SPY"]]
cur = "USD"
if os.path.exists("data/ind_EURUSD.csv"):
    fx = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
    out, last = [], None
    for d, p in spy:
        last = fx.get(d, last)
        if last: out.append((d, p / last))
    if len(out) > 200: spy, cur = out, "EUR"
ath = 0.0; ath_at = {}
for d, p in spy: ath = max(ath, p); ath_at[d] = ath
P = dict(spy)
st = json.load(open("data/einmal.json")) if os.path.exists("data/einmal.json") else dict(start=START, last_date=None, months=[], v=dict(sofort=dict(units=0.0, cash=1.0), raten=dict(units=0.0, cash=1.0), warten=dict(units=0.0, cash=1.0)), bought_warten=None, n_raten=0, rows=[])
for d, price in spy:
    if d < st["start"] or (st["last_date"] and d <= st["last_date"]): continue
    v = st["v"]
    if st["last_date"] is None:   # Starttag
        v["sofort"]["units"] = 1.0 / price; v["sofort"]["cash"] = 0.0
    if d[:7] not in st["months"] and st["n_raten"] < N:   # erster Kurstag jedes Monats ab Start: eine Rate
        st["months"].append(d[:7]); st["n_raten"] += 1; amt = 1.0 / N
        v["raten"]["units"] += amt / price; v["raten"]["cash"] -= amt
    if st["bought_warten"] is None and price / ath_at[d] - 1 <= THRESH:
        v["warten"]["units"] = v["warten"]["cash"] / price; v["warten"]["cash"] = 0.0; st["bought_warten"] = d
    val = {k: x["units"] * price + x["cash"] for k, x in v.items()}
    st["rows"].append(dict(date=d, **{k: round(x, 4) for k, x in val.items()}, dd=round(price / ath_at[d] - 1, 4)))
    st["last_date"] = d
json.dump(st, open("data/einmal.json", "w"), indent=1)
last = st["rows"][-1] if st["rows"] else None
pub = dict(start=st["start"], currency=cur, date=st["last_date"], thresh=THRESH, n_raten=st["n_raten"], bought_warten=st["bought_warten"],
           dd_ath=last["dd"] if last else None, values={k: last[k] for k in ("sofort", "raten", "warten")} if last else None, rows=st["rows"])
json.dump(pub, open("site/einmal.json", "w"), indent=1)
print(f"Einmalanlage {st['last_date']}: " + (", ".join(f"{k} {last[k]:.4f}" for k in ("sofort", "raten", "warten")) + f"; Raten {st['n_raten']}/{N}; Warten gekauft: {st['bought_warten']}" if last else "keine Daten"))
