"""Saisonalität (REGELN 2026-11-22, Regeln vorab): Monate, Sell in May, Jahreswechsel, Wahlzyklus, Wochentag, Monatswechsel. Schreibt fragen.json["saison"]."""
import csv, json, datetime as dt, numpy as np
LAST = "2026-10"
def daily(path, col=1):
    out = []
    for r in list(csv.reader(open(path)))[1:]:
        if r[col]: out.append((dt.date.fromisoformat(r[0]), float(r[col])))
    return sorted(out)
spx = daily("data/spx_long.csv"); btcd = daily("data/btc_long.csv")
def month_end(d):
    o = {}
    for day, v in d: o[day.strftime("%Y-%m")] = v
    return o
sp_m = month_end(spx); bt_m = month_end([x for x in btcd if x[0] >= dt.date(2014, 9, 1)])
gold = {}
for r in list(csv.reader(open("data/gold_long.csv")))[1:]:
    if r[1] and r[0] >= "1971-08": gold[r[0][:7]] = float(r[1])
def mrets(s, a, b):
    ms = [m for m in sorted(s) if a <= m <= b]; return {ms[i]: s[ms[i]] / s[ms[i - 1]] - 1 for i in range(1, len(ms))}
A = {"S&P 500": mrets(sp_m, "1927-12", LAST), "Gold": mrets(gold, "1971-08", LAST), "Bitcoin": mrets(bt_m, "2014-09", LAST)}
def year_matrix(r):
    ys = sorted({int(m[:4]) for m in r}); rows, yy = [], []
    for y in ys:
        row = [r.get("%d-%02d" % (y, k)) for k in range(1, 13)]
        if all(v is not None for v in row): rows.append(row); yy.append(y)
    return np.array(rows), yy
def qual(M):
    n = len(M); h = n // 2; hit = (M > 0).mean(0); m1 = M[:h].mean(0); m2 = M[h:].mean(0)
    return ((hit >= .7) & (m1 > 0) & (m2 > 0)) | ((hit <= .3) & (m1 < 0) & (m2 < 0)), hit, M.mean(0), m1, m2
rng = np.random.default_rng(1); R = {}; months = {}
for name, r in A.items():
    M, yy = year_matrix(r); q, hit, mean, m1, m2 = qual(M)
    sh = []
    for _ in range(1000):
        P = np.array([rng.permutation(row) for row in M]); sh.append(qual(P)[0].sum())
    months[name] = dict(years=[yy[0], yy[-1]], n=len(yy), rows=[dict(m=k + 1, mean=round(float(mean[k]), 4), hit=round(float(hit[k]), 3), m1=round(float(m1[k]), 4), m2=round(float(m2[k]), 4), pattern=bool(q[k])) for k in range(12)],
                       n_pattern=int(q.sum()), chance=round(float(np.mean(sh)), 2))
R["monate"] = months
# Sell in May
def winter_summer(r, a_year):
    out = []
    for y in range(a_year, 2027):
        w = [r.get("%d-%02d" % (y - 1, 11)), r.get("%d-%02d" % (y - 1, 12))] + [r.get("%d-%02d" % (y, k)) for k in range(1, 5)]
        s = [r.get("%d-%02d" % (y, k)) for k in range(5, 11)]
        if all(v is not None for v in w + s): out.append((y, float(np.prod([1 + v for v in w]) - 1), float(np.prod([1 + v for v in s]) - 1)))
    return out
sim = {}
for name, a in (("S&P 500", 1928), ("Gold", 1972)):
    t = winter_summer(A[name], a); d = np.array([w - s for _, w, s in t]); n = len(t); h = n // 2
    sim[name] = dict(years=[t[0][0], t[-1][0]], n=n, winter=round(float(np.mean([w for _, w, _ in t])), 4), summer=round(float(np.mean([s for _, _, s in t])), 4), diff=round(float(d.mean()), 4), share=round(float((d > 0).mean()), 3),
                     d1=round(float(d[:h].mean()), 4), d2=round(float(d[h:].mean()), 4), pattern=bool(d.mean() >= .02 and (d > 0).mean() >= .6 and d[:h].mean() > 0 and d[h:].mean() > 0))
R["sell_in_may"] = sim
def strat(r, y0, y1):
    bh = [1.0]; sm = [1.0]
    for m in sorted(r):
        y = int(m[:4]); k = int(m[5:])
        if not (y0 <= y <= y1): continue
        bh.append(bh[-1] * (1 + r[m])); sm.append(sm[-1] * (1 + (r[m] if (k >= 11 or k <= 4) else 0)))
    def st(v):
        n = len(v) - 1; pk = dd = 0
        for x in v: pk = max(pk, x); dd = max(dd, 1 - x / pk)
        c = v[-1] ** (12 / n) - 1; return c, dd
    (c1, d1), (c2, d2) = st(bh), st(sm); return dict(bh=dict(cagr=round(c1, 4), mdd=round(d1, 3), ratio=round(c1 / d1, 3)), sim=dict(cagr=round(c2, 4), mdd=round(d2, 3), ratio=round(c2 / d2, 3)), better=bool(c2 / d2 > c1 / d1 and c2 >= c1 - .02))
