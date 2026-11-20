"""Ad-hoc: Silber gegen S&P 500 (SPY inkl. Dividenden), beides in Euro. Nur Ausgabe."""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp
fx = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
def eur(sym):
    d = fp.yahoo(sym); out = {}; last = None
    for k in sorted(d):
        last = fx.get(k, last)
        if last: out[k] = d[k] / last
    return out
S, P = eur("SI=F"), eur("SPY")
ks = sorted(set(S) & set(P)); end = ks[-1]
print(f"Stand {end}: Silber {S[end]:.2f} EUR/oz, Hoch {max(S.values()):.2f} am {max(S, key=S.get)}")
def at(d): return next(k for k in ks if k >= d)
print("Einmal kaufen, halten bis heute (Faktor in Euro):")
for y in ("2019-11-20","2020-11-20","2021-11-20","2016-11-20","2011-04-28","2006-11-20","2001-01-02"):
    k = at(y); print(f"  ab {k}: Silber x{S[end]/S[k]:.2f}  S&P x{P[end]/P[k]:.2f}")
print("Sparplan 100 EUR/Monat (erster Handelstag):")
for y in ("2019-11","2020-11","2016-11","2006-11"):
    ms = sorted({k[:7] for k in ks if k[:7] >= y}); s = p = 0
    for m in ms:
        k = at(m + "-01"); s += 100 / S[k]; p += 100 / P[k]
    n = len(ms) * 100; print(f"  ab {y}: eingezahlt {n} EUR -> Silber {s*S[end]:.0f}  S&P {p*P[end]:.0f}")
pk = max(S, key=S.get); print(f"Wer am Silber-Hoch {pk} kaufte: Silber x{S[end]/S[pk]:.2f}  S&P x{P[end]/P[pk]:.2f}")
