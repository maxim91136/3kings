"""Nur Ausgabe: Stand jetzt (Live-Kurse) gegen Vortagesschluss, in Euro. Aendert nichts."""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp
def last2(s):
    d = fp.yahoo(s); ks = sorted(d); return ks[-1], d[ks[-1]], d[ks[-2]]
fxd, fx_now, fx_prev = last2("EURUSD=X")
out = {}
for s in ["^GSPC", "SPY", "BTC-USD", "GC=F", "RACE", "MA", "V", "CTAS", "MSFT", "IDXX", "NVDA", "AMD"]:
    try: out[s] = last2(s)
    except Exception as e: print(s, "Fehler", e)
print(f"EURUSD {fxd} {fx_now:.4f} (Vortag {fx_prev:.4f})")
for s, (d, now, prev) in out.items():
    eur = s not in ("^GSPC",)
    ch = (now / fx_now) / (prev / fx_prev) - 1
    print(f"{s:8s} {d} jetzt {now:,.2f} USD = {now/fx_now:,.0f} EUR | Tag {now/prev-1:+.2%} USD, {ch:+.2%} EUR")
st = json.load(open("data/elite_state.json"))
ks = ["RACE", "MA", "V", "CTAS", "MSFT", "IDXX"]
e = sum((out[k][1] / fx_now) / st["p0"][k] for k in ks) / len(ks)
spy = (out["SPY"][1] / fx_now) / st["spy0"]
print(f"Schattenbuch wenn jetzt Schluss: Elite 6 {e:.4f} | S&P 500 {spy:.4f}")
