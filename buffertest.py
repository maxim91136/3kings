"""Puffer-Test Kronjuwelen (Regel: REGELN.md 2026-11-21). Nur Ausgabe."""
import csv, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp, universe
U = json.load(open("data/elite_universe.json"))
pool = {}
for r in universe.sp500():
    if r["sector"] in U["cyclic_sectors"] or r["sub"] in U["cyclic_subs"]: continue
    pool[r["sym"]] = "USD"
for sym, _nm, cur, cyc, *_ in U["extra"]:
    if not cyc: pool[sym] = cur
def get(sym):
    for i in range(3):
        try:
            d = fp.yahoo(sym)
            if len(d) > 300: return d
        except Exception: pass
        time.sleep(4 * (i + 1))
    return None
fxu = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
FX = {"USD": {d: 1 / v for d, v in fxu.items()}}
for c in set(pool.values()) - {"USD", "EUR"}: FX[c] = get(f"{c}EUR=X")
spy_usd = get("SPY")
cal = sorted(d for d in spy_usd if d >= "2005-01-01" and d in fxu or (d >= "2005-01-01" and any(k <= d for k in fxu)))
def eur(s, c):
    if c == "EUR": return s
    out, last, r = {}, None, FX.get(c)
    for d in sorted(s):
        last = r.get(d, last)
        if last: out[d] = s[d] * last * (0.01 if c == "GBP" else 1)
    return out
def ffill(s):  # auf den S&P-Kalender
    out, last = {}, None
    for d in cal:
        if d in s: last = s[d]
        if last is not None: out[d] = last
    return out
spy = ffill(eur(spy_usd, "USD"))
H, E = {}, {}
for sym, cur in pool.items():
    s = get(sym); time.sleep(0.5)
    if not s or min(s) > "2016-12-31": continue
    H[sym] = ffill(s); E[sym] = ffill(eur(s, cur))
print("Firmen mit Daten:", len(H))
days = [d for d in cal if d >= "2016-01-04"]; revs = days[::63]
wk = {}
for d in cal: wk[np.datetime64(d, "W")] = d
wdays = list(wk.values())
def stats(sym, d):
    h = H[sym]; t = f"{int(d[:4]) - 10}{d[4:]}"
    i0 = next((x for x in cal if x >= t), None)
    if i0 is None or i0 not in h or d not in h: return None, None
    c = (h[d] / h[i0]) ** (365.25 / (np.datetime64(d) - np.datetime64(i0)).astype(int)) - 1
    ws = [x for x in wdays if x <= d][-261:]
    if ws[0] not in E[sym]: return None, c
    a = np.array([E[sym][x] for x in ws]); b = np.array([spy[x] for x in ws]); ra, rb = a[1:] / a[:-1] - 1, b[1:] / b[:-1] - 1
    return float(np.cov(ra, rb)[0, 1] / rb.var(ddof=1)), float(c)
ST = {d: {s: stats(s, d) for s in H} for d in revs}
print("Prüfungen:", len(revs), revs[0], "bis", revs[-1])
VAR = {"ohne": (1.15, 0.17), "schmal": (1.20, 0.15), "mittel": (1.25, 0.14), "breit": (1.30, 0.12)}
def irr(flows, final, n_months):
    lo, hi = -0.5, 1.0
    for _ in range(80):
        m = (lo + hi) / 2; v = sum(f * (1 + m) ** ((n_months - i) / 12) for i, f in flows)
        (lo, hi) = (m, hi) if v < final else (lo, m)
    return m
res = {}
for name, (bo, co) in VAR.items():
    mem, sin, sout = set(), {}, {}; hist = []; changes = 0; returns = 0; left = {}
    for qi, d in enumerate(revs):
        add, rem = [], []
        for s in H:
            b, c = ST[d][s]
            pin = b is not None and c is not None and b < 1.15 and c >= 0.17
            pout = b is None or c is None or b > bo or c < co
            if s in mem:
                sout[s] = sout.get(s, 0) + 1 if pout else 0
                if sout[s] >= 2: rem.append(s)
            else:
                sin[s] = sin.get(s, 0) + 1 if pin else 0
                if sin[s] >= 2: add.append(s)
        for s in rem: mem.discard(s); sout[s] = 0; left[s] = qi
        for s in add:
            if s in left and qi - left[s] <= 8: returns += 1
            mem.add(s); sin[s] = 0
        if qi >= 2: changes += len(add) + len(rem)
        hist.append((d, sorted(mem)))
    # Sparplan: monatlich 100 EUR, gleich auf aktuelle Mitglieder, nie verkaufen
    months = sorted({d[:7] for d in days}); first = {}
    for d in days: first.setdefault(d[:7], d)
    units, su, flows, last = {}, 0.0, [], days[-1]
    for i, m in enumerate(months):
        d = first[m]; cur = [h for h in hist if h[0] <= d]; cur = cur[-1][1] if cur else []
        if not cur: continue
        for s in cur: units[s] = units.get(s, 0) + (100 / len(cur)) / E[s][d]
        su += 100 / spy[d]; flows.append((i, 100))
    val = sum(u * E[s][last] for s, u in units.items()); sv = su * spy[last]; n = len(months)
    # Einmalanlage (Ergänzung 2026-11-21): Start = erste Prüfung mit Mitgliedern, gleich gewichtet, umgeschichtet nur bei Änderungen
    segs = [h for i, h in enumerate(hist) if h[1] and (i == 0 or h[1] != hist[i - 1][1])]
    lv = 1.0; t0 = segs[0][0]
    for i, (d0, m0) in enumerate(segs):
        d1 = segs[i + 1][0] if i + 1 < len(segs) else last
        lv *= float(np.mean([E[x][d1] / E[x][d0] for x in m0]))
    yrs = (np.datetime64(last) - np.datetime64(t0)).astype(int) / 365.25
    lump = dict(start=t0, cagr=round(lv ** (1 / yrs) - 1, 4), spy_cagr=round((spy[last] / spy[t0]) ** (1 / yrs) - 1, 4), rebalances=len(segs) - 1)
    res[name] = dict(changes_py=round(changes / ((len(revs) - 2) / 4), 2), returns=returns, members_end=len(hist[-1][1]), avg_members=round(np.mean([len(h[1]) for h in hist[2:]]), 1),
                     paid=100 * len(flows), value=round(val), irr=round(irr(flows, val, n), 4), spy_value=round(sv), spy_irr=round(irr(flows, sv, n), 4), lump=lump)
    print(name, res[name])
print(json.dumps(res))
