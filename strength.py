"""Studie Relative Staerke fuer neues Geld (Kriterien vorab in REGELN.md). Aendert den Heartbeat NICHT. python3 strength.py"""
import csv, numpy as np

def load(path, cols):
    r = list(csv.DictReader(open(path)))
    r = [x for x in r if all(x.get(c) not in ("", None) for c in cols)]
    return [x["date"] for x in r], np.array([[float(x[c]) for c in cols] for x in r])

def sim(P, a, b, rule, cost):
    n = P.shape[1]; u = np.zeros(n); cash = paid = 0.0; under = 0.0
    for k, t in enumerate(range(a, b)):
        if k % 21 == 0: cash += 1; paid += 1
        if cash > 0:
            r6 = P[t] / P[t - 126] - 1; r12 = P[t - 21] / P[t - 252] - 1; r12f = P[t] / P[t - 252] - 1
            if rule == "M0": w = np.eye(n)[0]
            elif rule == "M1": w = np.ones(n) / n
            elif rule == "M2": w = np.eye(n)[np.argmax(r6)]
            elif rule == "M3": w = np.eye(n)[np.argmax(r12)]
            elif rule == "M4": w = np.eye(n)[np.argmax(r12)] if r12f[np.argmax(r12)] > 0 else None
            elif rule == "M5": w = np.eye(n)[np.argmin(r12)]
            if w is not None:
                u += cash * w * (1 - cost) / P[t]; cash = 0.0
        v = (u * P[t]).sum() + cash; under = min(under, v / paid - 1)
    return ((u * P[b - 1]).sum() + cash) / paid, under

def test(title, D, P, cost, base_label):
    L = 1260; st = list(range(252, len(D) - L, 21)); h = len(st) // 2
    R = {k: np.array([sim(P, s, s + L, k, cost) for s in st]) for k in ("M0", "M1", "M2", "M3", "M4", "M5")}
    print(f"\n=== {title}: {D[0]} .. {D[-1]}, {len(st)} Fenster a 5 Jahre (M0 = alles in {base_label}) ===")
    print(f"{'Regel':6s}{'Median':>8s}{'schl. 10%':>10s}{'schl. Buchverlust':>19s}{'1. Haelfte':>12s}{'2. Haelfte':>12s}")
    out = {}
    for k, x in R.items():
        m1, m2 = np.median(x[:h, 0]), np.median(x[h:, 0])
        print(f"{k:6s}{np.median(x[:,0]):8.2f}{np.percentile(x[:,0],10):10.2f}{x[:,1].min()*100:18.0f}%{m1:12.2f}{m2:12.2f}")
        out[k] = (np.median(x[:, 0]), m1, m2)
    return out

D, P = load("data/prices.csv", ["SPY", "BTC", "GLD"]); test("Test A: S&P, Bitcoin, Gold", D, P, 0.0007, "S&P")
D, P = load("data/prices.csv", ["SPY", "GLD"]); B = test("Test B: S&P, Gold", D, P, 0.0005, "S&P")
D, P = load("data/candidates.csv", ["VT", "EEM", "IEF", "XLK"]); C = test("Test C: VT, EEM, IEF, XLK", D, P, 0.0005, "VT (Welt)")
print("\nKriterium (Test B und C: Median >= +3 % ueber M0 und in beiden Haelften vorne):")
for k in ("M1", "M2", "M3", "M4", "M5"):
    ok = all(X[k][0] >= X["M0"][0] * 1.03 and X[k][1] > X["M0"][1] and X[k][2] > X["M0"][2] for X in (B, C))
    print(f"  {k}: {'ERFUELLT' if ok else 'nicht erfuellt'}")
