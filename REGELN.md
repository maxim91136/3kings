# Regeländerungen (Protokoll)

Regeln ändern sich nur am Saisonende oder nach ausdrücklicher Entscheidung. Jede Änderung steht hier.

- 2026-11-18: Bitcoin bekommt zusätzlich den Kandidaten **Trend SMA100** (schnelle Trend-Linie, 100 Tage).
  Grund: Test auf echten Kursen, Sharpe der Mannschaft 1,25 statt 1,12, gleicher Rückgang (15 %).
  Vorbehalt: Linie wurde nach Ansicht der Ergebnisse gewählt (Data-Snooping), p-Wert daher optimistisch.
  Wirkung heute: keine, Bitcoin-Champion bleibt Trend SMA200. Live im Schattenbuch beobachten.

## 2026-11-18: Aufnahmetest Aktien-ETFs und Power-Law (echte Daten)
- Gepruefte Kandidaten: URTH, VT, QUAL, MTUM, USMV, XLK, TLT, IEF, EFA, EEM, ETH. Keiner hat die Regeln bestanden (Mannschaft-Sharpe 1,25 ohne, 1,00 bis 1,24 mit Kandidat). Kein Wechsel, keine Ersatzbank-Aufnahme.
- Power-Law (kausal, Daten ab 2010): PL-Rampe Sharpe 0,87 = Halten, aber Rueckgang 49 % statt 83 %. Keine bessere Rendite. Kein Signal in der Heartbeat-Regel; nur als Info moeglich.

## 2026-11-18: Bitcoin-Gewichtung Stufe 2 (Entscheidung des Nutzers)
- Kapitalverteilung: Inverse Volatilitaet, Bitcoin-Gewicht x2 (Spot, kein Hebel, Summe nie ueber 100 %).
- Test 2017-2026: Rendite 14,9 -> 17,6 %/J, Rueckgang 15 -> 16 %, Sharpe 1,25 gleich. Stufen x3/x5 verworfen (Rueckgang 21/29 %). Rueckblick-Test, keine Garantie.
- XLK als vierter Koenig und Aufnahme der ETFs/ETH/Anleihen: nicht aufgenommen (kaum Effekt, zu nah an SPY).
- Aufnahmetest ETFs und Power-Law (echte Daten): alle 11 Kandidaten durchgefallen; Power-Law-Rampe = Halten bei geringerem Rueckgang, nicht aufgenommen.
- Naechste Pruefung der Regeln: Saisonende.

## 2026-11-18: Vorab festgelegt, woran wir die Regeln messen (bevor die Ergebnisse da sind)
Grundsatz: kein Hin und Her. Regeln aendern sich nur zum Saisonende oder per ausdruecklicher Entscheidung, nie nach Bauchgefuehl.
1. Langzeittest S&P 500 (longtest.py, Preisindex ab 1928): Der Trendfilter gilt fuer den S&P nur als belegt, wenn er in den Krisenepochen 1973-1982 UND 2000-2009 den Rueckgang gegenueber Halten senkt. Sonst wird er fuer den S&P neu bewertet (zum naechsten Saisonende).
2. Live-Pruefung (Schattenbuch, nach 4 Saisons = ca. Nov 2027): bestaetigt, wenn Rueckgang kleiner als beim Halten und Rendite hoechstens 2 Punkte darunter; gescheitert, wenn Rendite mehr als 5 Punkte darunter UND Rueckgang nicht kleiner; sonst weiter beobachten.

### Ergebnis Langzeittest S&P (2026-11-18, Preisindex 1930-2026, ohne Dividenden/Zins)
Kriterium 1 erfuellt: Trend SMA200 senkt den Rueckgang in 1973-1982 (48 -> 16 %) und 2000-2009 (57 -> 26 %). Ueber alles: Rendite 6,3 % vs 6,2 % (Halten), Rueckgang 49 % vs 83 %. Schwaeche: 2010-2026 Trend 6,6 % vs Halten 11,8 %/J. Vol-Target schuetzt in Crashs deutlich schwaecher (1930er 72 %, 2000er 47 %), war 2010-2026 aber besser als Trend. Keine Regelaenderung.

