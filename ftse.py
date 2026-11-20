"""Test FTSE All-World (VWRL) gegen S&P 500 (SPY), beides inkl. Ausschüttungen in Euro. Schreibt site/ftse.json. Kriterium siehe REGELN.md 2026-11-21."""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp
fx = {r["date"]: float(r["value"]) for r in csv.DictReader(open("data/ind_EURUSD.csv"))}
def usd2eur(d):
    out, last = {}, None
    for k in sorted(d):
        last = fx.get(k, last)
        if last: out[k] = d[k] / last
    return out
src = None
def tr(sym):
    """Gesamtrendite selbst gerechnet: Schlusskurs plus wiederangelegte Ausschüttungen (Yahoo-adjclose fehlt bei EU-Listings oft)."""
    import time
    j = json.loads(fp.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?period1=946684800&period2={int(time.time())}&interval=1d&events=div"))["chart"]["result"][0]
    cl = j["indicators"]["quote"][0]["close"]; adj = (j["indicators"].get("adjclose") or [{}])[0].get("adjclose")
    divs = {fp.day(int(t)): v["amount"] for t, v in (j.get("events", {}).get("dividends") or {}).items()}
    print(sym, "Ausschüttungen:", len(divs), "Summe", round(sum(divs.values()), 2), "| adj/close Start", adj and round(adj[0] / cl[0], 3))
    out, units = {}, 1.0
    for t, c in zip(j["timestamp"], cl):
        if not c: continue
        k = fp.day(t)
        if k in divs: units *= 1 + divs[k] / c
        out[k] = c * units
    return out
for sym, cur in (("VWRL.AS", "EUR"), ("VWRD.L", "USD")):
    try:
        d = tr(sym)
        if len(d) > 2000: F = d if cur == "EUR" else usd2eur(d); src = sym; break
    except Exception as e: print(sym, e)
S = usd2eur(fp.yahoo("SPY"))
ks = sorted(set(S) & set(F))
# Monatsende-Reihe
m = {}
for k in ks: m[k[:7]] = k
mk = [m[x] for x in sorted(m)]
def cagr(d, a, b): return (d[b] / d[a]) ** (365.25 / ((__import__("datetime").date.fromisoformat(b) - __import__("datetime").date.fromisoformat(a)).days)) - 1
def mdd(d, keys):
    hi, w = 0, 0
    for k in keys: hi = max(hi, d[k]); w = min(w, d[k] / hi - 1)
    return w
a, b = ks[0], ks[-1]; mid = ks[len(ks) // 2]
res = {"src": src, "from": a, "until": b, "mid": mid}
for name, d in (("spy", S), ("ftse", F)):
    res[name] = {"cagr": cagr(d, a, b), "h1": cagr(d, a, mid), "h2": cagr(d, mid, b), "mdd": mdd(d, ks), "x": d[b] / d[a]}
win = [(mk[i], mk[i + 60]) for i in range(len(mk) - 60)]
res["roll5"] = {"n": len(win), "ftse_better": sum(F[e] / F[s] > S[e] / S[s] for s, e in win)}
s = f = n = 0
for k in mk[:-1] + [mk[-1]]:
    s += 100 / S[k]; f += 100 / F[k]; n += 100
res["plan"] = {"paid": n, "spy": s * S[b], "ftse": f * F[b]}
r = res
res["pass"] = r["ftse"]["cagr"] > r["spy"]["cagr"] and r["ftse"]["h1"] > r["spy"]["h1"] and r["ftse"]["h2"] > r["spy"]["h2"] and r["ftse"]["mdd"] >= r["spy"]["mdd"]
res["rows"] = [[k[:7], round(S[k] / S[a], 4), round(F[k] / F[a], 4)] for k in mk]
json.dump(res, open("site/ftse.json", "w"), separators=(",", ":"))
print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1))
