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
    for pk, _tr, rec in eps:
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

# --- Stufenstrategien (REGELN 2026-11-22, Regeln vorab): feste Liste S1..S5, Vergleich R1..R3, Bewertung 60 Monate nach t20 ---
STRAT = {"S1": ([.2, .3, .4, .5], [.25] * 4), "S2": ([.2, .3, .4, .5], [.1, .2, .3, .4]), "S3": ([.2, .3, .4, .5], [.4, .3, .2, .1]),
         "S4": ([.3, .5], [.5, .5]), "S5": ([.2, .25, .3, .35, .4], [.2] * 5)}
def first_hit(pp, pk, end, x):
    return next((i for i in range(pk, end + 1) if (pp[pk] - pp[i]) / pp[pk] >= x), None)
def stufen_val(pp, pk, end, marks, ws, T):
    v = 0.0
    for x, w in zip(marks, ws, strict=False):
        i = first_hit(pp, pk, end, x)
        if i is not None and i <= T: v += 60 * w * pp[T] / pp[i]
        else: v += 60 * w
    return v
def idle(pp, pk, end, marks, ws, T):
    return sum(w for x, w in zip(marks, ws, strict=False) if (first_hit(pp, pk, end, x) is None or first_hit(pp, pk, end, x) > T))
res = {k: [] for k in list(STRAT) + ["R1", "R2", "R3"]}; idl = {k: [] for k in STRAT}; used = []
for pk, _tr, rec in eps:
    end = rec if rec is not None else len(p) - 1
    t20 = first_hit(p, pk, end, .2)
    if t20 is None or t20 + H >= len(p): continue
    T = t20 + H; used.append(ms[t20])
    for k, (mk, ws) in STRAT.items():
        res[k].append(stufen_val(p, pk, end, mk, ws, T)); idl[k].append(idle(p, pk, end, mk, ws, T))
    res["R1"].append(stufen_val(p, pk, end, [.2], [1], T)); res["R2"].append(stufen_val(p, pk, end, [.3], [1], T))
    res["R3"].append(sum(p[T] / p[t20 + j] for j in range(H)))
n = len(used); rows_s = {}
for k in res:
    v = res[k]
    rows_s[k] = dict(vs_spar=sum(1 for a, b in zip(v, res["R3"], strict=False) if a > b), vs_lump30=sum(1 for a, b in zip(v, res["R2"], strict=False) if a > b),
                     med=round(st.median(v) / 60, 3), worst=round(min(v) / 60, 3), idle=round(st.mean(idl[k]), 3) if k in idl else None,
                     vals=[round(a / 60, 3) for a in v])
s1 = rows_s["S1"]; test = n >= 5
out["stufen"] = dict(n=n, months=used, rows=rows_s, testable=test, share=round(s1["vs_spar"] / n, 3) if n else None,
                     confirmed=bool(test and s1["vs_spar"] / n >= 2 / 3),
                     best_med=max(STRAT, key=lambda k: rows_s[k]["med"]), best_worst=max(STRAT, key=lambda k: rows_s[k]["worst"]))
