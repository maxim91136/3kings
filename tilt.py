"""Test (aendert den Heartbeat NICHT): Bitcoin-Gewichtung und XLK (Tech) als Zusatz.
  python3 tilt.py"""
import csv, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "core"))
import lab, team
dates, names, P = lab.load_prices("data/prices.csv")
rows = list(csv.DictReader(open("data/candidates.csv")))
mp = {r["date"]: float(r["XLK"]) for r in rows if r["XLK"]}
x = np.array([mp.get(d, np.nan) for d in dates])
for j in range(len(x)):
    if not np.isfinite(x[j]): x[j] = x[j - 1]
P2 = np.column_stack([P, x]); nm = names + ["XLK"]
S = team.STRATS; STR = {"BTC": S + ["Trend SMA100 (Std.)"]}
def row(label, players, **kw):
    r = team.run_team(P2, nm, players, strats=STR, **kw)
    m = lab.metrics(*r["team"]); h = lab.metrics(*r["halten"])
    n = len(r["team"][0]); half = n // 2
    m1 = lab.metrics(r["team"][0][:half], r["team"][1][:half]); m2 = lab.metrics(r["team"][0][half:], r["team"][1][half:])
    a = r["alloc"][r["bounds"][-1]]
    print(f"{label:34s} {m['cagr']*100:5.1f}% {m['mdd']*100:5.0f}% {m['sharpe']:5.2f}   H1 {m1['cagr']*100:5.1f}%/{m1['mdd']*100:3.0f}%  H2 {m2['cagr']*100:5.1f}%/{m2['mdd']*100:3.0f}%   Halten-Team {h['cagr']*100:5.1f}%/{h['mdd']*100:3.0f}%   heute: " + " ".join(f"{p} {v*100:.0f}%" for p, v in zip(players, a, strict=False)))
print(f"Zeitraum {dates[lab.WARM]}..{dates[-1]}\n{'Variante':34s} {'Rend/J':>6s} {'Rueckg':>6s} {'Sharpe':>6s}")
B = ["BTC", "SPY", "GLD"]
for label, kw in (("A heute (inverse Vol.)", {}), ("B Bitcoin x2", {"tilt": {"BTC": 2}}), ("C Bitcoin x3", {"tilt": {"BTC": 3}}), ("D Bitcoin x5", {"tilt": {"BTC": 5}})):
    row(label, B, **kw)
print()
for label, kw in (("E +XLK vierter, ohne Deckel", {}), ("F +XLK Deckel 20 %", {"cap": {"XLK": .2}}), ("G +XLK Deckel 20 %, BTC x3", {"cap": {"XLK": .2}, "tilt": {"BTC": 3}})):
    row(label, B + ["XLK"], **kw)
row("H XLK statt SPY", ["BTC", "XLK", "GLD"])
row("I XLK statt SPY, BTC x3", ["BTC", "XLK", "GLD"], tilt={"BTC": 3})
