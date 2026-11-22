"""Prüfkalender (REGELN 2026-11-22): nächste vorab festgelegte Prüftermine mit Datum, für die Countdown-Karte. Schreibt site/calendar.json."""
import datetime as dt, json
H = {"2026-11-26", "2026-12-25", "2027-01-01", "2027-01-18", "2027-02-15", "2027-03-26", "2027-05-31", "2027-06-18", "2027-07-05",
     "2027-09-06", "2027-11-25", "2027-12-24"}   # US-Börsenfeiertage (NYSE), bei Bedarf ergänzen
h = json.load(open("site/heartbeat.json")); s = h.get("season", {})
base = dt.date.fromisoformat(h.get("data_date") or h.get("moves_date") or dt.date.today().isoformat())
def trading_days_after(d, n):
    while n > 0:
        d += dt.timedelta(days=1)
        if d.weekday() < 5 and d.isoformat() not in H: n -= 1
    return d
today = dt.date.today()
nxt_season = trading_days_after(base, int(s.get("days_left", 0))) if s.get("days_left") is not None else None
nm = (today.replace(day=1) + dt.timedelta(days=32)).replace(day=1)
eom = nm - dt.timedelta(days=1)
items = [
 dict(date=str(eom), de="Bitcoin Power Law: Monatsschluss entscheidet, ob die Untergrenze hält", en="Bitcoin power law: the monthly close decides whether the floor holds"),
 dict(date=str(nm), de="Monatsbericht (jeden Monat am 1.)", en="Monthly report (on the 1st of every month)"),
 dict(date=f"{today.year + 1}-01-01", de=f"Jahresbericht {today.year} (am 1. Januar)", en=f"Annual report {today.year} (on January 1)"),
]
if nxt_season: items.append(dict(date=str(nxt_season), approx=True, de=f"Saisonprüfung {s.get('n_seasons', 0) + 1}: Kronjuwelen, Talent Scouting, Taktikmodell (noch {s.get('days_left')} Handelstage)",
                                 en=f"Season review {s.get('n_seasons', 0) + 1}: Crown Jewels, Talent Scouting, tactical model ({s.get('days_left')} trading days left)"))
items += [
 dict(date="2027-11-20", de="Erste Bewertung: Barometer-Thesen A–D, These E (schwach gegen stark), These F (200-Tage-Linie), Taktikmodell, Sparplan S&P 500, Trendportfolio",
      en="First verdict: barometer hypotheses A–D, hypothesis E (weak vs strong), hypothesis F (200-day line), tactical model, S&P 500 savings plan, trend portfolio"),
 dict(date="2027-11-20", de="Bewertung Chronik Einmalanlage S&P 500: sofort, 12 Raten, Warten auf −20 %", en="Verdict chronicle S&P 500 lump sum: immediately, 12 instalments, waiting for −20 %"),
 dict(date="2028-11-08", approx=True, de="Vorwärtstest Monatswechsel (S&P 500): 24 Fenster, Bewertung", en="Forward test turn of the month (S&P 500): 24 windows, verdict"),
 dict(date="2029-01-05", approx=True, de="Vorwärtstest Dezember (S&P 500): 2026 bis 2028, Bewertung", en="Forward test December (S&P 500): 2026 to 2028, verdict"),
 dict(date="2029-11-15", approx=True, de="Vorwärtstest Bitcoin im Oktober: 2027 bis 2029, Bewertung", en="Forward test bitcoin in October: 2027 to 2029, verdict"),
 dict(date="2031-11-17", de="Endbewertung Kronjuwelen gegen S&P 500 (bewährt bei mindestens 2 Punkten Vorsprung pro Jahr)", en="Final verdict Crown Jewels versus S&P 500 (proven with a lead of at least 2 points a year)"),
 dict(date="2036-11-17", de="Zehnjahresbericht Kronjuwelen gegen S&P 500 (gleiche Maßstäbe wie 2031)", en="Ten-year report Crown Jewels versus S&P 500 (same measures as 2031)"),
 dict(date="2029-11-17", de="Dreijahresbericht aller Kron-Akten (17. bis 22.11.2029)", en="Three-year report of all case files (Nov 17 to 22, 2029)"),
 dict(date="2031-11-18", de="Fünfjahresbericht der Kron-Akten ohne Kronjuwelen (18. bis 22.11.2031)", en="Five-year report of the case files without the Crown Jewels (Nov 18 to 22, 2031)"),
 dict(date="2036-11-18", de="Zehnjahresbericht der Kron-Akten ohne Kronjuwelen (18. bis 22.11.2036)", en="Ten-year report of the case files without the Crown Jewels (Nov 18 to 22, 2036)"),
]
items = sorted((x for x in items if x["date"] >= today.isoformat()), key=lambda x: x["date"])
json.dump(dict(today=str(today), season=dict(n=s.get("n_seasons"), day=s.get("day_in_season"), left=s.get("days_left")) if s else None, items=items), open("site/calendar.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(items, ensure_ascii=False)[:400])
