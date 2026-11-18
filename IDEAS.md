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
