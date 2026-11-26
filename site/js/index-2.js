/* Nach-oben-Knopf: eigenständig, unabhängig vom Hauptskript */
(function(){var b=document.getElementById("totop");if(!b)return;var en=(document.documentElement.lang||"de")==="en"||/[?&]lang=en/.test(location.search);
document.getElementById("totopl").textContent=en?"Up":"Nach oben";b.setAttribute("aria-label",en?"Go up":"Nach oben");
function upd(){b.classList.toggle("on",(window.pageYOffset||document.documentElement.scrollTop)>window.innerHeight*1.2)}
window.addEventListener("scroll",upd,{passive:true});window.addEventListener("load",upd);upd();
b.addEventListener("click",function(){var r=window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches;try{window.scrollTo({top:0,behavior:r?"auto":"smooth"})}catch(e){window.scrollTo(0,0)}})})();
