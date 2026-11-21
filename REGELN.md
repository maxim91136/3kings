# Protokoll

Regeln ändern sich nur am Saisonende oder nach ausdrücklicher Entscheidung. Jede Änderung steht hier.

## 2026-11-18: Bitcoin bekommt zusätzlich den Kandidaten Trend SMA100
Schnelle Trend-Linie, 100 Tage.
Grund: Test auf echten Kursen, Sharpe der Mannschaft 1,25 statt 1,12, gleicher Rückgang (15 %).
Vorbehalt: Linie wurde nach Ansicht der Ergebnisse gewählt (Data-Snooping), p-Wert daher optimistisch.
Wirkung heute: keine, Bitcoin-Champion bleibt Trend SMA200. Live im Schattenbuch beobachten.

## 2026-11-18: Aufnahmetest Aktien-ETFs und Power-Law (echte Daten)
- Geprüfte Kandidaten: URTH, VT, QUAL, MTUM, USMV, XLK, TLT, IEF, EFA, EEM, ETH. Keiner hat die Regeln bestanden (Mannschaft-Sharpe 1,25 ohne, 1,00 bis 1,24 mit Kandidat). Kein Wechsel, keine Ersatzbank-Aufnahme.
- Power-Law (kausal, Daten ab 2010): PL-Rampe Sharpe 0,87 = Halten, aber Rückgang 49 % statt 83 %. Keine bessere Rendite. Kein Signal in der Heartbeat-Regel; nur als Info möglich.

## 2026-11-18: Bitcoin-Gewichtung Stufe 2 (ausdrückliche Entscheidung)
- Kapitalverteilung: Inverse Volatilität, Bitcoin-Gewicht x2 (Spot, kein Hebel, Summe nie über 100 %).
- Test 2017-2026: Rendite 14,9 -> 17,6 %/J, Rückgang 15 -> 16 %, Sharpe 1,25 gleich. Stufen x3/x5 verworfen (Rückgang 21/29 %). Rückblick-Test, keine Garantie.
- XLK als vierter König und Aufnahme der ETFs/ETH/Anleihen: nicht aufgenommen (kaum Effekt, zu nah an SPY).
- Aufnahmetest ETFs und Power-Law (echte Daten): alle 11 Kandidaten durchgefallen; Power-Law-Rampe = Halten bei geringerem Rückgang, nicht aufgenommen.
- Nächste Prüfung der Regeln: Saisonende.

## 2026-11-18: Vorab festgelegt, woran wir die Regeln messen (bevor die Ergebnisse da sind)
Grundsatz: kein Hin und Her. Regeln ändern sich nur zum Saisonende oder per ausdrücklicher Entscheidung, nie nach Bauchgefühl.
1. Langzeittest S&P 500 (longtest.py, Preisindex ab 1928): Der Trendfilter gilt für den S&P nur als belegt, wenn er in den Krisenepochen 1973-1982 UND 2000-2009 den Rückgang gegenüber Halten senkt. Sonst wird er für den S&P neu bewertet (zum nächsten Saisonende).
2. Live-Prüfung (Schattenbuch, nach 4 Saisons = ca. Nov 2027): bestätigt, wenn Rückgang kleiner als beim Halten und Rendite höchstens 2 Punkte darunter; gescheitert, wenn Rendite mehr als 5 Punkte darunter UND Rückgang nicht kleiner; sonst weiter beobachten.

### Ergebnis Langzeittest S&P (2026-11-18, Preisindex 1930-2026, ohne Dividenden/Zins)
Kriterium 1 erfüllt: Trend SMA200 senkt den Rückgang in 1973-1982 (48 -> 16 %) und 2000-2009 (57 -> 26 %). Über alles: Rendite 6,3 % vs 6,2 % (Halten), Rückgang 49 % vs 83 %. Schwäche: 2010-2026 Trend 6,6 % vs Halten 11,8 %/J. Vol-Target schützt in Crashs deutlich schwächer (1930er 72 %, 2000er 47 %), war 2010-2026 aber besser als Trend. Keine Regeländerung.

## 2026-11-18: Studie "Einstieg in Stufen" (vorab festgelegt, vor dem Rechnen)
Idee: nach einem Trendbruch nicht alles auf einmal, sondern mit einem Teil früher zurück. Genau 3 Regeln, nichts nachträglich dazu (Mehrfachtest-Schutz):
- R0 Basis: Trend SMA200 (ganz oder gar nicht).
- R1 Zwei Stufen: 50 % investiert, wenn Kurs über SMA50; weitere 50 %, wenn über SMA200.
- R2 Drei Stufen: je ein Drittel über SMA50, SMA100, SMA200.
- R3 Tief-Stufe: wie R0, zusätzlich 50 % investiert, wenn Kurs über SMA50 UND mindestens 20 % unter dem 252-Tage-Hoch lag (Erholung nach tiefem Rückgang).
Daten: S&P 500 ab 1930 (Epochen wie longtest.py), Bitcoin ab 2011 (btc_long.csv, vier Epochen). Kosten 5 bps (S&P) bzw. 10 bps (BTC) je Umschichtung.
Kriterium: Eine Regel gilt als besser als R0 nur, wenn (a) ihr Sharpe in der Mehrzahl der Epochen mindestens so gut ist wie R0 (S&P: mind. 4 von 6, BTC: mind. 3 von 4), (b) über alles Sharpe mind. +0,03, (c) der maximale Rückgang über alles nicht mehr als 3 Punkte und in den S&P-Krisenepochen 1973-1982 und 2000-2009 nicht mehr als 5 Punkte schlechter ist. Bestehen mehrere, gilt die einfachste. Gilt nur, wenn Kriterium für S&P UND Bitcoin erfüllt; sonst keine Änderung. Einbau frühestens zum Saisonende.

### Ergebnis Studie "Einstieg in Stufen" (2026-11-18, staged.py)
S&P (1930-2026): R1/R2/R3 verfehlen das Kriterium (Sharpe in nur 3 von 6 Epochen mindestens so gut wie R0; gesamt +0,01 bis +0,02). Stufen helfen 1930-1982, schaden 1983-2009 (Fehlsignale). Bitcoin (2011-2026): alle drei erfüllen das Kriterium (R1: Sharpe 1,20 -> 1,37, Rückgang 78 -> 71 %, in 4 von 4 Epochen besser). Gesamtkriterium (S&P UND Bitcoin) NICHT erfüllt -> keine Regeländerung. Offen für Saisonende: Bitcoin-Stufen (R1) als ausdrückliche Einzelentscheidung, nicht per Regel.

## 2026-11-18: Review (Opus) - vorab festgelegt, vor dem Rechnen (review.py)
Annahmen: S&P-Preisindex 1928-2026 ohne Dividenden, Cash ohne Zins (beides wirkt grob gegeneinander). Steuer: 26,375 % Abgeltungsteuer, 30 % Teilfreistellung (Aktien-ETF) = 18,46 % auf realisierte Gewinne, Verlusttopf, Freibetrag nicht berücksichtigt. Kosten 5 bps je Umschichtung. Umschichtung nur bei mehr als 2 Punkten Abweichung.
Frage 1 - fester Champion für den S&P: Trend SMA200 ersetzt die Champion-Wahl beim S&P, wenn er nach Steuern über 1930-2026 (a) Rendite höchstens 0,3 Punkte unter der Champion-Wahl, (b) kleineren Rückgang gesamt und (c) kleineren Rückgang in 1973-1982 und 2000-2009 hat.
Frage 2 - Kaufregel für neues Geld (monatlich gleicher Betrag, Fenster 10 und 20 Jahre, Start alle 6 Monate ab 1930):
  K1 sofort kaufen, nie verkaufen; K2 Kauf-Pause: kaufen nur über SMA200, sonst sammeln, Gesammeltes beim Signal kaufen, nie verkaufen; K3 Trend voll (kauft und verkauft mit SMA200); K4 Dip-Reserve: 80 % sofort, 20 % Reserve, Reserve komplett rein bei Rückgang >= 20 % vom 12-Monats-Hoch, nie verkaufen; K5 heutige Champion-Wahl.
  Empfohlen wird die Regel mit dem höchsten Median-Endvermögen nach Steuern über 20-Jahres-Fenster. Eine andere Regel wird nur empfohlen, wenn ihr Median höchstens 2 % darunter liegt UND ihr schlimmster Buchverlust (Wert/Eingezahlt) im Median der Fenster mindestens 10 Punkte kleiner ist.

### Ergebnis Review (2026-11-18, review.py)
Frage 1 ERFUELLT: nach Steuern 1930-2026 Trend SMA200 5,2 %/J, Rückgang 49 % vs Champion-Wahl 4,3 %/J, 64 % (Krisen 17 vs 22 %, 26 vs 49 %). Halten 6,0 %/J, 83 %. -> S&P spielt ab sofort fest Trend SMA200 (heartbeat.py FIXED). Mannschaft 2017-2026 dadurch praktisch gleich (17,6 %/J, Rückgang 17 statt 16 %, Sharpe 1,26).
Frage 2: 20-Jahres-Fenster Median Endwert/Eingezahlt: K1 sofort 2,14; K2 Kauf-Pause 2,14; K4 Dip-Reserve 2,08; K3 Trend voll 1,82; K5 Champion 1,69. Nach Kriterium empfohlen: K1 (sofort kaufen). K2 gleicher Median, schlimmster Buchverlust -38 statt -67 %, Median-Buchverlust nur 4 Punkte kleiner (Kriterium 10) -> nicht empfohlen, nur als ausdrückliche Entscheidung möglich.
Seite: "Neues Geld / nur S&P 500" zeigt jetzt K1 (kaufen, ganzer Betrag) plus Trendlage als Info.

