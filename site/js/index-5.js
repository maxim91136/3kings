(function(){function op(t){for(var d=t&&t.closest("details");d;d=d.parentElement&&d.parentElement.closest("details"))d.open=true}
function go(h){if(!h||h.length<2)return;var t=document.getElementById(decodeURIComponent(h.slice(1)));if(t){op(t);setTimeout(function(){t.scrollIntoView()},30)}}
document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest('a[href^="#"]');if(a)go(a.getAttribute("href"))});
addEventListener("hashchange",function(){go(location.hash)});setTimeout(function(){go(location.hash)},1500)})()
