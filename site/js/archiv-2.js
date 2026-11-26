{const EN2=document.documentElement.lang==="en",b=document.getElementById("totop");document.getElementById("totopl").textContent=EN2?"Up":"Nach oben";b.setAttribute("aria-label",EN2?"Go up":"Nach oben");
const upd=()=>b.classList.toggle("on",scrollY>innerHeight*1.2);addEventListener("scroll",upd,{passive:true});upd();
b.onclick=()=>scrollTo({top:0,behavior:matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth"})}