## 2026-11-18: Kaufregel neues Geld = "nicht am Hoch" (ausdrückliche Entscheidung)
Ausgangsidee: nicht am Allzeithoch kaufen. ath.py (S&P 1930-2026, monatlich, vor Steuern): "nicht am Hoch" (kaufen nur, wenn mind. 3 % unter dem Allzeithoch, sonst sammeln) 20 Jahre Median 2,43 vs sofort 2,44, besser in 41 % der Fenster - kostet praktisch nichts. "Warte auf -10 %" kostet deutlich (2,18). Kauf ab -20 % brachte im Schnitt mehr (5 Jahre 10,9 vs 8,7 %/J am Hoch), Kauf am Hoch war aber nicht öfter im Minus als bei -3 bis -20 %.
Regel: S&P innerhalb 3 % vom Allzeithoch -> sammeln; sonst Betrag plus Reserve kaufen. Ersetzt K1 auf der Seite.

## 2026-11-18: Studie "Bewertung + Angst" für die Kaufregel (vorab festgelegt, valuation.py)
Neues Geld monatlich, S&P-Preisindex, vor Steuern, Cash ohne Zins, Dividenden nicht enthalten. Bewertung = Shiller-KGV als Perzentil seiner EIGENEN Geschichte bis zum jeweiligen Tag (kausal). Angst = VIX (erst ab 1990).
Regeln: N "nicht am Hoch" (heutige Regel, kaufen ab 3 % unter Allzeithoch). B1 Bewertungsbremse: ist das KGV im obersten Fünftel seiner Geschichte, wird erst ab 10 % unter dem Hoch gekauft, sonst wie N. B2 wie B1, aber erst ab 20 %. B3 wie B1, gesammeltes Geld wird nach spätestens 12 Monaten trotzdem investiert. A1 (ab 1990) Angst-Kauf: wie N, zusätzlich wird bei VIX >= 30 sofort alles investiert, auch nahe am Hoch. A2 (ab 1990): B1 plus Angst-Kauf (VIX >= 30 hebt die Bremse auf).
Kriterium: eine Regel ersetzt N nur, wenn über 20-Jahres-Fenster (bzw. 10-Jahres-Fenster bei den Angst-Regeln) der Median-Endwert höchstens 1 % unter N liegt UND die schlechtesten 10 % besser sind als bei N, ODER der Median mindestens 2 % über N liegt.

### Ergebnis Studie "Bewertung + Angst" (2026-11-18)
Keine Regel erfüllt das Kriterium, N bleibt. 20 J ab 1930: N 2,43 | B1 2,26 (längste Wartezeit 6,2 J) | B2 2,19 (9,6 J) | B3 2,40. Grund: Shiller-KGV seit 1995 an 94 % der Tage im obersten Fünftel seiner Geschichte - eine Bewertungsbremse wartet jahrelang. 10 J ab 1990: A1 (Angst-Kauf VIX >= 30) identisch mit N, weil hohe Angst immer mit Kursen mehr als 3 % unter dem Hoch zusammenfiel - N kauft in Angstphasen also schon. A2 1,47 vs N 1,53.

## 2026-11-18: Nachtrag "relative Bewertung" (vorab festgelegt, valuation.py --relativ)
Shiller-KGV als Perzentil nur der letzten 10 bzw. 20 Jahre (kausal). R10/R20: im obersten Fünftel dieses Fensters erst ab 10 % unter dem Hoch kaufen, sonst wie N. R10c: wie R10, nach spätestens 12 Monaten Warten trotzdem kaufen. G10: im untersten Fünftel der letzten 10 Jahre sofort kaufen, auch nahe am Hoch, sonst wie N. Gleiches Kriterium wie oben (20-Jahres-Fenster ab 1930).
Ergebnis: keine Regel erfüllt das Kriterium, N bleibt. N 2,43 | R10 2,19 | R20 2,26 | R10c 2,37 | G10 2,43 (identisch mit N: günstige Phasen fielen immer mit Kursen unter dem Hoch zusammen). Relativ "teuer" ist an rund 36 % der Tage - die Bremse verpasst dann die Aufschwünge.

## 2026-11-18: Studie "Relative Stärke für neues Geld" (vorab festgelegt, strength.py)
Monatlich 1 Einheit neues Geld, nie verkaufen, Kosten 5 bps (BTC 10 bps). Fenster 5 Jahre, Start jeden Monat. Regeln:
M0 alles in den S&P (Vergleich). M1 gleich auf alle verteilt. M2 alles in den Stärksten der letzten 6 Monate. M3 alles in den Stärksten der letzten 12 Monate ohne den letzten Monat (12-1). M4 wie M3, aber nur wenn dessen 12-Monats-Rendite positiv ist, sonst sammeln bis eine positiv wird (Dual Momentum). M5 alles in den Schwächsten der letzten 12 Monate (antizyklisch).
Test A: Bitcoin, S&P, Gold (2015-2026). Test B: nur S&P und Gold (ohne Bitcoin). Test C: breite ETFs VT, EEM, IEF, XLK (2008-2026, Kurse inkl. Ausschüttungen).
Kriterium: eine Regel schlägt M0 nur, wenn ihr Median-Endwert in Test B UND Test C mindestens 3 % über M0 (bzw. über VT in Test C) liegt und sie in beiden Hälften der Startzeitpunkte vorne ist. Test A allein zählt nicht (Bitcoin-Rückblick).
Ergebnis: keine Regel erfüllt das Kriterium, keine Änderung. Test B (S&P/Gold): alle Regeln 1,42-1,43 vs S&P 1,49. Test C: Stärke 12-1 (M3/M4) 1,48 vs Welt-ETF 1,29 - kauft aber fast nur XLK (Tech-Rückblick 2008-2026), antizyklisch (M5) 1,14. Test A (mit Bitcoin): alles, was Bitcoin beimischt, schlägt den S&P (1,96-2,17), antizyklisch am besten (2,17) - nur Rückblick, zählt nicht.

## 2026-11-18: Kaufsignal in Euro (eurtest.py)
Euro-Anleger 2004-2026, 10-Jahres-Fenster, Werte in Euro: sofort 2,121 | Signal in Dollar 2,125 | Signal in Euro 2,125 (in 100 % der Fenster mindestens so gut wie sofort). Signale unterscheiden sich an 21 % der Tage. -> Signal und Schattenbuch Sparplan rechnen ab jetzt mit dem S&P in Euro (sparplan.py, USE_EUR).

## 2026-11-18: Euro-Sicht für die Mannschaft (nur Befund, keine Änderung)
Mannschaft 2017-2026 in Euro gerechnet: 15,4 %/J, Rückgang 16 %, Sharpe 1,07 (in Dollar 17,6 %, 17 %, 1,26). Halten in Euro 22,9 %/J, Rückgang 25 %. Der Abstand zum Halten ist in Euro grösser, weil der Cash-Anteil die Dollar-Gewinne nicht mitnimmt. Trendsignale Dollar vs Euro verschieden: Bitcoin 2 %, S&P 12 %, Gold 22 % der Tage. Ob die Mannschaft in Euro rechnen soll: Entscheidung zum Saisonende. Seite zeigt Abstand zum Allzeithoch für alle drei in Euro.

## 2026-11-18: Langzeittest Gold (vorab festgelegt, goldtest.py)
Daten: Goldpreis monatlich (datasets/gold-prices, USD) ab 1971-08 (Ende fester Goldpreis). Monatliche Signale, Kosten 5 bps, Cash ohne Zins. Halten vs Trend 10 Monate (entspricht etwa 200 Tagen).
Kriterium: Der Trendfilter gilt für Gold als belegt, wenn er den grössten Rückgang gesamt UND in der Baisse-Epoche 1981-2000 senkt und die Rendite gesamt höchstens 2 Punkte pro Jahr unter Halten liegt. Dann spielt Gold im Prüfstand fest Trend SMA200 (wie der S&P). Sonst spielt Gold fest Halten.
Ergebnis Gold (1971-2026, monatlich): Trend 10,1 %/J, Rückgang 32 % vs Halten 8,6 %/J, 62 %; 1981-2000 Rückgang 31 vs 54 %. Kriterium ERFUELLT -> Gold spielt im Prüfstand fest Trend SMA200.
Hinweis: im kurzen Fenster 2017-2026 (Euro) war die Mannschaft mit Gold-Trend schwächer (12,9 %/J, Rückgang 21 %, Sharpe 0,94) als mit Gold-Wahl (15,4 %, 16 %, 1,07). Die Langzeitdaten zählen (vorab festgelegt).

## 2026-11-18: Prüfstand rechnet in Euro (ausdrückliche Entscheidung)
heartbeat.py rechnet alle Kurse in Euro (to_eur). Befund 2017-2026 in Euro: Mannschaft 12,9 %/J, Rückgang 21 %, Sharpe 0,94; alle drei gleich halten 22,9 %/J, Rückgang 25 %, Sharpe 1,19. Die Mannschaft liegt in Euro auch risikobereinigt hinter dem Halten - zum Saisonende ehrlich bewerten.

