"""Holt Tageskurse (bereinigt, Total Return) der Elite-9-Aktien von Yahoo -> data/elite.csv. Fehler sind nicht fatal."""
import csv, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp

T = {"RACE": "RACE", "MA": "MA", "V": "V", "CTAS": "CTAS", "MSFT": "MSFT", "IDXX": "IDXX"}
import json
META = json.load(open("data/elite_meta.json")) if os.path.exists("data/elite_meta.json") else {}
if os.path.exists("data/elite_members.json"):  # Mitglieder + Ausgeschiedene (bleiben im Sparplan-Bestand)
    _h = json.load(open("data/elite_hist.json")) if os.path.exists("data/elite_hist.json") else []
    T = {k: k for k in dict.fromkeys(json.load(open("data/elite_members.json")) + [x for e in _h for x in e["members"]])}
CUR = {k: META.get(k, {}).get("cur", "USD") for k in T}
data = {}; home = {}
for k, sym in T.items():
    for i in range(3):
        try:
            d = fp.yahoo(sym)
            if CUR.get(k, "USD") != "USD":  # in Dollar umrechnen (Heimatwährung separat für die 10-J.-Regel)
                home.setdefault("_", {})[k] = dict(d); fxs = fp.yahoo(f"{CUR[k]}USD=X"); last = None; dd = {}
                for t in sorted(d):
                    last = fxs.get(t, last)
                    if last: dd[t] = d[t] * last * (0.01 if CUR[k] == "GBP" else 1)
                d = dd
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

if home.get("_"):
    H = home["_"]; hd = sorted({d for s in H.values() for d in s if d < today})
    with open("data/elite_home.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["date"] + list(H))
        for d in hd: w.writerow([d] + [round(H[c][d], 4) if d in H[c] else "" for c in H])
