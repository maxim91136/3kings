"""Faktor-ETFs und Elite 9: Kennzahlen und Schattenbuch -> site/watch.json (nur Anzeige). Kriterien in REGELN.md."""
import csv, json, os
import numpy as np

def load(path):
    return list(csv.DictReader(open(path))) if os.path.exists(path) else []

fx = {r["date"]: float(r["value"]) for r in load("data/ind_EURUSD.csv")}
def eur(series, usd=True):
    """{datum: preis} -> Euro. Fehlende Wechselkurse: letzter bekannter."""
    out, last = {}, None
    for d in sorted(series):
        last = fx.get(d, last)
        if last: out[d] = series[d] / last if usd else series[d]
    return out
def col(rows, k): return {r["date"]: float(r[k]) for r in rows if r.get(k) not in ("", None)}

spy = eur({r["date"]: float(r["SPY"]) for r in load("data/prices.csv") if r["SPY"]})
def stats(p, dates):
    x = np.array([p[d] for d in dates]); r = x[1:] / x[:-1] - 1; eq = x / x[0]
    return dict(cagr=(x[-1] / x[0]) ** (252 / len(r)) - 1, mdd=float((1 - eq / np.maximum.accumulate(eq)).max()), sharpe=float(r.mean() / r.std() * 252 ** .5), vol=float(r.std() * 252 ** .5))
def beta(p, dates):
    a = np.array([p[d] for d in dates]); b = np.array([spy[d] for d in dates]); ra, rb = a[1:] / a[:-1] - 1, b[1:] / b[:-1] - 1
    return float(np.cov(ra, rb)[0, 1] / rb.var(ddof=1)), float(np.corrcoef(ra, rb)[0, 1])

out = dict(generated=None)
# ---------------- Faktor-ETFs
cand = load("data/candidates.csv")
if cand and spy:
    names = {"SPY": "S&P 500", "QUAL": "Qualität (QUAL)", "MTUM": "Momentum (MTUM)", "USMV": "Min. Schwankung (USMV)", "XLK": "Tech (XLK)", "VT": "Welt, alle Länder (VT)", "URTH": "Welt, MSCI World (URTH)"}
    names_en = {"SPY": "S&P 500", "QUAL": "Quality (QUAL)", "MTUM": "Momentum (MTUM)", "USMV": "Min. volatility (USMV)", "XLK": "Tech (XLK)", "VT": "World, all countries (VT)", "URTH": "World, MSCI World (URTH)"}
    series = {"SPY": spy}
    for k in names:
        if k != "SPY":
            s = col(cand, k)
            if s: series[k] = eur(s)
    d0 = max(min(s) for s in series.values()); d0 = max(d0, "2015-07-20")
    dates = sorted(d for d in spy if d >= d0 and all(d in s for s in series.values()))
    rows = []
    for k, s in series.items():
        st = stats(s, dates); b, c = beta(s, dates)
        rows.append(dict(key=k, name=names[k], name_en=names_en[k], cagr=round(st["cagr"], 4), mdd=round(st["mdd"], 3), sharpe=round(st["sharpe"], 2), beta=round(b, 2), corr=round(c, 2)))
    out["factor"] = dict(since=dates[0], until=dates[-1], rows=rows)

# ---------------- Elite 6 (2026-11-18: 5 aus Liste + IDEXX aus Screening)
el = load("data/elite.csv")
BR_EN = {"RACE": "Luxury cars", "MA": "Payments duopoly", "V": "Payments duopoly", "CTAS": "Recurring services", "MSFT": "Cloud and AI", "IDXX": "Veterinary diagnostics"}
NAMES = {"RACE": ("Ferrari", "Luxus-Autos", 23.7), "MA": ("Mastercard", "Zahlungs-Duopol", 20.9), "V": ("Visa", "Zahlungs-Duopol", 16.9),
         "CTAS": ("Cintas", "Wiederkehrende Dienste", 25.6), "MSFT": ("Microsoft", "Cloud und KI", 25.9),
         "IDXX": ("IDEXX", "Tierarzt-Diagnostik", None)}
