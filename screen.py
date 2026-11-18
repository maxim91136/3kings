"""Einmaliges Screening: weitere Kandidaten fuer Elite (Regeln: Beta < 1,15 und 10J-Rendite >= 17 % p. a.). Nur Ausgabe."""
import csv, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp

US = """AAPL NVDA AVGO ADBE INTU NOW ORCL CRM KLAC LRCX AMAT SNPS CDNS TXN ADI APH MSI ROP TYL FICO MSCI SPGI MCO ICE NDAQ VRSK CPRT ODFL
COST TJX ORLY AZO HD LOW NKE MCD CMG LULU UNH ISRG LLY ZTS IDXX TMO DHR SYK TDG HEI AME ROL FAST GWW POOL TSCO PGR BRK-B AXP BX KKR
TT ETN PH PAYX ADP CHD KO PEP PG WMT LIN SHW ECL META AMZN NFLX WST MPWR ANET CSGP EFX FDS BR WCN RSG TRV CB MMC AJG AON WRB ERIE
MKTX IT EW MTD WAT ROK NDSN GGG IDXX BRO TPL LMT NOC HCA CTAS MA V MSFT RACE GOOGL CME WM""".split()
EU = {"MC.PA": "EUR", "OR.PA": "EUR", "SU.PA": "EUR", "AI.PA": "EUR", "EL.PA": "EUR", "DSY.PA": "EUR", "RMS.PA": "EUR", "ASML.AS": "EUR",
      "WKL.AS": "EUR", "SAP.DE": "EUR", "DB1.DE": "EUR", "MUV2.DE": "EUR", "NOVO-B.CO": "DKK", "DSV.CO": "DKK", "LSEG.L": "GBP", "REL.L": "GBP",
      "EXPN.L": "GBP", "DGE.L": "GBP", "ULVR.L": "GBP", "ATCO-A.ST": "SEK", "INVE-B.ST": "SEK", "EVO.ST": "SEK", "LISN.SW": "CHF", "SIKA.SW": "CHF",
      "PGHN.SW": "CHF", "NESN.SW": "CHF", "CSU.TO": "CAD"}
def get(sym):
    for i in range(3):
        try:
            d = fp.yahoo(sym)
            if len(d) > 300: return d
        except Exception as e: print(sym, "Fehler", e)
        time.sleep(10)
    return None
fxu = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
fx = {"USD": {d: 1 / v for d, v in fxu.items()}, "EUR": None}
for c in {"DKK", "GBP", "SEK", "CHF", "CAD"}:
    fx[c] = get(f"{c}EUR=X"); time.sleep(1)
def eur(s, c):
    if c == "EUR": return s
    out, last, r = {}, None, fx.get(c)
    if not r: return None
    for d in sorted(s):
        last = r.get(d, last)
        if last: out[d] = s[d] * last * (0.01 if c == "GBP" else 1)
    return out
spy = eur(get("SPY"), "USD")
def beta(p):
    ds = [d for d in sorted(p) if d in spy][-1260:]
    a = np.array([p[d] for d in ds]); b = np.array([spy[d] for d in ds]); ra, rb = a[1:] / a[:-1] - 1, b[1:] / b[:-1] - 1
    return float(np.cov(ra, rb)[0, 1] / rb.var(ddof=1))
def cagr10(s):
    ds = sorted(s); d1 = ds[-1]; y = int(d1[:4]) - 10; t = f"{y}{d1[4:]}"
    i0 = next((d for d in ds if d >= t), None)
    if not i0 or i0 > f"{y}{d1[4:8]}28" or ds[0] > t: return None
    return (s[d1] / s[i0]) ** (365.25 / (np.datetime64(d1) - np.datetime64(i0)).astype(int)) - 1
res = []
for sym, cur in [(u, "USD") for u in dict.fromkeys(US)] + list(EU.items()):
    s = get(sym); time.sleep(1.2)
    if not s: res.append((sym, None, None)); continue
    e = eur(s, cur)
    res.append((sym, None if not e else round(beta(e), 2), cagr10(s)))
res.sort(key=lambda r: -(r[2] or -9))
print("\nSYMBOL       BETA   10J      ERGEBNIS")
for sym, b, c in res:
    ok = b is not None and c is not None and b < 1.15 and c >= 0.17
    why = "BESTANDEN" if ok else ("keine Daten/zu jung" if b is None or c is None else ("Beta" if b >= 1.15 else "") + (" Rendite" if c < 0.17 else ""))
    print(f"{sym:11s} {b if b is not None else '-':>5}  {'-' if c is None else f'{c*100:5.1f} %'}  {why}")
