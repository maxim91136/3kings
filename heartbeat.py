"""3Kings Heartbeat: berechnet aus data/prices.csv die Mannschafts-Empfehlung (KEINE Auto-Trades).

Ablauf je Lauf:
  1. Mannschaft (core/team.py) auf allen bisherigen Kursen rechnen -> Champion je Spieler, Zielanteile.
  2. Mit dem zuletzt GEHALTENEN Soll vergleichen. Nur wenn ein Anteil um >= BAND (5 Punkte) abweicht,
     lautet die Empfehlung 'umschichten' - sonst 'nichts tun' (gegen Zappelei).
  3. Schattenbuch fortschreiben: Was waere passiert, wenn man jede Empfehlung befolgt haette?
     Daneben der Vergleich 'gleich gewichtet halten'. data/ledger.csv + data/state.json.
  4. site/heartbeat.json schreiben (die Seite liest sie).
Regeländerungen passieren nur am Saisonende (core/team.py), nie mitten in der Saison.
"""
import csv, json, os, sys
from datetime import datetime, timezone

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "core"))
import lab, team

PLAYERS = ["BTC", "SPY", "GLD"]
TILT = {"BTC": 2.0}   # Regel seit 2026-11-18: Bitcoin bekommt doppeltes Gewicht in der Kapitalverteilung (Spot, kein Hebel)
EXTRA = {"BTC": ["Trend SMA100 (Std.)"]}      # Regelaenderung 18.11.2026: schnelle Trend-Linie nur fuer Bitcoin (siehe REGELN.md)
LABEL = {"BTC": "Bitcoin", "SPY": "S&P 500", "GLD": "Gold"}
BAND = 0.05                                   # vorab festgelegt, nicht optimiert
DATA, SITE = "data", "site"


def current_plan(P, names):
    res = team.run_team(P, names, PLAYERS, strats={p: team.STRATS + EXTRA.get(p, []) for p in PLAYERS}, tilt=TILT)
    T, ix = len(P), {n: i for i, n in enumerate(names)}
    t0 = res["bounds"][-1]
    alloc = res["alloc"][T - 1]
    plan = {}
    for k, p in enumerate(PLAYERS):
        cost = team.COST.get(p, 0.0005)
        champ = res["history"][p][-1]
        w = float(lab.build_strategies(names, cost)[champ](P, ix[p])[T - 1])
        digits = "".join(ch for ch in champ.split(" (")[0] if ch.isdigit())
        line_n = int(digits) if champ.startswith("Trend") and digits else 200
        sma = P[T - line_n:, ix[p]].mean()
        plan[p] = dict(champion=champ.split(" (")[0], strat_weight=round(w, 4), alloc=round(float(alloc[k]), 4),
                       target=round(float(alloc[k]) * w, 4), price=float(P[T - 1, ix[p]]),
                       line_n=line_n, vs_line=round(float(P[T - 1, ix[p]] / sma - 1), 4),
                       dd_high=round(float(P[T - 1, ix[p]] / P[max(0, T - 252):T, ix[p]].max() - 1), 4))
    left = t0 + team.SEASON - (T - 1)
    return plan, dict(day_in_season=int(T - 1 - t0), days_left=int(left), n_seasons=len(res["bounds"]))


def load_state():
    p = os.path.join(DATA, "state.json")
    return json.load(open(p)) if os.path.exists(p) else None


def ledger_tail(n=400):
    p = os.path.join(DATA, "ledger.csv")
    if not os.path.exists(p):
        return []
    return list(csv.DictReader(open(p)))[-n:]


def advance(state, dates, P, names):
    """Schattenbuch bis zum letzten Kurstag fortschreiben (altes gehaltenes Soll wirkt auf die Folgetage)."""
    ix = {n: i for i, n in enumerate(names)}
    R = lab.returns(P)
    i0 = dates.index(state["last_date"])
    for i in range(i0 + 1, len(dates)):
        state["shadow"] *= 1 + sum(state["held"][p] * R[i, ix[p]] for p in PLAYERS)
        state["hold"] *= 1 + sum(R[i, ix[p]] for p in PLAYERS) / len(PLAYERS)
    state["last_date"] = dates[-1]


def main():
    dates, names, P = lab.load_prices(os.path.join(DATA, "prices.csv"))
    need = lab.WARM + team.SEASON + 2
    if len(P) < need:
        raise SystemExit(f"Zu wenig gemeinsame Kurstage: {len(P)} ({dates[0]} .. {dates[-1]}), benoetigt {need}. Siehe Log von fetch_prices.py.")
    plan, season = current_plan(P, names)
    last = dates[-1]
    state = load_state()
    first = state is None
    if first:
        state = dict(start=last, last_date=last, shadow=1.0, hold=1.0, held={p: 0.0 for p in PLAYERS}, n_actions=0)
    elif last > state["last_date"]:
        advance(state, dates, P, names)

    target = {p: plan[p]["target"] for p in PLAYERS}
    moves = []
    for p in PLAYERS:
        d = target[p] - state["held"][p]
        if abs(d) >= BAND:
            moves.append(dict(player=p, name=LABEL[p], von=round(state["held"][p], 4), auf=target[p], delta=round(d, 4)))
    new_day = first or (last > state.get("last_logged", ""))
    if moves:                                                  # Empfehlung befolgt: gehaltenes Soll = neues Ziel
        cost = sum(abs(m["delta"]) * team.COST.get(m["player"], 0.0005) for m in moves)
        state["shadow"] *= 1 - cost
        if new_day:
            state["n_actions"] += 1
        for m in moves:
            state["held"][m["player"]] = target[m["player"]]
    cash = round(1 - sum(state["held"].values()), 4)

    if new_day:
        os.makedirs(DATA, exist_ok=True)
        path = os.path.join(DATA, "ledger.csv")
        new = not os.path.exists(path)
        with open(path, "a", newline="") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["date", "BTC", "SPY", "GLD", "cash", "shadow", "hold", "action"])
            w.writerow([last] + [state["held"][p] for p in PLAYERS] + [cash, round(state["shadow"], 5),
                                                                       round(state["hold"], 5),
                                                                       "; ".join(f"{m['name']} {m['von']:.2f}->{m['auf']:.2f}" for m in moves) or "-"])
        state["last_logged"] = last
    json.dump(state, open(os.path.join(DATA, "state.json"), "w"), indent=1)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out = dict(generated_at=now, data_date=last, players=plan, season=season, held=state["held"], cash=cash,
               moves=moves, shadow=round(state["shadow"], 4), hold=round(state["hold"], 4), since=state["start"],
               n_actions=state["n_actions"], band=BAND, ledger_tail=ledger_tail())
    os.makedirs(SITE, exist_ok=True)
    json.dump(out, open(os.path.join(SITE, "heartbeat.json"), "w"), indent=1)

    print(f"Kurstag {last} | Saisontag {season['day_in_season']}/{team.SEASON}, Wahl in {season['days_left']} Tagen")
    for p in PLAYERS:
        x = plan[p]
        print(f"  {LABEL[p]:8s} Champion {x['champion']:18s} Ziel {x['target']*100:5.1f}% (gehalten {state['held'][p]*100:5.1f}%)")
    print("  Cash", f"{cash*100:.1f}%", "|", "AKTION: " + ", ".join(f"{m['name']} {m['von']*100:.0f}->{m['auf']*100:.0f}%" for m in moves) if moves else "| nichts tun")
    print(f"  Schattenbuch {state['shadow']:.4f} vs Halten {state['hold']:.4f} (seit {state['start']})")


if __name__ == "__main__":
    main()
