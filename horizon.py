"""Zeithorizonte: kleine, vorab festgelegte Auswahl; ALLE Ergebnisse werden gezeigt (kein Herauspicken).
  python3 horizon.py [--data data/prices.csv]
Teil 1: Trend-Linie (einfacher Schnitt) 50/100/150/200/300 Tage je Spieler, gleiches Fenster wie das Labor.
Teil 2: Mannschaft mit Rueckblick fuer die Championwahl (252/504/756 Tage) x Saisonlaenge (21/63/126 Tage).
Beurteilen nach dem PLATEAU (liegen Nachbarwerte aehnlich?), nicht nach dem Spitzenwert."""
import argparse, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "core"))
import lab, team

ap = argparse.ArgumentParser(); ap.add_argument("--data", default="data/prices.csv"); a = ap.parse_args()
dates, names, P = lab.load_prices(a.data)
R = lab.returns(P)
print(f"{len(dates)} Tage ({dates[0]} .. {dates[-1]}), Auswertung ab {dates[lab.WARM]}\n")
print("TEIL 1: Trend-Linie (Schnitt der letzten N Tage), Kauf wenn Kurs darueber, sonst Cash")
for i, nm in enumerate(names):
    cost = 0.0010 if nm == "BTC" else 0.0005
    print(f"== {nm}")
    print(f"{'Linie':14s}{'Rendite/J':>10s}{'Sharpe':>8s}{'Rueckgang':>11s}{'investiert':>11s}{'Wechsel/J':>10s}")
    rows = [("Halten", np.ones(len(P)))]
    for n in (50, 100, 150, 200, 300):
        m = lab.sma(P[:, i], n)
        rows.append((f"SMA {n}", np.where(np.isfinite(m) & (P[:, i] > m), 1.0, 0.0)))
    for lbl, w in rows:
        net = lab.backtest(w, R[:, i], cost)[lab.WARM:]
        ww = w[lab.WARM:]
        m = lab.metrics(net, ww)
        flips = np.abs(np.diff(ww)).sum() / (len(ww) / lab.ANN)
        print(f"{lbl:14s}{m['cagr']*100:9.1f}%{m['sharpe']:8.2f}{m['mdd']*100:10.0f}%{m['invested']*100:10.0f}%{flips:10.1f}")
    print()
print("TEIL 2: Mannschaft (BTC, SPY, GLD): Rueckblick x Saisonlaenge  ->  Sharpe / Rendite pro Jahr / Rueckgang")
base = None
print(f"{'':>12s}" + "".join(f"{'Saison '+str(s):>24s}" for s in (21, 63, 126)))
for look in (252, 504, 756):
    line = f"Rueckblick {look:3d}"
    for sea in (21, 63, 126):
        team.LOOK, team.SEASON = look, sea
        r = team.run_team(P, names, ["BTC", "SPY", "GLD"])["team"]
        m = lab.metrics(*r)
        line += f"{m['sharpe']:8.2f} /{m['cagr']*100:5.1f}% /{m['mdd']*100:4.0f}% "
    print(line)