## 2026-11-18: Gegencheck Total Return, Zinsen, Inflation, Start 1929 (vorab festgelegt, totalreturn.py)
Anlass: Kritik einer zweiten KI (Gemini): Preisindex ohne Dividenden, Cash ohne Zins, nominal, Start erst 1930. Daten: Shiller (datasets/s-and-p-500), monatlich 1871-06/2023 (Dividende, Inflation, Zins 10 J.). Total Return = (Kurs + Dividende/12) / Vormonatskurs - 1. Cash-Zins unbekannt (nur 10-Jahres-Zins vorhanden): Test mit 0 % und mit 50 % des 10-Jahres-Zinses als grobe Näherung für Tagesgeld/Kurzläufer. Real = durch US-Inflation (CPI). Kosten 5 bps. Keine Steuern.
Frage A (Kaufregel): Monatlich 1 Einheit, 20-Jahres-Fenster, Start alle 6 Monate ab 1929-01 (inkl. 1929), Total Return, Cash mit Zins. "Nicht am Hoch" (kaufen ab 3 % unter Allzeithoch, Monatskurse) hält, wenn Median-Endwert mindestens 99 % von "sofort kaufen" UND die schlechtesten 10 % nicht mehr als 1 % darunter liegen. Zusätzlich einzeln: Start im Hoch September 1929 und Start März 2000 (20 und 10 Jahre) - nur Information.
Frage B (Trend): Trend 10 Monate (~200 Tage) auf Total Return mit Cash-Zins gegen Halten, Epochen wie longtest.py. Trend bleibt belegt, wenn er in 1973-1982 und 2000-2009 den Rückgang gegenüber Halten senkt UND über alles die Rendite höchstens 1,0 Punkt/J unter Halten liegt (nominal, Cash mit 50 % des 10-J-Zinses). Sonst wird der Trend als Absturzbremse neu bewertet (Saisonende).

### Ergebnis Gegencheck Total Return (2026-11-18, totalreturn.py, Shiller 1929-2023)
Frage A: Kriterium NICHT erfüllt (7 von 8 Varianten). Mit Dividenden und Zinsen kostet "nicht am Hoch" mehr als im Preisindex-Test: 20 J nominal Median 3,39 vs sofort 3,46 (ca. 2 % weniger), 10 J 1,74 vs 1,79 (ca. 3 %); besser als sofort nur in 1-12 % der Fenster (vorher 41 %). Einzelstarts Sept 1929, März 2000, Jan 1973: praktisch identisch zu sofort. Schlechteste 10 % nur ca. 1-4 % schlechter. Der frühere Befund "kostet praktisch nichts" gilt nur ohne Dividenden und war zu optimistisch; die Kritik war berechtigt.
Frage B: Trend 10 Monate bleibt belegt: 1930-2023 Total Return 10,9 %/J, Rückgang 22 % vs Halten 9,8 %/J, 78 %; 1973-1982 11 vs 39 %, 2000-2009 6 vs 49 %. Schwäche bleibt 1983-1999 und 2010-2023 (2-3 Punkte/J hinter Halten).
Die Regel "nicht am Hoch" war eine ausdrückliche Entscheidung (Grundsatz); Kosten jetzt bekannt: ca. 2-3 % des Endvermögens im Median. Änderung nur durch ausdrückliche Entscheidung.

## 2026-11-18: Kaufregel neues Geld = sofort kaufen (ausdrückliche Entscheidung, ersetzt "nicht am Hoch")
Grund: Gegencheck Total Return (totalreturn.py): "nicht am Hoch" kostet 2-3 % Endvermögen, besser als sofort nur in 1-12 % der Fenster. Grundsatz: Zahlen gehen vor Prinzip. Seite zeigt immer "Kaufen". "Nicht am Hoch" läuft als Vergleich im Schattenbuch Sparplan weiter (sparplan.py: regel_signal). Prüfung: nach einem Jahr. Rückgängig: signal in sparplan.py wieder an buy koppeln.

## 2026-11-18: Elite 9 und Faktor-ETFs (nur Anzeige und Schattenbuch, kein Geld)
Ausnahme von "keine Einzelaktien": nur Beobachtung, keine Empfehlung, kein Einfluss auf die Kaufregel.
Elite 9 (Ausgangsliste vom 2026-11-18, Auswahl im RUECKBLICK, Quelle der Zahlen unklar): CME Group, Ferrari, Waste Management, Mastercard, Visa, Cintas, Hermès (Paris, EUR), Microsoft, Alphabet. 9 Regeln der Liste: Beta < 1,15; Bruttomarge > 50 %; Monopol/Duopol; keine Zyklizität; Preissetzungsmacht; kein existenzielles Disruptionsrisiko; 10-Jahres-Rendite (Total Return) ~17 % p. a.; Verschuldung/Eigenkapital < 1,0; Burggraben wächst.
Automatisch berechnet (aus Kursen): Beta (täglich, 5 Jahre, gegen S&P 500) und 10-Jahres-Rendite p. a. Alles andere (Marge, Monopol, Zyklik, Disruption, Burggraben, Verschuldung) wird NICHT geprüft, nur übernommen. Die berechneten Werte werden mit den Listenwerten verglichen; Abweichung > 3 Punkte wird angezeigt.
Ein Rückwärts-Test der Liste ist wertlos (Survivorship: Regel 7 wählt Gewinner der Vergangenheit). Er wird nur zur Illustration gezeigt und so gekennzeichnet. DER Test ist das Schattenbuch Elite ab 2026-11-18: 9 Aktien gleich gewichtet, in Euro, gegen S&P 500 in Euro.
Kriterium (nach 3 Jahren, ab 2029-11): bewährt, wenn Rendite mindestens 2 Punkte pro Jahr über dem S&P UND der Rückgang nicht grösser; gescheitert, wenn die Rendite unter dem S&P liegt; sonst weiter beobachten. Nach 1 Jahr nur Zwischenstand, keine Bewertung.
Faktor-ETFs: QUAL (Qualität), MTUM (Momentum), USMV (Min. Volatilität), XLK (Tech), dazu VT und URTH (Welt) gegen SPY, in Euro, ab 2015-07. Anzeige: Rendite pro Jahr, Rückgang, Sharpe, Beta. Aufnahmetest vom 2026-11-18: alle durchgefallen (siehe oben). Keine neue Regel.

## 2026-11-18: Elite 9 wird Elite 5 (ausdrückliche Entscheidung: wer die Regeln nicht besteht, fliegt raus)
Prüfbar sind nur Regel 1 (Beta < 1,15) und Regel 7 (10-Jahres-Rendite >= 17 % p. a., hart gelesen). Ergebnis aus Kursen: Bestanden: Mastercard (0,89 / 20,7), Visa (0,82 / 18,6), Ferrari (0,90 / 23,3), Cintas (0,77 / 24,4), Microsoft (1,09 / 25,0). Raus: Alphabet (Beta 1,19), CME (14,8 %), Waste Management (15,5 %), Hermès (14,0 %). Die Liste ist ab jetzt eingefroren (keine automatische Änderung). Schattenbuch Elite startet neu mit den 5, gleich gewichtet, in Euro, gegen S&P 500; Kriterium unverändert (3 Jahre, +2 Punkte p. a., Rückgang nicht grösser). Die anderen sieben Regeln bleiben ungeprüft.

## 2026-11-18: Screening nach weiteren Elite-Kandidaten (vor dem Rechnen festgelegt)
Universum: ca. 130 bekannte Qualitätsfirmen USA/Europa (Liste in screen.py). Harte Regeln wie bei Elite 5: Beta < 1,15 (5 Jahre täglich, in Euro gegen S&P 500 in Euro) UND 10-Jahres-Rendite >= 17 % p. a. (Heimatwährung, inkl. Dividenden). Wer besteht, wird danach von Hand gegen die weichen Regeln (Marge > 50 %, Monopol, nicht zyklisch, Verschuldung < 1, kein Disruptionsrisiko) eingeschätzt; diese Einschätzung ist Urteil, nicht Messung. Aufnahme nur durch ausdrückliche Entscheidung. Hinweis: Auswahl nach vergangener Rendite findet per Definition die Gewinner der Vergangenheit.

## 2026-11-18: Screening-Ergebnis, Elite 5 wird Elite 6 (ausdrückliche Entscheidung)
Ca. 40 von 130 bestehen die harten Regeln; nach den weichen Regeln (Urteil) bleiben IDEXX (Beta 1,09 / 19,7 %), ASML (30,3 %, aber zyklisch), Constellation Software (18,8 %), Deutsche Börse (18,3 %; Beta europäischer Werte wegen Zeitzonen zu niedrig gemessen). Aufgenommen: nur IDEXX. ASML nicht (zyklisch, Regel gilt), obwohl einzigartig. Schattenbuch startet neu mit 6, Kriterium unverändert.

## 2026-11-18: Elite 6 Aufnahmewerte eingefroren
Beta und 10-Jahres-Rendite der Elite 6 gelten fest zum Stichtag 2026-11-18 (data/elite_frozen.json), keine nächtliche Neuberechnung. Nach vorn misst nur das Schattenbuch. Neuer Stand nur bei ausdrücklicher Überprüfung.

## 2026-11-18: Margenregel präzisiert (ausdrückliche Entscheidung)
Gemini-Prüfung: Cintas Bruttomarge 49,7 % (Q4 GJ 2025) knapp unter 50 %. Entscheidung: Cintas bleibt. Die Margenregel ist eine weiche Regel (Urteil) und gilt ab jetzt als "Bruttomarge rund 50 % oder mehr, Toleranz 1 Punkt". Die harten Regeln (Beta < 1,15, 10J >= 17 %) bleiben ohne Toleranz.

