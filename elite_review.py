"""Kronjuwelen-Saisonprüfung (REGELN.md 2026-11-21). Läuft im nächtlichen Datenlauf nach elitescreen.py, nur wenn eine neue Saison begonnen hat.
Mitglieder: alle vier Regeln (Beta, 10-J.-Rendite, Marge, Nettoverschuldung/EBITDA). Durchgefallen = Verwarnung, zwei Saisons in Folge = raus.
Neue Kandidaten: alle vier Regeln zwei Saisons in Folge bestanden -> automatisch aufgenommen; Meldung privat per Telegram.
Schattenbuch verkettet (Stand bei Änderung = neue Basis, alle Mitglieder gleich gewichtet). Ergebnis ins Regelbuch DE/EN."""
import json, os
rv = json.load(open("data/elite_reviews.json")); hb = json.load(open("site/heartbeat.json")); n = hb["season"]["n_seasons"]
if n <= rv["last_season"]:
    print(f"Kronjuwelen-Prüfung: keine neue Saison ({n})"); raise SystemExit(0)
sc = json.load(open("data/elite_screen.json")) if os.path.exists("data/elite_screen.json") else {"season": 0}
if sc["season"] != n:
    print("Kronjuwelen-Prüfung: Screening dieser Saison fehlt, später erneut"); raise SystemExit(0)
mem = json.load(open("data/elite_members.json")); rows = {r["sym"]: r for r in sc["rows"]}
meta = json.load(open("data/elite_meta.json")) if os.path.exists("data/elite_meta.json") else {}
nm = lambda k: meta.get(k, {}).get("name") or rows.get(k, {}).get("name") or k
sk = rv.setdefault("strikes", {}); out, warn = [], []
for k in mem:   # Puffer: nur klare Verfehlung zählt (fail_out)
    r = rows.get(k, {"fail_out": True})
    sk[k] = sk.get(k, 0) + 1 if r.get("fail_out", True) else 0
    if sk[k] >= 2: out.append(k)
    elif sk[k] == 1: warn.append(k)
stay = [k for k in mem if k not in out]
d = sc["date"]
if out:   # Sparplan-Index: Ausgeschiedene bekommen kein neues Geld mehr, werden aber nicht verkauft
    hist = json.load(open("data/elite_hist.json")); hist.append({"date": d, "members": stay, "next": True})
    json.dump(hist, open("data/elite_hist.json", "w"), indent=1); json.dump(stay, open("data/elite_members.json", "w"))
for k in out: sk.pop(k, None)
cand = [s for s in sc["bank"] if s not in stay]
fz = {"stand": d, "rows": [{"key": k, "beta": rows.get(k, {}).get("beta"), "cagr10": rows.get(k, {}).get("cagr10")} for k in stay]}
json.dump(fz, open("data/elite_frozen.json", "w"), indent=1)
import elite_bank   # automatische Aufnahme (Index-Logik, Entscheidung 2026-11-21): Schattenbuch verkettet, Regelbuch-Eintrag
for k in cand: elite_bank.admit(rows[k], how="automatisch nach Regel", how_en="automatic per rule", d=d)
def line(k, en=False):
    r = rows.get(k, {})
    num = lambda x, pc=False: "–" if x is None else (f"{x*100:.1f}" if pc else f"{x}")
    t = f"{nm(k)} {num(r.get('beta'))} / {num(r.get('cagr10'), True)} % / {num(r.get('margin'), True)} % / {num(r.get('nd_ebitda'))}"
    return t if en else t.replace(".", ",")
de = (f"\n## {d}: Kronjuwelen-Saisonprüfung (Saison {n - 1} beendet, automatisch)\nMitglieder (Beta / 10-J.-Rendite / Bruttomarge / Nettoverschuldung zu EBITDA): " + "; ".join(line(k) for k in mem) + ".\n"
      + (f"Ausgeschieden (zwei Prüfungen in Folge durchgefallen): {', '.join(nm(k) for k in out)}. Kein Verkauf; neues Geld nur noch an {len(stay)} Werte.\n" if out else "")
      + (f"Verwarnt (erstmals durchgefallen): {', '.join(nm(k) for k in warn)}.\n" if warn else "")
      + (f"Aufgenommen (zwei Saisons in Folge alle Regeln bestanden): {', '.join(nm(k) for k in cand)}.\n" if cand else "Keine neuen Aufnahmekandidaten.\n"))
en = (f"\n## {d}: Crown Jewels season review (season {n - 1} ended, automatic)\nMembers (beta / 10-year return / gross margin / net debt to EBITDA): " + "; ".join(line(k, True) for k in mem) + ".\n"
      + (f"Dropped (failed two reviews in a row): {', '.join(nm(k) for k in out)}. No sale; new money only to {len(stay)} stocks.\n" if out else "")
      + (f"Warned (failed for the first time): {', '.join(nm(k) for k in warn)}.\n" if warn else "")
      + (f"Admitted (passed all rules two seasons in a row): {', '.join(nm(k) for k in cand)}.\n" if cand else "No new admission candidates.\n"))
open("REGELN.md", "a").write(de); open("REGELN.en.md", "a").write(en)
nowm = json.load(open("data/elite_members.json"))
msg = [f"💎 <b>Kronjuwelen: Saisonprüfung {d}</b>"]
msg += [f"➕ Neu: {nm(k)} → Sparplan starten" for k in cand] + [f"➖ Raus: {nm(k)} → Sparplan stoppen, NICHT verkaufen" for k in out]
msg += [f"⚠️ Verwarnt: {nm(k)} (raus, wenn die nächste Prüfung wieder klar verfehlt wird)" for k in warn]
msg += (["Keine Änderung. Sparpläne bleiben, wie sie sind."] if not (cand or out) else [f"Jetzt {len(nowm)} Werte, Rate gleich verteilt (je 1/{len(nowm)}): {', '.join(nm(k) for k in nowm)}"])
json.dump(["\n".join(msg)], open("data/elite_notify.json", "w"), ensure_ascii=False)
rv["last_season"] = n; rv["reviews"].append({"date": d, "season": n - 1, "out": out, "warn": warn, "ready": cand})
json.dump(rv, open("data/elite_reviews.json", "w"), indent=1)
print(de)
