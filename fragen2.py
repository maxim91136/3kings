"""Warum Gold und Bitcoin (REGELN 2026-11-22, Regeln vorab): Bitcoin gegen S&P 500 und Gold, Diversifikation, Mischungen.
Ergänzt site/fragen.json um die Schlüssel bitcoin, divers, drittel. Nur lokale Daten."""
import json, statistics as st
exec(open("fragen.py").read().split("R = {}")[0])  # Daten und Hilfsfunktionen aus fragen.py
last = min(max(tr), max(g), max(btc))
def ym(m, n): y, mo = int(m[:4]), int(m[5:]); t = y * 12 + mo - 1 - n; return "%04d-%02d" % (t // 12, t % 12 + 1)
def stats(s, start, end=None):
    end = end or last; ms = [m for m in sorted(s) if start <= m <= end]; v = [s[m] / s[ms[0]] for m in ms]; c, d = cagr_mdd(v)
    return dict(cagr=round(c, 4), mdd=round(d, 3), ratio=round(c / d, 3))
S = {"S&P 500": tr, "Gold": g, "Bitcoin": btc}
wins = [("seit 2014-09", "2014-09"), ("10 Jahre", ym(last, 120)), ("5 Jahre", ym(last, 60))]
fen = []
for lab, st0 in wins:
    row = dict(label=lab, start=st0); row.update({k: stats(s, st0) for k, s in S.items()})
    row["btc_best"] = row["Bitcoin"]["cagr"] > max(row["S&P 500"]["cagr"], row["Gold"]["cagr"]); fen.append(row)
def rets(s, a, b):
    ms = [m for m in sorted(s) if a <= m <= b]; return {ms[i]: s[ms[i]] / s[ms[i - 1]] - 1 for i in range(1, len(ms))}
def beta_corr(a, b, start):
    ra, rb = rets(a, start, last), rets(b, start, last); ms = sorted(set(ra) & set(rb)); x = [rb[m] for m in ms]; y = [ra[m] for m in ms]
    mx, my = st.mean(x), st.mean(y); cov = sum((p - mx) * (q - my) for p, q in zip(x, y)); vx = sum((p - mx) ** 2 for p in x); vy = sum((q - my) ** 2 for q in y)
    return cov / vx, cov / (vx * vy) ** .5, ms, ra, rb
def crisis(a, start):
    _, _, ms, ra, rb = beta_corr(a, tr, start); worst = sorted(ms, key=lambda m: rb[m])[:max(1, len(ms) // 10)]
    return round(st.mean(ra[m] for m in worst), 4), round(st.mean(rb[m] for m in worst), 4), len(worst)
rows = []
for name, s, start in (("Gold", g, "1971-08"), ("Gold", g, "2014-09"), ("Bitcoin", btc, "2014-09")):
    b, c, ms, _, _ = beta_corr(s, tr, start); cm, sm, nw = crisis(s, start)
    rows.append(dict(name=name, start=start, n=len(ms), beta=round(b, 2), corr=round(c, 2), diversifies=c < .5, crisis=cm, sp_crisis=sm, n_worst=nw, protects=cm > 0))
yrs = []
for y in range(2015, int(last[:4])):
    a, z = "%d-12" % (y - 1), "%d-12" % y
    if a in btc and z in btc and a in tr and a in g:
        yrs.append(dict(y=y, btc=round(btc[z] / btc[a] - 1, 3), sp=round(tr[z] / tr[a] - 1, 3), gold=round(g[z] / g[a] - 1, 3)))
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