## 2026-11-18: Studie "Einstieg in Stufen" (vorab festgelegt, vor dem Rechnen)
Idee: nach einem Trendbruch nicht alles auf einmal, sondern mit einem Teil frueher zurueck. Genau 3 Regeln, nichts nachtraeglich dazu (Mehrfachtest-Schutz):
- R0 Basis: Trend SMA200 (ganz oder gar nicht).
- R1 Zwei Stufen: 50 % investiert, wenn Kurs ueber SMA50; weitere 50 %, wenn ueber SMA200.
- R2 Drei Stufen: je ein Drittel ueber SMA50, SMA100, SMA200.
- R3 Tief-Stufe: wie R0, zusaetzlich 50 % investiert, wenn Kurs ueber SMA50 UND mindestens 20 % unter dem 252-Tage-Hoch lag (Erholung nach tiefem Rueckgang).
Daten: S&P 500 ab 1930 (Epochen wie longtest.py), Bitcoin ab 2011 (btc_long.csv, vier Epochen). Kosten 5 bps (S&P) bzw. 10 bps (BTC) je Umschichtung.
Kriterium: Eine Regel gilt als besser als R0 nur, wenn (a) ihr Sharpe in der Mehrzahl der Epochen mindestens so gut ist wie R0 (S&P: mind. 4 von 6, BTC: mind. 3 von 4), (b) ueber alles Sharpe mind. +0,03, (c) der maximale Rueckgang ueber alles nicht mehr als 3 Punkte und in den S&P-Krisenepochen 1973-1982 und 2000-2009 nicht mehr als 5 Punkte schlechter ist. Bestehen mehrere, gilt die einfachste. Gilt nur, wenn Kriterium fuer S&P UND Bitcoin erfuellt; sonst keine Aenderung. Einbau fruehestens zum Saisonende.

### Ergebnis Studie "Einstieg in Stufen" (2026-11-18, staged.py)
S&P (1930-2026): R1/R2/R3 verfehlen das Kriterium (Sharpe in nur 3 von 6 Epochen mindestens so gut wie R0; gesamt +0,01 bis +0,02). Stufen helfen 1930-1982, schaden 1983-2009 (Fehlsignale). Bitcoin (2011-2026): alle drei erfuellen das Kriterium (R1: Sharpe 1,20 -> 1,37, Rueckgang 78 -> 71 %, in 4 von 4 Epochen besser). Gesamtkriterium (S&P UND Bitcoin) NICHT erfuellt -> keine Regelaenderung. Offen fuer Saisonende: Bitcoin-Stufen (R1) als ausdrueckliche Einzelentscheidung, nicht per Regel.

## 2026-11-18: Review (Opus) - vorab festgelegt, vor dem Rechnen (review.py)
Annahmen: S&P-Preisindex 1928-2026 ohne Dividenden, Cash ohne Zins (beides wirkt grob gegeneinander). Steuer: 26,375 % Abgeltungsteuer, 30 % Teilfreistellung (Aktien-ETF) = 18,46 % auf realisierte Gewinne, Verlusttopf, Freibetrag nicht beruecksichtigt. Kosten 5 bps je Umschichtung. Umschichtung nur bei mehr als 2 Punkten Abweichung.
Frage 1 - fester Champion fuer den S&P: Trend SMA200 ersetzt die Champion-Wahl beim S&P, wenn er nach Steuern ueber 1930-2026 (a) Rendite hoechstens 0,3 Punkte unter der Champion-Wahl, (b) kleineren Rueckgang gesamt und (c) kleineren Rueckgang in 1973-1982 und 2000-2009 hat.
Frage 2 - Kaufregel fuer neues Geld (monatlich gleicher Betrag, Fenster 10 und 20 Jahre, Start alle 6 Monate ab 1930):
  K1 sofort kaufen, nie verkaufen; K2 Kauf-Pause: kaufen nur ueber SMA200, sonst sammeln, Gesammeltes beim Signal kaufen, nie verkaufen; K3 Trend voll (kauft und verkauft mit SMA200); K4 Dip-Reserve: 80 % sofort, 20 % Reserve, Reserve komplett rein bei Rueckgang >= 20 % vom 12-Monats-Hoch, nie verkaufen; K5 heutige Champion-Wahl.
  Empfohlen wird die Regel mit dem hoechsten Median-Endvermoegen nach Steuern ueber 20-Jahres-Fenster. Eine andere Regel wird nur empfohlen, wenn ihr Median hoechstens 2 % darunter liegt UND ihr schlimmster Buchverlust (Wert/Eingezahlt) im Median der Fenster mindestens 10 Punkte kleiner ist.

