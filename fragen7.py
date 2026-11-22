"""Diversifikation über die Zeit (REGELN 2026-11-22, Regeln vorab): gleitende 24-Monats-Korrelation, Krisenmonate. Ergänzt fragen.json um korr_zeit."""
import json
exec(open("fragen2.py").read().split("R = json.load")[0])
def pc(x, y):
    mx, my = sum(x) / len(x), sum(y) / len(y); cv = sum((a - mx) * (b - my) for a, b in zip(x, y)); return cv / (sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y)) ** .5
def roll(a, b, start, L=24):
    ra, rb = rets(a, start, last), rets(b, start, last); ms = sorted(set(ra) & set(rb)); out = []
    for i in range(L, len(ms) + 1): w = ms[i - L:i]; out.append((w[-1], pc([ra[m] for m in w], [rb[m] for m in w])))
    return out
def crisis_corr(a, b, start):
    ra, rb, rs = rets(a, start, last), rets(b, start, last), rets(tr, start, last); ms = sorted(set(ra) & set(rb) & set(rs))
    worst = set(sorted(ms, key=lambda m: rs[m])[:max(1, len(ms) // 10)]); rest = [m for m in ms if m not in worst]
    return dict(n=len(worst), crisis=round(pc([ra[m] for m in worst], [rb[m] for m in worst]), 2) if len(worst) > 2 else None, rest=round(pc([ra[m] for m in rest], [rb[m] for m in rest]), 2))
rows = []
for name, a, b, st_ in (("Gold – S&P 500", g, tr, "1971-08"), ("Gold – S&P 500", g, tr, "2014-09"), ("Bitcoin – S&P 500", btc, tr, "2014-09"), ("Bitcoin – Gold", btc, g, "2014-09")):
    r = roll(a, b, st_); v = [x[1] for x in r]; lo = min(r, key=lambda x: x[1]); hi = max(r, key=lambda x: x[1])
    rows.append(dict(name=name, start=st_, n=len(v), lo=round(lo[1], 2), lo_m=lo[0], hi=round(hi[1], 2), hi_m=hi[0], now=round(v[-1], 2), share=round(sum(x >= .5 for x in v) / len(v), 3), stable=sum(x >= .5 for x in v) / len(v) <= .25,
                     crisis=crisis_corr(a, b, st_) if "S&P" in name else None, series=[(m, round(c, 2)) for m, c in (r if st_ == "2014-09" else r[::6])]))
R = json.load(open("site/fragen.json")); R["korr_zeit"] = dict(last=last, rows=rows); json.dump(R, open("site/fragen.json", "w"), ensure_ascii=False, indent=1)
for r in rows: print({k: r[k] for k in r if k != "series"})
