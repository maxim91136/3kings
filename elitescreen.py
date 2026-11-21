"""Elite-Screening je Saison (REGELN.md 2026-11-21 "Elite als eigener Index").
Universum: S&P 500 (aktuell, Wikipedia) + Europa-Liste, ohne zyklische Branchen (data/elite_universe.json) -> gar nicht erst gerechnet.
Aufnahme-Kriterien (alle): Beta < 1,15 (5 J. täglich, Euro gegen S&P 500 in Euro), 10-J.-Rendite >= 17 % p. a. (Heimatwährung, inkl. Dividenden),
Bruttomarge >= 49 % (rund 50 %, 1 Punkt Toleranz), Nettoverschuldung/EBITDA < 2, Beta aus Wochenschlusskursen. Mitglieder: fail_out nach Puffer-Grenzen (Beta > 1,30, Rendite < 12 %, Marge < 45 %, ND/EBITDA >= 2,5). Serie = Saisons in Folge bestanden. Aufnahme ab Serie 2 (nach Bestätigung). Mitglieder werden immer vollständig gerechnet.
Läuft nur, wenn eine neue Saison begonnen hat (oder mit --force). Schreibt data/elite_screen.json."""
import csv, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp, universe, fundamentals
from elite_steady import steady
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
pst = prev.get("base_streaks", {}) if prev["season"] == n else {r["sym"]: r.get("streak", 0) for r in prev["rows"]}
rows = []
for sym, p in pool.items():
    s = get(sym); time.sleep(0.7)
    if not s: continue
    c = cagr10(s)
    m = sym in mem
    I, O = R["in"], R["out"]
    if (c is None or c < I["cagr10_min"]) and not m: continue          # zu jung oder zu schwach: keine weiteren Abrufe
    e = eur(s, p["cur"]); b = None if not e else beta(e)
    if (b is None or b >= I["beta_max"]) and not m: continue
    f = fundamentals.fund(sym); time.sleep(0.7)
    uw, vol = steady(s)
    def miss(L, strict):
        return [k for k, bad in (("beta", b is None or (b >= L["beta_max"] if strict else b > L["beta_max"])), ("cagr10", c is None or c < L["cagr10_min"]),
                ("margin", f["margin"] is None or f["margin"] < L["margin_min"]), ("debt", f["nd_ebitda"] is None or f["nd_ebitda"] >= L["nd_ebitda_max"]),
                ("uw", uw is None or uw > L["uw_max"]), ("vol", vol is None or vol > L["vol_max"])) if bad]
    why = miss(I, True); ok = not why; out_why = miss(O, False)
    rows.append(dict(p, beta=None if b is None else round(b, 2), cagr10=None if c is None else round(c, 4), margin=None if f["margin"] is None else round(f["margin"], 3),
                     nd_ebitda=None if f["nd_ebitda"] is None else round(f["nd_ebitda"], 2), uw=None if uw is None else round(uw, 3), vol=None if vol is None else round(vol, 3), passed=ok, why=why, fail_out=bool(out_why), out_why=out_why, streak=(pst.get(sym, 0) + 1) if ok else 0, member=m))
for k in mem:  # Mitglied ohne Kurse: gilt als durchgefallen
    if not any(r["sym"] == k for r in rows): rows.append(dict(sym=k, name=k, cur="", branch="", branch_en="", beta=None, cagr10=None, margin=None, nd_ebitda=None, passed=False, why=["data"], fail_out=True, out_why=["data"], streak=0, member=True))
rows.sort(key=lambda r: (-r["passed"], -(r["cagr10"] or -9)))
last = sorted(spy)[-1]
out = dict(season=n, date=last, n_pool=len(pool), n_cyclic=skipped, rows=rows, base_streaks=pst,
           bank=[r["sym"] for r in rows if r["passed"] and r["streak"] >= R["streak_in"] and not r["member"]])
json.dump(out, open("data/elite_screen.json", "w"), ensure_ascii=False, indent=1)
print(f"Saison {n}, Stand {last}: {sum(r['passed'] for r in rows)} bestehen alles, Bank: {out['bank']}")
for r in rows[:40]: print(f"  {r['sym']:10s} {r['name'][:26]:26s} Beta {r['beta']} 10J {r['cagr10']} Marge {r['margin']} ND/EBITDA {r['nd_ebitda']} {'OK' if r['passed'] else '-'} Serie {r['streak']}{' (Elite)' if r['member'] else ''}")
