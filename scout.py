"""Talent-Scouting, Schritt 1 (nur Information): Wie sahen die heutigen Kronjuwelen in jungen Jahren aus?
Für jedes Mitglied: frühester Tag (wöchentlich ab 2010), an dem die Kurs-Regeln alle erfüllt waren
(10 J. Rendite >= 17 %, unter Wasser <= 20 %, Schwankung <= 30 %, Beta <= 1,15 in Euro gegen S&P 500, 5 J. Wochenkurse).
Marge/Schulden historisch nicht verfügbar, daher hier nicht geprüft.
Dann Profil zu mehreren früheren Zeitpunkten: 5 J. Rendite, Schwankung, Zeit unter Wasser, Beta, größter Rückgang. Nur Ausgabe."""
import csv, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp
mem = json.load(open("data/elite_members.json")); meta = json.load(open("data/elite_meta.json"))
fx = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
def get(s):
    for k in range(3):
        try: return fp.yahoo(s)
        except Exception: time.sleep(3)
spx = get("SPY")
def weekly(s, a, b):
    wk = {}
    for d in sorted(s):
        if a <= d <= b: wk[str(np.datetime64(d, "W"))] = (d, s[d])
    return [v for k, v in sorted(wk.items())]
def yrs_back(d, n): return f"{int(d[:4]) - n}{d[4:]}"
def prof(s, cur, d, n):
    w = weekly(s, yrs_back(d, n), d)
    if len(w) < n * 50: return None
    p = np.array([x[1] for x in w], float)
    dd = 1 - p / np.maximum.accumulate(p); r = np.diff(np.log(p))
    yr = (np.datetime64(w[-1][0]) - np.datetime64(w[0][0])).astype(int) / 365.25
    # Beta 5 J. in Euro gegen S&P 500 in Euro
    wb = weekly(s, yrs_back(d, 5), d); ws = dict(weekly(spx, yrs_back(d, 5), d))
    fxl = lambda dd_: next((fx[x] for x in sorted(fx, reverse=True) if x <= dd_), None)
    pairs = [(v / (fxl(dt) if cur == "USD" else 1), ws[dt] / fxl(dt)) for dt, v in wb if dt in ws]
    beta = None
    if len(pairs) > 200:
        a = np.diff(np.log([x[0] for x in pairs])); m = np.diff(np.log([x[1] for x in pairs])); beta = float(np.cov(a, m)[0, 1] / m.var(ddof=1))
    return dict(cagr=float((p[-1] / p[0]) ** (1 / yr) - 1), uw=float((dd > .2).mean()), vol=float(r.std(ddof=1) * np.sqrt(52)), mdd=float(dd.max()), beta=beta)
out = {}
for k in mem:
    s = get(k); time.sleep(0.5)
    if not s: continue
    cur = meta.get(k, {}).get("cur", "USD")
    first = None; d = "2010-01-01"; days = sorted(s)
    for d in [x for x in days if x >= "2010-01-01"][::5]:
        p10 = prof(s, cur, d, 10)
        if p10 and p10["cagr"] >= .17 and p10["uw"] <= .20 and p10["vol"] <= .30 and p10["beta"] is not None and p10["beta"] <= 1.15:
            first = d; break
    o = dict(name=meta.get(k, {}).get("name", k), first=first, ipo=days[0])
    if first:
        for lag in (0, 3, 5):
            dd_ = yrs_back(first, lag); pp = prof(s, cur, dd_, 5)
            o[f"t-{lag}"] = None if not pp else {a: round(b, 3) for a, b in pp.items() if b is not None}
    o["now5"] = {a: round(b, 3) for a, b in (prof(s, cur, days[-1], 5) or {}).items() if b is not None}
    out[k] = o; print(k, o)
print("RESULT " + json.dumps(out, ensure_ascii=False))
