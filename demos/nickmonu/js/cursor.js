/* ==========================================================================
   ZEIGER — nachziehender Ring plus Marke in Messing

   - Erscheint erst bei der ersten Mausbewegung. Vorher bleibt der normale
     Zeiger, sonst sitzt ein Ring verloren in der Bildschirmmitte.
   - Die Größe ändert sich über transform (scale), nicht über width/height:
     das rechnet die Grafikkarte, nicht das Layout. Der Strich bleibt dabei
     1 px dick (vector-effect: non-scaling-stroke).
   - Auf Touch-Geräten und bei „Bewegung reduzieren“ passiert nichts.
   ========================================================================== */

(function () {
  "use strict";

  if (typeof window === "undefined" || typeof document === "undefined") return;
  if (!window.matchMedia("(pointer: fine) and (hover: hover)").matches) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var EN = (document.documentElement.lang || "").toLowerCase().indexOf("en") === 0;

  var GROESSE = 88;                        // volle Größe (Bild, Video)
  var STUFE = { normal: 14 / GROESSE, link: 44 / GROESSE, media: 1, text: 0 };
  var HELL = "#EFE9DF", MESSING = "#BBA883";
  var MARKE = 11;

  // --- Ring ---------------------------------------------------------------

  var ring = document.createElement("div");
  ring.className = "nm-cursor";
  ring.setAttribute("aria-hidden", "true");
  ring.style.cssText =
    "position:fixed;left:0;top:0;width:" + GROESSE + "px;height:" + GROESSE + "px;" +
    "margin:" + (-GROESSE / 2) + "px 0 0 " + (-GROESSE / 2) + "px;" +
    "pointer-events:none;z-index:2147483000;opacity:0;" +
    "transition:opacity 180ms linear;will-change:transform;";
  ring.innerHTML =
    '<svg viewBox="0 0 88 88" width="88" height="88" style="position:absolute;inset:0;overflow:visible">' +
      '<circle cx="44" cy="44" r="43.5" fill="' + HELL + '" fill-opacity="0" stroke="' + HELL + '" ' +
      'stroke-width="1" vector-effect="non-scaling-stroke" style="transition:fill-opacity 180ms linear"/>' +
    "</svg>" +
    '<span style="position:absolute;inset:0;display:grid;place-items:center;' +
      "font:400 12px/1 'Instrument Sans',sans-serif;letter-spacing:0.08em;text-transform:uppercase;" +
      "color:" + HELL + ';opacity:0;transition:opacity 160ms linear">' + (EN ? "View" : "Ansehen") + "</span>";
  var kreis = ring.querySelector("circle");
  var beschriftung = ring.querySelector("span");

  // --- Marke (Kreuz in Messing, folgt ohne Verzögerung) -------------------

  var marke = document.createElement("div");
  marke.className = "nm-cursor";
  marke.setAttribute("aria-hidden", "true");
  marke.style.cssText =
    "position:fixed;left:0;top:0;width:0;height:0;pointer-events:none;" +
    "z-index:2147483001;opacity:0;transition:opacity 160ms linear;will-change:transform;";
  var kreuz = document.createElement("div");
  kreuz.style.cssText =
    "position:absolute;left:0;top:0;width:" + MARKE + "px;height:" + MARKE + "px;" +
    "transform:translate(-50%,-50%) rotate(45deg);" +
    "transition:transform 200ms cubic-bezier(0.23,1,0.32,1),opacity 160ms linear;";
  function strich(w, h) {
    var s = document.createElement("div");
    s.style.cssText =
      "position:absolute;left:50%;top:50%;border-radius:1px;background-color:" + MESSING + ";" +
      "width:" + w + "px;height:" + h + "px;transform:translate(-50%,-50%);";
    return s;
  }
  kreuz.appendChild(strich(MARKE, 1.5));
  kreuz.appendChild(strich(1.5, MARKE));
  marke.appendChild(kreuz);

  document.body.appendChild(ring);
  document.body.appendChild(marke);

  // --- Zustand ------------------------------------------------------------

  var wurzel = document.documentElement;
  var x = 0, y = 0, rx = 0, ry = 0;
  var s = STUFE.normal, sZiel = STUFE.normal;
  var modus = "normal";
  var aktiv = false;      // erst nach der ersten Bewegung
  var sichtbar = false;

  function anwenden() {
    sZiel = STUFE[modus];
    kreis.setAttribute("fill-opacity", modus === "link" ? "0.08" : "0");
    beschriftung.style.opacity = modus === "media" ? "1" : "0";
    kreuz.style.opacity = (modus === "media" || modus === "text") ? "0" : "1";
    kreuz.style.transform = "translate(-50%,-50%) rotate(" + (modus === "link" ? 0 : 45) + "deg)";
    wurzel.style.cursor = modus === "text" ? "" : "none";
  }

  function zeigen(an) {
    sichtbar = an;
    ring.style.opacity = an ? "1" : "0";
    marke.style.opacity = an ? "1" : "0";
  }

  window.addEventListener("pointermove", function (e) {
    if (e.pointerType && e.pointerType !== "mouse") return;
    x = e.clientX; y = e.clientY;
    if (!aktiv) {
      aktiv = true;
      rx = x; ry = y;
      anwenden();
      zeigen(true);
      window.requestAnimationFrame(tick);
    } else if (!sichtbar) {
      zeigen(true);
    }
    var ziel = e.target, naechster = "normal";
    if (ziel && typeof ziel.closest === "function") {
      if (ziel.closest('input, textarea, select, [contenteditable="true"], iframe')) naechster = "text";
      else if (ziel.closest('[data-cursor="media"]')) naechster = "media";
      else if (ziel.closest('a, button, label, [role="button"], [data-cursor="link"]')) naechster = "link";
    }
    if (naechster !== modus) { modus = naechster; anwenden(); }
  }, { passive: true });

  document.documentElement.addEventListener("pointerleave", function () { zeigen(false); });
  window.addEventListener("blur", function () { zeigen(false); });

  // --- Die Marke bleibt liegen -------------------------------------------
  // Nach jedem Klick bleibt kurz eine Marke an der Stelle und verblasst —
  // wie Spielmarken auf einer Bühne nach der Probe.

  function markeSetzen(px, py) {
    var m = document.createElement("div");
    m.className = "nm-cursor";
    m.setAttribute("aria-hidden", "true");
    m.style.cssText =
      "position:fixed;left:" + px + "px;top:" + py + "px;width:" + MARKE + "px;height:" + MARKE + "px;" +
      "margin:" + (-MARKE / 2) + "px 0 0 " + (-MARKE / 2) + "px;pointer-events:none;z-index:2147482999;" +
      "transform:rotate(45deg) scale(0.7);opacity:0;" +
      "transition:transform 1900ms cubic-bezier(0.23,1,0.32,1),opacity 1900ms cubic-bezier(0.4,0,0.6,1);";
    m.appendChild(strich(MARKE, 1.5));
    m.appendChild(strich(1.5, MARKE));
    document.body.appendChild(m);
    window.requestAnimationFrame(function () {
      m.style.opacity = "0.85";
      m.style.transform = "rotate(45deg) scale(1)";
      window.setTimeout(function () {
        m.style.opacity = "0";
        m.style.transform = "rotate(45deg) scale(1.55)";
      }, 90);
    });
    window.setTimeout(function () { if (m.parentNode) m.parentNode.removeChild(m); }, 2100);
  }

  document.addEventListener("pointerdown", function (e) {
    if (e.pointerType !== "mouse" || !aktiv) return;
    markeSetzen(e.clientX, e.clientY);
  }, { passive: true });

  // --- Schleife -----------------------------------------------------------

  function tick() {
    rx += (x - rx) * 0.18;
    ry += (y - ry) * 0.18;
    s  += (sZiel - s) * 0.2;
    ring.style.transform = "translate3d(" + rx.toFixed(2) + "px," + ry.toFixed(2) + "px,0) scale(" + s.toFixed(4) + ")";
    marke.style.transform = "translate3d(" + x + "px," + y + "px,0)";
    window.requestAnimationFrame(tick);
  }
})();
