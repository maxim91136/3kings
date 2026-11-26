const qs=new URLSearchParams(location.search);let LANG=qs.get("lang")||(()=>{try{return localStorage.getItem("lang")}catch(e){return null}})()||(navigator.language||"de").slice(0,2);if(LANG!=="en")LANG="de";try{localStorage.setItem("lang",LANG)}catch(e){}
const EN=LANG==="en";setTimeout(()=>{const a=document.getElementById("pk");if(a)a.href="protokoll.html?lang="+LANG},0);document.documentElement.lang=LANG;document.getElementById(EN?"len":"lde").className="on";document.getElementById("lde").href="?lang=de&v="+Date.now();document.getElementById("len").href="?lang=en&v="+Date.now();document.getElementById("back").href="./?lang="+LANG;
if(EN){document.title="3Kings · Rule book";document.getElementById("back").textContent="← Back to overview";document.getElementById("ttl").textContent="Rule book";document.getElementById("lead").innerHTML='What applies today, by topic. Derivation and earlier versions in the <a href="protokoll.html?lang=en">log</a>.'}
const esc=s=>s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
const inl=s=>esc(s).replace(/\*\*(.+?)\*\*/g,"<b>$1</b>").replace(/`(.+?)`/g,"<code>$1</code>")
 ;   // Regelbuch ist bereits im richtigen Zahlenformat
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
fetch(EN?"REGELBUCH.en.md":"REGELBUCH.md",{cache:"no-store"}).then(r=>r.text()).then(t=>{document.getElementById("doc").innerHTML=md(t)+`<h2>${EN?"Log":"Protokoll"}</h2><p><a href="protokoll.html?lang=${LANG}">${EN?"All decisions, tests and earlier versions with dates":"Alle Entscheidungen, Tests und früheren Fassungen mit Datum"} →</a></p>`}).catch(()=>{document.getElementById("doc").textContent=EN?"Rule book could not be loaded.":"Regelbuch konnte nicht geladen werden."});
