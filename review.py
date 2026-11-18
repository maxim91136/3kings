"""Review (Kriterien vorab in REGELN.md). Aendert den Heartbeat NICHT. python3 review.py
Teil 1: Einmalanlage je Epoche nach Steuern: Halten, Trend SMA200, Vol-Target 15 %, Champion-Wahl (wie Heartbeat).
Teil 2: Monatliches neues Geld, Kaufregeln K1-K5, 10/20-Jahres-Fenster nach Steuern."""
import csv, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "core"))
import lab, team

TAX, FREI, COST, BAND = 0.26375, 0.30, 0.0005, 0.02
rows = list(csv.DictReader(open("data/spx_long.csv")))
D = [r["date"] for r in rows]; p = np.array([float(r["SPX"]) for r in rows]); T = len(p)
s200 = lab.sma(p, 200)
hi = np.array([p[max(0, t - 251): t + 1].max() for t in range(T)]); dd = p / hi - 1
P1 = p.reshape(-1, 1); fns = lab.build_strategies(["SPX"], COST)
W = {"Halten": np.ones(T), "Trend SMA200": fns["Trend SMA200 (Std.)"](P1, 0), "Vol-Target 15%": fns["Vol-Target 15% (Std.)"](P1, 0)}
res = team.run_team(P1, ["SPX"], ["SPX"])
wc = np.ones(T); wc[lab.WARM:] = res["team"][1]; W["Champion-Wahl"] = np.nan_to_num(wc, nan=1.0)
W["Trend SMA200"] = np.nan_to_num(W["Trend SMA200"]); W["Vol-Target 15%"] = np.nan_to_num(W["Vol-Target 15%"])


def sim(a, b, mode, w=None, contrib=0, start=1.0):
    """Tage a..b-1. mode: 'w' (Gewicht folgt w), 'dca', 'pause', 'dip'. Rueckgabe: Wert nach Steuer, Pfad, Eingezahlt, Steuern."""
    u = basis = loss = taxpaid = res_ = 0.0; cash = start; paid = start
    path = np.empty(b - a); paidp = np.empty(b - a)

    def sell(q, t):
        nonlocal u, basis, loss, cash, taxpaid
        if q <= 0: return
        px = p[t]; cb = basis * q / u; g = (q * px - cb) * (1 - FREI)
        basis -= cb; u -= q
        if g > 0:
            off = min(loss, g); loss -= off; tx = (g - off) * TAX
        else:
            loss += -g; tx = 0.0
        cash += q * px * (1 - COST) - tx; taxpaid += tx

    def buy(amt, t):
        nonlocal u, basis, cash
        if amt <= 0: return
        u += amt * (1 - COST) / p[t]; basis += amt; cash -= amt

    for k, t in enumerate(range(a, b)):
        if contrib and k > 0 and k % 21 == 0:
            cash += contrib; paid += contrib
            if mode == "dip": res_ += 0.2 * contrib
        up = np.isfinite(s200[t]) and p[t] > s200[t]
        if mode == "w":
            V = u * p[t] + cash; tgt = w[t] * V; cur = u * p[t]
            if abs(tgt - cur) > BAND * V or (w[t] == 0 and u > 0) or (w[t] >= 0.999 and cash > BAND * V):
                if tgt < cur: sell((cur - tgt) / p[t], t)
                else: buy(min(tgt - cur, cash), t)
        elif mode == "dca": buy(cash, t)
        elif mode == "pause":
            if up: buy(cash, t)
        elif mode == "dip":
            if dd[t] <= -0.20: res_ = 0.0
            buy(max(cash - res_, 0.0), t)
        path[k] = u * p[t] + cash; paidp[k] = paid
    if u > 0: sell(u, b - 1)
    return cash, path, paidp, taxpaid


def mdd(x):
    pk = np.maximum.accumulate(x); return float(((pk - x) / pk).max())

