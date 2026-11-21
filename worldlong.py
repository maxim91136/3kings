"""Welt gegen USA über lange Zeit (MSCI Gesamtrendite brutto, Monatsende, USD). Regel: REGELN.md 2026-11-21. Schreibt site/worldlong.json."""
import json, os, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp
CODES = {"usa": 984000, "world": 990100, "acwi": 892400}
def msci(code):
    u = ("https://app2.msci.com/products/service/index/indexmaster/getLevelDataForGraph?currency_symbol=USD&index_variant=GRTR"
         f"&start_date=19691231&end_date=20991231&data_frequency=END_OF_MONTH&index_codes={code}")
    j = json.loads(fp.get(u))
    L = j["indexes"]["INDEX_LEVELS"]
    return {str(x["calc_date"])[:4] + "-" + str(x["calc_date"])[4:6]: float(x["level_eod"]) for x in L}
D = {k: msci(c) for k, c in CODES.items()}
for k, v in D.items(): print(k, len(v), min(v), max(v))
def stats(a, b):
    ks = sorted(set(D[a]) & set(D[b])); A, B = D[a], D[b]
    yrs = lambda i, j: (j - i) / 12
    cg = lambda X, i, j: (X[ks[j]] / X[ks[i]]) ** (1 / yrs(i, j)) - 1
    n = len(ks) - 1; mid = n // 2
    def mdd(X):
        hi = w = 0
        for k in ks: hi = max(hi, X[k]); w = min(w, X[k] / hi - 1)
        return w
    roll = {}
    for Y in (10, 20):
        m = Y * 12; w = [(i, i + m) for i in range(0, n - m + 1)]
        roll[Y] = {"n": len(w), "world_better": sum(B[ks[j]] / B[ks[i]] > A[ks[j]] / A[ks[i]] for i, j in w)}
    dec = []
    for y0 in range(int(ks[0][:4]) // 10 * 10, 2030, 10):
        s = [k for k in ks if int(k[:4]) >= y0 and int(k[:4]) < y0 + 10]
        p = [k for k in ks if k < s[0]] if s else []
        if not s: continue
        st = p[-1] if p else s[0]
        i, j = ks.index(st), ks.index(s[-1])
        if j - i < 24: continue
        dec.append([f"{y0}er", round(cg(A, i, j), 4), round(cg(B, i, j), 4), st, s[-1]])
    r = {"a": a, "b": b, "from": ks[0], "until": ks[-1], "mid": ks[mid],
         "usa": {"cagr": cg(A, 0, n), "h1": cg(A, 0, mid), "h2": cg(A, mid, n), "mdd": mdd(A)},
         "world": {"cagr": cg(B, 0, n), "h1": cg(B, 0, mid), "h2": cg(B, mid, n), "mdd": mdd(B)},
         "roll": roll, "decades": dec,
         "rows": [[k, round(A[k] / A[ks[0]], 3), round(B[k] / B[ks[0]], 3)] for k in ks]}
    u, w = r["usa"], r["world"]
    r["pass"] = w["cagr"] > u["cagr"] and w["h1"] > u["h1"] and w["h2"] > u["h2"] and w["mdd"] >= u["mdd"]
    return r
out = {"world": stats("usa", "world"), "acwi": stats("usa", "acwi")}
json.dump(out, open("site/worldlong.json", "w"), separators=(",", ":"))
for k, r in out.items(): print(k, json.dumps({x: y for x, y in r.items() if x != "rows"}, indent=0))
