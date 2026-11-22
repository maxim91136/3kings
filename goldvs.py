"""S&P 500 gegen Gold (REGELN 2026-11-22, nur Information): Monatsdaten in Dollar, S&P 500 mit Dividenden (Shiller), Gold (gold_long).
Langfristige Renditen ab mehreren Startpunkten, Gold in schweren S&P-Rückgängen, Mischungen seit 1971 (jährlich zurückgewichtet). Schreibt site/goldvs.json."""
import csv, json
sh = list(csv.DictReader(open("data/shiller.csv")))
g = {r[0][:7]: float(r[1]) for r in list(csv.reader(open("data/gold_long.csv")))[1:] if r[1]}
tr, lvl, prev = {}, 1.0, None
for r in sh:
    p = float(r["SP500"] or 0); d = float(r["Dividend"] or 0)
    if p <= 0: continue
    if prev: lvl *= (p + d / 12) / prev
    tr[r["Date"][:7]] = lvl; prev = p
ms = sorted(set(tr) & set(g)); end = ms[-1]
cg = lambda a, s: (s[end] / s[a]) ** (12 / (ms.index(end) - ms.index(a))) - 1
long = [dict(start=a, spx=round(cg(a, tr), 4), gold=round(cg(a, g), 4)) for a in ("1928-12", "1971-08", "1980-01", "2000-01", "2011-08")]
EP = [("1973–74", "1972-12", "1974-09"), ("1987", "1987-08", "1987-11"), ("2000–02", "2000-08", "2002-09"), ("2007–09", "2007-10", "2009-02"), ("2020", "2020-02", "2020-03"), ("2022", "2021-12", "2022-09")]
crash = [dict(name=n, spx=round(tr[b] / tr[a] - 1, 3), gold=round(g[b] / g[a] - 1, 3)) for n, a, b in EP if a in tr and b in g]
K = [m for m in ms if m >= "1971-08"]; mix = []
for w in (1.0, .9, .8, .7):
    a, b, vals = w, 1 - w, []
    for i in range(1, len(K)):
        a *= tr[K[i]] / tr[K[i - 1]]; b *= g[K[i]] / g[K[i - 1]]
        if K[i][5:] == "01": t = a + b; a, b = t * w, t * (1 - w)
        vals.append(a + b)
    pk = dd = 0
    for x in vals: pk = max(pk, x); dd = max(dd, 1 - x / pk)
    mix.append(dict(spx=w, cagr=round(vals[-1] ** (12 / len(vals)) - 1, 4), mdd=round(dd, 3)))
json.dump(dict(end=end, long=long, crash=crash, mix=mix), open("site/goldvs.json", "w"), ensure_ascii=False, indent=1)
print(end, long[0], mix[2])
