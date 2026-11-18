"""Backtest-Labor fuer grosse Maerkte (Bitcoin, Aktien-ETF, Gold, Silber).  Nur numpy.

Eiserne Regeln des Labors (damit keine Scheinerfolge entstehen):
  1. KAUSAL: Das Gewicht am Tagesende t nutzt nur Daten bis t und wirkt auf die Rendite t -> t+1.
     Ein Selbsttest (--selftest) prueft jede Strategie auf Blick in die Zukunft.
  2. KOSTEN: Jede Umschichtung kostet (BTC 10 bps, ETFs 5 bps je Umsatz).
  3. EIN GEMEINSAMES Auswertungsfenster fuer alle Strategien (die ersten 2 Jahre sind Anlaufzeit).
  4. KEINE freien Parameter-Optimierungen: feste, vorab festgelegte Parameter (weniger Overfitting).
  5. SIGNIFIKANZ: Block-Bootstrap auf Sharpe-Differenz gegen 'Halten'; Bonferroni-Schwelle
     fuer die Zahl getesteter Strategien. Ohne Signifikanz gilt: kein Beleg fuer einen Vorteil.

Neue Ideen (siehe build_strategies):
  EGE   Evidence-Gated Ensemble: Kapital folgt nur Teilstrategien, deren BISHERIGER Nachweis
        (Bayes) mit >= 80 % Wahrscheinlichkeit ueber Null liegt. Sonst: Cash.
  STRESS Cross-Asset-Stressthermometer: Korrelations-/Vol-/Gold-Silber-/Drawdown-Signale
        ueber mehrere Maerkte -> Exposure runter, wenn das Gesamtsystem unruhig wird.
  RAUPE  Nur in ruhigen Aufwaertsphasen investiert (viele kleine Gewinne) - und das Labor
        misst ausdruecklich die Schwanzverluste.
"""
import bisect, csv, math, warnings
from math import erf, sqrt

import numpy as np

ANN = 252
Phi = lambda z: 0.5 * (1 + erf(z / sqrt(2)))
WARM = 504                       # Tage Anlaufzeit (gemeinsam fuer alle Strategien)


# ------------------------------------------------------------------ Daten
def load_prices(path):
    with open(path) as f:
        rd = csv.reader(f)
        head = next(rd)
        rows = list(rd)
    return [r[0] for r in rows], head[1:], np.array([[float(x) for x in r[1:]] for r in rows])


def returns(P):
    R = np.zeros_like(P)
    R[1:] = P[1:] / P[:-1] - 1
    return R


# ------------------------------------------------------------------ kausale Bausteine
def sma(x, n):
    c = np.cumsum(np.insert(x, 0, 0.0))
    out = np.full(len(x), np.nan)
    out[n - 1:] = (c[n:] - c[:-n]) / n
    return out


def rolling_std(x, n):
    c1, c2 = np.cumsum(np.insert(x, 0, 0.0)), np.cumsum(np.insert(x * x, 0, 0.0))
    out = np.full(len(x), np.nan)
    m = (c1[n:] - c1[:-n]) / n
    v = (c2[n:] - c2[:-n]) / n - m * m
    out[n - 1:] = np.sqrt(np.maximum(v, 0) * n / (n - 1))
    return out


def rolling_corr(x, y, n):
    cs = lambda v: np.cumsum(np.insert(v, 0, 0.0))
    d = lambda c: c[n:] - c[:-n]
    mx, my = d(cs(x)) / n, d(cs(y)) / n
    cov = d(cs(x * y)) / n - mx * my
    vx, vy = d(cs(x * x)) / n - mx * mx, d(cs(y * y)) / n - my * my
    out = np.full(len(x), np.nan)
    out[n - 1:] = cov / np.sqrt(np.maximum(vx * vy, 1e-18))
    return out


def expanding_z(x, min_n=250):
    """z-Wert gegen die bisherige Historie (ohne den heutigen Wert in den Statistiken)."""
    out = np.full(len(x), np.nan)
    s = s2 = 0.0
    n = 0
    for i, v in enumerate(x):
        if np.isfinite(v):
            if n >= min_n:
                m = s / n
                out[i] = (v - m) / math.sqrt(max(s2 / n - m * m, 1e-18))
            s += v
            s2 += v * v
            n += 1
    return out


def expanding_below_quantile(x, q=0.7, min_n=250):
    hist, out = [], np.zeros(len(x), bool)
    for i, v in enumerate(x):
        if np.isfinite(v):
            if len(hist) >= min_n:
                out[i] = v <= hist[int(q * len(hist))]
            bisect.insort(hist, v)
    return out


