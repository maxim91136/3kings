"""Universum für das Elite-Screening: S&P 500 (aktuelle Mitglieder mit GICS-Branche, von Wikipedia) + feste Europa-Liste.
Ohne Argument: Branchenübersicht ausgeben. Modul: sp500() -> [dict(sym, name, sector, sub)]."""
import html, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_prices as fp
def _txt(c): return html.unescape(re.sub(r"<[^>]+>", "", c)).strip()
def sp500():
    t = fp.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    tab = t[t.index('id="constituents"'):]; tab = tab[:tab.index("</table>")]
    out = []
    for tr in tab.split("<tr")[2:]:
        c = [_txt(x) for x in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
        if len(c) >= 4: out.append(dict(sym=c[0].replace(".", "-"), name=c[1], sector=c[2], sub=c[3]))
    return out
if __name__ == "__main__":
    from collections import Counter
    L = sp500(); print("Mitglieder:", len(L))
    cnt = Counter((r["sector"], r["sub"]) for r in L)
    for (s, u), n in sorted(cnt.items()): print(f"{s} | {u} | {n} | " + ", ".join(r["sym"] for r in L if r["sub"] == u)[:120])
