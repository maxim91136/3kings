"""S&P 500 langfristig: Monatsendwerte aus data/spx_long.csv -> site/spx_long.json (nur Anzeige)."""
import csv, json
rows = list(csv.DictReader(open("data/spx_long.csv")))
m = {}
for r in rows: m[r["date"][:7]] = float(r["SPX"])
ks = sorted(m); last = rows[-1]
yrs = (int(last["date"][:4]) + int(last["date"][5:7]) / 12) - (int(ks[0][:4]) + int(ks[0][5:]) / 12)
p0, p1 = m[ks[0]], float(last["SPX"])
ath = max(float(r["SPX"]) for r in rows)
out = dict(since=ks[0], until=last["date"], last=p1, ath=ath, cagr=round((p1 / p0) ** (1 / yrs) - 1, 4), rows=[[k, round(m[k], 2)] for k in ks])
json.dump(out, open("site/spx_long.json", "w"), separators=(",", ":"))
print(f"spx_long.json: {len(ks)} Monate {ks[0]}..{last['date']}, {out['cagr']*100:.1f} %/J ohne Dividenden")