R["gegenprobe"] = dict(full=strat(A["S&P 500"], 1928, 2026), h1=strat(A["S&P 500"], 1928, 1976), h2=strat(A["S&P 500"], 1977, 2026))
# daily S&P
dates = [d for d, _ in spx]; P = np.array([v for _, v in spx]); ret = P[1:] / P[:-1] - 1; rd = dates[1:]
# Santa
yrs = {}
for i, d in enumerate(dates): yrs.setdefault(d.year, []).append(i)
w7 = P[7:] / P[:-7] - 1; avg7 = float(w7.mean()); sant = []
for y in range(1928, 2026):
    dec = [i for i in yrs[y] if dates[i].month == 12]; jan = [i for i in yrs.get(y + 1, []) if dates[i].month == 1]
    if len(dec) >= 6 and len(jan) >= 2: sant.append((y, P[jan[1]] / P[dec[-6]] - 1))
v = np.array([x for _, x in sant]); h = len(v) // 2
R["santa"] = dict(n=len(v), avg7=round(avg7, 4), mean=round(float(v.mean()), 4), share=round(float((v > 0).mean()), 3), m1=round(float(v[:h].mean() - avg7), 4), m2=round(float(v[h:].mean() - avg7), 4),
                  pattern=bool((v > 0).mean() >= .7 and v.mean() >= avg7 + .005 and v[:h].mean() > avg7 and v[h:].mean() > avg7))
# Wahlzyklus
yr = {}
for y in range(1928, 2026):
    a = [P[i] for i in yrs[y - 1]][-1] if y - 1 in yrs else None; b = [P[i] for i in yrs[y]][-1]
    if a: yr[y] = b / a - 1
cyc = {k: [r for y, r in yr.items() if (y - 1928) % 4 == k] for k in range(4)}; allm = float(np.mean(list(yr.values()))); ys = sorted(yr); half = ys[len(ys) // 2]
def dev(k, lo, hi): xs = [r for y, r in yr.items() if (y - 1928) % 4 == k and lo <= y < hi]; return float(np.mean(xs)) - float(np.mean([r for y, r in yr.items() if lo <= y < hi]))
R["wahl"] = dict(overall=round(allm, 4), rows=[dict(k=k, n=len(v), mean=round(float(np.mean(v)), 4), dev=round(float(np.mean(v)) - allm, 4), d1=round(dev(k, 0, half), 4), d2=round(dev(k, half, 9999), 4),
                 pattern=bool(abs(np.mean(v) - allm) >= .03 and np.sign(dev(k, 0, half)) == np.sign(dev(k, half, 9999)) == np.sign(np.mean(v) - allm))) for k, v in cyc.items()])
# Wochentag, Monatswechsel
wd = np.array([d.weekday() for d in rd]); allr = float(ret.mean()); mid = len(ret) // 2; rows = []
for k in range(5):
    sel = wd == k; m = float(ret[sel].mean()); m1 = float(ret[:mid][sel[:mid]].mean() - ret[:mid].mean()); m2 = float(ret[mid:][sel[mid:]].mean() - ret[mid:].mean())
    rows.append(dict(k=k, mean=round(m, 5), dev=round(m - allr, 5), d1=round(m1, 5), d2=round(m2, 5), pattern=bool(abs(m - allr) >= .0003 and np.sign(m1) == np.sign(m2) == np.sign(m - allr))))
R["wochentag"] = dict(overall=round(allr, 5), rows=rows)
tom = np.zeros(len(ret), bool); mk = [d.strftime("%Y-%m") for d in rd]
for i in range(len(rd)):
    first = [j for j in range(max(0, i - 3), i + 1) if mk[j] == mk[i]]
    if len(first) == len([j for j in range(max(0, i - 3), i + 1)]) and (i < 3 or mk[i - 3] != mk[i]) is False: pass
idx = {}
for i, m in enumerate(mk): idx.setdefault(m, []).append(i)
for m, l in idx.items():
    tom[l[:3]] = True; tom[l[-1]] = True
d_all = float(ret[tom].mean() - ret[~tom].mean()); d1 = float(ret[:mid][tom[:mid]].mean() - ret[:mid][~tom[:mid]].mean()); d2 = float(ret[mid:][tom[mid:]].mean() - ret[mid:][~tom[mid:]].mean())
R["monatswechsel"] = dict(diff=round(d_all, 5), d1=round(d1, 5), d2=round(d2, 5), n=int(tom.sum()), pattern=bool(d_all >= .0005 and d1 > 0 and d2 > 0))
J = json.load(open("site/fragen.json")); J["saison"] = R; json.dump(J, open("site/fragen.json", "w"), ensure_ascii=False, indent=1)
for k in ("monate",):
    for n, v in R[k].items(): print(n, v["years"], "Muster:", v["n_pattern"], "Zufall:", v["chance"], [(r["m"], r["mean"], r["hit"]) for r in v["rows"] if r["pattern"]])
print("Sell in May", R["sell_in_may"]); print("Gegenprobe", R["gegenprobe"]); print("Santa", R["santa"]); print("Wahl", R["wahl"]); print("Wochentag", R["wochentag"]); print("Monatswechsel", R["monatswechsel"])
