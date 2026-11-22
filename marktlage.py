"""Marktlage-Meldungen an den Kanal (REGELN 2026-11-22): Ampel-Wechsel und Bitcoin-Power-Law-Monatsschluss. Nur Information.
Zustand: data/marktlage_state.json. Ohne Telegram-Secrets (oder mit --dry) wird nur ausgegeben. --selftest simuliert Wechsel."""
import csv, json, os, sys, urllib.parse, urllib.request
ST = "data/marktlage_state.json"
NAME = dict(oil_m="Öl (Monatsänderung)", us10y="US-Zins 10 Jahre", ecb="EZB-Einlagenzins", cpi_us="Inflation USA", cpi_ez="Inflation Eurozone",
            fng="Angst und Gier Aktien", cfng="Angst und Gier Krypto", vix="VIX", cape="Shiller-KGV", buffett="Buffett-Indikator", curve="Zinskurve 10 J − 2 J",
            spx_d="S&P 500 Tagesänderung", btc_d="Bitcoin Tagesänderung", gold_d="Gold Tagesänderung")
SLOW = ["oil_m", "us10y", "ecb", "cpi_us", "cpi_ez", "fng", "cfng", "vix", "cape", "buffett", "curve"]; DAILY = ["spx_d", "btc_d", "gold_d"]
COL = dict(g="grün", y="gelb", r="rot", **{"": "ohne Farbe"})
PCT = {"oil_m", "cpi_us", "cpi_ez", "spx_d", "btc_d", "gold_d"}
FOOT = "Nur Information, kein Kauf- oder Verkaufssignal."
def fmt(k, x):
    try: x = float(x)
    except Exception: return "?"
    return (f"{x*100:+.1f} %".replace(".", ",").replace("-", "−")) if k in PCT else f"{x:.2f}".replace(".", ",").rstrip("0").rstrip(",")
def messages(rows, pl, st):
    """rows: Zeilen aus barometer.csv (dict), pl: powerlaw.json. Gibt (Meldungen, neuer Zustand) zurück."""
    msgs = []; st = json.loads(json.dumps(st)); last = rows[-1]; prev = rows[-2] if len(rows) > 1 else None
    first = "conf" not in st
    conf = st.setdefault("conf", {k: last.get(k + "_c", "") for k in SLOW}); pend = st.setdefault("pend", {})
    lines = []
    if first: st["daily_date"] = last["date"]
    if not first:
        for k in SLOW:
            new = last.get(k + "_c", "")
            if new == conf.get(k, ""): pend.pop(k, None); continue
            if pend.get(k) == new:   # zweiter Datentag in Folge
                lines.append(f"{NAME[k]}: {COL[conf.get(k, '')]} → {COL[new]} ({fmt(k, last.get(k))})"); conf[k] = new; pend.pop(k, None)
            else: pend[k] = new
        if st.get("daily_date") != last["date"]:
            for k in DAILY:
                if prev is not None and last.get(k + "_c") == "r" and prev.get(k + "_c") != "r":
                    lines.append(f"{NAME[k]}: {fmt(k, last.get(k))} (Kachel rot)")
            st["daily_date"] = last["date"]
    if lines: msgs.append("🚦 <b>Marktlage</b>\n" + "\n".join("• " + l for l in lines) + f"\nAmpel jetzt: {last.get('n_red', '?')} rot, {last.get('n_green', '?')} grün.\n" + FOOT)
    lm = (pl or {}).get("last_month") or {}
    if lm.get("final"):
        if "pl_below" not in st: st["pl_below"] = bool(lm["below"]); st["pl_m"] = lm["m"]
        elif lm["m"] != st.get("pl_m"):
            if bool(lm["below"]) != st["pl_below"]:
                msgs.append("₿ <b>Bitcoin Power Law, Monatsschluss " + lm["m"][5:] + "." + lm["m"][:4] + "</b>\n" + (f"Schluss {lm['close']:,} $ unter der Untergrenze ({lm['floor']:,} $): Untergrenze in diesem Monat gebrochen.".replace(",", ".") if lm["below"] else f"Schluss {lm['close']:,} $ wieder über der Untergrenze ({lm['floor']:,} $).".replace(",", ".")) + "\n" + FOOT)
            st["pl_below"] = bool(lm["below"]); st["pl_m"] = lm["m"]
    return msgs, st
def send(msgs):
    tok, ids = os.environ.get("TELEGRAM_BOT_TOKEN"), [c.strip() for c in os.environ.get("TELEGRAM_CHAT_ID", "").split(",") if c.strip()]
    if not (tok and ids) or "--dry" in sys.argv:
        for m in msgs: print("[Trockenlauf]", m.replace("\n", " | "))
        return
    for m in msgs:
        for c in ids:
            try: urllib.request.urlopen(f"https://api.telegram.org/bot{tok}/sendMessage", urllib.parse.urlencode(dict(chat_id=c, text=m, parse_mode="HTML", disable_web_page_preview="true")).encode(), timeout=20)
            except Exception as e: print("Fehler bei", c, e)
if __name__ == "__main__":
    rows = list(csv.DictReader(open("data/barometer.csv"))); pl = json.load(open("site/powerlaw.json"))
    st = json.load(open(ST)) if os.path.exists(ST) else {}
    if "--selftest" in sys.argv:
        import copy; r2 = copy.deepcopy(rows[-1]); r2["date"] = "2099-01-01"; r2["vix_c"] = "y"; r2["spx_d_c"] = "r"; r2["n_red"] = 9
        m, s = messages(rows + [r2], pl, {"conf": {k: rows[-1].get(k + "_c", "") for k in SLOW}, "pend": {}}); print("Tag 1:", m)
        r3 = copy.deepcopy(r2); r3["date"] = "2099-01-02"; m, s = messages(rows + [r2, r3], pl, s); print("Tag 2:", m)
        pl2 = json.loads(json.dumps(pl)); pl2["last_month"] = dict(m="2099-02", close=60000, floor=66000, below=not pl["last_month"]["below"], final=True)
        m, s = messages(rows, pl2, dict(s, pl_below=bool(pl["last_month"]["below"]), pl_m="2099-01")); print("PL:", m); sys.exit()
    msgs, st = messages(rows, pl, st); json.dump(st, open(ST, "w"), ensure_ascii=False, indent=1)
    send(msgs) if msgs else print("keine Marktlage-Meldung")
