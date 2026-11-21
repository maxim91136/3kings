import urllib.request,re
t=urllib.request.urlopen("https://ec.europa.eu/eurostat/api/dissemination/catalogue/toc/txt?lang=en",timeout=60).read().decode("utf-8","replace")
for l in t.splitlines():
    if "HICP" in l and ("annual rate" in l.lower() or "flash" in l.lower()): print(l[:200])
