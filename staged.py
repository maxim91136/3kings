"""Studie 'Einstieg in Stufen' (Regeln vorab in REGELN.md festgelegt). Aendert den Heartbeat NICHT. python3 staged.py"""
import csv, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "core"))
import lab

def load(path, col):
    r = list(csv.DictReader(open(path)))
    return [x["date"] for x in r], np.array([float(x[col]) for x in r])

def rules(p):
    s50, s100, s200 = lab.sma(p, 50), lab.sma(p, 100), lab.sma(p, 200)
    ab = lambda m: np.where(np.isfinite(m) & (p > m), 1.0, 0.0)
    hi = np.array([p[max(0, t - 251): t + 1].max() for t in range(len(p))])
    dd = p / hi - 1
    deep = np.zeros(len(p)); deep_flag = False
    for t in range(len(p)):                                 # "tief" = seit dem letzten Kurs ueber SMA200 war der Rueckgang >= 20 %
        if np.isfinite(s200[t]) and p[t] > s200[t]: deep_flag = False
        elif dd[t] <= -0.20: deep_flag = True
        deep[t] = 1.0 if deep_flag else 0.0
    r0 = ab(s200)
    return {"R0 Basis SMA200": r0,
            "R1 Zwei Stufen": 0.5 * ab(s50) + 0.5 * ab(s200),
            "R2 Drei Stufen": (ab(s50) + ab(s100) + ab(s200)) / 3,
            "R3 Tief-Stufe": np.where(r0 > 0, 1.0, 0.5 * ab(s50) * deep)}

def evaluate(title, dates, p, cost, eras, need):
    R = lab.returns(p.reshape(-1, 1))[:, 0]
    W = rules(p); N = {k: lab.backtest(w, R, cost) for k, w in W.items()}
    print(f"\n=== {title}: {dates[0]} .. {dates[-1]} ===")
    print(f"{'Epoche':14s}" + "".join(f"{k[:2]:>26s}" for k in W)); print(f"{'':14s}" + "".join(f"{'Rend/J Rueckg Sharpe':>26s}" for _ in W))
    sh = {k: [] for k in W}; res = {}
    for name, lo, hi in eras + [("ALLES", eras[0][1], eras[-1][2])]:
        idx = [i for i, x in enumerate(dates) if lo <= x <= hi and i >= 200]
        s, e = idx[0], idx[-1] + 1; line = f"{name:14s}"
        for k in W:
            m = lab.metrics(N[k][s:e], W[k][s:e]); line += f"{m['cagr']*100:9.1f}%{m['mdd']*100:6.0f}%{m['sharpe']:8.2f}  "
            if name != "ALLES": sh[k].append(m["sharpe"])
            res[k, name] = m
        print(line)
    print("Verdikt gegen R0:")
    out = {}
    for k in list(W)[1:]:
        wins = sum(a >= b for a, b in zip(sh[k], sh["R0 Basis SMA200"]))
        dS = res[k, "ALLES"]["sharpe"] - res["R0 Basis SMA200", "ALLES"]["sharpe"]
        dM = (res[k, "ALLES"]["mdd"] - res["R0 Basis SMA200", "ALLES"]["mdd"]) * 100
        crisis = [(res[k, n]["mdd"] - res["R0 Basis SMA200", n]["mdd"]) * 100 for n in ("1973-1982", "2000-2009") if (k, n) in res]
        ok = wins >= need and dS >= 0.03 and dM <= 3 and all(c <= 5 for c in crisis)
        out[k] = ok
        print(f"  {k}: Sharpe-Epochen besser/gleich {wins}/{len(sh[k])} (noetig {need}), Sharpe gesamt {dS:+.2f}, Rueckgang gesamt {dM:+.1f} Pkt" + (f", Krisen {crisis}" if crisis else "") + f"  -> {'ERFUELLT' if ok else 'nicht erfuellt'}")
    return out

d, p = load("data/spx_long.csv", "SPX")
d, p = [x for x in d if x >= "1928-01-01"], p[[i for i, x in enumerate(load('data/spx_long.csv','SPX')[0]) if x >= "1928-01-01"]]
eras = [("1930-1949", "1930-01-01", "1949-12-31"), ("1950-1972", "1950-01-01", "1972-12-31"), ("1973-1982", "1973-01-01", "1982-12-31"),
        ("1983-1999", "1983-01-01", "1999-12-31"), ("2000-2009", "2000-01-01", "2009-12-31"), ("2010-2026", "2010-01-01", "2026-12-31")]
a = evaluate("S&P 500 (Preisindex)", d, p, 0.0005, eras, 4)
d2, p2 = load("data/btc_long.csv", "BTC")
beras = [("2011-2014", "2011-01-01", "2014-12-31"), ("2015-2018", "2015-01-01", "2018-12-31"), ("2019-2022", "2019-01-01", "2022-12-31"), ("2023-2026", "2023-01-01", "2026-12-31")]
b = evaluate("Bitcoin", d2, p2, 0.0010, beras, 3)
print("\nGesamt (S&P UND Bitcoin erfuellt):", {k: a[k] and b[k] for k in a})