### Ergebnis Review (2026-11-18, review.py)
Frage 1 ERFUELLT: nach Steuern 1930-2026 Trend SMA200 5,2 %/J, Rueckgang 49 % vs Champion-Wahl 4,3 %/J, 64 % (Krisen 17 vs 22 %, 26 vs 49 %). Halten 6,0 %/J, 83 %. -> S&P spielt ab sofort fest Trend SMA200 (heartbeat.py FIXED). Mannschaft 2017-2026 dadurch praktisch gleich (17,6 %/J, Rueckgang 17 statt 16 %, Sharpe 1,26).
Frage 2: 20-Jahres-Fenster Median Endwert/Eingezahlt: K1 sofort 2,14; K2 Kauf-Pause 2,14; K4 Dip-Reserve 2,08; K3 Trend voll 1,82; K5 Champion 1,69. Nach Kriterium empfohlen: K1 (sofort kaufen). K2 gleicher Median, schlimmster Buchverlust -38 statt -67 %, Median-Buchverlust nur 4 Punkte kleiner (Kriterium 10) -> nicht empfohlen, nur als ausdrueckliche Entscheidung moeglich.
Seite: "Neues Geld / nur S&P 500" zeigt jetzt K1 (kaufen, ganzer Betrag) plus Trendlage als Info.

## 2026-11-18: Kaufregel neues Geld = "nicht am Hoch" (ausdrueckliche Entscheidung des Nutzers)
Grundsatz des Nutzers: nicht am Allzeithoch kaufen. ath.py (S&P 1930-2026, monatlich, vor Steuern): "nicht am Hoch" (kaufen nur, wenn mind. 3 % unter dem Allzeithoch, sonst sammeln) 20 Jahre Median 2,43 vs sofort 2,44, besser in 41 % der Fenster - kostet praktisch nichts. "Warte auf -10 %" kostet deutlich (2,18). Kauf ab -20 % brachte im Schnitt mehr (5 Jahre 10,9 vs 8,7 %/J am Hoch), Kauf am Hoch war aber nicht oefter im Minus als bei -3 bis -20 %.
Regel: S&P innerhalb 3 % vom Allzeithoch -> sammeln; sonst Betrag plus Reserve kaufen. Ersetzt K1 auf der Seite.

## 2026-11-18: Studie "Bewertung + Angst" fuer die Kaufregel (vorab festgelegt, valuation.py)
Neues Geld monatlich, S&P-Preisindex, vor Steuern, Cash ohne Zins, Dividenden nicht enthalten. Bewertung = Shiller-KGV als Perzentil seiner EIGENEN Geschichte bis zum jeweiligen Tag (kausal). Angst = VIX (erst ab 1990).
Regeln: N "nicht am Hoch" (heutige Regel, kaufen ab 3 % unter Allzeithoch). B1 Bewertungsbremse: ist das KGV im obersten Fuenftel seiner Geschichte, wird erst ab 10 % unter dem Hoch gekauft, sonst wie N. B2 wie B1, aber erst ab 20 %. B3 wie B1, gesammeltes Geld wird nach spaetestens 12 Monaten trotzdem investiert. A1 (ab 1990) Angst-Kauf: wie N, zusaetzlich wird bei VIX >= 30 sofort alles investiert, auch nahe am Hoch. A2 (ab 1990): B1 plus Angst-Kauf (VIX >= 30 hebt die Bremse auf).
Kriterium: eine Regel ersetzt N nur, wenn ueber 20-Jahres-Fenster (bzw. 10-Jahres-Fenster bei den Angst-Regeln) der Median-Endwert hoechstens 1 % unter N liegt UND die schlechtesten 10 % besser sind als bei N, ODER der Median mindestens 2 % ueber N liegt.

### Ergebnis Studie "Bewertung + Angst" (2026-11-18)
Keine Regel erfuellt das Kriterium, N bleibt. 20 J ab 1930: N 2,43 | B1 2,26 (laengste Wartezeit 6,2 J) | B2 2,19 (9,6 J) | B3 2,40. Grund: Shiller-KGV seit 1995 an 94 % der Tage im obersten Fuenftel seiner Geschichte - eine Bewertungsbremse wartet jahrelang. 10 J ab 1990: A1 (Angst-Kauf VIX >= 30) identisch mit N, weil hohe Angst immer mit Kursen mehr als 3 % unter dem Hoch zusammenfiel - N kauft in Angstphasen also schon. A2 1,47 vs N 1,53.

