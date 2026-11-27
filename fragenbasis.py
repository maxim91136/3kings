"""Gemeinsamer Kopf (Daten und Hilfsfunktionen) für die Fragen-Skripte; früher per exec aus fragen.py geladen."""
import csv
def monthly(path, col, key=0):
    out = {}
    for r in list(csv.reader(open(path)))[1:]:
        if r[col]: out[r[key][:7]] = float(r[col])  # letzter Wert des Monats gewinnt
    return out
sh = list(csv.DictReader(open("data/shiller.csv")))
tr, cpi, lvl, prev = {}, {}, 1.0, None
for r in sh:
    p = float(r["SP500"] or 0); d = float(r["Dividend"] or 0)
    if p <= 0: continue
    if prev: lvl *= (p + d / 12) / prev
    tr[r["Date"][:7]] = lvl; cpi[r["Date"][:7]] = float(r["Consumer Price Index"]); prev = p
g = monthly("data/gold_long.csv", 1); btc = monthly("data/btc_long.csv", 1); fxm = monthly("data/ind_EURUSD.csv", 1)
def cagr_mdd(v):
    n = len(v) - 1; pk = dd = 0
    for x in v: pk = max(pk, x); dd = max(dd, 1 - x / pk)
    return v[-1] ** (12 / n) - 1, dd
def mix(series, w, start, end, k):  # k = Monate zwischen Rückgewichtungen, 0 = nie
    ms = [m for m in sorted(set.intersection(*[set(s) for s in series])) if start <= m <= end]
    a = list(w); v = [1.0]
    for i in range(1, len(ms)):
        a = [x * s[ms[i]] / s[ms[i - 1]] for x, s in zip(a, series, strict=False)]
        t = sum(a)
        if k and i % k == 0: a = [t * x for x in w]
        v.append(sum(a))
    return v
