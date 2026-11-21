"""Testet die drei privaten Telegram-Meldungen (Taktikmodell, Kronjuwelen, Sparplan S&P 500). Ändert keinen Zustand."""
import json, subprocess, sys
json.dump(["🧪 <b>TEST Taktikmodell 3 Könige (Simulation)</b>\nSignal zum Schlusskurs vom 20.11.2026:\nS&P 500: 49 % → 0 % (verkaufen)\nUmsetzung am nächsten Handelstag. Nur ein Test.",
           "🧪 <b>TEST Kronjuwelen: Saisonprüfung</b>\n➕ Neu: Beispiel AG → Sparplan starten\n➖ Raus: Muster Inc → Sparplan stoppen, NICHT verkaufen\nJetzt 11 Werte, Rate gleich verteilt (je 1/11). Nur ein Test."],
          open("data/elite_notify.json", "w"), ensure_ascii=False)
subprocess.run([sys.executable, "elite_bank.py", "notify"], check=True)
subprocess.run([sys.executable, "notify.py", "--test"], check=True)
print("drei Testmeldungen gesendet")