## 2026-11-18: Nachtrag "relative Bewertung" (vorab festgelegt, valuation.py --relativ)
Shiller-KGV als Perzentil nur der letzten 10 bzw. 20 Jahre (kausal). R10/R20: im obersten Fuenftel dieses Fensters erst ab 10 % unter dem Hoch kaufen, sonst wie N. R10c: wie R10, nach spaetestens 12 Monaten Warten trotzdem kaufen. G10: im untersten Fuenftel der letzten 10 Jahre sofort kaufen, auch nahe am Hoch, sonst wie N. Gleiches Kriterium wie oben (20-Jahres-Fenster ab 1930).
Ergebnis: keine Regel erfuellt das Kriterium, N bleibt. N 2,43 | R10 2,19 | R20 2,26 | R10c 2,37 | G10 2,43 (identisch mit N: guenstige Phasen fielen immer mit Kursen unter dem Hoch zusammen). Relativ "teuer" ist an rund 36 % der Tage - die Bremse verpasst dann die Aufschwuenge.

## 2026-11-18: Studie "Relative Staerke fuer neues Geld" (vorab festgelegt, strength.py)
Monatlich 1 Einheit neues Geld, nie verkaufen, Kosten 5 bps (BTC 10 bps). Fenster 5 Jahre, Start jeden Monat. Regeln:
M0 alles in den S&P (Vergleich). M1 gleich auf alle verteilt. M2 alles in den Staerksten der letzten 6 Monate. M3 alles in den Staerksten der letzten 12 Monate ohne den letzten Monat (12-1). M4 wie M3, aber nur wenn dessen 12-Monats-Rendite positiv ist, sonst sammeln bis eine positiv wird (Dual Momentum). M5 alles in den Schwaechsten der letzten 12 Monate (antizyklisch).
Test A: Bitcoin, S&P, Gold (2015-2026). Test B: nur S&P und Gold (ohne Bitcoin). Test C: breite ETFs VT, EEM, IEF, XLK (2008-2026, Kurse inkl. Ausschuettungen).
Kriterium: eine Regel schlaegt M0 nur, wenn ihr Median-Endwert in Test B UND Test C mindestens 3 % ueber M0 (bzw. ueber VT in Test C) liegt und sie in beiden Haelften der Startzeitpunkte vorne ist. Test A allein zaehlt nicht (Bitcoin-Rueckblick).
Ergebnis: keine Regel erfuellt das Kriterium, keine Aenderung. Test B (S&P/Gold): alle Regeln 1,42-1,43 vs S&P 1,49. Test C: Staerke 12-1 (M3/M4) 1,48 vs Welt-ETF 1,29 - kauft aber fast nur XLK (Tech-Rueckblick 2008-2026), antizyklisch (M5) 1,14. Test A (mit Bitcoin): alles, was Bitcoin beimischt, schlaegt den S&P (1,96-2,17), antizyklisch am besten (2,17) - nur Rueckblick, zaehlt nicht.

## 2026-11-18: Kaufsignal in Euro (eurtest.py)
Euro-Anleger 2004-2026, 10-Jahres-Fenster, Werte in Euro: sofort 2,121 | Signal in Dollar 2,125 | Signal in Euro 2,125 (in 100 % der Fenster mindestens so gut wie sofort). Signale unterscheiden sich an 21 % der Tage. -> Signal und Schattenbuch Sparplan rechnen ab jetzt mit dem S&P in Euro (sparplan.py, USE_EUR).

## 2026-11-18: Euro-Sicht fuer die Mannschaft (nur Befund, keine Aenderung)
Mannschaft 2017-2026 in Euro gerechnet: 15,4 %/J, Rueckgang 16 %, Sharpe 1,07 (in Dollar 17,6 %, 17 %, 1,26). Halten in Euro 22,9 %/J, Rueckgang 25 %. Der Abstand zum Halten ist in Euro groesser, weil der Cash-Anteil die Dollar-Gewinne nicht mitnimmt. Trendsignale Dollar vs Euro verschieden: Bitcoin 2 %, S&P 12 %, Gold 22 % der Tage. Ob die Mannschaft in Euro rechnen soll: Entscheidung zum Saisonende. Seite zeigt Abstand zum Allzeithoch fuer alle drei in Euro.

