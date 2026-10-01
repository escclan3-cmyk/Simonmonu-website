/* ==========================================================================
   SEITE — was jede Seite braucht
     1  Kopfzeile: Linie beim Scrollen, weicht beim Lesen aus
     2  Menü am Handy: öffnen, schließen, Fokus halten, Esc
     3  Jahreszahl in der Fußzeile
   ========================================================================== */
(function () {
  "use strict";

  var kopf = document.querySelector(".kopf");
  if (!kopf) return;

  /* 1  KOPFZEILE ---------------------------------------------------------- */
  var zuletzt = window.scrollY, versteckt = false, geplant = false;
  function pruefe() {
    geplant = false;
    var y = window.scrollY, d = y - zuletzt;
    kopf.classList.toggle("ist-gescrollt", y > 8);
    if (Math.abs(d) < 8) return;
    zuletzt = y;
    var sollVersteckt = d > 0 && y > 400 && !kopf.classList.contains("menue-offen") && !kopf.contains(document.activeElement);
    if (sollVersteckt !== versteckt) {
      versteckt = sollVersteckt;
      kopf.classList.toggle("ist-versteckt", versteckt);
    }
  }
  window.addEventListener("scroll", function () {
    if (!geplant) { geplant = true; window.requestAnimationFrame(pruefe); }
  }, { passive: true });
  kopf.addEventListener("focusin", function () { versteckt = false; kopf.classList.remove("ist-versteckt"); });
  pruefe();

  /* 2  MENÜ ---------------------------------------------------------------- */
  var knopf = kopf.querySelector(".menue-knopf");
  var menue = document.getElementById("menue");
  var wort = kopf.querySelector(".menue-knopf-wort");
  var schmal = window.matchMedia("(max-width: 1179px)");
  var offen = false;

  // Alle bedienbaren Elemente der Kopfzeile in DOM-Reihenfolge (Logo, Menü, Knopf)
  function ziele() {
    return Array.prototype.slice.call(kopf.querySelectorAll("a[href], button")).filter(function (el) {
      return el.offsetWidth > 0 || el.offsetHeight > 0;
    });
  }
  function setze(wert, fokusZurueck) {
    offen = wert;
    kopf.classList.toggle("menue-offen", wert);
    knopf.setAttribute("aria-expanded", wert ? "true" : "false");
    wort.textContent = wert ? "Schließen" : "Menü";
    document.body.classList.toggle("menue-sperre", wert);
    var main = document.getElementById("inhalt");
    var fuss = document.querySelector(".fuss");
    [main, fuss].forEach(function (el) { if (el) { if (wert) el.setAttribute("inert", ""); else el.removeAttribute("inert"); } });
    if (wert) {
      // Das Menü beginnt direkt unter der Kopfzeile, auch wenn darüber noch die Demo-Leiste steht
      menue.style.top = Math.max(0, Math.round(kopf.getBoundingClientRect().bottom)) + "px";
      var erster = menue.querySelector("a");
      if (erster) window.setTimeout(function () { erster.focus(); }, 30);
    } else {
      menue.style.top = "";
      if (fokusZurueck) knopf.focus();
    }
  }
  if (knopf && menue) {
    knopf.addEventListener("click", function () { setze(!offen, false); });
    document.addEventListener("keydown", function (e) {
      if (offen && e.key === "Escape") setze(false, true);
    });
    menue.addEventListener("click", function (e) { if (offen && e.target.closest("a")) setze(false, false); });
    kopf.addEventListener("keydown", function (e) {
      if (!offen || e.key !== "Tab") return;
      var z = ziele(), erstes = z[0], letztes = z[z.length - 1];
      if (e.shiftKey && document.activeElement === erstes) { e.preventDefault(); letztes.focus(); }
      else if (!e.shiftKey && document.activeElement === letztes) { e.preventDefault(); erstes.focus(); }
    });
    var wechsel = function (m) { if (!m.matches && offen) setze(false, false); };
    if (schmal.addEventListener) schmal.addEventListener("change", wechsel);
  }

  /* 3  JAHR ---------------------------------------------------------------- */
  document.querySelectorAll("[data-jahr]").forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
