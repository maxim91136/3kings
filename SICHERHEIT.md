# Sicherheit 3Kings

Stand: 26.11.2026. Seit 26.11.2026 wird die Seite öffentlich gemacht (Cloudflare Access ist entfernt, Stand der Wache: ohne Access erreichbar) und kommt auf die Web-Audit-Seite von Dreier Labs.

## Prüfung

- **Art:** Code- und Konfigurationsprüfung (statisch), Browser-Test mit erzwungener Content-Security-Policy, Prüfung der Workflows.
- **Nicht geprüft:** die Live-Adressen. Aus der Prüfumgebung sind sie nicht erreichbar. Die Seite ist öffentlich, ein Zugriffsschutz gilt nicht mehr (Historie: Punkt A und D).
- **Tests:** `python3 -m unittest discover -s tests` (Kopfzeilen, CSP ohne Inline-Skripte, keine Inline-Handler, Escaping, https-Quellenlinks, kein eval).

## Befunde und Maßnahmen

| # | Befund | Maßnahme |
|---|---|---|
| 1 | Keine Sicherheits-Kopfzeilen | `site/_headers`: CSP, HSTS (ein Jahr, ohne Unterdomains, ohne Preload), nosniff, Framing verboten, Referrer- und Permissions-Policy, COOP/CORP |
| 2 | Inline-Skripte ohne Schutz | Alle Inline-Skripte (22, auch auf Archiv, Protokoll, Regelbuch) liegen jetzt in `site/js/`; CSP `script-src 'self'` ohne Hashes. Hash-Variante hatte die drei Unterseiten blockiert. Der Test verbietet neue Inline-Skripte |
| 3 | Ein Inline-Klick-Handler im Markup | in `site/lacht.js` ausgelagert (delegierter Listener) |
| 4 | Escaping ließ Anführungszeichen durch; Quellenlinks ohne Schema-Prüfung | `e()` escaped jetzt auch `"` und `'`; Quellenlinks nur mit `https://`, sonst `#` |
| 5 | Workflow-Eingaben (`symbol`, `mode`, `script`) direkt in die Shell interpoliert | Übergabe über Umgebungsvariablen (`lookup.yml`, `telegram.yml`, `adhoc.yml`) |

Geprüft und unauffällig: keine Geheimnisse im Repo (Telegram-Token nur als Secret), keine externen Skript- oder Bild-Quellen, kein `eval`, keine `javascript:`-Links, `robots.txt` und `X-Robots-Tag` mit `noindex`.

## Offen (bei dir, in Cloudflare und GitHub)

- **A. (Historie, durch Veröffentlichung überholt) workers.dev:** Worker-Access gilt für Produktion und Preview, also auch für `3kings.csrxfxzp6f.workers.dev`. Die Anwendung „3kings - Cloudflare Workers“ hat drei Regeln: „Cloudflare account members“ (nur du), „InnerCircle“ (bewusst freigegeben, sechs Personen per E-Mail) und „sentinel3“ (Service Auth für das Monitoring).
- **B. HSTS nur einmal setzen.** Der Header kommt aus `_headers`. In Cloudflare unter SSL/TLS, Edge Certificates, HSTS nicht zusätzlich aktivieren.
- **C. Zone 3kings.dev:** „Always Use HTTPS“ an, „Minimum TLS Version“ auf 1.2, vier CAA-Einträge (`pki.goog`, `letsencrypt.org`, `ssl.com`, `sectigo.com`), wie bei cyberlage.org.
- **D. (Historie, überholt) Access-Richtlinie:** InnerCircle bleibt absichtlich. Offen: MFA für InnerCircle (heute aus) und Session-Dauer (heute 1 Monat). Beides vor einer Veröffentlichung entscheiden.
- **E. GitHub:** Zwei-Faktor-Anmeldung aktiv, Branch-Schutz für `main` (kein Force-Push).
- **F. Actions auf Commit-Hashes gepinnt (erledigt 26.11.):** `actions/checkout@v5` und `actions/setup-python@v6`.

## Pflege

- Keine Inline-Skripte und keine `on…=`-Handler in den HTML-Dateien. Neuer Code kommt nach `site/js/` (der Test schlägt sonst an).
- Neue externe Quellen (Schriften, Bilder, Skripte) brauchen eine Erweiterung der CSP, sonst werden sie blockiert.

## Vor der Veröffentlichung (Checkliste)

- [x] Punkt A, B, C oben erledigt und in Cloudflare kontrolliert
- [x] MFA und Session-Dauer für InnerCircle entschieden
- [x] Actions auf Hashes gepinnt (Punkt F)
- [x] `noindex` in HTML, `robots.txt` und `X-Robots-Tag` entfernt (KI-Trainings-Bots bleiben ausgesperrt), `sitemap.xml` und `security.txt` ergänzt
- [ ] Eine externe Prüfung der öffentlichen Adresse (Header, TLS, Mail) mit dem Audit-Werkzeug von Dreier Labs
- [ ] Impressum und Datenschutz für die öffentliche Seite (der Footer verweist bereits auf dreierlabs.com)