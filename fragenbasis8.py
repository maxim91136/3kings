"""Gemeinsamer Kopf (Daten und Hilfsfunktionen) für die Fragen-Skripte; früher per exec aus fragen8.py geladen."""
import csv, datetime as dt, numpy as np
LAST = "2026-10"
def daily(path, col=1):
    out = []
    for r in list(csv.reader(open(path)))[1:]:
        if r[col]: out.append((dt.date.fromisoformat(r[0]), float(r[col])))
    return sorted(out)
spx = daily("data/spx_long.csv"); btcd = daily("data/btc_long.csv")
def month_end(d):
    o = {}
    for day, v in d: o[day.strftime("%Y-%m")] = v
    return o
sp_m = month_end(spx); bt_m = month_end([x for x in btcd if x[0] >= dt.date(2014, 9, 1)])
gold = {}
for r in list(csv.reader(open("data/gold_long.csv")))[1:]:
    if r[1] and r[0] >= "1971-08": gold[r[0][:7]] = float(r[1])
def mrets(s, a, b):
    ms = [m for m in sorted(s) if a <= m <= b]; return {ms[i]: s[ms[i]] / s[ms[i - 1]] - 1 for i in range(1, len(ms))}
A = {"S&P 500": mrets(sp_m, "1927-12", LAST), "Gold": mrets(gold, "1971-08", LAST), "Bitcoin": mrets(bt_m, "2014-09", LAST)}
def year_matrix(r):
    ys = sorted({int(m[:4]) for m in r}); rows, yy = [], []
    for y in ys:
        row = [r.get("%d-%02d" % (y, k)) for k in range(1, 13)]
        if all(v is not None for v in row): rows.append(row); yy.append(y)
    return np.array(rows), yy
def qual(M):
    n = len(M); h = n // 2; hit = (M > 0).mean(0); m1 = M[:h].mean(0); m2 = M[h:].mean(0)
    return ((hit >= .7) & (m1 > 0) & (m2 > 0)) | ((hit <= .3) & (m1 < 0) & (m2 < 0)), hit, M.mean(0), m1, m2
