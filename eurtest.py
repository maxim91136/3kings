"""Regel 'nicht am Hoch' aus Sicht eines Euro-Anlegers (2004-2026): Signal in Dollar oder in Euro? Aendert nichts. python3 eurtest.py"""
import csv, numpy as np
s = {r["date"]: float(r["SPX"]) for r in csv.DictReader(open("data/spx_long.csv"))}
fx = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
D = sorted(d for d in s if d in fx); usd = np.array([s[d] for d in D]); eur = usd / np.array([fx[d] for d in D])
# Allzeithoch in Dollar braucht die volle Historie davor
pre = max(v for d, v in s.items() if d < D[0]); ath_u = np.maximum.accumulate(np.maximum(usd, pre)); dd_u = usd / ath_u - 1
dd_e = eur / np.maximum.accumulate(eur) - 1
def sim(a, b, sig):
    u = cash = paid = 0.0
    for k, t in enumerate(range(a, b)):
        if k % 21 == 0: cash += 1; paid += 1
        if cash and (sig is None or sig[t] <= -0.03): u += cash / eur[t]; cash = 0
    return (u * eur[b - 1] + cash) / paid
L = 2520; st = range(252, len(D) - L, 21)
R = {k: np.array([sim(a, a + L, g) for a in st]) for k, g in (("sofort", None), ("Signal Dollar", dd_u), ("Signal Euro", dd_e))}
print(f"{D[0]}..{D[-1]}, {len(st)} Fenster a 10 Jahre, Werte in Euro (Preisindex ohne Dividenden)")
for k, x in R.items(): print(f"{k:14s} Median {np.median(x):.3f}  schl. 10% {np.percentile(x,10):.3f}  besser als sofort {(x>R['sofort']+1e-9).mean()*100:.0f} %")
print(f"Tage 'sammeln': Dollar {(dd_u>-0.03).mean()*100:.0f} %, Euro {(dd_e>-0.03).mean()*100:.0f} %, Signale verschieden an {((dd_u>-0.03)!=(dd_e>-0.03)).mean()*100:.0f} % der Tage")
