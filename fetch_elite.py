"""Holt Tageskurse (bereinigt, Total Return) der Elite-9-Aktien von Yahoo -> data/elite.csv. Fehler sind nicht fatal."""
import csv, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp

T = {"RACE": "RACE", "MA": "MA", "V": "V", "CTAS": "CTAS", "MSFT": "MSFT", "IDXX": "IDXX"}
import json
if os.path.exists("data/elite_members.json"): T = {k: v for k, v in T.items() if k in json.load(open("data/elite_members.json"))}
data = {}
for k, sym in T.items():
    for i in range(3):
        try:
            d = fp.yahoo(sym); 
            if len(d) < 500: raise ValueError(f"nur {len(d)} Tage")
            data[k] = d; print(f"{k}: {len(d)} Tage, {min(d)} .. {max(d)}"); break
        except Exception as e:
            print(f"{k} Versuch {i+1} fehlgeschlagen: {e}"); time.sleep(15)
    time.sleep(2)
if not data:
    raise SystemExit("keine Elite-Kurse - alte Datei bleibt")
today = time.strftime("%Y-%m-%d", time.gmtime())
days = sorted({d for s in data.values() for d in s if d < today}); cols = list(data)
os.makedirs("data", exist_ok=True)
with open("data/elite.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["date"] + cols)
    for d in days: w.writerow([d] + [round(data[c][d], 4) if d in data[c] else "" for c in cols])
print(f"elite.csv: {len(days)} Tage, Spalten {', '.join(cols)}")
