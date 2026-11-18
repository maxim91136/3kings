"""Langzeittest der S&P-500-Regel (aendert den Heartbeat NICHT). python3 longtest.py [--data data/spx_long.csv]
Preisindex ohne Dividenden und Cash ohne Zins: beides benachteiligt die Trendregel bzw. alle gleich (nur Vergleich Halten vs Regel).
Regeln wie im Heartbeat: Halten, Trend SMA200, Vol-Target 15 %. Kosten 5 bps je Umschichtung. Je Epoche getrennt ausgewertet."""
import argparse, csv, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "core"))
import lab
ap = argparse.ArgumentParser(); ap.add_argument("--data", default="data/spx_long.csv"); a = ap.parse_args()
rows = list(csv.DictReader(open(a.data)))
d = [r["date"] for r in rows]; P = np.array([[float(r["SPX"])] for r in rows])
R = lab.returns(P)[:, 0]
fns = lab.build_strategies(["SPX"], 0.0005)
S = {"Halten": "Halten (Baseline)", "Trend SMA200": "Trend SMA200 (Std.)", "Vol-Target 15%": "Vol-Target 15% (Std.)"}
W = {k: fns[v](P, 0) for k, v in S.items()}
N = {k: lab.backtest(W[k], R, 0.0005) for k in S}
eras = [("1930-1949", "1930-01-01", "1949-12-31"), ("1950-1972", "1950-01-01", "1972-12-31"), ("1973-1982", "1973-01-01", "1982-12-31"),
        ("1983-1999", "1983-01-01", "1999-12-31"), ("2000-2009", "2000-01-01", "2009-12-31"), ("2010-2026", "2010-01-01", "2026-12-31"), ("alles ab 1930", "1930-01-01", "2026-12-31")]
print(f"Daten {d[0]} .. {d[-1]} ({len(d)} Tage)\n")
print(f"{'Epoche':14s}" + "".join(f"{k:>30s}" for k in S) + f"{'Trend-Wechsel/J':>17s}")
print(f"{'':14s}" + "".join(f"{'Rend/J  Rueckg  Sharpe':>30s}" for _ in S))
for name, lo, hi in eras:
    idx = [i for i, x in enumerate(d) if lo <= x <= hi]
    if len(idx) < 300: continue
    s, e = idx[0], idx[-1] + 1
    line = f"{name:14s}"
    for k in S:
        m = lab.metrics(N[k][s:e], W[k][s:e])
        line += f"{m['cagr']*100:12.1f}%{m['mdd']*100:7.0f}%{m['sharpe']:8.2f}  "
    sw = np.abs(np.diff(W["Trend SMA200"][s:e])).sum() / (len(idx) / 252)
    print(line + f"{sw:12.1f}")
