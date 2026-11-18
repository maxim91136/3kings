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
