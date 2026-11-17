# 3Kings

Privates Forschungs- und Empfehlungssystem für drei Spieler: **Bitcoin, S&P 500 (SPY), Gold (GLD)**.
Es gibt **keine Auto-Trades**; es erzeugt nur eine tägliche Empfehlung und führt ein Schattenbuch.

- `core/lab.py`, `core/team.py` – Strategien und Mannschaftsregeln (Saison 63 Tage, Champion/Herausforderer, Inverse-Vol-Kapital)
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
