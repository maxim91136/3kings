"""Power-Law als 'guenstig'-Signal fuer Bitcoin - ehrlich getestet (KAUSAL).
Die Linie wird fuer jeden Tag NUR mit den Daten bis zu diesem Tag angepasst (log10 Preis gegen log10 Tage seit
Genesis, 3.1.2009). Abstand z = Abweichung vom Fit in Standardabweichungen der bisherigen Abweichungen.
Zwei vorab festgelegte Varianten (keine Optimierung):
  PL-binaer: investiert, wenn der Kurs unter der Linie liegt (z <= 0), sonst Cash
  PL-Rampe : Anteil = 0,5 - 0,5*z, begrenzt auf 0..1 (z=-1 -> 100 %, z=0 -> 50 %, z=+1 -> 0 %)
Beachte: Nur gut ein Zyklus an Daten (ab 2015); die Anpassung ist am Anfang instabil."""
import os, sys
from datetime import date
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "core"))
import lab

def pl_z(dates, price, min_n=252):
    x = np.log10(np.array([(date.fromisoformat(d) - date(2009, 1, 3)).days for d in dates], float))
    y = np.log10(price)
    n = np.arange(1, len(y) + 1)
    sx, sy, sxx, sxy, syy = (np.cumsum(v) for v in (x, y, x * x, x * y, y * y))
    b = (n * sxy - sx * sy) / (n * sxx - sx ** 2)
    a = (sy - b * sx) / n
    sse = syy - 2 * a * sy - 2 * b * sxy + n * a ** 2 + 2 * a * b * sx + b ** 2 * sxx
    sd = np.sqrt(np.maximum(sse, 0) / n)
    z = (y - (a + b * x)) / np.maximum(sd, 1e-9)
    z[:min_n] = np.nan
    return z

if __name__ == "__main__":
    dates, names, P = lab.load_prices("data/prices.csv")
    i = names.index("BTC"); p = P[:, i]; R = lab.returns(P)[:, i]
    z = pl_z(dates, p)
    LONG = "data/btc_long.csv"                       # wenn vorhanden: Anpassung mit der LANGEN Historie (ab 2010), weiter kausal
    if os.path.exists(LONG):
        import csv
        rows = list(csv.reader(open(LONG)))[1:]
        ld, lp = [r[0] for r in rows], np.array([float(r[1]) for r in rows])
        zl = dict(zip(ld, pl_z(ld, lp, min_n=500)))
        z = np.array([zl.get(d, np.nan) for d in dates])
        print(f"Lange Historie genutzt: {ld[0]} .. {ld[-1]} ({len(ld)} Tage)")
    W = {"Halten": np.ones(len(p)),
         "Trend SMA100": np.where(np.isfinite(lab.sma(p, 100)) & (p > lab.sma(p, 100)), 1.0, 0.0),
         "Trend SMA200": np.where(np.isfinite(lab.sma(p, 200)) & (p > lab.sma(p, 200)), 1.0, 0.0),
         "PL-binaer": np.where(np.isfinite(z) & (z <= 0), 1.0, 0.0),
         "PL-Rampe": np.where(np.isfinite(z), np.clip(0.5 - 0.5 * np.nan_to_num(z), 0, 1), 0.0)}
    cut = lab.WARM + (len(p) - lab.WARM) // 2
    print(f"Bitcoin {dates[0]} .. {dates[-1]}, Auswertung ab {dates[lab.WARM]}; heute z = {z[-1]:+.2f} (negativ = unter der Linie)\n")
    print(f"{'':14s}{'Rendite/J':>10s}{'Sharpe':>8s}{'Rueckgang':>11s}{'investiert':>11s}{'Sharpe 1.H':>11s}{'Sharpe 2.H':>11s}")
    sh = lambda x: x.mean() / x.std(ddof=1) * np.sqrt(252)
    for k, w in W.items():
        net = lab.backtest(w, R, 0.001)
        m = lab.metrics(net[lab.WARM:], w[lab.WARM:])
        print(f"{k:14s}{m['cagr']*100:9.1f}%{m['sharpe']:8.2f}{m['mdd']*100:10.0f}%{m['invested']*100:10.0f}%{sh(net[lab.WARM:cut]):11.2f}{sh(net[cut:]):11.2f}")
