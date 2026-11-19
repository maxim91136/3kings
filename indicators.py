"""Baut site/indicators.json aus data/ind_*.csv (nur Anzeige, keine Regel). Ampel nach eigener Geschichte des Indikators."""
import csv, json, os
from datetime import date, timedelta
from bisect import bisect_right


def load(name):
    f = f"data/ind_{name}.csv"
    if not os.path.exists(f): return {}
    return {r["date"]: float(r["value"]) for r in csv.DictReader(open(f))}


def pct(hist, x):
    v = sorted(hist); return bisect_right(v, x) / len(v)


def spy_ratio(since):
    """Kursveraenderung des S&P seit 'since' (fuer die Buffett-Schaetzung bis heute)."""
    rows = list(csv.DictReader(open("data/prices.csv")))
    old = [float(r["SPY"]) for r in rows if r["date"] <= since and r["SPY"]]
    return float(rows[-1]["SPY"]) / old[-1] if old else 1.0, rows[-1]["date"]


out = []
eq, gdp = load("NCBEILQ027S"), load("GDP")
if eq and gdp:
    common = sorted(set(eq) & set(gdp))
    ratio = {d: eq[d] / 1000 / gdp[d] for d in common if d >= "1950-01-01"}
    last = common[-1]
    qend = (date.fromisoformat(last) + timedelta(days=92)).replace(day=1) - timedelta(days=1)
    f, asof = spy_ratio(qend.isoformat())
    now = ratio[last] * f
    p = pct(ratio.values(), now)
    out.append(dict(key="buffett", name="Buffett-Indikator", value=f"{now*100:.0f} %", pct=round(p, 3), since="1950",
                    light="rot" if p >= 0.8 else "gruen" if p <= 0.33 else "gelb",
                    text="Börsenwert der US-Firmen im Verhältnis zur Wirtschaftsleistung. Hoch heißt teuer.",
                    note=f"Quartal bis {qend:%d.%m.%Y}, mit S&P-Kurs bis {asof} fortgeschrieben", higher="teurer"))
w5 = load("W5000")
if not (eq and gdp) and w5 and gdp:
    gk = sorted(gdp); wk = sorted(w5)
    def w_at(d):
        i = bisect_right(wk, d) - 1; return w5[wk[i]] if i >= 0 else None
    hist = []
    for g in gk:
        qe = ((date.fromisoformat(g) + timedelta(days=92)).replace(day=1) - timedelta(days=1)).isoformat()
        if qe >= wk[0] and w_at(qe): hist.append(w_at(qe) / gdp[g])
    now = w5[wk[-1]] / gdp[gk[-1]]; p = pct(hist, now)
    out.append(dict(key="buffett", name="Buffett-Indikator", value=f"{now*100:.0f} %", pct=round(p, 3), since=wk[0][:4],
                    light="rot" if p >= 0.8 else "gruen" if p <= 0.33 else "gelb",
                    text="Börsenwert aller US-Firmen (Wilshire 5000) im Verhältnis zur Wirtschaftsleistung. Hoch heißt teuer.",
                    note=f"Wilshire {wk[-1]}, Wirtschaftsleistung Quartal ab {gk[-1]}", higher="teurer"))
c = load("CAPE")
if c:
    k = max(c); p = pct(c.values(), c[k])
    out.append(dict(key="cape", name="Shiller-KGV", value=f"{c[k]:.1f}", pct=round(p, 3), since=min(c)[:4],
                    light="rot" if p >= 0.8 else "gruen" if p <= 0.33 else "gelb",
                    text="Kurs geteilt durch den Durchschnittsgewinn der letzten 10 Jahre. Hoch heißt teuer.", note=f"Stand {k}", higher="teurer"))
for key, nm, sub in (("FNG", "Fear & Greed Aktien", "CNN, 0 = extreme Angst, 100 = extreme Gier."),
                     ("CFNG", "Fear & Greed Krypto", "alternative.me, 0 = extreme Angst, 100 = extreme Gier.")):
    g = load(key)
    if g:
        k = max(g); x = g[k]
        lab = "extreme Angst" if x <= 25 else "Angst" if x <= 45 else "neutral" if x < 55 else "Gier" if x < 75 else "extreme Gier"
        out.append(dict(key=key.lower(), name=nm, value=f"{x:.0f} · {lab}", pct=None, since=None,
                        light="gruen" if x <= 25 else "rot" if x >= 75 else "gelb",
                        text=sub + " Extreme Angst war oft eine Kaufgelegenheit.", note=f"Stand {k}", higher=None))
if c:
    k = max(c); e = 1 / c[k]
    out.append(dict(key="expect", name="Erwartete Rendite pro Jahr", value=f"≈ {e*100:.1f} %", pct=None, since=None, light=None,
                    text=f"Bei einem Shiller-KGV von {c[k]:.1f}".replace(".", ",") + ": grob diese Rendite über der Inflation in den nächsten 10 Jahren (US-Aktien). Faustregel: 1 geteilt durch das KGV. Grobe Richtung, keine Prognose.",
                    note="", higher=None))