ix = lambda d: next(i for i, x in enumerate(D) if x >= d)
eras = [("1930-1949", "1930-01-01", "1950-01-01"), ("1950-1972", "1950-01-01", "1973-01-01"), ("1973-1982", "1973-01-01", "1983-01-01"),
        ("1983-1999", "1983-01-01", "2000-01-01"), ("2000-2009", "2000-01-01", "2010-01-01"), ("2010-2026", "2010-01-01", "2099-01-01"), ("ALLES", "1930-01-01", "2099-01-01")]
print("TEIL 1: Einmalanlage nach Steuern (Rendite/J, Rueckgang, Steuer gezahlt in % vom Endwert)")
print(f"{'Epoche':11s}" + "".join(f"{k:>24s}" for k in W))
R1 = {}
for name, lo, hi_ in eras:
    a = ix(lo); b = T if hi_ > D[-1] else ix(hi_); yrs = (b - a) / 252; line = f"{name:11s}"
    for k in W:
        v, path, _, tx = sim(a, b, "w", W[k])
        cg = v ** (1 / yrs) - 1; m = mdd(path); R1[k, name] = (cg, m)
        line += f"{cg*100:9.1f}% {m*100:5.0f}% {tx/max(v,1e-9)*100:5.1f}%  "
    print(line)
c, t_ = R1["Champion-Wahl", "ALLES"], R1["Trend SMA200", "ALLES"]
ok = t_[0] >= c[0] - 0.003 and t_[1] < c[1] and all(R1["Trend SMA200", e][1] < R1["Champion-Wahl", e][1] for e in ("1973-1982", "2000-2009"))
print(f"Frage 1 (fester Trend statt Champion-Wahl): {'ERFUELLT' if ok else 'nicht erfuellt'}  Rendite {t_[0]*100:.2f} vs {c[0]*100:.2f}, Rueckgang {t_[1]*100:.0f} vs {c[1]*100:.0f}\n")

print("TEIL 2: Monatlich 1 Einheit neues Geld, Endwert nach Steuern als Vielfaches des Eingezahlten")
K = [("K1 sofort", "dca", None), ("K2 Kauf-Pause", "pause", None), ("K3 Trend voll", "w", W["Trend SMA200"]), ("K4 Dip-Reserve", "dip", None), ("K5 Champion", "w", W["Champion-Wahl"])]
for years in (10, 20):
    L = years * 252; starts = list(range(ix("1930-01-01"), T - L, 126))
    out = {k: [] for k, _, _ in K}; uw = {k: [] for k, _, _ in K}
    for s in starts:
        for k, mode, w in K:
            v, path, paidp, _ = sim(s, s + L, mode, w, contrib=1.0, start=1.0)
            out[k].append(v / paidp[-1]); uw[k].append(float((path / paidp - 1).min()))
    base = np.array(out["K1 sofort"])
    print(f"\n{years}-Jahres-Fenster: {len(starts)} Starts {D[starts[0]][:4]}..{D[starts[-1]][:4]}")
    print(f"{'Regel':16s}{'Median':>8s}{'schl. 10%':>10s}{'bestes 10%':>11s}{'schl. Buchverlust (Median/schlimmster)':>40s}{'besser als K1':>15s}")
    for k, _, _ in K:
        x = np.array(out[k]); y = np.array(uw[k])
        print(f"{k:16s}{np.median(x):8.2f}{np.percentile(x,10):10.2f}{np.percentile(x,90):11.2f}{np.median(y)*100:25.0f}% / {y.min()*100:4.0f}%{(x>base+1e-9).mean()*100:14.0f}%")
    if years == 20:
        med = {k: np.median(out[k]) for k in out}; best = max(med, key=med.get)
        alt = [k for k in med if k != best and med[k] >= 0.98 * med[best] and np.median(uw[k]) - np.median(uw[best]) >= 0.10]
        print(f"Frage 2: hoechster Median = {best}; Alternative nach Kriterium: {alt or 'keine'}")
