/* ==========================================================================
   AUFMASS — Startanimation der Startseite

   Die Seite misst beim Laden das Browserfenster aus: Eckmarken rahmen das
   Fenster ein, eine Maßlinie läuft von Rand zu Rand, die echte Breite wird
   eingetragen. Dann wandern die Eckmarken zum Foto und passen es ein, und
   der Hero wird aus der Vorzeichnung „ausgeführt“. Danach tritt die
   Maßlinie zurück und kommt nur wieder, wenn man das Fenster breiter oder
   schmäler zieht.

   Ablauf (erster Aufruf in der Sitzung, gesamt ca. 1,5 s):
      40 ms  Eckmarken rahmen das ganze Fenster ein
     200 ms  Maßlinie läuft von links nach rechts (540 ms)
     720 ms  rechte Begrenzung, Maß wird eingetragen
     820 ms  Eckmarken wandern zum Foto und werden dessen Marken
     860 ms  Hero wird aus der Vorzeichnung satt
    1450 ms  fertig, Linie wird grau
   Weitere Aufrufe in derselben Sitzung: nur die Linie, 0,4 s.

   Sicherungen:
   - Ohne JavaScript: keine Maßlinie, Seite steht fertig da.
   - Den Anfangszustand setzt das kleine Skript im <head> (Klasse
     aufmass-voll). Läuft es nicht (CSP, alter Browser), wird nichts
     abgedunkelt; hier läuft dann nur die Linie.
   - Das Kopfskript nimmt aufmass-voll nach 3 s in jedem Fall wieder weg.
   - Klick, Taste, Scrollen oder Wischen: sofort Endzustand.
   - Lädt die Seite langsam (Start nach 1,2 s) oder steht sie beim Laden
     nicht ganz oben, entfällt das Intro.
   - „Bewegung reduzieren“: Linie steht sofort fertig da.
   ========================================================================== */
