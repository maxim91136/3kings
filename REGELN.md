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
