"""Kauf am Allzeithoch vs guenstig kaufen (S&P-Preisindex 1928-2026). Aendert den Heartbeat NICHT. python3 ath.py"""
import csv, numpy as np
r = list(csv.DictReader(open("data/spx_long.csv"))); D = [x["date"] for x in r]; p = np.array([float(x["SPX"]) for x in r]); T = len(p)
ath = np.maximum.accumulate(p); dd = p / ath - 1
print("Teil A: Was brachte ein Kauf, je nach Abstand zum Allzeithoch? (ab 1950, Preisindex ohne Dividenden)")
print(f"{'Abstand zum Hoch':18s}{'Anteil Tage':>12s}{'1 Jahr spaeter':>16s}{'im Minus':>10s}{'5 Jahre spaeter':>17s}{'im Minus':>10s}")
s0 = next(i for i, d in enumerate(D) if d >= "1950-01-01")
for lab, lo, hi in (("am Hoch (0-3 %)", -0.03, 0.01), ("3-10 % darunter", -0.10, -0.03), ("10-20 % darunter", -0.20, -0.10), ("ueber 20 % darunter", -1, -0.20)):
    i = np.array([t for t in range(s0, T) if lo < dd[t] <= hi])
    i1 = i[i < T - 252]; i5 = i[i < T - 1260]
    f1 = p[i1 + 252] / p[i1] - 1; f5 = (p[i5 + 1260] / p[i5]) ** 0.2 - 1
    print(f"{lab:18s}{len(i)/(T-s0)*100:11.0f}%{np.median(f1)*100:15.1f}%{(f1<0).mean()*100:9.0f}%{np.median(f5)*100:13.1f}%/J{(f5<0).mean()*100:9.0f}%")

def sim(a, b, rule):
    u = cash = paid = 0.0; wait = 0; under = []
    for k, t in enumerate(range(a, b)):
        if k % 21 == 0: cash += 1; paid += 1
        if rule == "sofort": go = True
        elif rule == "nicht am Hoch": go = dd[t] <= -0.03
        elif rule == "warte -10 %": go = dd[t] <= -0.10
        elif rule == "warte -10 %, max 12 Mon.": go = dd[t] <= -0.10 or wait >= 252
        if go and cash > 0: u += cash * 0.9995 / p[t]; cash = 0; wait = 0
        elif cash > 0: wait += 1
        under.append((u * p[t] + cash) / paid - 1)
    return (u * p[b - 1] + cash) / paid, min(under), cash / paid
print("\nTeil B: Monatlich 1 Einheit, Endwert/Eingezahlt (vor Steuern, Cash ohne Zins)")
for years in (10, 20):
    L = years * 252; st = range(next(i for i, d in enumerate(D) if d >= "1930-01-01"), T - L, 63)
    R = {k: np.array([sim(s, s + L, k) for s in st]) for k in ("sofort", "nicht am Hoch", "warte -10 %", "warte -10 %, max 12 Mon.")}
    print(f"\n{years} Jahre ({len(st)} Startpunkte)\n{'Regel':26s}{'Median':>8s}{'schl. 10%':>10s}{'besser als sofort':>19s}{'schl. Buchverlust':>19s}")
    for k, x in R.items():
        print(f"{k:26s}{np.median(x[:,0]):8.2f}{np.percentile(x[:,0],10):10.2f}{(x[:,0]>R['sofort'][:,0]+1e-9).mean()*100:18.0f}%{x[:,1].min()*100:18.0f}%")
