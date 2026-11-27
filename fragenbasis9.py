"""Gemeinsamer Kopf (Daten und Hilfsfunktionen) für die Fragen-Skripte; früher per exec aus fragen9.py geladen."""
import numpy as np
def winter_summer(r, a_year):
    out = []
    for y in range(a_year, 2027):
        w = [r.get("%d-%02d" % (y - 1, 11)), r.get("%d-%02d" % (y - 1, 12))] + [r.get("%d-%02d" % (y, k)) for k in range(1, 5)]
        s_ = [r.get("%d-%02d" % (y, k)) for k in range(5, 11)]
        if all(v is not None for v in w + s_): out.append((y, float(np.prod([1 + v for v in w]) - 1), float(np.prod([1 + v for v in s_]) - 1)))
    return out
def yearly(r, y0, y1):
    out = {}
    for y in range(y0, y1 + 1):
        row = [r.get("%d-%02d" % (y, k)) for k in range(1, 13)]
        if all(v is not None for v in row): out[y] = np.array(row)
    return out
def win_ret(row_by_year, y, start, L):  # Fenster aus L Monaten ab Monat start (1..12), ggf. in das Folgejahr hinein
    vals = []
    for i in range(L):
        m = start + i; yy = y + (m - 1) // 12; mm = (m - 1) % 12 + 1; vals.append(row_by_year.get(yy, [None] * 12)[mm - 1] if yy in row_by_year else None)
    return None if any(v is None for v in vals) else float(np.prod([1 + v for v in vals]) - 1)
