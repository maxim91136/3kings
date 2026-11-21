"""Kronjuwelen: Aufnahme per Telegram-Bestätigung (REGELN.md 2026-11-21).
  python elite_bank.py propose   -> nächsten aufnahmereifen Kandidaten aus der Warteschlange privat vorschlagen (wenn keiner offen)
  python elite_bank.py poll      -> Antworten abholen (nur privater Chat), Aufnehmen/Ablehnen, Erinnerung nach 7 Tagen, dann nächster
  python elite_bank.py test SYM  -> Testvorschlag (Bestätigung ändert nichts)
Zustand: data/elite_pending.json {queue, current, rejected, season}, Offset: data/tg_offset.json."""
import csv, json, os, subprocess, sys, urllib.parse, urllib.request
from datetime import datetime, timezone
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", ""); IDS = [c.strip() for c in os.environ.get("TELEGRAM_CHAT_ID", "").split(",") if c.strip()]
USER = next((c for c in IDS if not c.startswith("-")), None)
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
def num(x, pc=False): return "–" if x is None else (f"{x*100:.1f}" if pc else f"{x}").replace(".", ",")
def row(sym):
    return next((r for r in load("data/elite_screen.json", {"rows": []})["rows"] if r["sym"] == sym), None)
def card(c, head):
    return (f"💎 <b>{head}</b>\n<b>{c['name']}</b> ({c['sym']}, {c.get('branch','')})\n10 Jahre {num(c.get('cagr10'), True)} % p. a. · Beta {num(c.get('beta'))}"
            f" · Marge {num(c.get('margin'), True)} % · Nettoverschuldung {num(c.get('nd_ebitda'))}× EBITDA\nAlle Regeln {c.get('streak', 0)} Saisons in Folge bestanden.")
def btn(sym): return [{"text": "✅ Aufnehmen", "callback_data": f"in:{sym}"}, {"text": "❌ Ablehnen", "callback_data": f"no:{sym}"}]
def propose():
    q = load(PEND, {"queue": []})
    if q.get("current"): print("Vorschlag offen:", q["current"]["sym"]); return
    mem = json.load(open("data/elite_members.json"))
    while q.get("queue"):
        sym = q["queue"].pop(0); c = row(sym)
        if not c or sym in mem or sym in q.get("rejected", []): continue
        rest = [x for x in q["queue"] if x not in mem]
        mid = say(card(c, "Kronjuwelen: Aufnahme vorschlagen") + (f"\nDanach in der Warteschlange: {len(rest)}" if rest else ""), btn(sym))
        q["current"] = dict(sym=sym, row=c, msg=mid, created=now(), reminded=False, test=False); save(PEND, q); print("Vorschlag:", sym); return
    save(PEND, q); print("Warteschlange leer")
def test(sym):
    q = load(PEND, {"queue": []}); c = row(sym) or dict(sym=sym, name=sym)
    mid = say(card(c, "Kronjuwelen: Aufnahme (TEST)") + "\n\nTest: Die Antwort ändert nichts.", btn(sym))
    q["current"] = dict(sym=sym, row=c, msg=mid, created=now(), reminded=False, test=True); save(PEND, q)
def regeln(de, en):
    for f, t in (("REGELN.md", de), ("REGELN.en.md", en)):
        open(f, "a").write(t); open(f"site/{f}", "w").write(open(f).read())
