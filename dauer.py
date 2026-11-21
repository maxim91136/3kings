"""Untersuchung (keine Regel): Welche Messung erkennt Dauerläufer?
Messungen über 10 Jahre Wochenkurse (Heimatwährung, inkl. Dividenden):
  r2     Gleichmäßigkeit: R² des linearen Trends der log-Kurse
  vol    eigene Schwankung pro Jahr (gesamt, nicht nur Markt-Anteil wie Beta)
  mdd    größter Rückgang vom Hoch
  uw     Anteil der Wochen mehr als 20 % unter dem bisherigen Hoch
  roll3  schlechteste rollende 3-Jahres-Rendite p. a.
  pos1   Anteil positiver rollender 1-Jahres-Renditen
  half   schwächere der beiden 5-Jahres-Hälften (Rendite p. a.)
Test: Messung im Fenster davor -> Ergebnis im 10-Jahres-Fenster danach (2006-16 -> 2016-26 und 2001-11 -> 2011-21).
Ziel "Dauerläufer danach": beide Hälften mind. 8 % p. a. UND größter Rückgang unter 40 %.
Nur Aktien mit mind. 12 % p. a. im Fenster davor (Kandidaten-Nähe). Überlebensbias: heutiges Universum."""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp, universe
U = json.load(open("data/elite_universe.json"))
pool = {r["sym"]: r["name"] for r in universe.sp500() if r["sector"] not in U["cyclic_sectors"]}
for sym, nm, cur, cyc, br, br_en in U["extra"]:
    if not cyc: pool[sym] = nm
mem = json.load(open("data/elite_members.json"))
def weekly(s):
    wk = {}
    for d in sorted(s): wk[str(np.datetime64(d, "W"))] = (d, s[d])
    return [v for k, v in sorted(wk.items())]
def cagr(a, b, yrs): return (b / a) ** (1 / yrs) - 1
def measures(w):
    p = np.array([x[1] for x in w]); n = len(p)
    if n < 500: return None
    lp = np.log(p); t = np.arange(n)
    k, c0 = np.polyfit(t, lp, 1); r2 = 1 - ((lp - (k * t + c0)) ** 2).sum() / ((lp - lp.mean()) ** 2).sum()
    r = np.diff(lp); vol = r.std(ddof=1) * np.sqrt(52)
    hi = np.maximum.accumulate(p); dd = 1 - p / hi
    roll3 = min(cagr(p[i], p[i + 156], 3) for i in range(0, n - 156, 4))
    pos1 = np.mean([p[i + 52] > p[i] for i in range(0, n - 52)])
    h = n // 2; half = min(cagr(p[0], p[h], h / 52), cagr(p[h], p[-1], (n - h) / 52))
    return dict(cagr=cagr(p[0], p[-1], n / 52), r2=r2 if k > 0 else 0.0, vol=vol, mdd=dd.max(), uw=float((dd > .2).mean()),
                roll3=roll3, pos1=float(pos1), half=half)
def window(w, a, b): return [x for x in w if a <= x[0] < b]
data = {}
for sym in pool:
    try: s = fp.yahoo(sym)
    except Exception: s = None
    time.sleep(0.4)
    if s and len(s) > 2000: data[sym] = weekly(s)
print("Kurse:", len(data), "von", len(pool))
keys = ["r2", "vol", "mdd", "uw", "roll3", "pos1", "half"]
good_dir = dict(r2=1, vol=-1, mdd=-1, uw=-1, roll3=1, pos1=1, half=1)
def spearman(x, y):
    rx, ry = np.argsort(np.argsort(x)), np.argsort(np.argsort(y)); return float(np.corrcoef(rx, ry)[0, 1])
res = {}
for (a, m, b) in (("2001-11-20", "2011-11-20", "2021-11-20"), ("2006-11-20", "2016-11-20", "2026-11-20")):
    rows = []
    for sym, w in data.items():
        pre, post = measures(window(w, a, m)), measures(window(w, m, b))
        if not pre or not post or pre["cagr"] < .12: continue
        ok = post["half"] >= .08 and post["mdd"] < .40
        rows.append((sym, pre, post, ok))
    out = dict(n=len(rows), base=round(np.mean([r[3] for r in rows]), 3), cagr_after=round(float(np.mean([r[2]["cagr"] for r in rows])), 4), m={})
    for k in keys:
        x = [r[1][k] * good_dir[k] for r in rows]
        top = sorted(rows, key=lambda r: -r[1][k] * good_dir[k])[: len(rows) // 3]; bot = sorted(rows, key=lambda r: r[1][k] * good_dir[k])[: len(rows) // 3]
        out["m"][k] = dict(rho_ok=round(spearman(x, [r[3] for r in rows]), 3), rho_cagr=round(spearman(x, [r[2]["cagr"] for r in rows]), 3),
                           rho_mdd=round(spearman(x, [-r[2]["mdd"] for r in rows]), 3),
                           top_ok=round(np.mean([r[3] for r in top]), 3), bot_ok=round(np.mean([r[3] for r in bot]), 3),
                           top_cagr=round(float(np.mean([r[2]["cagr"] for r in top])), 4), bot_cagr=round(float(np.mean([r[2]["cagr"] for r in bot])), 4))
    res[f"{a[:4]}-{m[:4]}->{b[:4]}"] = out
now = {}
for sym in mem:
    if sym in data:
        v = measures(window(data[sym], "2016-11-20", "2026-12-31"))
        if v: now[sym] = {k: round(float(x), 3) for k, x in v.items()}
for sym in ("MA", "AAPL", "ISRG", "COST", "NVDA"):
    if sym in data and sym not in now:
        v = measures(window(data[sym], "2016-11-20", "2026-12-31")); now[sym + "*"] = {k: round(float(x), 3) for k, x in v.items()} if v else None
print("RESULT " + json.dumps(dict(test=res, now=now), ensure_ascii=False))
