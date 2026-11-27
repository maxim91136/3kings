"""Satelliten-Aufteilung: Sicherheits-Test mit jährlichem, halbjährlichem und vierteljährlichem Standard-Rhythmus plus Diversifikation
(REGELN 2026-11-22, Regeln vorab). Ergänzt site/fragen.json um den Schlüssel rhythmus."""
import json
from fragenbasis import btc
from fragenbasis import cagr_mdd
from fragenbasis import g
from fragenbasis import tr
from fragenbasis2 import last, rets
from fragenbasis import fxm, mix
RH = {"nie": 0, "jährlich": 12, "halbjährlich": 6, "vierteljährlich": 3, "monatlich": 1}
def rule(c, d, bc, bd): return c / d > bc / bd and d <= bd + .05
def mixd(series, w, a, b, k): return cagr_mdd(mix(series, w, a, b, k))
def win(series_fn, keys, a, b, L, k):
    ms = [m for m in sorted(tr) if a <= m <= b and m in g]; res = {x: [0, 0] for x in keys}
    for i in range(len(ms) - L):
        s0, e0 = ms[i], ms[i + L]; bc, bd = mixd(*series_fn(keys[0]), s0, e0, k)
        for x in keys[1:]: c, d = mixd(*series_fn(x), s0, e0, k); res[x][1] += 1; res[x][0] += rule(c, d, bc, bd)
    return {x: v[0] / v[1] for x, v in res.items() if x != keys[0]}, len(ms) - L
gs = list(range(0, 101, 5)); tri = [(a, b) for a in range(0, 51, 5) for b in range(0, 51 - a, 5)]
gfn = lambda x: ([tr, g], [1 - x / 100, x / 100]); tfn = lambda t: ([tr, g, btc], [1 - (t[0] + t[1]) / 100, t[0] / 100, t[1] / 100])
eur = lambda s: {m: s[m] / fxm[m] for m in s if m in fxm}; tr_e, g_e = eur(tr), eur(g)
def vol(v): r = [v[i] / v[i - 1] - 1 for i in range(1, len(v))]; mu = sum(r) / len(r); return (sum((x - mu) ** 2 for x in r) / (len(r) - 1)) ** .5 * 12 ** .5
ms14 = [m for m in sorted(set(tr) & set(g) & set(btc)) if "2014-09" <= m <= last]
def avol(s): return vol([s[m] for m in ms14])
sv = (avol(tr), avol(g), avol(btc))
# Korrelationen (f)
def corr(s, a):
    ra, rb = rets(s, a, last), rets(tr, a, last); m = sorted(set(ra) & set(rb)); x = [rb[i] for i in m]; y = [ra[i] for i in m]
    mx, my = sum(x) / len(x), sum(y) / len(y); cv = sum((p - mx) * (q - my) for p, q in zip(x, y, strict=False)); return cv / (sum((p - mx) ** 2 for p in x) * sum((q - my) ** 2 for q in y)) ** .5
cf = dict(gold71=corr(g, "1971-08"), gold14=corr(g, "2014-09"), btc=corr(btc, "2014-09")); f_ok = all(v < .5 for v in cf.values())
out = {}
for lab in ("jährlich", "halbjährlich", "vierteljährlich"):
    k = RH[lab]
    A = {}; base = mixd(*gfn(0), "1971-08", last, k)
    for x in gs: c, d = mixd(*gfn(x), "1971-08", last, k); A[x] = rule(c, d, *base) if x else False
    r1, n1 = win(gfn, gs, "1971-08", last, 120, k)
    eb = mixd([tr_e, g_e], [1, 0], "2003-12", last, k); E = {}
    for x in gs[1:]: c, d = mixd([tr_e, g_e], [1 - x / 100, x / 100], "2003-12", last, k); E[x] = rule(c, d, *eb)
    r3, n3 = win(tfn, [(0, 0)] + [t for t in tri if t != (0, 0)], "2014-09", last, 60, k)
    bB = mixd(*tfn((0, 0)), "2014-09", last, k); cand = []
    for t in tri:
        if t == (0, 0): continue
        c, d = mixd(*tfn(t), "2014-09", last, k)
        if not rule(c, d, *bB): continue
        sp, go, bt = 100 - t[0] - t[1], t[0], t[1]
        a_ = True; b_ = (A[go] if go else True); c_ = r3[t] >= .75 and (r1[go] >= .75 if go else True); d_ = (E[go] if go else True)
        cs = {x: mixd(*tfn(t), "2014-09", last, kk) for x, kk in RH.items()}; me = cs[lab]
        e_ = not any(v[0] >= me[0] + .002 and v[1] <= me[1] + .01 for x, v in cs.items() if x != lab)
        vv = mix([tr, g, btc], [sp / 100, go / 100, bt / 100], "2014-09", last, k); pv = vol(vv); dr = (sp / 100 * sv[0] + go / 100 * sv[1] + bt / 100 * sv[2]) / pv
        cand.append(dict(sp=sp, gold=go, btc=bt, cagr=round(c, 4), mdd=round(d, 3), ratio=round(c / d, 3), r3=round(r3[t], 3), r1=round(r1[go], 3) if go else None, vol=round(pv, 3), divq=round(dr, 2),
                         a=a_, b=b_, c=c_, d=d_, e=e_, f=f_ok, alle=a_ and b_ and c_ and d_ and e_ and f_ok))
    ok = sorted([r for r in cand if r["alle"]], key=lambda r: -r["ratio"])
    out[lab] = dict(n_cand=len(cand), n_alle=len(ok), best=ok[:10], best_btc=next((r for r in ok if r["btc"] >= 5), None), n_btc=sum(r["btc"] >= 5 for r in ok), n1=n1, n3=n3,
                    cand=sorted(cand, key=lambda r: -r["ratio"])[:14], A_ok=[x for x in gs if A.get(x)], E_ok=[x for x in E if E[x]])
R = json.load(open("site/fragen.json")); R["rhythmus"] = dict(corr={k: round(v, 2) for k, v in cf.items()}, f_ok=f_ok, vol=dict(sp=round(sv[0], 3), gold=round(sv[1], 3), btc=round(sv[2], 3)), per=out)
json.dump(R, open("site/fragen.json", "w"), ensure_ascii=False, indent=1)
print("Korrelationen", cf, "f ok", f_ok, "Vol", sv)
for lab, o in out.items():
    print("==", lab, "Kandidaten", o["n_cand"], "alle Bedingungen", o["n_alle"], "davon mit >=5% Bitcoin", o["n_btc"], "Gold-Test ok:", o["A_ok"][:3], "..", o["A_ok"][-1])
    for r in o["best"][:6]: print("  ", r["sp"], r["gold"], r["btc"], "Rendite", r["cagr"], "Rück", r["mdd"], "Verh", r["ratio"], "r1", r["r1"], "r3", r["r3"], "Vol", r["vol"], "DQ", r["divq"])
    print("  beste mit Bitcoin:", {k: o["best_btc"][k] for k in ("sp", "gold", "btc", "cagr", "mdd", "ratio", "divq")} if o["best_btc"] else None)