v = load("VIXCLS")
if v:
    k = max(v); p = pct(v.values(), v[k])
    out.append(dict(key="vix", name="Angst-Index VIX", value=f"{v[k]:.1f}", pct=round(p, 3), since=min(v)[:4],
                    light="gruen" if p >= 0.8 else "rot" if p <= 0.2 else "gelb",
                    text="Erwartete Schwankung. Viel Angst war oft eine Kaufgelegenheit, sehr wenig Angst heißt Sorglosigkeit.",
                    note=f"Stand {k}", higher="ängstlicher"))
y, ylab = load("T10Y2Y"), "Zinskurve 10 J − 2 J"
if not y: y, ylab = load("CURVE"), "Zinskurve 10 J − 3 M"
if y:
    k = max(y); x = y[k]
    out.append(dict(key="curve", name=ylab, value=f"{x:+.2f} %".replace("+", "+"), pct=None, since=min(y)[:4],
                    light="rot" if x < 0 else "gelb" if x < 0.5 else "gruen",
                    text="Unter null (invertiert) ging Rezessionen oft voraus, meist mit 6 bis 24 Monaten Abstand.", note=f"Stand {k}", higher=None))
t = load("DTB3") or load("IRX")
if t:
    k = max(t)
    out.append(dict(key="rate", name="US-Geldmarktzins", value=f"{t[k]:.2f} %", pct=None, since=None, light=None,
                    text="Zins für kurzfristig geparktes Geld in den USA. Grobe Richtung für Tagesgeld.", note=f"Stand {k}", higher=None))
import re
from datetime import date as _d
def _en_date(m):
    return _d(int(m.group(1)), int(m.group(2)), int(m.group(3))).strftime("%b %d, %Y").replace(" 0", " ")
EN = {"buffett": ("Buffett Indicator", "Market value of US companies relative to economic output (GDP). High means expensive."),
      "cape": ("Shiller P/E (CAPE)", "Price divided by average earnings of the last 10 years. High means expensive."),
      "fng": ("Fear & Greed (stocks)", "CNN, 0 = extreme fear, 100 = extreme greed. Extreme fear was often a buying opportunity."),
      "cfng": ("Fear & Greed (crypto)", "alternative.me, 0 = extreme fear, 100 = extreme greed. Extreme fear was often a buying opportunity."),
      "vix": ("Fear index VIX", "Expected volatility. High fear was often a buying opportunity; very low fear signals complacency."),
      "curve": (None, "Below zero (inverted) often preceded recessions, typically by 6 to 24 months."),
      "rate": ("US money market rate", "Interest on short-term cash in the US. Rough guide for savings rates.")}
LAB = [("extreme Angst", "extreme fear"), ("extreme Gier", "extreme greed"), ("Angst", "fear"), ("Gier", "greed")]
for i in out:
    nm, tx = EN.get(i["key"], (None, None))
    if i["key"] == "curve": nm = i["name"].replace("Zinskurve", "Yield curve").replace(" J", "Y").replace(" M", "M")
    if i["key"] == "expect":
        nm = "Expected return per year"
        cape = re.search(r"von ([\d.,]+)", i["text"]).group(1).replace(",", ".")
        tx = f"At a Shiller P/E of {cape}: roughly this return above inflation over the next 10 years (US stocks). Rule of thumb: 1 divided by the P/E. Rough direction, not a forecast."
    v = i["value"]
    for a_, b_ in LAB: v = v.replace(a_, b_)
    n = i["note"]
    n = re.sub(r"Wilshire (\S+), Wirtschaftsleistung Quartal ab (\S+)", r"Wilshire \1, GDP quarter from \2", n)
    n = re.sub(r"Quartal bis (\S+), mit S&P-Kurs bis (\S+) fortgeschrieben", r"Quarter to \1, extended with S&P to \2", n)
    n = re.sub(r"^Stand ", "As of ", n)
    n = re.sub(r"(\d{4})-(\d{2})-(\d{2})", _en_date, n)
    n = re.sub(r"(\d{2})\.(\d{2})\.(\d{4})", lambda m: _d(int(m.group(3)), int(m.group(2)), int(m.group(1))).strftime("%b %d, %Y").replace(" 0", " "), n)
    i.update(name_en=nm or i["name"], text_en=tx or i["text"], value_en=v, note_en=n,
             higher_en={"teurer": "pricier", "ängstlicher": "more fearful"}.get(i["higher"]))
for i in out:
    i["value"] = re.sub(r"(\d)\.(\d)", r"\1,\2", i["value"])
    i["note"] = re.sub(r"(\d)\.(\d)", r"\1,\2", i["note"])
    i["note"] = re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\3.\2.\1", i["note"])
os.makedirs("site", exist_ok=True)
json.dump(dict(indicators=out), open("site/indicators.json", "w"), ensure_ascii=False, indent=1)
print("indicators.json:", ", ".join(f"{i['name']} {i['value']} ({i['light']})" for i in out) or "keine Daten")