def stress_score(P, names):
    """Cross-Asset-Stress: Mittel mehrerer z-Werte. Hoch = System unruhig."""
    R, T = returns(P), len(P)
    ix = {n: i for i, n in enumerate(names)}
    z = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if "BTC" in ix and "SPY" in ix:                                   # Korrelation steigt in Krisen
            z.append(expanding_z(rolling_corr(R[:, ix["BTC"]], R[:, ix["SPY"]], 60)))
        for n in ("SPY", "BTC"):                                          # Volatilitaet
            if n in ix:
                z.append(expanding_z(np.log(np.maximum(rolling_std(R[:, ix[n]], 20), 1e-9))))
        if "GLD" in ix and "SLV" in ix:                                   # Gold/Silber-Verhaeltnis steigt bei Angst
            lr = np.log(P[:, ix["GLD"]] / P[:, ix["SLV"]])
            ch = np.full(T, np.nan)
            ch[60:] = lr[60:] - lr[:-60]
            z.append(expanding_z(ch))
        if "SPY" in ix:                                                   # Tiefe des Drawdowns
            s = P[:, ix["SPY"]]
            rm = np.array([s[max(0, i - 251): i + 1].max() for i in range(T)])
            z.append(expanding_z(-(s / rm - 1)))
        return np.nanmean(np.clip(np.array(z), -3, 3), axis=0)


# ------------------------------------------------------------------ Backtest
def backtest(w, r, cost):
    dw = np.abs(np.diff(w, prepend=0.0))
    net = np.zeros(len(w))
    net[1:] = w[:-1] * r[1:] - cost * dw[:-1]
    return net


def metrics(net, w):
    eq = np.cumprod(1 + net)
    T = len(net)
    peak = np.maximum.accumulate(eq)
    mdd = float(((peak - eq) / peak).max())
    cagr = float(eq[-1] ** (ANN / T) - 1)
    sd = net.std(ddof=1)
    sharpe = float(net.mean() / sd * sqrt(ANN)) if sd > 0 else 0.0
    inm = w[:-1] > 0
    k = max(int(len(net) * 0.01), 1)
    return dict(cagr=cagr, vol=float(sd * sqrt(ANN)), sharpe=sharpe, mdd=mdd,
                calmar=cagr / mdd if mdd > 0 else 0.0,
                pos=float((net[1:][inm] > 0).mean()) if inm.any() else 0.0,
                worst=float(net.min()), tail=float(np.sort(net)[:k].mean()),
                invested=float(inm.mean()), final=float(eq[-1]))


