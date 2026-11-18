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
        rows.append(dict(key=k, name=names[k], cagr=round(st["cagr"], 4), mdd=round(st["mdd"], 3), sharpe=round(st["sharpe"], 2), beta=round(b, 2), corr=round(c, 2)))
    out["factor"] = dict(since=dates[0], until=dates[-1], rows=rows)

# ---------------- Elite 6 (2026-11-18: 5 aus Liste + IDEXX aus Screening)
el = load("data/elite.csv")
NAMES = {"RACE": ("Ferrari", "Luxus-Autos", 23.7), "MA": ("Mastercard", "Zahlungs-Duopol", 20.9), "V": ("Visa", "Zahlungs-Duopol", 16.9),
         "CTAS": ("Cintas", "Wiederkehrende Dienste", 25.6), "MSFT": ("Microsoft", "Cloud und KI", 25.9),
         "IDXX": ("IDEXX", "Tierarzt-Diagnostik", None)}
if el and spy:
    local, ep = {}, {}
    for k in NAMES:
        s = col(el, k)
        if len(s) > 500: local[k] = s; ep[k] = eur(s, usd=(k != "RMS"))
    spyusd = {r["date"]: float(r["SPY"]) for r in load("data/prices.csv") if r["SPY"]}
    last = max(spyusd)
    def cagr10(s, d1):
        ds = sorted(s); y, m, dd = d1.split("-"); target = f"{int(y)-10}-{m}-{dd}"
        i0 = next((d for d in ds if d >= target), None)
        if not i0 or i0 > f"{int(y)-10}-{m}-28" or d1 not in s: return None
        yrs = (np.datetime64(d1) - np.datetime64(i0)).astype(int) / 365.25
        return (s[d1] / s[i0]) ** (1 / yrs) - 1
    rows = []
    for k, (nm, br, claim) in NAMES.items():
        if k not in local: rows.append(dict(key=k, name=nm, branch=br, claim=claim, missing=True)); continue
        d1 = max(local[k]); ds = [d for d in sorted(local[k]) if d in spy and d in ep[k]][-1260:]
        b, _ = beta(ep[k], [d for d in ds if d in spy]) if len(ds) > 300 else (None, None)
        c = cagr10(local[k], d1)
        rows.append(dict(key=k, name=nm, branch=br, claim=claim, beta=None if b is None else round(b, 2), cagr10=None if c is None else round(c, 4), until=d1))
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
    # Schattenbuch ab Start
    sp_path = "data/elite_state.json"
    last_d = min(max(ep[k]) for k in ks)
    st = json.load(open(sp_path)) if os.path.exists(sp_path) else dict(start=last_d, p0={k: ep[k][last_d] for k in ks}, spy0=spy[last_d], rows=[])
    if last_d >= st["start"] and (not st["rows"] or st["rows"][-1]["date"] != last_d) and last_d in spy:
        e = float(np.mean([ep[k][last_d] / st["p0"][k] for k in ks if k in st["p0"]])); st["rows"].append(dict(date=last_d, elite=round(e, 4), spy=round(spy[last_d] / st["spy0"], 4)))
        json.dump(st, open(sp_path, "w"), indent=1)
    out["elite"] = dict(stand=fz["stand"] if fz else None, rows=rows, back=back, shadow=dict(start=st["start"], rows=st["rows"][-400:]))
json.dump(out, open("site/watch.json", "w"), ensure_ascii=False, indent=1)
print("watch.json:", ", ".join(k for k in out if k != "generated"))
if "factor" in out:
    for r in out["factor"]["rows"]: print(f"  {r['name']:26s} {r['cagr']*100:5.1f} %/J  Rueckg {r['mdd']*100:3.0f} %  Sharpe {r['sharpe']:.2f}  Beta {r['beta']:.2f}")
if "elite" in out:
    for r in out["elite"]["rows"]: print("  ", r["name"], "fehlt" if r.get("missing") else f"Beta {r['beta']}  10J {None if r['cagr10'] is None else round(r['cagr10']*100,1)} % (Liste {r['claim']})")
    print("  Rueckblick:", out["elite"]["back"])
