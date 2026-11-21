"""Einmalige Auswertung: Kronjuwelen-Regeln mit 5-Jahres- statt 10-Jahres-Rendite (nur Ausgabe, schreibt nichts)."""
import csv, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp, universe, fundamentals
U = json.load(open("data/elite_universe.json")); R = U["rules"]
hb = json.load(open("site/heartbeat.json")); n = hb["season"]["n_seasons"]
prev = json.load(open("data/elite_screen.json")) if os.path.exists("data/elite_screen.json") else {"season": 0, "rows": []}
mem = json.load(open("data/elite_members.json"))
pool, skipped = {}, 0
for r in universe.sp500():
    if r["sector"] in U["cyclic_sectors"] or r["sub"] in U["cyclic_subs"]: skipped += 1; continue
    pool[r["sym"]] = dict(sym=r["sym"], name=r["name"], cur="USD", branch=r["sub"], branch_en=r["sub"])
for sym, nm, cur, cyc, br, br_en in U["extra"]:
    if cyc: skipped += 1; continue
    pool[sym] = dict(sym=sym, name=nm, cur=cur, branch=br, branch_en=br_en)
print(f"Universum: {len(pool)} gerechnet, {skipped} zyklisch ausgelassen")
def get(sym):
    for i in range(3):
        try:
            d = fp.yahoo(sym)
            if len(d) > 300: return d
        except Exception as e: print(sym, "Fehler", e)
        time.sleep(5 * (i + 1))
    return None
fxu = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
FX = {"USD": {d: 1 / v for d, v in fxu.items()}}
for c in {p["cur"] for p in pool.values()} - {"USD", "EUR"}:
    FX[c] = get(f"{c}EUR=X"); time.sleep(1)
def eur(s, c):
    if c == "EUR": return s
    out, last, r = {}, None, FX.get(c)
    if not r: return None
    for d in sorted(s):
        last = r.get(d, last)
        if last: out[d] = s[d] * last * (0.01 if c == "GBP" else 1)
    return out
spy = eur(get("SPY"), "USD")
def beta(p):
    """Beta aus Wochenschlusskursen (letzter Handelstag je Kalenderwoche), 5 Jahre = 260 Wochen, beides in Euro (REGELN 2026-11-21)."""
    wk = {}
    for d in sorted(p):
        if d in spy: wk[np.datetime64(d, "W")] = d
    ds = list(wk.values())[-261:]
    if len(ds) < 120: return None
    a = np.array([p[d] for d in ds]); b = np.array([spy[d] for d in ds]); ra, rb = a[1:] / a[:-1] - 1, b[1:] / b[:-1] - 1
    return float(np.cov(ra, rb)[0, 1] / rb.var(ddof=1))
def cagr10(s):
    ds = sorted(s); d1 = ds[-1]; y = int(d1[:4]) - 10; t = f"{y}{d1[4:]}"
    i0 = next((d for d in ds if d >= t), None)
    if not i0 or ds[0] > t: return None
    return float((s[d1] / s[i0]) ** (365.25 / (np.datetime64(d1) - np.datetime64(i0)).astype(int)) - 1)

def cagrN(s, n):
    ds = sorted(s); d1 = ds[-1]; t = f"{int(d1[:4]) - n}{d1[4:]}"
    i0 = next((d for d in ds if d >= t), None)
    if not i0 or ds[0] > t: return None
    return float((s[d1] / s[i0]) ** (365.25 / (np.datetime64(d1) - np.datetime64(i0)).astype(int)) - 1)
I = R["in"]; out = []
for sym, p in pool.items():
    s = get(sym); time.sleep(0.5)
    if not s: continue
    c5, c10 = cagrN(s, 5), cagrN(s, 10)
    watch = sym in ("AAPL", "NVDA") or sym in mem
    if (c5 is None or c5 < I["cagr10_min"]) and not watch: continue
    e = eur(s, p["cur"]); b = None if not e else beta(e)
    if (b is None or b >= I["beta_max"]) and not watch: continue
    f = fundamentals.fund(sym); time.sleep(0.5)
    why = [k for k, bad in (("beta", b is None or b >= I["beta_max"]), ("rendite5", c5 is None or c5 < I["cagr10_min"]),
           ("marge", f["margin"] is None or f["margin"] < I["margin_min"]), ("schulden", f["nd_ebitda"] is None or f["nd_ebitda"] >= I["nd_ebitda_max"])) if bad]
    out.append(dict(sym=sym, name=p["name"], branch=p["branch"], beta=None if b is None else round(b, 2), c5=None if c5 is None else round(c5, 3),
                    c10=None if c10 is None else round(c10, 3), margin=f["margin"] and round(f["margin"], 3), nd=f["nd_ebitda"] and round(f["nd_ebitda"], 2), ok=not why, why=why, member=sym in mem))
out.sort(key=lambda r: (-r["ok"], -(r["c5"] or -9)))
print("RESULT " + json.dumps(out, ensure_ascii=False))
