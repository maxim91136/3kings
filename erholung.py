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

# --- Nach dem Absturz (REGELN 2026-11-22, Regeln vorab): Einstieg beim ersten Monatsschluss X % unter dem Hoch, 60 Einheiten, 60 Monate ---
H = 60
def wert(pp, t0):
    """(Einmal, Sparplan) Wert nach H Monaten; None wenn der Bewertungsmonat fehlt."""
    if t0 + H >= len(pp): return None
    e = H * pp[t0 + H] / pp[t0]; s = sum(pp[t0 + H] / pp[t0 + j] for j in range(H))
    return e, s
def fall(pp, t0):
    w = wert(pp, t0)
    if w is None: return None
    return dict(lump=round(w[0], 2), spar=round(w[1], 2), lead=round((w[0] - w[1]) / H, 3))
def block(entries):
    done = [e for e in entries if e["lead"] is not None]
    ahead = sum(1 for e in done if e["lead"] > 0)
    return dict(cases=entries, n=len(done), open=len(entries) - len(done), ahead=ahead,
                share=round(ahead / len(done), 3) if done else None,
                med_lead=round(st.median([e["lead"] for e in done]), 3) if done else None)
def entry(pp, mm, t0):
    f = fall(pp, t0) or dict(lump=None, spar=None, lead=None)
    return dict(month=mm[t0], **f)
nach = {}
for X in (0.0, 0.2, 0.3, 0.5):
    ent = []
    for pk, tr, rec in eps:
        end = rec if rec is not None else len(p) - 1
        t0 = pk if X == 0 else next((i for i in range(pk, end + 1) if (p[pk] - p[i]) / p[pk] >= X), None)
        if t0 is not None: ent.append(entry(p, ms, t0))
    nach[str(int(X * 100))] = block(ent)
main = nach["30"]; main["testable"] = main["n"] >= 5; main["confirmed"] = bool(main["testable"] and main["share"] >= 2 / 3)
out["nach"] = nach
# --- Mitlaufende Akte "Absturz-Annahme": ab 2026-11, erster Monatsschluss >= 30 % unter dem Hoch einer Phase ---
today = dt.date.today(); lastm = (today.replace(day=1) - dt.timedelta(days=1)).strftime("%Y-%m")
mo = {}
for r in list(csv.reader(open("data/spx_long.csv")))[1:]:
    if r[1]: mo[r[0][:7]] = float(r[1])
fm = [k for k in sorted(mo) if k <= lastm]; fp = [mo[k] for k in fm]
ath = fp[0]; hit = False; cases = []
for i in range(1, len(fp)):
    if fp[i] >= ath: ath = fp[i]; hit = False; continue
    if not hit and (ath - fp[i]) / ath >= 0.30:
        hit = True
        if fm[i] > LAST: cases.append(entry(fp, fm, i))
dd = round((ath - fp[-1]) / ath, 3)
out["forward"] = dict(since=LAST, last_month=fm[-1], ath=round(ath, 2), dd=dd, hit=hit, cases=cases, n=len([c for c in cases if c["lead"] is not None]))
json.dump(out, open("site/erholung.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: out[k] for k in ("nach", "forward")}, ensure_ascii=False, indent=1))
