"""Telegram-Nachricht (optional, vorbereitet). Meldet sich nur, wenn
  1. das Kaufsignal fuer neues Geld wechselt (Kaufen <-> Sammeln), oder
  2. eine seltene Lage eintritt: Shiller-KGV nicht mehr rot UND Fear & Greed Aktien <= 25 (guenstig plus extreme Angst).
Braucht die Secrets TELEGRAM_BOT_TOKEN und TELEGRAM_CHAT_ID; ohne sie passiert nichts. Zustand: data/notify_state.json."""
import json, os, urllib.parse, urllib.request

st_path = "data/notify_state.json"
st = json.load(open(st_path)) if os.path.exists(st_path) else {}
s = json.load(open("site/sparplan.json"))
ind = {i["key"]: i for i in json.load(open("site/indicators.json")).get("indicators", [])} if os.path.exists("site/indicators.json") else {}
msgs = []
import sys
TEST = "--test" in sys.argv
if TEST: msgs.append("🧪 TEST Sparplan S&P 500: So sieht eine Signalmeldung aus, z. B. „Neues Geld jetzt SAMMELN“ oder die seltene Lage „günstig plus extreme Angst“. Nur ein Test.")
if st.get("signal") and st["signal"] != s["signal"]:
    msgs.append(f"3Kings: Neues Geld jetzt {s['signal'].upper()}. S&P 500 {abs(s['dd_ath'])*100:.1f} % unter dem Allzeithoch ({s['currency']}).")
cheap_fear = ind.get("cape", {}).get("light") not in (None, "rot") and ind.get("fng", {}).get("light") == "gruen"
if cheap_fear and not st.get("cheap_fear"):
    msgs.append("3Kings: Seltene Lage - Bewertung nicht mehr teuer und extreme Angst im Markt.")
if not TEST:
    st.update(signal=s["signal"], cheap_fear=cheap_fear)
    json.dump(st, open(st_path, "w"))
tok, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
if not msgs:
    raise SystemExit("keine Meldung noetig")
if not (tok and chat):
    raise SystemExit("Telegram nicht eingerichtet - waere gemeldet worden: " + " | ".join(msgs))
user = next((c.strip() for c in chat.split(",") if c.strip() and not c.strip().startswith("-")), None)  # nur privat
for m in msgs:
    urllib.request.urlopen(f"https://api.telegram.org/bot{tok}/sendMessage", urllib.parse.urlencode(dict(chat_id=user, text=m)).encode(), timeout=20)
print("gesendet:", msgs)
