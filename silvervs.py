"""Silber gegen Gold und S&P 500 (REGELN 2026-11-22, Regeln vorab festgelegt). Nur Ausgabe.
Monatspreise in Dollar: Silber aus den Weltbank-Rohstoffdaten (Pink Sheet), Gold aus data/gold_long.csv (wie die Gold-Karte),
S&P 500 mit Dividenden (Shiller). Fenster: 1971-08, 1980-01, 2000-01, 2011-08."""
import csv, io, os, subprocess, sys, urllib.request
import netz
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "openpyxl"], check=False)
import openpyxl
URL = "https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx"
raw = netz.oeffne(urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read()
wb = openpyxl.load_workbook(io.BytesIO(raw), read_only=True, data_only=True)
sh_name = next(n for n in wb.sheetnames if "Monthly Prices" in n)
rows = list(wb[sh_name].iter_rows(values_only=True))
hi = next(i for i, r in enumerate(rows) if any(isinstance(c, str) and c.strip().lower() == "silver" for c in r))
col = next(j for j, c in enumerate(rows[hi]) if isinstance(c, str) and c.strip().lower() == "silver")
s = {}
for r in rows[hi + 1:]:
    k = r[0]
    if isinstance(k, str) and "M" in k and k[:4].isdigit():
        try: s[f"{k[:4]}-{k[5:7]}"] = float(r[col])
        except (TypeError, ValueError): pass
print("Silber Monate:", len(s), min(s), max(s), "letzter", s[max(s)])
g = {r[0][:7]: float(r[1]) for r in list(csv.reader(open("data/gold_long.csv")))[1:] if r[1]}
tr, lvl, prev = {}, 1.0, None
for r in csv.DictReader(open("data/shiller.csv")):
    p = float(r["SP500"] or 0); d = float(r["Dividend"] or 0)
    if p <= 0: continue
    if prev: lvl *= (p + d / 12) / prev
    tr[r["Date"][:7]] = lvl; prev = p
ms = sorted(set(tr) & set(g) & set(s)); end = ms[-1]; print("gemeinsames Ende", end)
def cg(a, x, e=None):
    e = e or end; return (x[e] / x[a]) ** (12 / (ms.index(e) - ms.index(a))) - 1
def mdd(a, x):
    pk = dd = 0
    for m in ms[ms.index(a):]:
        pk = max(pk, x[m]); dd = max(dd, 1 - x[m] / pk)
    return dd
W = ("1971-08", "1980-01", "2000-01", "2011-08"); res = {}
print("\nFenster | CAGR Silber / Gold / S&P | MDD Silber / Gold / S&P | Rendite/MDD Silber / Gold")
c2 = c3 = 0
for a in W:
    cs, cgd, cp = cg(a, s), cg(a, g), cg(a, tr); ds, dg, dp = mdd(a, s), mdd(a, g), mdd(a, tr)
    rs, rg = cs / ds, cgd / dg; c2 += cs > cgd; c3 += rs > rg
    print(a, f"| {cs*100:.1f} / {cgd*100:.1f} / {cp*100:.1f} | {ds*100:.0f} / {dg*100:.0f} / {dp*100:.0f} | {rs:.2f} / {rg:.2f}")
print(f"Regel 2 (Rendite höher): {c2} von 4 -> {'erfüllt' if c2>=3 else 'NICHT erfüllt'}")
print(f"Regel 3a (Rendite/Rückgang besser): {c3} von 4 -> {'erfüllt' if c3>=3 else 'NICHT erfüllt'}")
K = [m for m in ms if m >= "1971-08"]
def mix(w, x):
    a, b, vals = w, 1 - w, []
    for i in range(1, len(K)):
        a *= tr[K[i]] / tr[K[i - 1]]; b *= x[K[i]] / x[K[i - 1]]
        if K[i][5:] == "01": t = a + b; a, b = t * w, t * (1 - w)
        vals.append(a + b)
    pk = dd = 0
    for v in vals: pk = max(pk, v); dd = max(dd, 1 - v / pk)
    return vals[-1] ** (12 / len(vals)) - 1, dd
print("\nMischungen seit 1971 (CAGR, MDD): S&P-Anteil | Silber | Gold")
for w in (1.0, .9, .8, .7):
    ms_, mg_ = mix(w, s), mix(w, g); print(f"{int(w*100)}%", f"Silber {ms_[0]*100:.1f}/{ms_[1]*100:.0f}", f"Gold {mg_[0]*100:.1f}/{mg_[1]*100:.0f}")
ms8, mg8 = mix(.8, s), mix(.8, g); ok4 = ms8[0] > mg8[0] and ms8[1] <= mg8[1]
print(f"Regel 4 (80/20: mehr Rendite UND nicht tieferer Rückgang): {'erfüllt' if ok4 else 'NICHT erfüllt'}")
EP = [("1973–74", "1972-12", "1974-09"), ("1987", "1987-08", "1987-11"), ("2000–02", "2000-08", "2002-09"), ("2007–09", "2007-10", "2009-02"), ("2020", "2020-02", "2020-03"), ("2022", "2021-12", "2022-09")]
print("\nS&P-Abstürze: S&P / Silber / Gold"); ss = gg = n = 0
for nme, a, b in EP:
    if a in tr and a in s and b in s and a in g:
        x, y, z = tr[b] / tr[a] - 1, s[b] / s[a] - 1, g[b] / g[a] - 1; ss += y; gg += z; n += 1
        print(nme, f"{x*100:.0f}% / {y*100:.0f}% / {z*100:.0f}%")
print(f"Durchschnitt Silber {ss/n*100:.1f}% vs Gold {gg/n*100:.1f}% -> Regel 5 (Schutz): {'erfüllt' if ss>=gg else 'NICHT erfüllt'}")
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import fetch_prices as fp
    fx = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
    def eur(sym):
        d = fp.yahoo(sym); out = {}; last = None
        for k in sorted(d):
            last = fx.get(k, last)
            if last: out[k] = d[k] / last
        return out
    E = {n_: eur(t) for n_, t in (("Silber", "SI=F"), ("Gold", "GC=F"), ("S&P", "SPY"))}
    a = "2011-08-01"; d0 = lambda x: next(k for k in sorted(x) if k >= a); e1 = min(max(x) for x in E.values())
    yrs = (__import__("datetime").date.fromisoformat(e1) - __import__("datetime").date.fromisoformat(d0(E["Gold"]))).days / 365.25
    print(f"\nEuro seit {d0(E['Gold'])} bis {e1}: " + ", ".join(f"{n_} {((E[n_][e1]/E[n_][d0(E[n_])])**(1/yrs)-1)*100:.1f}%" for n_ in E))
except Exception as ex:
    print("Euro-Teil nicht möglich:", ex)
