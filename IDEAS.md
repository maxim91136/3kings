# Ideenliste 3Kings (nur sammeln, noch nichts gebaut)

## Strategien fürs Turnier (jede muss die gleiche Prüfung bestehen: Kosten, Look-ahead-Test, feste Parameter)
- [x] Halten
- [x] Trend SMA200
- [x] Vol-Target 15 %
- [x] Familie "Halten + Nachkaufen" (gebaut: accumulate.py, erster Test siehe unten) (EINE Strategie mit Varianten, Basis = Halten):
      Variante A: nie nachkaufen (= reines Halten)
      Variante B: bei Rücksetzer nachkaufen (Dip, Schwelle vorab festgelegt)
      Variante C: regelmäßig nachkaufen (Sparplan)
      Variante D: Kombination aus B und C
      Verkauft wird nicht, nur aufgestockt; Zahl der Käufe und Kosten werden ausgewiesen
- [ ] Einstieg bei leerer Position: gleiche Familie, nur mit Startsumme in Teilbeträgen (Tranchen) statt auf einmal

## Regeln für alle Strategien
- Wenig handeln: Umschichtungen kosten Geld. Umsatz und Kosten je Strategie mit ausweisen.
- Test mit vielen Startterminen (rollierend), nicht nur ab einem Tag.
- Mehr Strategien = mehr Gefahr von Zufallstreffern: Signifikanzschwelle anpassen.

## Spielerkader später ausweiten
- Weitere Herausforderer über die drei Großen hinaus (Einzelaktien wie Apple, Nvidia usw.)
- Achtung Überlebens-Verzerrung: Wer heute als Gewinner bekannt ist, verfälscht den Rückblick.

## Seite
- Beide Varianten sichtbar: Empfehlung gegen Halten, später mit Kurve

## Erste Ergebnisse (accumulate.py, echte Kurse 2015-2026, Frist 3 Jahre, viele überlappende Starts)
- Keine Nachkauf-Variante schlägt die Einmalanlage beim mittleren Endwert (BTC 3,70 gegen 3,65 / 3,32 / 3,31).
- Dip-Nachkauf liegt fast gleichauf (besser als Halten in 33-41 % der Starts), Rückgang bei SPY/GLD etwas kleiner.
- Sparplan und Kombination kosten Rendite, weil Geld länger in Cash liegt.
- Offen: andere Schwellen und längere Zeiträume (nur vorab festlegen), dann in die Mannschaft/das Turnier einbauen.

## Zeithorizonte (wichtig, Ausbau nach und nach)
- Welche Linie? SMA 50/100/200/300, evtl. EMA. Welcher Rückblick fürs Turnier (252/504/756 Tage)? Welche Saisonlänge?
- Vorgehen: feste, kleine Auswahl vorab festlegen, ALLE Ergebnisse zeigen (nicht nur das beste), Signifikanzschwelle an die Zahl der Tests anpassen.
- Je Spieler getrennt auswerten: Bitcoin tickt anders als Gold.

## Seite: "Neues Geld"
- Eigener Bereich: Wo zuerst nachlegen? Regel vorher festlegen, dann testen.

## Stand 18.11. (Plan A-B-C)
- A: Aktien-ETFs als Spieler (URTH, VT, QUAL, MTUM, USMV, XLK; Reserve TLT, IEF, EFA, EEM, ETH) -> `admit.py`, Daten per Workflow `candidates`
- B: Power-Law als Günstig-Signal für Bitcoin, kausal: erster Test mit Daten ab 2015 schlechter als Halten (Sharpe 0,70/0,68 gegen 0,87); mit langer Historie (ab 2010) wiederholen
- C: Langfrist-Plan als Kern, 3Kings als Steuerung für Neues Geld und taktischen Teil

## Rahmen fuer neues Geld (Plan C, Stand 2026-11-18)
Startlage: fast nichts vorhanden, alles kommt aus kuenftigem Geld. Deshalb gibt es keinen zweiten "Kern-Plan": der Kern IST die Zielverteilung der Mannschaft.
1. Geld kommt rein (Sparrate oder Einmalbetrag) -> Betrag auf der Seite unter "Neues Geld" eintragen -> sofort nach Ziel-Anteilen investieren (Einmalanlage schlug Dip-Warten, siehe accumulate.py).
2. Der Cash-Anteil des Plans (Spieler im Trend-Aus) bleibt Cash. Bitcoin kommt erst bei Signal dazu.
3. Kleine Betraege: nicht in drei Haeppchen zerlegen (Gebuehren, Mindestorder). Dann nur den Spieler kaufen, der am weitesten unter seinem Ziel liegt.
4. Verkaufen nur bei "Aktion empfohlen" mit Abweichung >= 5 Punkte. Sonst nichts tun.
5. Das System kennt deinen echten Bestand nicht. Es nennt nur das Soll.

### Kern (Entscheidung 2026-11-18)
Vorhandene Bitcoin (ca. 0,31 BTC, davon 0,25 Familie, Rest Sparplan fuers Kind) sind KERN: werden gehalten, nie vom System bewegt, nicht in die Mannschaft eingerechnet. Die Mannschaft steuert nur NEUES Geld (ab 2027 groesser, Sparplaene/monatlich). Cash, das wegen Trend-Aus eines Spielers parkt, gehoert zum Plan und wird bei Signal investiert.
Kern erweitert: auch Gold/Silber-Muenzen (ca. 10.000). Bitcoin + Edelmetalle zusammen schon ca. 30.000 -> Neues Geld faktisch NUR in S&P 500 (Spieler SPY), bis dessen Anteil am Gesamtvermoegen ungefaehr beim Ziel liegt (heute 32 %, also grob die ersten ~10.000 neues Geld). Bitcoin/Gold-Ziele der Seite fuer neues Geld ignorieren. Danach neu bewerten. Seite zeigt weiterhin nur Ziele, keinen Bestand.

## Technik und Recht (notiert 23.11.2026)
- [ ] Schriften lokal einbinden statt über Google Fonts (Datenschutz, wie auf dreierlabs.com)
- [ ] Seite als echte Web-App (PWA): Manifest, Vollbild, ggf. Push-Mitteilungen
