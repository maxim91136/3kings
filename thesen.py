"""Rücktest der Barometer-Thesen A–D (Regelbuch, Marktbarometer). Kriterien vorab festgelegt (REGELN.md 21.11.2026).
Rendite = Kursänderung 12 Monate nach dem Tag (ohne Dividenden), verglichen mit dem Schnitt aller Tage im selben Zeitraum.
Episode = zusammenhängende Signalphase; neue Episode erst nach mindestens 60 Tagen ohne Signal. Schreibt site/thesen.json."""
import csv, json, bisect, datetime as dt
D = lambda s: dt.date.fromisoformat(s[:10])
def series(f, col=1):
    out = []
    for r in list(csv.reader(open(f)))[1:]:
        try: out.append((D(r[0]), float(r[col])))
        except (ValueError, IndexError): pass
    return sorted(out)
def fwd(ser, days=365):
    ds = [d for d, _ in ser]; res = {}
    for d, p in ser:
        i = bisect.bisect_left(ds, d + dt.timedelta(days=days))
        if i < len(ds) and (ds[i] - d).days < days + 10: res[d] = ser[i][1] / p - 1
    return res
def episodes(days, gap=60):
    n, last = 0, None
    for d in sorted(days):
        if last is None or (d - last).days > gap: n += 1
        last = d
    return n
def stat(sig, fr):
    s = [fr[d] for d in sig if d in fr]; a = list(fr.values())
    ep = episodes([d for d in sig if d in fr]); m, ma = (sum(s) / len(s) if s else None), sum(a) / len(a)
    return dict(n_days=len(s), episodes=ep, mean=round(m, 4) if m is not None else None, mean_all=round(ma, 4),
                hit=round(sum(x > 0 for x in s) / len(s), 3) if s else None, hit_all=round(sum(x > 0 for x in a) / len(a), 3),
                start=str(min(fr)), end=str(max(fr)))
out = {}
# A: VIX rot (>30) als Ersatz, da Angst und Gier Aktien erst seit 2025 vorliegt; S&P 500 täglich seit 1990
spx = series("data/spx_long.csv"); vix = dict(series("data/ind_VIXCLS.csv"))
fr = {d: r for d, r in fwd(spx).items() if d >= dt.date(1990, 1, 2)}
a = stat([d for d in fr if vix.get(d, 0) > 30], fr)
a["pass"] = a["mean"] is not None and a["mean"] >= a["mean_all"] + .03 and a["episodes"] >= 5
a["note"] = "VIX über 30 als Ersatz; Angst und Gier Aktien liegt erst seit 2025 vor"; out["A"] = a
# B, C: Shiller-Monatsdaten (S&P 500, US-Inflation, 10-J.-Zins, KGV)
sh = [r for r in csv.DictReader(open("data/shiller.csv")) if float(r["Consumer Price Index"] or 0) > 0]
cpi = {D(r["Date"]): float(r["Consumer Price Index"]) for r in sh}; yl = {D(r["Date"]): float(r["Long Interest Rate"]) for r in sh}
pe = {D(r["Date"]): float(r["PE10"]) for r in sh if float(r["PE10"] or 0) > 0}
spm = sorted((D(r["Date"]), float(r["SP500"])) for r in sh)
frm = fwd(spm, 365); yoy = {}
for d in cpi:
    p = d.replace(year=d.year - 1)
    if p in cpi: yoy[d] = cpi[d] / cpi[p] - 1
frb = {d: r for d, r in frm.items() if d >= dt.date(1900, 1, 1) and d in yoy}
b = stat([d for d in frb if yoy[d] > .035 and yl[d] > 4.75], frb)
b["pass"] = b["mean"] is not None and b["mean"] <= b["mean_all"] - .03 and b["episodes"] >= 5
b["note"] = "Monatsdaten seit 1900 (Shiller)"; out["B"] = b
vm = {}
for d, v in series("data/ind_VIXCLS.csv"): vm.setdefault(d.replace(day=1), v)
xs, ys = [], []
for d, r in frm.items():
    if d >= dt.date(1990, 1, 1) and d in yoy and d in vm and d in pe:
        xs.append((vm[d] > 30) + (pe[d] > 30) + (yoy[d] > .035) + (yl[d] > 4.75)); ys.append(r)
mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=False)); r = cov / (sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys)) ** .5
by = {k: [y for x, y in zip(xs, ys, strict=False) if x == k] for k in sorted(set(xs))}
out["C"] = dict(r=round(r, 3), n_months=len(xs), pass_=abs(r) < .1, pass__=None,
    by_red={str(k): dict(n=len(v), mean=round(sum(v) / len(v), 4)) for k, v in by.items()},
    note="Monate seit 1990, rote Kacheln aus VIX, Shiller-KGV, US-Inflation, US-Zins (die mit langer Historie)")
out["C"]["pass"] = out["C"].pop("pass_"); out["C"].pop("pass__")
# D: Angst und Gier Krypto rot (<25) und Bitcoin unter Power-Law-Mitte, täglich seit 2018
btc = series("data/btc_long.csv"); cf = dict(series("data/ind_CFNG.csv"))
mid = lambda d: 1.0117e-17 * ((d - dt.date(2009, 1, 3)).days) ** 5.82
px = dict(btc); frd = {d: r for d, r in fwd(btc).items() if d >= dt.date(2018, 2, 1)}
dd = stat([d for d in frd if cf.get(d, 99) < 25 and px[d] < mid(d)], frd)
dd["pass"] = dd["mean"] is not None and dd["mean"] >= dd["mean_all"] + .10 and dd["episodes"] >= 5
dd["note"] = "täglich seit 2018 (Angst und Gier Krypto ab Februar 2018)"; out["D"] = dd
# Einordnung der aktuellen Werte: Anteil der Zeit mit niedrigerem Wert
M = json.load(open("site/macro.json")); I = {x["key"]: x for x in json.load(open("site/indicators.json"))["indicators"]}
num = lambda s: float(str(s).split(" ")[0].replace(",", "."))
def pct(hist, v): return round(sum(x < v for x in hist) / len(hist), 3) if hist and v is not None else None
cur = dict(vix=num(I["vix"]["value"]) if "vix" in I else None, cfng=num(I["cfng"]["value"]) if "cfng" in I else None,
           us10y=(M.get("us10y") or {}).get("value"), cpi_us=(M.get("cpi_us") or {}).get("value"))
out["pct"] = dict(vix=dict(p=pct([v for _, v in series("data/ind_VIXCLS.csv")], cur["vix"]), since=1990),
    cfng=dict(p=pct([v for _, v in series("data/ind_CFNG.csv")], cur["cfng"]), since=2018),
    us10y=dict(p=pct(list(yl.values()), cur["us10y"]), since=1871),
    cpi_us=dict(p=pct(list(yoy.values()), cur["cpi_us"]), since=1872))
bl = btc[-1]
out["active"] = dict(A=bool(cur["vix"] and cur["vix"] > 30), B=bool(cur["cpi_us"] and cur["us10y"] and cur["cpi_us"] > .035 and cur["us10y"] > 4.75),
                     D=bool(cur["cfng"] is not None and cur["cfng"] < 25 and bl[1] < mid(bl[0])), btc_vs_mid=round(bl[1] / mid(bl[0]) - 1, 3))
out["date"] = str(dt.date.today())
json.dump(out, open("site/thesen.json", "w"), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False, indent=1))