## 2026-11-18: Schattenbuch Elite auf 5 Jahre verlängert (ausdrückliche Entscheidung)
Bewertung nach 5 statt 3 Jahren, also ab 2031-11. Kriterium sonst unverändert (mindestens +2 Punkte p. a. über S&P 500 bei nicht größerem Rückgang = bewährt; Rendite unter S&P = gescheitert). Zwischenstände jährlich, ohne Bewertung. Änderung vor dem ersten Datenpunkt, also ohne Kenntnis von Ergebnissen.

## 2026-11-19: Test Kaufregel für Einzelaktien (vor dem Rechnen festgelegt)
Frage: Lohnt bei Einzelaktien Warten auf Abstand zum Allzeithoch?
Universum: alle ca. 130 Firmen aus screen.py (nicht nur Elite 6, sonst Survivorship maximal). Rest-Bias: auch das Universum besteht aus heutigen Großunternehmen.
Ablauf je Aktie: ab 2006-01 (oder ab 10 Jahre Historie) jeden Monat 1 Einheit Geld. "sofort": sofort kaufen. "warten X" (X = 10, 15, 20, 25 %): Geld sammeln (2 % Zins p. a.), alles kaufen, sobald Kurs <= (1 - X) * bisheriges Hoch. Ende 2026-11: Wert pro eingezahlter Einheit, Rest-Cash zählt mit Zins. Kurse bereinigt (inkl. Dividenden), Heimatwährung, Monatsendwerte.
Kriterium: Eine Warteregel gilt als belegt, wenn sie (a) im Median über alle Aktien mindestens 3 % mehr Endvermögen bringt, (b) bei mindestens 60 % der Aktien besser ist als sofort, und (c) beides auch im Zeitraum 2016-2026 allein gilt. Sonst: gilt nicht. Ergebnis ändert nur, was auf der Seite steht, keine Käufe.
Anzeige: Abstand zum Hoch je Elite-Aktie (aktuell, nur Info).
Ergebnis 2026-11-19 (138 Aktien, MMC ohne Daten): Warten ist bei Einzelaktien klar schlechter. Ab 2006 Median: 10 % -3,4 %, 15 % -6,9 %, 20 % -10,0 %, 25 % -16,3 %; besser nur bei 7-10 % der Aktien. Ab 2016: -4,5 / -8,1 / -13,3 / -21,4 %; besser bei 9-21 %. Kriterium in beiden Zeiträumen klar verfehlt. Warteregel für Einzelaktien: GILT NICHT. Rest-Bias: Universum aus heutigen Großunternehmen.

## 2026-11-19: Kauf-Warten bei Bitcoin (gleicher Aufbau wie Einzelaktien, Monatsgeld, 2 % Zins auf Wartegeld)
Rollierende Fenster ab 2013 (3 und 5 Jahre). Warten auf -20/-30/-40/-50/-60 % vom Hoch: Median -6 bis -17 %, besser nur in 10-27 % der Startmonate. Ganze Zeit 2013-2026: -30 bis -53 %. Gilt nicht. Einschränkung: nur ein Wert, kurze Historie.

## 2026-11-19: Test "nur die Größten" (S&P 500 Top 20) - vor dem Rechnen festgelegt
Der iShares S&P 500 Top 20 (IE000VA628D5) existiert erst seit 11/2024, zu kurz. Ersatz mit gleicher Idee: XLG (S&P 500 Top 50, ab 2005) und OEF (S&P 100, ab 2000), gegen SPY, Kurse inkl. Ausschüttungen, in Euro.
Kriterium (wie Faktor-ETFs): Aufnahme nur, wenn Rendite p. a. höher UND in BEIDEN Hälften (bis 2015 / ab 2015) höher UND maximaler Rückgang nicht größer als SPY. Sonst nur Anzeige.
Ergebnis (in Euro, 2005-06 bis 2026-11): XLG 11,4 %/J (Rückgang 47 %) vs SPY 11,3 % (51 %); bis 2015 6,8 vs 8,0 %; ab 2015 15,3 vs 14,0 %. OEF: 11,5 vs 11,3 %; bis 2015 7,3 vs 8,0; ab 2015 15,0 vs 14,0. Über 21 Jahre praktisch gleich, Vorsprung nur seit 2015 (Mega-Cap-Phase), davor schlechter. Kriterium (beide Hälften) verfehlt. Nicht aufgenommen. Der Top 20 ist noch konzentrierter (NVIDIA, Apple, Microsoft allein über 40 %), also eine Wette auf die Fortsetzung der letzten zehn Jahre.

## 2026-11-19: Kauf-Warten bei Gold (gleicher Aufbau wie Bitcoin und Einzelaktien)
Monatsgeld, 2 % Zins auf Wartegeld, rollierende 5- und 10-Jahres-Fenster ab 1975 (Monatsdaten in Dollar). Warten auf −10 bis −30 % vom Hoch: Median ±0 % (Gold lag 1980–2008 fast immer unter dem alten Hoch, die Regel kaufte dann ohnehin sofort), besser nur in 14–35 % der Startmonate, schlechtester Fall −54 %, bester +19 %. Gilt nicht. Damit ist "sofort kaufen" für alle drei Assets (S&P 500, Bitcoin, Gold) und für Einzelaktien geprüft.

## 2026-11-19: Seite allgemein und zweisprachig
Die Seite wird ohne Bezug auf einen persönlichen Bestand formuliert und behandelt alle drei Assets gleich. Kopfbereich: je Asset Kurs, Veränderung, Abstand zum Hoch und das Testergebnis "Kaufen". Rechner mit frei wählbarer Aufteilung (voreingestellt je ein Drittel, keine Gewichtungsempfehlung). Sprachen Deutsch und Englisch.

## 2026-11-20: Studie "Zeithorizonte" (vorab festgelegt, vor dem Rechnen; horizon.py + horizonlong.py)
Frage: Ist SMA200 als Trendlinie ein Zufallstreffer, oder liegt es auf einem Plateau? Und passen Rückblick 504 / Saison 63 der Mannschaft?
Feste Auswahl (nichts nachträglich dazu, ALLE Ergebnisse werden gezeigt):
- Linien: SMA 50, 100, 150, 200, 300 (Kurs darüber = investiert, sonst Cash). Gold nur monatlich: 3, 5, 7, 10, 14 Monate (entspricht etwa 63..294 Tage).
- Teil 1 kurz (horizon.py, echte Kurse 2015-2026, Euro-Sicht nicht enthalten): Linien je Spieler.
- Teil 1 lang (horizonlong.py): S&P 500 ab 1930 in den Epochen von longtest.py (6 Epochen); Bitcoin ab 2011 in 4 Epochen (2011-2014, 2015-2018, 2019-2022, 2023-2026); Gold monatlich ab 1971 (informativ). Preisindex, Cash ohne Zins, Kosten 5 bps (BTC 10 bps).
- Teil 2 (horizon.py, 2015-2026): Mannschaft Rückblick 252/504/756 x Saison 21/63/126, nur Information.
Kriterium Linie (Ersatz von SMA200): Eine andere Linie N ersetzt SMA200 nur, wenn sie für S&P UND Bitcoin Folgendes erfüllt:
 (a) Sharpe über alles mindestens +0,05 gegenüber SMA200;
 (b) Sharpe in der Mehrzahl der Epochen mindestens so gut wie SMA200 (S&P mind. 4 von 6, BTC mind. 3 von 4);
 (c) maximaler Rückgang über alles höchstens 3 Punkte schlechter, in den S&P-Krisenepochen 1973-1982 und 2000-2009 höchstens 5 Punkte schlechter als SMA200;
 (d) Plateau: beide Nachbarlinien von N (in der Reihenfolge 50-100-150-200-300) haben über alles mindestens den Sharpe von SMA200 (kein Einzelspitzenwert).
 Mehrfachtest-Schutz: 4 Alternativen je Wert, deshalb gelten (a) bis (d) gemeinsam und für beide Werte. Bestehen mehrere, gilt die einfachste (SMA200 bleibt bei Gleichstand).
 Gold: nur Information, keine Regeländerung (Gold ist fest SMA200 nach Langzeittest).
Kriterium Teil 2: keine Regeländerung aus Teil 2 allein (nur 11 Jahre, ein Regime). Befund nur nach Plateau beurteilen. Änderung frühestens zum Saisonende per ausdrücklicher Entscheidung.
Ist das Kriterium nicht erfüllt: SMA200 bleibt, die Linienwahl gilt als nicht belegt anders.

### Ergebnis Studie "Zeithorizonte" (2026-11-20, horizon.py + horizonlong.py)
Kriterium NICHT erfüllt, keine Regeländerung: SMA200 bleibt.
- S&P 1930-2026 (Sharpe über alles): SMA50 0,52 | 100 0,53 | 150 0,53 | 200 0,57 | 300 0,56 (Halten 0,42). Rückgang 47-53 % statt 83 %. Alle Linien liegen auf einem Plateau; die Länge ist fast egal, der Trendfilter selbst zählt. Keine Alternative besteht (a) und (b) (Epochen besser als SMA200: 2-3 von 6, nötig 4). SMA300 ist fast gleich (Plateau, Rückgang ok), aber nicht +0,05 besser.
- Bitcoin 2011-2026 (Sharpe über alles): SMA50 1,27 | 100 1,16 | 150 1,07 | 200 1,03 | 300 0,99 (Halten 0,90). SMA50 und SMA100 bestehen alle vier Punkte für Bitcoin, aber nicht für den S&P; der Test verlangt beide. Vorbehalt: kurze Linien wechseln oft (13 bzw. 8 Mal pro Jahr), Kosten 10 bps sind eingerechnet, Steuern nicht.
- Gold monatlich (nur Info): 3 bis 14 Monate alle Sharpe 0,66-0,72, Rückgang 29-40 % statt 62 %; wieder ein Plateau.
- Kurzes Fenster 2017-2026 (Teil 1): S&P- und Gold-Linien liegen alle unter Halten bei der Rendite (SPY 7-10,5 % vs 13,9 %), mit etwa 20 % statt 34 % Rückgang.
- Teil 2 (Mannschaft, 2017-2026): Rückblick 504 liegt auf einem Plateau (Sharpe 1,11-1,14, Rückgang 14-17 %, über alle drei Saisonlängen). Rückblick 252 ist schwächer (Sharpe 1,04-1,08, Rückgang 22-25 %). Der Spitzenwert Rückblick 756 / Saison 126 (1,23) hat schwächere Nachbarn (1,06 und 1,14): Einzelspitze, nicht übernehmen.
Offen für Saisonende: Bitcoin-Linie (SMA50/100 schlagen SMA200 bei Bitcoin allein; SMA100 ist bereits als Kandidat im Bitcoin-Kader, Data-Snooping-Vorbehalt von 2026-11-18 gilt).