json.dump(out, open("site/erholung.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(out["stufen"], ensure_ascii=False, indent=1))

# --- Neurechnung mit Dividenden und Zins auf Bargeld (REGELN 2026-11-22, Regeln vorab) ---
sh = {}
for r in csv.DictReader(open("data/shiller.csv")):
    if float(r["Dividend"]) > 0 and float(r["Long Interest Rate"]) > 0:
        sh[r["Date"][:7]] = (float(r["Dividend"]) / float(r["SP500"]), float(r["Long Interest Rate"]) / 100)
lastsh = sh[max(sh)]
dyr = [sh.get(k, lastsh if k > max(sh) else None) for k in ms]
G = [None] + [p[i] / p[i - 1] + dyr[i][0] / 12 for i in range(1, len(p))]
C = [None] + [1 + dyr[i][1] / 12 for i in range(1, len(p))]
def sim(S, T, buys):
    """buys: {Monat: Einheiten}; Startkasse 60 in S, Kauf am Monatsende, Bewertung in T."""
    cash = 60.0; eq = 0.0
    for t in range(S, T + 1):
        if t > S: cash *= C[t]; eq *= G[t]
        a = buys.get(t, 0.0)
        if a: cash -= a; eq += a
    return eq + cash
def add(d, k, v): d[k] = d.get(k, 0.0) + v
nach_tr = {}
for X in (0.0, 0.2, 0.3, 0.5):
    ent = []
    for pk, _tr, rec in eps:
        end = rec if rec is not None else len(p) - 1
        t0 = pk if X == 0 else first_hit(p, pk, end, X)
        if t0 is None: continue
        if t0 + H >= len(p): ent.append(dict(month=ms[t0], lump=None, spar=None, lead=None)); continue
        e = sim(t0, t0 + H, {t0: 60.0}); s_ = sim(t0, t0 + H, {t0 + j: 1.0 for j in range(H)})
        ent.append(dict(month=ms[t0], lump=round(e, 2), spar=round(s_, 2), lead=round((e - s_) / H, 3)))
    nach_tr[str(int(X * 100))] = block(ent)
m3 = nach_tr["30"]; m3["testable"] = m3["n"] >= 5; m3["confirmed"] = bool(m3["testable"] and m3["share"] >= 2 / 3)
res = {k: [] for k in list(STRAT) + ["R1", "R2", "R3"]}
for pk, _tr, rec in eps:
    end = rec if rec is not None else len(p) - 1
    t20 = first_hit(p, pk, end, .2)
    if t20 is None or t20 + H >= len(p): continue
    T = t20 + H
    for k, (mk, ws) in STRAT.items():
        b = {}
        for x, w in zip(mk, ws, strict=False):
            i = first_hit(p, pk, end, x)
            if i is not None and i <= T: add(b, i, 60 * w)
        res[k].append(sim(t20, T, b))
    res["R1"].append(sim(t20, T, {t20: 60.0}))
    i30 = first_hit(p, pk, end, .3); res["R2"].append(sim(t20, T, {i30: 60.0} if i30 is not None and i30 <= T else {}))
    res["R3"].append(sim(t20, T, {t20 + j: 1.0 for j in range(H)}))
rt = {}
for k in res:
    v = res[k]
    rt[k] = dict(vs_spar=sum(1 for a, b in zip(v, res["R3"], strict=False) if a > b), vs_lump30=sum(1 for a, b in zip(v, res["R2"], strict=False) if a > b),
                 med=round(st.median(v) / 60, 3), worst=round(min(v) / 60, 3), vals=[round(a / 60, 3) for a in v])
nn = len(res["R3"])
out["tr"] = dict(shiller_end=max(sh), nach=nach_tr, stufen=dict(n=nn, rows=rt, testable=nn >= 5,
                 confirmed=bool(nn >= 5 and rt["S1"]["vs_spar"] / nn >= 2 / 3),
                 best_med=max(STRAT, key=lambda k: rt[k]["med"]), best_worst=max(STRAT, key=lambda k: rt[k]["worst"])))
json.dump(out, open("site/erholung.json", "w"), ensure_ascii=False, indent=1)

# --- Restliche Review-Punkte (REGELN 2026-11-22, Regeln vorab): Spannen, Test 1 mit Dividenden, real, Euro ---
from math import comb
def cp(k, n, a=0.05):
    """Clopper-Pearson 95 %, ohne scipy (Bisektion auf der Binomialverteilung)."""
    if not n: return None
    def tail_ge(pp): return sum(comb(n, i) * pp ** i * (1 - pp) ** (n - i) for i in range(k, n + 1))
    def tail_le(pp): return sum(comb(n, i) * pp ** i * (1 - pp) ** (n - i) for i in range(0, k + 1))
    def bis(f, target, inc):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if (f(mid) < target) == inc: lo = mid
            else: hi = mid
        return (lo + hi) / 2
    lo = 0.0 if k == 0 else bis(tail_ge, a / 2, True)
    hi = 1.0 if k == n else bis(tail_le, a / 2, False)
    return [round(lo, 3), round(hi, 3)]
cpi = {}
for r in csv.DictReader(open("data/shiller.csv")):
    if float(r["Consumer Price Index"]) > 0: cpi[r["Date"][:7]] = float(r["Consumer Price Index"])
fx = {}
for r in list(csv.reader(open("data/ind_EURUSD.csv")))[1:]:
    if len(r) > 1 and r[1]: fx[r[0][:7]] = float(r[1])
def arr(f):
    return [None] + [f(i) for i in range(1, len(p))]
GR = arr(lambda i: G[i] * cpi[ms[i - 1]] / cpi[ms[i]] if ms[i] in cpi and ms[i - 1] in cpi else None)
CR = arr(lambda i: C[i] * cpi[ms[i - 1]] / cpi[ms[i]] if ms[i] in cpi and ms[i - 1] in cpi else None)
GE = arr(lambda i: G[i] * fx[ms[i - 1]] / fx[ms[i]] if ms[i] in fx and ms[i - 1] in fx else None)
CE = arr(lambda i: C[i] if ms[i] in fx and ms[i - 1] in fx else None)
def simx(S, T, buys, Gx, Cx):
    if T >= len(p) or any(Gx[t] is None for t in range(S + 1, T + 1)): return None
    if ms[S] not in (fx if Gx is GE else cpi if Gx is GR else ms): return None
    cash = 60.0; eq = 0.0
    for t in range(S, T + 1):
        if t > S: cash *= Cx[t]; eq *= Gx[t]
        a = buys.get(t, 0.0)
        if a: cash -= a; eq += a
    return eq + cash
def t1(Gx):
    rows = []
    for pk, tr, _rec in eps:
        def lump(pk=pk, tr=tr):
            w = 1.0
            for t in range(pk + 1, len(p)):
                if Gx[t] is None: return None
                w *= Gx[t]
                if t > tr and w >= 1: return t - pk
            return None
        def spar_(pk=pk, tr=tr):
            v = 0.0; paid = 0
            for t in range(pk, len(p)):
                if t > pk:
                    if Gx[t] is None: return None
                    v *= Gx[t]
                v += 1; paid += 1
                if t > tr and v >= paid: return t - pk
            return None
        if Gx is GE and ms[pk] not in fx: continue
        if Gx is GR and ms[pk] not in cpi: continue
        rows.append(dict(peak=ms[pk], lump=lump(), spar=spar_()))
    done = [r for r in rows if r["lump"] is not None and r["spar"] is not None]
    return dict(rows=rows, n=len(done), earlier=sum(1 for r in done if r["spar"] < r["lump"]),
                med_lump=round(st.median([r["lump"] for r in done])) if done else None,
                med_spar=round(st.median([r["spar"] for r in done])) if done else None)
def t23(Gx, Cx):
    nb = {}
    for X in (0.0, 0.2, 0.3, 0.5):
        ent = []
        for pk, _tr, rec in eps:
            end = rec if rec is not None else len(p) - 1
            t0 = pk if X == 0 else first_hit(p, pk, end, X)
            if t0 is None: continue
            e = simx(t0, t0 + H, {t0: 60.0}, Gx, Cx); s_ = simx(t0, t0 + H, {t0 + j: 1.0 for j in range(H)}, Gx, Cx)
            if Gx is GE and e is None: continue
            ent.append(dict(month=ms[t0], lump=None if e is None else round(e, 2), spar=None if s_ is None else round(s_, 2),
                            lead=None if e is None or s_ is None else round((e - s_) / H, 3)))
        b = block(ent); b["ci"] = cp(b["ahead"], b["n"]); nb[str(int(X * 100))] = b
    m = nb["30"]; m["testable"] = m["n"] >= 5; m["confirmed"] = bool(m["testable"] and m["share"] >= 2 / 3)
    rs = {k: [] for k in list(STRAT) + ["R1", "R2", "R3"]}
    for pk, _tr, rec in eps:
        end = rec if rec is not None else len(p) - 1
        t20 = first_hit(p, pk, end, .2)
        if t20 is None: continue
        T = t20 + H; vals = {}
        for k, (mk, ws) in STRAT.items():
            bb = {}
            for x, w in zip(mk, ws, strict=False):
                i = first_hit(p, pk, end, x)
                if i is not None and i <= T: add(bb, i, 60 * w)
            vals[k] = simx(t20, T, bb, Gx, Cx)
        vals["R1"] = simx(t20, T, {t20: 60.0}, Gx, Cx)
        i30 = first_hit(p, pk, end, .3); vals["R2"] = simx(t20, T, {i30: 60.0} if i30 is not None and i30 <= T else {}, Gx, Cx)
        vals["R3"] = simx(t20, T, {t20 + j: 1.0 for j in range(H)}, Gx, Cx)
        if any(v is None for v in vals.values()): continue
        for k in rs: rs[k].append(vals[k])
    nn = len(rs["R3"]); rows_ = {}
    for k, v in rs.items():
        if not v: continue
        rows_[k] = dict(vs_spar=sum(1 for a, b in zip(v, rs["R3"], strict=False) if a > b), med=round(st.median(v) / 60, 3), worst=round(min(v) / 60, 3))
    sb = dict(n=nn, rows=rows_, ci=cp(rows_["S1"]["vs_spar"], nn) if nn else None, testable=nn >= 5,
              confirmed=bool(nn >= 5 and rows_["S1"]["vs_spar"] / nn >= 2 / 3))
    return nb, sb
GN = [None] + [p[i] / p[i - 1] for i in range(1, len(p))]; CN = [None] + [1.0] * (len(p) - 1)
out["ci"] = dict(nach30=cp(out["nach"]["30"]["ahead"], out["nach"]["30"]["n"]), stufen=cp(out["stufen"]["rows"]["S1"]["vs_spar"], out["stufen"]["n"]),
                 tr_nach30=cp(out["tr"]["nach"]["30"]["ahead"], out["tr"]["nach"]["30"]["n"]), tr_stufen=cp(out["tr"]["stufen"]["rows"]["S1"]["vs_spar"], out["tr"]["stufen"]["n"]))
out["t1_tr"] = t1(G)
rn, rsb = t23(GR, CR); out["real"] = dict(cpi_end=max(cpi), t1=t1(GR), nach=rn, stufen=rsb)
en_, esb = t23(GE, CE); out["eur"] = dict(fx_start=min(fx), t1=t1(GE), nach=en_, stufen=esb)
json.dump(out, open("site/erholung.json", "w"), ensure_ascii=False, indent=1)
