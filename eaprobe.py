import urllib.request
t=urllib.request.urlopen("https://ec.europa.eu/eurostat/api/dissemination/catalogue/toc/txt?lang=en",timeout=60).read().decode("utf-8","replace")
for l in t.splitlines():
    c=l.split("\t")
    if len(c)>7 and c[1].strip('"').startswith(("prc_hicp","ei_cp","teicp")): print("ROW",c[1],c[0].strip()[:90],c[6],c[7])
