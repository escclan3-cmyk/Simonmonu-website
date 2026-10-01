/* ==========================================================================
   EINSATZ — Dinge kommen, wenn man sie erreicht

   data-einsatz="zeilen"  Überschrift mit <br>: Zeile für Zeile hinter einer
                          Kante hervor, in leicht ungleichem Takt — wie
                          jemand, der beim Sprechen atmet.
   data-einsatz           Block: gleitet kurz hoch und blendet auf.
                          Geschwister im selben Elternelement kommen
                          leicht versetzt nacheinander.
   data-einsatz="bild"    Bild: öffnet sich von leicht beschnitten auf
                          ganz, das Foto setzt sich aus leichter
                          Vergrößerung.

   Läuft einmal. Wer zurückscrollt, sieht nichts erneut.
   Der erste Bildschirm ist ausgenommen: er muss sofort dastehen.
   ========================================================================== */

(function () {
  "use strict";

  if (typeof window === "undefined" || !("IntersectionObserver" in window)) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var TAKT = [0, 78, 62, 96, 70, 88, 64, 92];

  var beobachter = new IntersectionObserver(function (eintraege, obs) {
    eintraege.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add("ist-da");
      obs.unobserve(e.target);
    });
  }, { rootMargin: "0px 0px -10% 0px", threshold: 0.12 });

  function imErstenBild(el) {
    var r = el.getBoundingClientRect();
    return r.top < window.innerHeight * 0.9;
  }

  document.querySelectorAll('[data-einsatz="zeilen"]').forEach(function (el) {
    if (imErstenBild(el)) return;
    var teile = el.innerHTML.split(/<br\s*\/?>/i);
    el.innerHTML = teile.map(function (t) {
      return '<span class="einsatz-zeile"><span class="einsatz-innen">' + t + "</span></span>";
    }).join("");
    el.querySelectorAll(".einsatz-innen").forEach(function (z, i) {
      z.style.transitionDelay = (i ? TAKT[i % TAKT.length] + i * 48 : 0) + "ms";
    });
    el.classList.add("einsatz");
    beobachter.observe(el);
  });

  document.querySelectorAll('[data-einsatz="bild"]').forEach(function (el) {
    if (imErstenBild(el)) return;
    el.classList.add("einsatz-bild");
    el.addEventListener("transitionend", function fertig(e) {
      if (e.target !== el || e.propertyName !== "clip-path") return;
      el.classList.add("ist-fertig");
      el.removeEventListener("transitionend", fertig);
    });
    beobachter.observe(el);
  });

  var gruppen = new Map();
  document.querySelectorAll("[data-einsatz]:not([data-einsatz='zeilen']):not([data-einsatz='bild'])").forEach(function (el) {
    if (imErstenBild(el)) return;
    var eltern = el.parentNode;
    var n = gruppen.get(eltern) || 0;
    gruppen.set(eltern, n + 1);
    el.classList.add("einsatz-block");
    el.style.transitionDelay = Math.min(n, 6) * 70 + "ms";
    beobachter.observe(el);
  });
})();
