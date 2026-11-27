"""Experiment: Mannschaft mit 4. Strategie 'Dip-Aufbau' im Turnier (aendert den Heartbeat NICHT)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "core"))
import lab, team
from collections import Counter

dates, names, P = lab.load_prices("data/prices.csv")
print("Look-ahead-Test Dip-Aufbau:", "BESTANDEN" if not lab.causality_test({"d": lab.build_strategies(names, 0.001)["Dip-Aufbau (Std.)"]}, P) else "DURCHGEFALLEN")
base = team.run_team(P, names, ["BTC", "SPY", "GLD"])
team.STRATS = team.STRATS + ["Dip-Aufbau (Std.)"]
new = team.run_team(P, names, ["BTC", "SPY", "GLD"])
hold = base["halten"]
for tag, r in (("Halten-Team", hold), ("Mannschaft (3 Strategien)", base["team"]), ("Mannschaft (+ Dip-Aufbau)", new["team"])):
    m = lab.metrics(*r)
    print(f"{tag:28s} CAGR {m['cagr']*100:5.1f}%  Sharpe {m['sharpe']:4.2f}  MDD {m['mdd']*100:4.1f}%  schl.Tag {m['worst']*100:5.1f}%")
for pl in ("BTC", "SPY", "GLD"):
    c = Counter(new["history"][pl])
    print(pl, "Champions:", ", ".join(f"{s.split(' (')[0]} {n/len(new['history'][pl])*100:.0f}%" for s, n in c.most_common()), "| aktuell:", new["history"][pl][-1].split(" (")[0])
# Einzelwerte BTC: Dip-Aufbau allein gegen Halten und Trend (Sharpe ueber das Auswertungsfenster)
R = lab.returns(P); fns = lab.build_strategies(names, 0.001)
for s in ("Halten (Baseline)", "Trend SMA200 (Std.)", "Dip-Aufbau (Std.)"):
    w = fns[s](P, 0); net = lab.backtest(w, R[:, 0], 0.001)[lab.WARM:]
    m = lab.metrics(net, w[lab.WARM:])
    print(f"BTC allein {s:22s} CAGR {m['cagr']*100:5.1f}%  Sharpe {m['sharpe']:4.2f}  MDD {m['mdd']*100:4.1f}%")
