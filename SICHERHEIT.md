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

- **A. workers.dev-Adresse prüfen (wichtig).** Access gilt nur für Adressen, die in einer Access-Anwendung stehen. Prüfe im privaten Fenster `https://3kings.csrxfxzp6f.workers.dev`: Es muss die Anmeldung kommen. Wenn nicht, die Adresse in die Access-Anwendung aufnehmen oder `workers_dev` in `wrangler.jsonc` auf `false` setzen, falls du sie nicht brauchst.
- **B. HSTS nur einmal setzen.** Der Header kommt aus `_headers`. In Cloudflare unter SSL/TLS, Edge Certificates, HSTS nicht zusätzlich aktivieren.
- **C. Zone 3kings.dev:** „Always Use HTTPS“ an, „Minimum TLS Version“ auf 1.2, vier CAA-Einträge (`pki.goog`, `letsencrypt.org`, `ssl.com`, `sectigo.com`), wie bei cyberlage.org.
- **D. Access-Richtlinie:** nur deine E-Mail (Aktion Allow), kurze Sitzungsdauer (z. B. 24 Stunden).
- **E. GitHub:** Zwei-Faktor-Anmeldung aktiv, Branch-Schutz für `main` (kein Force-Push).
- **F. Empfehlung, noch nicht gemacht:** Actions auf feste Commit-Hashes pinnen statt Versions-Tags. Das schützt vor manipulierten Tags in Drittanbieter-Actions.

## Pflege

- Änderungen an `index.html` mit Inline-Skripten: danach die Hashes in `site/_headers` neu setzen (der Test zeigt, welche fehlen).
- Neue externe Quellen (Schriften, Bilder, Skripte) brauchen eine Erweiterung der CSP, sonst werden sie blockiert.
