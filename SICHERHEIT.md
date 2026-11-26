# Sicherheit 3Kings

Stand: 26.11.2026. Diese Seite ist privat (Cloudflare Access, nur deine E-Mail), deshalb steht sie bewusst nicht auf der Web-Audit-Seite von Dreier Labs.

## Prüfung

- **Art:** Code- und Konfigurationsprüfung (statisch), Browser-Test mit erzwungener Content-Security-Policy, Prüfung der Workflows.
- **Nicht geprüft:** die Live-Adressen. Aus der Prüfumgebung sind sie nicht erreichbar. Der Zugriffsschutz (Cloudflare Access) muss von dir in einem privaten Fenster geprüft werden (siehe Punkt A unten).
- **Tests:** `python3 -m unittest discover -s tests` (8 Tests: Kopfzeilen, CSP-Hashes, keine Inline-Handler, Escaping, https-Quellenlinks, kein eval).

## Befunde und Maßnahmen

| # | Befund | Maßnahme |
|---|---|---|
| 1 | Keine Sicherheits-Kopfzeilen | `site/_headers`: CSP, HSTS (ein Jahr, ohne Unterdomains, ohne Preload), nosniff, Framing verboten, Referrer- und Permissions-Policy, COOP/CORP |
| 2 | Inline-Skripte ohne Schutz | Strikte CSP mit SHA-256-Hashes der 13 Inline-Skripte; der Test schlägt an, wenn Hashes nicht mehr passen |
| 3 | Ein Inline-Klick-Handler im Markup | in `site/lacht.js` ausgelagert (delegierter Listener) |
| 4 | Escaping ließ Anführungszeichen durch; Quellenlinks ohne Schema-Prüfung | `e()` escaped jetzt auch `"` und `'`; Quellenlinks nur mit `https://`, sonst `#` |
| 5 | Workflow-Eingaben (`symbol`, `mode`, `script`) direkt in die Shell interpoliert | Übergabe über Umgebungsvariablen (`lookup.yml`, `telegram.yml`, `adhoc.yml`) |

Geprüft und unauffällig: keine Geheimnisse im Repo (Telegram-Token nur als Secret), keine externen Skript- oder Bild-Quellen, kein `eval`, keine `javascript:`-Links, `robots.txt` und `X-Robots-Tag` mit `noindex`.

## Offen (bei dir, in Cloudflare und GitHub)

- **A. workers.dev: geprüft (26.11.).** Worker-Access gilt für Produktion und Preview, also auch für `3kings.csrxfxzp6f.workers.dev`. Die Anwendung „3kings - Cloudflare Workers“ hat drei Regeln: „Cloudflare account members“ (nur du), „InnerCircle“ (bewusst freigegeben, sechs Personen per E-Mail) und „sentinel3“ (Service Auth für das Monitoring).
- **B. HSTS nur einmal setzen.** Der Header kommt aus `_headers`. In Cloudflare unter SSL/TLS, Edge Certificates, HSTS nicht zusätzlich aktivieren.
- **C. Zone 3kings.dev:** „Always Use HTTPS“ an, „Minimum TLS Version“ auf 1.2, vier CAA-Einträge (`pki.goog`, `letsencrypt.org`, `ssl.com`, `sectigo.com`), wie bei cyberlage.org.
- **D. Access-Richtlinie:** InnerCircle bleibt absichtlich. Offen: MFA für InnerCircle (heute aus) und Session-Dauer (heute 1 Monat). Beides vor einer Veröffentlichung entscheiden.
- **E. GitHub:** Zwei-Faktor-Anmeldung aktiv, Branch-Schutz für `main` (kein Force-Push).
- **F. Actions auf Commit-Hashes pinnen (offen):** `actions/checkout@v5` und `actions/setup-python@v6`. Die Hashes konnte die Prüfumgebung nicht auflösen. Nachtragen, sobald die Hashes bekannt sind.

## Pflege

- Änderungen an `index.html` mit Inline-Skripten: danach die Hashes in `site/_headers` neu setzen (der Test zeigt, welche fehlen).
- Neue externe Quellen (Schriften, Bilder, Skripte) brauchen eine Erweiterung der CSP, sonst werden sie blockiert.

## Vor der Veröffentlichung (Checkliste)

- [ ] Punkt A, B, C oben erledigt und in Cloudflare kontrolliert
- [ ] MFA und Session-Dauer für InnerCircle entschieden
- [ ] Actions auf Hashes gepinnt (Punkt F)
- [ ] Öffentlich wäre die Seite nicht mehr „noindex“-geschützt: `robots.txt`, `X-Robots-Tag` und `noindex` entfernen, Zugriffsschutz durch Access bleibt aber die Hauptsperre
- [ ] Eine externe Prüfung der öffentlichen Adresse (Header, TLS, Mail) mit dem Audit-Werkzeug von Dreier Labs
- [ ] Impressum und Datenschutz für die öffentliche Seite (der Footer verweist bereits auf dreierlabs.com)
