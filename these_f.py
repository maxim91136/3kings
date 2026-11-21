"""These F (REGELN 2026-11-21): Monatlich festhalten, welche Kronjuwelen unter ihrer 200-Tage-Linie liegen.
Bewertung je Schnappschuss nach 12 Monaten: Rendite der Gruppe "unter" gegen "über" (gleich gewichtet, Heimatwährung). Schreibt data/these_f.json."""
import json, os
w = json.load(open("site/watch.json"))["elite"]["rows"]
d = max(r["until"] for r in w if r.get("until"))
f = "data/these_f.json"; h = json.load(open(f)) if os.path.exists(f) else {"snaps": []}
if "snaps" not in h: h = {"snaps": []}
if any(x["date"][:7] == d[:7] for x in h["snaps"]): raise SystemExit(f"These F: Monat {d[:7]} schon festgehalten")
h["snaps"].append(dict(date=d, below=[r["key"] for r in w if r.get("sma200") is not None and r["sma200"] < 0],
                       above=[r["key"] for r in w if r.get("sma200") is not None and r["sma200"] >= 0], gap={r["key"]: r.get("sma200") for r in w}))
json.dump(h, open(f, "w"), ensure_ascii=False, indent=1); print("These F festgehalten:", h["snaps"][-1])
