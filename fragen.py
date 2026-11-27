"""Die Fragen der Fragen (REGELN 2026-11-22, Regeln vorab): Beimischung, Euro gegen Dollar, Nachjustieren, Monatstag, Entnahme.
Nur lokale Daten (Shiller, gold_long, btc_long, spx_long, ind_EURUSD). Schreibt site/fragen.json."""
from fragenbasis import btc, cagr_mdd, cpi, fxm, g, mix, tr
import csv
import json
import statistics as st
R = {}
# F2 Beimischung
def blend(name, other, start, shares):
    rows = []
    for sh_ in shares:
        c, d = cagr_mdd(mix([tr, other], [1 - sh_, sh_], start, "9999", 12)); rows.append(dict(share=sh_, cagr=round(c, 4), mdd=round(d, 3), ratio=round(c / d, 3)))
    b = rows[0]
    for r in rows: r["ok"] = r["share"] > 0 and r["ratio"] > b["ratio"] and r["cagr"] >= b["cagr"] - 0.005
    return dict(name=name, start=start, rows=rows)
R["beimischung"] = [blend("Gold", g, "1971-08", [0, .05, .10, .20, .30]), blend("Bitcoin", btc, "2014-09", [0, .01, .02, .05, .10, .20])]
# F1 Euro/Dollar
def fxrow(name, s, start):
    ms = [m for m in sorted(set(s) & set(fxm)) if m >= start]
    usd = [s[m] / s[ms[0]] for m in ms]; eur = [s[m] / fxm[m] / (s[ms[0]] / fxm[ms[0]]) for m in ms]
    (cu, du), (ce, de) = cagr_mdd(usd), cagr_mdd(eur)
    return dict(name=name, start=ms[0], end=ms[-1], usd=round(cu, 4), eur=round(ce, 4), diff=round(ce - cu, 4), mdd_usd=round(du, 3), mdd_eur=round(de, 3), relevant=abs(ce - cu) >= .01)
R["euro"] = [fxrow("S&P 500", tr, "2003-12"), fxrow("Gold", g, "2003-12"), fxrow("Bitcoin", btc, "2014-09")]
# F3 Nachjustieren
IV = [("nie", 0), ("jährlich", 12), ("halbjährlich", 6), ("vierteljährlich", 3), ("monatlich", 1)]
re_ = []
for nm, k in IV:
    c, d = cagr_mdd(mix([tr, g], [.8, .2], "1971-08", "9999", k)); re_.append(dict(iv=nm, cagr=round(c, 4), mdd=round(d, 3)))
j = next(r for r in re_ if r["iv"] == "jährlich")
for r in re_: r["vs_jaehrlich"] = "Basis" if r is j else ("besser" if r["cagr"] >= j["cagr"] + .002 and r["mdd"] <= j["mdd"] + .01 else "schlechter" if r["cagr"] <= j["cagr"] - .002 and r["mdd"] >= j["mdd"] - .01 else "gleich")
R["nachjustieren"] = re_
# F5 Monatstag
px = list(csv.reader(open("data/spx_long.csv")))[1:]; dates = [r[0] for r in px]; p = [float(r[1]) for r in px]
by = {}
for i, d in enumerate(dates): by.setdefault(d[:7], []).append(i)
B = {"erster Handelstag": lambda L: L[0], "10. Handelstag": lambda L: L[9], "15. Handelstag": lambda L: L[14], "letzter Handelstag": lambda L: L[-1]}
res = {k: [] for k in B}; win = {k: 0 for k in B}; n = 0
for _m, L in sorted(by.items()):
    if len(L) < 15: continue
    row = {}
    for k, f in B.items():
        i = f(L)
        if i + 252 >= len(p): row = None; break
        row[k] = p[i + 252] / p[i] - 1
    if row:
        n += 1; [res[k].append(v) for k, v in row.items()]; win[max(row, key=row.get)] += 1
mt = [dict(bucket=k, mean=round(st.mean(v), 4), median=round(st.median(v), 4), best_share=round(win[k] / n, 3)) for k, v in res.items()]
sp = max(x["mean"] for x in mt) - min(x["mean"] for x in mt)
R["monatstag"] = dict(rows=mt, n=n, since=min(by), spread=round(sp, 4), relevant=sp >= .005)
# F6 Entnahme
ms = sorted(m for m in tr if cpi.get(m, 0) > 0); real = [tr[m] / cpi[m] for m in ms]; H = 360; ent = []
for w in (.03, .035, .04, .05, .06):
    fin = []
    for s in range(0, len(ms) - H):
        D = 100.0
        for t in range(s, s + H):
            D -= 100 * w / 12
            if D <= 0: D = 0; break
            D *= real[t + 1] / real[t]
        fin.append(D)
    ent.append(dict(rate=w, success=round(sum(x > 0 for x in fin) / len(fin), 3), median=round(st.median(fin), 1), worst=round(min(fin), 1), keep=round(sum(x >= 100 for x in fin) / len(fin), 3), n=len(fin), safe=sum(x > 0 for x in fin) / len(fin) >= .95))
R["entnahme"] = dict(rows=ent, since=ms[0], last_start=ms[len(ms) - H - 1])
json.dump(R, open("site/fragen.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