## 2026-11-18: Langzeittest Gold (vorab festgelegt, goldtest.py)
Daten: Goldpreis monatlich (datasets/gold-prices, USD) ab 1971-08 (Ende fester Goldpreis). Monatliche Signale, Kosten 5 bps, Cash ohne Zins. Halten vs Trend 10 Monate (entspricht etwa 200 Tagen).
Kriterium: Der Trendfilter gilt fuer Gold als belegt, wenn er den groessten Rueckgang gesamt UND in der Baisse-Epoche 1981-2000 senkt und die Rendite gesamt hoechstens 2 Punkte pro Jahr unter Halten liegt. Dann spielt Gold im Pruefstand fest Trend SMA200 (wie der S&P). Sonst spielt Gold fest Halten.
Ergebnis Gold (1971-2026, monatlich): Trend 10,1 %/J, Rueckgang 32 % vs Halten 8,6 %/J, 62 %; 1981-2000 Rueckgang 31 vs 54 %. Kriterium ERFUELLT -> Gold spielt im Pruefstand fest Trend SMA200.
Hinweis: im kurzen Fenster 2017-2026 (Euro) war die Mannschaft mit Gold-Trend schwaecher (12,9 %/J, Rueckgang 21 %, Sharpe 0,94) als mit Gold-Wahl (15,4 %, 16 %, 1,07). Die Langzeitdaten zaehlen (vorab festgelegt).

## 2026-11-18: Pruefstand rechnet in Euro (ausdrueckliche Entscheidung)
heartbeat.py rechnet alle Kurse in Euro (to_eur). Befund 2017-2026 in Euro: Mannschaft 12,9 %/J, Rueckgang 21 %, Sharpe 0,94; alle drei gleich halten 22,9 %/J, Rueckgang 25 %, Sharpe 1,19. Die Mannschaft liegt in Euro auch risikobereinigt hinter dem Halten - zum Saisonende ehrlich bewerten.

## 2026-11-18: Gegencheck Total Return, Zinsen, Inflation, Start 1929 (vorab festgelegt, totalreturn.py)
Anlass: Kritik einer zweiten KI (Gemini): Preisindex ohne Dividenden, Cash ohne Zins, nominal, Start erst 1930. Daten: Shiller (datasets/s-and-p-500), monatlich 1871-06/2023 (Dividende, Inflation, Zins 10 J.). Total Return = (Kurs + Dividende/12) / Vormonatskurs - 1. Cash-Zins unbekannt (nur 10-Jahres-Zins vorhanden): Test mit 0 % und mit 50 % des 10-Jahres-Zinses als grobe Naeherung fuer Tagesgeld/Kurzlaeufer. Real = durch US-Inflation (CPI). Kosten 5 bps. Keine Steuern.
Frage A (Kaufregel): Monatlich 1 Einheit, 20-Jahres-Fenster, Start alle 6 Monate ab 1929-01 (inkl. 1929), Total Return, Cash mit Zins. "Nicht am Hoch" (kaufen ab 3 % unter Allzeithoch, Monatskurse) haelt, wenn Median-Endwert mindestens 99 % von "sofort kaufen" UND die schlechtesten 10 % nicht mehr als 1 % darunter liegen. Zusaetzlich einzeln: Start im Hoch September 1929 und Start Maerz 2000 (20 und 10 Jahre) - nur Information.
Frage B (Trend): Trend 10 Monate (~200 Tage) auf Total Return mit Cash-Zins gegen Halten, Epochen wie longtest.py. Trend bleibt belegt, wenn er in 1973-1982 und 2000-2009 den Rueckgang gegenueber Halten senkt UND ueber alles die Rendite hoechstens 1,0 Punkt/J unter Halten liegt (nominal, Cash mit 50 % des 10-J-Zinses). Sonst wird der Trend als Absturzbremse neu bewertet (Saisonende).

