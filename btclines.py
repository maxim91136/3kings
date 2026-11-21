"""Bitcoin-Linien im Vergleich (REGELN 2026-11-21, nur Information): Halten, Trend 50/100/200/300 und Mix (anteilig).
Euro, Signal zum Schlusskurs, umgeschichtet zum nächsten Schlusskurs, Kosten 0,1 % je Seite.
Vorwärts ab START (Test nach vorn) und Rückblick über die ganze Historie zur Einordnung. Schreibt site/btclines.json."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "core"))
import lab
from heartbeat import to_eur
START, COST = "2026-11-20", 0.001
NAMES = {"Halten": "Halten (Baseline)", "Linie 50": "Trend 50 (Std.)", "Linie 100": "Trend SMA100 (Std.)",
         "Linie 200": "Trend SMA200 (Std.)", "Linie 300": "Trend 300 (Std.)", "Mix": "Trend-Mix 50/100/200/300 (Std.)"}
dates, names, P = lab.load_prices("data/prices.csv"); P = to_eur(dates, P)
a = names.index("BTC"); fns = lab.build_strategies(names, COST); r = lab.returns(P)[:, a]
dates = [str(d)[:10] for d in dates]; i0 = next(i for i, d in enumerate(dates) if d >= START)
out = dict(start=dates[i0], date=dates[-1], rows=[])
for lab_, key in NAMES.items():
    w = fns[key](P, a); w = np.nan_to_num(w)
    net = lab.backtest(w, r, COST)          # Gewicht von gestern auf heutige Rendite = Umschichtung zum nächsten Schluss
    eq = np.cumprod(1 + net); m = lab.metrics(net[lab.WARM:], w[lab.WARM:])
    sw = float(np.abs(np.diff(w[lab.WARM:])).sum() / ((len(w) - lab.WARM) / 252))
    out["rows"].append(dict(name=lab_, fwd=round(float(eq[-1] / eq[i0] - 1), 4), w_now=round(float(w[-1]), 2),
                            cagr=round(m["cagr"], 3) if isinstance(m, dict) else None, mdd=round(m["mdd"], 3) if isinstance(m, dict) else None,
                            sharpe=round(m["sharpe"], 2) if isinstance(m, dict) else None, switches=round(sw, 1)))
out["back_from"] = dates[lab.WARM]
json.dump(out, open("site/btclines.json", "w"), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False))