## 2026-11-21: Test "FTSE All-World gegen S&P 500" (vorab festgelegt, vor dem Rechnen; ftse.py)
Frage: Ist ein weltweiter Index als Kern besser als der S&P 500?
Daten: echter FTSE All-World über den Vanguard FTSE All-World ETF (VWRL, Start 05/2012; älter frei nicht verfügbar) gegen SPY, Kurse inkl. Ausschüttungen, in Euro, gleicher Zeitraum. Kosten der ETFs sind im Kurs enthalten.
Kennzahlen: Rendite p. a., maximaler Rückgang, beide Hälften des Zeitraums, Anteil rollierender 5-Jahres-Fenster mit Vorsprung, Sparplan 100 €/Monat.
Kriterium (wie Faktor-ETFs und Top 20): Der FTSE All-World ersetzt den S&P 500 als Kern nur, wenn Rendite p. a. höher UND in BEIDEN Hälften höher UND maximaler Rückgang nicht größer. Sonst nur Anzeige auf der Seite.
Datenkorrektur (vor der Auswertung, nach dem ersten Lauf bemerkt): Die Yahoo-Reihe des VWRL hat 2013 einen Sprung von −24 % an einem Tag ohne entsprechende Marktbewegung (Datenfehler). Regel: Tagesbewegung über 12 % beim FTSE bei weniger als 5 % beim SPY gilt als Datenbruch; der Test beginnt nach dem letzten Bruch. Das Kriterium bleibt unverändert.

### Ergebnis "FTSE All-World gegen S&P 500" (2026-11-21, ftse.py)
Zeitraum 06/2013 bis 11/2026 in Euro, inkl. Ausschüttungen. S&P 500 15,2 %/J (x6,68), FTSE All-World 11,8 %/J (x4,46). Hälften (Teilung 03/2020): bis 2020 15,3 vs 10,3 %, ab 2020 15,1 vs 13,3 %. Maximaler Rückgang 33,1 vs 33,3 %: die breitere Streuung hat den Rückgang nicht verringert. Rollierende 5-Jahres-Fenster: FTSE in 0 von 102 vorn. Sparplan 100 €/Monat (16.200 € eingezahlt): 46.076 vs 37.433 €.
Kriterium NICHT erfüllt (in keinem Punkt). Der S&P 500 bleibt Kern. Einschränkung: nur 13 Jahre und eine Phase mit starkem US-Vorsprung; davor (z. B. 2000-2009) lag die Welt vor den USA. Der Test zeigt also nur diese Phase, nicht, dass es immer so ist.

## 2026-11-21: Monatlicher Power-Law-Check Bitcoin (powerlaw.py, festgelegt vor der Auswertung)
Mittellinie (fairer Wert): 1,0117e-17 × Tage^5,82 (Tage seit 3.1.2009, in Dollar). Untergrenze: 0,42 × Mittellinie, abgestimmt auf die rote Untergrenze bei bitbo am 21.11.2026 (rund 68.000 $).
Prüfung: jeden abgeschlossenen Monat am Monatsschluss (letzter Tagesschluss, Dollar). Schluss unter der Untergrenze = "Untergrenze in diesem Monat gebrochen". Kurse innerhalb des Monats zählen nicht. Gezeigt werden Stand, Monate in Folge darunter und alle Monate darunter seit 2015.
Folge: nur Information. Die Kaufregel (kaufen, sobald Geld da ist) bleibt unberührt; eine Anpassung des Modells nur per ausdrücklicher Entscheidung.
Erste Auswertung (Daten ab 07/2015): Monatsschlüsse unter der Untergrenze bisher nur 06/2026 (58.524 $, 1,7 % darunter). Tiefste frühere Monatsschlüsse: 12/2022 und 09/2015 (je knapp über der Linie, 0,43 × Mittellinie). November 2026 liegt laufend bei etwa 0,36 × Mittellinie (Stand 20.11.).

## 2026-11-21: Langzeit-Ergänzung "Welt gegen USA" (vorab festgelegt, vor dem Rechnen; worldlong.py)
Anlass: Der FTSE-Test umfasst nur 13 Jahre (eine Phase mit US-Vorsprung). Der FTSE All-World selbst ist frei nicht lange verfügbar; Ersatz mit gleicher Idee aus einer Quelle (MSCI, Gesamtrendite brutto, Monatsende, Dollar): MSCI World und MSCI ACWI (Welt inkl. Schwellenländer) gegen MSCI USA (entspricht praktisch dem S&P 500). Rechnung in Dollar; für einen Euro-Anleger ändert die Währung beide Seiten gleich, der Vergleich bleibt gleich.
Zeitraum: so weit die freie MSCI-Schnittstelle reicht. Beim ersten Abruf zeigte sich: Anfragen vor 01/1997 werden abgelehnt, geliefert werden Monatswerte ab 12/2000. Damit fehlen die 1970er/80er (u. a. Japan-Blase, als die Welt vorn lag).
Kennzahlen: Rendite p. a., größter Rückgang, Jahrzehnte einzeln, Anteil rollierender 10- und 20-Jahres-Zeiträume mit Vorsprung der Welt.
Kriterium wie beim FTSE-Test: Die Welt ersetzt den S&P 500 als Kern nur, wenn Rendite p. a. höher UND in BEIDEN Hälften höher UND größter Rückgang nicht größer. Sonst bleibt der S&P 500; das Ergebnis wird angezeigt.

### Ergebnis "Welt gegen USA" (2026-11-21, worldlong.py)
Zeitraum 12/2000 bis 10/2026 (knapp 26 Jahre), MSCI Gesamtrendite brutto in Dollar. USA 9,0 %/J, World 8,0 %, ACWI 7,9 %. Hälften (Teilung 11/2013): bis 2013 USA 4,5 % vs World 4,8 % / ACWI 5,1 % (Welt vorn); ab 2013 13,7 vs 11,3 / 10,7 % (USA vorn). Größter Rückgang USA 50,6 %, World 53,7 %, ACWI 54,6 % (die Welt fiel tiefer, nicht flacher). Jahrzehnte: 2000er USA 0,0 % p. a., World 1,8 %, ACWI 2,7 %; 2010er 13,6 vs 10,1 / 9,4 %; 2020er bisher 15,0 vs 13,3 / 12,7 %. Rollierend: 10 Jahre Welt vorn in 36 (World) bzw. 43 (ACWI) von 191 Zeiträumen (19-23 %), 20 Jahre in 0 von 71.
Kriterium NICHT erfüllt (erste Hälfte knapp vorn, aber Gesamtrendite, zweite Hälfte und Rückgang verfehlt). Der S&P 500 bleibt Kern. Das verlorene US-Jahrzehnt 2000-2009 ist enthalten: die Welt lag dort vorn, aber nur mit 2 bis 3 Prozentpunkten p. a. und mit tieferem Rückgang. Weiterhin nicht enthalten: 1970er/80er.

## 2026-11-21: Elite-Saisonprüfung (ausdrückliche Entscheidung)
Ab jetzt wird die Elite an JEDEM Saisonende geprüft (Saison = 63 Handelstage wie beim Prüfstand; erstes Saisonende ca. Ende Januar 2027). Automatisch im nächtlichen Datenlauf (elitecheck.py, elite_review.py), sobald eine neue Saison beginnt.
Geprüft: die harten Regeln mit aktuellen Kursen, gleiche Methode wie beim Screening: Beta < 1,15 (5 Jahre täglich, in Euro gegen S&P 500 in Euro) UND 10-Jahres-Rendite >= 17 % p. a. (inkl. Dividenden). Wer nicht besteht, scheidet aus, ohne Ausnahme (wie Entscheidung 2026-11-18). Freie Plätze werden NICHT automatisch nachbesetzt; Aufnahme nur per Screening und ausdrücklicher Entscheidung.
Schattenbuch: läuft verkettet weiter (Stand beim Ausscheiden = neue Basis, die Verbleibenden gleich gewichtet ab dem Prüftag). Die Endbewertung November 2031 bleibt unverändert.
Aufnahmewerte werden zum Prüftag neu eingefroren. Jede Prüfung wird hier automatisch eingetragen. Die weichen Regeln (Marge rund 50 % mit 1 Punkt Toleranz, Marktstellung, Zyklik, Verschuldung) werden nicht automatisch geprüft.
Stand bei Einführung (Kurse 20.11.2026): alle 6 bestehen (Ferrari 0,90 / 23,0 %; Mastercard 0,88 / 20,1 %; Visa 0,81 / 18,1 %; Cintas 0,76 / 24,0 %; Microsoft 1,09 / 24,5 %; IDEXX 1,09 / 19,0 %). Knapp: Microsoft und IDEXX beim Beta (1,09 von 1,15), Visa bei der Rendite (18,1 von 17 %).

