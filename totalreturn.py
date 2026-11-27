"""Gegencheck mit Total Return, Cash-Zins, Inflation, Start 1929 (Kriterien vorab in REGELN.md). Aendert nichts. python3 totalreturn.py"""
import csv, numpy as np
r = [x for x in csv.DictReader(open("data/shiller.csv")) if float(x["Dividend"]) > 0 and float(x["Consumer Price Index"]) > 0 and float(x["Long Interest Rate"]) > 0]
D = [x["Date"][:7] for x in r]; P = np.array([float(x["SP500"]) for x in r]); DIV = np.array([float(x["Dividend"]) for x in r])
CPI = np.array([float(x["Consumer Price Index"]) for x in r]); RATE = np.array([float(x["Long Interest Rate"]) for x in r]) / 100
n = len(P); tr = np.r_[0, (P[1:] + DIV[1:] / 12) / P[:-1] - 1]; infl = np.r_[0, CPI[1:] / CPI[:-1] - 1]
ath = np.maximum.accumulate(P); dd = P / ath - 1
COST = 0.0005

def dca(a, b, rule, cf, real):
    u = cash = paid = 0.0
    for k, t in enumerate(range(a, b)):
        cash *= 1 + cf * RATE[t] / 12
        u *= 1 + tr[t] if k else 1
        cash += 1; paid += 1
        if rule == "sofort" or dd[t] <= -0.03: u += cash * (1 - COST); cash = 0.0
    v = u + cash
    return (v / (CPI[b - 1] / CPI[a]) if real else v) / paid if not real else v / paid / (CPI[b - 1] / CPI[a]) * 1.0

def run_dca(L, cf, real, starts):
    out = {}
    for rule in ("sofort", "nicht am Hoch"):
        out[rule] = np.array([dca(s, s + L, rule, cf, real) for s in starts])
    return out

print(f"Shiller-Daten {D[0]} .. {D[-1]}")
for label, cf in (("Cash ohne Zins", 0.0), ("Cash mit 50 % des 10-J-Zinses", 0.5)):
    for years in (20, 10):
        L = years * 12; starts = [i for i in range(len(P) - L) if D[i] >= "1929-01" and D[i][5:7] in ("01", "07")]
        for real in (False, True):
            o = run_dca(L, cf, real, starts); s, nh = o["sofort"], o["nicht am Hoch"]
            ok = np.median(nh) >= 0.99 * np.median(s) and np.percentile(nh, 10) >= 0.99 * np.percentile(s, 10)
            print(f"{label:32s}{years:3d} J {'real   ' if real else 'nominal'} {len(starts)} Starts | sofort Median {np.median(s):.2f} schl.10% {np.percentile(s,10):.2f} | nicht am Hoch Median {np.median(nh):.2f} schl.10% {np.percentile(nh,10):.2f} | besser in {(nh>s+1e-9).mean()*100:.0f} % | {'HAELT' if ok else 'haelt nicht'}")
print("\nEinzelstarts (nominal, Total Return, Cash mit 50 % Zins): Endwert je eingezahltem Euro")
for lab_, d0 in (("Sept 1929", "1929-09"), ("Maerz 2000", "2000-03"), ("Jan 1973", "1973-01")):
    i = D.index(d0)
    for years in (20, 10):
        L = years * 12
        if i + L <= len(P):
            o = run_dca(L, 0.5, False, [i]); print(f"  Start {lab_}, {years} J: sofort {o['sofort'][0]:.2f} | nicht am Hoch {o['nicht am Hoch'][0]:.2f}")

print("\nFRAGE B: Trend 10 Monate vs Halten, Total Return, Cash 50 % des 10-J-Zinses (nominal)")
sma = np.array([P[max(0, i - 9): i + 1].mean() if i >= 9 else np.nan for i in range(n)])
w = np.where(P > sma, 1.0, 0.0); w[:10] = 1.0
def ser(kind):
    net = np.zeros(n)
    for t in range(1, n):
        wt = 1.0 if kind == "Halten" else w[t - 1]
        net[t] = wt * tr[t] + (1 - wt) * 0.5 * RATE[t] / 12 - (COST * abs(w[t - 1] - w[t - 2]) if kind != "Halten" and t > 1 else 0)
    return net
N = {k: ser(k) for k in ("Halten", "Trend")}
def st(k, a, b):
    x = N[k][a:b]; eq = np.cumprod(1 + x); mdd = ((np.maximum.accumulate(eq) - eq) / np.maximum.accumulate(eq)).max()
    return eq[-1] ** (12 / len(x)) - 1, mdd
eras = [("1930-1949", "1930-01", "1949-12"), ("1950-1972", "1950-01", "1972-12"), ("1973-1982", "1973-01", "1982-12"), ("1983-1999", "1983-01", "1999-12"), ("2000-2009", "2000-01", "2009-12"), ("2010-2023", "2010-01", "2023-06"), ("ALLES ab 1930", "1930-01", "2023-06")]
R = {}
for name, lo, hi in eras:
    a, b = D.index(lo), D.index(hi) + 1; line = f"{name:14s}"
    for k in N:
        c, m = st(k, a, b); R[k, name] = (c, m); line += f"  {k}: {c*100:5.1f} %/J, Rueckgang {m*100:3.0f} %"
    print(line)
ok = R["Trend", "1973-1982"][1] < R["Halten", "1973-1982"][1] and R["Trend", "2000-2009"][1] < R["Halten", "2000-2009"][1] and R["Trend", "ALLES ab 1930"][0] >= R["Halten", "ALLES ab 1930"][0] - 0.01
print("Kriterium B:", "TREND BLEIBT BELEGT" if ok else "nicht erfuellt")
