"""S&P 500 gegen Gold, alle Mischungen seit 1971 (REGELN 2026-11-22, Regeln vorab). Ergänzt site/fragen.json um golda und test B (nur Filter)."""
import json
exec(open("fragen2.py").read().split("R = json.load")[0])
def run(a, b):
    out = []
    for gs in range(0, 101, 5):
        c, d = cagr_mdd(mix([tr, g], [1 - gs / 100, gs / 100], a, b, 12)); out.append(dict(gold=gs, cagr=round(c, 4), mdd=round(d, 3), ratio=round(c / d, 3)))
    return out
full = run("1971-08", last); base = full[0]
for r in full: r["ok"] = r["gold"] > 0 and r["ratio"] > base["ratio"] and r["mdd"] <= base["mdd"] + .05
def rk(rows): o = sorted(rows, key=lambda r: -r["ratio"]); return {r["gold"]: i + 1 for i, r in enumerate(o)}
info = {lab: rk(run(a, b)) for lab, a, b in (("1980", "1980-01", last), ("2000", "2000-01", last), ("h1", "1971-08", "1999-12"), ("h2", "2000-01", last))}
for r in full: r.update({"rank_" + k: v[r["gold"]] for k, v in info.items()})
ok = sorted([r for r in full if r["ok"]], key=lambda r: -r["ratio"])
R = json.load(open("site/fragen.json"))
K = R["konstellation"]; b50 = sorted([r for r in K["rows"] if r["ok"] and r["sp"] >= 50], key=lambda r: -r["ratio"])
R["golda"] = dict(last=last, base=base, rows=full, n_ok=len(ok), best=ok[:3])
R["konstellation"]["best50"] = b50[:5]
json.dump(R, open("site/fragen.json", "w"), ensure_ascii=False, indent=1)
print("Basis", base); print("erfüllen:", len(ok), "von", len(full) - 1)
for r in full: print(r)
print("--- Test B: beste mit S&P>=50 seit 2014")
for r in b50[:6]: print(r)
