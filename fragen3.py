"""Aufteilung der Satelliten (REGELN 2026-11-22, Regeln vorab): alle Mischungen S&P/Gold/Bitcoin in 5-%-Schritten, alle Anteile von 0 bis 100 %.
Ergänzt site/fragen.json um den Schlüssel konstellation."""
import json
from fragenbasis import btc
from fragenbasis import cagr_mdd
from fragenbasis import g
from fragenbasis import tr
from fragenbasis2 import last
from fragenbasis import mix
def run(a, b):
    out = []
    for gs in range(0, 101, 5):
        for bs in range(0, 101 - gs, 5):
            w = [1 - (gs + bs) / 100, gs / 100, bs / 100]
            c, d = cagr_mdd(mix([tr, g, btc], w, a, b, 12)); out.append(dict(sp=round(w[0] * 100), gold=gs, btc=bs, cagr=round(c, 4), mdd=round(d, 3), ratio=round(c / d, 3)))
    return out
full = run("2014-09", last); h1 = run("2014-09", "2020-08"); h2 = run("2020-09", last)
base = next(r for r in full if r["gold"] == 0 and r["btc"] == 0)
for r in full: r["ok"] = (r["gold"] + r["btc"]) > 0 and r["ratio"] > base["ratio"] and r["mdd"] <= base["mdd"] + .05
def rank(rows): 
    o = sorted(rows, key=lambda r: -r["ratio"]); return {(r["gold"], r["btc"]): i + 1 for i, r in enumerate(o)}
r1, r2 = rank(h1), rank(h2)
for r in full: r["rank1"] = r1[(r["gold"], r["btc"])]; r["rank2"] = r2[(r["gold"], r["btc"])]
ok = sorted([r for r in full if r["ok"]], key=lambda r: -r["ratio"])
R = json.load(open("site/fragen.json"))
R["konstellation"] = dict(last=last, base=base, n=len(full), n_ok=len(ok), best=ok[:5], rows=full)
json.dump(R, open("site/fragen.json", "w"), ensure_ascii=False, indent=1)
print("Mischungen:", len(full), "erfüllen Regel:", len(ok), "Basis", base)
for r in ok[:10]: print(r)
print("--- Hälften: beste je Hälfte")
for lab, rows in (("2014-2020", h1), ("2020-2026", h2)):
    t = sorted(rows, key=lambda r: -r["ratio"])[:3]; print(lab, [(r["sp"], r["gold"], r["btc"], r["ratio"]) for r in t])
print("80/10/10:", next(r for r in full if (r["gold"], r["btc"]) == (10, 10)))
