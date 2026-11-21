"""Marktbarometer: schreibt täglich Werte und Ampelfarben nach data/barometer.csv (Vorwärtstest der Thesen).
Grenzen wie im Regelbuch, Abschnitt Marktbarometer. Nur Information."""
import csv, json, os, re
ld = lambda f: json.load(open(f)) if os.path.exists(f) else {}
A = {x["key"]: x for x in ld("site/assets.json").get("assets", [])}
I = {x["key"]: x for x in ld("site/indicators.json").get("indicators", [])}
M = ld("site/macro.json")
def num(s):
    m = re.search(r"[-−+]?\d+(?:[.,]\d+)?", str(s)); return float(m.group().replace("−", "-").replace(",", ".")) if m else None
def lv(x, a, b, inv=False):
    if x is None: return ""
    return ("g" if x <= a else "y" if x <= b else "r") if inv else ("g" if x >= a else "y" if x >= b else "r")
g = lambda d, *k: (lambda v: v)(d.get(k[0], {}).get(k[1]) if d.get(k[0]) else None)
v = dict(
    spx_d=g(A, "SPY", "chg1d"), btc_d=g(A, "BTC", "chg1d"), gold_d=g(A, "GLD", "chg1d"),
    oil_m=g(M, "oil", "chg1m"), us10y=g(M, "us10y", "value"), ecb=g(M, "ecb", "value"),
    cpi_us=g(M, "cpi_us", "value"), cpi_ez=g(M, "cpi_ez", "value"),
    fng=num(I["fng"]["value"]) if "fng" in I else None, cfng=num(I["cfng"]["value"]) if "cfng" in I else None,
    vix=num(I["vix"]["value"]) if "vix" in I else None, cape=num(I["cape"]["value"]) if "cape" in I else None,
    buffett=num(I["buffett"]["value"]) if "buffett" in I else None, curve=num(I["curve"]["value"]) if "curve" in I else None)
c = dict(spx_d=lv(v["spx_d"], 0, -.02), btc_d=lv(v["btc_d"], 0, -.05), gold_d=lv(v["gold_d"], 0, -.02),
    oil_m=lv(v["oil_m"], .05, .15, 1), us10y=lv(v["us10y"], 4, 4.75, 1), ecb=lv(v["ecb"], 2.25, 3, 1),
    cpi_us=lv(v["cpi_us"], .025, .035, 1), cpi_ez=lv(v["cpi_ez"], .025, .035, 1), fng=lv(v["fng"], 50, 25),
    cfng=lv(v["cfng"], 50, 25), vix=lv(v["vix"], 20, 30, 1), cape=lv(v["cape"], 20, 30, 1),
    buffett=lv(v["buffett"], 100, 150, 1), curve=lv(v["curve"], .5, 0))
day = (A.get("SPY") or {}).get("date") or ""
if not day: raise SystemExit("kein Datum")
f = "data/barometer.csv"; keys = list(v)
head = ["date"] + keys + [k + "_c" for k in keys] + ["n_red", "n_green"]
row = [day] + ["" if v[k] is None else v[k] for k in keys] + [c[k] for k in keys] + [sum(x == "r" for x in c.values()), sum(x == "g" for x in c.values())]
rows = list(csv.reader(open(f))) if os.path.exists(f) else [head]
rows = [r for r in rows if r and r[0] != day] if rows[0] == head else [head]
rows.append([str(x) for x in row]); rows[1:] = sorted(rows[1:])
csv.writer(open(f, "w", newline="")).writerows(rows)
print(day, "rot", row[-2], "grün", row[-1])