if os.path.exists("data/elite_members.json"):  # Saisonprüfung/Bank (REGELN 2026-11-21): nur aktuelle Mitglieder, Nachrücker aus elite_meta.json
    _m = json.load(open("data/elite_members.json")); _meta = json.load(open("data/elite_meta.json")) if os.path.exists("data/elite_meta.json") else {}
    NAMES = {k: NAMES.get(k) or (_meta.get(k, {}).get("name", k), _meta.get(k, {}).get("branch", ""), None) for k in _m}
    for k in _m:
        if k not in BR_EN: BR_EN[k] = _meta.get(k, {}).get("branch_en", "")
if el and spy:
    local, ep = {}, {}
    for k in NAMES:
        s = col(el, k)
        if len(s) > 500: local[k] = s; ep[k] = eur(s, usd=(k != "RMS"))
    spyusd = {r["date"]: float(r["SPY"]) for r in load("data/prices.csv") if r["SPY"]}
    last = max(spyusd)
    def cagr10(s, d1, n=10):
        ds = sorted(s); y, m, dd = d1.split("-"); target = f"{int(y)-n}-{m}-{dd}"
        i0 = next((d for d in ds if d >= target), None)
        if not i0 or i0 > f"{int(y)-n}-{m}-28" or d1 not in s: return None
        yrs = (np.datetime64(d1) - np.datetime64(i0)).astype(int) / 365.25
        return (s[d1] / s[i0]) ** (1 / yrs) - 1
    rows = []
    for k, (nm, br, claim) in NAMES.items():
        if k not in local: rows.append(dict(key=k, name=nm, branch=br, branch_en=BR_EN.get(k, br), claim=claim, missing=True)); continue
        d1 = max(local[k]); ds = [d for d in sorted(local[k]) if d in spy and d in ep[k]][-1260:]
        b, _ = beta(ep[k], [d for d in ds if d in spy]) if len(ds) > 300 else (None, None)
        c = cagr10(local[k], d1); c5 = cagr10(local[k], d1, 5)
        rows.append(dict(key=k, name=nm, branch=br, branch_en=BR_EN.get(k, br), claim=claim, beta=None if b is None else round(b, 2), cagr10=None if c is None else round(c, 4), cagr5=None if c5 is None else round(c5, 4), until=d1, dd=round(1 - local[k][d1] / max(local[k].values()), 3)))
    fz = json.load(open("data/elite_frozen.json")) if os.path.exists("data/elite_frozen.json") else None
    if fz:  # Aufnahmewerte vom Stichtag, eingefroren
        fm = {r["key"]: r for r in fz["rows"]}
        for r in rows:
            if r["key"] in fm: r["beta"], r["cagr10"] = fm[r["key"]]["beta"], fm[r["key"]]["cagr10"]
    # Rueckblick (geschoent!): gleich gewichtet, taeglich, letzte 10 Jahre in Euro
    ks = [k for k in NAMES if k in ep]
    common = sorted(set.intersection(*[set(ep[k]) for k in ks]) & set(spy))
    cut = [d for d in common if d >= f"{int(common[-1][:4])-10}{common[-1][4:]}"]
    back = None
    if len(cut) > 1500:
        eq = {d: 0.0 for d in cut}; arr = np.array([[ep[k][d] for k in ks] for d in cut]); r = (arr[1:] / arr[:-1] - 1).mean(axis=1)
        idx = np.r_[1.0, np.cumprod(1 + r)]; sp = np.array([spy[d] for d in cut]); sidx = sp / sp[0]
        yrs = len(r) / 252
        back = dict(since=cut[0], until=cut[-1], elite=dict(cagr=round(idx[-1] ** (1 / yrs) - 1, 4), mdd=round(float((1 - idx / np.maximum.accumulate(idx)).max()), 3)),
                    spy=dict(cagr=round(sidx[-1] ** (1 / yrs) - 1, 4), mdd=round(float((1 - sidx / np.maximum.accumulate(sidx)).max()), 3)))
    # Änderungen mit "next": gelten erst ab dem nächsten Handelstag (Umsetzung zum Schlusskurs des Folgetags, REGELN 2026-11-21)
    # Schattenbuch als Sparplan-Index (REGELN 2026-11-21): monatlich gleicher Betrag, gleich verteilt auf die aktuellen Mitglieder, nie verkaufen
    hist = json.load(open("data/elite_hist.json")) if os.path.exists("data/elite_hist.json") else [dict(date="2026-11-17", members=list(NAMES))]
    held = list(dict.fromkeys(x for e in hist for x in e["members"]))
    pe = {}
    for k in held:
        sk_ = col(el, k)
        if sk_: pe[k] = eur(sk_, usd=True)
    start = hist[0]["date"]; sdays = [d for d in sorted(spy) if d >= start]
    units, su, paid, prow, lastp, month = {}, 0.0, 0.0, [], {}, None
    for d in sdays:
        for k in pe:
            if d in pe[k]: lastp[k] = pe[k][d]
        mem_d = [e for e in hist if (e["date"] < d if e.get("next") else e["date"] <= d)][-1]["members"]; mem_d = [k for k in mem_d if k in lastp]
        if d[:7] != month and mem_d:
            month = d[:7]; paid += 100
            for k in mem_d: units[k] = units.get(k, 0) + (100 / len(mem_d)) / lastp[k]
            su += 100 / spy[d]
        if paid: prow.append(dict(date=d, elite=round(sum(u * lastp[k] for k, u in units.items()) / paid, 4), spy=round(su * spy[d] / paid, 4), paid=paid))
    # Einmal-Schattenbuch daneben: Start 1,00, gleich gewichtet, umgeschichtet nur an Änderungstagen der Chronik
    lrows, lv, seg0, lp0 = [], 1.0, None, {}
    for d in sdays:
        mem_d = [k for k in [e for e in hist if (e["date"] < d if e.get("next") else e["date"] <= d)][-1]["members"] if k in pe and d in pe[k]]
        if not mem_d: continue
        if seg0 is None or mem_d != seg0:
            if seg0 is not None: lv *= float(np.mean([pe[k][d] / lp0[k] for k in seg0]))
            seg0 = mem_d; lp0 = {k: pe[k][d] for k in mem_d}
        v = lv * float(np.mean([pe[k][d] / lp0[k] for k in seg0]))
        lrows.append(dict(date=d, elite=round(v, 4), spy=round(spy[d] / spy[sdays[0]], 4)))
    st = dict(start=start, rows=prow, lump=lrows)
    out["elite"] = dict(stand=fz["stand"] if fz else None, n=len(NAMES), check=json.load(open("site/elite_check.json")) if os.path.exists("site/elite_check.json") else None, reviews=json.load(open("data/elite_reviews.json"))["reviews"] if os.path.exists("data/elite_reviews.json") else [], strikes=json.load(open("data/elite_reviews.json")).get("strikes", {}) if os.path.exists("data/elite_reviews.json") else {}, screen=(lambda sc: dict(date=sc["date"], season=sc["season"], n_pool=sc["n_pool"], n_cyclic=sc["n_cyclic"], bank=sc["bank"], rows=[dict(sym=r["sym"], name=r["name"], beta=r["beta"], cagr10=r["cagr10"], margin=r["margin"], nd=r.get("nd_ebitda"), streak=r["streak"]) for r in sc["rows"] if r["passed"] and not r["member"]][:15]))(json.load(open("data/elite_screen.json"))) if os.path.exists("data/elite_screen.json") else None, pending=(lambda c: dict(sym=c["sym"], name=c["row"]["name"], created=c["created"]) if c and not c.get("test") else None)(json.load(open("data/elite_pending.json")).get("current")) if os.path.exists("data/elite_pending.json") else None, rows=rows, back=back, shadow=dict(start=st["start"], rows=st["rows"], lump=st["lump"]))
json.dump(out, open("site/watch.json", "w"), ensure_ascii=False, indent=1)
print("watch.json:", ", ".join(k for k in out if k != "generated"))
if "factor" in out:
    for r in out["factor"]["rows"]: print(f"  {r['name']:26s} {r['cagr']*100:5.1f} %/J  Rueckg {r['mdd']*100:3.0f} %  Sharpe {r['sharpe']:.2f}  Beta {r['beta']:.2f}")
if "elite" in out:
    for r in out["elite"]["rows"]: print("  ", r["name"], "fehlt" if r.get("missing") else f"Beta {r['beta']}  10J {None if r['cagr10'] is None else round(r['cagr10']*100,1)} % (Liste {r['claim']})")
    print("  Rueckblick:", out["elite"]["back"])
