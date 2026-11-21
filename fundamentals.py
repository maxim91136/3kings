"""Bruttomarge und Verschuldung (Fremdkapital/Eigenkapital) von Yahoo (quoteSummary, mit Cookie+Crumb). Modul + Test."""
import http.cookiejar, json, sys, time, urllib.request
_cj = http.cookiejar.CookieJar(); _op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(_cj))
_UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}
_crumb = None
def _get(u):
    return _op.open(urllib.request.Request(u, headers=_UA), timeout=30).read().decode()
def crumb():
    global _crumb
    if _crumb: return _crumb
    try: _get("https://fc.yahoo.com")
    except Exception: pass
    _crumb = _get("https://query2.finance.yahoo.com/v1/test/getcrumb").strip(); return _crumb
def fund(sym):
    """-> dict(margin=Bruttomarge 0..1, de=Fremdkapital/Eigenkapital als Faktor) oder None-Werte."""
    for i in range(3):
        try:
            j = json.loads(_get(f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{sym}?modules=financialData&crumb={crumb()}"))
            f = j["quoteSummary"]["result"][0]["financialData"]
            g = f.get("grossMargins", {}).get("raw"); d = f.get("debtToEquity", {}).get("raw")
            debt = f.get("totalDebt", {}).get("raw") or 0; cash = f.get("totalCash", {}).get("raw") or 0; eb = f.get("ebitda", {}).get("raw")
            nd = None if not eb or eb <= 0 else (debt - cash) / eb   # Nettoverschuldung / EBITDA (Jahre bis schuldenfrei)
            return dict(margin=g, de=None if d is None else d / 100, nd_ebitda=nd)
        except Exception as e:
            err = e; time.sleep(3 * (i + 1))
    print(sym, "Fundamentaldaten fehlen:", err); return dict(margin=None, de=None, nd_ebitda=None)
if __name__ == "__main__":
    for s in sys.argv[1:] or ["MSFT", "CTAS", "RACE", "IDXX", "COST", "ASML.AS", "RMS.PA"]:
        print(s, fund(s)); time.sleep(1)
