/* ==========================================================================
   EINSATZ — Maßlinien und die Werkzeichnung ziehen sich einmal auf
   Elemente mit data-zeichnen bekommen .ist-da, sobald sie zu sehen sind.

   Sicherungen, damit nie etwas fehlt:
   - Ohne JavaScript, ohne IntersectionObserver oder bei „Bewegung
     reduzieren“ wird nichts versteckt: .zeichnen-bereit wird nie gesetzt.
   - Versteckt ist ohnehin nur die Eisen- bzw. Graphitlinie. Die graue
     Maßlinie und die Vorzeichnung darunter stehen immer da, Zahlen und
     Beschriftungen auch.
   - Meldet der Beobachter ein Element nach 1,8 s noch gar nicht (auch nicht
     als „nicht sichtbar“), wird es fertig gezeichnet gezeigt.
   - Vor dem Drucken wird alles fertig gezeichnet.
   ========================================================================== */
(function () {
  "use strict";
  var els = Array.prototype.slice.call(document.querySelectorAll("[data-zeichnen]"));
  if (!els.length) return;
  if (!("IntersectionObserver" in window)) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var gemeldet = [];
  var beobachter = new IntersectionObserver(function (eintraege) {
    eintraege.forEach(function (e) {
      if (gemeldet.indexOf(e.target) < 0) gemeldet.push(e.target);
      if (e.isIntersecting) {
        e.target.classList.add("ist-da");
        beobachter.unobserve(e.target);
      }
    });
  }, { rootMargin: "0px 0px -10% 0px", threshold: 0.15 });

  els.forEach(function (el) { beobachter.observe(el); });
  document.documentElement.classList.add("zeichnen-bereit");

  function alles() { els.forEach(function (el) { el.classList.add("ist-da"); }); }
  window.setTimeout(function () {
    els.forEach(function (el) { if (gemeldet.indexOf(el) < 0) el.classList.add("ist-da"); });
  }, 1800);
  window.addEventListener("beforeprint", alles);
})();
