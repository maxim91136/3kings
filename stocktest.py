"""Test: Warten auf Abstand zum Hoch bei Einzelaktien (Kriterien in REGELN.md, 2026-11-19). Nur Ausgabe."""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp
US = """AAPL NVDA AVGO ADBE INTU NOW ORCL CRM KLAC LRCX AMAT SNPS CDNS TXN ADI APH MSI ROP TYL FICO MSCI SPGI MCO ICE NDAQ VRSK CPRT ODFL
COST TJX ORLY AZO HD LOW NKE MCD CMG LULU UNH ISRG LLY ZTS IDXX TMO DHR SYK TDG HEI AME ROL FAST GWW POOL TSCO PGR BRK-B AXP BX KKR
TT ETN PH PAYX ADP CHD KO PEP PG WMT LIN SHW ECL META AMZN NFLX WST MPWR ANET CSGP EFX FDS BR WCN RSG TRV CB MMC AJG AON WRB ERIE
MKTX IT EW MTD WAT ROK NDSN GGG BRO TPL LMT NOC HCA CTAS MA V MSFT RACE GOOGL CME WM""".split()
EU = "MC.PA OR.PA SU.PA AI.PA EL.PA DSY.PA RMS.PA ASML.AS WKL.AS SAP.DE DB1.DE MUV2.DE NOVO-B.CO DSV.CO LSEG.L REL.L EXPN.L DGE.L ULVR.L ATCO-A.ST INVE-B.ST EVO.ST LISN.SW SIKA.SW PGHN.SW NESN.SW CSU.TO".split()
XS = [0.10, 0.15, 0.20, 0.25]; RATE = 0.02 / 12
def monthly(d):
    m = {}
    for k in sorted(d): m[k[:7]] = d[k]
    return m
def run(m, start):
    ks = [k for k in sorted(m) if k >= start]
    if len(ks) < 120: return None
    hist = [m[k] for k in sorted(m) if k < start]; hi = max(hist) if hist else m[ks[0]]
    res = {}
    for X in [0.0] + XS:
        units = cash = 0.0; h = hi
        for k in ks:
            p = m[k]; h = max(h, p); cash = cash * (1 + RATE) + 1
            if X == 0 or p <= (1 - X) * h: units += cash / p; cash = 0.0
        res[X] = (units * m[ks[-1]] + cash) / len(ks)
    return res
out = {"2006": [], "2016": []}
for sym in list(dict.fromkeys(US)) + EU:
    d = None
    for i in range(3):
        try:
            d = fp.yahoo(sym)
            if len(d) > 300: break
        except Exception as e: print(sym, "Fehler", e)
        time.sleep(8)
    time.sleep(1)
    if not d: continue
    m = monthly(d)
    for per, st in (("2006", "2006-01"), ("2016", "2016-01")):
        r = run(m, max(st, min(m))) if per == "2016" else run(m, max(st, min(m)))
        if r: out[per].append((sym, r))
for per, L in out.items():
    print(f"\nZeitraum ab {per}: {len(L)} Aktien")
    for X in XS:
        rel = np.array([r[X] / r[0.0] - 1 for _, r in L])
        print(f"  warten {int(X*100)} %: Median {np.median(rel)*100:+.1f} %, Mittel {rel.mean()*100:+.1f} %, besser bei {(rel>0).mean()*100:.0f} % der Aktien, schlechtestes {rel.min()*100:+.0f} %, bestes {rel.max()*100:+.0f} %")
