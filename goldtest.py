"""Langzeittest Gold (Kriterium vorab in REGELN.md). Aendert nichts. python3 goldtest.py"""
import csv, numpy as np
r = list(csv.DictReader(open("data/gold_long.csv"))); M = [x["month"] for x in r]; p = np.array([float(x["GOLD"]) for x in r])
ret = np.r_[0, p[1:] / p[:-1] - 1]
sma = np.array([p[max(0, i - 9): i + 1].mean() if i >= 9 else np.nan for i in range(len(p))])
w = {"Halten": np.ones(len(p)), "Trend 10 Mon.": np.where(p > sma, 1.0, 0.0)}
def stats(k, a, b):
    ww = w[k]; net = np.zeros(b - a)
    for j, t in enumerate(range(a, b)):
        if j: net[j] = ww[t - 1] * ret[t] - 0.0005 * abs(ww[t - 1] - ww[t - 2])
    eq = np.cumprod(1 + net); mdd = ((np.maximum.accumulate(eq) - eq) / np.maximum.accumulate(eq)).max()
    cagr = eq[-1] ** (12 / len(net)) - 1; sh = net.mean() / net.std() * 12 ** .5
    return cagr, mdd, sh
eras = [("1971-1980", "1971-08", "1980-12"), ("1981-2000", "1981-01", "2000-12"), ("2001-2011", "2001-01", "2011-12"), ("2012-2026", "2012-01", "2026-12"), ("ALLES", "1971-08", "2026-12")]
print(f"Gold {M[0]}..{M[-1]}\n{'Epoche':10s}{'Halten: Rend, Rueckg, Sharpe':>34s}{'Trend 10 Mon.: Rend, Rueckg, Sharpe':>40s}")
R = {}
for n, lo, hi in eras:
    a = M.index(lo); b = max(i for i, m in enumerate(M) if m <= hi) + 1
    line = f"{n:10s}"
    for k in w:
        c, m, s = stats(k, a, b); R[k, n] = (c, m); line += f"{c*100:16.1f}%{m*100:8.0f}%{s:8.2f}"
    print(line)
ok = R["Trend 10 Mon.", "ALLES"][1] < R["Halten", "ALLES"][1] and R["Trend 10 Mon.", "1981-2000"][1] < R["Halten", "1981-2000"][1] and R["Trend 10 Mon.", "ALLES"][0] >= R["Halten", "ALLES"][0] - 0.02
print("Kriterium Trend fuer Gold:", "ERFUELLT" if ok else "nicht erfuellt")
