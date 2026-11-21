"""Elite-Saisonprüfung (REGELN.md 2026-11-21). Läuft im nächtlichen Datenlauf nach heartbeat.py und elitecheck.py.
Nur wenn eine neue Saison begonnen hat: harte Regeln prüfen. Wer zwei Saisonprüfungen in Folge nicht besteht, fliegt raus (keine Ausnahme); beim ersten Mal Verwarnung.
Schattenbuch läuft verkettet weiter (Stand beim Ausscheiden = neue Basis, verbleibende gleich gewichtet).
Ergebnis in data/elite_reviews.json, Aufnahmewerte neu eingefroren, Eintrag ins Regelbuch DE/EN."""
import csv, json, os
NAMES = {"RACE": "Ferrari", "MA": "Mastercard", "V": "Visa", "CTAS": "Cintas", "MSFT": "Microsoft", "IDXX": "IDEXX"}
rv = json.load(open("data/elite_reviews.json")); hb = json.load(open("site/heartbeat.json"))
n = hb["season"]["n_seasons"]
if n <= rv["last_season"]:
    print(f"Elite-Prüfung: keine neue Saison ({n})"); raise SystemExit(0)
chk = json.load(open("site/elite_check.json")); mem = json.load(open("data/elite_members.json"))
rows = [r for r in chk["rows"] if r["key"] in mem]
# Ausscheiden erst nach zwei Saisonprüfungen in Folge durchgefallen (REGELN 2026-11-21, Änderung)
sk = rv.setdefault("strikes", {})
for r in rows: sk[r["key"]] = 0 if r["pass"] else sk.get(r["key"], 0) + 1
out = [r for r in rows if sk[r["key"]] >= 2]; stay = [r for r in rows if sk[r["key"]] < 2]
warn = [r for r in rows if sk[r["key"]] == 1]
for r in out: sk.pop(r["key"], None)
d = chk["date"]
st = json.load(open("data/elite_state.json"))
if out and stay:
    fx = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
    px = {r["date"]: r for r in csv.DictReader(open("data/elite.csv"))}
    last = max(k for k in px if k <= d); f = fx.get(last) or fx[max(k for k in fx if k <= last)]
    base = st["rows"][-1]["elite"] if st["rows"] else 1.0
    st["base"] = base; st["p0"] = {r["key"]: float(px[last][r["key"]]) / f for r in stay}
    st.setdefault("changes", []).append({"date": last, "out": [r["key"] for r in out], "base": base})
    json.dump(st, open("data/elite_state.json", "w"), indent=1)
    json.dump([r["key"] for r in stay], open("data/elite_members.json", "w"))
json.dump({"stand": d, "rows": [{"key": r["key"], "beta": r["beta"], "cagr10": r["cagr10"]} for r in (stay if stay else rows)]}, open("data/elite_frozen.json", "w"), indent=1)
pct = lambda x: "–" if x is None else f"{x*100:.1f}".replace(".", ",")
pen = lambda x: "–" if x is None else f"{x*100:.1f}"
res = "; ".join(f"{NAMES[r['key']]} {str(r['beta']).replace('.', ',')} / {pct(r['cagr10'])} %" for r in rows)
res_en = "; ".join(f"{NAMES[r['key']]} {r['beta']} / {pen(r['cagr10'])} %" for r in rows)
gone = ", ".join(NAMES[r["key"]] + (" (Beta)" if "beta" in r["why"] else "") + (" (Rendite)" if "cagr10" in r["why"] else "") for r in out)
gone_en = ", ".join(NAMES[r["key"]] + (" (beta)" if "beta" in r["why"] else "") + (" (return)" if "cagr10" in r["why"] else "") for r in out)
wn = ", ".join(NAMES[r["key"]] for r in warn); wn_en = wn
de = f"\n## {d}: Elite-Saisonprüfung (Saison {n - 1} beendet, automatisch nach Regel 2026-11-21)\nHarte Regeln mit aktuellen Kursen (Beta / 10-Jahres-Rendite): {res}.\n" + (f"Ausgeschieden: {gone}. Schattenbuch läuft verkettet mit den verbleibenden {len(stay)} weiter (gleich gewichtet ab {d}).\n" if out else ("Niemand scheidet aus.\n" if warn else f"Alle {len(rows)} bestehen. Keine Änderung.\n")) + (f"Verwarnt (1. Mal durchgefallen, scheidet aus, wenn die nächste Saisonprüfung ebenfalls nicht bestanden wird): {wn}.\n" if warn else "") + "Aufnahmewerte neu eingefroren. Weiche Regeln (Marge, Marktstellung usw.) nicht automatisch geprüft.\n"
en = f"\n## {d}: Elite season review (season {n - 1} ended, automatic per rule of Nov 21, 2026)\nHard rules with current prices (beta / 10-year return): {res_en}.\n" + (f"Dropped: {gone_en}. The shadow book continues chained with the remaining {len(stay)} (equal weight from {d}).\n" if out else ("Nobody is dropped.\n" if warn else f"All {len(rows)} pass. No change.\n")) + (f"Warned (failed for the first time, dropped if the next season review is also failed): {wn_en}.\n" if warn else "") + "Admission values re-frozen. Soft rules (margin, market position etc.) not checked automatically.\n"
open("REGELN.md", "a").write(de); open("REGELN.en.md", "a").write(en)
rv["last_season"] = n; rv["reviews"].append({"date": d, "season": n - 1, "rows": rows, "out": [r["key"] for r in out], "warn": [r["key"] for r in warn]})
json.dump(rv, open("data/elite_reviews.json", "w"), indent=1)
print(de)
