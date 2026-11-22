"""Erholung nach Abstuerzen: Einmalanlage gegen Sparplan (REGELN 2026-11-22, Regeln vorab). Schreibt site/erholung.json."""
import csv, json, datetime as dt, statistics as st
LAST = "2026-10"; THR = 0.20
m = {}
for r in list(csv.reader(open("data/spx_long.csv")))[1:]:
    if r[1]: m[r[0][:7]] = float(r[1])
ms = [k for k in sorted(m) if k <= LAST]; p = [m[k] for k in ms]
eps = []; ath = p[0]; pk = 0; tr = 0
for i in range(1, len(p)):
    if p[i] >= ath:
        if (ath - p[tr]) / ath >= THR: eps.append((pk, tr, i))
        ath = p[i]; pk = i; tr = i
    elif p[i] < p[tr] or tr == pk: tr = i
open_ep = (ath - p[tr]) / ath >= THR
if open_ep: eps.append((pk, tr, None))
def spar(pk, tr, end):
    units = 0.0
    for j in range(pk, len(p)):
        units += 1 / p[j]; paid = j - pk + 1
        if j > tr and units * p[j] >= paid: return j - pk
    return None
rows = []
for pk, tr, rec in eps:
    lump = None if rec is None else rec - pk
    sp = spar(pk, tr, rec)
    rows.append(dict(peak=ms[pk], trough=ms[tr], depth=round((p[pk] - p[tr]) / p[pk], 3), lump=lump, spar=sp))
done = [r for r in rows if r["lump"] is not None and r["spar"] is not None]
earlier = sum(1 for r in done if r["spar"] < r["lump"])
out = dict(until=LAST, n=len(done), earlier=earlier, share=round(earlier / len(done), 3) if done else None, confirmed=bool(done and earlier / len(done) >= 2 / 3),
           med_lump=round(st.median([r["lump"] for r in done])) if done else None, med_spar=round(st.median([r["spar"] for r in done])) if done else None, rows=rows)
json.dump(out, open("site/erholung.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1)[:2500])