### Ergebnis Gegencheck Total Return (2026-11-18, totalreturn.py, Shiller 1929-2023)
Frage A: Kriterium NICHT erfuellt (7 von 8 Varianten). Mit Dividenden und Zinsen kostet "nicht am Hoch" mehr als im Preisindex-Test: 20 J nominal Median 3,39 vs sofort 3,46 (ca. 2 % weniger), 10 J 1,74 vs 1,79 (ca. 3 %); besser als sofort nur in 1-12 % der Fenster (vorher 41 %). Einzelstarts Sept 1929, Maerz 2000, Jan 1973: praktisch identisch zu sofort. Schlechteste 10 % nur ca. 1-4 % schlechter. Der fruehere Befund "kostet praktisch nichts" gilt nur ohne Dividenden und war zu optimistisch; die Kritik war berechtigt.
Frage B: Trend 10 Monate bleibt belegt: 1930-2023 Total Return 10,9 %/J, Rueckgang 22 % vs Halten 9,8 %/J, 78 %; 1973-1982 11 vs 39 %, 2000-2009 6 vs 49 %. Schwaeche bleibt 1983-1999 und 2010-2023 (2-3 Punkte/J hinter Halten).
Die Regel "nicht am Hoch" ist eine ausdrueckliche Entscheidung des Nutzers (Grundsatz); Kosten jetzt bekannt: ca. 2-3 % des Endvermoegens im Median. Aenderung nur auf seine Entscheidung.

## 2026-11-18: Kaufregel neues Geld = sofort kaufen (Entscheidung des Nutzers, ersetzt "nicht am Hoch")
Grund: Gegencheck Total Return (totalreturn.py): "nicht am Hoch" kostet 2-3 % Endvermoegen, besser als sofort nur in 1-12 % der Fenster. Der Nutzer: Zahlen gehen vor Prinzip. Seite zeigt immer "Kaufen". "Nicht am Hoch" laeuft als Vergleich im Schattenbuch Sparplan weiter (sparplan.py: regel_signal). Pruefung: nach einem Jahr. Rueckgaengig: signal in sparplan.py wieder an buy koppeln.

## 2026-11-18: Elite 9 und Faktor-ETFs (Wunsch des Nutzers, nur Anzeige und Schattenbuch, kein Geld)
Ausnahme von "keine Einzelaktien": nur Beobachtung, keine Empfehlung, kein Einfluss auf die Kaufregel.
Elite 9 (Liste des Nutzers vom 2026-11-18, Auswahl im RUECKBLICK, Quelle der Zahlen unklar): CME Group, Ferrari, Waste Management, Mastercard, Visa, Cintas, Hermes (Paris, EUR), Microsoft, Alphabet. 9 Regeln der Liste: Beta < 1,15; Bruttomarge > 50 %; Monopol/Duopol; keine Zyklizitaet; Preissetzungsmacht; kein existenzielles Disruptionsrisiko; 10-Jahres-Rendite (Total Return) ~17 % p. a.; Verschuldung/Eigenkapital < 1,0; Burggraben waechst.
Automatisch berechnet (aus Kursen): Beta (taeglich, 5 Jahre, gegen S&P 500) und 10-Jahres-Rendite p. a. Alles andere (Marge, Monopol, Zyklik, Disruption, Burggraben, Verschuldung) wird NICHT geprueft, nur uebernommen. Die berechneten Werte werden mit den Listenwerten verglichen; Abweichung > 3 Punkte wird angezeigt.
Ein Rueckwaerts-Test der Liste ist wertlos (Survivorship: Regel 7 waehlt Gewinner der Vergangenheit). Er wird nur zur Illustration gezeigt und so gekennzeichnet. DER Test ist das Schattenbuch Elite ab 2026-11-18: 9 Aktien gleich gewichtet, in Euro, gegen S&P 500 in Euro.
Kriterium (nach 3 Jahren, ab 2029-11): bewaehrt, wenn Rendite mindestens 2 Punkte pro Jahr ueber dem S&P UND der Rueckgang nicht groesser; gescheitert, wenn die Rendite unter dem S&P liegt; sonst weiter beobachten. Nach 1 Jahr nur Zwischenstand, keine Bewertung.
Faktor-ETFs: QUAL (Qualitaet), MTUM (Momentum), USMV (Min. Volatilitaet), XLK (Tech), dazu VT und URTH (Welt) gegen SPY, in Euro, ab 2015-07. Anzeige: Rendite pro Jahr, Rueckgang, Sharpe, Beta. Aufnahmetest vom 2026-11-18: alle durchgefallen (siehe oben). Keine neue Regel.