def sharpe_diff_bootstrap(a, b, n_boot=2000, block=20, seed=0):
    """Sharpe(a) - Sharpe(b) mit Block-Bootstrap -> (Differenz, p fuer 'a nicht besser', 90%-Intervall)."""
    rng = np.random.default_rng(seed)
    T = len(a)
    nb = -(-T // block)
    idx = ((rng.integers(0, T, (n_boot, nb, 1)) + np.arange(block)) % T).reshape(n_boot, -1)[:, :T]
    sh = lambda x: x.mean(axis=1) / np.maximum(x.std(axis=1, ddof=1), 1e-12) * sqrt(ANN)
    d = sh(a[idx]) - sh(b[idx])
    obs = (a.mean() / a.std(ddof=1) - b.mean() / b.std(ddof=1)) * sqrt(ANN)
    return float(obs), float((d <= 0).mean()), (float(np.percentile(d, 5)), float(np.percentile(d, 95)))


def vault_path(net, tiers=((0.25, 0.30), (1.0, 0.50), (float("inf"), 0.70)), kill=0.6):
    """Gewinn-Tresor wie im Bot: gestaffelt sichern, Kill-Switch bei < 60 % Handelskapital."""
    eq = hwm = 1.0
    vault, killed = 0.0, False
    tot = np.zeros(len(net))
    for t, x in enumerate(net):
        if not killed:
            eq *= 1 + x
            if eq > hwm:
                frac = next(f for lim, f in tiers if (eq + vault) - 1 < lim)
                amt = frac * (eq - hwm)
                eq -= amt
                vault += amt
                hwm = eq
            if eq < kill:
                killed = True
        tot[t] = eq + vault
    return tot, vault, killed


# ------------------------------------------------------------------ Strategien (alle kausal)
def build_strategies(names, cost):
    def hold(P, a):
        return np.ones(len(P))

    def trend(n):
        def f(P, a):
            m = sma(P[:, a], n)
            return np.where(np.isfinite(m) & (P[:, a] > m), 1.0, 0.0)
        return f

    def momentum(P, a, n=252):
        w = np.zeros(len(P))
        w[n:] = (P[n:, a] > P[:-n, a]).astype(float)
        return w

    def voltarget(P, a, target=0.15):
        sd = rolling_std(returns(P)[:, a], 20) * sqrt(ANN)
        return np.where(np.isfinite(sd), np.clip(target / np.maximum(sd, 1e-9), 0, 1), 0.0)

    def dipbuild(P, a, base=0.7, step=0.1, tiers=(-0.10, -0.20, -0.30)):
        """Dip-Aufbau: Basis 70 % investiert; je Stufe (-10/-20/-30 % unter dem 252-Tage-Hoch)
        +10 % dazu. Ist der Kurs wieder >= 95 % des Hochs, faellt es auf die Basis zurueck."""
        p, T = P[:, a], len(P)
        w, k = np.zeros(T), 0
        for t in range(T):
            hi = p[max(0, t - 251): t + 1].max()
            if p[t] >= 0.95 * hi:
                k = 0
            else:
                k = max(k, sum(p[t] / hi - 1 <= th for th in tiers))
            w[t] = min(1.0, base + step * k)
        return w

    def raupe(P, a):
        m = sma(P[:, a], 100)
        calm = expanding_below_quantile(rolling_std(returns(P)[:, a], 20), 0.7)
        return np.where(np.isfinite(m) & (P[:, a] > m) & calm, 1.0, 0.0)

    def stress(P, a):
        S = stress_score(P, names)
        return np.where(np.isfinite(S), np.clip(1 - np.maximum(S, 0) / 2, 0, 1), 1.0)

    arms = [trend(50), trend(100), trend(200), momentum, voltarget, raupe, stress]

    def ege(P, a, window=756, thresh=0.8, tau=0.5):
        """Evidence-Gated Ensemble: jede Teilstrategie ('Arm') wird laufend ehrlich bewertet;
        nur Arme mit P(echter Vorteil > 0) >= thresh bekommen Kapital. Sonst Cash."""
        T, r = len(P), returns(P)[:, a]
        W = np.array([arm(P, a) for arm in arms])
        net = np.array([backtest(w, r, cost) for w in W])
        c1 = np.cumsum(np.insert(net, 0, 0.0, axis=1), axis=1)
        c2 = np.cumsum(np.insert(net * net, 0, 0.0, axis=1), axis=1)
        out = np.zeros(T)
        for t in range(WARM, T):
            n = min(window, t)
            lo = t + 1 - n
            m = (c1[:, t + 1] - c1[:, lo]) / n
            v = (c2[:, t + 1] - c2[:, lo]) / n - m * m
            sd = np.sqrt(np.maximum(v, 0) * n / (n - 1))
            ok = sd > 1e-9
            sr = np.where(ok, m / np.maximum(sd, 1e-9) * sqrt(ANN), 0.0)
            se2 = 1.0 / (n / ANN)                                      # Varianz des Sharpe-Schaetzers
            pm = sr * tau ** 2 / (tau ** 2 + se2)                      # Bayes-Schrumpfung Richtung 0
            ps = sqrt(tau ** 2 * se2 / (tau ** 2 + se2))
            p = np.array([Phi(x / ps) for x in pm])
            act = ok & (p >= thresh)
            if act.any():
                wt = p[act] - 0.5
                out[t] = float((W[act, t] * wt).sum() / wt.sum())
        return out

    return {"Halten (Baseline)": hold, "Trend SMA200 (Std.)": trend(200), "Trend SMA100 (Std.)": trend(100), "Vol-Target 15% (Std.)": voltarget,
            "Momentum 12M (Std.)": momentum, "Dip-Aufbau (Std.)": dipbuild, "RAUPE (ruhiger Aufwaertstrend)": raupe,
            "STRESS-Thermometer (cross-asset)": stress, "EGE (evidenz-gesteuert)": ege}


def causality_test(strategies, P, n_cuts=3, seed=1):
    """Gewichte aus abgeschnittener Historie muessen den Gewichten der vollen Historie entsprechen."""
    rng = np.random.default_rng(seed)
    bad = []
    for name, fn in strategies.items():
        full = fn(P, 0)
        for t0 in rng.integers(WARM + 50, len(P) - 5, n_cuts):
            part = fn(P[: t0 + 1], 0)
            if not np.isclose(full[t0], part[t0], atol=1e-9, equal_nan=True):
                bad.append((name, int(t0), float(full[t0]), float(part[t0])))
    return bad
