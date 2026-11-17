"""Mannschaft Stufe 1 (bewusst einfach): drei Spieler (Bitcoin, S&P 500, Gold).

Regeln (vorab festgelegt, nicht optimiert):
  * Jeder Spieler hat drei Strategien zur Auswahl: Halten, Trend SMA200, Vol-Target 15 %.
  * SAISON = 63 Handelstage (~ ein Quartal). Am Saisonende wird der Champion je Spieler bestimmt:
    Wer in den letzten 504 Tagen den besten Sharpe hatte, spielt die naechste Saison. Ein
    Herausforderer muss den Amtsinhaber um 0,2 Sharpe schlagen (gegen staendiges Wechseln).
    Start-Champion: Halten.
  * Kapital: Inverse Volatilitaet (letzte 63 Tage) - ruhigere Spieler bekommen mehr.
  * Vergleich: gleiche Gewichtung, aber ALLE Spieler halten nur (= Stufe 0).
Alles kausal: Entscheidungen am Saisonende nutzen nur Daten bis dahin.
"""
import numpy as np
import lab

SEASON, LOOK, MARGIN = 63, 504, 0.2
STRATS = ["Halten (Baseline)", "Trend SMA200 (Std.)", "Vol-Target 15% (Std.)"]
COST = {"BTC": 0.0010}


def run_team(P, names, players, cost_mult=1.0):
    R = lab.returns(P)
    T = len(P)
    ix = {n: i for i, n in enumerate(names)}
    cost = {p: COST.get(p, 0.0005) * cost_mult for p in players}
    W, NET = {}, {}
    for p in players:                                                 # alle Strategien je Spieler
        fns = lab.build_strategies(names, cost[p])
        for s in STRATS:
            w = fns[s](P, ix[p])
            W[p, s] = w
            NET[p, s] = lab.backtest(w, R[:, ix[p]], cost[p])
    sh = lambda x: x.mean() / max(x.std(ddof=1), 1e-12) * np.sqrt(lab.ANN)

    bounds = list(range(lab.WARM, T - 1, SEASON))                     # Saisonanfaenge
    champ = {p: STRATS[0] for p in players}
    w_real = {p: np.zeros(T) for p in players}
    w_hold = {p: W[p, STRATS[0]].copy() for p in players}
    alloc = np.zeros((T, len(players)))
    history = {p: [] for p in players}
    for t in bounds:
        end = min(t + SEASON, T - 1)
        for p in players:                                             # Champion-Wahl (nur Daten bis t)
            sc = {s: sh(NET[p, s][t - LOOK + 1: t + 1]) for s in STRATS}
            best = max(sc, key=sc.get)
            if sc[best] > sc[champ[p]] + MARGIN:
                champ[p] = best
            history[p].append(champ[p])
            w_real[p][t: end + 1] = W[p, champ[p]][t: end + 1]
        vol = np.array([R[t - 62: t + 1, ix[p]].std(ddof=1) for p in players])
        a = (1 / vol) / (1 / vol).sum()
        alloc[t: end + 1] = a
    out = {}
    for tag, wd in (("team", w_real), ("halten", w_hold)):
        net = np.zeros(T)
        expo = np.zeros(T)
        prev = np.zeros(len(players))
        for k, p in enumerate(players):
            net += alloc[:, k] * lab.backtest(wd[p], R[:, ix[p]], cost[p])
            expo += alloc[:, k] * wd[p]
        for t in bounds:                                              # Umschichtungskosten des Teams
            net[t + 1 if t + 1 < T else t] -= 0.0005 * np.abs(alloc[t] - prev).sum()
            prev = alloc[t]
        out[tag] = (net[lab.WARM:], expo[lab.WARM:])
    out["history"], out["bounds"], out["alloc"] = history, bounds, alloc
    return out


def seasons_table(res):
    a, b = res["team"][0], res["halten"][0]
    rows = []
    for k in range(0, len(a), SEASON):
        x, y = a[k: k + SEASON], b[k: k + SEASON]
        if len(x) == SEASON:
            rows.append((np.prod(1 + x) - 1, np.prod(1 + y) - 1))
    return np.array(rows)
