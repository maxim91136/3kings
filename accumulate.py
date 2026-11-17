"""Familie 'Halten + Nachkaufen' (nur aufstocken, nie verkaufen), getestet ueber VIELE Starttage.
  python3 accumulate.py [--data data/prices.csv] [--horizon 756] [--step 21]

Jeder Anleger hat am Start 1,0 Kapital. Alle Varianten bekommen dasselbe Kapital und dieselbe Frist;
was bis zum Ende nicht investiert wurde, bleibt Cash (null Zins) - dieser Nachteil wird mitgemessen.
  A  Einmalanlage:   alles am Start, dann halten (= reines Halten)
  B  Dip-Nachkauf:   70 % am Start; je 10 % nachkaufen bei -10 / -20 / -30 % unter dem 252-Tage-Hoch
                     (jede Stufe einmal je Rueckgang; Reset, wenn der Kurs wieder >= 95 % des Hochs ist)
  C  Sparplan:       1/12 pro Monat (21 Tage) ueber 12 Monate
  D  Kombination:    20 % am Start + 50 % Sparplan ueber 12 Monate + 30 % Dip-Reserve wie bei B
Parameter vorab festgelegt, nicht optimiert. Kosten: BTC 10 bps, ETFs 5 bps je Kauf.
Beachte: Ueberlappende Startfenster sind NICHT unabhaengig - die Zahl der Starts taeuscht Sicherheit vor.
"""
import argparse, sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "core"))
import lab

TIERS, TIER_SIZE, MONTH = (-0.10, -0.20, -0.30), 0.10, 21


def simulate(p, s, H, variant, cost):
    cash, sh = 1.0, 0.0
    used = [False] * 3
    n_buys, eq = 0, np.zeros(H + 1)
    invested = np.zeros(H + 1)

    def buy(x, price):
        nonlocal cash, sh, n_buys
        x = min(x, cash)
        if x > 1e-12:
            sh += x * (1 - cost) / price
            cash -= x
            n_buys += 1

    init = {"A": 1.0, "B": 0.7, "C": 0.0, "D": 0.2}[variant]
    dca_total = {"A": 0.0, "B": 0.0, "C": 1.0, "D": 0.5}[variant]
    dip = variant in ("B", "D")
    buy(init, p[s])
    for k in range(H + 1):
        t = s + k
        if dca_total and k > 0 and k % MONTH == 0 and k // MONTH <= 12:
            buy(dca_total / 12, p[t])
        if dip and k > 0:
            hi = p[max(0, t - 252): t + 1].max()
            dd = p[t] / hi - 1
            if p[t] >= 0.95 * hi:
                used = [False] * 3
            else:
                for j, th in enumerate(TIERS):
                    if dd <= th and not used[j]:
                        buy(TIER_SIZE, p[t])
                        used[j] = True
        eq[k] = cash + sh * p[t]
        invested[k] = sh * p[t] / eq[k]
    peak = np.maximum.accumulate(eq)
    return eq[-1], float(((peak - eq) / peak).max()), float(invested.mean()), n_buys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/prices.csv")
    ap.add_argument("--horizon", type=int, default=756)
    ap.add_argument("--step", type=int, default=21)
    a = ap.parse_args()
    dates, names, P = lab.load_prices(a.data)
    names_v = {"A": "Einmalanlage (Halten)", "B": "Dip-Nachkauf", "C": "Sparplan 12 Mon.", "D": "Kombination"}
    print(f"{len(dates)} Tage ({dates[0]} .. {dates[-1]}); Frist {a.horizon} Tage; Start alle {a.step} Tage\n")
    for i, nm in enumerate(names):
        p, cost = P[:, i], (0.0010 if nm == "BTC" else 0.0005)
        starts = list(range(0, len(p) - a.horizon - 1, a.step))
        res = {v: np.array([simulate(p, s, a.horizon, v, cost) for s in starts]) for v in "ABCD"}
        print(f"== {nm}: {len(starts)} Startpunkte (ueberlappend), erster {dates[starts[0]]}, letzter {dates[starts[-1]]}")
        print(f"{'Variante':24s}{'Endwert med.':>13s}{'besser als A':>14s}{'schlechtester':>15s}{'Rueckg. med.':>14s}{'investiert':>12s}{'Kaeufe':>8s}")
        for v in "ABCD":
            r, A = res[v], res["A"]
            ratio = r[:, 0] / A[:, 0]
            print(f"{names_v[v]:24s}{np.median(r[:,0]):13.2f}{(ratio > 1).mean()*100:13.0f}%{r[:,0].min():15.2f}"
                  f"{np.median(r[:,1])*100:13.0f}%{np.median(r[:,2])*100:11.0f}%{np.median(r[:,3]):8.1f}")
        print()


if __name__ == "__main__":
    main()
