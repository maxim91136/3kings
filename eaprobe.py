import json, urllib.request
for g in ("EA","EA20","EA21","EU27_2020"):
    try:
        j=json.loads(urllib.request.urlopen(f"https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_manr?geo={g}&coicop=CP00&unit=RCH_A&lastTimePeriod=2",timeout=15).read())
        t=j["dimension"]["time"]["category"]["index"];print(g,sorted(t,key=t.get),j["value"])
    except Exception as e: print(g,"ERR",str(e)[:80])
for k in ("ICP/M.U2.N.000000.4.ANR","ICP/M.I9.N.000000.4.ANR"):
    try:
        r=urllib.request.urlopen(f"https://data-api.ecb.europa.eu/service/data/{k}?lastNObservations=2&format=csvdata",timeout=15).read().decode().splitlines();print(k,r[-2:])
    except Exception as e: print(k,"ERR",str(e)[:80])
