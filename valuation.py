"""Studie Bewertung + Angst (Kriterien vorab in REGELN.md). Aendert den Heartbeat NICHT. python3 valuation.py"""
import csv, numpy as np
from bisect import bisect_right
r = list(csv.DictReader(open("data/spx_long.csv"))); D = [x["date"] for x in r]; p = np.array([float(x["SPX"]) for x in r]); T = len(p)
dd = p / np.maximum.accumulate(p) - 1
cape = {x["date"]: float(x["value"]) for x in csv.DictReader(open("data/ind_CAPE.csv"))}; ck = sorted(cape)
vix = {x["date"]: float(x["value"]) for x in csv.DictReader(open("data/ind_VIXCLS.csv"))}; vk = sorted(vix)
# kausales Perzentil: Wert des letzten bekannten Monats im Vergleich zu allen Monaten davor
cp = {}; hist = []
for k in ck:
    v = cape[k]; s = sorted(hist); cp[k] = bisect_right(s, v) / len(s) if s else 0.5; hist.append(v)
def last(keys, m, d):
    i = bisect_right(keys, d) - 1; return m[keys[i]] if i >= 0 else None
expensive = np.array([(last(ck, cp, d) or 0) >= 0.8 for d in D])
V = np.array([last(vk, vix, d) if d >= vk[0] else np.nan for d in D])

def go(rule, t, wait):
    near = dd[t] > -0.03
    if rule == "N": return not near
    if rule in ("B1", "B3", "A2"):
        ok = (dd[t] <= -0.10) if expensive[t] else not near
        if rule == "B3" and wait >= 252: ok = True
        if rule == "A2" and V[t] >= 30: ok = True
        return ok
    if rule == "B2": return (dd[t] <= -0.20) if expensive[t] else not near
    if rule == "A1": return (not near) or V[t] >= 30
    return True

def sim(a, b, rule):
    u = cash = paid = 0.0; wait = 0; maxw = 0; waiting = 0
    for k, t in enumerate(range(a, b)):
        if k % 21 == 0: cash += 1; paid += 1
        if cash > 0 and go(rule, t, wait): u += cash * 0.9995 / p[t]; cash = 0; wait = 0
        elif cash > 0: wait += 1; waiting += 1; maxw = max(maxw, wait)
    return (u * p[b - 1] + cash) / paid, maxw / 252, waiting / (b - a)

def table(rules, start, years):
    L = years * 252; st = range(next(i for i, d in enumerate(D) if d >= start), T - L, 63)
    R = {k: np.array([sim(s, s + L, k) for s in st]) for k in rules}; n = R["N"][:, 0]
    print(f"\n{years}-Jahres-Fenster ab {start[:4]} ({len(st)} Starts)\n{'Regel':6s}{'Median':>8s}{'schl. 10%':>10s}{'besser als N':>14s}{'Zeit am Warten':>16s}{'laengste Wartezeit':>20s}   Kriterium")
    for k, x in R.items():
        m, w10, mn = np.median(x[:, 0]), np.percentile(x[:, 0], 10), np.median(n)
        ok = "" if k == "N" else ("ERFUELLT" if (m >= mn * 0.99 and w10 > np.percentile(n, 10)) or m >= mn * 1.02 else "nicht erfuellt")
        print(f"{k:6s}{m:8.2f}{w10:10.2f}{(x[:,0]>n+1e-9).mean()*100:13.0f}%{np.mean(x[:,2])*100:15.0f}%{x[:,1].max():17.1f} J.   {ok}")
print("Anteil Tage 'KGV im obersten Fuenftel seiner Geschichte':", f"{expensive[D.index(next(d for d in D if d>='1930-01-02')):].mean()*100:.0f} %", "| seit 1995:", f"{expensive[next(i for i,d in enumerate(D) if d>='1995-01-01'):].mean()*100:.0f} %")
table(["N", "B1", "B2", "B3"], "1930-01-01", 20)
table(["N", "B1", "A1", "A2"], "1990-01-01", 10)
