"""Elite-Screening je Saison (REGELN.md 2026-11-21 "Elite als eigener Index").
Universum: S&P 500 (aktuell, Wikipedia) + Europa-Liste, ohne zyklische Branchen (data/elite_universe.json) -> gar nicht erst gerechnet.
Aufnahme-Kriterien (alle): Beta < 1,15 (5 J. täglich, Euro gegen S&P 500 in Euro), 10-J.-Rendite >= 17 % p. a. (Heimatwährung, inkl. Dividenden),
Bruttomarge >= 49 % (rund 50 %, 1 Punkt Toleranz), Fremdkapital/Eigenkapital < 1. Serie = Saisons in Folge bestanden. Bank = Serie >= 2.
Läuft nur, wenn eine neue Saison begonnen hat (oder mit --force). Schreibt data/elite_screen.json."""
import csv, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp, universe, fundamentals
U = json.load(open("data/elite_universe.json")); R = U["rules"]
hb = json.load(open("site/heartbeat.json")); n = hb["season"]["n_seasons"]
prev = json.load(open("data/elite_screen.json")) if os.path.exists("data/elite_screen.json") else {"season": 0, "rows": []}
if n <= prev["season"] and "--force" not in sys.argv:
    print(f"Elite-Screening: keine neue Saison ({n})"); raise SystemExit(0)
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
    ds = [d for d in sorted(p) if d in spy][-1260:]
    if len(ds) < 600: return None
    a = np.array([p[d] for d in ds]); b = np.array([spy[d] for d in ds]); ra, rb = a[1:] / a[:-1] - 1, b[1:] / b[:-1] - 1
    return float(np.cov(ra, rb)[0, 1] / rb.var(ddof=1))
def cagr10(s):
    ds = sorted(s); d1 = ds[-1]; y = int(d1[:4]) - 10; t = f"{y}{d1[4:]}"
    i0 = next((d for d in ds if d >= t), None)
    if not i0 or ds[0] > t: return None
    return float((s[d1] / s[i0]) ** (365.25 / (np.datetime64(d1) - np.datetime64(i0)).astype(int)) - 1)
pst = {r["sym"]: r.get("streak", 0) for r in prev["rows"]}
rows = []
for sym, p in pool.items():
    s = get(sym); time.sleep(0.7)
    if not s: continue
    c = cagr10(s)
    if c is None or c < R["cagr10_min"]: continue          # zu jung oder zu schwach: keine weiteren Abrufe
    e = eur(s, p["cur"]); b = None if not e else beta(e)
    if b is None or b >= R["beta_max"]: continue
    f = fundamentals.fund(sym); time.sleep(0.7)
    ok = f["margin"] is not None and f["de"] is not None and f["margin"] >= R["margin_min"] and f["de"] < R["de_max"]
    rows.append(dict(p, beta=round(b, 2), cagr10=round(c, 4), margin=None if f["margin"] is None else round(f["margin"], 3),
                     de=None if f["de"] is None else round(f["de"], 2), passed=ok, streak=(pst.get(sym, 0) + 1) if ok else 0,
                     member=(sym in mem)))
rows.sort(key=lambda r: (-r["passed"], -r["cagr10"]))
last = sorted(spy)[-1]
out = dict(season=n, date=last, n_pool=len(pool), n_cyclic=skipped, rows=rows,
           bank=[r["sym"] for r in rows if r["passed"] and r["streak"] >= R["streak_bank"] and not r["member"]])
json.dump(out, open("data/elite_screen.json", "w"), ensure_ascii=False, indent=1)
print(f"Saison {n}, Stand {last}: {sum(r['passed'] for r in rows)} bestehen alles, Bank: {out['bank']}")
for r in rows[:40]: print(f"  {r['sym']:10s} {r['name'][:26]:26s} Beta {r['beta']:.2f} 10J {r['cagr10']*100:5.1f} % Marge {r['margin']} FK/EK {r['de']} {'OK' if r['passed'] else '-'} Serie {r['streak']}{' (Elite)' if r['member'] else ''}")
