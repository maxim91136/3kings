const qs=new URLSearchParams(location.search);let LANG=qs.get("lang")||(()=>{try{return localStorage.getItem("lang")}catch(e){return null}})()||(navigator.language||"de").slice(0,2);if(LANG!=="en")LANG="de";try{localStorage.setItem("lang",LANG)}catch(e){}
const EN=LANG==="en";setTimeout(()=>{const a=document.getElementById("rb");if(a)a.href="regeln.html?lang="+LANG},0);document.documentElement.lang=LANG;document.getElementById(EN?"len":"lde").className="on";document.getElementById("lde").href="?lang=de&v="+Date.now();document.getElementById("len").href="?lang=en&v="+Date.now();document.getElementById("back").href="./?lang="+LANG;
if(EN){document.title="3Kings · Log";document.getElementById("back").textContent="← Back to overview";document.getElementById("ttl").textContent="Log";document.getElementById("lead").innerHTML='Every decision, test and change with its date. What applies today is in the <a href="regeln.html?lang=en">rule book</a>.'}
const esc=s=>s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
const inl=s=>esc(s).replace(/\*\*(.+?)\*\*/g,"<b>$1</b>").replace(/`(.+?)`/g,"<code>$1</code>")
 .replace(/\b(\d+)\.(\d+)\b/g,EN?"$1.$2":"$1,$2");
function md(t){let o="",list=false,para=[];
 const fp=()=>{if(para.length){o+="<p>"+inl(para.join(" "))+"</p>";para=[]}};
 const fl=()=>{if(list){o+="</ul>";list=false}};
 for(const raw of t.split("\n")){const l=raw.trimEnd();
  if(!l.trim()){fp();fl();continue}
  let m;
  if(m=l.match(/^(#{1,3})\s+(.*)/)){fp();fl();const n=m[1].length;
   if(n===1)continue;o+=`<h${n}>${inl(m[2])}</h${n}>`;continue}
  if(m=l.match(/^\s*[-*]\s+(.*)/)){fp();if(!list){o+="<ul>";list=true}o+="<li>"+inl(m[1])+"</li>";continue}
  if(list&&/^\s{2,}/.test(raw)){o=o.replace(/<\/li>$/," "+inl(l.trim())+"</li>");continue}
  fl();para.push(l.trim())}
 fp();fl();return o}
fetch(EN?"REGELN.en.md":"REGELN.md",{cache:"no-store"}).then(r=>r.text()).then(t=>{
 const parts=t.split(/\n(?=## )/),head=parts.shift(),secs=parts.reverse();   // neueste Einträge zuerst
 const last=(secs[0]||"").match(/^## (\d{4}-\d{2}-\d{2})/);
 document.getElementById("doc").innerHTML=`<h2 style="border-top:0;padding-top:0;margin-top:0">${EN?"Preface":"Vorbemerkung"}</h2>`+md(head)+(last?`<h2>${EN?"Entries, newest first":"Einträge, neueste zuerst"}</h2><p class="lead" style="margin:0 0 8px">${EN?"Latest entry: ":"Letzter Eintrag: "}${last[1].split("-").reverse().join(".")}</p>`:"")+md(secs.join("\n"))})
 .catch(()=>{document.getElementById("doc").textContent=EN?"Rule book could not be loaded.":"Regelbuch konnte nicht geladen werden."});
