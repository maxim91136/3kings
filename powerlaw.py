"""Power-Law-Check Bitcoin (Regel: REGELN.md 2026-11-21). Schreibt site/powerlaw.json.
Mittellinie 1.0117e-17 * Tage^5.82 (Tage seit 3.1.2009, Dollar), Untergrenze 0,42 x Mittellinie.
Geprüft wird jeder abgeschlossene Monat am Monatsschluss (letzter Tagesschluss, Dollar)."""
import csv, json
from datetime import date
G = date(2009, 1, 3); K = 0.42
fair = lambda d: 1.0117e-17 * ((date.fromisoformat(d) - G).days) ** 5.82
px = {r["date"]: float(r["BTC"]) for r in csv.DictReader(open("data/prices.csv")) if r.get("BTC")}
ks = sorted(px); last = ks[-1]
mon = {}
for k in ks: mon[k[:7]] = k
months = sorted(mon)
# Monat gilt als abgeschlossen, wenn ein späterer Monat Daten hat
done = months[:-1]
rows = []
for m in months:
    k = mon[m]; f = fair(k)
    rows.append({"m": m, "date": k, "close": round(px[k]), "fair": round(f), "floor": round(K * f), "ratio": round(px[k] / f, 3), "below": px[k] < K * f, "final": m in done})
streak = 0
for r in reversed([r for r in rows if r["final"]]):
    if r["below"]: streak += 1
    else: break
fl = [r for r in rows if r["final"]]
out = {"until": last, "k": K, "price": round(px[last]), "fair": round(fair(last)), "floor": round(K * fair(last)),
       "ratio": round(px[last] / fair(last), 3), "below_now": px[last] < K * fair(last),
       "last_month": fl[-1] if fl else None, "streak": streak,
       "broken_months": [r["m"] for r in fl if r["below"]], "n_months": len(fl),
       "rows": [[r["m"], r["close"], r["fair"], r["floor"]] for r in rows]}
json.dump(out, open("site/powerlaw.json", "w"), separators=(",", ":"))
print({k: v for k, v in out.items() if k != "rows"})
