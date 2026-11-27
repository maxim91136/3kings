"""Warum Gold und Bitcoin (REGELN 2026-11-22, Regeln vorab): Bitcoin gegen S&P 500 und Gold, Diversifikation, Mischungen.
Ergänzt site/fragen.json um die Schlüssel bitcoin, divers, drittel. Nur lokale Daten."""
from fragenbasis import btc
from fragenbasis import cagr_mdd
from fragenbasis import g
from fragenbasis import tr
from fragenbasis2 import fen, last, rows, yrs
import json
from fragenbasis import mix
R = json.load(open("site/fragen.json"))
R["bitcoin"] = dict(last=last, windows=fen, beta=rows[2]["beta"], beta_gold=rows[1]["beta"], high_beta=rows[2]["beta"] > 1.5, years=yrs, n_years=len(yrs),
                    beat_sp=sum(x["btc"] > x["sp"] for x in yrs), beat_gold=sum(x["btc"] > x["gold"] for x in yrs), best_all=all(f["btc_best"] for f in fen))
R["divers"] = dict(rows=rows)
mx = []
for lab, w in (("100/0/0", [1, 0, 0]), ("80/10/10", [.8, .1, .1]), ("60/20/20", [.6, .2, .2]), ("1/3 je", [1 / 3] * 3)):
    c, d = cagr_mdd(mix([tr, g, btc], w, "2014-09", last, 12)); mx.append(dict(label=lab, w=w, cagr=round(c, 4), mdd=round(d, 3), ratio=round(c / d, 3)))
for r in mx: r["better"] = r["label"] != "100/0/0" and r["ratio"] > mx[0]["ratio"] and r["mdd"] <= mx[0]["mdd"] + .05
R["drittel"] = dict(rows=mx, start="2014-09", last=last)
json.dump(R, open("site/fragen.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: R[k] for k in ("bitcoin", "divers", "drittel")}, ensure_ascii=False, indent=1))
