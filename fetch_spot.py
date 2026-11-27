"""Goldpreis in $ je Unze (Yahoo GC=F, Terminkontrakt als Naeherung fuer den Spotpreis) -> data/gold_spot.csv. Nur Anzeige."""
import csv, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp
for _i in range(3):
    try:
        d = fp.yahoo("GC=F")
        if len(d) > 200: break
    except Exception as e:
        print("GC=F Fehler", e)
    time.sleep(10)
else:
    sys.exit("gold_spot: keine Daten")
with open("data/gold_spot.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["date", "value"])
    for k in sorted(d): w.writerow([k, round(d[k], 2)])
print(f"gold_spot.csv: {len(d)} Tage bis {max(d)}, {d[max(d)]:.0f} $/oz")
