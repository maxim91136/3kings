"""Schattenbuch Trendportfolio 16 Märkte, ohne Hebel, in Euro (REGELN 2026-11-22). Nur Information, kein echtes Geld.
Regeln (vorab festgelegt, aus dem Test im Trading-Bot-Chat übernommen, nichts nachgebessert):
- 16 Märkte: SPY QQQ IWM EFA EEM GLD SLV DBC USO TLT IEF HYG VNQ UUP BTC ETH (Yahoo, Tagesschluss, in Euro umgerechnet).
- Je Markt sechs Signale: Kurs über dem Kurs vor 50/100/200 Tagen; Ausbruch über das 50/100/200-Tage-Hoch (aktiv, bis das jeweilige Tief unterschritten wird).
- Anteil = (aktive Signale / 6) x (10 % / 60-Tage-Schwankung p. a.) / 16. Nur long. Summe höchstens 100 % (ohne Hebel; darüber anteilig gekürzt). Rest Cash (ohne Zins).
- Signal am Schluss, Umsetzung zum nächsten Schluss, Kosten 0,05 % je Seite.
Schreibt data/trend16.csv (Kurse) und site/trend16.json."""
import csv, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp
M = ["SPY", "QQQ", "IWM", "EFA", "EEM", "GLD", "SLV", "DBC", "USO", "TLT", "IEF", "HYG", "VNQ", "UUP", "BTC-USD", "ETH-USD"]
START, COST, TV, FROM = "2026-11-20", 0.0005, 0.10, "2015-01-01"
fx = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
S = {}
for m in M:
    for k in range(3):
        try: s = fp.yahoo(m); break
        except Exception as e: s = None; time.sleep(3)
    if s: S[m] = s
    time.sleep(0.5)
if len(S) < len(M): print("fehlt:", [m for m in M if m not in S])
days = sorted(d for d in S["SPY"] if d >= "2014-01-01")
fxd, last = [], None
for d in days:
    last = fx.get(d, last); fxd.append(last)
P = np.full((len(days), len(M)), np.nan)
for j, m in enumerate(M):
    if m not in S: continue
    lastp = None
    for i, d in enumerate(days):
        lastp = S[m].get(d, lastp)
        if lastp is not None and fxd[i]: P[i, j] = lastp / fxd[i]
T, N = len(days), len(M)
R = np.zeros_like(P); R[1:] = P[1:] / P[:-1] - 1; R = np.nan_to_num(R)
sig = np.zeros((T, N))
for j in range(N):
    p = P[:, j]; s = np.zeros(T)
    for n in (50, 100, 200):
        tm = np.zeros(T); tm[n:] = (p[n:] > p[:-n]).astype(float); s += np.nan_to_num(tm)
        br = np.zeros(T); on = 0.0
        for t in range(n, T):
            if np.isnan(p[t]): continue
            win = p[t - n:t]
            if np.isnan(win).all(): continue
            if p[t] > np.nanmax(win): on = 1.0
            elif p[t] < np.nanmin(win): on = 0.0
            br[t] = on
        s += br
    sig[:, j] = s / 6
vol = np.full((T, N), np.nan)
for t in range(60, T): vol[t] = R[t - 59:t + 1].std(axis=0, ddof=1) * np.sqrt(252)
w = np.nan_to_num(sig * TV / np.where(vol > 0, vol, np.nan) / N)
w[np.isnan(P)] = 0
tot = w.sum(axis=1); w = w / np.maximum(tot, 1)[:, None]          # ohne Hebel
net = np.zeros(T); dw = np.abs(np.diff(w, axis=0, prepend=0)).sum(axis=1)
net[1:] = (w[:-1] * R[1:]).sum(axis=1) - COST * dw[:-1]
spy = R[:, 0]
def stats(x, a):
    x = x[a:]; eq = np.cumprod(1 + x); yrs = len(x) / 252
    return dict(cagr=round(float(eq[-1] ** (1 / yrs) - 1), 3), vol=round(float(x.std(ddof=1) * np.sqrt(252)), 3),
                sharpe=round(float(x.mean() / x.std(ddof=1) * np.sqrt(252)), 2), mdd=round(float((1 - eq / np.maximum.accumulate(eq)).max()), 3))
a0 = next(i for i, d in enumerate(days) if d >= FROM); i0 = next(i for i, d in enumerate(days) if d >= START)
eq, eqs = np.cumprod(1 + net), np.cumprod(1 + spy)
out = dict(start=days[i0], date=days[-1], fwd=round(float(eq[-1] / eq[i0] - 1), 4), fwd_spy=round(float(eqs[-1] / eqs[i0] - 1), 4),
           invested=round(float(w[-1].sum()), 3), back_from=days[a0], back=stats(net, a0), back_spy=stats(spy, a0),
           weights={m.replace("-USD", ""): round(float(w[-1, j]), 3) for j, m in enumerate(M) if w[-1, j] > 0.001},
           score={m.replace("-USD", ""): round(float(sig[-1, j]), 2) for j, m in enumerate(M)}, missing=[m for m in M if m not in S])
json.dump(out, open("site/trend16.json", "w"), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False))
