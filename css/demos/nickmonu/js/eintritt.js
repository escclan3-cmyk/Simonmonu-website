/* ==========================================================================
   EINTRITT — die Startansicht, einmal pro Besuch

   Stand 25. Ersetzt den gezeichneten Samtvorhang (Canvas, Federphysik,
   Soffitte, dicker Goldbalken, Tasten-Grafik). Der hat einen echten
   Gegenstand nachgeahmt — und genau das liest sich als „Photoshop-Intro“.
   Jetzt: nur Schrift, eine Linie und zwei flache Flügel.

   Ablauf
   1. Dunkel. Der Name kommt hinter seiner Kante hervor.
   2. Eine Haarlinie füllt sich von der Mitte nach außen in Messing, unten
      rechts zählt eine kleine Zahl mit. Beides zeigt den echten
      Ladestand (Schriften, erstes Bild, Seite) — frühestens nach 1,1 s,
      spätestens nach 2,8 s ist es voll.
   3. Name und Linie treten zurück, zwei flache Flügel gehen auseinander,
      und auf der Seite kommt der Name zeilenweise nach (css Abschnitt 14).

   Regeln
   - Läuft einmal pro Besuch (sessionStorage „nm-eintritt“). Mit ?intro an
     der Adresse läuft es immer — zum Vorführen.
   - Jede Taste, ein Klick, Mausrad oder Wischen beendet es sofort.
   - Bei „Bewegung reduzieren“ läuft nichts, die Seite steht sofort da.
   - Wird im <head> geladen (ohne defer), damit vor dem ersten Bild
     feststeht, ob abgedeckt wird. Nichts davon ist inline — die
     Content-Security-Policy erlaubt nur Skripte von dieser Domain.
   - Jede CSS-Regel dazu hat eine Sicherung: Nach 6 s ist alles sichtbar,
     auch wenn hier etwas abbricht.
   ========================================================================== */

(function () {
  "use strict";

  var EINST = {
    merker:     "nm-eintritt",
    mindestens: 1100,   // ms – die Linie läuft nie schneller voll
    hoechstens: 2800,   // ms – danach ist sie voll, egal was noch lädt
    halten:     160,    // ms – kurz stehen lassen, wenn voll
    zurueck:    260,    // ms – Name tritt zurück, bevor die Flügel gehen
    oeffnen:    1150,   // ms – wie in css .nm-tor-fluegel
    name:       "Nicholas Monu"
  };

  var wurzel = document.documentElement;
  var EN = (wurzel.lang || "").toLowerCase().indexOf("en") === 0;

  var reduziert = false;
  try { reduziert = window.matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) {}
  if (reduziert) return;

  var erzwungen = false;
  try { erzwungen = new URLSearchParams(window.location.search).has("intro"); } catch (e) {}

  if (!erzwungen) {
    var gesehen = false;
    try { gesehen = window.sessionStorage.getItem(EINST.merker) === "1"; } catch (e) {}
    if (gesehen) return;
  }
  try { window.sessionStorage.setItem(EINST.merker, "1"); } catch (e) {}

  // Ab hier läuft die Startansicht. Die Klasse deckt über CSS sofort ab.
  wurzel.classList.add("nm-start");

  var tor, linie, zahl, fertig = false, beendet = false;

  function bauen() {
    tor = document.createElement("div");
    tor.className = "nm-tor";
    tor.setAttribute("aria-hidden", "true");
    tor.innerHTML =
      '<div class="nm-tor-fluegel nm-tor-links"></div>' +
      '<div class="nm-tor-fluegel nm-tor-rechts"></div>' +
      '<div class="nm-tor-mitte">' +
        '<p class="nm-tor-name"><span></span></p>' +
        '<div class="nm-tor-linie"><i></i></div>' +
      "</div>" +
      '<div class="nm-tor-fuss"><span class="nm-tor-weiter"></span><span class="nm-tor-zahl">000</span></div>';
    tor.querySelector(".nm-tor-name span").textContent = EINST.name;
    tor.querySelector(".nm-tor-weiter").textContent = EN ? "Skip" : "Überspringen";
    linie = tor.querySelector(".nm-tor-linie i");
    zahl = tor.querySelector(".nm-tor-zahl");
    document.body.appendChild(tor);
    wurzel.classList.add("nm-tor-da");

    tor.addEventListener("pointerdown", beenden);
    window.addEventListener("wheel", beenden, { passive: true });
    window.addEventListener("touchmove", beenden, { passive: true });
    document.addEventListener("keydown", taste);

    messen();
  }

  function taste(e) {
    if (e.key === "Shift" || e.key === "Control" || e.key === "Alt" || e.key === "Meta") return;
    beenden();
  }

  // --- Ladestand: Schriften, erstes großes Bild, ganze Seite ----------------

  function messen() {
    var schriften = false, bild = false, seite = document.readyState === "complete";
    try {
      document.fonts.ready.then(function () { schriften = true; });
    } catch (e) { schriften = true; }

    var erstes = document.querySelector(".hero-bild img, .seitenkopf picture img");
    if (!erstes || (erstes.complete && erstes.naturalWidth)) bild = true;
    else {
      erstes.addEventListener("load", function () { bild = true; });
      erstes.addEventListener("error", function () { bild = true; });
    }
    if (!seite) window.addEventListener("load", function () { seite = true; });

    var t0 = performance.now(), gezeigt = 0;

    function tick(jetzt) {
      if (fertig) return;
      var t = Math.max(0, jetzt - t0);
      var ziel = (schriften ? 0.3 : 0.05) + (bild ? 0.5 : Math.min(0.4, t / 3000)) + (seite ? 0.2 : 0);
      ziel = Math.min(ziel, t / EINST.mindestens);
      if (t > EINST.hoechstens) ziel = 1;
      gezeigt += (ziel - gezeigt) * 0.14;
      if (ziel >= 1 && gezeigt > 0.996) gezeigt = 1;

      linie.style.transform = "scaleX(" + gezeigt.toFixed(4) + ")";
      var n = Math.round(gezeigt * 100);
      zahl.textContent = (n < 10 ? "00" : n < 100 ? "0" : "") + n;

      if (gezeigt >= 1) {
        fertig = true;
        window.setTimeout(beenden, EINST.halten);
        return;
      }
      window.requestAnimationFrame(tick);
    }
    window.requestAnimationFrame(tick);
  }

  // --- Abgang --------------------------------------------------------------

  function beenden() {
    if (beendet) return;
    beendet = true;
    fertig = true;
    window.removeEventListener("wheel", beenden);
    window.removeEventListener("touchmove", beenden);
    document.removeEventListener("keydown", taste);

    if (!tor) { wurzel.classList.add("nm-start-fertig"); return; }

    tor.classList.add("geht");
    window.setTimeout(function () {
      tor.classList.add("oeffnet");
      // Die Seite beginnt, während die Flügel noch gehen.
      window.setTimeout(function () { wurzel.classList.add("nm-start-fertig"); }, 120);
      window.setTimeout(function () {
        if (tor && tor.parentNode) tor.parentNode.removeChild(tor);
        tor = null;
      }, EINST.oeffnen + 80);
    }, EINST.zurueck);
  }

  if (document.body) bauen();
  else document.addEventListener("DOMContentLoaded", bauen);
})();
