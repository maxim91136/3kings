"""Dauerläufer-Messungen (REGELN 2026-11-21): 10 Jahre Wochenschlusskurse, Heimatwährung, inkl. Dividenden.
uw  = Anteil der Wochen mehr als 20 % unter dem bisherigen Hoch (Zeit unter Wasser)
vol = eigene Schwankung pro Jahr (Standardabweichung der Wochenrenditen x Wurzel 52)"""
import numpy as np
def steady(s, until=None):
    ds = sorted(d for d in s if until is None or d <= until)
    if not ds: return None, None
    d1 = ds[-1]; t = f"{int(d1[:4]) - 10}{d1[4:]}"
    if ds[0] > t: return None, None
    wk = {}
    for d in ds:
        if d >= t: wk[str(np.datetime64(d, "W"))] = s[d]
    p = np.array(list(wk.values()), dtype=float)
    if len(p) < 400: return None, None
    dd = 1 - p / np.maximum.accumulate(p)
    return float((dd > .2).mean()), float(np.diff(np.log(p)).std(ddof=1) * np.sqrt(52))
