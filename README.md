# 3Kings

Privates Forschungs- und Empfehlungssystem für drei Spieler: **Bitcoin, S&P 500 (SPY), Gold (GLD)**.
Es gibt **keine Auto-Trades**; es erzeugt nur eine tägliche Empfehlung und führt ein Schattenbuch.

- `core/lab.py`, `core/team.py` – Strategien und Mannschaftsregeln (Saison 63 Tage, Champion/Herausforderer, Inverse-Vol-Kapital, Bitcoin doppelt gewichtet)
- `fetch_prices.py` – Kurse (Coinbase/Yahoo, Reserven Binance-Datenhost/Stooq) -> `data/prices.csv`
- `heartbeat.py` – Empfehlung + Schattenbuch (`data/ledger.csv`, `data/state.json`) -> `site/heartbeat.json`
- `site/` – schlichte Seite (Cloudflare Pages, Ausgabeordner `site`, kein Build-Befehl)
- `.github/workflows/heartbeat.yml` – täglicher Lauf Di–Sa 00:30 UTC; Telegram optional

## Einrichtung (einmalig, bei dir)
1. Repository **privat** lassen. Actions -> Workflow `heartbeat` einmal per *Run workflow* starten und das Log lesen.
2. Cloudflare Pages: Repository verbinden, Build-Befehl leer, Ausgabeordner `site`, Domain `3kings.dev`.
3. Cloudflare Access davor setzen (nur deine E-Mail).
4. Optional Telegram: Secrets `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`.

Regeln ändern sich nur am Saisonende, nie mitten in der Saison. Der Kursabruf ist vor dem ersten Lauf ungetestet.

## Wo ist was (Überblick)
| Frage | Datei |
|---|---|
| Was läuft täglich? | `.github/workflows/heartbeat.yml` (Kurse holen, rechnen, committen) |
| Woher kommen die Kurse? | `fetch_prices.py` -> `data/prices.csv` |
| Was empfiehlt der Heartbeat? | `heartbeat.py` -> `site/heartbeat.json` |
| Welche Regeln gelten? | `core/lab.py` (Strategien), `core/team.py` (Saison, Champion) |
| Was wurde wann an den Regeln geändert? | `REGELN.md` |
| Was ist das Gedächtnis? | `data/ledger.csv` (Schattenbuch), `data/state.json` |
| Wie sieht die Seite aus? | `sparplan.py` | Kaufsignal (nicht am Hoch, in Euro) und Schattenbuch Sparplan |
| `site/index.html` |
| Neue Spieler testen / Daten holen | `admit.py` (Aufnahmeregeln), `fetch_candidates.py` + Workflow `candidates` (einmalig starten) |
| Tests, die nichts verändern | `run_dip.py`, `run_sma100.py`, `horizon.py`, `accumulate.py`, `powerlaw.py` |
| Ideen, noch nicht gebaut | `IDEAS.md` |
