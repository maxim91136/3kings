"""Frage 6 (REGELN 2026-11-22): S&P 500 gleich gewichtet (RSP) gegen nach Größe (SPY), Dollar, inkl. Ausschüttungen. Nur Ausgabe (JSON)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp
R, S = fp.yahoo("RSP"), fp.yahoo("SPY")
ds = sorted(set(R) & set(S)); print("von", ds[0], "bis", ds[-1])
def ev(a):
    d = [x for x in ds if x >= a]; r = [R[x] / R[d[0]] for x in d]; s = [S[x] / S[d[0]] for x in d]
    y = (len(d) - 1) / 252
    return d[0], r[-1] ** (1 / y) - 1, s[-1] ** (1 / y) - 1, r, s
def mdd(v):
    pk = dd = 0
    for x in v: pk = max(pk, x); dd = max(dd, 1 - x / pk)
    return dd
out = []; wins = 0
for a in ("2003-01-01", "2008-01-01", "2013-01-01", "2018-01-01"):
    d0, cr, cs, r, s = ev(a); wins += cr > cs; out.append(dict(from_=d0, rsp=round(cr, 4), spy=round(cs, 4), mdd_rsp=round(mdd(r), 3), mdd_spy=round(mdd(s), 3)))
    print(out[-1])
full = out[0]; ok = wins >= 3 and full["mdd_rsp"] <= full["mdd_spy"]
print("Fenster mit RSP besser:", wins, "von 4; Rückgang RSP", full["mdd_rsp"], "SPY", full["mdd_spy"], "->", "gleich gewichtet BESSER" if ok else "NICHT besser")
print(json.dumps(dict(rows=out, wins=wins, ok=ok, end=ds[-1])))