## 2026-11-21: Elite-Saisonprüfung geändert: zwei Saisons in Folge (ausdrückliche Entscheidung)
Grund: Eine einzelne Prüfung ist eine Momentaufnahme; Grenzfälle (z. B. Visa 18,1 % bei Grenze 17 %) könnten durch Rauschen ausscheiden, ohne automatischen Wiedereinstieg. Eine jährliche Prüfung wäre ebenfalls nur eine Momentaufnahme, nur seltener.
Neu: Wer eine Saisonprüfung nicht besteht, wird verwarnt. Wer zwei Saisonprüfungen IN FOLGE nicht besteht, scheidet aus (ohne Ausnahme). Wer nach einer Verwarnung wieder besteht, ist zurück auf null. Echter Verfall wird damit nach etwa einem halben Jahr erkannt. Alles andere aus dem Eintrag zuvor gilt unverändert. Änderung vor der ersten Prüfung, also ohne Kenntnis eines Ergebnisses.

## 2026-11-21: Elite als eigener Index mit Bank und Einwechslung (ausdrückliche Entscheidung)
Universum (jede Saison neu): aktuelle S&P-500-Mitglieder (mit GICS-Branche) + feste Europa-Liste (data/elite_universe.json). Zyklische Branchen werden vorab ausgeschlossen und gar nicht gerechnet (eingefroren am 21.11.2026, freigegeben):
- Sektoren komplett: Energie, Rohstoffe (Materials), Immobilien.
- Branchen: Werbung, Rundfunk, Verlage; Autos und Zulieferer, Hausbau, Baumärkte, Möbelhandel, Hotels/Kreuzfahrten, Casinos, Freizeitprodukte, Mode/Accessoires/Luxus, Schuhe, Elektronikhandel, Unterhaltungselektronik; Banken (groß und regional), Investmentbanken/Broker, Konsumkredite, Vermögensverwalter/Depotbanken; Landmaschinen, Luftfracht/Logistik, Bauprodukte, Güterverkehr, Bau/Engineering, Baumaschinen/Lkw, Elektrokomponenten, Schwere Elektrotechnik, Industriemaschinen, Fluglinien, Bahn, Großhandel, Mischkonzerne, Personaldienste, Personenbeförderung; Halbleiter, Halbleiter-Anlagen, Elektronikbauteile, Elektronikfertigung, Hardware/Speicher, Kommunikationstechnik, Technik-Großhandel, Elektronische Geräte/Instrumente.
- Europa nicht zyklisch: Ferrari, Hermès, L'Oréal, EssilorLuxottica, Dassault Systèmes, Wolters Kluwer, SAP, Deutsche Börse, Munich Re, Novo Nordisk, LSEG, RELX, Experian, Diageo, Unilever, Nestlé, Lindt, Constellation Software. Zyklisch (ausgeschlossen): LVMH, Schneider Electric, Air Liquide, ASML, DSV, Atlas Copco, Investor AB, Sika, Partners Group, Evolution.
Aufnahmekriterien (alle, automatisch): Beta < 1,15 (5 J. täglich, Euro gegen S&P 500 in Euro); 10-J.-Rendite >= 17 % p. a. (Heimatwährung, inkl. Dividenden); Bruttomarge >= 49 % (rund 50 %, 1 Punkt Toleranz); Fremdkapital/Eigenkapital < 1 (Marge und Verschuldung aus Yahoo-Fundamentaldaten).
Bank: wer alle Aufnahmekriterien zwei Saisonprüfungen in Folge besteht. Größe der Elite: 6 Plätze. Wird ein Platz frei, wird der Bankspieler mit der höchsten 10-J.-Rendite privat per Telegram zur Einwechslung vorgeschlagen; nur der private Chat des Betreibers kann bestätigen oder ablehnen (bei Ablehnung folgt der nächste). Nach Bestätigung: Aufnahme, Schattenbuch verkettet (alle gleich gewichtet ab dem Tag), Eintrag hier automatisch. Ohne Antwort bleibt der Platz frei; Erinnerung nach 7 Tagen.
Verbleib: unverändert nach den beiden harten Regeln (Beta, 10-J.-Rendite), zwei Saisonprüfungen in Folge durchgefallen = raus. Marge und Verschuldung gelten nur für die Aufnahme.
Erstes Screening: 21.11.2026 (zählt als Saison 38). Bank frühestens nach der nächsten Saisonprüfung (ca. Ende Januar 2027).
Einschränkung: Das Universum besteht aus heutigen Großunternehmen; Auswahl nach vergangener Rendite.

## 2026-11-21: Aus Elite 6 werden die "Kronjuwelen" (ausdrückliche Entscheidung)
Grund: Im ersten Screening erfüllten 12 Unternehmen alle Aufnahmeregeln; eine feste Grenze bei 6 wäre willkürlich (Platz 6 und 7 unterscheiden sich nur in vergangener Rendite) und lädt zum Hin und Her ein.
Neu:
1. Dynamischer Index: Wer alle Regeln erfüllt, ist drin, gleich gewichtet. Keine feste Größe. Ersetzt "6 Plätze" und "Bank" aus dem Eintrag zuvor.
2. Regeln für Aufnahme UND Verbleib gleich (vier Regeln): Beta < 1,15; 10-J.-Rendite >= 17 % p. a.; Bruttomarge >= 49 %; Nettoverschuldung/EBITDA < 2 (Schulden minus Bargeld geteilt durch operativen Gewinn). Ersetzt Fremdkapital/Eigenkapital < 1: diese Kennzahl wird durch Aktienrückkäufe verzerrt (Mastercard 3,5, MSCI/AbbVie/HCA negatives Eigenkapital), obwohl die Firmen solide finanziert sind. Negatives oder fehlendes EBITDA = nicht bestanden.
3. Beta aus Wochenschlusskursen (5 Jahre = 260 Wochen) statt Tageskursen: Tageskurse verzerren das Beta europäischer Aktien wegen unterschiedlicher Handelszeiten (Deutsche Börse täglich 0,05). Neu berechnet (Kurse 20.11.2026): Ferrari 0,84, Mastercard 0,81, Visa 0,75, Cintas 0,69, Microsoft 1,05, IDEXX 1,11.
4. Rein: alle vier Regeln zwei Saisonprüfungen in Folge bestanden, dann Vorschlag per Telegram (privat), Aufnahme nach Bestätigung; Ablehnung gilt bis zur nächsten Saisonprüfung. Raus: zwei Saisonprüfungen in Folge durchgefallen (automatisch). Bei jeder Änderung Schattenbuch verkettet, alle gleich gewichtet (Umschichtung nur bei Änderungen, also höchstens an Saisonenden).
5. Start: die bisherigen sechs Werte. Weitere Aufnahmen frühestens nach der nächsten Saisonprüfung (ca. Ende Januar 2027). Die Endbewertung des Schattenbuchs (November 2031) bleibt.

## 2026-11-21: Test "Puffer für die Kronjuwelen" (vorab festgelegt, vor dem Rechnen; buffertest.py)
Frage: Welcher Abstand zwischen Aufnahme- und Ausscheidegrenze verhindert das Hin und Her, ohne Rendite zu kosten? Hintergrund: privat nachgebildet als Sparplan-Index, der nie verkauft (Ausgeschiedene bekommen kein neues Geld, bleiben aber liegen).
Daten: die nicht-zyklischen Firmen des Screenings vom 21.11.2026, Tageskurse (Yahoo, inkl. Dividenden) ab 2006, in Euro. Prüfung jedes Quartal ab 2016 (63 Handelstage). Rein: Beta < 1,15 (Wochenkurse, 5 Jahre) UND 10-J.-Rendite >= 17 %, zwei Prüfungen in Folge. Start 2016 mit allen, die bei den ersten zwei Prüfungen bestehen.
Varianten (Raus nach zwei Prüfungen in Folge außerhalb): ohne Puffer (Beta > 1,15 oder < 17 %), schmal (> 1,20 oder < 15 %), mittel (> 1,25 oder < 14 %), breit (> 1,30 oder < 12 %).
Sparplan: 100 € je Monat, gleich verteilt auf die aktuellen Mitglieder, nie verkaufen. Vergleich: gleicher Sparplan auf den S&P 500.
Kennzahlen: Änderungen pro Jahr; "Rückkehrer" (raus und innerhalb von 8 Quartalen wieder rein); Endwert und Rendite p. a. (interner Zinsfuß) des Sparplans.
Kriterium: Gewählt wird der Puffer mit den wenigsten Rückkehrern, dessen Sparplan-Rendite höchstens 0,5 Punkte p. a. unter "ohne Puffer" liegt; Plateau: mindestens ein Nachbar (schmal/mittel/breit) liegt bei Rückkehrern und Rendite ähnlich. Sonst bleibt es ohne Puffer.
Grenzen: Marge und Verschuldung historisch nicht verfügbar, nur Beta und Rendite getestet. Firmenliste von heute (Pleiten fehlen, Rendite zu hoch); für den Vergleich der Varianten untereinander unkritisch.

