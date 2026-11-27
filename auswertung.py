"""Automatische Auswertung der Vorwärtstests (REGELN 2026-11-22, Regeln vorab). Läuft täglich; rechnet jeden Test einmal an/nach seinem Termin,
schreibt einen Protokolleintrag und meldet privat. Zustand: data/auswertung_state.json. --selftest rechnet die Funktionen auf alten Jahren."""
import csv, json, os, sys, datetime as dt, urllib.parse, urllib.request
import netz
import numpy as np
ST = "data/auswertung_state.json"
def daily(path):
    out = []
    for r in list(csv.reader(open(path)))[1:]:
        if len(r) > 1 and r[1]:
            try: out.append((dt.date.fromisoformat(r[0]), float(r[1])))
            except Exception: pass
    return sorted(out)
def month_close(d):
    o = {}
    for day, v in d: o[day.strftime("%Y-%m")] = v
    return o
def monatswechsel(spx, y0):
    """24 Fenster: letzter Handelstag der Monate (Nov y0) bis (Okt y0+2) plus je die ersten drei des Folgemonats."""
    dates = [d for d, _ in spx]; P = np.array([v for _, v in spx]); ret = P[1:] / P[:-1] - 1; rd = dates[1:]
    mk = [d.strftime("%Y-%m") for d in rd]; idx = {}
    for i, m in enumerate(mk): idx.setdefault(m, []).append(i)
    months = [f"{y0}-11", f"{y0}-12"] + [f"{y0 + 1}-{k:02d}" for k in range(1, 13)] + [f"{y0 + 2}-{k:02d}" for k in range(1, 11)]
    flag = np.zeros(len(ret), bool); wins = []
    for j, m in enumerate(months):
        nxt = f"{y0 + 2}-11" if m == f"{y0 + 2}-10" else months[j + 1] if j + 1 < len(months) else None
        if m not in idx or nxt not in idx or len(idx[nxt]) < 3: return None
        w = [idx[m][-1]] + idx[nxt][:3]; flag[w] = True; wins.append(w)
    lo = wins[0][0]; hi = wins[-1][-1]; sel = np.zeros(len(ret), bool); sel[lo:hi + 1] = True
    half = np.zeros(len(ret), bool); half[lo:wins[12][0]] = True; h2 = sel & ~half
    def diff(mask): return float(ret[mask & flag].mean() - ret[mask & ~flag].mean())
    d_all, d1, d2 = diff(sel), diff(half), diff(h2)
    return dict(diff=d_all, y1=d1, y2=d2, holds=bool(d_all >= .0005 and d1 > 0 and d2 > 0))
def monatsplus(closes, years, a, b, thr_mean):
    """Rendite Monatsschluss a (Vormonat) bis Monatsschluss b je Jahr; a, b = Monatszahlen (11,12 oder 9,10)."""
    r = []
    for y in years:
        pa = closes.get(f"{y - 1 if a > b else y}-{a:02d}"); pb = closes.get(f"{y}-{b:02d}")
        if pa is None or pb is None: return None
        r.append(pb / pa - 1)
    return dict(returns=r, mean=float(np.mean(r)), pos=int(sum(x > 0 for x in r)), holds=bool(sum(x > 0 for x in r) >= 2 and np.mean(r) >= thr_mean))
def pct(x, d=1, en=False):
    t = f"{x*100:+.{d}f} %".replace("-", "−")
    return t if en else t.replace(".", ",")
def nd(x, d=3, en=False):
    t = f"{x*100:+.{d}f}".replace("-", "−")
    return t if en else t.replace(".", ",")
