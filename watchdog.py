"""Wächter (seit 2026-11-21): prüft jeden Morgen, ob die Automatik gelaufen ist, und meldet Ausfälle privat per Telegram.
Prüft über die GitHub-API die letzten Änderungen an site/heartbeat.json (nächtlicher Datenlauf) und site/news.json (News-Monitor),
das Datum der Kurse und am Monatsanfang den Monatsbericht. Sonntags kurze Lebensmeldung. --test: Meldung immer senden."""
import json, os, subprocess, sys, urllib.parse, urllib.request
from datetime import datetime, timezone, timedelta, date
REPO = "maxim91136/3kings"; now = datetime.now(timezone.utc)
def last_commit(path):
    out = subprocess.run(["gh", "api", f"repos/{REPO}/commits?path={path}&per_page=1", "-q", ".[0].commit.committer.date"], capture_output=True, text=True).stdout.strip()
    return datetime.fromisoformat(out.replace("Z", "+00:00")) if out else None
def hours(t): return None if t is None else (now - t).total_seconds() / 3600
problems = []
hb = last_commit("site/heartbeat.json"); h = hours(hb)
lim = 60 if now.weekday() in (6, 0) else 26   # Datenlauf nur Di-Sa (nach US-Handelstagen): So/Mo längere Pause normal
if h is None or h > lim: problems.append(f"Nächtlicher Datenlauf: letzte Aktualisierung vor {'?' if h is None else round(h)} Stunden.")
try:
    dd = json.load(open("site/heartbeat.json"))["data_date"]
    age = (now.date() - date.fromisoformat(dd)).days
    if age > 4: problems.append(f"Kurse veraltet: letzter Kurstag {dd} ({age} Tage).")
except Exception as e: problems.append(f"heartbeat.json nicht lesbar: {e}")
nw = hours(last_commit("site/news.json"))
if nw is None or nw > 26: problems.append(f"News-Monitor: letzte Meldung vor {'?' if nw is None else round(nw)} Stunden.")
if now.day <= 3:
    pm = (now.replace(day=1) - timedelta(days=1)).strftime("%Y-%m")
    if now.day > 1 or now.hour >= 10:
        rep = json.load(open("site/reports.json")) if os.path.exists("site/reports.json") else {"items": []}
        if not any(x.get("type") == "month" and x.get("period") == pm for x in rep.get("items", [])):
            problems.append(f"Monatsbericht für {pm} fehlt.")
# Erweiterung (REGELN 2026-11-22): Workflows und Dateien, weil Schritte im Datenlauf Fehler verschlucken
for wf in ("heartbeat", "btclive"):
    out = subprocess.run(["gh", "run", "list", "-R", REPO, "--workflow", f"{wf}.yml", "-L", "1", "--json", "conclusion,createdAt", "-q", ".[0].conclusion"], capture_output=True, text=True).stdout.strip()
    if out == "failure": problems.append(f"Workflow {wf}: letzter Lauf gescheitert.")
for pth in ("site/calendar.json", "data/barometer.csv", "site/assets.json", "site/powerlaw.json"):
    hh = hours(last_commit(pth))
    if hh is None or hh > lim: problems.append(f"{pth}: letzte Aktualisierung vor {'?' if hh is None else round(hh)} Stunden.")
try:
    se = json.load(open("site/heartbeat.json")).get("season", {})
    if (se.get("day_in_season") or 0) > 63 or (se.get("days_left") is not None and se["days_left"] < 0): problems.append("Saisonprüfung überfällig (Saisontag über 63).")
except Exception: pass
msg = None
if problems: msg = "🚨 <b>3Kings: Wächter</b>\n" + "\n".join("• " + p for p in problems) + "\nDie Seite zeigt so lange den letzten Stand."
elif now.weekday() == 6 or "--test" in sys.argv: msg = "✅ <b>3Kings: Wächter</b>\nAlles läuft: Datenlauf, Kurse und News sind aktuell." + (" (Test)" if "--test" in sys.argv else "")
print(msg or "alles ok, keine Meldung")
tok, ids = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID", "")
user = next((c.strip() for c in ids.split(",") if c.strip() and not c.strip().startswith("-")), None)
if msg and tok and user:
    urllib.request.urlopen(f"https://api.telegram.org/bot{tok}/sendMessage", urllib.parse.urlencode(dict(chat_id=user, text=msg, parse_mode="HTML")).encode(), timeout=20)
