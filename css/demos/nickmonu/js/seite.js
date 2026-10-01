/* ==========================================================================
   SEITE — Kleinigkeiten, die jede Seite braucht
     1  Kopfzeile: Linie beim Scrollen, weicht beim Lesen aus, Menü am Handy
     2  Aktuell-Karte: zeigt den nächsten Termin, verschwindet danach
     3  Showreel: wird erst nach Klick von filmmakers.eu geladen
     4  Jahreszahl in der Fußzeile
   ========================================================================== */

(function () {
  "use strict";

  var EN = (document.documentElement.lang || "").toLowerCase().indexOf("en") === 0;

  /* 1  KOPFZEILE ---------------------------------------------------------- */

  var kopf = document.querySelector(".kopf");
  if (kopf) {
    var gescrollt = false;
    var pruefeKante = function () {
      var jetzt = window.scrollY > 8;
      if (jetzt !== gescrollt) {
        gescrollt = jetzt;
        kopf.classList.toggle("ist-gescrollt", jetzt);
      }
    };
    window.addEventListener("scroll", pruefeKante, { passive: true });
    pruefeKante();

    // Beim Lesen nach unten weicht die Kopfzeile aus, beim ersten Stück
    // zurück ist sie wieder da. Nie, solange das Menü offen ist oder der
    // Fokus in der Kopfzeile steht (Tastatur).
    var zuletzt = window.scrollY, versteckt = false, geplant = false;
    var verstecken = function (wert) {
      if (wert === versteckt) return;
      versteckt = wert;
      kopf.classList.toggle("ist-versteckt", wert);
    };
    var pruefeRichtung = function () {
      geplant = false;
      var y = window.scrollY, d = y - zuletzt;
      if (Math.abs(d) < 8) return;
      zuletzt = y;
      if (kopf.classList.contains("menue-offen") || kopf.contains(document.activeElement)) { verstecken(false); return; }
      verstecken(d > 0 && y > 320);
    };
    window.addEventListener("scroll", function () {
      if (!geplant) { geplant = true; window.requestAnimationFrame(pruefeRichtung); }
    }, { passive: true });
    kopf.addEventListener("focusin", function () { verstecken(false); });

    var knopf = kopf.querySelector(".menue-knopf");
    var menue = document.getElementById("menue");
    if (knopf && menue) {
      var offen = false;
      var setze = function (wert, fokusZurueck) {
        offen = wert;
        kopf.classList.toggle("menue-offen", wert);
        knopf.setAttribute("aria-expanded", wert ? "true" : "false");
        knopf.querySelector(".menue-knopf-wort").textContent =
          wert ? (EN ? "Close" : "Schließen") : (EN ? "Menu" : "Menü");
        document.body.classList.toggle("menue-sperre", wert);
        if (wert) {
          var erster = menue.querySelector("a");
          if (erster) window.setTimeout(function () { erster.focus(); }, 60);
        } else if (fokusZurueck) {
          knopf.focus();
        }
      };
      knopf.addEventListener("click", function () { setze(!offen, false); });
      document.addEventListener("keydown", function (e) {
        if (offen && e.key === "Escape") setze(false, true);
      });
      // Anker im Menü (z. B. #anfrage) schließen es.
      menue.addEventListener("click", function (e) {
        if (e.target.closest("a")) setze(false, false);
      });
      // Wird das Fenster breit, ist das Menü wieder eine Zeile.
      window.matchMedia("(min-width: 861px)").addEventListener("change", function (m) {
        if (m.matches && offen) setze(false, false);
      });
      // Fokus bleibt im offenen Menü.
      kopf.addEventListener("keydown", function (e) {
        if (!offen || e.key !== "Tab") return;
        var ziele = [knopf].concat(Array.prototype.slice.call(menue.querySelectorAll("a")));
        var erstes = ziele[0], letztes = ziele[ziele.length - 1];
        if (e.shiftKey && document.activeElement === erstes) { e.preventDefault(); letztes.focus(); }
        else if (!e.shiftKey && document.activeElement === letztes) { e.preventDefault(); erstes.focus(); }
      });
    }
  }

  /* 2  AKTUELL-KARTE ------------------------------------------------------
     data-termine="2026-09-24,2026-09-25,..." — die erste ist die Premiere.
     Vor der Premiere: „Premiere 24. September“. Danach: der nächste Termin.
     Nach dem letzten Termin verschwindet die Karte. */

  var MONATE = EN
    ? ["January","February","March","April","May","June","July","August","September","October","November","December"]
    : ["Jänner","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"];

  function datum(t) {
    return EN ? t.getDate() + " " + MONATE[t.getMonth()]
              : t.getDate() + ". " + MONATE[t.getMonth()];
  }

  document.querySelectorAll("[data-termine]").forEach(function (karte) {
    var termine = karte.getAttribute("data-termine").split(",").map(function (s) {
      var p = s.trim().split("-");
      return new Date(+p[0], +p[1] - 1, +p[2]);
    });
    var heute = new Date(); heute.setHours(0, 0, 0, 0);
    var naechster = null, index = -1;
    for (var i = 0; i < termine.length; i++) {
      if (termine[i] >= heute) { naechster = termine[i]; index = i; break; }
    }
    var ziel = karte.querySelector("[data-termin-text]");
    if (!naechster) {
      if (karte.hasAttribute("data-danach-weg")) karte.hidden = true;
      else if (ziel) ziel.textContent = karte.getAttribute("data-danach") || (EN ? "Most recent" : "Zuletzt");
      return;
    }
    if (!ziel) return;
    var ort = karte.getAttribute("data-ort") || "";
    var text;
    if (+naechster === +heute) text = index === 0 ? (EN ? "Premiere tonight" : "Heute Premiere") : (EN ? "Tonight" : "Heute Abend");
    else if (index === 0) text = (EN ? "Premiere " : "Premiere ") + datum(naechster);
    else text = (EN ? "Next: " : "Wieder am ") + datum(naechster);
    ziel.textContent = text + (ort ? " · " + ort : "");
  });

  /* 3  SHOWREEL -------------------------------------------------------------
     Früher: Klick lud ein iframe von filmmakers.eu nach. Filmmakers lässt
     sich aber serverseitig nicht einbetten (X-Frame-Options), das Feld blieb
     leer ("filmmakers.eu refused to connect"). Der Showreel-Knopf ist jetzt
     ein normaler Link mit target="_blank" — kein JavaScript nötig, siehe
     gemeinsam.py:showreel(). */

  /* 4  JAHR -------------------------------------------------------------- */

  var jahr = document.getElementById("jahr");
  if (jahr) jahr.textContent = String(new Date().getFullYear());
})();