def entry(key, res):
    d = dt.date.today().isoformat(); h = "hält" if res["holds"] else "hält nicht"; he = "holds" if res["holds"] else "does not hold"
    if key == "monatswechsel":
        tde, ten = "Vorwärtstest Monatswechsel (S&P 500): Ergebnis, automatisch ausgewertet", "Forward test turn of the month (S&P 500): result, evaluated automatically"
        bde = f"24 Fenster (November 2026 bis Oktober 2028), Regeln vom 22.11.2026 unverändert: Unterschied der Tagesrendite {nd(res['diff'])} Prozentpunkte (Schwelle 0,05), erstes Jahr {nd(res['y1'])}, zweites Jahr {nd(res['y2'])}. Das Muster {h}. Keine Änderung der Kaufregel. Keine Empfehlung."
        ben = f"24 windows (November 2026 to October 2028), rules of 22.11.2026 unchanged: difference in daily return {nd(res['diff'], 3, True)} percentage points (threshold 0.05), first year {nd(res['y1'], 3, True)}, second year {nd(res['y2'], 3, True)}. The pattern {he}. No change to the buy rule. No recommendation."
    else:
        dec = key == "dezember"
        tde = "Vorwärtstest " + ("Dezember (S&P 500, 2026 bis 2028)" if dec else "Bitcoin im Oktober (2027 bis 2029)") + ": Ergebnis, automatisch ausgewertet"
        ten = "Forward test " + ("December (S&P 500, 2026 to 2028)" if dec else "bitcoin in October (2027 to 2029)") + ": result, evaluated automatically"
        th = "+0,5 %" if dec else "+5 %"
        bde = f"Regeln vom 22.11.2026 unverändert: Renditen {'; '.join(pct(x) for x in res['returns'])}; {res['pos']} von 3 Jahren positiv, Mittel {pct(res['mean'])} (Schwelle: mindestens 2 von 3 positiv und Mittel mindestens {th}). Das Muster {h}. Keine Änderung der Kaufregel. Keine Empfehlung."
        ben = f"Rules of 22.11.2026 unchanged: returns {'; '.join(pct(x, 1, True) for x in res['returns'])}; {res['pos']} of 3 years positive, mean {pct(res['mean'], 1, True)} (threshold: at least 2 of 3 positive and mean at least {th.replace(',', '.')}). The pattern {he}. No change to the buy rule. No recommendation."
    return f"\n## {d}: {tde}\n{bde}\n", f"\n## {d}: {ten}\n{ben}\n", tde, bde
def private(msg):
    tok, ids = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID", "")
    user = next((c.strip() for c in ids.split(",") if c.strip() and not c.strip().startswith("-")), None)
    if tok and user: netz.oeffne(f"https://api.telegram.org/bot{tok}/sendMessage", urllib.parse.urlencode(dict(chat_id=user, text=msg, parse_mode="HTML")).encode(), timeout=20)
    else: print("[ohne Telegram]", msg)
if __name__ == "__main__":
    spx = daily("data/spx_long.csv"); btc = daily("data/btc_long.csv")
    if "--selftest" in sys.argv:
        print("Monatswechsel (Test auf 2019-11 bis 2021-10):", monatswechsel(spx, 2019)); print("Dezember 2017-2019:", monatsplus(month_close(spx), [2017, 2018, 2019], 11, 12, .005))
        print("Oktober Bitcoin 2018-2020:", monatsplus(month_close(btc), [2018, 2019, 2020], 9, 10, .05)); sys.exit()
    st = json.load(open(ST)) if os.path.exists(ST) else {}; today = dt.date.today().isoformat()
    jobs = [("monatswechsel", "2028-11-08", lambda: monatswechsel(spx, 2026)), ("dezember", "2029-01-05", lambda: monatsplus(month_close(spx), [2026, 2027, 2028], 11, 12, .005)),
            ("oktober", "2029-11-15", lambda: monatsplus(month_close(btc), [2027, 2028, 2029], 9, 10, .05))]
    for key, date, fn in jobs:
        if st.get(key) or today < date: continue
        res = fn()
        if res is None: print(key, "Daten noch unvollständig, später erneut"); continue
        de, en, tde, bde = entry(key, res)
        for f, t in (("REGELN.md", de), ("REGELN.en.md", en), ("site/REGELN.md", de), ("site/REGELN.en.md", en)): open(f, "a").write(t)
        private("🔬 <b>" + tde + "</b>\n" + bde + "\nDetails im Protokoll.")
        st[key] = dict(date=today, result=res); print("ausgewertet:", key)
    json.dump(st, open(ST, "w"), indent=1, default=str)