## 2026-11-21: Kronjuwelen: Aufnahme automatisch, Gewichtung gleich (ausdrückliche Entscheidung)
Aufnahme ohne Bestätigung: Wer alle vier Regeln zwei Saisonprüfungen in Folge besteht, wird bei der Saisonprüfung automatisch aufgenommen (Index-Logik, keine Einzelentscheidung). Telegram meldet Aufnahmen, Ausscheiden und Verwarnungen privat, nur zur Information. Ersetzt Punkt 4 ("Vorschlag per Telegram, Aufnahme nach Bestätigung") des Eintrags zuvor.
Gleichgewichtung bleibt: Die Rangfolge nach 10-Jahres-Rendite ist Vergangenheit und kein Qualitätsmaß; eine Gewichtung danach wäre eine Wette auf Fortsetzung. Eine Gewichtung nach Börsenwert würde von Microsoft, Visa und Mastercard dominiert. Gleich gewichtet ist die neutrale Regel ohne Schätzung. Die Rangfolge wird nur angezeigt.

### Ergebnis "Puffer für die Kronjuwelen" (2026-11-21, buffertest.py)
254 Firmen mit Daten, 44 Quartalsprüfungen 01/2016 bis 10/2026, Sparplan 100 €/Monat (12.700 € eingezahlt), nie verkaufen. Ohne Puffer: 40 Änderungen/Jahr, 55 Rückkehrer, Sparplan 11,3 % p. a. Schmal: 32, 25, 11,3 %. Mittel: 28, 13, 11,3 %. Breit: 23, 1, 11,3 %. Rendite in allen Varianten praktisch gleich (11,25-11,30 %).
Kriterium erfüllt für "breit" (wenigste Rückkehrer, Rendite gleich; Nachbar "mittel" ebenfalls mit wenigen Rückkehrern und gleicher Rendite).
Nebenbefund (wichtig): Gleicher Sparplan auf den S&P 500 im selben Zeitraum 13,9 % p. a. (27.499 € statt 23.700 €). Die Regel nur mit Beta und 10-J.-Rendite lag 2,6 Punkte p. a. hinter dem Index, trotz Firmenliste von heute (Pleiten fehlen, Ergebnis eher zu gut). Ohne Marge und Verschuldung wird der Index sehr groß (durchschnittlich 59 bis 89 Werte). Ob die beiden zusätzlichen Filter das ändern, ist historisch nicht prüfbar; das zeigt nur das Schattenbuch.

## 2026-11-21: Kronjuwelen als Sparplan-Index mit Puffer (ausdrückliche Entscheidung)
1. Puffer "breit": Aufnahme nur bei allen strengen Regeln (Beta < 1,15; 10-J.-Rendite >= 17 %; Bruttomarge >= 49 %; Nettoverschuldung/EBITDA < 2), zwei Prüfungen in Folge. Ausscheiden erst bei klarer Verfehlung, zwei Prüfungen in Folge: Beta > 1,30 oder 10-J.-Rendite < 12 %. Für Marge und Verschuldung analog gesetzt, NICHT getestet: Marge < 45 % oder Nettoverschuldung/EBITDA >= 2,5 (bzw. EBITDA negativ/fehlend).
2. Sparplan-Index, nie verkaufen: Jeden Monat gleicher Betrag, gleich verteilt auf die aktuellen Mitglieder. Ausgeschiedene bekommen kein neues Geld, bleiben aber im Bestand. Rückkehrer bekommen wieder Geld. Das Schattenbuch rechnet genau so (100 € je Monat ab 17.11.2026, gegen den gleichen Sparplan auf den S&P 500; Kennzahl Wert je eingezahltem Euro). Zusätzlich läuft das Einmal-Schattenbuch weiter (beide nebeneinander, ausdrückliche Entscheidung): gleich gewichtet, umgeschichtet nur bei Änderungen. Endbewertung November 2031: bewährt, wenn die Sparplan-Rendite (interner Zinsfuß) mindestens 2 Punkte p. a. über dem S&P-500-Sparplan liegt; gescheitert, wenn darunter.
3. Meldungen per Telegram (privat) bei jeder Änderung mit konkreten Schritten (Sparplan starten / stoppen, nicht verkaufen).
4. Kennzeichnung auf der Seite als Experiment mit dem Ergebnis des Puffer-Tests (Regel im Rückblick 2,6 Punkte p. a. hinter dem S&P 500). Am Kern ändert sich nichts: der S&P 500 bleibt das Fundament.

### Ergänzung Puffer-Test: Einmalanlage (vorab festgelegt, vor dem Rechnen)
Gleicher Aufbau, zusätzlich: Einmalanlage ab der ersten Prüfung mit Mitgliedern, gleich gewichtet, umgeschichtet (verkauft und gleich verteilt) nur bei Änderungen der Mitglieder; gegen Einmalanlage im S&P 500 ab demselben Tag. Kennzahl Rendite p. a. Frage: Liegt der Rückstand am Sparplan?
Ergebnis Einmalanlage (2026-11-21): Start 05.04.2016, S&P 500 14,3 % p. a. Ohne Puffer 12,7 %, schmal 13,1 %, mittel 13,6 %, breit 14,0 % (38 Umschichtungen). Mit Einmalanlage ist der Rückstand deutlich kleiner als im Sparplan (breit: 0,3 statt 2,6 Punkte p. a.); der Puffer hilft hier zusätzlich (weniger Verkäufe von Werten, die später zurückkommen). Geschlagen wird der S&P 500 aber in keiner Variante. Der Puffer "breit" bestätigt sich.

## 2026-11-21: Kronjuwelen-Start: vorige Saisonprüfung nachgerechnet (vorab festgelegt, vor dem Rechnen; eliteretro.py)
Grund: Die Anwärter hatten nur Serie 1, weil erst am 21.11. gerechnet wurde, nicht weil sie vorher nicht bestanden hätten.
Regel: Die vorige Saisonprüfung (Beginn der laufenden Saison) wird nachgerechnet. Beta (Wochenkurse, 5 J., Euro) und 10-J.-Rendite aus Kursen bis zum Stichtag; Marge und Nettoverschuldung/EBITDA mit den heutigen Werten (Annahme: in drei Monaten praktisch unverändert, historisch frei nicht verfügbar). Das Screening vom 21.11. zählt als Prüfung der laufenden Saison.
Folge: Wer zum Stichtag UND am 21.11. alle Regeln erfüllt, wird jetzt aufgenommen (Änderung in beiden Schattenbüchern ab dem 20.11., dem letzten Kurstag). Mitglieder, die zum Stichtag klar verfehlt hätten (Puffer-Grenzen), erhalten eine Verwarnung; bei klarer Verfehlung an beiden Terminen scheiden sie aus. Einmalig zum Start.

## 2026-11-20: Kronjuwelen-Aufnahme (Start: Saisonprüfungen 2026-10-27 und 2026-11-20 bestanden)
Lilly (Eli) (LLY): 10 J. 35,2 % p. a., Beta 0,65, Bruttomarge 83,6 %, Nettoverschuldung 0,96× EBITDA, alle Regeln 2 Saisons in Folge bestanden. Ab jetzt neues Geld gleich verteilt auf 7 Werte.

## 2026-11-20: Kronjuwelen-Aufnahme (Start: Saisonprüfungen 2026-10-27 und 2026-11-20 bestanden)
Veeva Systems (VEEV): 10 J. 20,4 % p. a., Beta 0,99, Bruttomarge 75,0 %, Nettoverschuldung -6,59× EBITDA, alle Regeln 2 Saisons in Folge bestanden. Ab jetzt neues Geld gleich verteilt auf 8 Werte.

## 2026-11-20: Kronjuwelen-Aufnahme (Start: Saisonprüfungen 2026-10-27 und 2026-11-20 bestanden)
Cboe Global Markets (CBOE): 10 J. 19,5 % p. a., Beta 0,15, Bruttomarge 53,9 %, Nettoverschuldung -0,53× EBITDA, alle Regeln 2 Saisons in Folge bestanden. Ab jetzt neues Geld gleich verteilt auf 9 Werte.

## 2026-11-20: Kronjuwelen-Aufnahme (Start: Saisonprüfungen 2026-10-27 und 2026-11-20 bestanden)
Vertex Pharmaceuticals (VRTX): 10 J. 19,2 % p. a., Beta 0,54, Bruttomarge 54,8 %, Nettoverschuldung 0,03× EBITDA, alle Regeln 2 Saisons in Folge bestanden. Ab jetzt neues Geld gleich verteilt auf 10 Werte.

## 2026-11-20: Kronjuwelen-Aufnahme (Start: Saisonprüfungen 2026-10-27 und 2026-11-20 bestanden)
Moody's Corporation (MCO): 10 J. 17,6 % p. a., Beta 0,97, Bruttomarge 74,6 %, Nettoverschuldung 1,48× EBITDA, alle Regeln 2 Saisons in Folge bestanden. Ab jetzt neues Geld gleich verteilt auf 11 Werte.

## 2026-11-21: News-Archiv (ausdrückliche Entscheidung)
Startseite: neueste Meldung, darunter aufklappbar nur die letzten 7 Tage. Meldungen älter als 30 Tage verschiebt der nächtliche Lauf in Monatsdateien (site/archive/news-JJJJ-MM.json, archive_news.py); nichts wird gelöscht. Archivseite archiv.html mit Monatsauswahl, Tagesmeldungen und Monats-/Jahresberichten. Die Grenze von 60 Einträgen im News-Monitor entfällt.

