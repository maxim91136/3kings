"""Satelliten-Aufteilung: Robustheit (REGELN 2026-11-22, Regeln vorab): R1 gleitende 10-Jahres-Fenster S&P/Gold seit 1971,
R2 Euro seit 2003, R3 gleitende 5-Jahres-Fenster 3 Anlagen (S&P >= 50 %) seit 2014, R4 Nachjustieren der Kandidaten; Sicherheits-Bedingungen a-e."""
import json
from fragenbasis import btc
from fragenbasis import cagr_mdd
from fragenbasis import g
from fragenbasis import tr
from fragenbasis2 import last
from fragenbasis import fxm, mix
def months(s, a, b): return [m for m in sorted(s) if a <= m <= b]
def rule(c, d, bc, bd): return c / d > bc / bd and d <= bd + .05
def win_share(series_fn, shares, a, b, L):
    ms = months(tr, a, b); ms = [m for m in ms if m in g and (btc is None or True)]
    out = {k: [0, 0] for k in shares}
    for i in range(0, len(ms) - L):
        s0, e0 = ms[i], ms[i + L]
        bc, bd = cagr_mdd(mix(series_fn(shares[0]) [0], series_fn(shares[0])[1], s0, e0, 12))
        for k in shares[1:]:
            ss, w = series_fn(k); c, d = cagr_mdd(mix(ss, w, s0, e0, 12)); out[k][1] += 1; out[k][0] += rule(c, d, bc, bd)
    return {k: round(v[0] / v[1], 3) for k, v in out.items() if k != shares[0]}, len(ms) - L
# R1
gs = list(range(0, 101, 5)); r1, n1 = win_share(lambda x: ([tr, g], [1 - x / 100, x / 100]), gs, "1971-08", last, 120)
# R2 Euro
eur = lambda s: {m: s[m] / fxm[m] for m in s if m in fxm}
tr_e, g_e = eur(tr), eur(g); full_e = []
base_e = cagr_mdd(mix([tr_e, g_e], [1, 0], "2003-12", last, 12))
for x in gs:
    c, d = cagr_mdd(mix([tr_e, g_e], [1 - x / 100, x / 100], "2003-12", last, 12)); full_e.append(dict(gold=x, cagr=round(c, 4), mdd=round(d, 3), ratio=round(c / d, 3), ok=x > 0 and rule(c, d, *base_e)))
# R3
tri = [(a, b) for a in range(0, 51, 5) for b in range(0, 51 - a, 5)]
r3, n3 = win_share(lambda k: ([tr, g, btc], [1 - (k[0] + k[1]) / 100, k[0] / 100, k[1] / 100]), [(0, 0)] + [t for t in tri if t != (0, 0)], "2014-09", last, 60)
# R4
def reb(sp, go, bt):
    res = {}
    for lab, k in (("nie", 0), ("jährlich", 12), ("halbjährlich", 6), ("vierteljährlich", 3), ("monatlich", 1)):
        c, d = cagr_mdd(mix([tr, g, btc], [sp / 100, go / 100, bt / 100], "2014-09", last, k)); res[lab] = (c, d)
    y = res["jährlich"]; out = {}
    for lab, (c, d) in res.items():
        v = "gleich"
        if c >= y[0] + .002 and d <= y[1] + .01: v = "besser"
        elif c <= y[0] - .002 or d >= y[1] + .01: v = "schlechter"
        out[lab] = dict(cagr=round(c, 4), mdd=round(d, 3), vs_jaehrlich=v if lab != "jährlich" else "–")
    return out
K = json.load(open("site/fragen.json"))["konstellation"]["rows"]; A = {r["gold"]: r for r in json.load(open("site/fragen.json"))["golda"]["rows"]}
cand = []
for r in K:
    if r["sp"] < 50 or not r["ok"]: continue
    gsh, bsh = r["gold"], r["btc"]
    a_ = True; b_ = A[gsh]["ok"] if gsh > 0 else True
    c_ = r3[(gsh, bsh)] >= .75 and (r1.get(gsh, 1) >= .75 if gsh > 0 else True)
    d_ = next(x for x in full_e if x["gold"] == gsh)["ok"] if gsh > 0 else True
    cand.append(dict(sp=r["sp"], gold=gsh, btc=bsh, cagr=r["cagr"], mdd=r["mdd"], ratio=r["ratio"], r3=r3[(gsh, bsh)], r1=r1.get(gsh), c=c_, d=d_, b=b_))
for r in cand:
    r["reb"] = reb(r["sp"], r["gold"], r["btc"]) if r["c"] and r["d"] and r["b"] else None
    r["e"] = r["reb"] is not None and not any(v["vs_jaehrlich"] == "besser" for v in r["reb"].values())
    r["alle"] = r["b"] and r["c"] and r["d"] and r["e"]
ok = sorted([r for r in cand if r["alle"]], key=lambda r: -r["ratio"])
R = json.load(open("site/fragen.json"))
R["robust"] = dict(r1=[dict(gold=k, share=v) for k, v in r1.items()], n1=n1, euro=full_e, n3=n3,
                   cand=sorted(cand, key=lambda r: -r["ratio"])[:12], n_cand=len(cand), n_alle=len(ok), best=ok[:10],
                   reb=[dict(label="%d/%d/%d" % t, **{"r": reb(*t)}) for t in ((50, 40, 10), (50, 35, 15), (60, 40, 0), (80, 10, 10))])
json.dump(R, open("site/fragen.json", "w"), ensure_ascii=False, indent=1)
print("Fenster R1:", n1, " R3:", n3)
print("R1 Anteil Fenster mit erfüllter Regel je Goldanteil:", r1)
print("R2 Euro:"); [print(x) for x in full_e if x["gold"] in (0, 20, 30, 40, 50)]
print("Kandidaten (S&P>=50, Gesamtfenster ok):", len(cand), " alle Bedingungen:", len(ok))
for r in sorted(cand, key=lambda r: -r["ratio"])[:10]: print({k: r[k] for k in ("sp", "gold", "btc", "ratio", "r3", "r1", "b", "c", "d", "e", "alle")})
print("R4:"); [print(x["label"], {k: (v["cagr"], v["mdd"], v["vs_jaehrlich"]) for k, v in x["r"].items()}) for x in R["robust"]["reb"]]
print("BEST:", ok[:3])
