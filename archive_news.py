"""News-Archiv (Entscheidung 2026-11-21): Meldungen älter als 30 Tage wandern aus site/news.json in site/archive/news-YYYY-MM.json.
Nichts wird gelöscht. site/archive/index.json listet alle Monate mit Meldungen oder Berichten. Läuft im nächtlichen Datenlauf."""
import json, os
from datetime import date, timedelta
cut = (date.today() - timedelta(days=30)).isoformat()
n = json.load(open("site/news.json")); keep, move = [], {}
for x in n.get("items", []):
    (keep.append(x) if x.get("date", "9999") >= cut else move.setdefault(x["date"][:7], []).append(x))
key = lambda x: (x.get("date", ""), str(x.get("headline", "")).startswith(("Wochenende", "Weekend")))
for m, xs in move.items():
    p = f"site/archive/news-{m}.json"; old = json.load(open(p))["items"] if os.path.exists(p) else []
    seen = {key(x) for x in xs}; allx = xs + [x for x in old if key(x) not in seen]
    allx.sort(key=lambda x: (x.get("date", ""), not key(x)[1]), reverse=True)
    json.dump({"month": m, "items": allx}, open(p, "w"), ensure_ascii=False, indent=1)
if move:
    n["items"] = keep; json.dump(n, open("site/news.json", "w"), ensure_ascii=False, indent=1)
# Schattenbücher je Monat (vollständige Tageswerte; Startseite zeigt nur 30 Tage)
import csv
sh = {}
if os.path.exists("data/ledger.csv"):
    for r in csv.DictReader(open("data/ledger.csv")):
        sh.setdefault(r["date"][:7], {}).setdefault(r["date"], {}).update(team=float(r["shadow"]), team_hold=float(r["hold"]))
if os.path.exists("site/watch.json"):
    el = json.load(open("site/watch.json")).get("elite", {}).get("shadow", {})
    for r in el.get("lump", []): sh.setdefault(r["date"][:7], {}).setdefault(r["date"], {}).update(kj=r["elite"], kj_spy=r["spy"])
    for r in el.get("rows", []): sh.setdefault(r["date"][:7], {}).setdefault(r["date"], {}).update(kjp=r["elite"], kjp_spy=r["spy"])
for m, days in sh.items():
    json.dump({"month": m, "rows": [dict(date=d, **v) for d, v in sorted(days.items(), reverse=True)]}, open(f"site/archive/shadow-{m}.json", "w"))
months = {f[5:12] for f in os.listdir("site/archive") if f.startswith("news-")} | set(sh)
months |= {x["date"][:7] for x in keep if x.get("date")}
r = json.load(open("site/reports.json")) if os.path.exists("site/reports.json") else {"items": []}
months |= {x["period"][:7] for x in r.get("items", []) if x.get("type") == "month"}
json.dump({"months": sorted(months, reverse=True)}, open("site/archive/index.json", "w"))
print(f"Archiv: {sum(len(v) for v in move.values())} Meldungen verschoben, Monate: {sorted(months, reverse=True)}")
