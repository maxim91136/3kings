"""Test: Trend SMA100 als zusaetzlicher Kandidat im Turnier (nur Bitcoin / alle Spieler). Aendert den Heartbeat nicht."""
import sys, os
import numpy as np
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "core"))
import lab, team
dates, names, P = lab.load_prices("data/prices.csv")
pl = ["BTC", "SPY", "GLD"]; S = team.STRATS; X = "Trend SMA100 (Std.)"
fns = lab.build_strategies(names, 0.001)
print("Look-ahead SMA100:", "BESTANDEN" if not lab.causality_test({"x": fns[X]}, P) else "DURCHGEFALLEN")
runs = {"Halten-Team": None,
        "Mannschaft heute (3 Kandidaten)": None,
        "+ SMA100 nur fuer Bitcoin": {"BTC": S + [X]},
        "+ SMA100 fuer alle": {p: S + [X] for p in pl}}
base = team.run_team(P, names, pl)
for name in runs:
    if name == "Halten-Team": r, res = base["halten"], base
    elif name.startswith("Mannschaft heute"): r, res = base["team"], base
    else:
        res = team.run_team(P, names, pl, strats=runs[name]); r = res["team"]
    m = lab.metrics(*r)
    print(f"{name:34s} Rendite {m['cagr']*100:5.1f}%  Sharpe {m['sharpe']:4.2f}  Rueckgang {m['mdd']*100:3.0f}%  schl.Tag {m['worst']*100:5.1f}%")
    if "SMA100" in name:
        for p in pl:
            c = Counter(res["history"][p]); n = len(res["history"][p])
            print("    ", p, ", ".join(f"{k.split(' (')[0]} {v/n*100:.0f}%" for k, v in c.most_common()), "| aktuell:", res["history"][p][-1].split(" (")[0])
d, p_, ci = lab.sharpe_diff_bootstrap(team.run_team(P, names, pl, strats={"BTC": S + [X]})["team"][0], base["team"][0])
print(f"Sharpe-Differenz (+SMA100 Bitcoin) minus heute: {d:+.2f}  (p = {p_:.2f}, 90%-Intervall {ci[0]:+.2f} .. {ci[1]:+.2f})")
