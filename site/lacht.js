// Joker-Knopf: kurzer Lacher bei Klick (delegiert, damit kein Inline-Handler nötig ist).
document.addEventListener("click", function (ev) {
  var b = ev.target.closest && ev.target.closest(".capbtn");
  if (!b) return;
  b.classList.remove("laugh");
  void b.offsetWidth;
  b.classList.add("laugh");
});