def admit(c):
    sym = c["sym"]; d = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    mem = json.load(open("data/elite_members.json")); mem.append(sym); json.dump(mem, open("data/elite_members.json", "w"))
    meta = load("data/elite_meta.json", {}); meta[sym] = dict(name=c["name"], branch=c.get("branch", ""), branch_en=c.get("branch_en", ""), cur=c.get("cur", "USD")); save("data/elite_meta.json", meta)
    subprocess.run([sys.executable, "fetch_elite.py"], check=False)
    fx = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
    px = list(csv.DictReader(open("data/elite.csv")))
    last = next(r for r in reversed(px) if all(r.get(k) for k in mem)); f = fx.get(last["date"]) or fx[max(k for k in fx if k <= last["date"])]
    st = json.load(open("data/elite_state.json")); base = st["rows"][-1]["elite"] if st["rows"] else 1.0
    st["base"] = base; st["p0"] = {k: float(last[k]) / f for k in mem}
    st.setdefault("changes", []).append(dict(date=last["date"], add=[sym], base=base)); save("data/elite_state.json", st)
    fz = json.load(open("data/elite_frozen.json")); fz["rows"] = [r for r in fz["rows"] if r["key"] != sym] + [dict(key=sym, beta=c.get("beta"), cagr10=c.get("cagr10"))]; save("data/elite_frozen.json", fz)
    vals = f"10 J. {num(c.get('cagr10'), True)} % p. a., Beta {num(c.get('beta'))}, Bruttomarge {num(c.get('margin'), True)} %, Nettoverschuldung {num(c.get('nd_ebitda'))}× EBITDA"
    regeln(f"\n## {d}: Kronjuwelen-Aufnahme (per Telegram bestätigt)\n{c['name']} ({sym}): {vals}, alle Regeln {c.get('streak')} Saisons in Folge bestanden. Schattenbuch verkettet ab {last['date']}, alle {len(mem)} gleich gewichtet.\n",
           f"\n## {d}: Crown Jewels admission (confirmed via Telegram)\n{c['name']} ({sym}): 10 yrs {(c.get('cagr10') or 0)*100:.1f} % p.a., beta {c.get('beta')}, gross margin {(c.get('margin') or 0)*100:.1f} %, net debt {c.get('nd_ebitda')}x EBITDA, passed all rules {c.get('streak')} seasons in a row. Shadow book chained from {last['date']}, all {len(mem)} equally weighted.\n")
    subprocess.run([sys.executable, "elitecheck.py"], check=False); subprocess.run([sys.executable, "watch.py"], check=False)
    return len(mem)
def poll():
    q = load(PEND, {"queue": []}); off = load(OFF, {"offset": 0})
    for u in api("getUpdates", offset=off["offset"], timeout=0, allowed_updates=["callback_query"]).get("result", []):
        off["offset"] = u["update_id"] + 1; save(OFF, off); cq = u.get("callback_query")
        if not cq: continue
        if str(cq["from"]["id"]) != USER: api("answerCallbackQuery", callback_query_id=cq["id"], text="Nur der Betreiber kann entscheiden."); continue
        act, sym = cq["data"].split(":", 1); cur = q.get("current")
        if not cur or cur["sym"] != sym: api("answerCallbackQuery", callback_query_id=cq["id"], text="Dieser Vorschlag ist nicht mehr offen."); continue
        api("answerCallbackQuery", callback_query_id=cq["id"], text="Wird verarbeitet …")
        try: api("editMessageReplyMarkup", chat_id=USER, message_id=cur["msg"], reply_markup={"inline_keyboard": []})
        except Exception: pass
        q["current"] = None; save(PEND, q)
        if cur.get("test"): say(f"✅ Test: Antwort „{'Aufnehmen' if act == 'in' else 'Ablehnen'}“ für {cur['row']['name']} empfangen. Nichts geändert."); continue
        if act == "in": n = admit(cur["row"]); say(f"💎 <b>{cur['row']['name']}</b> ist aufgenommen. Kronjuwelen: {n} Werte. Schattenbuch verkettet, Regelbuch ergänzt.")
        else:
            q.setdefault("rejected", []).append(sym); save(PEND, q); say(f"❌ {cur['row']['name']} abgelehnt (bis zur nächsten Saisonprüfung).")
            d = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            regeln(f"\n## {d}: Kronjuwelen: Aufnahme abgelehnt (per Telegram)\n{cur['row']['name']} ({sym}) erfüllt die Regeln, Aufnahme ausdrücklich abgelehnt. Erneuter Vorschlag frühestens zur nächsten Saisonprüfung.\n",
                   f"\n## {d}: Crown Jewels: admission rejected (via Telegram)\n{cur['row']['name']} ({sym}) meets the rules; admission explicitly rejected. Proposed again at the next season review at the earliest.\n")
        q = load(PEND, {"queue": []}); propose(); q = load(PEND, {"queue": []})
    save(OFF, off)
    cur = q.get("current")
    if cur and not cur.get("reminded") and not cur.get("test"):
        if (datetime.now(timezone.utc) - datetime.strptime(cur["created"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)).days >= 7:
            say(f"⏰ Erinnerung: Aufnahme-Vorschlag <b>{cur['row']['name']}</b> ist noch offen (seit {cur['created'][:10]})."); cur["reminded"] = True; save(PEND, q)
if __name__ == "__main__":
    if not TOKEN or not USER: raise SystemExit("Telegram-Secrets fehlen")
    a = sys.argv[1] if len(sys.argv) > 1 else "poll"
    if a == "propose": propose()
    elif a == "test": test(sys.argv[2])
    else: poll()
