"""Kronjuwelen-Saisonprüfung (REGELN.md 2026-11-21). Läuft im nächtlichen Datenlauf nach elitescreen.py, nur wenn eine neue Saison begonnen hat.
Mitglieder: alle vier Regeln (Beta, 10-J.-Rendite, Marge, Nettoverschuldung/EBITDA). Durchgefallen = Verwarnung, zwei Saisons in Folge = raus.
Neue Kandidaten: alle vier Regeln zwei Saisons in Folge bestanden -> Warteschlange für die Telegram-Bestätigung (elite_bank.py).
Schattenbuch verkettet (Stand bei Änderung = neue Basis, alle Mitglieder gleich gewichtet). Ergebnis ins Regelbuch DE/EN."""
import csv, json, os
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
for k in mem:
    r = rows.get(k, {"passed": False, "why": ["data"]})
    sk[k] = 0 if r["passed"] else sk.get(k, 0) + 1
    if sk[k] >= 2: out.append(k)
    elif sk[k] == 1: warn.append(k)
stay = [k for k in mem if k not in out]
d = sc["date"]
if out and stay:
    fx = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
    px = list(csv.DictReader(open("data/elite.csv")))
    last = next(r for r in reversed(px) if all(r.get(k) for k in stay)); f = fx.get(last["date"]) or fx[max(k for k in fx if k <= last["date"])]
    st = json.load(open("data/elite_state.json")); base = st["rows"][-1]["elite"] if st["rows"] else 1.0
    st["base"] = base; st["p0"] = {k: float(last[k]) / f for k in stay}
    st.setdefault("changes", []).append({"date": last["date"], "out": out, "base": base})
    json.dump(st, open("data/elite_state.json", "w"), indent=1)
    json.dump(stay, open("data/elite_members.json", "w"))
for k in out: sk.pop(k, None)
cand = [s for s in sc["bank"] if s not in stay]
if cand:
    q = json.load(open("data/elite_pending.json")) if os.path.exists("data/elite_pending.json") else {}
    q["queue"] = [s for s in cand if s != (q.get("current") or {}).get("sym")]; q["season"] = n; q["rejected"] = []
    json.dump(q, open("data/elite_pending.json", "w"), ensure_ascii=False, indent=1)
fz = {"stand": d, "rows": [{"key": k, "beta": rows.get(k, {}).get("beta"), "cagr10": rows.get(k, {}).get("cagr10")} for k in stay]}
json.dump(fz, open("data/elite_frozen.json", "w"), indent=1)
def line(k, en=False):
    r = rows.get(k, {})
    num = lambda x, pc=False: "–" if x is None else (f"{x*100:.1f}" if pc else f"{x}")
    t = f"{nm(k)} {num(r.get('beta'))} / {num(r.get('cagr10'), True)} % / {num(r.get('margin'), True)} % / {num(r.get('nd_ebitda'))}"
    return t if en else t.replace(".", ",")
de = (f"\n## {d}: Kronjuwelen-Saisonprüfung (Saison {n - 1} beendet, automatisch)\nMitglieder (Beta / 10-J.-Rendite / Bruttomarge / Nettoverschuldung zu EBITDA): " + "; ".join(line(k) for k in mem) + ".\n"
      + (f"Ausgeschieden (zwei Prüfungen in Folge durchgefallen): {', '.join(nm(k) for k in out)}. Schattenbuch verkettet mit {len(stay)} Werten.\n" if out else "")
      + (f"Verwarnt (erstmals durchgefallen): {', '.join(nm(k) for k in warn)}.\n" if warn else "")
      + (f"Aufnahmereif (zwei Saisons in Folge bestanden), Bestätigung per Telegram: {', '.join(nm(k) for k in cand)}.\n" if cand else "Keine neuen Aufnahmekandidaten.\n"))
en = (f"\n## {d}: Crown Jewels season review (season {n - 1} ended, automatic)\nMembers (beta / 10-year return / gross margin / net debt to EBITDA): " + "; ".join(line(k, True) for k in mem) + ".\n"
      + (f"Dropped (failed two reviews in a row): {', '.join(nm(k) for k in out)}. Shadow book chained with {len(stay)} stocks.\n" if out else "")
      + (f"Warned (failed for the first time): {', '.join(nm(k) for k in warn)}.\n" if warn else "")
      + (f"Ready for admission (passed two seasons in a row), confirmation via Telegram: {', '.join(nm(k) for k in cand)}.\n" if cand else "No new admission candidates.\n"))
open("REGELN.md", "a").write(de); open("REGELN.en.md", "a").write(en)
rv["last_season"] = n; rv["reviews"].append({"date": d, "season": n - 1, "out": out, "warn": warn, "ready": cand})
json.dump(rv, open("data/elite_reviews.json", "w"), indent=1)
print(de)
