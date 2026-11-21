"""Kronjuwelen: Nachberechnung der vorigen Saisonprüfung zum Start (REGELN.md 2026-11-21).
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
res = []
for r in sc["rows"]:
    if not (r["passed"] or r["member"]): continue
    s = get(r["sym"]); time.sleep(0.5)
    if not s: continue
    h = at(s, D); e = at(eur(s, r["cur"] or "USD"), D)
    braw = beta(e); b, c = round(braw, 2), cagr10(h)
    m, nd = r["margin"], r["nd_ebitda"]
    pin = braw <= I["beta_max"] and c is not None and c >= I["cagr10_min"] and m is not None and m >= I["margin_min"] and nd is not None and nd < I["nd_ebitda_max"]
    fout = braw > O["beta_max"] or c is None or c < O["cagr10_min"] or m is None or m < O["margin_min"] or nd is None or nd >= O["nd_ebitda_max"]
    res.append(dict(sym=r["sym"], name=r["name"], member=r["member"], beta_D=b, cagr10_D=None if c is None else round(c, 4), pass_D=bool(pin), fail_out_D=bool(fout), pass_now=r["passed"], fail_out_now=r.get("fail_out", not r["passed"])))
print("Stichtag letzte Saisonprüfung:", D, "| heute:", sc["date"])
for x in res: print(f"  {x['sym']:8s} {x['name'][:24]:24s} {'MITGLIED' if x['member'] else 'Anwärter'}  Stichtag: Beta {x['beta_D']} 10J {x['cagr10_D']} -> {'besteht' if x['pass_D'] else ('klar verfehlt' if x['fail_out_D'] else 'knapp nicht')} | heute {'besteht' if x['pass_now'] else '-'}")
json.dump(dict(D=D, rows=res), open("data/elite_retro.json", "w"), ensure_ascii=False, indent=1)
if "--apply" in sys.argv:
    import elite_bank
    rv = json.load(open("data/elite_reviews.json")); sk = rv.setdefault("strikes", {})
    for x in res:
        if x["member"]: sk[x["sym"]] = (1 if x["fail_out_D"] else 0) + (1 if x["fail_out_D"] and x["fail_out_now"] else 0)
    json.dump(rv, open("data/elite_reviews.json", "w"), indent=1)
    rows = {r["sym"]: r for r in sc["rows"]}
    for x in res:
        if not x["member"] and x["pass_D"] and x["pass_now"]:
            rows[x["sym"]]["streak"] = 2; rows[x["sym"]]["member"] = True
            elite_bank.admit(rows[x["sym"]], how=os.environ.get("RETRO_HOW", f"Start: Saisonprüfungen {D} und {sc['date']} bestanden"), how_en=os.environ.get("RETRO_HOW_EN", f"start: season reviews {D} and {sc['date']} passed"), d=sc["date"])
    sc["rows"] = list(rows.values()); sc["bank"] = []
    json.dump(sc, open("data/elite_screen.json", "w"), ensure_ascii=False, indent=1)
