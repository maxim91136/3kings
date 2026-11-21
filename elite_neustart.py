"""Kronjuwelen-Neustart mit Dauerläufer-Regeln (REGELN 2026-11-21): Mitglied ist, wer am 27.10. UND 20.11.2026 alle Aufnahmeregeln erfüllt.
Stichtag = Beginn der laufenden Saison (letzte Saisonprüfung). Beta (Wochenkurse, 5 J., Euro) und 10-J.-Rendite zum Stichtag aus Kursen;
Marge und Nettoverschuldung/EBITDA: aktuelle Werte (Annahme: in drei Monaten praktisch unverändert).
Ohne --apply nur Ausgabe. Mit --apply: Serie 2 für Anwärter, die zum Stichtag UND heute bestehen -> Aufnahme; Verwarnungen für Mitglieder."""
import csv, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp
U = json.load(open("data/elite_universe.json")); I, O = U["rules"]["in"], U["rules"]["out"]
sc = json.load(open("data/elite_screen.json")); hb = json.load(open("site/heartbeat.json"))
spyu = {r["date"]: float(r["SPY"]) for r in csv.DictReader(open("data/prices.csv")) if r.get("SPY")}
cal = sorted(spyu); D = cal[-(hb["season"]["day_in_season"] + 1)]
fxu = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
def get(sym):
    for i in range(3):
        try: return fp.yahoo(sym)
        except Exception: time.sleep(4 * (i + 1))
FX = {"USD": {d: 1 / v for d, v in fxu.items()}}
def eur(s, c):
    if c == "EUR": return s
    if c not in FX: FX[c] = get(f"{c}EUR=X")
    out, last, r = {}, None, FX[c]
    for d in sorted(s):
        last = r.get(d, last)
        if last: out[d] = s[d] * last * (0.01 if c == "GBP" else 1)
    return out
spy = eur(spyu, "USD")
def at(s, D):  # Kurse bis Stichtag
    return {d: v for d, v in s.items() if d <= D}
def beta(p):
    wk = {}
    for d in sorted(p):
        if d in spy: wk[np.datetime64(d, "W")] = d
    ds = list(wk.values())[-261:]
    a = np.array([p[d] for d in ds]); b = np.array([spy[d] for d in ds]); ra, rb = a[1:] / a[:-1] - 1, b[1:] / b[:-1] - 1
    return float(np.cov(ra, rb)[0, 1] / rb.var(ddof=1))
def cagr10(s):
    ds = sorted(s); d1 = ds[-1]; t = f"{int(d1[:4]) - 10}{d1[4:]}"; i0 = next((d for d in ds if d >= t), None)
    return None if not i0 or ds[0] > t else float((s[d1] / s[i0]) ** (365.25 / (np.datetime64(d1) - np.datetime64(i0)).astype(int)) - 1)
from elite_steady import steady
sys.argv += []
rows = {r["sym"]: r for r in sc["rows"]}
for k in json.load(open("data/elite_members.json")):
    if k not in rows: print("fehlt im Screening:", k)
res = []
for sym, r in rows.items():
    s = get(sym); time.sleep(0.5)
    if not s: continue
    h = at(s, D); e = at(eur(s, r["cur"] or "USD"), D)
    b, c = round(beta(e), 2), cagr10(h); uw, vol = steady(s, D)
    m, nd = r["margin"], r["nd_ebitda"]
    pd = (b < I["beta_max"] and c is not None and c >= I["cagr10_min"] and m is not None and m >= I["margin_min"] and nd is not None
          and nd < I["nd_ebitda_max"] and uw is not None and uw <= I["uw_max"] and vol is not None and vol <= I["vol_max"])
    res.append(dict(sym=sym, name=r["name"], was=r["member"], pass_D=bool(pd), pass_now=r["passed"], beta_D=b, uw_D=uw and round(uw, 3), vol_D=vol and round(vol, 3)))
new = [x["sym"] for x in res if x["pass_D"] and x["pass_now"]]
old = json.load(open("data/elite_members.json"))
print("Stichtage", D, sc["date"]); print("neu:", new); print("raus:", [k for k in old if k not in new]); print("rein:", [k for k in new if k not in old])
for x in res: print(x)
json.dump(dict(D=D, rows=res), open("data/elite_neustart.json", "w"), ensure_ascii=False, indent=1)
if "--apply" in sys.argv and new:
    import elite_bank
    d = sc["date"]; meta = elite_bank.load("data/elite_meta.json", {})
    for k in new:
        if k not in meta: meta[k] = dict(name=rows[k]["name"], branch=rows[k].get("branch", ""), branch_en=rows[k].get("branch_en", ""), cur=rows[k].get("cur") or "USD")
    elite_bank.save("data/elite_meta.json", meta)
    json.dump(new, open("data/elite_members.json", "w"))
    hist = elite_bank.load("data/elite_hist.json", []); hist.append({"date": d, "members": new, "next": True}); elite_bank.save("data/elite_hist.json", hist)
    elite_bank.save("data/elite_frozen.json", {"stand": d, "rows": [dict(key=k, beta=rows[k]["beta"], cagr10=rows[k]["cagr10"]) for k in new]})
    rv = elite_bank.load("data/elite_reviews.json", {"reviews": []}); rv["strikes"] = {}; elite_bank.save("data/elite_reviews.json", rv)
    for k in new: rows[k]["member"] = True; rows[k]["streak"] = max(rows[k].get("streak", 0), 2)
    for k in old:
        if k not in new and k in rows: rows[k]["member"] = False
    sc["rows"] = list(rows.values()); sc["bank"] = []; json.dump(sc, open("data/elite_screen.json", "w"), ensure_ascii=False, indent=1)
    nm = lambda k: meta.get(k, {}).get("name", k)
    out = [k for k in old if k not in new]; inn = [k for k in new if k not in old]
    elite_bank.regeln(f"\n## {d}: Kronjuwelen-Neustart mit Dauerläufer-Regeln (automatisch nach Regel)\nPrüfungen 27.10. und 20.11.2026 nachgerechnet. Mitglieder ({len(new)}): {', '.join(nm(k) for k in new)}. Neu: {', '.join(nm(k) for k in inn) or 'keine'}. Ohne neues Geld (kein Verkauf): {', '.join(nm(k) for k in out) or 'keine'}. Wirksam ab dem nächsten Handelstag.\n",
                      f"\n## {d}: Crown Jewels restart with steady-runner rules (automatic per rule)\nReviews Oct 27 and Nov 20, 2026 recalculated. Members ({len(new)}): {', '.join(nm(k) for k in new)}. New: {', '.join(nm(k) for k in inn) or 'none'}. No new money (no sale): {', '.join(nm(k) for k in out) or 'none'}. Effective from the next trading day.\n")
    import subprocess; subprocess.run([sys.executable, "fetch_elite.py"], check=False)