## 2026-11-21: Seite neu gegliedert (ausdrückliche Entscheidung)
Reihenfolge nach Priorität: Aktuell (News kompakt mit aufklappbaren Details, Berichte, Kaufen, drei Karten, Rechner, Marktlage, Bitcoin Power Law), Belege (Der Beleg, König der Könige mit FTSE-Test, Welt gegen USA und Faktor-ETFs als aufklappbare Details, S&P 500 seit 1928), Experimente (Kronjuwelen, Schattenbuch Sparplan, Prüfstand Mannschaft). Verlaufstabellen (Mannschaft, Kronjuwelen, Sparplan) auf der Startseite: letzte 7 Tage (wie bei den News); alle Tageswerte der Schattenbücher im Archiv je Monat. Menü oben links mit denselben Gruppen. Inhalte und Zahlen unverändert.

## 2026-11-21: Regelbuch und Protokoll getrennt (ausdrückliche Entscheidung)
Das Regelbuch (REGELBUCH.md, Seite regeln.html) zeigt nur, was heute gilt, nach Themen, mit "seit"-Datum je Regel. Diese Datei ist ab jetzt das Protokoll (Seite protokoll.html, neueste Einträge zuerst). Jede Regeländerung: Regelbuch anpassen UND Eintrag hier. Automatische Saisonprüfungen schreiben nur ins Protokoll.

## 2026-11-21: Telegram-Filter korrigiert (Durchsicht)
Der Kronjuwelen-Abschnitt des Monatsberichts wurde in Telegram versehentlich herausgefiltert (Filter stammte aus der Zeit der internen Elite 6). Jetzt: Kronjuwelen-Zeilen gehen neutral in den Kanal; Schattenbuch-Zeilen bleiben intern; Sparplan-Schritte nur privat.

## 2026-11-21: Namen geschärft (ausdrückliche Entscheidung)
"Schattenbuch Sparplan" heißt "Schattenbuch Sparplan S&P 500". "Mannschaft" heißt "Taktikmodell 3 Könige": Es wählt je Saison die Strategie pro Wert (Trend, für Bitcoin aus Kandidaten) und verteilt das Kapital nach Schwankung, ist also mehr als ein reines Trendmodell. Inhalt unverändert.

## 2026-11-21: Taktikmodell: Signal bleibt sichtbar, private Meldung (Fehlerbehebung)
Fehler: Die Nacht läuft mehrmals. Der erste Lauf führte das Signal im Schattenbuch aus, spätere Läufe derselben Nacht sahen keine Abweichung mehr und zeigten "Nichts tun". So war der Verkauf vom 20.11. (S&P 500 49 % → 0 %) auf der Seite nie zu sehen. Jetzt: Das Signal eines Datentags bleibt bis zum nächsten Datentag sichtbar ("Signal zum Schlusskurs vom …, Umsetzung am nächsten Handelstag"); bei jedem neuen Signal kommt eine private Telegram-Meldung. Offener Punkt (nicht geändert): Das Schattenbuch rechnet die Umschichtung zum Schlusskurs des Signaltags; real ist erst der nächste Handelstag möglich.

## 2026-11-21: Taktikmodell: Umsetzung am nächsten Handelstag (ausdrückliche Entscheidung)
Bisher buchte das Schattenbuch eine Umschichtung zum Schlusskurs desselben Tages, an dem das Signal entstand (einen Tag zu optimistisch: real sieht man das Signal erst am Morgen danach). Neu: Signal zum Schlusskurs von Tag D, Ausführung im Schattenbuch zum Schlusskurs des nächsten Handelstags; bis dahin gilt der alte Bestand. Rückwirkend angewendet auf das Signal vom 20.11.2026 (S&P 500 49 % → 0 %): Ausführung erst am nächsten Handelstag; Schattenbuch 0,9674 → 0,9676 (Handelskosten zurückgebucht). Seite zeigt offenes Signal und danach "Umgesetzt zum Schlusskurs vom … (Signal vom …)".

## 2026-11-21: Kronjuwelen: Umsetzung am nächsten Handelstag (ausdrückliche Entscheidung)
Wie beim Taktikmodell: Änderungen aus der Saisonprüfung (Aufnahme, Ausscheiden) gelten in beiden Schattenbüchern erst ab dem Schlusskurs des nächsten Handelstags, nicht schon zum Schlusskurs des Prüftags. Rückwirkend für die fünf Aufnahmen vom 20.11.2026 (Eli Lilly, Veeva, Vertex, Cboe, Moody's): wirksam ab dem nächsten Handelstag; die Werte bis zum 20.11. ändern sich dadurch nicht.

## 2026-11-21: Wächter für den Wächter (ausdrückliche Entscheidung)
watchdog.py, täglich 8:04 UTC (9:04 Uhr Winterzeit): meldet privat per Telegram, wenn der nächtliche Datenlauf oder der News-Monitor länger als 26 Stunden nichts geschrieben hat, die Kurse älter als 4 Tage sind oder am Monatsanfang der Monatsbericht fehlt. Sonntags kurze Meldung "Alles läuft".

## 2026-11-21: Marktbarometer mit Ampelfarben (ausdrückliche Entscheidung)
Neue Leiste „Lage auf einen Blick“ oben auf der Seite mit S&P 500, Bitcoin, Gold, Öl, US-Zins, EZB-Zins, Euro in Dollar, Inflation USA und Eurozone, Angst und Gier, VIX. Kacheln grün, gelb oder rot nach den Grenzen im Regelbuch (Abschnitt Marktbarometer). Nur Information, kein Signal. Quellen: Yahoo, EZB-Datenportal, US-Arbeitsstatistik (BLS), Eurostat (neue HICP-Reihe ab 2026).

## 2026-11-21: Marktlage zusammengeführt, Thesen zum Barometer (ausdrückliche Entscheidung)
Die alte Marktlage weiter unten und die Kacheln oben sind jetzt ein Block „Marktlage“ oben. Neu als Kacheln: Shiller-KGV, Buffett-Indikator, Zinskurve (Grenzen im Regelbuch). Die alte Chancen-Farbe (extreme Angst = grün) entfällt, damit es nur eine Farblogik gibt; die Einordnung „war oft eine Kaufgelegenheit“ steht weiter als Text in den Details. Vier Thesen A bis D vorab festgelegt (siehe Regelbuch), Werte und Farben werden ab heute täglich festgehalten. Start: 10 von 14 Kacheln rot, 1 grün.

## 2026-11-21: Rücktest der Barometer-Thesen (Kriterien vorab im Code festgelegt)
thesen.py, nächtlich. A (VIX über 30 als Ersatz für Angst und Gier): S&P 500 12 Monate danach +22,3 % statt +10,2 %, 26 Phasen seit 1990: bestätigt. B (US-Inflation über 3,5 % und 10-J.-Zins über 4,75 %): +5,6 % statt +7,3 %, 14 Phasen seit 1900, Abstand unter 3 Punkten: nicht bestätigt. C (Zahl roter Kacheln sagt nichts): widerlegt, Korrelation −0,18; 0–1 rot ca. +11 %, 2 rot +5 %, 3 rot −4 % (aus VIX, KGV, Inflation, Zins). D (Krypto-Angst rot und Bitcoin unter Power-Law-Mitte): +193 % statt +78 %, 7 Phasen seit 2018: bestätigt, kurze Historie. Heute aktiv: A, B, D. Nur Einordnung, Kaufregel unberührt. Neue Kachel Bitcoin zur Power-Law-Mitte (16 Kacheln, Raster 4 × 4 bzw. 2 × 8).

## 2026-11-21: Seite neu geordnet (ausdrückliche Entscheidung, keine Regeländerung)
Power-Law-Check direkt unter der Marktlage. Kaufen und Rechner sind ein Block. Neu unter Experimente: „Schattenbücher im Überblick“ mit allen vier Büchern (Kronjuwelen Einmalanlage und Sparplan, Sparplan S&P 500, Taktikmodell) und dem Abstand zum jeweiligen Vergleich.

## 2026-11-21: Hinweis Mehrfachtest bei den Barometer-Thesen
Nach externer Prüfung ergänzt: Vier Thesen auf denselben Daten, eine kann auch zufällig passen; p-Werte sind wegen überlappender 12-Monats-Fenster nicht aussagekräftig. Keine Regeländerung.

## 2026-11-21: Größe der Kronjuwelen unter Beobachtung
Keine Obergrenze für die Zahl der Mitglieder, keine Regeländerung. Die Größe des Index wird beobachtet.

## 2026-11-21: Kronjuwelen, Unterbranchen-Ausschluss gestrichen (ausdrückliche Entscheidung)
Anlass: Apple wurde als „Technology Hardware“ gar nicht gerechnet, obwohl ein großer Teil des Geschäfts aus Services stammt. Statt einer Ausnahme für Apple gilt ein Grundsatz: Ausgeschlossen bleiben nur die Sektoren Energie, Rohstoffe und Immobilien; über Konjunkturschwankung entscheidet bei allen anderen das Beta. Alle anderen Regeln bleiben, die Marge bleibt bei 49 % (Ursprung: „über 50 %“ aus der Elite-9-Liste, 1 Punkt Toleranz seit 18.11.2026). Gilt ab der nächsten Saisonprüfung (ca. Ende Januar 2027), Aufnahme wie immer erst nach zwei bestandenen Prüfungen in Folge.
Prüfung vorab (nur Information): 185 Firmen kommen zusätzlich in die Wertung. Heute würden 4 alle Regeln erfüllen: Evolution (Beta 0,44, 10 J. 32,9 %), ASML (1,08; 29,3 %), Garmin (0,86; 20,8 %), Investor AB (0,64; 20,7 %). Apple: Beta 1,14, 10 J. 29,6 %, Marge 48,8 % (0,2 Punkte zu wenig), Schulden 0,2: scheitert nur an der Marge (Jahresmarge 2025: 46,9 %, Rekord seit den 1990ern).
