"""Telegram-Nachricht (optional): nur bei Aktion oder samstags als Wochenrueckblick.
Braucht die Secrets TELEGRAM_BOT_TOKEN und TELEGRAM_CHAT_ID; ohne sie passiert nichts."""
import json, os, urllib.parse, urllib.request
from datetime import datetime, timezone

tok, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
if not (tok and chat):
    raise SystemExit("Telegram nicht eingerichtet - uebersprungen")
h = json.load(open("site/heartbeat.json"))
weekly = datetime.now(timezone.utc).weekday() == 5
if not h["moves"] and not weekly:
    raise SystemExit("keine Aktion, kein Wochenrueckblick")
L = [f"3Kings {h['data_date']}"]
if h["moves"]:
    L.append("AKTION:")
    L += [f"  {m['name']}: {m['von']*100:.0f}% -> {m['auf']*100:.0f}%" for m in h["moves"]]
else:
    L.append("Nichts tun.")
L.append("Bestand: " + ", ".join(f"{v['champion']} {h['held'][k]*100:.0f}%" if False else f"{k} {h['held'][k]*100:.0f}%" for k, v in h["players"].items()) + f", Cash {h['cash']*100:.0f}%")
L.append(f"Schattenbuch {h['shadow']:.3f} vs Halten {h['hold']:.3f}")
L.append(f"Saison: Wahl in {h['season']['days_left']} Handelstagen")
data = urllib.parse.urlencode({"chat_id": chat, "text": "\n".join(L)}).encode()
urllib.request.urlopen(f"https://api.telegram.org/bot{tok}/sendMessage", data, timeout=20)
print("gesendet")
