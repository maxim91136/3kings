"""Zeithorizonte, Langzeit (aendert den Heartbeat NICHT). python3 horizonlong.py
Vorab festgelegt in REGELN.md (2026-11-20). Linien SMA 50/100/150/200/300 auf S&P 500 (ab 1930, Epochen wie longtest.py)
und Bitcoin (ab 2011-07, vier Epochen); Gold nur monatlich und nur Information.
Preisindex, Cash ohne Zins, Kosten 5 bps (BTC 10 bps). Alle Ergebnisse werden gezeigt, dann das Kriterium (a)-(d) geprueft."""
import csv, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "core"))
import lab

LINES = (50, 100, 150, 200, 300)


def load(path, col):
    rows = list(csv.DictReader(open(path)))
    return [r[next(iter(r))] for r in rows], np.array([float(r[col]) for r in rows])


def weights(p, n):
    m = lab.sma(p, n)
    return np.where(np.isfinite(m) & (p > m), 1.0, 0.0)


def run(path, col, cost, eras, title):
    d, p = load(path, col)
    R = lab.returns(p.reshape(-1, 1))[:, 0]
    W = {"Halten": np.ones(len(p))}
    for n in LINES:
        W[f"SMA{n}"] = weights(p, n)
    N = {k: lab.backtest(w, R, cost) for k, w in W.items()}
    res = {}
    print(f"=== {title}: {d[0]} .. {d[-1]}")
    print(f"{'Epoche':12s}{'Linie':8s}{'Rend/J':>8s}{'Rueckg':>8s}{'Sharpe':>8s}{'Wechsel/J':>10s}")
    for name, lo, hi in eras:
        idx = [i for i, x in enumerate(d) if lo <= x <= hi]
        if len(idx) < 300:
            continue
        s, e = idx[0], idx[-1] + 1
        for k in W:
            m = lab.metrics(N[k][s:e], W[k][s:e])
            fl = np.abs(np.diff(W[k][s:e])).sum() / (len(idx) / 252)
            res[name, k] = m
            print(f"{name:12s}{k:8s}{m['cagr']*100:7.1f}%{m['mdd']*100:7.0f}%{m['sharpe']:8.2f}{fl:10.1f}")
        print()
    return res


def check(res, eras_all, crisis, need, label):
    """Kriterium (a)-(d) aus REGELN.md. Gibt je Linie zurueck, ob sie besteht."""
    out = {}
    names = [f"SMA{n}" for n in LINES]
    for k in names:
        if k == "SMA200":
            continue
        a = res[eras_all, k]["sharpe"] >= res[eras_all, "SMA200"]["sharpe"] + 0.05
        ep = [e for e in {x[0] for x in res} if e != eras_all]
        better = sum(res[e, k]["sharpe"] >= res[e, "SMA200"]["sharpe"] for e in ep)
        b = better >= need
        c1 = res[eras_all, k]["mdd"] <= res[eras_all, "SMA200"]["mdd"] + 0.03
        c2 = all(res[e, k]["mdd"] <= res[e, "SMA200"]["mdd"] + 0.05 for e in crisis if (e, k) in res)
        i = names.index(k)
        nb = [names[j] for j in (i - 1, i + 1) if 0 <= j < len(names)]
        dd = all(res[eras_all, x]["sharpe"] >= res[eras_all, "SMA200"]["sharpe"] for x in nb)
        out[k] = (a, b, c1 and c2, dd, better, len(ep))
        print(f"{label} {k}: (a) Sharpe+0,05 {a} | (b) Epochen {better}/{len(ep)} (noetig {need}) {b} | (c) Rueckgang {c1 and c2} | (d) Plateau {dd}  -> {'BESTEHT' if all(out[k][:4]) else 'nein'}")
    return {k: all(v[:4]) for k, v in out.items()}


spx_eras = [("1930-1949", "1930-01-01", "1949-12-31"), ("1950-1972", "1950-01-01", "1972-12-31"), ("1973-1982", "1973-01-01", "1982-12-31"),
            ("1983-1999", "1983-01-01", "1999-12-31"), ("2000-2009", "2000-01-01", "2009-12-31"), ("2010-2026", "2010-01-01", "2026-12-31"),
            ("alles", "1930-01-01", "2026-12-31")]
btc_eras = [("2011-2014", "2011-07-01", "2014-12-31"), ("2015-2018", "2015-01-01", "2018-12-31"), ("2019-2022", "2019-01-01", "2022-12-31"),
            ("2023-2026", "2023-01-01", "2026-12-31"), ("alles", "2011-07-01", "2026-12-31")]

rs = run("data/spx_long.csv", "SPX", 0.0005, spx_eras, "S&P 500 (Preisindex)")
rb = run("data/btc_long.csv", "BTC", 0.0010, btc_eras, "Bitcoin")
print("=== KRITERIUM (REGELN.md 2026-11-20)")
ok_s = check(rs, "alles", ("1973-1982", "2000-2009"), 4, "S&P")
ok_b = check(rb, "alles", (), 3, "BTC")
both = [k for k in ok_s if ok_s[k] and ok_b.get(k)]
print("\nBesteht fuer S&P UND Bitcoin:", both if both else "keine -> SMA200 bleibt")

# Gold nur Information (monatlich, Linien in Monaten ~ 63..294 Tage)
print("\n=== Gold monatlich ab 1971-08 (nur Information)")
d, p = load("data/gold_long.csv", "GOLD")
i0 = next(i for i, x in enumerate(d) if x >= "1971-08")
r = np.zeros(len(p)); r[1:] = p[1:] / p[:-1] - 1
print(f"{'Linie':10s}{'Rend/J':>8s}{'Rueckg':>8s}{'Sharpe':>8s}{'Wechsel/J':>10s}")
for lbl, w in [("Halten", np.ones(len(p)))] + [(f"{n} Mon.", weights(p, n)) for n in (3, 5, 7, 10, 14)]:
    wd = np.concatenate([[0.0], w[:-1]])
    net = wd * r - np.abs(np.diff(np.concatenate([[0.0], wd]))) * 0.0005
    net = net[i0:]
    eq = np.cumprod(1 + net)
    yrs = len(net) / 12
    cagr = eq[-1] ** (1 / yrs) - 1
    mdd = (eq / np.maximum.accumulate(eq) - 1).min()
    sh = net.mean() / max(net.std(ddof=1), 1e-12) * np.sqrt(12)
    fl = np.abs(np.diff(w[i0:])).sum() / yrs
    print(f"{lbl:10s}{cagr*100:7.1f}%{-mdd*100:7.0f}%{sh:8.2f}{fl:10.1f}")
