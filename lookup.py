"""Ad-hoc: Kursbild einer Aktie in Euro (Hoch, Abstand, 200-Tage-Linie, Wochen-Tiefs als Unterstützungen). Nur Ausgabe."""
import csv, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp
sym = sys.argv[1]
d = fp.yahoo(sym); fx = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
ks = sorted(d); last = None; e = {}
for k in ks:
    last = fx.get(k, last)
    if last: e[k] = d[k] / last
ks = sorted(e); p = np.array([e[k] for k in ks])
print(f"{sym}: {ks[-1]} {p[-1]:.2f} EUR ({d[ks[-1]]:.2f} USD), Tag {p[-1]/p[-2]-1:+.1%}, 1M {p[-1]/p[-22]-1:+.1%}, 1J {p[-1]/p[-253]-1:+.1%}")
i = int(p.argmax()); print(f"Allzeithoch {ks[i]} {p[i]:.2f} EUR, Abstand {p[-1]/p[i]-1:+.1%}")
for n in (50, 200): print(f"SMA{n}: {p[-n:].mean():.2f} EUR ({p[-1]/p[-n:].mean()-1:+.1%})")
# Wochenschluss-Tiefs/Hochs der letzten 2 Jahre (Swing-Punkte, 5 Wochen links/rechts)
w = {}
for k, v in zip(ks, p): w[np.datetime64(k, "W")] = (k, v)
wk = list(w.values())[-110:]; vals = np.array([v for _, v in wk])
print("Swing-Tiefs (Wochenschluss, 2 Jahre):")
for j in range(5, len(wk) - 2):
    if vals[j] == vals[max(0, j-5):j+6].min(): print(f"  {wk[j][0]} {vals[j]:.0f} EUR")
print("Swing-Hochs:")
for j in range(5, len(wk) - 2):
    if vals[j] == vals[max(0, j-5):j+6].max(): print(f"  {wk[j][0]} {vals[j]:.0f} EUR")
