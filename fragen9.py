"""Saisonalität nach Seasonax-Vorbild (REGELN 2026-11-22, Regeln vorab): Chart, Jahresbalken, Kennzahlen, Fenstertest mit Hälften. Ergänzt fragen.json["saison2"]."""
from fragenbasis9 import win_ret, winter_summer, yearly
import json
import numpy as np
from fragenbasis8 import A
S = {"S&P 500": yearly(A["S&P 500"], 1928, 2025), "Gold": yearly(A["Gold"], 1972, 2025)}
R = {}
# A Chart
def path(Y, ys): M = np.array([Y[y] for y in ys]); cum = np.cumprod(1 + M, axis=1) - 1; return [0.0] + [round(float(x), 4) for x in cum.mean(0)]
R["chart"] = {"S&P 500 alle": path(S["S&P 500"], sorted(S["S&P 500"])), "S&P 500 20 Jahre": path(S["S&P 500"], [y for y in S["S&P 500"] if y >= 2006]), "Gold": path(S["Gold"], sorted(S["Gold"]))}
# B Balken
dec = {y: float(S["S&P 500"][y][11]) for y in S["S&P 500"]}
ws = {y: (w - s) for y, w, s in winter_summer(A["S&P 500"], 1929) if y <= 2026}
R["balken"] = dict(dez=[[y, round(v, 4)] for y, v in sorted(dec.items())], ws=[[y, round(v, 4)] for y, v in sorted(ws.items())])
# C Kennzahlen
def stats(vals, ys):
    v = np.array(vals); up = v[v > 0]; dn = v[v < 0]
    return dict(n=len(v), hit=round(float((v > 0).mean()), 3), mean=round(float(v.mean()), 4), sd=round(float(v.std(ddof=1)), 4), avg_gain=round(float(up.mean()), 4) if len(up) else None, avg_loss=round(float(dn.mean()), 4) if len(dn) else None,
                max_gain=round(float(v.max()), 4), max_loss=round(float(v.min()), 4), last5=round(float(np.mean(v[-5:])), 4))
wl = lambda r, a_year: [(y, w, s) for y, w, s in winter_summer(r, a_year)]
sp_t = wl(A["S&P 500"], 1929); gd_t = wl(A["Gold"], 1972)
R["kennzahlen"] = [dict(name="S&P 500", fenster="Dezember", **stats([dec[y] for y in sorted(dec)], None)),
                   dict(name="S&P 500", fenster="Nov–Apr", **stats([w for _, w, _ in sp_t], None)), dict(name="S&P 500", fenster="Mai–Okt", **stats([s for _, _, s in sp_t], None)),
                   dict(name="Gold", fenster="Nov–Apr", **stats([w for _, w, _ in gd_t], None)), dict(name="Gold", fenster="Mai–Okt", **stats([s for _, _, s in gd_t], None))]
# D Fenstertest
def finder(Y, ys_a, ys_b):
    res = {}
    for L in (1, 2, 3):
        for st in range(1, 13):
            res[(st, L)] = {y: win_ret(Y, y, st, L) for y in sorted(Y)}
    def sel(ys, key): return [res[key][y] for y in ys if res[key][y] is not None]
    def stat(ys, key): v = np.array(sel(ys, key)); return float((v > 0).mean()), float(v.mean())
    out = []
    for lab, ys_a_, ys_b_ in (("erste → zweite Hälfte", ys_a, ys_b), ("zweite → erste Hälfte", ys_b, ys_a)):
        cands = [(stat(ys_a_, k), k) for k in res if stat(ys_a_, k)[1] > 0]
        (hit_a, mean_a), key = max(cands, key=lambda c: (c[0][0], c[0][1]))
        hit_b, mean_b = stat(ys_b_, key); L = key[1]; allm = float(np.mean([stat(ys_b_, k)[1] for k in res if k[1] == L]))
        out.append(dict(richtung=lab, start=key[0], L=L, hit_a=round(hit_a, 3), mean_a=round(mean_a, 4), hit_b=round(hit_b, 3), mean_b=round(mean_b, 4), mean_all=round(allm, 4), haelt=bool(hit_b >= .6 and mean_b > allm)))
    return out
sp_ys = sorted(S["S&P 500"]); gd_ys = sorted(S["Gold"]); h = len(sp_ys) // 2; hg = len(gd_ys) // 2
R["fenster"] = {"S&P 500": finder(S["S&P 500"], sp_ys[:h], sp_ys[h:]), "Gold": finder(S["Gold"], gd_ys[:hg], gd_ys[hg:])}
R["halbjahre"] = dict(sp=[sp_ys[0], sp_ys[h - 1], sp_ys[h], sp_ys[-1]], gold=[gd_ys[0], gd_ys[hg - 1], gd_ys[hg], gd_ys[-1]])
J = json.load(open("site/fragen.json")); J["saison2"] = R; json.dump(J, open("site/fragen.json", "w"), ensure_ascii=False, indent=1)
print(R["halbjahre"]); [print(k, x) for k, x in R["fenster"].items() for x in x]; [print(x) for x in R["kennzahlen"]]
print("Chart S&P all", R["chart"]["S&P 500 alle"]); print("Chart 20y", R["chart"]["S&P 500 20 Jahre"]); print("Gold", R["chart"]["Gold"])
