"""Elite-Bank: Einwechslung per Telegram-Bestätigung (REGELN.md 2026-11-21).
  python elite_bank.py propose   -> ist ein Platz frei und kein Vorschlag offen: bester Bankkandidat (höchste 10-J.-Rendite) per Telegram privat vorschlagen
  python elite_bank.py poll      -> Antworten abholen (nur vom privaten Chat), Einwechseln/Ablehnen ausführen, Erinnerung nach 7 Tagen
  python elite_bank.py test SYM  -> Testvorschlag (Bestätigung ändert nichts)
Zustand: data/elite_pending.json, Update-Offset: data/tg_offset.json."""
import csv, json, os, subprocess, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", ""); IDS = [c.strip() for c in os.environ.get("TELEGRAM_CHAT_ID", "").split(",") if c.strip()]
USER = next((c for c in IDS if not c.startswith("-")), None)  # nur der private Chat entscheidet
U = json.load(open("data/elite_universe.json")); SIZE = U["rules"]["size"]
PEND = "data/elite_pending.json"; OFF = "data/tg_offset.json"
now = lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
def api(m, **kw):
    d = urllib.parse.urlencode({k: (json.dumps(v) if isinstance(v, (dict, list)) else v) for k, v in kw.items()}).encode()
    return json.loads(urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/{m}", d, timeout=40).read())
def load(p, d): return json.load(open(p)) if os.path.exists(p) else d
def save(p, o): json.dump(o, open(p, "w"), ensure_ascii=False, indent=1)
def say(text, buttons=None):
    kw = dict(chat_id=USER, text=text, parse_mode="HTML")
    if buttons: kw["reply_markup"] = {"inline_keyboard": [buttons]}
    return api("sendMessage", **kw)["result"]["message_id"]
def pct(x): return f"{x*100:.1f}".replace(".", ",")
def candidates(rej):
    sc = load("data/elite_screen.json", {"rows": [], "bank": []}); mem = json.load(open("data/elite_members.json"))
    rows = {r["sym"]: r for r in sc["rows"]}
    return [rows[s] for s in sc["bank"] if s in rows and s not in mem and s not in rej]
def propose(test_sym=None):
    p = load(PEND, None)
    if p and p.get("sym") and not test_sym: print("Vorschlag offen:", p["sym"]); return
    mem = json.load(open("data/elite_members.json")); rej = (p or {}).get("rejected", [])
    if test_sym:
        sc = {r["sym"]: r for r in load("data/elite_screen.json", {"rows": []})["rows"]}
        c = sc.get(test_sym) or dict(sym=test_sym, name=test_sym, beta=0, cagr10=0, margin=0, de=0, streak=0, branch="")
        cs = [c]
    else:
        if len(mem) >= SIZE: print("Elite voll, kein Vorschlag"); return
        cs = candidates(rej)
        if not cs:
            if not (p or {}).get("empty_sent"):
                say(f"👑 <b>Elite: {SIZE - len(mem)} Platz frei</b>\nAuf der Bank ist derzeit kein Kandidat (zwei Saisons in Folge bestanden). Der Platz bleibt frei bis zur nächsten Saisonprüfung.")
                save(PEND, dict(sym=None, rejected=rej, empty_sent=True, created=now()))
            return
    c = cs[0]
    t = (f"👑 <b>Elite: Einwechslung{' (TEST)' if test_sym else ''}</b>\n{SIZE - len(mem)} Platz frei. Vorschlag von der Bank:\n\n"
         f"<b>{c['name']}</b> ({c['sym']}, {c.get('branch','')})\n10 Jahre {pct(c['cagr10'])} % p. a. · Beta {str(c['beta']).replace('.', ',')}"
         f" · Marge {pct(c['margin'] or 0)} % · FK/EK {str(c['de']).replace('.', ',')}\nBestanden {c['streak']} Saisons in Folge."
         + (f"\nWeitere Kandidaten: {', '.join(x['name'] for x in cs[1:4])}" if len(cs) > 1 else "")
         + ("\n\nTest: Bestätigen ändert nichts." if test_sym else ""))
    mid = say(t, [{"text": "✅ Einwechseln", "callback_data": f"in:{c['sym']}"}, {"text": "❌ Ablehnen", "callback_data": f"no:{c['sym']}"}])
    save(PEND, dict(sym=c["sym"], name=c["name"], row=c, msg=mid, created=now(), reminded=False, rejected=rej, test=bool(test_sym)))
    print("Vorschlag gesendet:", c["sym"])
def regeln(de, en):
    open("REGELN.md", "a").write(de); open("REGELN.en.md", "a").write(en)
def admit(p):
    c = p["row"]; sym = c["sym"]; d = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    mem = json.load(open("data/elite_members.json")); mem.append(sym); json.dump(mem, open("data/elite_members.json", "w"))
    meta = load("data/elite_meta.json", {}); meta[sym] = dict(name=c["name"], branch=c.get("branch", ""), branch_en=c.get("branch_en", ""), cur=c.get("cur", "USD")); save("data/elite_meta.json", meta)
    subprocess.run([sys.executable, "fetch_elite.py"], check=False)
    # Schattenbuch verketten: Stand jetzt = neue Basis, alle Mitglieder gleich gewichtet ab dem letzten gemeinsamen Kurstag
    fx = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
    px = list(csv.DictReader(open("data/elite.csv")))
    last = next(r for r in reversed(px) if all(r.get(k) for k in mem)); f = fx.get(last["date"]) or fx[max(k for k in fx if k <= last["date"])]
    st = json.load(open("data/elite_state.json")); base = st["rows"][-1]["elite"] if st["rows"] else 1.0
    st["base"] = base; st["p0"] = {k: float(last[k]) / f for k in mem}
    st.setdefault("changes", []).append(dict(date=last["date"], add=[sym], base=base)); save("data/elite_state.json", st)
    fz = json.load(open("data/elite_frozen.json")); fz["rows"] = [r for r in fz["rows"] if r["key"] != sym] + [dict(key=sym, beta=c["beta"], cagr10=c["cagr10"])]; save("data/elite_frozen.json", fz)
    regeln(f"\n## {d}: Elite-Einwechslung (per Telegram bestätigt)\n{c['name']} ({sym}) rückt von der Bank nach: 10 Jahre {pct(c['cagr10'])} % p. a., Beta {str(c['beta']).replace('.', ',')}, Bruttomarge {pct(c['margin'])} %, FK/EK {str(c['de']).replace('.', ',')}, {c['streak']} Saisons in Folge bestanden. Schattenbuch verkettet ab {last['date']} (Basis {str(base).replace('.', ',')}), alle {len(mem)} gleich gewichtet.\n",
           f"\n## {d}: Elite substitution (confirmed via Telegram)\n{c['name']} ({sym}) moves up from the bench: 10 years {c['cagr10']*100:.1f} % p.a., beta {c['beta']}, gross margin {c['margin']*100:.1f} %, debt/equity {c['de']}, passed {c['streak']} seasons in a row. Shadow book chained from {last['date']} (base {base}), all {len(mem)} equally weighted.\n")
    subprocess.run([sys.executable, "elitecheck.py"], check=False); subprocess.run([sys.executable, "watch.py"], check=False)
    for f2 in ("REGELN.md", "REGELN.en.md"):
        open(f"site/{f2}", "w").write(open(f2).read())
    return len(mem)
def poll():
    p = load(PEND, None); off = load(OFF, {"offset": 0})
    res = api("getUpdates", offset=off["offset"], timeout=0, allowed_updates=["callback_query"]).get("result", [])
    for u in res:
        off["offset"] = u["update_id"] + 1; q = u.get("callback_query")
        if not q: continue
        if str(q["from"]["id"]) != USER:
            api("answerCallbackQuery", callback_query_id=q["id"], text="Nur der Betreiber kann entscheiden."); continue
        act, sym = q["data"].split(":", 1)
        if not p or p.get("sym") != sym:
            api("answerCallbackQuery", callback_query_id=q["id"], text="Dieser Vorschlag ist nicht mehr offen."); continue
        api("answerCallbackQuery", callback_query_id=q["id"], text="Wird verarbeitet …")
        try: api("editMessageReplyMarkup", chat_id=USER, message_id=p["msg"], reply_markup={"inline_keyboard": []})
        except Exception: pass
        if p.get("test"):
            say(f"✅ Test: Antwort „{'Einwechseln' if act == 'in' else 'Ablehnen'}“ für {p['name']} empfangen. Es wurde nichts geändert.")
            os.remove(PEND); p = None; continue
        if act == "in":
            n = admit(p); os.remove(PEND); p = None
            say(f"✅ <b>{load('data/elite_meta.json', {}).get(sym, {}).get('name', sym)}</b> ist eingewechselt. Elite {n}, Schattenbuch läuft verkettet weiter, Regelbuch ergänzt.")
        else:
            rej = p.get("rejected", []) + [sym]; os.remove(PEND)
            say(f"❌ {p['name']} abgelehnt.")
            offer(rej); p = load(PEND, None)
    save(OFF, off)
    p = load(PEND, None)
    if p and p.get("sym") and not p.get("reminded") and not p.get("test"):
        age = (datetime.now(timezone.utc) - datetime.strptime(p["created"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)).days
        if age >= 7:
            say(f"⏰ Erinnerung: Der Einwechsel-Vorschlag <b>{p['name']}</b> ist noch offen (Nachricht vom {p['created'][:10]})."); p["reminded"] = True; save(PEND, p)
def offer(rej):
    mem = json.load(open("data/elite_members.json")); cs = candidates(rej)
    if not cs:
        say("Keine weiteren Kandidaten auf der Bank. Der Platz bleibt frei bis zur nächsten Saisonprüfung.")
        save(PEND, dict(sym=None, rejected=rej, empty_sent=True, created=now())); return
    c = cs[0]
    t = (f"👑 <b>Elite: nächster Vorschlag</b>\n<b>{c['name']}</b> ({c['sym']}, {c.get('branch','')})\n10 Jahre {pct(c['cagr10'])} % p. a. · Beta {str(c['beta']).replace('.', ',')}"
         f" · Marge {pct(c['margin'] or 0)} % · FK/EK {str(c['de']).replace('.', ',')}\nBestanden {c['streak']} Saisons in Folge.")
    mid = say(t, [{"text": "✅ Einwechseln", "callback_data": f"in:{c['sym']}"}, {"text": "❌ Ablehnen", "callback_data": f"no:{c['sym']}"}])
    save(PEND, dict(sym=c["sym"], name=c["name"], row=c, msg=mid, created=now(), reminded=False, rejected=rej, test=False))
if __name__ == "__main__":
    if not TOKEN or not USER: raise SystemExit("Telegram-Secrets fehlen")
    a = sys.argv[1] if len(sys.argv) > 1 else "poll"
    if a == "propose": propose()
    elif a == "test": propose(test_sym=sys.argv[2])
    else: poll()
