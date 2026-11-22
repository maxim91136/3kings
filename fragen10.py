"""Saisonalität Bitcoin (REGELN 2026-11-22, Regeln vorab). Ergänzt fragen.json["saison_btc"]."""
import json, numpy as np
exec(open("fragen9.py").read().split("S = {")[0])
B = yearly(A["Bitcoin"], 2015, 2025); ys = sorted(B); h = len(ys) // 2
t = [(y, w, s_) for y, w, s_ in winter_summer(A["Bitcoin"], 2015) if y <= 2025]
d = np.array([w - s_ for _, w, s_ in t]); n = len(t); hh = n // 2
sim = dict(n=n, winter=round(float(np.mean([w for _, w, _ in t])), 4), summer=round(float(np.mean([s_ for _, _, s_ in t])), 4), diff=round(float(np.mean(d)), 4), median_diff=round(float(np.median(d)), 4), share=round(float((d > 0).mean()), 3),
           d1=round(float(d[:hh].mean()), 4), d2=round(float(d[hh:].mean()), 4), pattern=bool(d.mean() >= .02 and (d > 0).mean() >= .6 and d[:hh].mean() > 0 and d[hh:].mean() > 0))
def stats(vals):
    v = np.array(vals); up = v[v > 0]; dn = v[v < 0]
    return dict(n=len(v), hit=round(float((v > 0).mean()), 3), mean=round(float(v.mean()), 4), median=round(float(np.median(v)), 4), sd=round(float(v.std(ddof=1)), 4), max_gain=round(float(v.max()), 4), max_loss=round(float(v.min()), 4), last5=round(float(v[-5:].mean()), 4))
kz = [dict(fenster="Nov–Apr", **stats([w for _, w, _ in t])), dict(fenster="Mai–Okt", **stats([s_ for _, _, s_ in t]))]
res = {(st, L): {y: win_ret(B, y, st, L) for y in ys} for L in (1, 2, 3) for st in range(1, 13)}
def stat(yy, k): v = np.array([res[k][y] for y in yy if res[k][y] is not None]); return float((v > 0).mean()), float(v.mean())
fen = []
for lab, a_, b_ in (("erste → zweite Hälfte", ys[:h], ys[h:]), ("zweite → erste Hälfte", ys[h:], ys[:h])):
    c = [(stat(a_, k), k) for k in res if stat(a_, k)[1] > 0]; (ha, ma), key = max(c, key=lambda x: (x[0][0], x[0][1]))
    hb, mb = stat(b_, key); L = key[1]; allm = float(np.mean([stat(b_, k)[1] for k in res if k[1] == L]))
    fen.append(dict(richtung=lab, start=key[0], L=L, hit_a=round(ha, 3), mean_a=round(ma, 4), hit_b=round(hb, 3), mean_b=round(mb, 4), mean_all=round(allm, 4), haelt=bool(hb >= .6 and mb > allm)))
M = np.array([B[y] for y in ys]); cum = np.cumprod(1 + M, axis=1) - 1; med = [0.0] + [round(float(x), 4) for x in np.median(cum, axis=0)]
R = dict(years=[ys[0], ys[-1]], halves=[ys[0], ys[h - 1], ys[h], ys[-1]], sell_in_may=sim, kennzahlen=kz, fenster=fen, chart_median=med)
J = json.load(open("site/fragen.json")); J["saison_btc"] = R; json.dump(J, open("site/fragen.json", "w"), ensure_ascii=False, indent=1)
print(R["halves"], sim); [print(x) for x in kz]; [print(x) for x in fen]; print(med)