(function () {
  "use strict";
  var d = document.documentElement;
  var hero = document.querySelector(".start-kopf");
  if (!hero) return;

  var bewegt = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var kannAnimieren = bewegt && typeof hero.animate === "function";
  var EASE = "cubic-bezier(0.22, 1, 0.36, 1)";
  var LAUF = "cubic-bezier(0.65, 0, 0.35, 1)";

  /* --- Maßlinie bauen ----------------------------------------------------- */
  var am = document.createElement("div");
  am.className = "aufmass";
  am.setAttribute("aria-hidden", "true");
  am.innerHTML =
    '<span class="am-hilfe am-links"></span><span class="am-hilfe am-rechts"></span>' +
    '<span class="am-linie"></span>' +
    '<span class="am-strich am-links"></span><span class="am-strich am-rechts"></span>' +
    '<span class="am-text"><span class="am-was">Aufmaß Ihres Fensters</span> <span class="am-wert"></span></span>';
  hero.insertBefore(am, hero.firstChild);

  var teil = function (s) { return am.querySelector(s); };
  var wert = teil(".am-wert");
  var breite = 0;

  function messen() {
    var b = d.clientWidth;
    if (b === breite) return false;
    breite = b;
    wert.textContent = String(b).replace(/\B(?=(\d{3})+(?!\d))/g, ".") + " px";
    return true;
  }
  messen();

  /* Nach dem Aufmaß tritt die Linie zurück (Klasse ist-weg). Beim Ziehen am
     Fenster kommt sie wieder und misst mit, danach tritt sie wieder zurück.
     Nur wenn sich die Breite ändert: Auf dem Handy feuert resize auch beim
     Ein- und Ausblenden der Adressleiste. */
  var bild = 0, ruhe = 0, weg = 0;
  function zuruecktreten(nach) {
    window.clearTimeout(weg);
    weg = window.setTimeout(function () { am.classList.add("ist-weg"); }, nach);
  }
  window.addEventListener("resize", function () {
    if (bild) return;
    bild = window.requestAnimationFrame(function () {
      bild = 0;
      if (!messen()) return;
      am.classList.remove("ist-weg");
      am.classList.add("ist-am-messen");
      window.clearTimeout(ruhe);
      ruhe = window.setTimeout(function () { am.classList.remove("ist-am-messen"); }, 700);
      zuruecktreten(1600);
    });
  });

  /* --- Intro -------------------------------------------------------------- */
  var voll = d.classList.contains("aufmass-voll");
  var laeufe = [], uhren = [], ecken = null, fertig = false;

  function nach(ms, fn) { uhren.push(window.setTimeout(fn, ms)); }
  function an(el, frames, opt) {
    opt.fill = "backwards";
    var a = el.animate(frames, opt);
    laeufe.push(a);
    return a;
  }

  function ende() {
    if (fertig) return;
    fertig = true;
    uhren.forEach(window.clearTimeout);
    laeufe.forEach(function (a) { try { a.finish(); } catch (e) {} });
    if (ecken) { ecken.remove(); ecken = null; }
    d.classList.remove("aufmass-voll", "aufmass-kurz", "aufmass-ecken", "aufmass-lauf");
    am.classList.add("ist-gemessen");
    zuruecktreten(1400);
    abmelden();
  }

  function sofort() {
    if (fertig) return;
    d.classList.add("aufmass-sofort");
    ende();
    window.requestAnimationFrame(function () {
      window.requestAnimationFrame(function () { d.classList.remove("aufmass-sofort"); });
    });
  }

  var ereignisse = ["pointerdown", "keydown", "wheel", "touchstart", "scroll"];
  function anmelden() {
    ereignisse.forEach(function (t) { window.addEventListener(t, sofort, { passive: true }); });
  }
  function abmelden() {
    ereignisse.forEach(function (t) { window.removeEventListener(t, sofort, { passive: true }); });
  }

  // Kein Intro: reduzierte Bewegung oder kein Web Animations API.
  if (!kannAnimieren) {
    d.classList.remove("aufmass-voll", "aufmass-kurz");
    am.classList.add("ist-gemessen", "ist-weg");
    return;
  }

  // Seite hat lange gebraucht oder steht nicht ganz oben (Neuladen mitten
  // auf der Seite): nicht noch zusätzlich warten lassen.
  if (voll && ((window.performance && performance.now() > 1200) || window.scrollY > 40)) {
    d.classList.add("aufmass-sofort");
    d.classList.remove("aufmass-voll");
    window.requestAnimationFrame(function () {
      window.requestAnimationFrame(function () { d.classList.remove("aufmass-sofort"); });
    });
    voll = false;
  }

  anmelden();

  if (!voll) {
    // Kurzfassung: nur die Linie, ca. 0,4 s. Nichts wird abgedunkelt.
    an(teil(".am-linie"), [{ transform: "scaleX(0)" }, { transform: "scaleX(1)" }],
       { duration: 380, easing: EASE });
    [".am-hilfe.am-links", ".am-strich.am-links", ".am-hilfe.am-rechts", ".am-strich.am-rechts"].forEach(function (s, i) {
      an(teil(s), [{ opacity: 0 }, { opacity: 1 }], { duration: 120, delay: i < 2 ? 0 : 300 });
    });
    an(teil(".am-text"), [{ opacity: 0 }, { opacity: 1 }], { duration: 200, delay: 220 });
    nach(420, ende);
    return;
  }

  // Volle Fassung
  d.classList.add("aufmass-lauf", "aufmass-ecken");

  an(teil(".am-hilfe.am-links"), [{ transform: "scaleY(0)" }, { transform: "scaleY(1)" }],
     { duration: 160, delay: 160, easing: EASE });
  an(teil(".am-strich.am-links"), [{ opacity: 0, transform: "rotate(-45deg) scaleX(0.3)" }, { opacity: 1, transform: "rotate(-45deg) scaleX(1)" }],
     { duration: 140, delay: 180, easing: EASE });
  an(teil(".am-linie"), [{ transform: "scaleX(0)" }, { transform: "scaleX(1)" }],
     { duration: 540, delay: 200, easing: LAUF });
  an(teil(".am-hilfe.am-rechts"), [{ transform: "scaleY(0)" }, { transform: "scaleY(1)" }],
     { duration: 160, delay: 720, easing: EASE });
  an(teil(".am-strich.am-rechts"), [{ opacity: 0, transform: "rotate(-45deg) scaleX(0.3)" }, { opacity: 1, transform: "rotate(-45deg) scaleX(1)" }],
     { duration: 140, delay: 730, easing: EASE });
  an(teil(".am-text"), [{ clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0 0 0)" }],
     { duration: 320, delay: 750, easing: EASE });

  // Eckmarken: Zuerst rahmen sie das ganze Fenster ein (das Fenster wird
  // zum Blatt), dann wandern sie zum Foto und werden dort zu dessen
  // Eckmarken. Am Ende übernehmen wieder die gezeichneten Marken aus
  // stil.css (gleiche Lage, gleiche Stärke).
  var rahmen = document.querySelector(".start-bild .blatt-bild");
  if (rahmen) {
    var r = rahmen.getBoundingClientRect();
    var vw = d.clientWidth, vh = window.innerHeight;
    var rand = vw < 600 ? 8 : 14, gross = vw < 600 ? 20 : 28, klein = 14;
    var sichtbar = r.top < vh - 80;            // Foto im ersten Bild?
    var farbe = getComputedStyle(d);
    var eisen = farbe.getPropertyValue("--eisen").trim() || "#943A2C";
    var grau = farbe.getPropertyValue("--graphit-3").trim() || "#6D6865";
    ecken = document.createElement("span");
    ecken.className = "am-ecken";
    ecken.setAttribute("aria-hidden", "true");
    ecken.style.setProperty("--am-rand", rand + "px");
    ecken.style.setProperty("--am-gross", gross + "px");
    var ziele = {
      ol: [r.left - rand, r.top - rand],
      or: [r.right - (vw - rand), r.top - rand],
      ul: [r.left - rand, r.bottom - (vh - rand)],
      ur: [r.right - (vw - rand), r.bottom - (vh - rand)]
    };
    ["ol", "or", "ul", "ur"].forEach(function (k, i) {
      var s = document.createElement("span");
      s.className = "am-ecke am-" + k;
      ecken.appendChild(s);
      an(s, [{ opacity: 0, transform: "scale(0.4)" }, { opacity: 1, transform: "scale(1)" }],
         { duration: 240, delay: 40 + i * 30, easing: EASE });
      var z = ziele[k];
      var seiten = { ol: ["Top", "Left"], or: ["Top", "Right"], ul: ["Bottom", "Left"], ur: ["Bottom", "Right"] }[k];
      var von = { transform: "translate(0,0)", width: gross + "px", height: gross + "px", borderColor: eisen };
      var bis = { transform: "translate(" + z[0] + "px," + z[1] + "px)", width: klein + "px", height: klein + "px", borderColor: grau };
      seiten.forEach(function (seite) { von["border" + seite + "Width"] = "2px"; bis["border" + seite + "Width"] = "1px"; });
      var hin = sichtbar ? [von, bis] : [{ opacity: 1 }, { opacity: 0 }];
      laeufe.push(s.animate(hin, { duration: sichtbar ? 580 : 300, delay: 820, easing: EASE, fill: "forwards" }));
    });
    document.body.appendChild(ecken);
  }

  nach(860, function () { d.classList.remove("aufmass-voll"); });
  nach(1450, ende);
})();
