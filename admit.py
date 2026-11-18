"""Aufnahmetest fuer neue Spieler (vorab festgelegte Regeln). Aendert den Heartbeat NICHT.
  python3 admit.py [--cands data/candidates.csv]
Je Kandidat wird die Mannschaft mit und ohne ihn auf DEMSELBEN Zeitraum gerechnet (Kandidat-Start bis heute).
Regeln (vorab festgelegt):
  1. Mindestens 10 Jahre Kurse.
  2. Kein Doppelgaenger: Korrelation der Tagesrenditen mit der heutigen Mannschaft < 0,8.
  3. Mannschaftsbeitrag in BEIDEN Zeithaelften: Sharpe nicht schlechter (Toleranz 0,02) UND Rueckgang nicht tiefer
     (Toleranz 1 Punkt); ueber alles muss eine der beiden Kennzahlen deutlich besser sein (Sharpe +0,03 oder Rueckgang -1,5 Punkte).
Wer besteht, kommt auf die ERSATZBANK (zwei Saisons nur im Schattenbuch, noch ohne Kapital). Alle Ergebnisse werden gezeigt."""
import argparse, csv, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "core"))
import lab, team

ap = argparse.ArgumentParser(); ap.add_argument("--cands", default="data/candidates.csv"); ap.add_argument("--data", default="data/prices.csv")
a = ap.parse_args()
dates, names, P = lab.load_prices(a.data)
rows = list(csv.DictReader(open(a.cands)))
cmap = {c: {r["date"]: float(r[c]) for r in rows if r[c] not in ("", None)} for c in rows[0] if c != "date"}
BASE = ["BTC", "SPY", "GLD"]
S = team.STRATS
STR = {"BTC": S + ["Trend SMA100 (Std.)"]}
GROUP = {"Gruppe 1": ["URTH", "VT", "QUAL", "MTUM", "USMV", "XLK"]}
sh = lambda x: x.mean() / x.std(ddof=1) * np.sqrt(252)


def stats(net, expo):
    m = lab.metrics(net, expo)
    return m["sharpe"], m["mdd"], m["cagr"]


print(f"Basis: {dates[0]} .. {dates[-1]}; Kandidaten: {', '.join(cmap)}\n")
print(f"{'Kandidat':9s}{'Jahre':>6s}{'Korr.':>7s}  {'Sharpe ohne->mit':>17s}{'Rueckg. ohne->mit':>19s}   Haelften (Sharpe, Rueckg. Delta)      Ergebnis")
for c, mp in cmap.items():
    idx = [i for i, d in enumerate(dates) if d in mp]
    if not idx:
        print(f"{c:9s} keine Kurse im Zeitraum"); continue
    first = idx[0]
    ser = np.array([mp.get(d, np.nan) for d in dates[first:]])
    ok = np.isfinite(ser)
    if (~ok).mean() > 0.02:
        print(f"{c:9s} zu viele Luecken ({(~ok).mean()*100:.0f} %)"); continue
    for j in range(len(ser)):                      # kleine Luecken auffuellen
        if not np.isfinite(ser[j]): ser[j] = ser[j - 1]
    years = len(ser) / 252
    P2 = np.column_stack([P[first:], ser]); nm2 = names + [c]
    if years < 10:
        print(f"{c:9s}{years:6.1f}  durchgefallen: weniger als 10 Jahre Kurse"); continue
    b = team.run_team(P2, nm2, BASE, strats=STR)["team"]
    w = team.run_team(P2, nm2, BASE + [c], strats=STR)["team"]
    R = lab.returns(P2)[lab.WARM:, nm2.index(c)]
    corr = float(np.corrcoef(b[0], R)[0, 1])
    s0, d0, _ = stats(*b); s1, d1, _ = stats(*w)
    n = len(b[0]); h = n // 2
    halves, okh = [], True
    for sl in (slice(0, h), slice(h, n)):
        x0, y0, _ = stats(b[0][sl], b[1][sl]); x1, y1, _ = stats(w[0][sl], w[1][sl])
        halves.append(f"{x1 - x0:+.2f}/{(y1 - y0) * 100:+.0f}")
        okh &= (x1 >= x0 - 0.02) and (y1 <= y0 + 0.01)
    better = (s1 >= s0 + 0.03) or (d1 <= d0 - 0.015)
    res = "AUF DIE ERSATZBANK" if (corr < 0.8 and okh and better) else "durchgefallen: " + ", ".join(
        r for r, f in (("Doppelgaenger", corr >= 0.8), ("Haelften", not okh), ("kein klarer Gewinn", not better)) if f)
    print(f"{c:9s}{years:6.1f}{corr:7.2f}  {s0:7.2f} -> {s1:5.2f}  {d0*100:8.0f}% -> {d1*100:3.0f}%   {halves[0]:>9s}  {halves[1]:>9s}      {res}")
