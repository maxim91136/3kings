"""Telegram: schickt neue News (site/news.json) und neue Berichte (site/reports.json) an den Bot.
Modus 'setup': zeigt die Chat-ID(s) aus getUpdates. Braucht TELEGRAM_BOT_TOKEN (und TELEGRAM_CHAT_ID zum Senden).
Zustand (was schon gesendet wurde): data/tg_sent.json."""
import json, os, sys, urllib.parse, urllib.request
tok, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
LANG = os.environ.get("TG_LANG", "de")
SITE = "https://3kings.dev"
if not tok: sys.exit("TELEGRAM_BOT_TOKEN fehlt (GitHub Secret anlegen)")
def api(method, **kw):
    data = urllib.parse.urlencode(kw).encode() if kw else None
    return json.load(urllib.request.urlopen(f"https://api.telegram.org/bot{tok}/{method}", data, timeout=20))
if len(sys.argv) > 1 and sys.argv[1] == "setup":
    ups = api("getUpdates").get("result", [])
    ids = {f'{c.get("id")} ({c.get("type")}{": " + c["title"] if c.get("title") else ""})' for u in ups for c in [(u.get("message") or u.get("channel_post") or u.get("my_chat_member") or {}).get("chat", {})] if c.get("id")}
    print("Chat-IDs:", ", ".join(map(str, ids)) if ids else "keine - erst dem Bot eine Nachricht schreiben (z. B. /start)")
    sys.exit()
if not chat: sys.exit("TELEGRAM_CHAT_ID fehlt (GitHub Secret anlegen)")
def esc(s):
    s = str(s).replace("€/oz", " € je Unze" if LANG == "de" else " € per oz").replace("$/oz", " $ je Unze" if LANG == "de" else " $ per oz").replace("/oz", " je Unze" if LANG == "de" else " per oz")
    s = s.replace("  ", " ").replace("€ € ", "€ ")
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def public(l):  # Schattenbücher nicht in Telegram; Kronjuwelen (öffentlicher Index) dürfen in Berichte
    return not any(w in l for w in ("Schattenbuch", "Schattenbücher", "shadow book", "Shadow book", "Chronik", "Chroniken", "chronicle", "Chronicle", "Elite 6"))
st_path = "data/tg_sent.json"
TEST = len(sys.argv) > 1 and sys.argv[1] == "test"
st = {} if TEST else (json.load(open(st_path)) if os.path.exists(st_path) else {})
en = LANG == "en"
out = []
if os.path.exists("site/news.json"):
    it = json.load(open("site/news.json")).get("items", [])
    if it:
        x = it[0]; key = f"{x.get('date')}|{str(x.get('headline','')).startswith('Wochenende')}"
        if st.get("news") != key:
            hl = x.get("headline_en") if en and x.get("headline_en") else x.get("headline", "")
            ln = x.get("lines_en") if en and x.get("lines_en") else x.get("lines", [])
            icon = "🔶" if x.get("move") else "👑"
            from datetime import date as _d
            y_, m_, d_ = map(int, str(x.get("date", "2000-01-01")).split("-"))
            dt = _d(y_, m_, d_)
            wd = (["Mo.", "Di.", "Mi.", "Do.", "Fr.", "Sa.", "So."] if not en else ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])[dt.weekday()]
            weekend = str(x.get("headline", "")).startswith("Wochenende")
            if en: head = f"📅 {'Bitcoin weekend' if weekend else 'Trading day'} {wd}, {dt.strftime('%b')} {dt.day}, {dt.year}"
            else: head = f"📅 {'Bitcoin am Wochenende' if weekend else 'Börsentag'} {wd}, {dt:%d.%m.%Y}"
            src = "\n".join(f'<a href="{esc(s["url"])}">{esc(s["title"])}</a>' for s in x.get("sources", [])[:3])
            out.append(("news", key, f"<i>{head}</i>\n{icon} <b>{esc(hl)}</b>\n\n" + "\n\n".join(esc(l) for l in ln if public(l)) + (f"\n\n{src}" if src else "")))
if os.path.exists("site/reports.json"):
    for x in ([] if TEST else reversed(json.load(open("site/reports.json")).get("items", [])[:2])):
        key = f"{x.get('type')}|{x.get('period')}|{x.get('published')}"
        if key in st.get("reports", []): continue
        ti = x.get("title_en") if en and x.get("title_en") else x.get("title", "")
        ln = x.get("lines_en") if en and x.get("lines_en") else x.get("lines", [])
        kind = ("Annual report" if x.get("type") == "year" else "Monthly report") if en else ("Jahresbericht" if x.get("type") == "year" else "Monatsbericht")
        body = "\n".join(f"\n<b>{esc(l[2:])}</b>" if l.startswith("# ") else esc(l) for l in ln if public(l) and not l.startswith(("# Elite", "# Schattenb", "# Shadow", "# Chronik", "# Chronicle")))
        out.append(("report", key, f"📊 <b>{kind} {esc(ti)}</b>\n{body}"))
for kind, key, text in out:
    for i in range(0, len(text), 3900):
        for c in [c.strip() for c in chat.split(",") if c.strip()]:
            try: api("sendMessage", chat_id=c, text=text[i:i + 3900], parse_mode="HTML", disable_web_page_preview="true")
            except Exception as e: print("Fehler bei", c, e)
    if kind == "news": st["news"] = key
    else: st.setdefault("reports", []).append(key); st["reports"] = st["reports"][-50:]
    print("gesendet:", kind, key)
if not TEST: json.dump(st, open(st_path, "w"), indent=1)
if not out: print("nichts Neues")
