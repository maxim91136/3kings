#!/usr/bin/env python3
"""Siegel einer Kronakte aendern. Schreibt immer einen Protokolleintrag.
Aufruf: python siegel.py <id> <offen|aufgeklaert|eingestellt> "Begruendung DE" "Reason EN"
"""
import json, sys, datetime
ST={"offen":("Fall offen","case open"),"aufgeklaert":("aufgeklärt","solved"),"eingestellt":("eingestellt","closed")}
def run(i,st,de,en,today=None,base="."):
    f=base+"/site/siegel.json"; m=json.load(open(f))
    if i not in m: raise SystemExit("unbekannte Akte: "+i)
    if st not in ST: raise SystemExit("unbekannter Zustand: "+st)
    if not de.strip() or not en.strip(): raise SystemExit("Begruendung (DE und EN) ist Pflicht")
    day=today or datetime.date.today().isoformat(); old=m[i]; m[i]=st
    json.dump(m,open(f,"w"),indent=1)
    td=f"\n## {day}: Siegel {i}: {ST[old][0]} → {ST[st][0]}\n{de}\n"
    te=f"\n## {day}: Seal {i}: {ST[old][1]} → {ST[st][1]}\n{en}\n"
    for p,t in (("REGELN.md",td),("REGELN.en.md",te),("site/REGELN.md",td),("site/REGELN.en.md",te)):
        open(base+"/"+p,"a").write(t)
if __name__=="__main__":
    if "--selftest" in sys.argv:
        import tempfile,os,shutil
        t=tempfile.mkdtemp(); os.makedirs(t+"/site")
        json.dump({"d-x":"offen"},open(t+"/site/siegel.json","w"))
        for p in ("REGELN.md","REGELN.en.md","site/REGELN.md","site/REGELN.en.md"): open(t+"/"+p,"w").write("")
        run("d-x","aufgeklaert","Regel erfüllt.","Rule met.","2030-01-01",t)
        assert json.load(open(t+"/site/siegel.json"))["d-x"]=="aufgeklaert"
        assert "Siegel d-x" in open(t+"/REGELN.md").read() and "Seal d-x" in open(t+"/site/REGELN.en.md").read()
        try: run("d-x","eingestellt","","x",None,t); raise AssertionError
        except SystemExit: pass
        shutil.rmtree(t); print("selftest ok")
    else:
        if len(sys.argv)!=5: raise SystemExit(__doc__)
        run(*sys.argv[1:5])
